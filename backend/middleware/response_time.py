# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


import time

from flask import g, request

from common import logger, util


class ResponseTimeMiddleware:
    def __init__(self, app):
        self.app = app

        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    @staticmethod
    def before_request():
        g.request_start_time = time.time()

    @staticmethod
    def after_request(response):
        duration_us = util.get_duration_us(g.request_start_time)
        logger.info("{} - - {} {} {} {} {}".format(request.remote_addr, request.method,
                                                   request.path, response.status_code, response.content_length, duration_us))
        return response
