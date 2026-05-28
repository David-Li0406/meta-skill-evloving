# Engine Configuration

Database-specific engine configurations for production use.

---

## SQLite Configuration

Best for development and small applications.

```python
from sqlmodel import create_engine
from sqlalchemy.pool import StaticPool

# Development (in-memory)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,  # SQL logging for debug
)

# Development (file-based)
engine = create_engine(
    "sqlite:///./database.db",
    connect_args={"check_same_thread": False},
    echo=True,
)

# Testing (isolated in-memory)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

### SQLite Notes
- `check_same_thread=False`: Required for FastAPI async
- `StaticPool`: Single connection for in-memory databases
- No connection pooling needed for file-based SQLite
- WAL mode for better concurrent read/write: `PRAGMA journal_mode=WAL`

---

## PostgreSQL Configuration

Recommended for production.

```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

# Basic connection
DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"

# With SSL
DATABASE_URL = "postgresql://user:password@host:5432/dbname?sslmode=require"

# Production configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,           # Base connections to maintain
    max_overflow=10,       # Extra connections under load
    pool_timeout=30,       # Seconds to wait for connection
    pool_recycle=1800,     # Recycle every 30 minutes
    pool_pre_ping=True,    # Verify connection before use
    echo=False,            # Disable SQL logging
)
```

### Connection Pool Sizing Guide

| Application Type | pool_size | max_overflow |
|------------------|-----------|--------------|
| Small API | 5 | 5 |
| Medium API | 10 | 20 |
| High-traffic API | 20 | 40 |
| Worker process | 2 | 5 |

**Rule**: `pool_size + max_overflow < PostgreSQL max_connections`

### PostgreSQL Async (Optional)

```python
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Async engine
async_engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost:5432/dbname",
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

# Async session
async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session
```

---

## MySQL Configuration

```python
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool

DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/dbname"

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,     # MySQL default wait_timeout is 8 hours
    pool_pre_ping=True,
    echo=False,
)
```

### MySQL Notes
- Use `mysql+pymysql://` driver
- Set `pool_recycle` < MySQL `wait_timeout`
- Consider `charset=utf8mb4` for full Unicode support

---

## Environment-Based Configuration

Production pattern using environment variables.

```python
import os
from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool, NullPool

def get_engine():
    """Create engine based on environment."""
    database_url = os.getenv("DATABASE_URL")
    environment = os.getenv("ENVIRONMENT", "development")

    if environment == "production":
        return create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=False,
        )
    elif environment == "testing":
        return create_engine(
            database_url or "sqlite:///:memory:",
            poolclass=NullPool,  # No pooling for tests
            echo=False,
        )
    else:  # development
        return create_engine(
            database_url or "sqlite:///./dev.db",
            connect_args={"check_same_thread": False} if "sqlite" in (database_url or "") else {},
            echo=True,
        )

engine = get_engine()
```

---

## Connection Pool Types

| Pool Type | Use Case |
|-----------|----------|
| `QueuePool` | Default, general purpose, maintains pool of connections |
| `NullPool` | No pooling, new connection each time (tests, serverless) |
| `StaticPool` | Single connection reused (SQLite in-memory) |
| `SingletonThreadPool` | One connection per thread |
| `AssertionPool` | Debug mode, ensures single connection |

### When to Use Each

```python
from sqlalchemy.pool import QueuePool, NullPool, StaticPool

# Web application (default)
engine = create_engine(url, poolclass=QueuePool)

# Serverless (Lambda, Cloud Functions)
engine = create_engine(url, poolclass=NullPool)

# SQLite in-memory testing
engine = create_engine("sqlite:///:memory:", poolclass=StaticPool)

# Background workers with limited connections
engine = create_engine(
    url,
    poolclass=QueuePool,
    pool_size=2,
    max_overflow=3,
)
```

---

## Engine Events and Hooks

```python
from sqlalchemy import event

engine = create_engine(DATABASE_URL)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configure SQLite on each connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Called when connection retrieved from pool."""
    pass

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """Called when connection returned to pool."""
    pass
```

---

## Database Initialization

```python
from sqlmodel import SQLModel, create_engine

def init_db(engine):
    """Initialize database tables."""
    # Import all models to register them
    from app.models import User, Order, Item  # noqa

    # Create all tables
    SQLModel.metadata.create_all(engine)

def drop_db(engine):
    """Drop all tables (use with caution)."""
    SQLModel.metadata.drop_all(engine)

# Usage
if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    init_db(engine)
```

### With Alembic (Recommended for Production)

```python
# Don't use create_all in production
# Instead, use Alembic migrations

# alembic.ini
# [alembic]
# script_location = alembic

# alembic/env.py
from app.models import SQLModel
target_metadata = SQLModel.metadata

# Generate migration
# alembic revision --autogenerate -m "Add user table"

# Apply migration
# alembic upgrade head
```
