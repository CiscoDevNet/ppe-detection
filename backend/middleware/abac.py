# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import json
from common import logger
from common.abac import can_access_rest, AnonymousPermissions
from common.policy import Policy
from flask import abort, g, request


class AbacMiddleware:
    def __init__(self, prefix, app):
        self.prefix = prefix
        self.policy = Policy("policy.json")

        def before():
            return self.before_request()
        app.before_request(before)

    def before_request(self):
        if request.method == "OPTIONS" or not request.path.startswith(self.prefix):
            return

        if not request.url_rule:
            return
        
        logger.debug("Enter ABAC middleware for request: {method} {path}".format(method=request.method,
                                                                                 path=request.path))

        user_claims = g.get('user_claims')
        user_perms = AnonymousPermissions
        if user_claims:
            user_perms = user_claims['perms']

        policy = self.policy.lookup(request.url_rule.rule)
        if not can_access_rest(user_perms, policy, request.method):
            logger.info("Access denied based on ABAC policy({perms} - {policy}) for request: {method} {path}"
                        .format(policy=json.dumps(policy),
                                method=request.method,
                                path=request.path,
                                perms=user_perms))
            abort(403)
