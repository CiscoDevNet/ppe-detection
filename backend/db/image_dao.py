# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

# from common import logger
from config import config

# from models.image import Image
# from services.cassandra_client import CassandraClient, to_dict


class ImageDao:
    table_name = "ppe.images"

    fields = {
        "id": "text",
        "path": "text",
    }

    indexes = []
    pks = []

    def __init__(self):
        self.image_dir = config.app["imageDir"]

    def get(self, id):
        return True

    def remove(self, id):
        return True

    def save(self, image):
        return True

    def find(self, args):
        pass
