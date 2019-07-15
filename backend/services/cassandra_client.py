# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from cassandra.cluster import Cluster
from cassandra.util import OrderedMapSerializedKey

from common import logger


def to_dict(row, fields):
    d = {}
    for x in fields:
        f = getattr(row, x.lower())
        if isinstance(f, OrderedMapSerializedKey):
            f = dict(f)
        d[x] = f
    return d


class CassandraClient:
    def __init__(self, config):
        self.cluster = Cluster(config['cassandra']['contactPoints'], protocol_version=3)
        self.session = self.cluster.connect()
        # from cassandra.query import dict_factory
        # self.session.row_factory = dict_factory

    def execute(self, cql, params=[]):
        if params is None or len(params) == 0:
            return self.session.execute(cql, params)
        pstmt = self.session.prepare(cql)
        return self.session.execute(pstmt, params)

    def create_keyspace(self, opts):
        keyspace = opts.keyspace
        replication = opts.replication
        durable_writes = opts.durable_writes
        cql = """CREATE KEYSPACE IF NOT EXISTS {ks} WITH replication = {{
            'class': 'SimpleStrategy', 
            'replication_factor': '{rp}'
        }}  AND durable_writes = {dw};""".format(ks=keyspace, rp=replication, dw=durable_writes)
        logger.info(cql)
        return self.execute(cql)

    def create_table(self, table, pks, fields, indexes, **kwargs):
        pks = pks or ['id']
        indexes = indexes or []
        p_fields = ["{} {}".format(k,v) for k,v in fields.items()]
        cql = "CREATE TABLE IF NOT EXISTS {table} ({fields}, PRIMARY KEY ({pks}))".format(
            table=table, 
            fields=",".join(p_fields), 
            pks=",".join(pks))

        if len(kwargs) > 0:
            cql += " WITH"
            if kwargs.get("clustering_order_by") is not None:
                cql +=  " CLUSTERING ORDER BY {column_n_order}".format(column_n_order=kwargs["clustering_order_by"])

        logger.info(cql)
        self.execute(cql)
        for idx in indexes:
            cql = "CREATE INDEX IF NOT EXISTS idx_{prefix}_{idx} ON {table} ({idx})".format(
                prefix=table.split(".")[1],
                idx=idx, 
                table=table)
            logger.info(cql)
            self.execute(cql)

    def create_udt(self, type, fields):
        p_fields = ["{} {}".format(k,v) for k,v in fields.items()]
        cql = "CREATE TYPE {type} ({fields})".format(
            type=type, 
            fields=",".join(p_fields))
        logger.info(cql)
        self.execute(cql)
