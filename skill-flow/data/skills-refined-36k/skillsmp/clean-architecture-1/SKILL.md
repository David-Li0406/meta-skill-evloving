---
name: clean-architecture
description: Guide for implementing Clean Architecture in Python/FastAPI projects. Use when creating new modules, refactoring existing code to Clean Architecture, designing layer structures, or implementing Port/Adapter patterns. Triggers on "clean architecture", "hexagonal", "ports and adapters", "layer structure", "DIP", "dependency inversion".
---

# Clean Architecture Implementation Guide

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                         Dependency Rule                          │
│          Dependencies ALWAYS point inward (to Domain)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Presentation ──▶ Application ──▶ Domain ◀── Infrastructure    │
│   (Controllers)    (Use Cases)    (Entities)   (Adapters)       │
│                                                                  │
│   Infrastructure IMPLEMENTS Domain/Application Ports             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

| Layer | Responsibility | Allowed Dependencies |
|-------|---------------|---------------------|
| **Domain** | Business rules, Entities, Value Objects | None (pure Python) |
| **Application** | Use Cases, Orchestration | Domain only |
| **Infrastructure** | DB, External APIs, Framework adapters | Domain, Application |
| **Presentation** | HTTP/CLI, Request/Response handling | Application |

## Standard Directory Structure

```
app_name/
├── domain/
│   ├── entities/           # Aggregate roots, Entities
│   ├── value_objects/      # Immutable value types
│   ├── services/           # Domain services (stateless)
│   ├── ports/              # Domain-level abstractions
│   ├── enums/              # Domain enumerations
│   └── exceptions/         # Domain exceptions
│
├── application/
│   ├── commands/           # Write Use Cases (Interactors)
│   ├── queries/            # Read Use Cases (QueryServices)
│   ├── ports/              # Application-level abstractions
│   ├── dto/                # Data Transfer Objects
│   ├── services/           # Application services
│   └── exceptions/         # Application exceptions
│
├── infrastructure/
│   ├── adapters/           # Port implementations
│   ├── persistence/        # ORM, migrations
│   ├── integrations/       # External API clients
│   └── exceptions/         # Infrastructure exceptions
│
├── presentation/
│   └── http/
│       ├── controllers/    # FastAPI routers
│       ├── dependencies/   # FastAPI Depends
│       └── schemas/        # Pydantic request/response
│
└── setup/
    ├── config.py           # Settings
    └── dependencies.py     # DI wiring
```

## Port & Adapter Pattern

### Defining Ports (Interfaces)

```python
# application/ports/user_repository.py
from typing import Protocol

class UserRepository(Protocol):
    """Port: Abstract interface for user persistence"""

    async def get_by_id(self, user_id: UserId) -> User | None: ...
    async def save(self, user: User) -> None: ...
    async def exists_by_email(self, email: Email) -> bool: ...
```

### Implementing Adapters

```python
# infrastructure/adapters/postgres_user_repository.py
class PostgresUserRepository:
    """Adapter: Concrete implementation using PostgreSQL"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UserId) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id.value)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return self._to_entity(row) if row else None
```

## CQRS Pattern

### Command (Write Operation)

```python
# application/commands/create_user.py
@dataclass(frozen=True)
class CreateUserCommand:
    email: str
    password: str

class CreateUserInteractor:
    def __init__(
        self,
        user_repo: UserRepository,
        hasher: PasswordHasher,
        tx: TransactionManager,
    ):
        self._repo = user_repo
        self._hasher = hasher
        self._tx = tx

    async def execute(self, cmd: CreateUserCommand) -> UserId:
        # Domain logic
        user = User.create(
            email=Email(cmd.email),
            password_hash=await self._hasher.hash(cmd.password),
        )
        await self._repo.save(user)
        await self._tx.commit()
        return user.id
```

### Query (Read Operation)

```python
# application/queries/get_user.py
class GetUserQueryService:
    def __init__(self, reader: UserQueryGateway):
        self._reader = reader

    async def execute(self, user_id: UUID) -> UserDTO | None:
        return await self._reader.get_by_id(user_id)
```

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Port (data access) | `{Entity}Repository` or `{Entity}Gateway` | `UserRepository` |
| Port (action) | `{Action}er` | `PasswordHasher`, `TokenGenerator` |
| Adapter | `{Tech}{Port}` | `PostgresUserRepository`, `BcryptHasher` |
| Command Use Case | `{Verb}{Noun}Interactor` | `CreateUserInteractor` |
| Query Use Case | `{Verb}{Noun}QueryService` | `ListUsersQueryService` |
| Value Object | `{Noun}` (noun form) | `Email`, `UserId`, `Money` |

## Reference Files

- **Layer details**: See [layer-structure.md](./references/layer-structure.md)
- **Port/Adapter examples**: See [port-adapter.md](./references/port-adapter.md)
- **CQRS patterns**: See [cqrs-patterns.md](./references/cqrs-patterns.md)
- **Evaluation checklist**: See [evaluation-checklist.md](./references/evaluation-checklist.md)
- **Anti-patterns to avoid**: See [anti-patterns.md](./references/anti-patterns.md)

## Eco² Project Conventions

This project follows conventions from `docs/foundations/16-fastapi-clean-example-analysis.md`:

- Use `Protocol` over ABC for interfaces (structural typing)
- Gateway naming for CQRS split (`CommandGateway`, `QueryGateway`)
- Separate `Flusher` and `TransactionManager` ports
- Value Objects with self-validation in `__post_init__`
