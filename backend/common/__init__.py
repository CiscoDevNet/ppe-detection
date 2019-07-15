# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import logging
import sys
from logmatic import JsonFormatter
from config import config


class ContinueI(Exception):
    def __init__(self):
        pass


def get_logger(name, level=logging.INFO):
    if config["log"]["type"] == "json":
        formatter = JsonFormatter(fmt="%(asctime) %(name) %(filename) %(funcName) %(levelname) %(lineno) %(message)",
                                  extra={"service": config["serviceName"]})
    else:
        fmt = '%(asctime)s %(levelname)-6s - [{service}:%(filename)s:%(funcName)s:%(lineno)s] - %(message)s'.format(
            service=config["serviceName"])
        formatter = logging.Formatter(fmt)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    l = logging.getLogger(name)
    l.setLevel(level)
    l.addHandler(console_handler)
    return l


logger = get_logger(config["serviceName"])

