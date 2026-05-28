# Application Layer Patterns

The application layer orchestrates use cases using domain objects. Depends only on domain layer.

## Use Cases

Each use case represents a single application operation:

```python
from pydantic import BaseModel, Field
from typing import Protocol


class UserRepository(Protocol):
    def find_by_id(self, id: str) -> "User | None": ...
    def find_by_email(self, email: str) -> "User | None": ...
    def save(self, user: "User") -> "User": ...


class CreateUserRequest(BaseModel):
    """Request DTO for creating a user."""

    model_config = {"frozen": True}

    email: str = Field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
    name: str = Field(min_length=1, max_length=100)


class CreateUserResponse(BaseModel):
    """Response DTO for user creation."""

    model_config = {"frozen": True}

    success: bool
    user_id: str | None = None
    error: str | None = None


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository

    def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # Check if user exists
        existing = self._repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(success=False, error="Email already exists")

        # Create and save user
        user = User(email=request.email, name=request.name)
        saved = self._repository.save(user)

        return CreateUserResponse(success=True, user_id=saved.id)
```

## DTOs (Data Transfer Objects)

Use frozen Pydantic models for crossing layer boundaries:

```python
from pydantic import BaseModel
from datetime import datetime


class UserDTO(BaseModel):
    """User data transfer object."""

    model_config = {"frozen": True}

    id: str
    email: str
    name: str
    created_at: datetime

    @classmethod
    def from_entity(cls, user: "User") -> "UserDTO":
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        )


class PagedResult[T](BaseModel):
    """Generic paginated result."""

    model_config = {"frozen": True}

    items: list[T]
    total: int
    page: int
    page_size: int
```

## Application Services

Coordinate multiple use cases or cross-cutting concerns:

```python
from typing import Protocol


class EventPublisher(Protocol):
    def publish(self, event: "DomainEvent") -> None: ...


class UserApplicationService:
    def __init__(
        self,
        create_user: CreateUserUseCase,
        event_publisher: EventPublisher,
    ):
        self._create_user = create_user
        self._publisher = event_publisher

    def register_user(self, request: CreateUserRequest) -> CreateUserResponse:
        result = self._create_user.execute(request)
        if result.success and result.user_id:
            self._publisher.publish(UserCreated(user_id=result.user_id, email=request.email))
        return result
```

## Command/Query Pattern (Optional)

Separate read and write operations:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class CommandHandler(ABC, Generic[TRequest, TResponse]):
    @abstractmethod
    def handle(self, command: TRequest) -> TResponse: ...


class QueryHandler(ABC, Generic[TRequest, TResponse]):
    @abstractmethod
    def handle(self, query: TRequest) -> TResponse: ...


# Usage
class GetUserQuery(BaseModel):
    model_config = {"frozen": True}

    user_id: str


class GetUserQueryHandler(QueryHandler[GetUserQuery, UserDTO | None]):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def handle(self, query: GetUserQuery) -> UserDTO | None:
        user = self._repository.find_by_id(query.user_id)
        return UserDTO.from_entity(user) if user else None
```

## Rules

1. **Depend only on domain** - No infrastructure imports
2. **Use Pydantic for DTOs** - With frozen=True for immutability
3. **One use case per class** - Single responsibility
4. **Return DTOs, not entities** - Prevent domain leakage
5. **Handle business rules here** - Orchestration logic lives in use cases
