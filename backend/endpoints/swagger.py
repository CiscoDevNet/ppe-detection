# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

from collections import OrderedDict

from flask import jsonify, redirect, send_from_directory

from config import config
from models.error import Error


class SwaggerEndpoint:
    def __init__(self, app, routes):
        paths = {}
        definitions = {"Error": Error.schema}

        for route in routes.metas:
            rs = paths.get(route.meta['path'])
            if rs is None:
                rs = {}
                paths[route.meta['path']] = rs
            rs[route.method] = route.meta

        for name, model in routes.models.items():
            definitions[name] = model.schema

        ad = OrderedDict()
        ad["swagger"] = "2.0"
        ad["info"] = {
            "title": "DevNet {name} ".format(name=config['serviceName'].capitalize()),
            "description": "DevNet Cloudification Platform {name} Microservice".format(name=config['serviceName'].capitalize()),
            "termsOfService": "https://developer.cisco.com/site/terms-and-conditions/",
            "contact": {
                "name": "Cloudy Team",
                "email": "devnet-cloud-engineering@cisco.com"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
            },
            "version": "1.0.0"
        }
        ad["externalDocs"] = {
            "description": "Visit Cisco DevNet",
            "url": "https://developer.cisco.com"
        }
        ad["host"] = config['serviceHost'] + ":" + str(config['servicePort'])
        ad["schemes"] = ["http"]
        ad["consumes"] = ["application/json"]
        ad["produces"] = ["application/json"]
        ad["paths"] = paths
        ad["definitions"] = definitions

        def cleanup_list(l):
            newl = []
            for value in l:
                if value is None or value is "":
                    pass
                if isinstance(value, list):
                    newl.append(cleanup_list(value))
                elif isinstance(value, dict):
                    if len(value) is not 0:
                        newl.append(cleanup_dict(value))
                else:
                    newl.append(value)
            return newl

        def cleanup_dict(d):
            newd = OrderedDict()
            for key, value in d.items():
                if value is None or value is "":
                    pass
                elif isinstance(value, list):
                    newd[key] = cleanup_list(value)
                elif isinstance(value, dict):
                    if len(value) is not 0:
                        newd[key] = cleanup_dict(value)
                else:
                    newd[key] = value
            return newd

        apidocs = cleanup_dict(ad)

        @app.route("/apidocs.json", methods=['GET'])
        def get_apidocs():
            return jsonify(apidocs)

        @app.route("/apidocs")
        def static_apidocs():
            return redirect("/apidocs/")

        @app.route(config["public"]["path"] + "<path:file>")
        def static_files(file):
            if file.endswith("/"):
                file = file + "index.html"
            return send_from_directory(config["public"]["directory"], file)


        @app.route(config["public"]["path"])
        def static_root():
            return static_files('index.html')
