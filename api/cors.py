"""Initialise Cross-Origin Resource Sharing."""

from flask_cors import CORS

cors = CORS(
    resources={r"/api/*": {"origins": ["https://mandarin-web-app.herokuapp.com"]}},
)
