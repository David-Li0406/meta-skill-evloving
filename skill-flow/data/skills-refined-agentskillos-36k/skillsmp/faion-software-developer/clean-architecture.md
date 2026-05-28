---
id: clean-architecture
name: "Clean Architecture"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Clean Architecture

## Overview

Clean Architecture separates concerns into concentric layers, with dependencies pointing inward. The core business logic remains independent of frameworks, databases, and delivery mechanisms. This methodology covers implementation patterns across different languages and frameworks.

## When to Use

- Complex business logic applications
- Long-lived enterprise systems
- Projects requiring high testability
- Applications that may change infrastructure
- Teams practicing Domain-Driven Design

## Key Principles

1. **Dependency rule** - Dependencies point inward toward higher-level policies
2. **Entities** - Enterprise business rules, framework-independent
3. **Use cases** - Application-specific business rules
4. **Interface adapters** - Convert data between layers
5. **Frameworks and drivers** - External tools and delivery mechanisms

## Best Practices

### Layer Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Frameworks & Drivers                      │
│  (Web, UI, DB, Devices, External Interfaces)                │
├─────────────────────────────────────────────────────────────┤
│                    Interface Adapters                        │
│  (Controllers, Gateways, Presenters)                        │
├─────────────────────────────────────────────────────────────┤
│                    Application Business Rules                │
│  (Use Cases / Interactors)                                  │
├─────────────────────────────────────────────────────────────┤
│                    Enterprise Business Rules                 │
│  (Entities)                                                 │
└─────────────────────────────────────────────────────────────┘

Dependencies flow INWARD only:
  Frameworks → Adapters → Use Cases → Entities
```

### Project Structure

```
src/
├── domain/                     # Entities layer
│   ├── entities/
│   │   ├── user.py
│   │   └── order.py
│   ├── value_objects/
│   │   ├── email.py
│   │   └── money.py
│   ├── events/
│   │   └── domain_events.py
│   ├── exceptions/
│   │   └── domain_exceptions.py
│   └── interfaces/             # Repository interfaces
│       ├── user_repository.py
│       └── order_repository.py
│
├── application/                # Use cases layer
│   ├── use_cases/
│   │   ├── users/
│   │   │   ├── create_user.py
│   │   │   ├── get_user.py
│   │   │   └── update_user.py
│   │   └── orders/
│   │       └── place_order.py
│   ├── interfaces/             # Application service interfaces
│   │   ├── unit_of_work.py
│   │   └── event_publisher.py
│   └── dto/
│       ├── user_dto.py
│       └── order_dto.py
│
├── infrastructure/             # Frameworks layer
│   ├── persistence/
│   │   ├── repositories/
│   │   │   └── user_repository_impl.py
│   │   ├── orm/
│   │   │   └── models.py
│   │   └── unit_of_work_impl.py
│   ├── services/
│   │   ├── email_service.py
│   │   └── payment_gateway.py
│   └── config/
│       └── database.py
│
└── presentation/               # Interface adapters
    ├── api/
    │   ├── controllers/
    │   │   └── user_controller.py
    │   ├── schemas/
    │   │   └── user_schemas.py
    │   └── middleware/
    └── cli/
        └── commands.py
```

### Domain Layer (Entities)

```python
# domain/entities/user.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from domain.value_objects.email import Email
from domain.events.domain_events import UserCreated, UserEmailChanged
from domain.exceptions.domain_exceptions import DomainError


@dataclass
class User:
    """User entity - core business rules."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    email: Email = field(default_factory=lambda: Email(""))
    role: str = "member"
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    _events: list = field(default_factory=list, repr=False)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if len(self.name) < 2:
            raise DomainError("Name must be at least 2 characters")

    @classmethod
    def create(cls, name: str, email: str) -> "User":
        """Factory method for creating new users."""
        user = cls(
            name=name,
            email=Email(email),
        )
        user._events.append(UserCreated(user.id, email))
        return user

    def change_email(self, new_email: str) -> None:
        """Change user's email with validation."""
        old_email = self.email.value
        self.email = Email(new_email)
        self._events.append(UserEmailChanged(self.id, old_email, new_email))

    def promote_to_admin(self) -> None:
        """Promote user to admin role."""
        if self.role == "admin":
            raise DomainError("User is already an admin")
        self.role = "admin"

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def collect_events(self) -> list:
        """Collect and clear domain events."""
        events = self._events.copy()
        self._events.clear()
        return events


# domain/value_objects/email.py
from dataclasses import dataclass
import re

from domain.exceptions.domain_exceptions import DomainError


@dataclass(frozen=True)
class Email:
    """Email value object with validation."""

    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise DomainError(f"Invalid email format: {self.value}")
        # Normalize to lowercase
        object.__setattr__(self, 'value', self.value.lower())

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


