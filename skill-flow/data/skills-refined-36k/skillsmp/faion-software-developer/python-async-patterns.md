---
id: python-async-patterns
name: "Python Async Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Python Async Patterns

## Overview

Asynchronous programming in Python enables efficient handling of I/O-bound operations like network requests, database queries, and file operations. This methodology covers asyncio patterns, concurrent execution, and best practices for production async code.

## When to Use

- Building high-performance APIs (FastAPI, aiohttp)
- Making multiple concurrent HTTP requests
- Database operations with async drivers (asyncpg, aiosqlite)
- Real-time applications (WebSockets)
- Background task processing

## Key Principles

1. **Async for I/O** - Use async only for I/O-bound operations
2. **Avoid blocking** - Never call sync I/O in async context
3. **Structured concurrency** - Use TaskGroup for managing tasks
4. **Proper cleanup** - Always handle cancellation and cleanup
5. **Limit concurrency** - Use semaphores to prevent resource exhaustion

## Best Practices

### Basic Async/Await

```python
import asyncio
import httpx


async def fetch_user(user_id: int) -> dict:
    """Fetch user data from API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        response.raise_for_status()
        return response.json()


async def main():
    user = await fetch_user(123)
    print(f"User: {user['name']}")


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
```

### Concurrent Execution with gather

```python
import asyncio
import httpx


async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        return response.json()


async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    """Fetch multiple users concurrently."""
    urls = [f"https://api.example.com/users/{uid}" for uid in user_ids]

    # Create tasks for all requests
    tasks = [fetch_data(url) for url in urls]

    # Execute concurrently - completes when ALL finish
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out errors
    users = [r for r in results if not isinstance(r, Exception)]
    return users


async def main():
    # Sequential: 10 * 0.5s = 5 seconds
    # Concurrent: ~0.5 seconds total
    user_ids = list(range(1, 11))
    users = await fetch_all_users(user_ids)
    print(f"Fetched {len(users)} users")
```

### TaskGroup (Python 3.11+)

```python
import asyncio


async def process_item(item: str) -> str:
    """Process single item."""
    await asyncio.sleep(0.1)  # Simulate I/O
    return f"Processed: {item}"


async def process_all_items(items: list[str]) -> list[str]:
    """Process items concurrently with TaskGroup."""
    results = []

    async with asyncio.TaskGroup() as tg:
        for item in items:
            # Tasks start immediately
            task = tg.create_task(process_item(item))
            # Store task to get result later

    # All tasks completed when exiting context
    # If any task raises, others are cancelled
    return results


# Error handling with TaskGroup
async def safe_process():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(might_fail())
            tg.create_task(might_fail())
    except* ValueError as eg:
        # Handle group of ValueErrors
        for exc in eg.exceptions:
            print(f"ValueError: {exc}")
    except* TypeError as eg:
        # Handle group of TypeErrors
        for exc in eg.exceptions:
            print(f"TypeError: {exc}")
```

### Rate Limiting with Semaphore

```python
import asyncio
import httpx


async def fetch_with_limit(
    urls: list[str],
    max_concurrent: int = 5,
) -> list[dict]:
    """Fetch URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def fetch_one(url: str) -> dict | None:
        async with semaphore:  # Only N concurrent
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, timeout=30.0)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching {url}: {e}")
                return None

    tasks = [fetch_one(url) for url in urls]
    results = await asyncio.gather(*tasks)

    return [r for r in results if r is not None]


# Usage - only 5 requests at a time
async def main():
    urls = [f"https://api.example.com/items/{i}" for i in range(100)]
    data = await fetch_with_limit(urls, max_concurrent=10)
```

### Timeouts

```python
import asyncio


async def slow_operation() -> str:
    """Operation that might take too long."""
    await asyncio.sleep(10)
    return "Done"


async def with_timeout():
    """Execute with timeout."""
    try:
        # Method 1: wait_for
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        return result
    except asyncio.TimeoutError:
        print("Operation timed out")
        return None


# Python 3.11+ - timeout context manager
async def with_timeout_context():
    """Execute with timeout context."""
    try:
        async with asyncio.timeout(2.0):
            result = await slow_operation()
            return result
    except asyncio.TimeoutError:
        print("Operation timed out")
        return None


# Deadline-based timeout
async def with_deadline():
    """Execute with absolute deadline."""
    deadline = asyncio.get_event_loop().time() + 5.0

    try:
        async with asyncio.timeout_at(deadline):
            await task1()
            await task2()  # Remaining time from deadline
    except asyncio.TimeoutError:
        print("Deadline exceeded")
```

