"""Factory functions to instantiate the app while avoiding circular imports."""

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from db import db
from cors import cors
from reroutes import reroutes
from routes import routes
from exercises.blank_fill import blank_exercises
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


def create_app() -> Flask:
    """Instantiate the app."""
    app = Flask(__name__, static_folder="../build", static_url_path="/")

    # Settings are loaded before and after extensions just in case some extensions
    #  need Flask settings to be already in place at init time.
    load_settings(app)
    register_extensions(app)
    load_settings(app)

    return app


def load_settings(app: Flask):
    """Load all settings for the app from local_settings.py in a dict called `settings`.
    The operation is skipped if the file or the dict are not found, and Flask will use
    default configuration.
    
    Settings reference for Flask:
    https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values
    """
    app.config["SECRET_KEY"] = "super-secret"

    try:
        from local_settings import settings

        app.config.update(settings)
    except (ImportError, AttributeError):
        pass


def register_extensions(app: Flask):
    """Register the database, any blueprint and other extensions."""
    db.init_app(app)
    Migrate(app, db)
    cors.init_app(app, resources=app.config["CORS_RESOURCES"])

    JWT(app, authentication_handler=authenticate, identity_handler=identity)

    # Blueprints
    app.register_blueprint(reroutes)
    app.register_blueprint(routes)
    app.register_blueprint(blank_exercises)

    Api(app)
