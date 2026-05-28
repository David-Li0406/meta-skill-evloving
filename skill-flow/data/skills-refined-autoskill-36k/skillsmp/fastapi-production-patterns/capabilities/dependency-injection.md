# Dependency Injection

## Overview
FastAPI's dependency injection system for managing shared resources, test doubles, and complex dependency graphs.

## Core Concepts

**Dependency injection (DI)** provides:
- Automatic dependency resolution
- Shared resource management
- Testability through overrides
- Clean separation of concerns

## Patterns

### 1. Basic Dependency

```python
from fastapi import Depends

async def get_db():
    async with AsyncSession(engine) as session:
        yield session

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    return users.scalars().all()
```

### 2. Cached Dependencies

```python
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()

@lru_cache()
def get_redis_client():
    return redis.Redis(host=settings.REDIS_HOST)

@app.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    return settings.dict()
```

### 3. Yield Dependencies (Cleanup)

```python
async def get_db():
    async with AsyncSession(engine) as session:
        yield session
        # Automatic cleanup after response
        await session.close()
```

### 4. Dependency Chaining

```python
async def get_db():
    async with AsyncSession(engine) as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_token(token, db)
    if not user:
        raise HTTPException(status_code=401)
    return user

async def get_admin_user(
    user: User = Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=403)
    return user

@app.get("/admin/dashboard")
async def admin_dashboard(admin: User = Depends(get_admin_user)):
    return {"admin": admin.email}
```

## Testing with Overrides

```python
from fastapi.testclient import TestClient

def test_update_user():
    # Override dependency for test
    async def override_get_db():
        return test_session  # Use test DB

    app.dependency_overrides[get_db] = override_get_db
    try:
        client = TestClient(app)
        response = client.patch("/users/1", json={"name": "Test"})
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()  # Always clean up!
```

## Class-Based Dependencies

```python
class CommonQueryParams:
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at"
    ):
        self.skip = skip
        self.limit = limit
        self.order_by = order_by

@app.get("/items")
async def get_items(commons: CommonQueryParams = Depends()):
    return {
        "items": items[commons.skip:commons.limit],
        "order": commons.order_by
    }
```

## Annotated Dependencies (Python 3.9+)

```python
from typing import Annotated

DbSession = Annotated[AsyncSession, Depends(get_db)]

@app.get("/users")
async def get_users(db: DbSession):
    # No need to repeat Depends(get_db)
    return await db.execute(select(User))
```

## Best Practices

| Practice | Why |
|----------|-----|
| Use `yield` for resources | Automatic cleanup |
| Always clear overrides | Prevents test pollution |
| Chain dependencies | FastAPI auto-resolves |
| Cache singletons | `lru_cache` for config |
| Type hint dependencies | Better IDE support |

## Common Mistakes

```python
# ❌ Manual dependency passing
async def endpoint(db: AsyncSession):
    db = await get_db()  # Wrong!

# ✅ Let FastAPI handle it
async def endpoint(db: AsyncSession = Depends(get_db)):
    pass
```

## See Also
- [Database Lifecycle Management](database-lifecycle-management.md)
- [Async Testing](async-testing.md)
