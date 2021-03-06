from flask import Flask, request, Response, Blueprint
from encodejson import jsonify
import mongodal
import dailyintakes

mongo = mongodal.MongoDAL()
mongo.connect()

app = Flask(__name__)
collection = "users"
users_controller = Blueprint("users_controller", __name__)


def get_user(username):
    user_dict = {"username": username}

    cursor = mongo.find(collection, user_dict)
    users = [e for e in cursor]
    if len(users) == 0:
        raise Exception("There is no user {0}".format(username))
    elif len(users) == 1:
        return users[0]
    else:
        raise Exception("Why are there more than one {0}".format(username))


@users_controller.route('/user/<username>', methods=['GET'])
def handle_user(username):
    try:
        return jsonify(get_user(username))
    except Exception as err:
        return err


@users_controller.route('/user/<username>/status', methods=['GET'])
def get_user_status(username):
    try:
        user = get_user(username)
        return jsonify(dailyintakes.status(user))
    except Exception as err:
        print 'err: '
        print err
        print err.args
        return jsonify(err)


@users_controller.route('/user/<username>/meals', methods=['GET', 'POST'])  # POST params: { recipe_id: ID }
def get_user_meals(username):
    try:
        user = get_user(username)
        user_dict = {"username": username}
        if request.method == 'GET':
            return jsonify(user['daily_meals'])
        if request.method == 'POST':
            newmeals = [request.form['recipe_id']]
            if 'daily_meals' in user:
                newmeals = newmeals + user['daily_meals']

            mongo.update_one('users', user_dict, newmeals)
    except Exception as err:
        return err


@users_controller.route('/user/<username>/meals/<index>', methods=['DELETE'])
def delete_user_meal(username, index):
    try:
        if request.method == 'DELETE':
            user = get_user(username)
            user_dict = {"username": username}
            newmeals = user['daily_meals'].pop(index)
            return jsonify(mongo.update_one(collection, user_dict, {'daily_meals': newmeals}))
    except Exception as err:
        return err
