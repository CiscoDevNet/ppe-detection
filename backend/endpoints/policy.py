# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import json

from flask import Response, abort, jsonify, request

from common import logger
from db.policy_dao import PolicyDao
from models.error import Error
from models.policy import Policy

policy_dao = PolicyDao()


def _get_policy(id):
    policy = policy_dao.get(id)
    if not policy:
        abort(404)
    else:
        return jsonify(policy.to_json())


def _delete_policy(id):
    policy = policy_dao.remove(id)
    if not policy:
        return Response(None, status=404, mimetype='application/json')
    else:
        return Response(None, status=204, mimetype='application/json')


def _update_policy(id):
    policy = Policy(request.json)
    if not policy:
        abort(404)
    else:
        policy.update(request.json)
        policy.id = id
        try:
            policy.validate()
        except ValueError as e:
            abort(400, str(e))
        else:
            return jsonify(policy_dao.save(policy).to_json())


def _create_policy():
    if not request.headers.get("Content-Type").startswith("application/json"):
        return json.dumps(Error(415, "Content-Type must be application/json").to_json()), 415, {'Content-Type': 'application/json'}

    policy = Policy(request.json)
    logger.info("policy data is {}".format(policy.__dict__))
    try:
        policy.validate()
    except ValueError as e:
        abort(400, str(e))
    return jsonify(policy_dao.save(policy).to_json())


def _list_policys():
    return jsonify([m.to_json() for m in policy_dao.find(request.args)])


class PolicyEndpoint:
    def __init__(self, route):
        route.get("/v1/policys/{id}")\
            .description("retrieve a specific Policy")\
            .tags("policys")\
            .parameter(name="id", required=True, description="policy id")\
            .returns(Policy, 200)\
            .returns(None, 401, 500)\
            .to(_get_policy)

        route.delete("/v1/policys/{id}")\
            .description("delete a specific Policy")\
            .tags("policys")\
            .auth_required()\
            .parameter(name="id", required=True, description="policy id")\
            .returns(None, 204, 401, 500)\
            .to(_delete_policy)

        route.put("/v1/policys/{id}")\
            .description("update a specific Policy")\
            .tags("policys")\
            .auth_required()\
            .parameter(name="id", required=True, description="policy id")\
            .returns(Policy, 200)\
            .returns(None, 401, 500)\
            .reads(Policy)\
            .to(_update_policy)

        route.post("/v1/policys")\
            .description("create new Policy")\
            .tags("policys")\
            .auth_required()\
            .returns(Policy, 200)\
            .returns(None, 401, 500)\
            .reads([Policy])\
            .to(_create_policy)

        route.get("/v1/policys")\
            .description("list all Policys")\
            .tags("policys")\
            .returns([Policy], 200)\
            .returns(None, 401, 500)\
            .parameter("limit", "integer", "query", "max items to return at one time")\
            .parameter("offset", "string", "query", "starting offset")\
            .to(_list_policys)