### Async Context Managers

```python
import asyncio
from contextlib import asynccontextmanager


class AsyncDatabaseConnection:
    """Async context manager for database."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection = None

    async def __aenter__(self):
        """Connect when entering context."""
        self.connection = await asyncpg.connect(self.dsn)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting."""
        if self.connection:
            await self.connection.close()
        return False  # Don't suppress exceptions


# Function-based async context manager
@asynccontextmanager
async def get_db_session():
    """Get database session with cleanup."""
    session = await create_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


# Usage
async def main():
    async with AsyncDatabaseConnection(DSN) as conn:
        result = await conn.fetch("SELECT * FROM users")

    async with get_db_session() as session:
        await session.execute("INSERT INTO logs VALUES ($1)", ["event"])
```

### Async Generators

```python
import asyncio
from typing import AsyncIterator


async def fetch_pages(base_url: str) -> AsyncIterator[dict]:
    """Fetch paginated data as async generator."""
    page = 1
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(f"{base_url}?page={page}")
            data = response.json()

            if not data["items"]:
                break

            for item in data["items"]:
                yield item

            page += 1


async def process_stream():
    """Process items as they arrive."""
    async for item in fetch_pages("https://api.example.com/items"):
        print(f"Processing: {item['id']}")
        # Process each item without loading all in memory


# Async comprehension
async def get_names():
    names = [item["name"] async for item in fetch_pages(URL)]
    return names
```

### Background Tasks

```python
import asyncio
from collections.abc import Callable, Awaitable


class BackgroundTasks:
    """Manage background tasks."""

    def __init__(self):
        self.tasks: set[asyncio.Task] = set()

    def add_task(
        self,
        coro: Awaitable,
        *,
        name: str | None = None,
    ) -> asyncio.Task:
        """Add background task."""
        task = asyncio.create_task(coro, name=name)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task

    async def shutdown(self, timeout: float = 5.0):
        """Gracefully shutdown all tasks."""
        for task in self.tasks:
            task.cancel()

        if self.tasks:
            await asyncio.wait(self.tasks, timeout=timeout)


# Usage in FastAPI
background = BackgroundTasks()


@app.on_event("shutdown")
async def shutdown():
    await background.shutdown()


@app.post("/orders")
async def create_order(data: OrderCreate):
    order = await order_service.create(data)

    # Fire-and-forget background task
    background.add_task(
        send_order_confirmation(order.id),
        name=f"confirm-{order.id}",
    )

    return order
```

### Running Sync Code in Async

```python
import asyncio
from functools import partial


def cpu_intensive_task(data: bytes) -> bytes:
    """CPU-bound synchronous task."""
    # Heavy computation
    return processed_data


async def process_with_executor(data: bytes) -> bytes:
    """Run sync code without blocking event loop."""
    loop = asyncio.get_running_loop()

    # Run in thread pool (default executor)
    result = await loop.run_in_executor(None, cpu_intensive_task, data)

    return result


# With ProcessPoolExecutor for CPU-bound
from concurrent.futures import ProcessPoolExecutor

process_pool = ProcessPoolExecutor(max_workers=4)


async def cpu_bound_async(data: bytes) -> bytes:
    """Run CPU-bound in process pool."""
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(process_pool, cpu_intensive_task, data)
    return result
```

## Anti-patterns

### Avoid: Sync I/O in Async Code

```python
# BAD - blocks event loop
async def fetch_data():
    response = requests.get(URL)  # Sync HTTP!
    return response.json()

# GOOD - use async client
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        return response.json()
```

### Avoid: Not Awaiting Coroutines

```python
# BAD - coroutine never executes
async def main():
    fetch_data()  # Missing await!

# GOOD
async def main():
    await fetch_data()
```

### Avoid: Fire-and-Forget Without Tracking

```python
# BAD - task may be garbage collected
async def handle():
    asyncio.create_task(background_job())  # Lost reference

# GOOD - store task reference
tasks = set()

async def handle():
    task = asyncio.create_task(background_job())
    tasks.add(task)
    task.add_done_callback(tasks.discard)
```

## References

- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python - Async IO](https://realpython.com/async-io-python/)
- [httpx - Async HTTP](https://www.python-httpx.org/)
- [asyncpg - Async PostgreSQL](https://magicstack.github.io/asyncpg/)
