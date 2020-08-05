"""Factory functions to instantiate the app while avoiding circular imports."""

from flask import Flask
from models import db
from cors import cors
from jwt import jwt
from routes import api
from reroutes import reroutes


def create_app() -> Flask:
    """Instantiate the app."""
    app = Flask(__name__, static_folder="../build", static_url_path="/")
    register_extensions(app)
    return app


def register_extensions(app: Flask):
    """Register the database, any blueprint and other extensions."""
    db.init_app(app)
    cors.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    
    # Blueprints
    app.register_blueprint(reroutes)
