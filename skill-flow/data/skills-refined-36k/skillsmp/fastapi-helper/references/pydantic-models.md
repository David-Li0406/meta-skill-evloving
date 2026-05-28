# FastAPI Pydantic Models Reference

## Basic Models

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

# Usage
item = Item(name="Foo", price=42.0)
item_dict = item.model_dump()  # Convert to dict
item_json = item.model_dump_json()  # Convert to JSON string
```

## Field Validation

```python
from pydantic import BaseModel, Field, field_validator, model_validator

class Item(BaseModel):
    name: str = Field(
        ...,  # Required
        min_length=1,
        max_length=100,
        description="Item name",
        examples=["Widget"]
    )
    price: float = Field(
        ...,
        gt=0,           # Greater than
        le=10000,       # Less than or equal
        description="Item price"
    )
    quantity: int = Field(default=1, ge=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.title()

    @model_validator(mode="after")
    def check_total(self) -> "Item":
        if self.price * self.quantity > 100000:
            raise ValueError("Total value too high")
        return self
```

## Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = "USA"

class User(BaseModel):
    name: str
    address: Address
    tags: list[str] = []

# Usage
user = User(
    name="John",
    address={"street": "123 Main", "city": "NYC"}
)
```

## Request/Response Models Pattern

```python
# Base model with shared fields
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

# For creating (no ID)
class ItemCreate(ItemBase):
    pass

# For updating (all optional)
class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None

# For response (includes ID, timestamps)
class Item(ItemBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}  # For ORM mode

# Usage
@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate):
    db_item = crud.create_item(item)
    return db_item

@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    return crud.update_item(item_id, item.model_dump(exclude_unset=True))
```

## Common Field Types

```python
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr
from typing import Literal
from enum import Enum
from uuid import UUID
from datetime import datetime, date, time

class Status(str, Enum):
    pending = "pending"
    active = "active"
    completed = "completed"

class User(BaseModel):
    id: UUID
    email: EmailStr
    password: SecretStr
    website: HttpUrl | None = None
    status: Status = Status.pending
    role: Literal["admin", "user", "guest"] = "user"
    created_at: datetime
    birth_date: date | None = None
```

## Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class Item(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace from strings
        str_min_length=1,           # Min string length
        from_attributes=True,       # Enable ORM mode
        extra="forbid",             # Forbid extra fields
        populate_by_name=True,      # Allow population by field name
        use_enum_values=True        # Use enum values instead of enum objects
    )

    name: str
    price: float
```

## Generic Response Models

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    data: T
    message: str = "Success"

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int

# Usage
@app.get("/items/", response_model=PaginatedResponse[Item])
async def list_items(page: int = 1, size: int = 10):
    items = get_items(page, size)
    return PaginatedResponse(
        items=items,
        total=100,
        page=page,
        size=size
    )
```
