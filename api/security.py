"""Security utilities used for authentication etc."""

import hashlib
import secrets
from local_settings import settings
from models import User


ENCODING = "utf-8"


def utf8_to_bytes(string: str) -> bytes:
    return bytes(string, encoding=ENCODING)


def hash_password(password: str, salt: str) -> str:
    """Hash a password with the given salt."""
    hasher = hashlib.sha3_256()
    hasher.update(utf8_to_bytes(password))
    hasher.update(utf8_to_bytes(salt))
    hasher.update(utf8_to_bytes(settings["SECRET_KEY"]))
    
    return str(hasher.digest(), encoding=ENCODING)


def generate_apikey(user: User) -> str:
    """Generate a new API key for a user."""
    hasher = hashlib.sha3_512()
    hasher.update(utf8_to_bytes(user.email))
    hasher.update(secrets.token_bytes())
    
    return str(hasher.digest(), encoding=ENCODING)
