# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import redis

from common import logger


class RedisClient:
    def __init__(self, config):
        if config.redis["enabled"]:
            self.connection = redis.Redis(config.redis["host"], config.redis["port"], config.redis["db"])
        else:
            self.connection = None

    def setex(self, key, time, value):
        if self.connection is None:
            return
        if not self.connection.setex(key, time, value):
            logger.info("Failed to set key={}, value={}".format(key, value))

    def exists(self, *keys):
        if self.connection is None:
            return True
        return self.connection.exists(*keys) == 1
