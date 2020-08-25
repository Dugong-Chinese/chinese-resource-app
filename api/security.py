"""Security utilities used for authentication etc."""

import hashlib
from local_settings import settings


def hash_password(password: str, salt: str) -> str:
    """Hash a password with the given salt."""
    hasher = hashlib.sha3_256()
    encoding = "utf-8"
    hasher.update(bytes(password, encoding))
    hasher.update(bytes(salt, encoding))
    hasher.update(bytes(settings["SECRET_KEY"], encoding))
    
    return str(hasher.digest())
