---
title: Async Patterns
impact: CRITICAL
impactDescription: Prevents server blocking, enables concurrency
tags: async, await, blocking, performance, asyncio
---

# Async Patterns

FastAPI runs on async, blocking operations freeze the entire server.

## Rule 1: Never Use Blocking I/O in Async Functions

```python
# ❌ INCORRECT - blocks event loop
import time
import requests

@app.get("/data")
async def get_data():
    time.sleep(5)  # blocks ALL requests for 5 seconds!
    response = requests.get("https://api.example.com")  # blocking!
    return response.json()

# ✅ CORRECT - non-blocking
import asyncio
import httpx

@app.get("/data")
async def get_data():
    await asyncio.sleep(5)  # non-blocking
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
    return response.json()
```

## Rule 2: Use run_in_executor for Blocking Libraries

```python
# ❌ INCORRECT - blocking library in async context
@app.get("/process")
async def process_image():
    # PIL is blocking
    result = Image.open("large.jpg").resize((100, 100))
    return {"status": "done"}

# ✅ CORRECT - run blocking code in threadpool
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def blocking_process():
    return Image.open("large.jpg").resize((100, 100))

@app.get("/process")
async def process_image():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, blocking_process)
    return {"status": "done"}
```

## Rule 3: Use Async Database Drivers

```python
# ❌ INCORRECT - sync driver
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql://...")  # sync!

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# ✅ CORRECT - async driver
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("postgresql+asyncpg://...")

async def get_db():
    async with AsyncSession(engine) as session:
        yield session
```

## Rule 4: Parallel Async Operations

```python
# ❌ INCORRECT - sequential (3x latency)
async def get_dashboard_data():
    user = await get_user()
    orders = await get_orders()
    notifications = await get_notifications()
    return {"user": user, "orders": orders, "notifications": notifications}

# ✅ CORRECT - parallel (1x latency)
async def get_dashboard_data():
    user, orders, notifications = await asyncio.gather(
        get_user(),
        get_orders(),
        get_notifications()
    )
    return {"user": user, "orders": orders, "notifications": notifications}
```

## Rule 5: Use def for CPU-Bound Sync Operations

```python
# For simple CPU-bound operations, use def (not async def)
# FastAPI will run it in a threadpool automatically

# ✅ CORRECT - simple sync endpoint
@app.get("/compute")
def compute_something():
    # This runs in threadpool, doesn't block other async handlers
    result = heavy_cpu_computation()
    return {"result": result}

# ✅ CORRECT - async endpoint for I/O
@app.get("/fetch")
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
    return response.json()
```

## Rule 6: Async Context Managers

```python
# ✅ CORRECT - proper async resource management
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connection():
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()

@app.get("/data")
async def get_data():
    async with get_connection() as conn:
        return await conn.fetch_data()
```

## Detection Checklist

Look for these blocking patterns:

- [ ] `time.sleep()` in async functions
- [ ] `requests.get/post()` instead of `httpx` or `aiohttp`
- [ ] Sync database drivers (`psycopg2` instead of `asyncpg`)
- [ ] `open()` for file I/O (use `aiofiles`)
- [ ] Sequential `await` when parallel is possible
- [ ] CPU-heavy operations without threadpool
