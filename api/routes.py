"""Define the main routes of the app.

Documentation for the API, 1.0.0:
    https://app.swaggerhub.com/apis-docs/berzi/dugong-chinese/1.0.0
"""

from flask import Blueprint, request as flask_request
from flask_restful import Resource, abort, Api
from functools import wraps
from flask_jwt import jwt_required, current_identity
from models import db, User, APIKey, PermLevel
from security import hash_password, generate_apikey


routes = Blueprint(
    "routes",
    __name__,
    static_folder="../build",
    static_url_path="/",
    url_prefix="/api/",  # This applies to all resources in this blueprint.
)

api = Api(routes)


class Login(Resource):
    """Routes for login purposes."""
    
    def post(self, request):
        req_data = request.get_json()
        user = User.query.filter_by(email=req_data["username"]).first()
        
        # To prevent timing attacks, get fake data and effect normal check operations
        #  even if the user is not found. getattr() is used because user could be None.
        stored_password = getattr(user, "password", "N/A")
        salt = getattr(user, "salt", "N/A")
        
        hashed_input = hash_password(req_data["password"], salt)
        
        if hashed_input == stored_password:
            user_id = getattr(user, "id", -1)
            apikey = APIKey.query.filter_by(user_id=user_id).first()
            
            if not apikey or apikey.level == PermLevel.REVOKED.value:
                # noinspection PyArgumentList
                apikey = APIKey(
                    generate_apikey(user),
                    PermLevel.READ.value,
                    user.id,
                )
                db.session.add(apikey)
                db.session.commit()
            
            return {"APIKey": apikey.key}, 200
        
        return ("Password is incorrect or the username entered is not registered.", 401)
    
    def delete(self, request):
        key_parts = request.headers.get("Authorization", "")
        # A correct header looks like `Bearer APIKEYHERE`
        key_type, _, key = key_parts.partition(" ")
        
        if not key or key_type != "Bearer":
            return "This content requires an authenticated user.", 401
        
        key = key.strip()
        
        # First, check if the key belongs to any user
        key_in_db = APIKey.query.filter_by(key=key).first()
        
        if not key_in_db or key_in_db.level == PermLevel.REVOKED.value:
            return {}, 404
        
        key_in_db.level = PermLevel.REVOKED.value
        db.session.commit()
        
        return ("API-Key revoked successfully. A new login will generate a new key with"
                " basic permissions.", 200)


api.add_resource(Login, "login")
# TODO delete below this


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
    """Demonstrates a GET request with a dynamic route."""

    def get(self, num):  # unlimited number of arguments
        return {"result": num * 10}


class ParamExample(Resource):
    """Demonstrates a GET request with parameters."""

    def get(self):
        """Usage: /api/add?add1=5&add2=7 will return 12"""
        # NOTE: come out as strings
        args = flask_request.args
        add1 = args["add1"]
        add2 = args["add2"]

        return {"result": int(add1) + int(add2)}


# add resources within Blueprint
api.add_resource(ComplexExample, "multiply/<int:num>")
api.add_resource(SimpleExample, "test")
api.add_resource(ParamExample, "add")
