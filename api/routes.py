"""Define the main routes of the app.

Documentation for the API, 1.0.0:
    https://app.swaggerhub.com/apis-docs/berzi/dugong-chinese/1.0.0
"""

from flask import Blueprint, request
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError
from models import db, Lemma, User, PermLevel
from security import (
    generate_random_salt,
    hash_password,
    get_or_create_api_key,
    ENCODING,
    only_users,
    only_admin_or_self,
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

    @only_users
    def delete(self, apikey):
        """Invalidate the user's API key."""
        apikey.level = PermLevel.REVOKED.value
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

        users = self._query_users(user_id, email).all()

        if not users:
            return {}, 404

        return (
            [
                {
                    "id": u.id,
                    "creation_date": u.creation_date,
                    "email": u.email,
                    "lemmas": u.lemmas,
                }
                for u in users
            ],
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

    @only_admin_or_self
    def patch(self, user):
        """Edit individual fields on a user. Non-admins can only edit some fields on
        their own account.
        """

        req_data = request.get_json()
        invalid_fields = []
        for key in req_data:
            if not hasattr(user, key) or key in ("id", "salt"):
                invalid_fields.append(key)
                continue

            if not invalid_fields:
                if key == "email":
                    new_email = req_data[key]
                    try:
                        validate_email(new_email)
                    except ValidationError:
                        return "Invalid format for email address.", 400
                    user.email = new_email
                elif key == "password":
                    new_password = req_data[key]
                    try:
                        validate_password(new_password)
                    except ValidationError:
                        return "New password is not secure enough or too long.", 400
                    new_salt = generate_random_salt()
                    user.password = hash_password(new_password, new_salt)
                    user.salt = new_salt
                elif key == "lemmas":
                    lemma_refs = req_data[key]
                    if isinstance(lemma_refs[0], int):
                        lemma_filter = Lemma.id.in_(lemma_refs)
                    else:
                        lemma_filter = Lemma.content.in_(lemma_refs)
                    lemmas = Lemma.query.filter(lemma_filter)
                    user.lemmas.extend(lemmas)

        if invalid_fields:
            return f"Invalid fields: {', '.join(invalid_fields)}", 400

        db.session.commit()

        return {}, 204

    @only_admin_or_self
    def delete(self, user):
        """Delete the user account."""
        db.session.delete(user)
        db.session.commit()

        return {}, 204


api.add_resource(Login, "login")
api.add_resource(Users, "users")
