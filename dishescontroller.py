from flask import request, Response, Blueprint
from encodejson import jsonify

import mongodal
import recipeshelper

mongo = mongodal.MongoDAL()
rhelper = recipeshelper.RecipesHelper()

collection_name = "recipes"
dishes_controller = Blueprint('dishes_controller', __name__)


@dishes_controller.route("/dish/<dish_id>", methods=['GET'])
def get_dish(dish_id):
    mongo.connect()
    try:
        result = mongo.find_one(collection_name, {"fatsecret_id": dish_id})
    except Exception:
        result = {}

    mongo.disconnect()

    return jsonify(result)


@dishes_controller.route("/list_dishes_general/<hour>", methods=['GET'])
def list_dishes_general(hour):
    dishes_for_now = list_dishes(hour)
    result = sort_by_health(dishes_for_now)
    return jsonify(result)


@dishes_controller.route("/list_dishes_for_user/<hour>/<user>", methods=['GET'])
def list_dishes_for_user(hour, user):
    dishes_for_now = list_dishes(hour)
    result = sort_by_health_for_user(dishes_for_now, user)
    return jsonify(result)


def hour_to_meal(hour):
    if hour < 11:
        return 0
    elif hour < 16:
        return 1
    else:
        return 2


def is_dish_for_now(dish, meal):
    meals = dish.get('meals')
    if meals is not None:
        return meal in meals
    else:
        return False


def sort_by_health(dishes):
    return dishes


def sort_by_health_for_user(dishes, user):
    return dishes


def list_dishes(hour):
    mongo.connect()

    try:
        cursor = mongo.find(collection_name, {})
        meal = hour_to_meal(hour)
        dishes_for_now = [dish for dish in cursor if is_dish_for_now(dish, meal)]

        for dish in dishes_for_now:
            try:
                dish['recipe'] = rhelper.get_recipe_by_id(dish['fatsecret_id'])
            except Exception:
                dish['recipe'] = {}

        return dishes_for_now

    except Exception:
        return {}
    finally:
        mongo.disconnect()
