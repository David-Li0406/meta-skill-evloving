# Async Conversion (Sync → Async)

## Overview
Converting synchronous Python code to async, replacing blocking operations with async equivalents for production FastAPI applications.

## Problem Statement
**The async conversion challenge:**
- Simply adding `async/await` keywords doesn't make code async
- Blocking operations (requests, time.sleep, sync DB) kill event loop performance
- `run_in_executor` is a band-aid, not a solution

## Library Mapping

| Sync Library   | Async Replacement           | Notes               |
|----------------|-----------------------------|---------------------|
| `requests`     | `httpx.AsyncClient`         | HTTP calls          |
| `sqlalchemy`   | `sqlalchemy.ext.asyncio`    | Database operations |
| `time.sleep()` | `asyncio.sleep()`           | Delays              |
| `open()`       | `aiofiles`                  | File I/O            |
| `subprocess`   | `asyncio.create_subprocess` | Process spawning    |
| `redis`        | `aioredis`                  | Redis operations    |
| `motor`        | `pymongo`                   | MongoDB async       |

## Pattern: Sync → Async

### Before (Blocking)
```python
# Old sync utility
def get_user_data(user_id: int) -> dict:
    # Blocking DB call
    user = db.session.query(User).filter(User.id == user_id).first()

    # Blocking HTTP call
    response = requests.get(f"https://api.external.com/user/{user_id}")

    return {"user": user, "external": response.json()}

# Naive "async" wrapper (STILL BLOCKS!)
@app.get("/users/{user_id}")
async def get_user_endpoint(user_id: int):
    return await run_in_executor(None, get_user_data, user_id)
```

### After (Properly Async)
```python
async def get_user_data(user_id: int, db: AsyncSession) -> dict:
    # Async DB call
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    # Async HTTP call
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.external.com/user/{user_id}")

    return {"user": user, "external": response.json()}

@app.get("/users/{user_id}")
async def get_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_data(user_id, db)
```

## Common Conversion Patterns

### 1. Database Queries
```python
# Sync
users = session.query(User).all()
user = session.query(User).filter(User.id == id).first()

# Async
result = await session.execute(select(User))
users = result.scalars().all()
result = await session.execute(select(User).where(User.id == id))
user = result.scalar_one_or_none()
```

### 2. HTTP Requests
```python
# Sync
response = requests.get(url)
data = response.json()

# Async
async with httpx.AsyncClient() as client:
    response = await client.get(url)
    data = response.json()
```

### 3. File Operations
```python
# Sync
with open('file.txt') as f:
    content = f.read()

# Async
async with aiofiles.open('file.txt') as f:
    content = await f.read()
```

## Anti-Patterns

### ❌ Using `run_in_executor`
```python
# This blocks threads, doesn't scale
await asyncio.to_thread(sync_function, args)
```

### ❌ Mixing sync and async
```python
# Don't call sync code from async
async def bad_pattern():
    result = sync_database_call()  # Blocks!
```

## Testing Async Conversion

```python
@pytest.mark.asyncio
async def test_async_conversion():
    # Verify no blocking calls
    # Verify proper await usage
    result = await async_function()
    assert result is not None
```

## Performance Impact

| Pattern | Throughput | Latency | CPU Usage |
|---------|-----------|---------|-----------|
| Pure blocking | 100 req/s | 500ms | 10% |
| `run_in_executor` | 200 req/s | 250ms | 50% |
| Proper async | 1000+ req/s | 50ms | 20% |

## See Also
- [Database Lifecycle Management](database-lifecycle-management.md)
- [Python to API Conversion](python-to-api-conversion.md)
