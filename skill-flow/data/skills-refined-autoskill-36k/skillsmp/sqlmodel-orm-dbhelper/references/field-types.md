# SQLModel Field Types

Complete reference for field types, validators, and constraints.

---

## Basic Field Types

### String Fields

```python
from sqlmodel import Field, SQLModel
from sqlalchemy import Text, String

class Example(SQLModel, table=True):
    # Fixed length string (VARCHAR)
    name: str = Field(max_length=100)

    # String with index
    code: str = Field(max_length=50, index=True)

    # Unique string
    email: str = Field(max_length=255, unique=True, index=True)

    # Nullable string
    description: str | None = Field(default=None, max_length=500)

    # Unlimited text (TEXT type)
    content: str = Field(sa_type=Text)

    # String with default
    status: str = Field(default="active", max_length=20)
```

### Numeric Fields

```python
from decimal import Decimal
from sqlmodel import Field, SQLModel
from sqlalchemy import Numeric

class Product(SQLModel, table=True):
    # Integer primary key
    id: int | None = Field(default=None, primary_key=True)

    # Integer with index
    quantity: int = Field(default=0, index=True)

    # Float
    rating: float = Field(default=0.0)

    # Decimal for financial data (precise)
    price: Decimal = Field(
        default=Decimal("0.00"),
        sa_type=Numeric(precision=10, scale=2)
    )

    # Positive integer constraint
    stock: int = Field(ge=0)  # Pydantic validation
```

### Boolean Fields

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Boolean with default
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    # Indexed boolean for filtering
    is_admin: bool = Field(default=False, index=True)
```

### Date and Time Fields

```python
from datetime import datetime, date, time
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime, Date, Time

class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # DateTime with auto-now
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # DateTime with timezone
    scheduled_at: datetime = Field(sa_type=DateTime(timezone=True))

    # Date only
    event_date: date

    # Time only
    start_time: time

    # Nullable datetime
    completed_at: datetime | None = Field(default=None)

    # Updated timestamp
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )
```

### UUID Fields

```python
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Resource(SQLModel, table=True):
    # UUID as primary key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_type=PG_UUID(as_uuid=True)  # PostgreSQL native UUID
    )

    # UUID as regular field
    external_id: UUID = Field(default_factory=uuid4, unique=True)
```

---

## JSON Fields

### Basic JSON

```python
from typing import Any
from sqlmodel import Field, SQLModel
from sqlalchemy import JSON

class Config(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # JSON field (any structure)
    settings: dict = Field(default={}, sa_type=JSON)

    # JSON with list
    tags: list = Field(default=[], sa_type=JSON)

    # Typed JSON (Pydantic validates)
    metadata: dict[str, Any] = Field(default={}, sa_type=JSON)
```

### PostgreSQL JSONB (Queryable)

```python
from sqlalchemy.dialects.postgresql import JSONB

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # JSONB with GIN index for queries
    attributes: dict = Field(
        default={},
        sa_type=JSONB,
        sa_column_kwargs={"index": True}  # GIN index
    )
```

### Querying JSON Fields

```python
from sqlmodel import select
from sqlalchemy import cast, String

# PostgreSQL JSONB query
statement = select(Product).where(
    Product.attributes["color"].astext == "red"
)

# JSON path query
statement = select(Product).where(
    Product.attributes["specs"]["weight"].astext.cast(Integer) > 100
)
```

---

## Enum Fields

```python
from enum import Enum
from sqlmodel import Field, SQLModel
from sqlalchemy import Enum as SAEnum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Enum stored as string
    status: OrderStatus = Field(default=OrderStatus.PENDING)

    # Alternative: explicit SA Enum type
    priority: str = Field(
        default="normal",
        sa_type=SAEnum("low", "normal", "high", name="priority_enum")
    )
```

---

## Array Fields (PostgreSQL)

```python
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String, Integer

class Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Array of strings
    tags: list[str] = Field(
        default=[],
        sa_type=ARRAY(String)
    )

    # Array of integers
    category_ids: list[int] = Field(
        default=[],
        sa_type=ARRAY(Integer)
    )
```

### Querying Arrays

```python
from sqlalchemy import any_, all_

# Contains element
statement = select(Article).where(Article.tags.contains(["python"]))

# Any element matches
statement = select(Article).where("python" == any_(Article.tags))
```

---

## Field Constraints

### Primary Keys

```python
class User(SQLModel, table=True):
    # Auto-increment integer PK
    id: int | None = Field(default=None, primary_key=True)

class Resource(SQLModel, table=True):
    # UUID PK
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class OrderItem(SQLModel, table=True):
    # Composite primary key
    order_id: int = Field(primary_key=True, foreign_key="order.id")
    product_id: int = Field(primary_key=True, foreign_key="product.id")
```

### Foreign Keys

```python
class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Required foreign key
    user_id: int = Field(foreign_key="user.id", index=True)

    # Optional foreign key
    coupon_id: int | None = Field(
        default=None,
        foreign_key="coupon.id",
        index=True
    )

    # Foreign key with cascade
    product_id: int = Field(
        foreign_key="product.id",
        sa_column_kwargs={"ondelete": "CASCADE"}
    )
```

### Unique Constraints

```python
from sqlalchemy import UniqueConstraint

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Single column unique
    email: str = Field(unique=True, index=True)

    # Composite unique constraint
    __table_args__ = (
        UniqueConstraint("org_id", "username", name="uq_user_org_username"),
    )
```

### Check Constraints

```python
from sqlalchemy import CheckConstraint

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    price: Decimal
    discount_price: Decimal | None = None

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_product_price_positive"),
        CheckConstraint(
            "discount_price IS NULL OR discount_price < price",
            name="ck_product_discount_less_than_price"
        ),
    )
```

---

## Pydantic Validators

SQLModel inherits Pydantic's validation.

```python
from pydantic import field_validator, model_validator
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255)
    username: str = Field(min_length=3, max_length=50)
    age: int | None = Field(default=None, ge=0, le=150)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

    @model_validator(mode="after")
    def validate_model(self):
        # Cross-field validation
        return self
```

---

## Default Values

```python
from datetime import datetime
from uuid import uuid4

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Static default
    status: str = Field(default="draft")
    count: int = Field(default=0)

    # Factory default (called for each instance)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    uuid: UUID = Field(default_factory=uuid4)

    # Server default (database generates)
    sequence: int = Field(
        sa_column_kwargs={"server_default": "nextval('item_seq'::regclass)"}
    )
```

---

## Common Patterns

### Timestamp Mixin

```python
from datetime import datetime
from sqlmodel import Field, SQLModel

class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": "now()"}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": "now()",
            "onupdate": datetime.utcnow
        }
    )
```

### Soft Delete Mixin

```python
class SoftDeleteMixin(SQLModel):
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: datetime | None = Field(default=None)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
```

### Audit Mixin

```python
class AuditMixin(TimestampMixin):
    created_by: int | None = Field(default=None, foreign_key="user.id")
    updated_by: int | None = Field(default=None, foreign_key="user.id")
```
