# -*- coding: utf-8 -*-
"""
This Module is ppe
Example:
    $python video_demo.py
Author: Ming'en Zheng
"""
import os
import time
from multiprocessing import Process, Queue, Value
import queue
import numpy as np
import tensorflow as tf
import cv2
import argparse
import requests
from distutils.version import StrictVersion
import visualization_utils as vis_utils
import config
import base64


if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
    raise ImportError('Please upgrade your TensorFlow installation to v1.12.*')


def load_model(inference_model_path):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(inference_model_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    return detection_graph


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(image, sess, tensor_dict):
    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

    output_dict = sess.run(tensor_dict, feed_dict={image_tensor: image})

    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]

    return output_dict


def is_wearing_hardhat(person_box, hardhat_box, intersection_ratio):
    xA = max(person_box[0], hardhat_box[0])
    yA = max(person_box[1], hardhat_box[1])
    xB = min(person_box[2], hardhat_box[2])
    yB = min(person_box[3], hardhat_box[3])

    interArea = max(0, xB - xA ) * max(0, yB - yA )

    hardhat_size = (hardhat_box[2] - hardhat_box[0]) * (hardhat_box[3] - hardhat_box[1])

    if interArea / hardhat_size > intersection_ratio:
        return True
    else:
        return False


def is_wearing_vest(person_box, vest_box, vest_intersection_ratio):
    xA = max(person_box[0], vest_box[0])
    yA = max(person_box[1], vest_box[1])
    xB = min(person_box[2], vest_box[2])
    yB = min(person_box[3], vest_box[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)

    vest_size = (vest_box[2] - vest_box[0]) * (vest_box[3] - vest_box[1])

    if interArea / vest_size > vest_intersection_ratio:
        return True
    else:
        return False


def is_wearing_hardhat_vest(hardhat_boxes, vest_boxes, person_box):
    hardhat_flag = False
    vest_flag = False
    hardhat_intersection_ratio = 0.6
    vest_intersection_ratio = 0.6

    for hardhat_box in hardhat_boxes:
        hardhat_flag = is_wearing_hardhat(person_box, hardhat_box, hardhat_intersection_ratio)
        if hardhat_flag:
            break

    for vest_box in vest_boxes:
        vest_flag = is_wearing_vest(person_box, vest_box, vest_intersection_ratio)
        if vest_flag:
            break

    return hardhat_flag, vest_flag


def post_message_process(run_flag, message_queue):
    
    while run_flag.value:
        try:
            camera_id, output_dict, image, min_score_thresh = message_queue.get(block=True, timeout=5)
            post_message(camera_id, output_dict, image, min_score_thresh)
        except queue.Empty:
            continue


def post_message(camera_id, output_dict, image, min_score_thresh):
    message = dict()
    message["timestamp"] = int(time.time() * 1000)
    message["cameraId"] = camera_id

    image_info = {}
    image_info["height"] = image.shape[0]
    image_info["width"] = image.shape[1]
    image_info["format"] = "jpeg"

    success, encoded_image = cv2.imencode('.jpg', image)
    content = encoded_image.tobytes()
    image_info["raw"] = base64.b64encode(content).decode('utf-8')

    message["image"] = image_info

    detection_scores = np.where(output_dict["detection_scores"] > min_score_thresh, True, False)

    detection_boxes = output_dict["detection_boxes"][detection_scores]
    detection_classes = output_dict["detection_classes"][detection_scores]

    hardhat_boxes = detection_boxes[np.where(detection_classes == 1)]
    vest_boxes = detection_boxes[np.where(detection_classes == 2)]
    person_boxes = detection_boxes[np.where(detection_classes == 3)]

    persons = []
    for person_box in person_boxes:
        person = dict()
        person["hardhat"], person["vest"] = is_wearing_hardhat_vest(hardhat_boxes, vest_boxes, person_box)
        persons.append(person)

    message["persons"] = persons
   
    if len(persons) == 0:
        return False

    print(message["persons"])
    try:
        headers = {'Content-type': 'application/json'}
        if len(persons):
            result = requests.post(config.detection_api, json=message, headers=headers)
            print(result)
            return True
    except requests.exceptions.ConnectionError:
        print("Connect to backend failed")
    return False


def video_processing(graph, category_index, video_file_name, show_video_window, camera_id, run_flag, message_queue):
    cap = cv2.VideoCapture(video_file_name)

    if show_video_window:
        cv2.namedWindow('ppe', cv2.WINDOW_NORMAL)
        if config.display_full_screen:
            cv2.setWindowProperty('ppe', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.setWindowProperty('ppe', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

    if (config.capture_image_width, config.capture_image_height) in config.supported_video_resolution:
        print("video_processing:", "supported video resoulution")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.capture_image_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.capture_image_height)

    with graph.as_default():
        print("video_processing:", "default tensorflow graph")
        ops = tf.get_default_graph().get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in [
            'num_detections', 'detection_boxes', 'detection_scores',
            'detection_classes', 'detection_masks'
        ]:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                    tensor_name)
        with tf.Session() as sess:
            print("video_processing:", "tensorflow session")
            send_message_time = time.time()
            frame_counter = 0
            while True:
                ret, frame = cap.read()

                if config.input_type.lower() == "file":
                    frame_counter += 1
                    if frame_counter == int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
                        frame_counter = 0
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue

                if frame is None:
                    print("video_processing:", "null frame")
                    break

                image_expanded = np.expand_dims(frame, axis=0)
                output_dict = run_inference_for_single_image(image_expanded, sess, tensor_dict)

                vis_utils.visualize_boxes_and_labels_on_image_array(
                    frame,
                    output_dict['detection_boxes'],
                    output_dict['detection_classes'],
                    output_dict['detection_scores'],
                    category_index,
                    instance_masks=output_dict.get('detection_masks'),
                    use_normalized_coordinates=True,
                    line_thickness=4)

                if time.time() - send_message_time > config.message_send_interval / 1000.0:
                    resized_frame = cv2.resize(frame, dsize=(config.storage_image_width, config.storage_image_height))
                    try:
                        message_queue.put_nowait((camera_id, output_dict, resized_frame, config.object_confidence_threshold))
                    except queue.Full:
                        print("message queue is full")
                    else:
                        send_message_time = time.time()

                if show_video_window:
                    resized_frame = cv2.resize(frame, dsize=(config.display_window_width, config.display_window_height))
                    cv2.imshow('ppe', resized_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        run_flag.value = 0
                        break

    print("video_processing:", "releasing video capture")
    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="Hardhat and Vest Detection", add_help=True)
    parser.add_argument("--model_dir", type=str, required=True, help="path to model directory")
    parser.add_argument("--video_file_name", type=str, required=True, help="path to video file, or camera device, i.e /dev/video1")
    parser.add_argument("--show_video_window", type=int, required=True, help="the flag for showing the video window, 0 is not dispaly, 1 display")
    parser.add_argument("--camera_id", type=str, required=True, help="camera identifier")
    args = parser.parse_args()

    frozen_model_path = os.path.join(args.model_dir, "frozen_inference_graph.pb")
    if not os.path.exists(frozen_model_path):
        print("frozen_inference_graph.db file is not exist in model directory")
        exit(-1)
    print("loading model")
    graph = load_model(frozen_model_path)
    category_index = {1: {'id': 1 , 'name': 'hardhat'},
                      2: {'id': 2, 'name': 'vest'},
                      3: {'id': 3, 'name': 'person'}}
    
    print("start message queue")
    run_flag = Value('i', 1)
    message_queue = Queue(1)
    p = Process(target=post_message_process, args=(run_flag, message_queue))
    p.start()
    print("video processing")
    video_processing(graph, category_index, args.video_file_name, args.show_video_window, args.camera_id, run_flag, message_queue)
    p.join()

if __name__ == '__main__':
    main()

