from datetime import datetime

from flask import Flask, jsonify, request

from config import config
from notification.factory import NotificationFactory


notification_svc = NotificationFactory.instance(config)


MSG_TEMPLATE = """
### ppe demo
**Alert** at **{point}** at {time}
> total_person={total_person} without_hardhat={without_hardhat} without_vest={without_vest} without_both={without_both}
"""


def _construct_msg(ts, point, total_person, without_hardhat, without_vest, without_both):
    t = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")
    return MSG_TEMPLATE.format(
        time=t, point=point, total_person=total_person, without_hardhat=without_hardhat, without_vest=without_vest, without_both=without_both)


class HttpError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


app = Flask(__name__)


@app.errorhandler(HttpError)
def handle_http_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    print("[Error]:", error.message)
    return response


@app.route("/")
def home():
    return "ok"


# {
#     "id": "331404be-7c57-11e9-a345-dca90488d3b9",
#     "cameraId": "camera1",
#     "timestamp": 1558506692,
#     "persons": [
#       {
#         "hardhat": true,
#         "vest": true
#       },
#       {
#         "hardhat": true,
#         "vest": true
#       }
#     ],
#     "image": {
#       "height": 200,
#       "width": 300,
#       "format": "jpeg",
#       "raw": "base64 encoded data",
#       "url": "http://ppe-backend:7200/images/uuid1"
#     },
#     "createdAt": 1558506697000,
#     "updatedAt": 1558506697000
#  }
@app.route("/v1/detections", methods=["POST"])
def create_detections_v1():
    js = request.json
    js["image"]["raw"] = "omited"
    cameraId = js.get("cameraId")
    if cameraId is None:
        print("json field missing")
        raise HttpError("cameraId missing", status_code=400)
    print("[Info] recieved:", js["cameraId"], js["timestamp"])

    without_hardhat = len(list(filter(lambda p: not p["hardhat"], js["persons"])))
    without_vest = len(list(filter(lambda p: not p["vest"], js["persons"])))
    without_both = len(list(filter(lambda p: not p["vest"] and not p["hardhat"], js["persons"])))
    if without_hardhat > 0 or without_vest > 0 or without_both > 0:
        print("[Warn]", "someone violate the rule")
        msg = _construct_msg(js["timestamp"], js["cameraId"], len(js["persons"]), without_hardhat - without_both, without_vest - without_both, without_both)
        notification_svc.send(msg)
    else:
        print("[Info]", "no one violate the rule")

    return jsonify(request.json), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["port"])
