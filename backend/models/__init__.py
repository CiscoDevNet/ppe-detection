# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


class Common:
    def __init__(self, id, obj=None):
        if obj:
            self.id = id
        elif id:
            obj = id

        if obj:
            self.update(obj)

    def validate(self):
        for prop in self.__class__.schema["required"]:
            if not hasattr(self, prop) or not getattr(self, prop):
                raise ValueError(prop + " is required")
            else:
                value = getattr(self, prop)
                if isinstance(value, Common):
                    value.validate()

    def update(self, obj):
        if not isinstance(obj, dict):
            obj = obj.__dict__
        for prop in self.__class__.schema["properties"]:
            if prop in obj or hasattr(obj, prop):
                setattr(self, prop, obj[prop])
        # for prop, value in self.__class__.schema["properties"].items():
        #     if prop in obj or hasattr(obj, prop):
                # if value.get("$ref") is not None:
                #     class_name = value["$ref"].split("/")[-1]
                #     setattr(self, prop, eval(class_name)(obj[prop]))
                # else:
                #     setattr(self, prop, obj[prop])

    def to_json(self):
        return self.__dict__

    def __getattr__(self, name):
        if name in self.__class__.schema["properties"]:
            return self.__dict__.get(name, None)
        return None


Common.schema = {
    "required": [
    ],
    "properties": {
    }
}


# TODO: hack here
class ImageType(Common):
    pass


ImageType.schema = {
    "required": [
        "height",
        "width",
        "format",
        "raw",
    ],
    "properties": {
        "height": {"type": "number"},
        "width": {"type": "number"},
        "format": {"type": "string"},  # TODO: enums: "jpeg", "png"
        "raw": {"type": "string"},
        "url": {"type": "string"},
    }
}


class PersonType(Common):
    pass


PersonType.schema = {
    "required": [
        "height",
        "width",
        "format",
        "raw",
    ],
    "properties": {
        "hardhat": {"type": "boolean"},
        "vest": {"type": "boolean"},
    }
}
