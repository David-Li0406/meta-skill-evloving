# FastAPI Production Troubleshooting

## Connection Issues

### "Too many connections" database error

**Symptoms:**
- Error: `FATAL: remaining connection slots are reserved`
- Occurs under load or with multiple workers

**Causes:**
1. Engine created at import time (not in lifespan)
2. Missing `engine.dispose()` in shutdown
3. Pool parameters not configured

**Fix:**
```python
# ❌ Wrong - engine at import
engine = create_async_engine(DATABASE_URL)

# ✅ Correct - engine in lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
    )
    yield
    await engine.dispose()  # Critical!
```

### "Server closed the connection" unexpectedly

**Symptoms:**
- Error: `server closed the connection unexpectedly`
- Occurs after idle period

**Cause:** Database closes idle connections

**Fix:**
```python
engine = create_async_engine(
    DATABASE_URL,
    pool_recycle=3600,  # Recycle every hour
)
```

## Performance Issues

### Slow requests under load

**Symptoms:**
- Requests timeout
- High latency

**Causes:**
1. Blocking operations in async functions
2. Using `requests` library
3. Too small connection pool

**Fixes:**
```python
# ❌ Wrong - blocking
def get_data():
    return requests.get(url)  # Blocks!

# ✅ Correct - async
async def get_data():
    async with httpx.AsyncClient() as client:
        return await client.get(url)
```

### Memory leaks

**Symptoms:**
- Memory usage grows over time
- OOM crashes

**Causes:**
1. Loading entire files into memory
2. Not closing database sessions
3. Caching without limits

**Fixes:**
```python
# ❌ Wrong - loads entire file
content = await file.read()  # 1GB file!

# ✅ Correct - stream
async for chunk in file.stream_chunked(1024*1024):
    process(chunk)
```

## Testing Issues

### Tests hang indefinitely

**Symptoms:**
- Tests never complete
- No error output

**Cause:** Using `TestClient` with async app

**Fix:**
```python
# ❌ Wrong
from fastapi.testclient import TestClient
client = TestClient(app)

# ✅ Correct
from httpx import AsyncClient
async with AsyncClient(app=app) as client:
    ...
```

### Tests pass isolation but fail together

**Symptoms:**
- Individual tests pass
- `pytest` fails when running all tests

**Cause:** Database bleeding between tests

**Fix:**
```python
@pytest.fixture
async def db_session():
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()  # Critical!
```

## Pydantic Issues

### Validation errors on valid data

**Symptoms:**
- 422 errors on valid input
- "field required" errors

**Cause:** Pydantic v1 vs v2 syntax

**Fix:**
```python
# Pydantic v1
data = user.dict(exclude_unset=True)

# Pydantic v2
data = user.model_dump(exclude_unset=True)
```

### Partial updates don't work

**Symptoms:**
- Unprovided fields become `None`
- Data gets corrupted

**Fix:**
```python
# ❌ Wrong
update_data = user_update.model_dump()

# ✅ Correct
update_data = user_update.model_dump(exclude_unset=True)
```

## Deployment Issues

### Workers crash on startup

**Symptoms:**
- Workers exit immediately
- "Address already in use" errors

**Cause:** All workers trying to create pools simultaneously

**Fix:**
```python
# Stagger worker startup or use single process
# For gunicorn:
# gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 502 errors after deployment

**Symptoms:**
- Intermittent 502 errors
- Requests timeout

**Causes:**
1. Workers not ready
2. Database not accessible
3. Port conflicts

**Fix:**
```python
# Add health check
@app.get("/health")
async def health():
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except:
        raise HTTPException(status_code=503)
```

## Debugging Tips

### Enable SQL logging

```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Show all SQL queries
)
```

### Check connection pool status

```python
@app.get("/debug/pool")
async def pool_status():
    pool = app.state.db_engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
    }
```

### Profile slow endpoints

```python
import time

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Getting Help

1. Check logs: `tail -f logs/app.log`
2. Verify database: `psql -h localhost -U user -d db`
3. Test health endpoint: `curl http://localhost:8000/health`
4. Check pool status: `curl http://localhost:8000/debug/pool`
