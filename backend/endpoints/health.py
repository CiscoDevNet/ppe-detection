# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


from flask import jsonify


class Health:
    def __init__(self, status):
        self.status = status


Health.schema = {
    "required": [
        "status"
    ],
    "properties": {
        "status": {"type": "string"}
    }
}


def _check_health():
    return jsonify(Health("OK").__dict__)


class HealthEndpoint:
    def __init__(self, route):
        route.get("/v1/healthz")\
            .description("health check")\
            .returns(Health, 200)\
            .to(_check_health)

