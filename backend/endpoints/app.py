# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


from flask import Flask, request
from flask_socketio import SocketIO, emit

from common import logger
from config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
async_mode = config.socketio["async_mode"]
if async_mode == "":
    async_mode = None
# async_mode = "threading"
socketio = SocketIO(app, async_mode=async_mode, manage_session=False)
logger.info("socketio is in {} async mode".format(async_mode))


@socketio.on('connect')
def handle_connect():
    logger.info("new connected sid={}".format(request.sid))
    emit("status", {"type": "connected", "msg": "connected"})


@socketio.on('disconnect')
def handle_disconnect():
    logger.info("disconnected sid={}".format(request.sid))
    emit("status", "disconnected")


# the following are for debug purpose, ignore
@socketio.on('ping')
def handle_ping(msg):
    logger.info("ping recieved" + msg)


@socketio.on('pong')
def handle_pong(msg):
    logger.info("pong recieved" + msg)
