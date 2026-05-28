---
name: fastapi-testing
description: Use this skill to configure pytest-asyncio with test database fixtures and integration tests for FastAPI routers.
---

# FastAPI Testing Setup

## Overview

This skill covers setting up pytest-asyncio for integration testing FastAPI routers with a test database.

## Test Configuration in `pyproject.toml`

Ensure `pyproject.toml` has the following configuration:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
pythonpath = ["src"]
```

## Add Test Database URL to Config

Update `src/app/config.py` to include a test database URL:

```python
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Test database (optional, falls back to modifying database_url)
    test_database_url: PostgresDsn | None = None

settings = Settings()
```

Update `.env.example` to include the test database URL:

```bash
# Test database
TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname_test
```

## Create `tests/conftest.py`

Create `tests/conftest.py` with the following content:

```python
import asyncio
from collections.abc import Generator
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.config import settings

# Get test database URL
def get_test_database_url() -> str:
    """Get the test database URL."""
    if settings.test_database_url:
        return str(settings.test_database_url)
    # Fallback: modify main database URL to use test database
    main_url = str(settings.database_url)
    return main_url.replace("/dbname", "/dbname_test")

# Create test engine
test_engine = create_async_engine(
    get_test_database_url(),
    echo=False,
    pool_pre_ping=True,
)

# Create test session factory
test_async_session_factory = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
```