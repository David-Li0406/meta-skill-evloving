# Port & Adapter Pattern Reference

## Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                    Hexagonal Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Driving Side                              Driven Side          │
│   (Primary)                                 (Secondary)          │
│                                                                  │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│   │  HTTP   │───▶│ Driving │───▶│  App    │───▶│ Driven  │───▶ │
│   │ Request │    │  Port   │    │  Core   │    │  Port   │     │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│        │              ▲              │              ▲       │   │
│        │              │              │              │       │   │
│   ┌─────────┐         │         ┌───┴───┐         │   ┌────┴──┐│
│   │Controller│        │         │Domain │         │   │Database│
│   │(Adapter)│─────────┘         │Logic  │         └───│Adapter│ │
│   └─────────┘                   └───────┘             └───────┘ │
│                                                                  │
│   Adapters IMPLEMENT Ports                                      │
│   Core DEFINES Ports (interfaces)                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Port Types

### 1. Domain Ports

Located in `domain/ports/` - abstractions for domain-level concerns.

```python
# domain/ports/password_hasher.py
from typing import Protocol

class PasswordHasher(Protocol):
    """Domain port for password hashing"""

    async def hash(self, raw_password: str) -> PasswordHash: ...
    async def verify(self, raw_password: str, hash: PasswordHash) -> bool: ...


# domain/ports/id_generator.py
class IdGenerator(Protocol):
    """Domain port for ID generation"""

    def generate(self) -> UserId: ...
```

### 2. Application Ports

Located in `application/ports/` - abstractions for application-level concerns.

```python
# application/ports/user_repository.py (Write operations)
class UserRepository(Protocol):
    """Application port for user write operations"""

    async def get_by_id(self, id: UserId) -> User | None: ...
    async def get_by_email(self, email: Email) -> User | None: ...
    async def save(self, user: User) -> None: ...
    async def delete(self, user: User) -> None: ...


# application/ports/user_query_gateway.py (Read operations)
class UserQueryGateway(Protocol):
    """Application port for user read operations (CQRS)"""

    async def get_by_id(self, id: UUID) -> UserDTO | None: ...
    async def list_all(
        self,
        limit: int,
        offset: int,
        filters: UserFilters | None = None,
    ) -> list[UserDTO]: ...
    async def count(self, filters: UserFilters | None = None) -> int: ...


# application/ports/transaction_manager.py
class TransactionManager(Protocol):
    """Application port for transaction control"""

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


# application/ports/flusher.py
class Flusher(Protocol):
    """Application port for flushing pending changes"""

    async def flush(self) -> None: ...
```

### 3. Infrastructure Internal Ports

Located in `infrastructure/.../ports/` - for swappable infrastructure components.

```python
# infrastructure/cache/ports/cache_store.py
class CacheStore(Protocol):
    """Infrastructure port for cache - allows Redis/Memcached swap"""

    async def get(self, key: str) -> bytes | None: ...
    async def set(self, key: str, value: bytes, ttl: int | None = None) -> None: ...
    async def delete(self, key: str) -> None: ...
```

---

## Adapter Implementations

### Repository Adapter (PostgreSQL)

```python
# infrastructure/adapters/postgres_user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class PostgresUserRepository:
    """Adapter implementing UserRepository using PostgreSQL"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: UserId) -> User | None:
        stmt = select(UserModel).where(UserModel.id == id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: Email) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, user: User) -> None:
        model = self._to_model(user)
        merged = await self._session.merge(model)
        self._session.add(merged)

    async def delete(self, user: User) -> None:
        stmt = select(UserModel).where(UserModel.id == user.id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)

    # Mapping methods
    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            email=Email(model.email),
            password_hash=PasswordHash(model.password_hash),
            role=UserRole(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id.value,
            email=entity.email.value,
            password_hash=entity.password_hash.value,
            role=entity.role.value,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )
```

### Password Hasher Adapter (bcrypt)

