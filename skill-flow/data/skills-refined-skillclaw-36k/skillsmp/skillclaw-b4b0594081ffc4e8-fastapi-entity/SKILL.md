---
name: fastapi-entity
description: Use this skill when you need to create a new entity in a FastAPI application, including all necessary components like models, schemas, repositories, services, routers, dependencies, and filters.
---

# FastAPI Entity Creation

## Overview

This skill covers creating a complete entity with all necessary files following the entity-based folder structure. Each entity is self-contained with its own model, schemas, repository, service, router, dependencies, and filters.

## Entity Folder Structure

For an entity named `items`:

```
src/app/items/
├── __init__.py
├── models.py          # SQLAlchemy model
├── schemas.py         # Pydantic schemas
├── repository.py      # Data access layer
├── service.py         # Business logic layer
├── router.py          # API endpoints
├── dependencies.py    # FastAPI dependencies
└── filters.py         # fastapi-filter definitions
```

## Step 1: Create `__init__.py`

Create `src/app/{entity}/__init__.py`:

```python
from app.items.models import Item
from app.items.repository import ItemRepository
from app.items.router import router
from app.items.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.items.service import ItemService

__all__ = [
    "Item",
    "ItemCreate",
    "ItemUpdate",
    "ItemResponse",
    "ItemRepository",
    "ItemService",
    "router",
]
```

## Step 2: Create `models.py`

Create `src/app/{entity}/models.py`:

```python
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Item(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """
    Item model.

    Attributes:
        id: UUID primary key
        name: Item name (required)
        description: Item description (optional)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        deleted_at: Soft delete timestamp
    """

    __tablename__ = "items"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
```

## Step 3: Create `schemas.py`

Create `src/app/{entity}/schemas.py`:

```python
from pydantic import Field

from app.core.schemas import (
    BaseCreateSchema,
    BaseResponseSchema,
    BaseResponseWithDeletedSchema,
    BaseUpdateSchema,
)


class ItemCreate(BaseCreateSchema):
    """Schema for creating an item."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Item name",
        example="Sample Item"
    )
```