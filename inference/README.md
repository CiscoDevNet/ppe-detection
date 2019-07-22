# PPE_Inference
Hardhat, Vest and Person Detection to keep construction work safety.

## Requirements
1. python3
2. tensorflow-gpu >= 1.12
3. opencv

## Run
python3 video_demo.py --model_dir=xxx  --video_file_name=xxx --show_video_window=xxx --camera_id=xxx

* model_dir: the path to model directory<br>
* video_file_name: input video file name or usb camera device name, such as "/dev/video0"<br>
* show_video_window: the flag to show video window, the options are {0, 1}
* camera_id: camera identifier, represent deployed camera

