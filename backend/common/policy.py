# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


import json
import re
import sys
from pathlib import Path
from common import logger, ContinueI
from common.uri_path import UriPath


default_policy = {'read': [{"": ""}], 'write': [{"": ""}], 'delete': [{"": ""}]}


def strip_placeholder_names(url):
    if url.endswith('/'):
        url = url[0:-1]
    return re.sub(r'<.+?>', '{}', url)


def split_route(r):
    uri_path = UriPath(r)
    return {
        "base": uri_path.base,
        "params": uri_path.params.keys()
    }


class Policy:
    def __init__(self, policy_file=None):
        self.policies = {}
        if policy_file and Path(policy_file).is_file():
            try:
                with open(policy_file) as data_file:
                    data = json.load(data_file)
                    policies = data['policies']
                    for route in policies.keys():
                        ep = split_route(route)
                        ep['policy'] = policies.get(route)
                        eps = self.policies.get(ep['base'])
                        if eps is None:
                            eps = []
                            self.policies[ep['base']] = eps
                        eps.append(ep)
            except Exception as e:
                logger.error("Failed to load policy file '{file}': {message}".format(file=policy_file, message=str(e)))
                sys.exit(1)
        else:
            logger.info("Policy file '{file}' not found, ignore policy".format(file=policy_file))

    def lookup(self, url):
        url = strip_placeholder_names(url)
        up = UriPath(url)
        # Maybe the uri contained parameters, e.g. /foo/{id}/bar so don't use uri.Path
        ps = self.policies.get(up.base, [])

        # There may be many matches for a given endpoint with the same base url.
        # This is because /foo/bar?zoo is treated as distinct from /foo/bar.
        # So we implement a greedy match by choosing the endpoint which matches the most
        # params from the request.
        match = None
        for p in ps:
            try:
                p['params'] = p.get('params', [])
                if len(p['params']) != 0:
                    qps = up['params']
                    for param in p['params']:
                        if qps[param] is None:
                            raise ContinueI()

                if match is None or len(p['params']) > len(match['params']):
                    match = p.get('policy')
            except ContinueI:
                continue

        if match is None:
            match = default_policy
        return match
