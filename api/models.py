"""Database models for the RESTful API."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


db = SQLAlchemy()


# Models and tables for users and authentication in general
lemmas_helper = db.Table(
    "lemmas_to_users_mtm",
    db.Column("lemma_id", db.Integer, db.ForeignKey("lemma.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class Lemma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # content is not set as unique because there might be lemmas of different kinds
    #  that look exactly the same.
    content = db.Column(db.String, nullable=False)
    # TODO difficulty index, depending on how we decide to implement that


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_joined = db.Column(db.DateTime(timezone=True), server_default=text("NOW()"))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)
    lemmas = db.relationship(
        "Lemma", secondary=lemmas_helper, lazy="subquery", backref="users"
    )

    def __repr__(self):
        return f"<Users {self.email}>"


class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_emitted = db.Column(db.DateTime(timezone=True), server_default=text("NOW()"))
    key = db.Column(db.String, unique=True, nullable=False)
    is_revoked = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return (
            f"<API key for user"
            f" {self.user_id} ({'invalid' if self.is_revoked else 'valid'})>"
        )


# Models and tables for resources.
tags_helper = db.Table(
    "tags_to_resources_mtm",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column(
        "resource_id", db.Integer, db.ForeignKey("resource.id"), primary_key=True
    ),
)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime(timezone=True), server_default=text("NOW()"))
    names = db.relationship("ResourceName", backref="resource", lazy=True)
    urls = db.relationship("ResourceURL", backref="resource", lazy=True)
    tags = db.relationship(
        "Tag", secondary=tags_helper, lazy="subquery", backref="resources"
    )
    parent_id = db.Column(db.Integer, db.ForeignKey("resource.id"), nullable=True)


class ResourceName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, unique=True, nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("resource.id"), nullable=False)

    def __repr__(self):
        return f"<Resource Name {self.value} for ID {self.resource_id}>"


class ResourceUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, unique=True, nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("resource.id"), nullable=False)

    def __repr__(self):
        return f"<Resource URL for ID {self.resource_id}: {self.value}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag {self.value}>"
