---
name: fastapi-core-models
description: Use this skill when you need to create a SQLAlchemy base model with UUID, timestamp, and soft delete mixins for FastAPI applications.
---

# FastAPI Core Models

## Overview

This skill covers creating the base SQLAlchemy model and reusable mixins for UUID primary keys, timestamps, and soft delete functionality.

## Create core/models.py

Create `src/app/core/models.py`:

```python
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Includes AsyncAttrs for proper async lazy loading support.
    All models should inherit from this class.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.
        Converts CamelCase to snake_case and pluralizes.

        Example: UserProfile -> user_profiles
        """
        import re
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        return f"{name}s"


class UUIDMixin:
    """
    Mixin that adds a UUID primary key.

    Uses PostgreSQL's native UUID type for optimal storage and indexing.
    Generates UUID4 by default.
    """

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        sort_order=-100,  # Ensure id appears first in table
    )


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamps.

    - created_at: Set once when record is created (server-side default)
    - updated_at: Updated automatically on every modification

    All timestamps are timezone-aware UTC.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        sort_order=100,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        sort_order=101,
    )


class SoftDeleteMixin:
    """
    Mixin that adds soft delete functionality.

    - deleted_at: NULL means not deleted, timestamp means deleted
    - Records are never physically deleted, only marked
    """

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
```