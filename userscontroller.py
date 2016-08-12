from flask import Flask, request, Response, jsonify
import mongodal

mongo = mongodal.MongoDAL()
app = Flask(__name__)
collection = "users"

@app.route('/', methods=['GET'])
def home():
    return "hello niggas"


def update_one(collection, where, set_value):
    mongo.connect()
    db = mongo.db()

    result = db[collection].update_one(
        where,
        {
            "$set": set_value,
            "$currentDate": {"lastModified": True}
        }
    )

    return result

    mongo.disconnect()


def get_user(username):
    user_dict = {"username": username}
    mongo.connect()

    cursor = mongo.find(collection, user_dict)
    users = [e for e in cursor]
    if len(users) == 0:
        raise Exception("There is no user {0}".format(username))
    elif len(users) == 1:
        return users[0]
    else:
        raise Exception("Why are there more than one {0}".format(username))

    mongo.disconnect()


@app.route('/user/<username>', methods=['GET'])
def handle_user(username):
    try:
        return str(get_user(username))
    except Exception as err:
        return err


@app.route('/user/<username>/status', methods=['GET'])
def get_user_status(username):
    try:
        user = get_user(username)
        #TODO:elad
        user['daily_meals']
    except Exception as err:
        return err


@app.route('/user/<username>/meals', methods=['GET'])
def get_user_meals(username):
    try:
        if request.method == 'GET':
            user = get_user(username)
            return str(user['daily_meals'])
    except Exception as err:
        return err


@app.route('/user/<username>/meals/<index>', methods=['DELETE'])
def delete_user_meal(username, index):
    try:
        if request.method == 'DELETE':
            user = get_user(username)
            user_dict = {"username": username}
            newmeals = user['daily_meals'].pop(index)
            return str(update_one(collection, user_dict, {'daily_meals': newmeals}))
    except Exception as err:
        return err




app.run('0.0.0.0', 8080)
