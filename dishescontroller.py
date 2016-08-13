# from fatsecret import Fatsecret
# import sys
# import json
# method = sys.argv[1]
# arguments = sys.argv[2:]
#
# fs = Fatsecret("21a6cd97e2644a00a7fc7c7d7ae00527", "392dba9edc6b40fe8ef11f860f9043f9")
# Fatsecret()
# for argument in arguments:
#     with open(argument + "-" + method + ".txt", "w+") as f_out:
#         if method == "search":
#             result = fs.recipes_search(argument, max_results=5, page_number=5)
#         else:
#             result = fs.recipe_get(argument)
#         result_json = json.dumps(result)
#         f_out.write(result_json)

from flask import request, Response, jsonify, Blueprint
import mongodal
import recipeshelper

mongo = mongodal.MongoDAL()
collection_name = "recipes"
dishes_controller = Blueprint('dishes_controller', __name__)


@dishes_controller.route("/dish/<dish_id>", methods=['GET'])
def get_dish(dish_id):
    mongo.connect()
    try:
        result =  mongo.find_one(collection_name, {"_id": dish_id})
    except Exception as err_msg:
        result = {}

    mongo.disconnect()

    return jsonify(result)