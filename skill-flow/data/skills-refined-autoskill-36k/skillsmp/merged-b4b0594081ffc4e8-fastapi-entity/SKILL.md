---
name: fastapi-entity
description: Create a new entity with model, schemas, repository, service, router, dependencies, and filters.
---

# FastAPI Entity Creation

## Overview

This skill covers creating a complete entity with all necessary files following the entity-based folder structure. Each entity is self-contained with its own model, schemas, repository, service, router, dependencies, and filters.

## Entity Folder Structure

For an entity named `<entity>`:

```
src/app/<entity>/
├── __init__.py
├── models.py          # SQLAlchemy model
├── schemas.py         # Pydantic schemas
├── repository.py      # Data access layer
├── service.py         # Business logic layer
├── router.py          # API endpoints
├── dependencies.py    # FastAPI dependencies
└── filters.py         # fastapi-filter definitions
```

## Step 1: Create __init__.py

Create `src/app/{entity}/__init__.py`:

```python
from app.<entity>.models import <Entity>
from app.<entity>.repository import <Entity>Repository
from app.<entity>.router import router
from app.<entity>.schemas import <Entity>Create, <Entity>Response, <Entity>Update
from app.<entity>.service import <Entity>Service

__all__ = [
    "<Entity>",
    "<Entity>Create",
    "<Entity>Update",
    "<Entity>Response",
    "<Entity>Repository",
    "<Entity>Service",
    "router",
]
```

## Step 2: Create models.py

Create `src/app/{entity}/models.py`:

```python
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

class <Entity>(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """
    <Entity> model.

    Attributes:
        id: UUID primary key
        name: <Entity> name (required)
        description: <Entity> description (optional)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        deleted_at: Soft delete timestamp
    """

    __tablename__ = "<entity>"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
```

## Step 3: Create schemas.py

Create `src/app/{entity}/schemas.py`:

```python
from pydantic import Field

from app.core.schemas import (
    BaseCreateSchema,
    BaseResponseSchema,
    BaseResponseWithDeletedSchema,
    BaseUpdateSchema,
)

class <Entity>Create(BaseCreateSchema):
    """Schema for creating an <Entity>."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="<Entity> name",
        examples=["My <Entity>"],
    )
    description: str | None = Field(
        default=None,
        max_length=5000,
        description="<Entity> description",
        examples=["A detailed description of the <Entity>"],
    )

class <Entity>Update(BaseUpdateSchema):
    """Schema for updating an <Entity>. All fields optional for PATCH."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="<Entity> name",
    )
    description: str | None = Field(
        default=None,
        max_length=5000,
        description="<Entity> description",
    )

class <Entity>Response(BaseResponseSchema):
    """Schema for <Entity> responses."""

    name: str
    description: str | None

class <Entity>ResponseWithDeleted(BaseResponseWithDeletedSchema):
    """Schema for <Entity> responses including soft delete info."""

    name: str
    description: str | None
```

## Step 4: Create repository.py

Create `src/app/{entity}/repository.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.postgres_repository import PostgresRepository
from app.<entity>.models import <Entity>
from app.<entity>.schemas import <Entity>Create, <Entity>Update

class <Entity>Repository(PostgresRepository[<Entity>, <Entity>Create, <Entity>Update]):
    """
    Repository for <Entity> entity.

    Inherits all CRUD, pagination, filtering, bulk operations,
    and soft delete methods from PostgresRepository.

    Add entity-specific query methods here.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, <Entity>)

    async def get_by_name(self, name: str) -> <Entity> | None:
        """
        Get <Entity> by name.

        Args:
            name: <Entity> name to search for

        Returns:
            <Entity> if found, None otherwise
        """
        return await self.get_by_field("name", name)
```

## Step 5: Create service.py

Create `src/app/{entity}/service.py`:

