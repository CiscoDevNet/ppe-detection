# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import json
import os


class Config:
    def __init__(self, args):
        for k, v in args.items():
            if isinstance(v, dict):
                self.__dict__[k] = Config(v)
            else:
                self.__dict__[k] = v

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __getitem__(self, name):
        obj = self.__dict__.get(name)
        if isinstance(obj, Config):
            return obj
        if obj is not None:
            return obj
        return os.getenv(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __setitem__(self, name, value):
        self.update({name: value})

    def get(self, name, default_value):
        ret = self.__getattr__(name)
        if ret is None:
            ret = default_value
        return ret

    def to_json(self):
        ret = {}
        for k, v in self.__dict__.items():
            if isinstance(v, Config):
                ret[k] = v.to_json()
            else:
                ret[k] = v

        return ret

    def update(self, o):
        def _update(obj, c):
            for k, v in c.items():
                t = obj.get(k)
                if isinstance(t, Config):
                    _update(t.__dict__, v)
                elif isinstance(v, dict):
                    obj[k] = Config(v)
                else:
                    obj[k] = v

        _update(self.__dict__, o)


corsFileList = os.getenv("CORS_WHITELIST_FILEPATH", "/etc/cors/cors.list")

corsList = []
if os.path.isfile(corsFileList):
    f = open(corsFileList, "r")
    corsList = f.readlines()
    for c in corsList:
        corsList.append(c.strip())
else:
    corsList = [
        "https://(.+)?.cisco.com",
        "https://(.+)?.devnetcreate.io",
        "https://(.+)?.devnetcloud.com",
        "https://local.cisco.com:3002",
        "http://{}:{}".format(os.getenv("PPE_BACKEND_HOST", "0.0.0.0"), os.getenv("PPE_BACKEND_PORT", "5000"))
    ]

config = Config({
    "serviceName": "ppe-backend",
    "serviceHost": os.getenv("PPE_BACKEND_HOST", "0.0.0.0"),
    "servicePort": int(os.getenv("PPE_BACKEND_PORT", "7030")),
    "corsList": corsList,
    "vault": {
        "apiVersion": "v1",
        "endpoint": os.getenv("PPE_BACKEND_ENCRYPTION_BASEURL", "http://127.0.0.1:8200"),
        "token": os.getenv("PPE_BACKEND_ENCRYPTION_AUTH_TOKEN", "5520878e-3b1e-f265-0ef6-8bc30317d1b3"),
        "defaultKey": os.getenv("PPE_BACKEND_ENCRYPTION_DEFAULT_KEY", "default_key"),
        "jwtSecretValue": os.getenv("JWT_SECRET", ""),
    },
    "cassandra": {
        "contactPoints": os.getenv("PPE_BACKEND_CASSANDRA_HOSTS", "127.0.0.1").split(","),
        "keyspace": os.getenv("PPE_BACKEND_CASSANDRA_KEYSPACE", "ppe"),
        "username": os.getenv("PPE_BACKEND_CASSANDRA_USERNAME", ""),
        "password": os.getenv("PPE_BACKEND_CASSANDRA_PASSWORD", ""),
        "durable_writes": os.getenv("PPE_BACKEND_CASSANDRA_DURABLE_WRITES", "true"),
        "replication": int(os.getenv("PPE_BACKEND_CASSANDRA_REPLICATION", "1"))
    },
    "blob": {
        "endpoint": os.getenv("BLOB_BASEURL", "http://127.0.0.1:9985")
    },
    "redis": {
        "enabled": os.getenv("REDIS_ENABLED", "False").lower() == "true",
        "host": os.getenv("REDIS_HOST", "127.0.0.1"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
        "db": int(os.getenv("REDIS_DB", "0")),
    },
    "public": {
        "directory": "public",
        "path": "/"
    },
    "log": {
        "name": "ppe-backend",
        "level": os.getenv("LOG_LEVEL", "info"),
        "type": os.getenv("LOG_TYPE", ""),
        "src": True
    },
    "cookie": {
        "extension": os.getenv("AUTH_COOKIE_EXTENSION", ""),
        "domain": os.getenv("AUTH_COOKIE_DOMAIN", ".cisco.com")
    },
    "camera": {
        "check_in": os.getenv("CHECK_IN_CAMMERAS", "camera1,camera_in").split(","),
        "check_out": os.getenv("CHECK_OUT_CAMMERAS", "camera2,camera_out").split(","),
        "point1": os.getenv("POINT1_CAMMERAS", "camera3,camera_point1").split(","),
        "point2": os.getenv("POINT2_CAMMERAS", "camera4,camera_point2").split(","),
    },
    "socketio": {
        # available values are eventlet/threading or leave this empty
        "async_mode": os.getenv("SOCKETIO_ASYNC_MODE", "eventlet")
    },
    "spark": {
        # "enabled": os.getenv("SPARK_ENABLED", "True").lower() == "true",
        "enabled": os.getenv("SPARK_ENABLED", "False").lower() == "true",
        "debug": os.getenv("SPARK_DEBUG", "True").lower() == "true",
        "url": os.getenv("SPARK_URL", "https://api.ciscospark.com/v1"),
        "token": os.getenv("SPARK_TOKEN", "MmY2NzliMWYtMWRkMi00YzNjLTgxMzYtNGQyZmQwMTY5ZjE3MzA0ZDA1NTUtYmU4"),
        "roomName": os.getenv("SPARK_ROOM_NAME", "PPE-demo"),
        "roomId": os.getenv("SPARK_ROOM_ID", "Y2lzY29zcGFyazovL3VzL1JPT00vZDgzMThiYTAtN2I5NS0xMWU5LTkwMmItNzdkMmM4NGE2YjFh"),
    },
    "notification": {
        "numThreshold": int(os.getenv("NOTIFICATION_NUM_THRESHOLD", "10")),
        "intervalThreshold": int(os.getenv("NOTIFICATION_INTERVAL_THRESHOLD", "10")),  # in seconds
        "syncMode": os.getenv("NOTIFICATION_SYNC_MODE", "False").lower() == "true",
        "queueSize": int(os.getenv("NOTIFICATION_QUEUE_SIZE", "32")),
        "workerCount": int(os.getenv("NOTIFICATION_QUEUE_SIZE", "1")),
        "enabled": os.getenv("NOTIFICATION_ENABLED", "False").lower() == "true",
    },
    "app": {
        "imageTTL": int(os.getenv("IMAGE_TTL", "300")),  # must above 0
        "imageDir": os.getenv("IMAGE_DIR", "/tmp/ppe"),
        "imageRootUrl": os.getenv("IMAGE_ROOT_URL", "http://localhost:7030/v1/images/"),
        "sameRecordThreshold": int(os.getenv("SAME_RECORD_THRESHOLD", "60000")),  # 60s
    },
})

if os.path.isfile(".config.json"):
    cfg = json.load(open(".config.json"))
    config.update(cfg)


if __name__ == '__main__':
    print(json.dumps(config.to_json(), indent=" " * 4))
