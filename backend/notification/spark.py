import json
import requests
from notification.provider import Provider


class Spark(Provider):
    def __init__(self, config):
        self.token = config["token"]
        self.room_id = config["room_id"]
        self.url = config["url"]
        self.msg_url = "{}/messages".format(self.url)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token)
        }

    def send(self, msg):
        body = {
            "roomId": self.room_id,
            "markdown": msg,
        }

        r = requests.post(self.msg_url, json.dumps(body), headers=self.headers)
        if r.status_code != 200:
            print("[Error]", "send spark message failed with code={}, resp={}".format(r.status_code, r.content))
            return False

        print("[Debug]", msg)
        print("[Info]", "send spark message successfully")
        return True
