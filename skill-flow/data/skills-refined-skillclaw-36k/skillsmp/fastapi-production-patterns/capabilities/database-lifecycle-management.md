# Database Lifecycle Management

## Overview
Proper management of database engine lifecycle to prevent connection leaks and pool exhaustion in production FastAPI applications.

## Problem Statement
**Silent failures that kill production:**
- Engines created at import time never close connections
- Missing shutdown handlers cause connection leaks
- Unconfigured connection pools exhaust under load
- "Too many connections" errors under concurrent load

## Pattern

### ❌ Broken (Baseline Failure)
```python
# database.py - Created at import time!
engine = create_async_engine(DATABASE_URL)

# main.py - Deprecated pattern
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# NO shutdown handler - connections leak forever!
```

### ✅ Production Pattern
```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - create engine HERE, not at import
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=10,           # Critical for multi-worker deployments
        max_overflow=20,        # Allow bursting above pool_size
        pool_recycle=3600,      # Recycle connections after 1 hour
    )
    app.state.db_engine = engine

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown - CRITICAL: close connections
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

async def get_db() -> AsyncSession:
    async with AsyncSession(app.state.db_engine) as session:
        yield session
```

## Key Parameters

| Parameter | Purpose | Typical Value |
|-----------|---------|---------------|
| `pool_size` | Base connection pool size | 10-20 |
| `max_overflow` | Additional connections under load | 20-40 |
| `pool_recycle` | Prevents DB closing idle connections | 3600 (1 hour) |
| `pool_pre_ping` | Test connections before use | `True` |

## Symptoms of Misconfiguration

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| "Too many connections" DB error | Missing shutdown handler | Add `engine.dispose()` |
| Connection timeout under load | Pool too small or missing `max_overflow` | Increase pool parameters |
| "Server closed the connection" unexpectedly | DB closing idle connections | Set `pool_recycle` |
| Workers start slowly | All workers creating pools simultaneously | Stagger worker startup |

## Testing

```python
# Test that connections are properly closed
@pytest.mark.asyncio
async def test_database_lifecycle():
    from test_app import app, lifespan
    from sqlalchemy import text

    async with lifespan(app):
        # Verify engine exists
        assert hasattr(app.state, 'db_engine')

    # After context exit, verify cleanup
    # Engine should be disposed
```

## See Also
- [Async Testing Capability](async-testing.md)
- [Dependency Injection Capability](dependency-injection.md)
