# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


import base64
import json
import requests
from common import logger
from services.jwt_client import Jwt, defaultAbac


class Blob:
    def __init__(self, blob, parse = False):
        self.type = blob.get("type")
        self.name = blob.get("name")
        self.description = blob.get("description", "")
        self.version = blob.get("version", "")
        self.abac = blob.get("abac", defaultAbac)
        if not isinstance(self.abac, dict):
            self.abac = self.abac.__dict__
        self.tags = blob.get("tags", [])
        self.created_at = blob.get("created_at")
        self.last_modified = blob.get("last_modified")
        data = blob.get("data")
        if parse:
            self.data = json.loads(str(base64.b64decode(data), 'UTF-8'))
        else:
            self.data = data

    def __repr__(self):
        return "Blob({})".format(self.name)


class BlobType:
    def __init__(self, blob_type):
        self.name = blob_type.get("name")
        self.encrypted = blob_type.get("encrypted", False)
        self.jsonschema = blob_type.get("jsonschema", "{}")
        self.custom_index_fields = blob_type.get("custom_index_fields")
        self.abac = blob_type.get("abac", defaultAbac)
        if not isinstance(self.abac, dict):
            self.abac = self.abac.__dict__
        self.tags = blob_type.get("tags", [])
        self.created_at = blob_type.get("created_at")
        self.last_modified = blob_type.get("last_modified")

    def __repr__(self):
        return "BlobType({})".format(self.name)

    def load_schemas(self, model):
        pass
        

class BlobClient:
    def __init__(self, config):
        self.endpoint = config['blob']['endpoint']

    def create_blob_type(self, blob_type):
        if isinstance(blob_type, str):
            blob_type = BlobType({'name': blob_type})
        elif isinstance(blob_type, dict):
            blob_type = BlobType(blob_type)

        uri = self.endpoint + "/v1/blobtype/"
        r = requests.post(uri, headers=BlobClient.__new_header__(), json=blob_type.__dict__)
        r.raise_for_status()
        return BlobType(r.json())

    def get_blob_type(self, name):
        uri = self.endpoint + "/v1/blobtype/" + name
        r = requests.get(uri, headers=BlobClient.__new_header__())
        r.raise_for_status()
        return BlobType(r.json())

    def list_blob_types(self):
        uri = self.endpoint + "/v1/blobtype/"
        r = requests.get(uri, headers=BlobClient.__new_header__())
        r.raise_for_status()
        if r.status_code == 204:
            return []
        else:
            return [BlobType(x) for x in r.json()]

    def save_blob(self, blob):
        if blob.data is not None:
            blob.data = str(base64.b64encode(str.encode(json.dumps(blob.data.__dict__))), "UTF-8")
        
        uri = self.endpoint + "/v1/blob/" + blob.type
        r = requests.post(uri, headers=BlobClient.__new_header__(), json=blob.__dict__)
        r.raise_for_status()
        return Blob(r.json(), True)

    def get_blob(self, blob_type, name):
        uri = self.endpoint + "/v1/blob/" + blob_type + "/" + name
        r = requests.get(uri, headers=BlobClient.__new_header__())
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return Blob(r.json(), True)

    def delete_blob(self, blob_type, name):
        uri = self.endpoint + "/v1/blob/" + blob_type + "/" + name
        r = requests.delete(uri, headers=BlobClient.__new_header__())
        if r.status_code == 404:
            return False
        r.raise_for_status()
        return True

    def list_blobs(self, blob_type, args={}):
        uri = self.endpoint + "/v1/blob/" + blob_type
        r = requests.get(uri, headers=BlobClient.__new_header__(), params=args)
        r.raise_for_status()
        if r.status_code == 204:
            return []
        else:
            return [Blob(x, True) for x in r.json()]

    @staticmethod
    def __new_header__():
        return {
            'Authorization': 'Bearer ' + Jwt.get_sudo_token(),
            'Content-Type': 'application/json'
        }
