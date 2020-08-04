from flask import Flask, request
from flask_restful import Resource, Api, abort
from functools import wraps
from flask_cors import CORS

app = Flask(__name__, static_folder="../build", static_url_path="/")
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://mandarin-web-app.herokuapp.com"]}})

from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcdwxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app.config['SECRET_KEY'] = 'super-secret' # TODO: move to environment variable

jwt = JWT(app, authenticate, identity)

def checkuser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_identity.username == 'user1':
            return func(*args, **kwargs)
        return abort(401)
    return wrapper

# GET request, no parameters
class SimpleExample(Resource):
    """
    Demonstrates simple GET + POST requests.
    """
    decorators = [checkuser, jwt_required()]

    def get(self):
        # simply have the function name be 'get' and return a dict with the name ("response") and the text that you will send
        # TODO: Syntax error, please fix
        # return {"response": f"Hello {current_identity.username}!"}
        return {"response": "Hello Fix me!"}

    def post(self):
        # get POST data with request.get_json()
        some_json = request.get_json()  # whatever was posted
        return {"you sent": some_json}


class ComplexExample(Resource):
    """
    Demonstrates a GET request with parameters.
    """

    def get(self, num):  # unlimited number of arguments
        return {"result": num * 10}


class Index(Resource):
    """
    Serves index from build folder
    """
    def get(self):  # unlimited number of arguments
        return app.send_static_file('index.html')

#index route
api.add_resource(Index, "/")

# link resources to their respective URLs
api.add_resource(SimpleExample, "/api/test")
# whatever you call the parameter will be the way that it needs to be invoked, for example here it would be e.g. ...?num=5
api.add_resource(
    ComplexExample, "/api/multiply/<int:num>"
)  # specify variable type (or typecast)

# if __name__ == "__main__":
#     app.run()
# you can start the server by cding to the directory and running python3 api.py; it will start on localhost:5000 (if not in use)
