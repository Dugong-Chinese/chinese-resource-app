from flask import Blueprint
from flask_restful import Resource


reroutes = Blueprint(
    "reroutes",
    __name__,
    static_folder="../build",
    static_url_path="/",
)


class Index(Resource):
    """Serves index from build folder."""

    def get(self):
        return reroutes.send_static_file("index.html")
