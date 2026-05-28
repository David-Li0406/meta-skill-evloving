"""
High-Performance conftest.py Template for FastAPI + Pytest

Features:
- Session-scoped async engine (created once)
- Function-scoped sessions with transaction rollback
- AsyncClient for native async testing
- Factory fixtures for test data creation
"""
import pytest
import asyncio
from typing import AsyncGenerator, Callable
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool

# Update these imports to match your project structure
from app.main import app
from app.database import Base, get_db
from app.models import User, Item  # Add your models

# Test database URL - use SQLite for speed, or match production DB
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# For PostgreSQL: "postgresql+asyncpg://user:pass@localhost/test_db"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session-scoped async fixtures."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    """
    Session-scoped database engine.

    - Created once at start of test session
    - Schema created once, dropped at end
    - NullPool prevents connection issues in async tests
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False,  # Set True for SQL debugging
    )

    # Create all tables once
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup at end of session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Function-scoped database session with transaction rollback.

    Each test runs in a transaction that rolls back after completion.
    This is much faster than recreating schemas per test.
    """
    async_session_factory = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client with dependency override.

    Uses httpx.AsyncClient for native async support.
    ~20% faster than sync TestClient for async endpoints.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ============================================================================
# Factory Fixtures - Customize for your models
# ============================================================================

@pytest.fixture
def user_factory(db_session: AsyncSession) -> Callable:
    """Factory for creating test users."""
    async def _create_user(
        email: str = "test@example.com",
        password: str = "hashedpassword",
        is_active: bool = True,
        **kwargs
    ) -> User:
        user = User(
            email=email,
            hashed_password=password,
            is_active=is_active,
            **kwargs
        )
        db_session.add(user)
        await db_session.flush()
        await db_session.refresh(user)
        return user

    return _create_user


@pytest.fixture
def item_factory(db_session: AsyncSession) -> Callable:
    """Factory for creating test items."""
    async def _create_item(
        name: str = "Test Item",
        price: float = 10.0,
        quantity: int = 1,
        **kwargs
    ) -> Item:
        item = Item(
            name=name,
            price=price,
            quantity=quantity,
            **kwargs
        )
        db_session.add(item)
        await db_session.flush()
        await db_session.refresh(item)
        return item

    return _create_item


# ============================================================================
# Authentication Fixtures
# ============================================================================

@pytest.fixture
async def authenticated_client(
    client: AsyncClient,
    user_factory: Callable,
) -> AsyncGenerator[AsyncClient, None]:
    """Client with valid authentication token."""
    from app.auth import create_access_token, get_current_user

    user = await user_factory()
    token = create_access_token({"sub": str(user.id)})

    # Override auth dependency
    app.dependency_overrides[get_current_user] = lambda: user

    client.headers["Authorization"] = f"Bearer {token}"
    yield client

    app.dependency_overrides.pop(get_current_user, None)


# ============================================================================
# Performance Monitoring (Optional)
# ============================================================================

@pytest.fixture(autouse=True)
def log_slow_tests(request):
    """Log tests that take longer than 1 second."""
    import time
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    if duration > 1.0:
        print(f"\n[SLOW TEST] {request.node.name}: {duration:.2f}s")
