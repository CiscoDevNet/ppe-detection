# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from models import Common


class Policy(Common):
    pass


Policy.schema = {
    "required": [
    ],
    "properties": {
        "notificationEnabled": {"type": "boolean"},
        "notificationNumThreshold": {"type": "number"},
        "notificationIntervalThreshold": {"type": "number"},
    }
}
