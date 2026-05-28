# TDD Workflow: Red-Green-Refactor

## The TDD Cycle

```
    ┌─────────────────────────────────────┐
    │                                     │
    ▼                                     │
┌───────┐     ┌───────┐     ┌──────────┐  │
│  RED  │ ──▶ │ GREEN │ ──▶ │ REFACTOR │ ─┘
└───────┘     └───────┘     └──────────┘
Write         Write          Optimize
failing       minimal        without
test          code           breaking
```

## Step 1: RED - Write Failing Test First

Write a test that defines expected behavior. It MUST fail initially.

```python
# tests/test_items.py
import pytest
from httpx import AsyncClient
from pydantic import BaseModel

# Define expected response shape with Pydantic
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    total_value: float  # Computed field

class PaginatedItems(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    size: int
    pages: int

@pytest.mark.asyncio
async def test_get_items_with_pagination_and_filters(client: AsyncClient, item_factory):
    """
    RED: Test complex route with query params.
    Expected: GET /items?min_price=5&max_price=50&page=1&size=10
    """
    # Arrange: Create test data
    await item_factory(name="Cheap", price=3.0, quantity=10)
    await item_factory(name="Mid", price=25.0, quantity=5)
    await item_factory(name="Expensive", price=100.0, quantity=2)

    # Act: Call endpoint with filters
    response = await client.get(
        "/items",
        params={"min_price": 5, "max_price": 50, "page": 1, "size": 10}
    )

    # Assert: Validate with Pydantic (not just status code)
    assert response.status_code == 200

    # Validate response shape
    data = PaginatedItems(**response.json())
    assert data.total == 1  # Only "Mid" matches
    assert data.page == 1
    assert len(data.items) == 1
    assert data.items[0].name == "Mid"
    assert data.items[0].total_value == 125.0  # price * quantity
```

Run test - it MUST fail:
```bash
pytest tests/test_items.py::test_get_items_with_pagination_and_filters -v
# Expected: FAILED (404 or AttributeError)
```

## Step 2: GREEN - Minimal Implementation

Write the minimum code to make the test pass. No optimization yet.

```python
# app/schemas.py
from pydantic import BaseModel, computed_field

class ItemBase(BaseModel):
    name: str
    price: float
    quantity: int = 1

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    @computed_field
    @property
    def total_value(self) -> float:
        return self.price * self.quantity

    model_config = {"from_attributes": True}

class PaginatedItems(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    size: int
    pages: int
```

```python
# app/routers/items.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from math import ceil

from app.database import get_db
from app.models import Item
from app.schemas import ItemResponse, PaginatedItems

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=PaginatedItems)
async def get_items(
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Build query with filters
    query = select(Item)

    if min_price is not None:
        query = query.where(Item.price >= min_price)
    if max_price is not None:
        query = query.where(Item.price <= max_price)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Paginate
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)

    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedItems(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=ceil(total / size) if total > 0 else 0
    )
```

Run test - it MUST pass:
```bash
pytest tests/test_items.py::test_get_items_with_pagination_and_filters -v
# Expected: PASSED
```

## Step 3: REFACTOR - Optimize

Now improve code quality and performance without breaking tests.

```python
# app/routers/items.py (refactored)
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from math import ceil
from typing import Annotated

from app.database import get_db
from app.models import Item
from app.schemas import PaginatedItems

router = APIRouter(prefix="/items", tags=["items"])

# Reusable dependencies
PaginationParams = Annotated[
    tuple[int, int],
    Depends(lambda page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100): (page, size))
]

async def get_pagination(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100)
) -> tuple[int, int]:
    return page, size

@router.get("", response_model=PaginatedItems)
async def get_items(
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    pagination: tuple[int, int] = Depends(get_pagination),
    db: AsyncSession = Depends(get_db)
):
    page, size = pagination

    # Build filters once
    filters = []
    if min_price is not None:
        filters.append(Item.price >= min_price)
    if max_price is not None:
        filters.append(Item.price <= max_price)

    where_clause = and_(*filters) if filters else True

    # Single optimized query with count
    base_query = select(Item).where(where_clause)

    # Execute count and data in parallel-friendly way
    count_result = await db.execute(
        select(func.count(Item.id)).where(where_clause)
    )
    total = count_result.scalar() or 0

    # Fetch paginated results
    offset = (page - 1) * size
    result = await db.execute(base_query.offset(offset).limit(size))
    items = result.scalars().all()

    return PaginatedItems(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=ceil(total / size) if total > 0 else 0
    )
```

Run all tests to ensure refactor didn't break anything:
```bash
pytest tests/ -v
# All tests should pass
```

## Parametrized Testing for Edge Cases

```python
@pytest.mark.asyncio
@pytest.mark.parametrize("min_price,max_price,expected_count", [
    (None, None, 3),      # No filter - all items
    (0, 5, 1),            # Only cheap
    (20, 30, 1),          # Only mid-range
    (50, 200, 1),         # Only expensive
    (1000, 2000, 0),      # No matches
])
async def test_items_price_filter_combinations(
    client: AsyncClient,
    item_factory,
    min_price,
    max_price,
    expected_count
):
    # Arrange
    await item_factory(name="Cheap", price=3.0)
    await item_factory(name="Mid", price=25.0)
    await item_factory(name="Expensive", price=100.0)

    # Act
    params = {}
    if min_price is not None:
        params["min_price"] = min_price
    if max_price is not None:
        params["max_price"] = max_price

    response = await client.get("/items", params=params)

    # Assert
    assert response.status_code == 200
    assert response.json()["total"] == expected_count
```

## TDD Checklist

| Phase | Action | Verification |
|-------|--------|--------------|
| RED | Write test with assertions | Test fails with expected error |
| GREEN | Implement minimal code | Test passes |
| REFACTOR | Optimize/clean code | All tests still pass |
| REPEAT | Next feature/edge case | Cycle continues |
