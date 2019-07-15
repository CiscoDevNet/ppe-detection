# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import base64
import json
import os
import uuid
from datetime import datetime
from multiprocessing import Queue

from flask import Response, abort, jsonify, request

from common import logger
from common.util import current_timestamp_ms
from config import config
from db.detection_dao import DetectionDao
from endpoints.app import socketio
from endpoints.policy import policy_dao
from endpoints.var import abnormal_count_map, redis_cli
from models.detection import Detection
from models.error import Error
from services.spark import Spark

detection_dao = DetectionDao()

msg_queue = Queue(config.notification["queueSize"])

spark_cli = Spark(config)


MSG_TEMPLATE = """
### ppe demo
**Alert** at **{point}** at {time}
> tatal_person={total_person} without_hardhat={without_hardhat} without_vest={without_vest} without_both={without_both}
"""


def _construct_msg(ts, point, total_person, without_hardhat, without_vest, without_both):
    t = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")
    return MSG_TEMPLATE.format(
        time=t, point=point, total_person=total_person, without_hardhat=without_hardhat, without_vest=without_vest, without_both=without_both)


def _get_detection(id):
    detection = detection_dao.get(id)
    if not detection:
        abort(404)
    else:
        return jsonify(detection.to_json())


def _delete_detection(id):
    detection = detection_dao.remove(id)
    if not detection:
        return Response(None, status=404, mimetype='application/json')
    else:
        return Response(None, status=204, mimetype='application/json')


def _update_detection(id):
    detection = Detection(request.json)
    if not detection:
        abort(404)
    else:
        detection.update(request.json)
        detection.id = id
        try:
            detection.validate()
        except ValueError as e:
            abort(400, str(e))
        else:
            return jsonify(detection_dao.save(detection).to_json())


def _create_detection():
    if not request.headers.get("Content-Type").startswith("application/json"):
        return json.dumps(Error(415, "Content-Type must be application/json").to_json()), 415, {'Content-Type': 'application/json'}

    detection = Detection(request.json)
    detection.id = str(uuid.uuid1())
    try:
        detection.validate()
    except ValueError as e:
        abort(400, str(e))
    detection.createdAt = current_timestamp_ms()
    detection.updatedAt = detection.createdAt

    # upload the file to /images, now just do it here
    file_name = detection.id + "." + detection.image["format"]
    file_path = os.path.join(config.app["imageDir"], file_name)
    try:
        fh = open(file_path, "wb")
        fh.write(base64.b64decode(detection.image["raw"]))
        fh.close()
    except BaseException as e:
        logger.error(str(e))
        return json.dumps(Error(400, "raw data is not invalid base64").to_json()), 400, {'Content-Type': 'application/json'}
    detection.image["url"] = config.app["imageRootUrl"] + file_name
    detection.image["raw"] = ""
    # redis
    redis_cli.setex(file_name, config.app["imageTTL"], "")
    # send notification
    without_hardhat = len(list(filter(lambda p: not p["hardhat"], detection.persons)))
    without_vest = len(list(filter(lambda p: not p["vest"], detection.persons)))
    without_both = len(list(filter(lambda p: not p["vest"] and not p["hardhat"], detection.persons)))
    status = 0
    if without_hardhat > 0 or without_vest > 0 or without_both > 0:
        if without_both > 0:
            status = 3
        elif without_hardhat > 0:
            status = 2
        else:
            status = 1
        d = detection
        msg = _construct_msg(d.timestamp, d.cameraId, len(d.persons), without_hardhat - without_both, without_vest - without_both, without_both)
        files = [d.image["url"]]
        if policy_dao.notificationEnabled:
            logger.info("send notification is enabled")
            global abnormal_count_map
            if abnormal_count_map.get(detection.cameraId) is None:
                abnormal_count_map[detection.cameraId] = 0
            else:
                abnormal_count_map[detection.cameraId] += 1
            logger.info("current abnormal_count_map is {}".format(abnormal_count_map))
            if abnormal_count_map[detection.cameraId] > policy_dao.notificationNumThreshold:
                logger.info("above threshold, will send notification")
                logger.info("files are {}".format(files))
                abnormal_count_map[detection.cameraId] = 0
                if config.notification["syncMode"]:
                    logger.info("send msg in sync mode")
                    spark_cli.send_msg(msg, files)
                else:
                    logger.info("send msg in async mode")
                    msg_queue.put((msg, files))
    detection.status = status
    result = detection_dao.save(detection).to_json()
    # push to frontend through socketio
    logger.info("sending data through socketio")
    socketio.emit("detection", result, broadcast=True)
    return jsonify(result)


def _list_detections():
    if request.args.get("status"):
        status_args = request.args["status"].split(",")
        if len(status_args) > 1:
            result = []
            request_args = request.args.to_dict()
            for arg in status_args:
                request_args["status"] = arg
                result.extend([m.to_json() for m in detection_dao.find(request_args)])
            return jsonify(result)

    return jsonify([m.to_json() for m in detection_dao.find(request.args)])


class DetectionEndpoint:
    def __init__(self, route):
        route.get("/v1/detections/{id}")\
            .description("retrieve a specific Detection")\
            .tags("detections")\
            .parameter(name="id", required=True, description="detection id")\
            .returns(Detection, 200)\
            .returns(None, 401, 500)\
            .to(_get_detection)

        route.delete("/v1/detections/{id}")\
            .description("delete a specific Detection")\
            .tags("detections")\
            .auth_required()\
            .parameter(name="id", required=True, description="detection id")\
            .returns(None, 204, 401, 500)\
            .to(_delete_detection)

        route.put("/v1/detections/{id}")\
            .description("update a specific Detection")\
            .tags("detections")\
            .auth_required()\
            .parameter(name="id", required=True, description="detection id")\
            .returns(Detection, 200)\
            .returns(None, 401, 500)\
            .reads(Detection)\
            .to(_update_detection)

        route.post("/v1/detections")\
            .description("create new Detection")\
            .tags("detections")\
            .auth_required()\
            .returns(Detection, 200)\
            .returns(None, 401, 500)\
            .reads([Detection])\
            .to(_create_detection)

        route.get("/v1/detections")\
            .description("list all Detections")\
            .tags("detections")\
            .returns([Detection], 200)\
            .returns(None, 401, 500)\
            .parameter("limit", "integer", "query", "max items to return at one time")\
            .parameter("offset", "string", "query", "starting offset")\
            .to(_list_detections)
