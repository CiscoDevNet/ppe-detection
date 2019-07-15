#  For developer only

## package process

### build ppe-backend

* build image
```
docker pull containers.cisco.com/cocreate/ppe-backend
```
If you want change something, and build your own image, try this:
```
git clone https://wwwin-github.cisco.com/DevNet/ppe-backend
make changes
docker build . -t containers.cisco.com/cocreate/ppe-backend
```
* save this image
```
docker save containers.cisco.com/cocreate/ppe-backend -o ppe-backend.tar
```

### build ppe-frontend

This is a the frontend we will use for this demo.

ppe-frontend use the UI boilplate designed for DevNet website, so there will
be extra work to make it as a local Docker image.

* build image
Because Drone.io we are using does not support multi-stage build, if we want to
build a image in smaller size, so we have to build the image manually
```
git clone https://wwwin-github.cisco.com/DevNet/ppe-frontend
make changes
docker build . -f Dockerfile -t ppe-frontend
```
* save this image
```
docker save ppe-frontend -o ppe-frontend.tar
```

### put all the things together

in a shell script `package.sh`
```
rm -rf release
mkdir release
mv ppe-backend.tar release/
mv ppe-frontend.tar release/
cp docker-compose.yaml release/
cp nginx.conf release/
cp README.md release/
cp release-note.md release/
tar zcvf ppe-release-0417.tar.gz -C release .
```
copy to the deployment machine:
```
scp ppe-release-* ppe:/tmp/
```
