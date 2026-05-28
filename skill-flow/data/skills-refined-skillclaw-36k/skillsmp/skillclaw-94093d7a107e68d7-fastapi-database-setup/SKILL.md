---
name: fastapi-database-setup
description: Use this skill when you need to configure an async SQLAlchemy 2.0 engine, session factory, and database dependency for FastAPI applications.
---

# FastAPI Database Setup

## Overview

This skill covers setting up async SQLAlchemy 2.0 with PostgreSQL using the asyncpg driver.

## Create `database.py`

Create `src/app/database.py`:

```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.config import settings

# Create async engine
engine = create_async_engine(
    str(settings.database_url),
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Verify connections before use
)

# Create async session factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    
    Yields an async session and ensures it's closed after use.
    Uses the same session throughout the request lifecycle.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
```

## Create `dependencies.py`

Create `src/app/dependencies.py`:

```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    
    Usage in routers:
        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
```

## Key Configuration Options

### Engine Options

| Option          | Purpose                             | Default         |
| --------------- | ----------------------------------- | --------------- |
| `echo`          | Log all SQL statements              | `False`         |
| `pool_size`     | Number of persistent connections    | `5`             |
| `max_overflow`  | Additional connections allowed      | `10`            |
| `pool_pre_ping` | Test connection validity            | `True`          |
| `pool_recycle`  | Recycle connections after N seconds | `-1` (disabled) |

### Session Options

| Option          | Purpose                             | Recommended     |
| --------------- | ----------------------------------- | --------------- |
| `expire_on_commit` | Controls object expiration after commit | `False`      |
| `autocommit`    | Controls automatic commit behavior  | `False`         |
| `autoflush`     | Controls automatic flushing behavior | `False`         |