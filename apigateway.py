from flask import Flask
from dishescontroller import dishes_controller
from userscontroller import users_controller


app = Flask(__name__)

app.register_blueprint(dishes_controller, url_prefix='/dishes')
app.register_blueprint(users_controller, url_prefix='/users')


if __name__ == "__main__":
    app.run("0.0.0.0", 9000)
