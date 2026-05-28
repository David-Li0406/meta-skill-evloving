---
name: async-python
description: Master asynchronous Python programming for high-performance concurrent applications using asyncio, aiohttp, and async database access.
---

# Async Python Skill

Master asynchronous Python programming for high-performance concurrent applications.

## Asyncio Fundamentals

### Basic Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Simulated async fetch."""
    await asyncio.sleep(1)  # Simulates I/O
    return {"url": url, "data": "..."}

async def main():
    # Sequential (slow)
    result1 = await fetch_data("https://api1.com")
    result2 = await fetch_data("https://api2.com")

    # Concurrent (fast)
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
    )
    return results

# Run the event loop
asyncio.run(main())
```

### Task Groups (Python 3.11+)

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data("https://api1.com"))
        task2 = tg.create_task(fetch_data("https://api2.com"))

    # All tasks complete when exiting context
    return task1.result(), task2.result()
```

## HTTP Requests with aiohttp

### Client Session

```python
import aiohttp
import asyncio

async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()

async def main():
    # Reuse session for connection pooling
    async with aiohttp.ClientSession() as session:
        urls = [
            "https://api.example.com/users",
            "https://api.example.com/posts",
            "https://api.example.com/comments",
        ]

        tasks = [fetch_json(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                print(f"Error fetching {url}: {result}")
            else:
                print(f"Got {len(result)} items from {url}")

asyncio.run(main())
```

### With Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def fetch_with_retry(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
        response.raise_for_status()
        return await response.json()
```

## Async Database Access

### With asyncpg (PostgreSQL)

```python
import asyncpg

async def main():
    # Connection pool
    pool = await asyncpg.create_pool(
        "postgresql://user:pass@localhost/db",
        min_size=5,
        max_size=20,
    )

    async with pool.acquire() as conn:
        # Single query
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1", user_id
        )

        # Multiple rows
        users = await conn.fetch(
            "SELECT * FROM users WHERE active = $1", True
        )

        # Transaction
        async with conn.transaction():
            await conn.execute(
                "UPDATE users SET balance = balance - $1 WHERE id = $2",
                100, sender_id
            )
            await conn.execute(
                "UPDATE users SET balance = balance + $1 WHERE id = $2",
                100, receiver_id
            )

    await pool.close()
```

### With SQLAlchemy Async

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.active == True))
        return result.scalars().all()
```

## Concurrency Patterns

### Semaphore for Rate Limiting

```python
async def fetch_with_limit(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

### Producer-Consumer Queue

```python
async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
    # Signal completion
    await queue.put(None)

async def consumer(queue: asyncio.Queue, worker_id: int):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        # Process item
        await process(item)
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=100)

    # Start consumers
    consumers = [
        asyncio.create_task(consumer(queue, i))
        for i in range(5)
    ]

    # Start producer
    await producer(queue, items)

    # Wait for queue to be processed
    await queue.join()

    # Cancel consumers
    for c in consumers:
        c.cancel()
```

### Timeout Handling

```python
async def with_timeout():
    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        print("Operation timed out")
        result = None
    return result
```

## FastAPI Integration

```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    # Shutdown
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with app.state.pool.acquire() as conn:
        yield conn

@app.get("/users/{user_id}")
async def get_user(user_id: int, db = Depends(get_db)):
    user = await db.fetchrow(
        "SELECT * FROM users WHERE id = $1", user_id
    )
    return user
```

## Performance Tips

```python
# 1. Use uvloop for faster event loop
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 2. Batch database operations
async def insert_many(items: list[dict]):
    async with pool.acquire() as conn:
        await conn.executemany(
            "INSERT INTO items (name, value) VALUES ($1, $2)",
            [(i["name"], i["value"]) for i in items]
        )

# 3. Stream large responses
async def stream_response():
    async with session.get(url) as response:
        async for chunk in response.content.iter_chunked(8192):
            yield chunk
```

## Anti-Patterns

❌ Blocking I/O in async code (`time.sleep`, sync HTTP)  
❌ Creating new sessions per request  
❌ Not closing resources properly  
❌ Ignoring exceptions in gather  
❌ Running CPU-bound work in event loop  

✅ Use async versions (`asyncio.sleep`, `aiohttp`)  
✅ Reuse connection pools  
✅ Use context managers  
✅ Handle exceptions: `return_exceptions=True`  
✅ Use `run_in_executor` for CPU work  

```python
# CPU-bound work
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(
    None,  # Default executor
    cpu_intensive_function,
    arg1, arg2
)
```

## When to Use This Skill

Use this skill when you need to:

- Handle multiple I/O operations concurrently (API calls, database queries)
- Build async web servers or clients
- Process data streams asynchronously
- Implement producer-consumer patterns with async queues
- Run blocking I/O operations without blocking the event loop
- Create async context managers for resource management
- Implement async iterators for streaming data
- Control concurrency with semaphores and locks
- Handle timeouts and cancellation in async operations
- Mix CPU-bound and I/O-bound operations efficiently

## Best Practices

- Use `asyncio.run()` for the main entry point
- Create tasks with `asyncio.create_task()` for concurrent execution
- Use `gather()` when you need all results
- Use `wait()` when you need fine-grained control
- Always handle `CancelledError` in long-running tasks
- Use semaphores to limit concurrent operations
- Prefer async context managers for resource management
- Use `asyncio.Queue` for producer-consumer patterns
- Run blocking I/O in thread pool with `run_in_executor()`
- Run CPU-bound tasks in process pool
- Set appropriate timeouts for network operations
- Use structured concurrency patterns (nurseries)

## Common Pitfalls

- Forgetting to await coroutines (creates coroutine object, doesn't run)
- Blocking the event loop with CPU-intensive work
- Not handling task cancellation properly
- Using `time.sleep()` instead of `asyncio.sleep()`
- Creating too many concurrent tasks without limits
- Not closing resources properly in async context
- Mixing blocking and async code incorrectly
- Not handling exceptions in background tasks
- Forgetting to call `task_done()` with `Queue`
- Using global event loop instead of `asyncio.run()`

## Resources

- [asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [PEP 492 - Coroutines](https://peps.python.org/pep-0492/)
- [PEP 525 - Async Generators](https://peps.python.org/pep-0525/)
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)