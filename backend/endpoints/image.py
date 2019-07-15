# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------

import base64
import os
import uuid

from flask import Response, abort, jsonify, request, send_from_directory

from common import logger
from config import config
from db.image_dao import ImageDao
from endpoints.var import redis_cli
from models.image import Image

image_dao = ImageDao()


def _get_image(id):
    if not redis_cli.exists(id):
        abort(403)
    return send_from_directory(config["app"]["imageDir"], id)
    # image = image_dao.get(id)
    # if not image:
    #     abort(404)
    # else:
    #     return jsonify(image.to_json())


def _delete_image(id):
    image = image_dao.remove(id)
    if not image:
        return Response(None, status=404, mimetype='application/json')
    else:
        return Response(None, status=204, mimetype='application/json')


def _update_image(id):
    image = Image(request.json)
    if not image:
        abort(404)
    else:
        image.update(request.json)
        image.id = id
        try:
            image.validate()
        except ValueError as e:
            abort(400, str(e))
        else:
            return jsonify(image_dao.save(image).to_json())


def _create_image():
    image = Image(request.json)
    logger.info("image data is {}".format(image.__dict__))
    image.id = str(uuid.uuid1())

    file_name = image.id + "." + image.image.format
    file_path = os.path.join(config.app["imageDir"], file_name)
    fh = open(file_path, "wb")
    fh.write(base64.b64decode(image.image.raw))
    fh.close()
    image.image["url"] = config.app["imageRootUrl"] + file_name
    try:
        image.validate()
    except ValueError as e:
        abort(400, str(e))
    else:
        result = image_dao.save(image).to_json()
        return jsonify(result)


def _list_images():
    return jsonify([m.to_json() for m in image_dao.find(request.args)])


class ImageEndpoint:
    # def __init__(self, app, route):
    def __init__(self, route):
        route.get("/v1/images/{id}")\
            .description("retrieve a specific Image")\
            .tags("images")\
            .parameter(name="id", required=True, description="image id")\
            .to(_get_image)
        # route.get("/v1/images/{id}")\
        #     .description("retrieve a specific Image")\
        #     .tags("images")\
        #     .parameter(name="id", required=True, description="image id")\
        #     .returns(Image, 200)\
        #     .returns(None, 401, 500)\
        #     .to(_get_image)

        # route.delete("/v1/images/{id}")\
        #     .description("delete a specific Image")\
        #     .tags("images")\
        #     .auth_required()\
        #     .parameter(name="id", required=True, description="image id")\
        #     .returns(None, 204, 401, 500)\
        #     .to(_delete_image)

        # route.put("/v1/images/{id}")\
        #     .description("update a specific Image")\
        #     .tags("images")\
        #     .auth_required()\
        #     .parameter(name="id", required=True, description="image id")\
        #     .returns(Image, 200)\
        #     .returns(None, 401, 500)\
        #     .reads(Image)\
        #     .to(_update_image)

        # route.post("/v1/images")\
        #     .description("create new Image")\
        #     .tags("images")\
        #     .auth_required()\
        #     .returns(Image, 200)\
        #     .returns(None, 401, 500)\
        #     .reads([Image])\
        #     .to(_create_image)

        # route.get("/v1/images")\
        #     .description("list all Images")\
        #     .tags("images")\
        #     .returns([Image], 200)\
        #     .returns(None, 401, 500)\
        #     .parameter("limit", "integer", "query", "max items to return at one time")\
        #     .parameter("offset", "string", "query", "starting offset")\
        #     .to(_list_images)

        # @app.route("/image/" + "<path:file>")
        # def static_images(file):
        #     if file.endswith("/"):
        #         file = file + "index.html"
        #     return send_from_directory(config["app"]["imageDir"], file)
