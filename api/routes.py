"""Define the main routes of the app.

Documentation for the API, 1.0.0:
    https://app.swaggerhub.com/apis-docs/berzi/dugong-chinese/1.0.0
"""

from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from models import db, User, APIKey, PermLevel
from security import (
    generate_random_salt,
    hash_password,
    get_or_create_api_key,
    ENCODING,
)
from validators import validate_password, ValidationError, validate_email


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
        """Log the user in, verifying and matching login data to an API key."""
        req_data = request.get_json()
        user = User.query.filter_by(email=req_data["username"]).first()

        # To prevent timing attacks, get fake data and effect normal check operations
        #  even if the user is not found. getattr() is used because user could be None.
        stored_password = getattr(user, "password", None)
        salt = getattr(user, "salt", "N/A")

        hashed_input = hash_password(req_data["password"], salt)

        if hashed_input == stored_password:
            apikey = get_or_create_api_key(user)

            return {"APIKey": apikey.key}, 200

        return ("Password is incorrect or the username entered is not registered.", 401)

    def delete(self):
        """Invalidate the user's API key."""
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

        return (
            "API-Key revoked successfully. A new login will generate a new key with"
            " basic permissions.",
            200,
        )


class Users(Resource):
    """Routes to retrieve and manage user accounts."""

    def get(self):
        """Get data on users."""
        user_id = request.args.get("user_id", None, type=int)
        email = request.args.get("email", None)

        if not user_id and not email:
            return ("A user_id or email GET parameter must be specified."), 400

        user = User.query.filter((User.email == email) | (User.id == user_id))

        if not user:
            return {}, 404

        return (
            {
                "id": user.id,
                "creation_date": user.creation_date,
                "email": user.email,
                "lemmas": user.lemmas,
            },
            200,
        )

    def post(self):
        """Register a new user."""
        req_body = request.get_json()

        not_found = []
        required_fields = ("email", "password")
        for field in required_fields:
            if field not in req_body.keys():
                not_found.append(field)

        if not_found:
            return (
                f"Required field(s) not found:"
                f" {', '.join(field for field in not_found)}",
                400,
            )

        # Check if email is valid
        user_email = req_body["email"]
        try:
            validate_email(user_email)
        except ValidationError:
            return "Incorrect format for field: email", 400

        # Check if password is secure enough
        user_password = req_body["password"]
        try:
            validate_password(user_password)
        except ValidationError:
            return (
                "Password is not secure enough: include at least one uppercase,"
                " one lowercase, one number and one symbol, and keep it between"
                " 12 and 255 characters long. Whitespace is not allowed.",
                400,
            )

        salt = generate_random_salt()
        hashed_password = hash_password(user_password, salt)

        # noinspection PyArgumentList
        new_user = User(
            email=user_email,
            password=hashed_password,
            salt=str(salt, encoding=ENCODING),
        )
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            return {}, 409

        apikey = get_or_create_api_key(new_user)

        return apikey, 201


api.add_resource(Login, "login")
api.add_resource(Users, "users")
