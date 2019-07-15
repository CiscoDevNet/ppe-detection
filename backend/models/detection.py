# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from models import Common


class Detection(Common):
    pass


Detection.schema = {
    "required": [
        "cameraId",
        "timestamp",
        "persons",
        "image",
    ],
    "properties": {
        "cameraId": {"type": "string"},
        "createdAt": {"type": "number"},
        "image": {"$ref": "#definitions/Image"},
        "persons": {"$ref": "#definitions/Person"},
        "status": {"type": "number"},
        "timestamp": {"type": "number"},
        "updatedAt": {"type": "number"},
        "id": {"type": "string"}
    }
}
