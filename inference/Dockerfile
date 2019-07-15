FROM containers.cisco.com/cocreate/ppe-base

WORKDIR /opt/ppe

RUN pip install requests

COPY *.py ./

CMD python3 video_demo.py --model_dir=./model  --video_file_name=/dev/video0 --show_video_window=0 --camera_id=default
