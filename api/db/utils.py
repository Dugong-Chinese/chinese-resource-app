"""Database utility functions to avoid code repetition"""
from typing import Optional
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from .models import User

def query_users(user_id: Optional[int], email: Optional[str]) -> BaseQuery:
    """Find a user by id and/or email and return the query."""
    return User.query.filter((User.email == email) | (User.id == user_id))
