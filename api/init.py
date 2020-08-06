"""Factory functions to instantiate the app while avoiding circular imports."""

from flask import Flask
from flask_restful import Api
from models import db
from cors import cors
from jwt import jwt
from reroutes import reroutes, Index
from routes import routes, SimpleExample, ComplexExample, ParamExample


def create_app() -> Flask:
    """Instantiate the app."""
    app = Flask(__name__, static_folder="../build", static_url_path="/")
    register_extensions(app)
    return app


def register_extensions(app: Flask):
    """Register the database, any blueprint and other extensions."""
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    # Routes
    api = Api(app)
    api.add_resource(Index, "/")
    api.add_resource(SimpleExample, "/test")
    api.add_resource(ComplexExample, "/multiply/<int:num>")
    api.add_resource(ParamExample, "/add")

    # Blueprints
    app.register_blueprint(reroutes)
    app.register_blueprint(routes)
