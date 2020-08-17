"""Database models for the RESTful API."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import ARRAY
import enum


db = SQLAlchemy()


class BaseModel:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


# Models and tables for users and authentication in general
lemmas_helper = db.Table(
    "lemmas_to_users_mtm",
    db.Column("lemma_id", db.Integer, db.ForeignKey("lemma.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class LemmaType(enum.IntEnum):
    """Type of lemma, meant to be used in arrays as lemmas can have multiple types.
    An unknown type is represented by an empty array.
    
    Remember to use LemmaType.SOMETYPE.value when inserting or comparing database data,
    as the column itself technically accepts integers.
    """

    NOUN = enum.auto()
    ADJECTIVE = enum.auto()
    VERB = enum.auto()
    PARTICLE = enum.auto()
    IDIOM = enum.auto()


class Lemma(BaseModel, db.Model):
    """A single lemma: a word, idiom, expression or grammatical construction."""

    # `content` is not set as unique because there might be lemmas of different kinds
    #  that look exactly the same.
    content = db.Column(db.String, nullable=False)

    # Type is encoded as integer and not array because of implementation and performance
    #  issues due to SQLAlchemy and PostgreSQL.
    type_ = db.Column(ARRAY(db.SmallInteger), name="type", default=[])
    # TODO difficulty index, depending on how we decide to implement that


class User(BaseModel, db.Model):
    """A user on the platform."""

    date_joined = db.Column(db.DateTime(timezone=True), server_default=text("NOW()"))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)
    lemmas = db.relationship(
        "Lemma", secondary=lemmas_helper, lazy="subquery", backref="users"
    )

    def __repr__(self):
        return f"<Users {self.email}>"


class PermLevel(enum.IntEnum):
    """Actions permitted by a certain key.
    
    Remember to use PermLevel.SOMEVALUE.value; see documentation on LemmaType enum.
    """

    REVOKED = enum.auto()
    READ = enum.auto()
    EDIT = enum.auto()
    CREATE = enum.auto()
    ADMIN = enum.auto()


class APIKey(BaseModel, db.Model):
    """An API-key associated to a user and needed to access the API."""

    date_emitted = db.Column(db.DateTime(timezone=True), server_default=text("NOW()"))
    key = db.Column(db.String, unique=True, nullable=False)
    level = db.Column(db.SmallInteger, nullable=False, default=PermLevel.READ.value)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return (
            f"<API key for user"
            f" {self.user_id} ({'invalid' if self.is_revoked else 'valid'})>"
        )


# Models and tables for resources.
tags_helper = db.Table(
    "tags_to_resources_mtm",
    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey("tag.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "resource_id",
        db.Integer,
        db.ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Resource(BaseModel, db.Model):
    """A learning resource on the platform."""

    date_added = db.Column(db.DateTime(timezone=True), server_default=text("NOW()"))
    upvotes = db.Column(db.Integer, nullable=False, default=0)
    downvotes = db.Column(db.Integer, nullable=False, default=0)
    names = db.relationship("ResourceName", backref="resource", lazy=True)
    urls = db.relationship("ResourceURL", backref="resource", lazy=True)
    tags = db.relationship(
        "Tag", secondary=tags_helper, lazy="subquery", backref="resources"
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )


class ResourceName(BaseModel, db.Model):
    """One name for a resource on the platform."""

    value = db.Column(db.String, unique=True, nullable=False)
    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    def __repr__(self):
        return f"<Resource Name {self.value} for ID {self.resource_id}>"


class ResourceUrl(BaseModel, db.Model):
    """One URL to the concrete document or page representing a learning resource."""

    value = db.Column(db.String, unique=True, nullable=False)
    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    def __repr__(self):
        return f"<Resource URL for ID {self.resource_id}: {self.value}>"


class Tag(BaseModel, db.Model):
    """A tag to classify learning resources."""

    value = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag {self.value}>"


class Review(BaseModel, db.Model):
    """A user review on a learning resource."""

    content = db.Column(db.String, nullable=False)
    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
