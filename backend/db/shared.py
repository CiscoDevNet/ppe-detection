from common import logger


def add_condition(cql, args, string_fields, number_fields):
    conditions = []
    for field in string_fields:
        if args.get(field):
            conditions.append(" {}='{}'".format(field, args[field]))
    for field in number_fields:
        if args.get(field):
            conditions.append(" {}={}".format(field, args[field]))
    if args.get('offset'):
        conditions.append(" token(id) > token('{}')".format(args['offset']))
    if len(conditions) > 0:
        cql += " WHERE" + "AND".join(conditions)
    limit = args.get('limit')
    if not limit:
        limit = 10
        cql += " LIMIT {}".format(limit)
    logger.info(cql)
    return cql
