# Database Connections in Docker

Patterns for SQLModel, SQLAlchemy, and Neon PostgreSQL in containerized environments.

---

## Connection Pool Strategies

### NullPool (Recommended for Neon/PgBouncer)

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    pool_pre_ping=True,
)
```

**When to use**:
- Neon PostgreSQL (has built-in PgBouncer)
- External PgBouncer
- Serverless/Lambda deployments
- Kubernetes with many pods

**Why**: External pooler manages connections. Application-level pooling conflicts with external poolers.

### QueuePool (Default for Direct Connections)

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
```

**When to use**:
- Direct PostgreSQL connection
- No external connection pooler
- Single container deployment

---

## Neon PostgreSQL Configuration

### Connection Strings

```bash
# Pooled connection (for application)
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx-pooler.region.aws.neon.tech/db?sslmode=require

# Direct connection (for migrations)
DATABASE_URL_DIRECT=postgresql+asyncpg://user:pass@ep-xxx.region.aws.neon.tech/db?sslmode=require
```

### Docker Environment

```yaml
# docker-compose.yml
services:
  api:
    environment:
      - DATABASE_URL=${NEON_POOLED_URL}

  migrate:
    environment:
      # Use direct connection for Alembic
      - DATABASE_URL=${NEON_DIRECT_URL}
```

### Neon-Specific Settings

```python
# Disable statement caching (Neon recommendation)
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    pool_pre_ping=True,
    connect_args={
        "statement_cache_size": 0,  # Neon requirement
        "prepared_statement_cache_size": 0,
    },
)
```

---

## SQLModel Session Pattern

### Async Session Factory

```python
# app/core/database.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    poolclass=NullPool,
    pool_pre_ping=True,
    echo=settings.debug,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Dependency Injection

```python
# app/routers/users.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session

@router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()
```

---

## Health Checks

### Database Health Endpoint

```python
# app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

router = APIRouter()

@router.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### docker-compose Health Check

```yaml
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health/db"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    depends_on:
      db:
        condition: service_healthy
```

---

## Connection Handling

### Stale Connection Recovery

```python
# pool_pre_ping tests connection before use
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Required for containerized apps
)
```

### Connection Timeout

```python
from sqlalchemy import event

engine = create_async_engine(
    DATABASE_URL,
    connect_args={
        "timeout": 10,  # Connection timeout
        "command_timeout": 30,  # Query timeout
    },
)
```

### Graceful Shutdown

```python
# app/main.py
from contextlib import asynccontextmanager
from app.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown: close all connections
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

---

## Migrations in Containers

### Alembic Configuration

```python
# alembic/env.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

def run_migrations_online():
    # Use direct connection (not pooled)
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=NullPool,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(do_run_migrations())
```

### Migration Container

```yaml
# docker-compose.yml
services:
  migrate:
    build:
      context: .
      target: runtime
    command: ["alembic", "upgrade", "head"]
    environment:
      # CRITICAL: Use direct connection for migrations
      - DATABASE_URL=${DATABASE_URL_DIRECT}
    profiles:
      - migrate

# Run: docker compose --profile migrate up migrate
```

### Migration Script

```bash
#!/bin/bash
# scripts/migrate.sh

set -e

echo "Running database migrations..."
alembic upgrade head

echo "Migrations complete!"
```

```dockerfile
# Add to testing stage
COPY scripts/migrate.sh /app/scripts/
RUN chmod +x /app/scripts/migrate.sh
```

---

## Testing Database Connections

### Test Configuration

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,  # Shared connection for tests
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def session(engine):
    async with AsyncSession(engine) as session:
        yield session
```

### Integration Test with Real Database

```yaml
# docker-compose.test.yml
services:
  test:
    build:
      target: testing
    environment:
      - DATABASE_URL=postgresql+asyncpg://test:test@db:5432/test
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 5s
      timeout: 5s
      retries: 5
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | DB not ready | Use `depends_on` with health check |
| `Too many connections` | No pooling | Use NullPool with external pooler |
| `Connection reset` | Stale connection | Enable `pool_pre_ping=True` |
| `SSL required` | Missing sslmode | Add `?sslmode=require` to URL |
| `Prepared statement` error | Statement caching | Disable with `statement_cache_size=0` |
| Slow migrations | Using pooled connection | Use direct connection for Alembic |
