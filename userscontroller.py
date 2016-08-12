from flask import Flask, request, Response, jsonify
import mongodal

mongo = mongodal.MongoDAL()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "hello niggas"


@app.route('/user/<username>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def handle_user(username):
    user_dict = {"username": username}
    collection = "users"
    mongo.connect()

    if request.method == 'GET':
        cursor = mongo.find(collection, user_dict)
        users = [e for e in cursor]
        if len(users) == 0:
            return "There is no user {0}".format(username)
        elif len(users) == 1:
            return str(users[0])
        else:
            return "Why are there more than one {0}".format(username)

    mongo.disconnect()

app.run('0.0.0.0', 8080)