```python
from uuid import UUID

from app.core.service import BaseService
from app.exceptions import ConflictError, NotFoundError
from app.<entity>.models import <Entity>
from app.<entity>.repository import <Entity>Repository
from app.<entity>.schemas import <Entity>Create, <Entity>Update

class <Entity>Service(BaseService[<Entity>, <Entity>Create, <Entity>Update]):
    """
    Service for <Entity> entity.

    Contains business logic and validation rules.
    Delegates data access to the repository.
    """

    def __init__(self, repository: <Entity>Repository):
        super().__init__(repository)
        self._repository: <Entity>Repository = repository

    async def create(self, obj_in: <Entity>Create) -> <Entity>:
        """
        Create a new <Entity>.

        Validates that the name is unique before creation.

        Args:
            obj_in: <Entity> creation data

        Returns:
            Created <Entity>

        Raises:
            ConflictError: If <Entity> with same name exists
        """
        existing = await self._repository.get_by_name(obj_in.name)
        if existing:
            raise ConflictError(
                resource="<Entity>",
                field="name",
                value=obj_in.name,
            )
        return await super().create(obj_in)

    async def get_by_id_or_raise(self, id: UUID) -> <Entity>:
        """
        Get <Entity> by ID or raise NotFoundError.

        Args:
            id: <Entity> UUID

        Returns:
            <Entity> instance

        Raises:
            NotFoundError: If <Entity> not found
        """
        item = await self.get_by_id(id)
        if not item:
            raise NotFoundError(resource="<Entity>", id=id)
        return item

    async def update(
        self,
        id: UUID,
        obj_in: <Entity>Update,
        exclude_unset: bool = True,
    ) -> <Entity>:
        """
        Update an <Entity>.

        Validates name uniqueness if name is being changed.

        Args:
            id: <Entity> UUID to update
            obj_in: Update data
            exclude_unset: Only update explicitly set fields

        Returns:
            Updated <Entity>

        Raises:
            NotFoundError: If <Entity> not found
            ConflictError: If new name conflicts with existing <Entity>
        """
        await self.get_by_id_or_raise(id)

        if obj_in.name is not None:
            existing = await self._repository.get_by_name(obj_in.name)
            if existing and existing.id != id:
                raise ConflictError(
                    resource="<Entity>",
                    field="name",
                    value=obj_in.name,
                )

        item = await super().update(id, obj_in, exclude_unset)
        if item is None:
            raise NotFoundError(resource="<Entity>", id=id)
        return item

    async def delete_or_raise(self, id: UUID) -> bool:
        """
        Delete an <Entity> or raise if not found.

        Args:
            id: <Entity> UUID to delete

        Returns:
            True if deleted

        Raises:
            NotFoundError: If <Entity> not found
        """
        await self.get_by_id_or_raise(id)
        return await self.delete(id)

    async def soft_delete_or_raise(self, id: UUID) -> bool:
        """
        Soft delete an <Entity> or raise if not found.

        Args:
            id: <Entity> UUID to soft delete

        Returns:
            True if soft deleted

        Raises:
            NotFoundError: If <Entity> not found
        """
        await self.get_by_id_or_raise(id)
        return await self.soft_delete(id)
```

## Step 6: Create filters.py

Create `src/app/{entity}/filters.py`:

```python
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from app.<entity>.models import <Entity>

class <Entity>Filter(Filter):
    """
    Filter specification for <Entity> queries.

    Supports filtering by:
    - name: Exact match
    - name__ilike: Case-insensitive partial match
    - description__ilike: Case-insensitive partial match

    Supports ordering by any field.
    """

    name: Optional[str] = None
    name__ilike: Optional[str] = None
    description__ilike: Optional[str] = None
    order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = <Entity>
        ordering_field_name = "order_by"
```

## Step 7: Create dependencies.py

Create `src/app/{entity}/dependencies.py`:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.<entity>.repository import <Entity>Repository
from app.<entity>.service import <Entity>Service

def get_<entity>_repository(
    session: AsyncSession = Depends(get_db),
) -> <Entity>Repository:
    """
    Dependency that provides a <Entity>Repository instance.

    Args:
        session: Database session from get_db dependency

    Returns:
        <Entity>Repository instance
    """
    return <Entity>Repository(session)

def get_<entity>_service(
    repository: <Entity>Repository = Depends(get_<entity>_repository),
) -> <Entity>Service:
    """
    Dependency that provides a <Entity>Service instance.

    Args:
        repository: <Entity>Repository from get_<entity>_repository dependency

    Returns:
        <Entity>Service instance
    """
    return <Entity>Service(repository)
```

## Step 8: Create router.py

Create `src/app/{entity}/router.py`:

```python
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params

from app.<entity>.dependencies import get_<entity>_service
from app.<entity>.filters import <Entity>Filter
from app.<entity>.models import <Entity>
from app.<entity>.schemas import <Entity>Create, <Entity>Response, <Entity>Update
from app.<entity>.service import <Entity>Service

