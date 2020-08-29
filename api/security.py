"""Security utilities used for authentication etc."""

import hashlib
import secrets
from functools import wraps
from flask import request
from local_settings import settings
from typing import Tuple, Union, Literal
from models import db, User, APIKey, PermLevel, query_users


ENCODING = "utf-8"


class AuthorisationError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code

    def as_tuple(self) -> Tuple[str, int]:
        return self.message, self.code


def utf8_to_bytes(string: str) -> bytes:
    return bytes(string, encoding=ENCODING)


def hash_password(password: str, salt: Union[str, bytes]) -> str:
    """Hash a password with the given salt."""
    hasher = hashlib.sha3_256()
    hasher.update(utf8_to_bytes(password))
    hasher.update(utf8_to_bytes(salt) if isinstance(salt, str) else salt)
    hasher.update(utf8_to_bytes(settings["SECRET_KEY"]))

    return str(hasher.digest(), encoding=ENCODING)


def generate_apikey(user_email: str) -> str:
    """Generate a new API key for a user."""
    hasher = hashlib.sha3_512()
    hasher.update(utf8_to_bytes(user_email))
    hasher.update(secrets.token_bytes())

    return str(hasher.digest(), encoding=ENCODING)


def generate_random_salt() -> bytes:
    """Generate a random salt for use with hashing passwords."""
    hasher = hashlib.sha3_256()
    hasher.update(secrets.token_bytes(256))

    return hasher.digest()


def get_or_create_api_key(user: User) -> APIKey:
    """Get the API key for the selected user or create a new one if needed.
    
    Since the user ID is needed, the user object must have already been committed to the
    database.
    """

    if not user.id:
        raise ValueError(
            "User object must be committed to db before generating an API key."
        )

    user_id = user.id
    apikey = APIKey.query.filter_by(user_id=user_id).order_by(APIKey.id.desc()).first()

    if not apikey or apikey.level == PermLevel.REVOKED.value:
        # noinspection PyArgumentList
        apikey = APIKey(
            key=generate_apikey(user), level=PermLevel.READ.value, user_id=user_id,
        )
        db.session.add(apikey)
        db.session.commit()

    return apikey


def verify_api_key(auth_header: str) -> Union[Literal[False], APIKey]:
    """Check an Authorization token for an API key. Return the key if valid and found in
    the database, False otherwise.
    """

    # A correct header looks like `Bearer APIKEYHERE`
    key_type, _, key = auth_header.partition(" ")

    if not key or key_type != "Bearer":
        return False

    key = key.strip()

    # First, check if the key belongs to any user
    key_in_db = APIKey.query.filter_by(key=key).first()

    if not key_in_db:
        return False

    return key_in_db


def get_api_key_or_raise():
    """Get the API key value from the request header. Raise AuthorisationError if
     not valid.
    """

    key_parts = request.headers.get("Authorization", "")
    key = verify_api_key(key_parts)
    if not key or key.level == PermLevel.REVOKED.value:
        raise AuthorisationError("Login is required for this operation.", 401)

    return key


def only_users(func):
    """Decorator for endpoints that require an API key to be accessed.
    Requires the endpoint to accept a keyword argument `apikey`.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            key = get_api_key_or_raise()
        except AuthorisationError as e:
            return e.as_tuple()

        return func(*args, apikey=key, **kwargs)

    return wrapped


def only_admin_or_self(func):
    """Decorator for endpoints that users can only apply to themselves unless admin.
    Requires the endpoint to accept a keyword argument `user` or **kwargs.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            key = get_api_key_or_raise()
        except AuthorisationError as e:
            return e.as_tuple()

        user_id = request.args.get("user_id", None, type=int)
        email = request.args.get("email", None)

        if not user_id and not email:
            return "A user_id or email GET parameter must be specified.", 400

        user = query_users(user_id, email).first()
        if not user:
            return {}, 404

        # If not admin, can only patch own account.
        if key.level < PermLevel.ADMIN:
            calling_user = User.query.get(key.user_id)
            if calling_user != user:
                return (
                    "Insufficient authorization. You can only patch your own"
                    " account.",
                    403,
                )

        return func(*args, user=user, **kwargs)

    return wrapped
