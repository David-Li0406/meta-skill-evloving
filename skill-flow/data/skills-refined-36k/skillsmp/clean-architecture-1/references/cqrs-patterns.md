# CQRS Patterns Reference

Command Query Responsibility Segregation - separating read and write models.

## Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                         CQRS Pattern                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                         ┌─────────────┐                         │
│                         │   Client    │                         │
│                         └──────┬──────┘                         │
│                                │                                 │
│              ┌─────────────────┴─────────────────┐              │
│              │                                   │              │
│              ▼                                   ▼              │
│      ┌───────────────┐                  ┌───────────────┐      │
│      │   Commands    │                  │    Queries    │      │
│      │ (Write Model) │                  │ (Read Model)  │      │
│      └───────┬───────┘                  └───────┬───────┘      │
│              │                                   │              │
│              ▼                                   ▼              │
│      ┌───────────────┐                  ┌───────────────┐      │
│      │  Repository   │                  │ Query Gateway │      │
│      │  (Entities)   │                  │   (DTOs)      │      │
│      └───────┬───────┘                  └───────┬───────┘      │
│              │                                   │              │
│              └─────────────┬─────────────────────┘              │
│                            │                                    │
│                            ▼                                    │
│                     ┌───────────┐                               │
│                     │  Database │                               │
│                     └───────────┘                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Command Pattern (Write Operations)

### Command DTO

```python
# application/commands/create_user.py
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    """Immutable command DTO"""
    email: str
    password: str
    role: str = "user"


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    user_id: UUID
    email: str | None = None
    role: str | None = None


@dataclass(frozen=True, slots=True)
class DeleteUserCommand:
    user_id: UUID
    reason: str | None = None
```

### Command Handler (Interactor)

```python
# application/commands/create_user.py
class CreateUserInteractor:
    """
    Command handler naming: {Verb}{Noun}Interactor

    Responsibilities:
    1. Validate authorization
    2. Execute domain logic
    3. Persist changes
    4. Manage transaction
    5. Publish events (optional)
    """

    def __init__(
        self,
        user_repo: UserRepository,
        user_service: UserService,
        tx: TransactionManager,
        events: EventPublisher,
    ):
        self._repo = user_repo
        self._service = user_service
        self._tx = tx
        self._events = events

    async def execute(self, cmd: CreateUserCommand) -> UserId:
        # 1. Create domain entity via service
        user = await self._service.create_user(
            email=Email(cmd.email),
            raw_password=cmd.password,
            role=UserRole(cmd.role),
        )

        # 2. Persist
        await self._repo.save(user)

        # 3. Commit transaction
        await self._tx.commit()

        # 4. Publish event (after commit)
        await self._events.publish(UserCreated(user_id=user.id))

        # 5. Return identifier only (not full entity)
        return user.id
```

### Command Result Types

```python
# Commands typically return:
# 1. Created resource ID
async def execute(self, cmd: CreateUserCommand) -> UserId: ...

# 2. Nothing (void)
async def execute(self, cmd: DeleteUserCommand) -> None: ...

# 3. Simple result DTO
@dataclass
class UpdateResult:
    updated: bool
    version: int

async def execute(self, cmd: UpdateUserCommand) -> UpdateResult: ...
```

---

## Query Pattern (Read Operations)

### Query DTO

```python
# application/queries/list_users.py
from dataclasses import dataclass
from enum import Enum

class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"

@dataclass(frozen=True, slots=True)
class ListUsersQuery:
    """Query parameters"""
    limit: int = 20
    offset: int = 0
    sort_by: str = "created_at"
    sort_order: SortOrder = SortOrder.DESC
    role_filter: str | None = None
    is_active: bool | None = None


@dataclass(frozen=True, slots=True)
class GetUserQuery:
    user_id: UUID
```

### Query Handler (QueryService)

```python
# application/queries/list_users.py
class ListUsersQueryService:
    """
    Query handler naming: {Verb}{Noun}QueryService

    Characteristics:
    1. Read-only (no state changes)
    2. No transaction management
    3. Returns DTOs (not entities)
    4. Can use optimized read models
    """

    def __init__(self, reader: UserQueryGateway):
        self._reader = reader

    async def execute(self, query: ListUsersQuery) -> PaginatedResult[UserDTO]:
        users = await self._reader.list_all(
            limit=query.limit,
            offset=query.offset,
            sort_by=query.sort_by,
            sort_order=query.sort_order,
            filters=UserFilters(
                role=query.role_filter,
                is_active=query.is_active,
            ),
        )

        total = await self._reader.count(
            filters=UserFilters(
                role=query.role_filter,
                is_active=query.is_active,
            ),
        )

        return PaginatedResult(
            items=users,
            total=total,
            limit=query.limit,
            offset=query.offset,
        )
```

### Query Result Types (DTOs)

