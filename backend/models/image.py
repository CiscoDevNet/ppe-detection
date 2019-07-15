# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from models import Common


class Image(Common):
    pass


Image.schema = {
    "required": [
        "id",
        "path",
    ],
    "properties": {
        "path": {"type": "string"},
        "id": {"type": "string"}
    }
}