# domain/interfaces/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.user import User


class UserRepository(ABC):
    """Repository interface for User entity."""

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass
```

### Application Layer (Use Cases)

```python
# application/use_cases/users/create_user.py
from dataclasses import dataclass
from uuid import UUID

from domain.entities.user import User
from domain.interfaces.user_repository import UserRepository
from application.interfaces.unit_of_work import UnitOfWork
from application.interfaces.event_publisher import EventPublisher
from application.dto.user_dto import UserDTO
from application.exceptions import ApplicationError


@dataclass
class CreateUserInput:
    name: str
    email: str
    organization_id: UUID


@dataclass
class CreateUserOutput:
    user: UserDTO


class CreateUserUseCase:
    """Use case for creating a new user."""

    def __init__(
        self,
        user_repository: UserRepository,
        unit_of_work: UnitOfWork,
        event_publisher: EventPublisher,
    ):
        self._user_repository = user_repository
        self._unit_of_work = unit_of_work
        self._event_publisher = event_publisher

    async def execute(self, input_data: CreateUserInput) -> CreateUserOutput:
        # Check if user exists
        existing = await self._user_repository.find_by_email(input_data.email)
        if existing:
            raise ApplicationError("User with this email already exists")

        # Create user entity
        user = User.create(
            name=input_data.name,
            email=input_data.email,
        )

        # Persist and commit
        async with self._unit_of_work:
            await self._user_repository.save(user)
            await self._unit_of_work.commit()

        # Publish domain events
        for event in user.collect_events():
            await self._event_publisher.publish(event)

        return CreateUserOutput(user=UserDTO.from_entity(user))


# application/use_cases/users/get_user.py
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.interfaces.user_repository import UserRepository
from application.dto.user_dto import UserDTO
from application.exceptions import NotFoundError


@dataclass
class GetUserInput:
    user_id: UUID


class GetUserUseCase:
    """Use case for retrieving a user by ID."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def execute(self, input_data: GetUserInput) -> UserDTO:
        user = await self._user_repository.find_by_id(input_data.user_id)

        if not user:
            raise NotFoundError(f"User not found: {input_data.user_id}")

        return UserDTO.from_entity(user)


# application/dto/user_dto.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.user import User


@dataclass
class UserDTO:
    """Data transfer object for User."""

    id: UUID
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserDTO":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email.value,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )


# application/interfaces/unit_of_work.py
from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """Unit of Work pattern interface."""

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
```

### Infrastructure Layer

```python
# infrastructure/persistence/repositories/user_repository_impl.py
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import User
from domain.interfaces.user_repository import UserRepository
from domain.value_objects.email import Email
from infrastructure.persistence.orm.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.lower())
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, user: User) -> None:
        model = self._to_model(user)
        self._session.add(model)

    async def delete(self, user: User) -> None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=Email(model.email),
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            name=entity.name,
            email=entity.email.value,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )


# infrastructure/persistence/unit_of_work_impl.py
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.unit_of_work import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy implementation of Unit of Work."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
```

### Presentation Layer (Interface Adapters)

```python
# presentation/api/controllers/user_controller.py
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.users.create_user import CreateUserUseCase, CreateUserInput
from application.use_cases.users.get_user import GetUserUseCase, GetUserInput
from application.exceptions import ApplicationError, NotFoundError
from presentation.api.schemas.user_schemas import (
    CreateUserRequest,
    UserResponse,
)
from presentation.api.dependencies import get_create_user_use_case, get_get_user_use_case

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    try:
        output = await use_case.execute(
            CreateUserInput(
                name=request.name,
                email=request.email,
                organization_id=request.organization_id,
            )
        )
        return UserResponse.from_dto(output.user)
    except ApplicationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
):
    try:
        user_dto = await use_case.execute(GetUserInput(user_id=user_id))
        return UserResponse.from_dto(user_dto)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
```

## Anti-patterns

### Avoid: Leaking Domain Logic

```python
# BAD - business logic in controller
@router.post("/users")
async def create_user(request: CreateUserRequest):
    if await user_repo.find_by_email(request.email):
        raise HTTPException(400, "Email exists")
    user = User(name=request.name, email=request.email)
    await user_repo.save(user)
    return user

# GOOD - delegate to use case
@router.post("/users")
async def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    output = await use_case.execute(CreateUserInput(...))
    return UserResponse.from_dto(output.user)
```

### Avoid: Framework Coupling in Domain

```python
# BAD - SQLAlchemy in domain entity
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    email = Column(String, unique=True)

# GOOD - pure Python domain entity
@dataclass
class User:
    email: Email
    name: str
```

## References

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Ports and Adapters Pattern](https://herbertograca.com/2017/09/14/ports-adapters-architecture/)
