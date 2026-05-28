---
name: fastapi-postgres-repository
description: Use this skill when you need to implement a PostgreSQL repository with support for bulk upserts, soft delete filtering, and integration with FastAPI pagination and filtering.
---

# FastAPI PostgreSQL Repository Implementation

## Overview

This skill covers the implementation of a PostgreSQL repository that supports all CRUD operations, bulk upserts using ON CONFLICT, soft delete filtering, and integration with FastAPI pagination and filtering.

## Create common/postgres_repository.py

Create `src/app/common/postgres_repository.py`:

```python
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any, Generic
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Base, SoftDeleteMixin
from app.core.repository import (
    AbstractRepository,
    CreateSchemaType,
    ModelType,
    UpdateSchemaType,
)

class PostgresRepository(
    AbstractRepository[ModelType, CreateSchemaType, UpdateSchemaType],
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
):
    """
    PostgreSQL implementation of the abstract repository.

    Provides full CRUD operations with:
    - Automatic soft delete filtering
    - PostgreSQL-specific bulk upsert (ON CONFLICT)
    - FastAPI pagination integration
    - FastAPI filter integration

    Usage:
        class ItemRepository(PostgresRepository[Item, ItemCreate, ItemUpdate]):
            pass
    """

    def __init__(self, session: AsyncSession, model: type[ModelType]):
        """
        Initialize repository with database session and model class.

        Args:
            session: SQLAlchemy async session
            model: SQLAlchemy model class
        """
        self._session = session
        self._model = model

    @property
    def _has_soft_delete(self) -> bool:
        """Check if model supports soft delete."""
        return issubclass(self._model, SoftDeleteMixin)

    def _base_query(self, include_deleted: bool = False):
        """
        Create base SELECT query with optional soft delete filtering.

        Args:
            include_deleted: If True, include soft-deleted records
        """
        # Implementation of the base query goes here
```