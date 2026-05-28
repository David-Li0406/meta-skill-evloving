"""
Pydantic Models for CRUD API
Request and response schemas
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)


class UserCreate(UserBase):
    """Schema for creating a user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user (all fields optional)"""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)


class User(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
