# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import json

import requests

from common import logger

TEST_FILE = "https://alln-extcloud-storage.cisco.com/ciscoblogs/5ce5ac69ea19f-460x230.png"


class Spark:
    def __init__(self, config):
        self.enabled = config["spark"]["enabled"]
        self.debug = config["spark"]["debug"]
        self.token = config["spark"]["token"]
        self.roomId = config["spark"]["roomId"]
        self.url = config["spark"]["url"]
        self.msg_url = "{}/messages".format(self.url)
        self.room_url = "{}/rooms".format(self.url)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token)
        }

    def send_msg(self, msg, files=None):
        logger.info("spark message to send is {}".format(msg))
        if self.enabled:
            if self.debug and files is not None:
                files = [TEST_FILE]
            self._send(msg, files)
        else:
            logger.info("spark is disabled")


    """files should be array of image url"""
    def _send(self, msg, files=None):
        body = {
            "roomId": self.roomId,
            # "text": msg,
            "markdown": msg,
        }
        if files is not None:
            body["files"] = files

        r = requests.post(self.msg_url, json.dumps(body), headers=self.headers)
        if r.status_code != 200:
            logger.error("send spark message failed with code={}, resp={}".format(r.status_code, r.content))
            return False

        logger.info("send spark message successfully")
        return True

    def get_roomId_by_name(self, name):
        r = requests.get(self.room_url, headers=self.headers)

        print(r.json())
        if r.status_code != 200:
            logger.error("get roomId failed with code={}, resp={}".format(r.status_code, r.content))
            return None

        for item in r.json()["items"]:
            if item["title"] == name:
                logger.info("get roomId successfully, roomId={}".format(item["id"]))
                return item["id"]
