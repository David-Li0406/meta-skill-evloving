---
name: fastapi-core-service
description: Use this skill when you need to create a base service class that wraps repository operations and provides business logic hooks in a FastAPI application.
---

# FastAPI Core Service

## Overview

This skill covers creating the base service class that acts as an intermediary between routers and repositories. Services contain business logic and orchestrate repository calls.

## Create core/service.py

Create `src/app/core/service.py`:

```python
from collections.abc import Sequence
from typing import Generic
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage

from app.core.repository import (
    AbstractRepository,
    CreateSchemaType,
    ModelType,
    UpdateSchemaType,
)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base service class providing standard CRUD operations.

    Services:
    - Wrap repository operations
    - Contain business logic
    - Orchestrate multiple repository calls
    - Handle cross-cutting concerns (logging, events, etc.)

    Services should NOT:
    - Write SQL queries (delegate to repository)
    - Handle HTTP concerns (that's the router's job)
    - Access the database session directly

    Type Parameters:
        ModelType: SQLAlchemy model class
        CreateSchemaType: Pydantic schema for create operations
        UpdateSchemaType: Pydantic schema for update operations

    Usage:
        class ItemService(BaseService[Item, ItemCreate, ItemUpdate]):
            pass
    """

    def __init__(
        self,
        repository: AbstractRepository[ModelType, CreateSchemaType, UpdateSchemaType],
    ):
        """
        Initialize service with repository.

        Args:
            repository: Repository instance for data access
        """
        self._repository = repository

    # ==================== Basic CRUD ====================

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Override to add business logic before/after creation.

        Args:
            obj_in: Creation data

        Returns:
            Created model instance
        """
        return await self._repository.create(obj_in)

    async def get_by_id(self, id: UUID) -> ModelType | None:
        """
        Get a single record by ID.

        Args:
            id: UUID of the record

        Returns:
            Model instance if found, None
        """
        return await self._repository.get_by_id(id)
```