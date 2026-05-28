"""
SQLModel Models Template

Usage:
1. Copy this file to your project as app/models.py
2. Customize the Task model or add your own models
3. Import models in your routes
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# === DATABASE MODELS ===
class Task(SQLModel, table=True):
    """Task model - user's tasks stored in the database.

    The user_id field links to the Better Auth user via JWT 'sub' claim.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # From JWT 'sub' claim
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# === REQUEST MODELS ===
class TaskCreate(SQLModel):
    """Request model for creating tasks."""

    title: str
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    """Request model for updating tasks.

    All fields are optional - only provided fields will be updated.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# === RESPONSE MODELS ===
class TaskRead(SQLModel):
    """Response model for tasks."""

    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime
