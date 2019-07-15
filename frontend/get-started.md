# get started

## environments

#### Lab
* backend
```
http://10.140.92.58:8080/v1/detections
http://10.140.92.58:8080/v1/images/{imageId}
```
* frontend debug UI
```
http://10.140.92.58:8080/admin
```


## tutorial

* build the backend docker image
```
git clone https://wwwin-github.cisco.com/DevNet/ppe-backend
cd ppe-backend
docker build . -t containers.cisco.com/cocreate/ppe-backend
```

* start backend service with docker-compose
```
docker-compose up -d
```

* add backend IP to /etc/hosts
```
# if backend in local machine
127.0.0.1 ppe-backend
# if backend in Shanghai Lab machine
10.140.92.58 ppe-backend
```
* (optional) If you dont use local backend, change the config to meet your need.
```
export REACT_APP_BACKEND_API_URL=http://localhost:9030
export REACT_APP_BACKEND_SOCKETIO_URL=http://localhost:9030
```

* start app
```
npm start
```

* test app
```
npm test
```

* simulte checkin checkout with API.

```
POST localhost:7030/v1/detections

{
    "cameraId": "camera1",
    "timestamp": 1558506692000,  // timestamp in ms
    "persons": [
      {
        "hardhat": true,
        "vest": true
      },
      {
        "hardhat": false,
        "vest": true
      }
    ],
    "image": {
      "height": 200,
      "width": 300,
      "format": "jpeg",
      "raw": "base64 encoded image bytes"
    },
}
```
```
GET localhost:7030/v1/detections
query:

cameraId=camera1
status=1
limit=20 // default limit is 10

status=
0: all valid
1: only have someone without vest
2: only have someone without hardhat
3: have someone without vest and hardhat

response:

[
    {
        "cameraId": "camera2",
        "createdAt": "Wed, 22 May 2019 06:31:37 GMT", // this is for internal use
        "id": "uuid20",
        "image": {
            "format": "jpeg",
            "height": 443,
            "raw": "",
            "url": "http://ppe-backend:7030/v1/images/pic-1-0-2.jpeg",
            "width": 804
        },
        "persons": [
            {
                "hardhat": true,
                "vest": true
            }
        ],
        "status": 0,
        "timestamp": 1558506192000,
        "updatedAt": 1558506697000 // this is for internal use
    }
]
```


* Get image API

```
localhost:7030/v1/images/{id}
```

* socketIO event
```
key: detection
value:
    {
        "cameraId": "camera2",
        "createdAt": "Wed, 22 May 2019 06:31:37 GMT", // this is for internal use
        "id": "uuid20",
        "image": {
            "format": "jpeg",
            "height": 443,
            "raw": "",
            "url": "http://ppe-backend:7030/v1/images/pic-1-0-2.jpeg",
            "width": 804
        },
        "persons": [
            {
                "hardhat": true,
                "vest": true
            }
        ],
        "status": 0,
        "timestamp": 1558506192000,
        "updatedAt": 1558506697000 // this is for internal use
    }
```


* build a production ready image

```
docker build . -f Dockerfile.prod -t ppe-frontend-production
```
