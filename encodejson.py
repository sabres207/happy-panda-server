from flask import Flask, Response
import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def jsonify(obj):
    obj.pop('_id', None)
    dat = JSONEncoder().encode(obj)
    return Response(response=dat, status=200, mimetype="application/json")



