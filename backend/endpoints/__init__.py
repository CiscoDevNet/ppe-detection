# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import json
import os
import shutil

from common import logger
from config import config
from endpoints.detection import detection_dao
from models.detection import Detection

try:
    with open('mockups/detection_data.json') as data_file:
        data = json.load(data_file)
        for o in data:
            detection_dao.save(Detection(o))
        logger.info("{size} mockup Detection data loaded from {file}".format(size=len(data), file='detection_data.json'))
except IOError:
    pass

try:
    src = 'mockups/images/'
    dest = config.app["imageDir"]
    files = os.listdir(src)
    for f in files:
        shutil.copy(os.path.join(src, f), os.path.join(dest, f))
    logger.info("{size} mockup images copied to {dest}".format(size=len(files), dest=dest))
except BaseException as e:
    logger.info("Failed to load mockup images:" + str(e))
    pass
