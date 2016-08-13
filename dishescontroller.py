from flask import request, Response, Blueprint
from encodejson import jsonify

import mongodal
import recipeshelper
import unicodedata

RECIPE_HTML = '<div><h1>{0}</h1><h3>{1}</h3><h3>amount of servings: {2}</h3><h2>Ingredients</h2>' \
              '<ul style="list-style-type:circle">{3}</ul><h2>Directions</h2><ol>{4}</ol><p>rating: {5}/5</p>' \
              '<p>difficulty: {6}</p><p>preperation time: {7} minutes</p></div>'
LI_HTML = "<li>{0}</li>"

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


@dishes_controller.route("/", methods=['GET'])
def list_dishes_general():
    hour = request.args.get("hour")
    if hour is None:
        return []
    user = request.args.get("user")
    dishes_for_now = list_dishes(hour)

    if user is not None:
        sorted_list = sort_by_health_for_user(dishes_for_now, user)
    else:
        sorted_list = sort_by_health(dishes_for_now)

    for dish in sorted_list:
        add_html_description(dish)

    return jsonify(sorted_list)



def hour_to_meal(hour):
    if 4 < hour <= 11:
        return 0
    elif 11 < hour <= 16:
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


def add_html_description(dish):
    recipe = dish['recipe']
    if recipe is not None:
        dish_name = recipe.get('recipe_name')
        recipe_description = recipe.get('recipe_description')
        servings_amount = recipe.get('number_of_servings')

        ingredients_list = recipe.get('ingredients').get('ingredient')
        ingredients_li_string = ""
        for ingr in ingredients_list:
            ingr_description = ingr.get('ingredient_description')
            if ingr_description is not None:
                ingr_description = unicodedata.normalize('NFKD', ingr_description).encode('ascii', 'ignore')
                ingredients_li_string += LI_HTML.format(ingr_description)

        directionsn_list = recipe.get('directions').get('direction')
        directions_li_string = ""
        for direct in directionsn_list:
            direct_description = direct.get('direction_description')
            direct_description = unicodedata.normalize('NFKD', direct_description).encode('ascii', 'ignore')
            directions_li_string += LI_HTML.format(direct_description)

        difficulty = dish.get('difficulty')
        preparation_time = dish.get('preparation_time_min')
        rating = recipe.get('rating')

        dish['html_description'] = RECIPE_HTML.format(dish_name, recipe_description, servings_amount,
                                                      ingredients_li_string, directions_li_string, rating, difficulty,
                                                      preparation_time)
