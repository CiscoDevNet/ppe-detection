# Installation & Usage

## prerequisite

* docker
* docker-compose

## Installation

* Get the ppe-release-$date.tar.gz
* extract to some dir
```
mkdir -p ./ppe-release
tar zxvf ppe-release-$date.tar -C ./ppe-release
```
* get the whole solution running/upgrade(a simple k3s is embed)
```
cd ./ppe-release
docker load -i ppe-backend.tar
docker load -i ppe-frontend.tar
docker-compose up -d
```
Now you have everything running
* destroy the whole cluster
```
docker-compose down --volumes
```
* If the release need database schema change, you need to delete the database
```
rm -rf .data/cassandra
```

## Usage

* The frontend UI:  http://127.0.0.1:9031
* The backend API:  http://127.0.0.1:9030

## environments

### shanghai Lab

```
http://10.140.92.58:8080/admin
```

### AWS

```
http://ppe-demo.devnetcloud.com/admin
https://ppe-demo.devnetcloud.com/admin
http://aiml-ppe-detection-lb-1883461432.us-west-2.elb.amazonaws.com
```
