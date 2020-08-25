"""Blueprint for local settings. Copy this file and rename to `local_settings.py`
before editing with your local settings.

DO NOT push your local settings and secret key to the repo: ensure `local_settings.py`
is ignored by Git.

You can override these settings by setting identically named environment variables.
Check Flask setting names here:
    https://flask.palletsprojects.com/en/1.1.x/config/#builtin-configuration-values
 then add any additional setting for extensions.
"""

import os
from flask import Flask


DEBUG = False

settings = {
    # For security. DO NOT reuse the same secret key in production as in development
    # DO NOT divulge nor include in version control.
    # NOTE: Changing the secret key causes all existing registered users to fail
    #  authentication.
    "SECRET_KEY": "",
    # Flask-SQLAlchemy
    # Format: protocol+backend://user:password@host:port/database, many parts optional
    "SQLALCHEMY_DATABASE_URI": "postgresql://localhost:5432",
    "SQLALCHEMY_ECHO": DEBUG,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,  # Removes unneeded overhead.
}

for k, initial in Flask(__name__).config.items():
    settings[k] = os.environ.get(k, settings.get(k, initial))
