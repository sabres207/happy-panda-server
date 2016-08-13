from flask import Flask, request, Response, Blueprint
import mongodal
from random import randint
from encodejson import jsonify

mongo = mongodal.MongoDAL()
mongo.connect()

app = Flask(__name__)
collection = "tips"
tips_controller = Blueprint("tips_controller", __name__)


@tips_controller.route('', methods=['GET'])
def handle_tips():
    try:
        cursor = mongo.find(collection, {})
        tips = [e for e in cursor]
        return jsonify(tips[randint(0, len(tips) - 1)])
    except Exception as err:
        return jsonify(err)
