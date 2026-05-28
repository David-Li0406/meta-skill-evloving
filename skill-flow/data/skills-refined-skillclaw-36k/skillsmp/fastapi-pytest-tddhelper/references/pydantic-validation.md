# Pydantic Validation in Tests

## Why Validate with Pydantic (Not Just Status Codes)

```python
# BAD: Only checks status code
def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    # Response could have wrong shape, missing fields, wrong types!

# GOOD: Validates entire response shape
from app.schemas import ItemResponse

def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    item = ItemResponse(**response.json())  # Raises ValidationError if wrong shape
    assert item.name == "Expected Name"
```

## Response Schema Definitions

```python
# tests/schemas.py - Test-specific response schemas
from pydantic import BaseModel, Field
from datetime import datetime

class ErrorResponse(BaseModel):
    detail: str

class ValidationErrorDetail(BaseModel):
    loc: list[str | int]
    msg: str
    type: str

class ValidationErrorResponse(BaseModel):
    detail: list[ValidationErrorDetail]

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    created_at: datetime

    model_config = {"extra": "forbid"}  # Fail on unexpected fields

class PaginatedResponse(BaseModel):
    items: list[ItemResponse]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    size: int = Field(ge=1)
    pages: int = Field(ge=0)
```

## Validation Patterns

### Validate Success Responses

```python
@pytest.mark.asyncio
async def test_create_item_returns_valid_response(client: AsyncClient):
    response = await client.post("/items/", json={"name": "Widget", "price": 10.0})

    assert response.status_code == 201

    # Validate response matches expected schema
    item = ItemResponse(**response.json())
    assert item.name == "Widget"
    assert item.price == 10.0
    assert item.id is not None  # Auto-generated
```

### Validate Error Responses

```python
@pytest.mark.asyncio
async def test_get_nonexistent_item_returns_404(client: AsyncClient):
    response = await client.get("/items/99999")

    assert response.status_code == 404

    error = ErrorResponse(**response.json())
    assert "not found" in error.detail.lower()

@pytest.mark.asyncio
async def test_create_item_invalid_data_returns_422(client: AsyncClient):
    response = await client.post("/items/", json={"name": "", "price": -10})

    assert response.status_code == 422

    error = ValidationErrorResponse(**response.json())
    assert len(error.detail) >= 1

    # Check specific validation errors
    error_fields = [e.loc[-1] for e in error.detail]
    assert "price" in error_fields or "name" in error_fields
```

### Validate List Responses

```python
@pytest.mark.asyncio
async def test_list_items_returns_valid_paginated_response(
    client: AsyncClient,
    item_factory
):
    # Create test data
    for i in range(15):
        await item_factory(name=f"Item {i}", price=float(i))

    response = await client.get("/items/", params={"page": 1, "size": 10})

    assert response.status_code == 200

    # Validate pagination structure
    data = PaginatedResponse(**response.json())
    assert data.total == 15
    assert data.page == 1
    assert data.size == 10
    assert len(data.items) == 10
    assert data.pages == 2

    # Validate each item in list
    for item in data.items:
        assert isinstance(item, ItemResponse)
        assert item.id is not None
```

### Validate Computed/Derived Fields

```python
from pydantic import computed_field

class ItemWithTotal(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

    @computed_field
    @property
    def total_value(self) -> float:
        return self.price * self.quantity

@pytest.mark.asyncio
async def test_item_response_includes_computed_total(client: AsyncClient, item_factory):
    await item_factory(name="Widget", price=25.0, quantity=4)

    response = await client.get("/items/")
    items = [ItemWithTotal(**i) for i in response.json()["items"]]

    assert items[0].total_value == 100.0  # 25.0 * 4
```

## Generic Response Validator

```python
# tests/utils.py
from typing import TypeVar, Type
from pydantic import BaseModel
from httpx import Response

T = TypeVar("T", bound=BaseModel)

def validate_response(response: Response, schema: Type[T], status_code: int = 200) -> T:
    """
    Validate response status and parse body with Pydantic schema.

    Usage:
        item = validate_response(response, ItemResponse, 201)
    """
    assert response.status_code == status_code, (
        f"Expected {status_code}, got {response.status_code}: {response.text}"
    )
    return schema(**response.json())

def validate_list_response(
    response: Response,
    item_schema: Type[T],
    status_code: int = 200
) -> list[T]:
    """Validate list response and parse each item."""
    assert response.status_code == status_code
    return [item_schema(**item) for item in response.json()]
```

```python
# Usage in tests
from tests.utils import validate_response, validate_list_response

@pytest.mark.asyncio
async def test_create_and_get_item(client: AsyncClient):
    # Create
    create_response = await client.post("/items/", json={"name": "Test", "price": 10.0})
    created = validate_response(create_response, ItemResponse, 201)

    # Get
    get_response = await client.get(f"/items/{created.id}")
    fetched = validate_response(get_response, ItemResponse)

    assert fetched.id == created.id
    assert fetched.name == created.name
```

## Strict Mode for Extra Fields

```python
class StrictItemResponse(BaseModel):
    """Fails if API returns unexpected fields."""
    id: int
    name: str
    price: float

    model_config = {"extra": "forbid"}

@pytest.mark.asyncio
async def test_response_has_no_extra_fields(client: AsyncClient, item_factory):
    await item_factory()
    response = await client.get("/items/1")

    # This will raise ValidationError if response has fields
    # not defined in StrictItemResponse
    StrictItemResponse(**response.json())
```
