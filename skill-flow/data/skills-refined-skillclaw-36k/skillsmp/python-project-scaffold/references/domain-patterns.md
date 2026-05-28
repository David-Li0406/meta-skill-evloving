# Domain Layer Patterns

The domain layer is the innermost layer containing core business logic. Uses Pydantic for validation and immutability.

> **Note:** While pure DDD suggests zero external dependencies in the domain layer, we pragmatically use Pydantic for its powerful validation, serialization, and immutability features.

## Entities

Entities have identity and lifecycle. Use Pydantic BaseModel with `id` field:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    email: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
```

## Value Objects

Immutable objects without identity. Use `frozen=True` for immutability:

```python
from pydantic import BaseModel, Field


class Money(BaseModel):
    """Monetary value with currency."""

    model_config = {"frozen": True}

    amount: int = Field(gt=0, description="Amount in smallest unit (cents)")
    currency: str = Field(min_length=3, max_length=3)

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(amount=self.amount + other.amount, currency=self.currency)


class Email(BaseModel):
    """Email address value object with validation."""

    model_config = {"frozen": True}

    value: str = Field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")


class Address(BaseModel):
    """Physical address value object."""

    model_config = {"frozen": True}

    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: str = Field(min_length=1)
    country: str = Field(min_length=2, max_length=2)
```

## Repository Interfaces (Ports)

Define abstract interfaces for persistence. Infrastructure implements these:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def find_by_id(self, id: str) -> T | None: ...

    @abstractmethod
    def find_all(self) -> list[T]: ...

    @abstractmethod
    def save(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...


class UserRepository(Repository["User"], ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> "User | None": ...
```

## Domain Services

Stateless operations that don't belong to a single entity:

```python
from pydantic import BaseModel


class PricingService(BaseModel):
    """Domain service for price calculations."""

    tax_rate: float = 0.1

    def calculate_total(self, subtotal: Money, discount: Money) -> Money:
        net = subtotal.add(Money(amount=-discount.amount, currency=subtotal.currency))
        tax = Money(amount=int(net.amount * self.tax_rate), currency=net.currency)
        return net.add(tax)
```

## Domain Events

Use frozen models for immutable events:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class DomainEvent(BaseModel):
    """Base class for domain events."""

    model_config = {"frozen": True}

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreated(DomainEvent):
    user_id: str
    email: str
```

## Validation Patterns

Leverage Pydantic's built-in validators:

```python
from pydantic import BaseModel, Field, field_validator


class Product(BaseModel):
    model_config = {"frozen": True}

    name: str = Field(min_length=1, max_length=100)
    price: int = Field(gt=0)
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()
```

## Domain Exceptions

Define domain-specific exceptions that represent business rule violations:

```python
class DomainException(Exception):
    """Base exception for domain errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""

    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id '{entity_id}' not found")


class ValidationError(DomainException):
    """Raised when domain validation fails."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message)


class DuplicateEntityError(DomainException):
    """Raised when attempting to create a duplicate entity."""

    def __init__(self, entity_type: str, field: str, value: str):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} with {field} '{value}' already exists")


class BusinessRuleViolationError(DomainException):
    """Raised when a business rule is violated."""

    pass
```

## Rules

1. **Use Pydantic BaseModel** - For entities, value objects, and domain events
2. **frozen=True for value objects** - Ensures immutability
3. **Validation in models** - Use Field constraints and validators
4. **Business logic in methods** - Entities can have behavior
5. **Repository interfaces only** - Implementations live in infrastructure
6. **Domain exceptions** - Define business error types in domain layer
