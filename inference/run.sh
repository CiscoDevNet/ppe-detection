#! /bin/bash

modprobe uvcvideo nodrop=1 timeout=6000

DISPLAY=:0 xhost +
docker run --name exe-ppe-demo \
            --privileged \
            --device=/dev/nvhost-ctrl \
            --device=/dev/nvhost-ctrl-gpu \
            --device=/dev/nvhost-prof-gpu \
            --device=/dev/nvmap \
            --device=/dev/nvhost-gpu \
            --device=/dev/nvhost-vic \
            --device=/dev/nvhost-as-gpu \
            -v /usr/lib/aarch64-linux-gnu/tegra:/usr/lib/aarch64-linux-gnu/tegra \
            -v ./model:/opt/ppe/model \
            --device=/dev/video0 \
            -e "DISPLAY=:0" \
            -e "PPE_MESSAGE_SEND_INTERVAL=10000" \
            -e "PPE_OBJECT_CONFIDENCE_THRESHOLD=0.5" \
            -e "PPE_CAPTURE_IMAGE_WIDTH=640" \
            -e "PPE_CAPTURE_IMAGE_HEIGHT=480" \
            -e "PPE_DISPLAY_FULL_SCREEN=False" \
            -e "PPE_DISPLAY_WINDOW_WIDTH=640" \
            -e "PPE_DISPLAY_WINDOW_HEIGHT=480" \
            -e "PPE_INPUT_TYPE=camera" \
            -e "PPE_DETECTION_URL=http://ppe-demo.devnetcloud.com/v1/detections" \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -it containers.cisco.com/cocreate/ppe-inference-client python3 video_demo.py --model_dir=./model  --video_file_name=/dev/video0 --show_video_window=0 --camera_id=camera1
