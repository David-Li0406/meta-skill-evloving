"""
SQLAlchemy Database Models for Todo API
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Category(Base):
    """Category database model"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(7), nullable=True)  # Hex color code
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    todos = relationship("Todo", back_populates="category", cascade="all, delete-orphan")


class Todo(Base):
    """Todo database model"""
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="todos")
