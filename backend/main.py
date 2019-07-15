# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


import logging
import os
from multiprocessing import Process

# import wsgiserver
# from flask import Flask
from flask_cors import CORS

import common
from common.util import ensure_dir
from config import config
from endpoints.app import app, socketio
from endpoints.detection import DetectionEndpoint, msg_queue
from endpoints.health import HealthEndpoint
from endpoints.image import ImageEndpoint
from endpoints.notfication_sender import send_process
from endpoints.policy import PolicyEndpoint
from endpoints.swagger import SwaggerEndpoint
from middleware.abac import AbacMiddleware
from middleware.response_time import ResponseTimeMiddleware
from middleware.route import Routes
from middleware.user import UserMiddleware

CORS(app, resources={
    r"/v1/*": {
        "origins": config['corsList'],
        "allow_headers": ['X-Requested-With', 'Accept', 'Content-Type', 'Origin', 'Authorization', 'Token'],
        "supports_credentials": True
    }
})
UserMiddleware("/v1/", app)
AbacMiddleware("/v1/", app)
ResponseTimeMiddleware(app)

routes = Routes()
HealthEndpoint(routes)
DetectionEndpoint(routes)
ImageEndpoint(routes)
PolicyEndpoint(routes)
routes.attach(app)

# ImageEndpoint(app, routes)
SwaggerEndpoint(app, routes)


if __name__ == '__main__':
    common.get_logger('werkzeug', logging.INFO)
    ensure_dir(config.app["imageDir"])
    for i in range(int(config.notification['workerCount'])):
        common.logger.info("starting notification worker {}".format(i))
        worker = Process(target=send_process, args=(msg_queue,))
        worker.start()
    if os.getenv("FLASK_ENV") == "production":
        common.logger.info("* Running on http://{}:{}/ (Press CTRL+C to quit)".format(config.serviceHost, config.servicePort))
        socketio.run(app, host=config.serviceHost, port=config.servicePort, log_output=True)
        # server = wsgiserver.WSGIServer(app, host=config.serviceHost, port=config.servicePort)
        # server.start()
    else:
        socketio.run(app, host=config.serviceHost, port=config.servicePort, log_output=True)