```python
# application/dto/user.py
from dataclasses import dataclass
from typing import TypedDict

# Option 1: Dataclass DTO
@dataclass(frozen=True, slots=True)
class UserDTO:
    id: UUID
    email: str
    role: str
    is_active: bool
    created_at: datetime


# Option 2: TypedDict (for JSON serialization)
class UserDTO(TypedDict):
    id: str
    email: str
    role: str
    is_active: bool
    created_at: str


# Paginated result
@dataclass(frozen=True)
class PaginatedResult(Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int

    @property
    def has_next(self) -> bool:
        return self.offset + len(self.items) < self.total

    @property
    def has_prev(self) -> bool:
        return self.offset > 0
```

---

## Gateway Pattern (Read Model)

### Query Gateway Interface

```python
# application/ports/user_query_gateway.py
from typing import Protocol

class UserQueryGateway(Protocol):
    """
    Read-only gateway for queries.
    Returns DTOs, not domain entities.
    Can use optimized read models (denormalized, cached).
    """

    async def get_by_id(self, user_id: UUID) -> UserDTO | None: ...

    async def list_all(
        self,
        limit: int,
        offset: int,
        sort_by: str,
        sort_order: SortOrder,
        filters: UserFilters | None = None,
    ) -> list[UserDTO]: ...

    async def count(self, filters: UserFilters | None = None) -> int: ...

    async def exists(self, user_id: UUID) -> bool: ...
```

### Query Gateway Implementation

```python
# infrastructure/adapters/postgres_user_reader.py
class PostgresUserReader:
    """
    Optimized reader for queries.
    Can use different techniques:
    - Direct SQL (no ORM overhead)
    - Read replicas
    - Cached views
    - Materialized views
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: UUID) -> UserDTO | None:
        # Direct SQL for performance
        stmt = text("""
            SELECT id, email, role, is_active, created_at
            FROM users
            WHERE id = :user_id
        """)
        result = await self._session.execute(stmt, {"user_id": user_id})
        row = result.fetchone()

        if not row:
            return None

        return UserDTO(
            id=row.id,
            email=row.email,
            role=row.role,
            is_active=row.is_active,
            created_at=row.created_at,
        )

    async def list_all(
        self,
        limit: int,
        offset: int,
        sort_by: str,
        sort_order: SortOrder,
        filters: UserFilters | None = None,
    ) -> list[UserDTO]:
        query = select(UserModel)

        if filters:
            if filters.role:
                query = query.where(UserModel.role == filters.role)
            if filters.is_active is not None:
                query = query.where(UserModel.is_active == filters.is_active)

        # Dynamic sorting
        order_col = getattr(UserModel, sort_by)
        if sort_order == SortOrder.DESC:
            order_col = order_col.desc()
        query = query.order_by(order_col)

        query = query.limit(limit).offset(offset)

        result = await self._session.execute(query)
        rows = result.scalars().all()

        return [self._to_dto(row) for row in rows]
```

---

## Command vs Query Comparison

| Aspect | Command | Query |
|--------|---------|-------|
| **Purpose** | Modify state | Read state |
| **Handler name** | `{Verb}{Noun}Interactor` | `{Verb}{Noun}QueryService` |
| **Input** | Command DTO | Query DTO |
| **Output** | ID or void | DTO or list[DTO] |
| **Transaction** | Required | Not required |
| **Repository** | Write Repository | Query Gateway |
| **Returns** | Domain types | Plain DTOs |
| **Side effects** | Yes (DB writes, events) | No |
| **Caching** | Generally no | Can be cached |

---

## Advanced: Event Sourcing Integration

```python
# With event sourcing, commands produce events
class CreateUserInteractor:
    async def execute(self, cmd: CreateUserCommand) -> UserId:
        # Create entity (generates events internally)
        user = User.create(
            email=Email(cmd.email),
            password_hash=await self._hasher.hash(cmd.password),
        )

        # Save events to event store
        await self._event_store.save(user.id, user.pending_events)

        # Clear pending events
        user.clear_events()

        return user.id

# Query side rebuilds from events or uses projections
class UserProjection:
    async def on_user_created(self, event: UserCreated) -> None:
        await self._read_db.execute(
            "INSERT INTO users_view (id, email, ...) VALUES (...)"
        )
```

---

## Eco² Project Examples

```python
# apps/chat_worker/application/commands/classify_intent_command.py
@dataclass(frozen=True)
class ClassifyIntentCommand:
    message: str
    conversation_id: str
    user_id: str

class ClassifyIntentInteractor:
    def __init__(
        self,
        classifier: IntentClassifier,
        cache: IntentCache,
    ):
        self._classifier = classifier
        self._cache = cache

    async def execute(self, cmd: ClassifyIntentCommand) -> IntentResult:
        # Check cache first
        cached = await self._cache.get(cmd.message)
        if cached:
            return cached

        # Classify
        result = await self._classifier.classify(cmd.message)

        # Cache result
        await self._cache.set(cmd.message, result)

        return result
```
