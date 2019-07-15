# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from common import logger
from config import config
from models.policy import Policy


class PolicyDao:

    notificationEnabled = config.notification["enabled"]
    notificationNumThreshold = config.notification["numThreshold"]
    notificationIntervalThreshold = config.notification["intervalThreshold"]

    def __init__(self):
        pass

    def get(self, id):
        return Policy({
            "notificationEnabled": self.__class__.notificationEnabled,
            "notificationNumThreshold": self.__class__.notificationNumThreshold,
            "notificationIntervalThreshold": self.__class__.notificationIntervalThreshold,
        })

    def remove(self, id):
        return True

    def save(self, policy):
        if policy.notificationEnabled is not None:
            self.__class__.notificationEnabled = policy.notificationEnabled
        if policy.notificationNumThreshold is not None:
            self.__class__.notificationNumThreshold = policy.notificationNumThreshold
        if policy.notificationIntervalThreshold is not None:
            self.__class__.notificationIntervalThreshold = policy.notificationIntervalThreshold
        logger.info("policy changed")
        return Policy({
            "notificationEnabled": self.__class__.notificationEnabled,
            "notificationNumThreshold": self.__class__.notificationNumThreshold,
            "notificationIntervalThreshold": self.__class__.notificationIntervalThreshold,
        })

    def find(self, args):
        pass
