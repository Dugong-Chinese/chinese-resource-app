from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort
from functools import wraps
from flask_cors import CORS

# store reroutes in separate file
from reroutes import reroutes, Index

app = Flask(__name__, static_folder="../build", static_url_path="/")
api = Api(app)
db = SQLAlchemy(app)

cors = CORS(
    app, resources={r"/api/*": {"origins": ["https://mandarin-web-app.herokuapp.com"]}}
)

app.register_blueprint(reroutes)

from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


class User:
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, "user1", "abcxyz"),
    User(2, "user2", "abcdwxyz"),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_table.get(user_id, None)


app.config["SECRET_KEY"] = "super-secret"  # TODO: move to environment variable

jwt = JWT(app, authenticate, identity)


def checkuser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_identity.username == "user1":
            return func(*args, **kwargs)
        return abort(401)

    return wrapper


# GET request, no parameters
class SimpleExample(Resource):
    """Demonstrates simple GET + POST requests."""

    decorators = [checkuser, jwt_required()]

    def get(self):
        # simply have the function name be 'get' and return a dict with the name
        # ("response") and the text that you will send
        return {"response": f"Hello {current_identity.username}!"}

    def post(self):
        # get POST data with request.get_json()
        some_json = request.get_json()  # whatever was posted
        return {"you sent": some_json}


class ComplexExample(Resource):
    """Demonstrates a GET request with parameters."""

    def get(self, num):  # unlimited number of arguments
        return {"result": num * 10}


class ParamExample(Resource):
    """
    Demonstrates a GET request with parameters.
    """

    def get(self):
        """
        Usage: /api/add?add1=5&add2=7 will return 12
        """
        # NOTE: come out as strings
        args = request.args
        add1 = args["add1"]
        add2 = args["add2"]

        return {"result": int(add1) + int(add2)}


# reroute files below
api.add_resource(Index, "/")

# link resources to their respective URLs
api.add_resource(SimpleExample, "/api/test")
# whatever you call the parameter will be the way that it needs to be invoked,
# for example here it would be e.g. ...?num=5
api.add_resource(
    ComplexExample, "/api/multiply/<int:num>"
)  # specify variable type (or typecast)
api.add_resource(ParamExample, "/api/add")


if __name__ == "__main__":
    # Locally, create a sibling file to api.py, "local_settings.py"
    # and put `debug = True` in it to run the API in debug mode.
    # In production, this will automatically default to False.
    try:
        import local_settings

        debug = local_settings.debug
    except (ImportError, AttributeError):
        debug = False
    debug = bool(debug)

    app.run(debug=debug)
