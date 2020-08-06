"""Database models for the RESTful API."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_joined = db.Column(db.DateTime(timezone=True), server_default=text("NOW()"))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)
    # TODO known vocabulary

    def __repr__(self):
        return f"<Users {self.email}>"
