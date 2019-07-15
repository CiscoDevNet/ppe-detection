# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from config import config
from common import logger
from services.cassandra_client import CassandraClient

cassandra_client = CassandraClient(config)
cassandra_client.create_keyspace(config['cassandra'])
logger.info("Keyspace {} created successfully".format(config['cassandra']['keyspace']))
