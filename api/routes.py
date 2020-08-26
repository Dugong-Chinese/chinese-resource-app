"""Define the main routes of the app.

Documentation for the API, 1.0.0:
    https://app.swaggerhub.com/apis-docs/berzi/dugong-chinese/1.0.0
"""

from flask import Blueprint, request
from flask_restful import Resource, Api
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
    
    def post(self):
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
    
    def delete(self):
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


class Users(Resource):
    """Routes to retrieve and manage user accounts."""
    
    def get(self):
        user_id = request.args.get("user_id", None, type=int)
        email = request.args.get("email", None)
        
        if not user_id and not email:
            return ("A user_id or email GET parameter must be specified."), 400
        
        user = User.query.filter(
            (User.email == email) | (User.id == user_id)
        )
        
        if not user:
            return {}, 404
        
        return {
            "id": user.id,
            "creation_date": user.creation_date,
            "email": user.email,
            "lemmas": user.lemmas,
        }, 200


api.add_resource(Login, "login")
api.add_resource(Users, "users")