```python
# infrastructure/adapters/bcrypt_password_hasher.py
import bcrypt
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BcryptPasswordHasher:
    """Adapter implementing PasswordHasher using bcrypt"""

    def __init__(
        self,
        work_factor: int = 12,
        executor: ThreadPoolExecutor | None = None,
    ):
        self._work_factor = work_factor
        self._executor = executor or ThreadPoolExecutor(max_workers=4)

    async def hash(self, raw_password: str) -> PasswordHash:
        loop = asyncio.get_running_loop()
        hash_bytes = await loop.run_in_executor(
            self._executor,
            self._hash_sync,
            raw_password,
        )
        return PasswordHash(hash_bytes.decode())

    async def verify(self, raw_password: str, hash: PasswordHash) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._executor,
            self._verify_sync,
            raw_password,
            hash,
        )

    def _hash_sync(self, raw_password: str) -> bytes:
        salt = bcrypt.gensalt(rounds=self._work_factor)
        return bcrypt.hashpw(raw_password.encode(), salt)

    def _verify_sync(self, raw_password: str, hash: PasswordHash) -> bool:
        return bcrypt.checkpw(raw_password.encode(), hash.value.encode())
```

### External API Adapter (gRPC)

```python
# infrastructure/integrations/grpc_character_client.py
import grpc

class GrpcCharacterClient:
    """Adapter for Character service via gRPC"""

    def __init__(self, channel: grpc.aio.Channel):
        self._stub = CharacterServiceStub(channel)

    async def get_character(self, character_id: str) -> CharacterDTO | None:
        try:
            request = GetCharacterRequest(id=character_id)
            response = await self._stub.GetCharacter(request)
            return CharacterDTO(
                id=response.id,
                name=response.name,
                personality=response.personality,
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise CharacterServiceError(str(e)) from e

    async def list_characters(self) -> list[CharacterDTO]:
        request = ListCharactersRequest()
        response = await self._stub.ListCharacters(request)
        return [
            CharacterDTO(id=c.id, name=c.name, personality=c.personality)
            for c in response.characters
        ]
```

---

## Dependency Injection Wiring

### Using FastAPI Depends

```python
# setup/dependencies.py
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return PostgresUserRepository(session)

def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher(work_factor=12)

def get_create_user_interactor(
    repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    tx: TransactionManager = Depends(get_transaction_manager),
) -> CreateUserInteractor:
    return CreateUserInteractor(
        user_repo=repo,
        hasher=hasher,
        tx=tx,
    )
```

---

## Testing with Mock Adapters

```python
# tests/unit/mocks.py
class MockUserRepository:
    """In-memory mock for testing"""

    def __init__(self):
        self._users: dict[UserId, User] = {}

    async def get_by_id(self, id: UserId) -> User | None:
        return self._users.get(id)

    async def save(self, user: User) -> None:
        self._users[user.id] = user


class MockPasswordHasher:
    """Simple mock that doesn't actually hash"""

    async def hash(self, raw_password: str) -> PasswordHash:
        return PasswordHash(f"hashed_{raw_password}")

    async def verify(self, raw_password: str, hash: PasswordHash) -> bool:
        return hash.value == f"hashed_{raw_password}"


# tests/unit/test_create_user.py
async def test_create_user_success():
    # Arrange
    repo = MockUserRepository()
    hasher = MockPasswordHasher()
    tx = MockTransactionManager()
    interactor = CreateUserInteractor(repo, hasher, tx)

    # Act
    user_id = await interactor.execute(
        CreateUserCommand(email="test@example.com", password="secret123")
    )

    # Assert
    assert user_id is not None
    saved_user = await repo.get_by_id(user_id)
    assert saved_user is not None
    assert saved_user.email.value == "test@example.com"
```

---

## Port Naming Conventions

| Purpose | Port Name | Adapter Name |
|---------|-----------|--------------|
| Entity persistence | `{Entity}Repository` | `Postgres{Entity}Repository` |
| Read-only queries | `{Entity}QueryGateway` | `Postgres{Entity}Reader` |
| External service | `{Service}Client` | `Grpc{Service}Client` |
| Hashing/Crypto | `{Action}er` | `Bcrypt{Action}er` |
| ID generation | `{Entity}IdGenerator` | `Uuid{Entity}IdGenerator` |
| Caching | `CacheStore` | `RedisCacheStore` |
| Messaging | `MessagePublisher` | `RabbitMQPublisher` |
