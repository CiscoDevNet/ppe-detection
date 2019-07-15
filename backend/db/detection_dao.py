# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from common import logger
from config import config
from db.shared import add_condition
from models import ImageType, PersonType
from models.detection import Detection
from services.cassandra_client import CassandraClient, to_dict


class PersonUDT:
    type_name = "ppe.person"

    fields = {
        "hardhat": "boolean",
        "vest": "boolean",
    }

    def __init__(self):
        self.cassandra_client = CassandraClient(config)
        try:
            self.cassandra_client.create_udt(PersonUDT.type_name, PersonUDT.fields)
            logger.info("type {} created".format(PersonUDT.type_name))
        except Exception as e:
            logger.warn("failed to create type {}: {}".format(PersonUDT.type_name, str(e)))


class ImageUDT:
    type_name = "ppe.image"

    fields = {
        "height": "int",
        "width": "int",
        "format": "text",
        "raw": "text",
        "url": "text",
    }

    def __init__(self):
        self.cassandra_client = CassandraClient(config)
        try:
            self.cassandra_client.create_udt(ImageUDT.type_name, ImageUDT.fields)
            logger.info("type {} created".format(ImageUDT.type_name))
        except Exception as e:
            logger.warn("failed to create type {}: {}".format(ImageUDT.type_name, str(e)))


class DetectionDao:
    table_name = "ppe.detections"

    fields = {
        "id": "text",
        "cameraId": "text",
        "createdAt": "timestamp",
        "image": "FROZEN<image>",
        "persons": "list<FROZEN<person>>",
        "status": "int",
        "timestamp": "bigint",
        "updatedAt": "bigint"
    }

    indexes = ["id", "status"]
    pks = ["cameraId", "timestamp"]

    ImageUDT()
    PersonUDT()

    def __init__(self):
        self.cassandra_client = CassandraClient(config)
        # TODO: hack
        # self.cassandra_client.cluster.register_user_type("ppe", "image", ImageType)
        # self.cassandra_client.cluster.register_user_type("ppe", "person", PersonType)
        try:
            self.cassandra_client.create_table(DetectionDao.table_name, DetectionDao.pks, DetectionDao.fields, DetectionDao.indexes, clustering_order_by="(timestamp DESC)")
            logger.info("table {} created".format(DetectionDao.table_name))
        except Exception as e:
            logger.warn("failed to create table {}: {}".format(DetectionDao.table_name, str(e)))

    def get(self, id):
        cql = "SELECT cameraId, createdAt, image, persons, status, timestamp, updatedAt, id FROM {} WHERE id = ? LIMIT 1".format(
            DetectionDao.table_name)
        rows = self.cassandra_client.execute(cql, [id])
        for row in rows:
            return Detection(to_dict(row, DetectionDao.fields.keys()))
        return None

    def remove(self, id):
        cql = "DELETE FROM {} WHERE id = ?".format(DetectionDao.table_name)
        self.cassandra_client.execute(cql, [id])
        return True

    def save(self, detection):
        logger.info("detection to insert is {}".format(detection.__dict__))
        # TODO: hack here
        persons = [PersonType(p) for p in detection.persons]
        cql = "INSERT INTO {} (cameraId, createdAt, image, persons, status, timestamp, updatedAt, id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(
            DetectionDao.table_name)
        self.cassandra_client.execute(cql, [
            detection.cameraId,
            detection.createdAt,
            ImageType(detection.image),
            persons,
            detection.status,
            detection.timestamp,
            detection.updatedAt,
            detection.id,
        ])
        return detection

    def find(self, args):
        cql = "SELECT cameraId,createdAt,image,persons,status,timestamp,updatedAt,id FROM {}".format(DetectionDao.table_name)
        cql = add_condition(cql, args, ['cameraId'], ['status'])

        logger.info("cql is {}".format(cql))
        rows = self.cassandra_client.execute(cql)
        return [Detection(to_dict(row, DetectionDao.fields.keys())) for row in rows]
