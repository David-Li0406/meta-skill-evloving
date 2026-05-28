---
name: fastapi-core-repository
description: Use this skill when you need to create an abstract base repository interface for data access operations in a FastAPI application.
---

# FastAPI Core Repository (Abstract)

## Overview

This skill covers creating the abstract base repository that defines the interface for all data access operations. This is the contract that concrete implementations must follow.

## Create core/repository.py

Create `src/app/core/repository.py`:

```python
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage
from pydantic import BaseModel

from app.core.models import Base

# Type variables for generic repository
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class AbstractRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Abstract base repository defining the interface for data access.

    This is the ONLY place where SQL/database operations should be defined.
    All methods are async and work with SQLAlchemy models.

    Type Parameters:
        ModelType: SQLAlchemy model class
        CreateSchemaType: Pydantic schema for create operations
        UpdateSchemaType: Pydantic schema for update operations
    """

    # ==================== Basic CRUD ====================

    @abstractmethod
    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            obj_in: Pydantic schema with creation data

        Returns:
            Created model instance with generated id and timestamps
        """
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> ModelType | None:
        """
        Get a single record by ID.

        Args:
            id: UUID primary key

        Returns:
            Model instance if found, None otherwise

        Note:
            Excludes soft-deleted records by default.
        """
        ...

    @abstractmethod
    async def get_all(self) -> Sequence[ModelType]:
        """
        Get all records.

        Returns:
            Sequence of all model instances

        Note:
            Excludes soft-deleted records by default.
        """
        ...
```