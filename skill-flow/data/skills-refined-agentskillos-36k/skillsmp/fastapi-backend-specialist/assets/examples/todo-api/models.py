"""
Pydantic Models for Todo API
Request and response schemas
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# ========== Category Models ==========

class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class CategoryCreate(CategoryBase):
    """Schema for creating a category"""
    pass


class Category(CategoryBase):
    """Schema for category response"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========== Todo Models ==========

class TodoBase(BaseModel):
    """Base todo schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False
    category_id: Optional[int] = None


class TodoCreate(TodoBase):
    """Schema for creating a todo"""
    pass


class TodoUpdate(BaseModel):
    """Schema for updating a todo (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
    category_id: Optional[int] = None


class Todo(TodoBase):
    """Schema for todo response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class TodoWithCategory(Todo):
    """Todo with category information"""
    category: Optional[Category] = None


# ========== Pagination Models ==========

class PaginatedTodosResponse(BaseModel):
    """Paginated response for todos"""
    todos: List[TodoWithCategory]
    total: int
    skip: int
    limit: int
