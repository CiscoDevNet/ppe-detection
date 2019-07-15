# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import types
import re
from http.client import responses


class Parameter:
    def __init__(self, name="", t="string", where="path", desc="", required=False, default=""):
        self.meta = {
            "name": name,
            "type": t,
            "in": where,
            "description": desc,
            "required": required,
            "default": default
        }

    def name(self, name):
        self.meta["name"] = name
        return self

    def required(self, required):
        self.meta["required"] = required
        return self

    def where(self, where):
        self.meta["in"] = where
        return self

    def type(self, t):
        self.meta["type"] = t
        self.meta["schema"] = ""
        return self

    def value(self, default):
        self.meta["default"] = default
        return self

    def schema(self, schema):
        self.meta["schema"] = schema
        self.meta["type"] = ""
        return self

    def items(self, items):
        self.meta["items"] = items
        return self


class Routes:
    def __init__(self):
        self.metas = []
        self.models = {}

    def get(self, path):
        r = Route(self).get(path)
        self.metas.append(r)
        return r

    def post(self, path):
        r = Route(self).post(path)
        self.metas.append(r)
        return r

    def put(self, path):
        r = Route(self).put(path)
        self.metas.append(r)
        return r

    def delete(self, path):
        r = Route(self).delete(path)
        self.metas.append(r)
        return r

    def head(self, path):
        r = Route(self).head(path)
        self.metas.append(r)
        return r

    def patch(self, path):
        r = Route(self).patch(path)
        self.metas.append(r)
        return r

    def add_model(self, model, name=None):
        if name is None:
            name = model.__name__
        self.models[name] = model
        return self

    def add_models(self, *models):
        for model in models:
            self.add_model(model)
        return self

    def attach(self, flask_app):
        r = re.compile(r"\{(.+?)\}", re.IGNORECASE)
        for route in self.metas:
            rpath = route.meta["path"]
            vars = re.findall(r, rpath)
            for v in vars:
                rpath = rpath.replace("{%s}" % v, "<%s>" % v)
            flask_app.route(rpath, methods=[route.method.upper()])(route.fn)


class Route:
    def __init__(self, routes):
        self.routes = routes
        self.fn = None
        self.method = "get",
        self.meta = {
            "path": "",
            "description": "",
            "tags": [],
            "parameters": [],
            "produces": ["application/json"],
            "consumes": ["application/json"],
            "operationId": "",
            "summary": "",
            "responses": {}
        }

    def get(self, path):
        self.method = 'get'
        self.meta["path"] = path
        return self

    def post(self, path):
        self.method = 'post'
        self.meta["path"] = path
        return self

    def put(self, path):
        self.method = 'put'
        self.meta["path"] = path
        return self

    def delete(self, path):
        self.method = 'delete'
        self.meta["path"] = path
        return self

    def head(self, path):
        self.method = 'head'
        self.meta["path"] = path
        return self

    def patch(self, path):
        self.method = 'patch'
        self.meta["path"] = path
        return self

    def description(self, desc):
        self.meta["description"] = desc
        if self.meta["summary"] is "":
            self.meta["summary"] = desc
        return self

    def summary(self, summary):
        self.meta["summary"] = summary
        if self.meta["description"] is "":
            self.meta["description"] = summary
        return self

    def tags(self, *tags):
        self.meta["tags"] = tags
        return self

    def operation(self, operation_id):
        self.meta["operationId"] = operation_id
        return self

    def produces(self, *mime_types):
        self.meta["produces"] = mime_types
        return self

    def consumes(self, *mime_types):
        self.meta["consumes"] = mime_types
        return self

    def to(self, fn):
        if not isinstance(fn, types.FunctionType):
            raise TypeError("must be a function")

        self.fn = fn
        if self.meta["operationId"] is "":
            self.meta["operationId"] = fn.__name__.strip("_")
        return self

    def parameter(self, name="", t="string", where="path", description="", required=False, default=""):
        self.meta["parameters"].append(Parameter(name, t, where, description, required, default).meta)
        return self

    def auth_required(self, token_type="Bearer"):
        self.parameter("Authorization", "string", "header", "authorization header", True, token_type)
        return self

    def reads(self, model):
        p = Parameter().name("body").where('body').required(True)
        p.schema(self.__detect_schema(model))
        if "default" in p.meta:
            del(p.meta["default"])
        self.meta["parameters"].append(p.meta)
        return self

    def returns(self, model, *codes):
        for code in codes:
            self.meta["responses"][code] = {
                "description": responses[code]
            }
            if model is not None:
                self.meta["responses"][code]['schema'] = self.__detect_schema(model)
        return self

    def __detect_schema(self, model):
        if isinstance(model, str):
            return {
                "type": model
            }

        if isinstance(model, list):
            if isinstance(model[0], type):
                self.routes.models[model[0].__name__] = model[0]
                return {
                    "type": "array",
                    "items": {"$ref": "#definitions/" + model[0].__name__}
                }
            else:
                return {
                    "type": "array",
                    "items": {
                        "type": type(model[0])
                    }
                }

        if isinstance(model, type):
            self.routes.models[model.__name__] = model
            return {
                "$ref": "#/definitions/" + model.__name__
            }

        return {
            "type": "string"
        }
