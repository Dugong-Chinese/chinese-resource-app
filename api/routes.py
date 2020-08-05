"""Define the main routes of the app."""

from flask import Blueprint
from flask_restful import Resource, Api, abort
from functools import wraps
from flask_jwt import jwt_required, current_identity


routes = Blueprint(
    "routes",
    __name__,
    static_folder="../build",
    static_url_path="/",
)


def checkuser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_identity.username == "user1":
            return func(*args, **kwargs)
        return abort(401)

    return wrapper


class SimpleExample(Resource):
    """Demonstrates simple GET + POST requests."""

    decorators = [checkuser, jwt_required()]

    def get(self):
        # simply have the function name be 'get' and return a dict with the name
        # ("response") and the text that you will send
        return {"response": f"Hello {current_identity.username}!"}

    def post(self, request):
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

    def get(self, request):
        """
        Usage: /api/add?add1=5&add2=7 will return 12
        """
        # NOTE: come out as strings
        args = request.args
        add1 = args["add1"]
        add2 = args["add2"]

        return {"result": int(add1) + int(add2)}


api = Api()
api.add_resource(Index, "/")
# link resources to their respective URLs
api.add_resource(SimpleExample, "/api/test")
# whatever you call the parameter will be the way that it needs to be invoked,
# for example here it would be e.g. ...?num=5
api.add_resource(
    ComplexExample, "/api/multiply/<int:num>"
)  # specify variable type (or typecast)
api.add_resource(ParamExample, "/api/add")
