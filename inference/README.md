# PPE_Inference
Hardhat, Vest and Person Detection to keep construction work safety.

## Requirements
1. python3
2. tensorflow-gpu >= 1.12
3. opencv

## Run
python3 video_demo.py --model_dir=xxx  --video_file_name=xxx --show_video_window=xxx

* model_dir: the path to model directory<br>
* video_file_name: input video file name or usb camera device name, such as "/dev/video0"<br>
* show_video_window: the flag to show video window, the options are {0, 1}

## Run as docker image

* get the image `ppe-client`. Either build your own or get an existing one.
* get the model data, and place it under ./model
```
find and download the newest frozen_inference_graph.pb from https://cisco.app.box.com/folder/77461537168
ls ./model
frozen_inference_graph.pb
```
* execute the file `./run.sh`
    * if it failed, check if the variables are right, like `/dev/video0`, `echo $DISPLAY`
* then the screen should pop up
* If you want to run with more jetsons, please change the `camera_id` to different values.
* if you cannot see the screen, use the below trick, and change DISPLAY in docker run to ip-of-machine:0
```
apt-get install socat
export DISPLAY=:0
xhost +
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CONNECT:/tmp/.X11-unix/X0
```
## Tips

1. The container will be stuck at "Adding visible gpu devices:0 " for several minutes.
2. If you meet error when running it in jetson directly, try to use ssh to login and execute

## Build docker image

build env: jetson tx2 or nano, so you need to scp this repo to it.

### prerequisite

* Use the libcudnn newer libcudnn this will be copied to the image
```
mkdir libcudnn
cp /usr/lib/aarch64-linux-gnu/libcudnn* ./libcudnn/
```

### Option1: use a prebuilt base image, preferred
```
docker build . -t containers.cisco.com/cocreate/ppe-inference-client
```

### Option2: use a prebuilt base image

This take shorter time, and verified in Shanghai Lab.

* Download a prebuild image from box, and copy it to your build machine, eg Jetson tx2.
```
https://cisco.app.box.com/folder/75665413558
```
* Load the image
```
docker load -i emotion.gpu.tar
```
* Build the base image
```
docker build . -f Dockerfile.ppebase -t ppe-base
```
* Build ppe-client
```
docker build . -t ppe-client
```

### Option3: build from scretch

The build time depends on your network speed, may take quite some time.
```
docker build . -f Dockerfile.full -t ppe-client
```
