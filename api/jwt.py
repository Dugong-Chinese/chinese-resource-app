"""Initialisation of JSON Token authentication."""

from flask_jwt import JWT
from werkzeug.security import safe_str_cmp


class User:
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __str__(self):
        return f"User(id='{self.id}')"


USERS = [
    User(1, "user1", "abcxyz"),
    User(2, "user2", "abcdwxyz"),
]

username_table = {u.username: u for u in USERS}
userid_table = {u.id: u for u in USERS}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_table.get(user_id, None)


jwt = JWT(authentication_handler=authenticate, identity_handler=identity)