router = APIRouter(prefix="/<entity>", tags=["<entity>"])

@router.post(
    "",
    response_model=<Entity>Response,
    status_code=status.HTTP_201_CREATED,
    summary="Create <Entity>",
    description="Create a new <Entity> with the provided data.",
)
async def create_<entity>(
    obj_in: <Entity>Create,
    service: <Entity>Service = Depends(get_<entity>_service),
) -> <Entity>:
    """Create a new <Entity>."""
    return await service.create(obj_in)

@router.get(
    "",
    response_model=Page[<Entity>Response],
    summary="List <entity>",
    description="Get a paginated list of <entity> with optional filtering.",
)
async def list_<entity>(
    params: Params = Depends(),
    filter_spec: <Entity>Filter = FilterDepends(<Entity>Filter),
    service: <Entity>Service = Depends(get_<entity>_service),
) -> Page[<Entity>]:
    """List <entity> with pagination and filtering."""
    return await service.get_paginated(params, filter_spec)

@router.get(
    "/{<entity>_id}",
    response_model=<Entity>Response,
    summary="Get <entity>",
    description="Get a single <entity> by ID.",
)
async def get_<entity>(
    <entity>_id: UUID,
    service: <Entity>Service = Depends(get_<entity>_service),
) -> <Entity>:
    """Get <entity> by ID."""
    return await service.get_by_id_or_raise(<entity>_id)

@router.patch(
    "/{<entity>_id}",
    response_model=<Entity>Response,
    summary="Update <entity>",
    description="Update an existing <entity>. Only provided fields will be updated.",
)
async def update_<entity>(
    <entity>_id: UUID,
    obj_in: <Entity>Update,
    service: <Entity>Service = Depends(get_<entity>_service),
) -> <Entity>:
    """Update <entity> by ID."""
    return await service.update(<entity>_id, obj_in)

@router.delete(
    "/{<entity>_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete <entity>",
    description="Soft delete an <entity> by ID.",
)
async def delete_<entity>(
    <entity>_id: UUID,
    service: <Entity>Service = Depends(get_<entity>_service),
) -> None:
    """Soft delete <entity> by ID."""
    await service.soft_delete_or_raise(<entity>_id)

@router.post(
    "/{<entity>_id}/restore",
    response_model=<Entity>Response,
    summary="Restore <entity>",
    description="Restore a soft-deleted <entity>.",
)
async def restore_<entity>(
    <entity>_id: UUID,
    service: <Entity>Service = Depends(get_<entity>_service),
) -> <Entity>:
    """Restore a soft-deleted <entity>."""
    await service.restore(<entity>_id)
    return await service.get_by_id_or_raise(<entity>_id)
```

## Step 9: Register Router

Update `src/app/api/v1/__init__.py`:

```python
from fastapi import APIRouter

from app.<entity>.router import router as <entity>s_router

router = APIRouter()

router.include_router(<entity>s_router)
```

## Step 10: Register Model for Alembic

Update `alembic/env.py`:

```python
# Import models for autogenerate
from app.<entity>.models import <Entity>  # noqa: F401
```

## Step 11: Create Migration

```bash
uv run alembic revision --autogenerate -m "add <entity> table"
uv run alembic upgrade head
```

## Generated API Endpoints

| Method | Path                         | Description            |
| ------ | ---------------------------- | ---------------------- |
| POST   | `/api/v1/<entity>`           | Create <entity>        |
| GET    | `/api/v1/<entity>`           | List <entity> (paginated) |
| GET    | `/api/v1/<entity>/{id}`      | Get <entity> by ID     |
| PATCH  | `/api/v1/<entity>/{id}`      | Update <entity>        |
| DELETE | `/api/v1/<entity>/{id}`      | Soft delete <entity>   |
| POST   | `/api/v1/<entity>/{id}/restore` | Restore <entity>     |

## Query Parameters for List Endpoint

**Pagination:**

- `page`: Page number (default: 1)
- `size`: Items per page (default: 50)

**Filtering:**

- `name`: Exact name match
- `name__ilike`: Case-insensitive name contains
- `description__ilike`: Case-insensitive description contains

**Ordering:**

- `order_by`: Field to order by (prefix with `-` for descending)

**Example:**

```
GET /api/v1/<entity>?page=1&size=20&name__ilike=widget&order_by=-created_at
```

## Adding Relationships

For entities with relationships:

```