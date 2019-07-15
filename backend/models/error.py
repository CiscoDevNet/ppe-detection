# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import collections


class Error:
    def __init__(self, code, message=None):
        self.code = code
        self.message = message

    def get_model(self):
        return collections.OrderedDict([("code", self.code),
                                        ("message", self.message)])
                                        
    def to_json(self):
        return self.__dict__


Error.schema = {
    'required': [
        "code",
        "message"
    ],
    'properties': {
        "code": {'type': "integer"},
        "message": {'type': "string"}
    }
}
