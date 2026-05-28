---
name: fastapi-core-schemas
description: Use this skill when you need to create Pydantic v2 base schemas for consistent request validation and response serialization in FastAPI applications.
---

# FastAPI Core Schemas

## Overview

This skill covers creating base Pydantic v2 schemas for consistent request/response handling across the application.

## Create core/schemas.py

Create `src/app/core/schemas.py`:

```python
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models.

    Configured with:
    - from_attributes: Enables ORM mode (read from SQLAlchemy models)
    - populate_by_name: Allow using field names or aliases
    - str_strip_whitespace: Strip whitespace from string fields
    - validate_default: Validate default values
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_default=True,
    )


class BaseCreateSchema(BaseSchema):
    """
    Base schema for create operations.

    Does NOT include id, timestamps, or deleted_at.
    Only fields that the client provides when creating a resource.
    """

    pass


class BaseUpdateSchema(BaseSchema):
    """
    Base schema for update operations.

    All fields should be Optional to support partial updates (PATCH).
    Does NOT include id, timestamps, or deleted_at.
    """

    pass


class BaseResponseSchema(BaseSchema):
    """
    Base schema for response serialization.

    Includes:
    - id: UUID primary key
    - created_at: Creation timestamp
    - updated_at: Last update timestamp
    """

    id: UUID
    created_at: datetime
    updated_at: datetime


class BaseResponseWithDeletedSchema(BaseResponseSchema):
    """
    Response schema that includes soft delete information.

    Use when the API needs to return deleted_at field,
    such as admin endpoints or trash/archive views.
    """

    deleted_at: datetime | None = None
```

## Usage Example

When creating entity schemas, inherit from the base schemas:

```python
# src/app/items/schemas.py
from uuid import UUID
from pydantic import Field

from app.core.schemas import (
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
)


class ItemCreate(BaseCreateSchema):
    """Schema for creating an item."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    category_id: UUID
```