"""Factory functions to instantiate the app while avoiding circular imports."""

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from models import db
from cors import cors
from jwt import jwt
from reroutes import reroutes
from routes import routes


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

    try:
        from local_settings import settings

        app.config.update(settings)
    except (ImportError, AttributeError):
        pass


def register_extensions(app: Flask):
    """Register the database, any blueprint and other extensions."""
    db.init_app(app)
    Migrate(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(reroutes)
    app.register_blueprint(routes)

    Api(app)
