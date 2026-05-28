# High-Performance Conftest Patterns

## Fixture Scoping Strategy

| Scope | Use Case | Performance Impact |
|-------|----------|-------------------|
| `session` | DB engine, app instance | Create once, reuse across all tests |
| `function` | DB session with rollback | Isolation without schema recreation |
| `class` | Shared state within test class | Moderate reuse |

## Async Database Engine (Session Scope)

```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base, get_db

# Use NullPool for testing - avoids connection pool issues with async
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session-scoped async fixtures."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def async_engine():
    """Session-scoped engine - created once, reused across all tests."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,  # Prevents connection pool issues in tests
        echo=False  # Set True for debugging SQL
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
```

## Transaction Rollback Pattern (Function Scope)

```python
@pytest.fixture(scope="function")
async def db_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Function-scoped session with transaction rollback.

    Performance: Avoids schema recreation per test.
    Each test runs in a transaction that rolls back.
    """
    async_session = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()  # Rollback after each test
```

## AsyncClient Fixture

```python
@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client with dependency override.

    Why AsyncClient over TestClient:
    - Native async support (no sync/async bridging overhead)
    - ~20% faster for async endpoints
    - Proper handling of async context managers
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
```

## Authenticated Client Fixture

```python
@pytest.fixture
async def auth_client(client: AsyncClient, db_session: AsyncSession):
    """Client with authentication headers."""
    # Create test user
    user = User(email="test@example.com", hashed_password="...")
    db_session.add(user)
    await db_session.flush()

    # Generate token
    token = create_access_token({"sub": str(user.id)})
    client.headers["Authorization"] = f"Bearer {token}"

    yield client
```

## Factory Fixtures

```python
@pytest.fixture
def item_factory(db_session: AsyncSession):
    """Factory for creating test items with defaults."""
    async def _create_item(
        name: str = "Test Item",
        price: float = 10.0,
        quantity: int = 1
    ) -> Item:
        item = Item(name=name, price=price, quantity=quantity)
        db_session.add(item)
        await db_session.flush()
        await db_session.refresh(item)
        return item
    return _create_item
```

## Complete conftest.py Template

```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator, Callable
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base, get_db
from app.models import User, Item

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture
def user_factory(db_session: AsyncSession) -> Callable:
    async def _create(email: str = "test@example.com", **kwargs) -> User:
        user = User(email=email, **kwargs)
        db_session.add(user)
        await db_session.flush()
        await db_session.refresh(user)
        return user
    return _create

@pytest.fixture
def item_factory(db_session: AsyncSession) -> Callable:
    async def _create(name: str = "Item", price: float = 10.0, **kwargs) -> Item:
        item = Item(name=name, price=price, **kwargs)
        db_session.add(item)
        await db_session.flush()
        await db_session.refresh(item)
        return item
    return _create
```
