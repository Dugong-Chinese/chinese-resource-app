"""Security utilities used for authentication etc."""

import hashlib
import secrets
from local_settings import settings
from typing import Union
from models import db, User, APIKey, PermLevel


ENCODING = "utf-8"


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
    
    Since the user ID is needed, the user must be already committed to the database.
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
