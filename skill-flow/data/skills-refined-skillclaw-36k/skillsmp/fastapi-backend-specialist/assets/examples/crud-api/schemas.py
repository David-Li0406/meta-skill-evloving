"""
SQLAlchemy Database Models for CRUD API
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
