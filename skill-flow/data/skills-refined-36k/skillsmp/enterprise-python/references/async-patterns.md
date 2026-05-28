# Async and Concurrency Patterns

Advanced patterns for asyncio, threading, and multiprocessing in Python.

## Table of Contents
- [Asyncio Fundamentals](#asyncio-fundamentals)
- [Concurrency Patterns](#concurrency-patterns)
- [Error Handling in Async](#error-handling-in-async)
- [Resource Management](#resource-management)
- [Performance Optimization](#performance-optimization)

## Asyncio Fundamentals

### Proper Async Function Structure
```python
import asyncio
from typing import TypeVar
from collections.abc import Awaitable, Callable

T = TypeVar("T")

async def with_timeout(
    coro: Awaitable[T],
    timeout: float,
    default: T | None = None
) -> T | None:
    """Execute coroutine with timeout, returning default on timeout."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return default
```

### Async Context Managers
```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def managed_connection(url: str) -> AsyncGenerator[Connection, None]:
    conn = await Connection.create(url)
    try:
        yield conn
    finally:
        await conn.close()

# Usage
async with managed_connection("postgres://...") as conn:
    await conn.execute(query)
```

## Concurrency Patterns

### Gather with Error Handling
```python
async def fetch_all_safe(urls: list[str]) -> list[Response | Exception]:
    """Fetch all URLs, returning results or exceptions."""
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

async def fetch_all_strict(urls: list[str]) -> list[Response]:
    """Fetch all URLs, failing fast on first error."""
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_url(url)) for url in urls]
    return [task.result() for task in tasks]
```

### Semaphore for Rate Limiting
```python
class RateLimitedClient:
    def __init__(self, max_concurrent: int = 10) -> None:
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._client = httpx.AsyncClient()

    async def fetch(self, url: str) -> Response:
        async with self._semaphore:
            return await self._client.get(url)

    async def fetch_many(self, urls: list[str]) -> list[Response]:
        return await asyncio.gather(*[self.fetch(url) for url in urls])
```

### Producer-Consumer Pattern
```python
async def producer(queue: asyncio.Queue[str], items: list[str]) -> None:
    for item in items:
        await queue.put(item)
    await queue.put(None)  # Sentinel to signal completion

async def consumer(queue: asyncio.Queue[str | None], worker_id: int) -> None:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        await process_item(item)
        queue.task_done()

async def run_pipeline(items: list[str], num_workers: int = 5) -> None:
    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=100)
    
    producer_task = asyncio.create_task(producer(queue, items))
    consumer_tasks = [
        asyncio.create_task(consumer(queue, i))
        for i in range(num_workers)
    ]
    
    await producer_task
    await queue.join()
    for _ in range(num_workers):
        await queue.put(None)
    await asyncio.gather(*consumer_tasks)
```

## Error Handling in Async

### Structured Error Handling
```python
class AsyncOperationError(Exception):
    """Base exception for async operations."""
    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause

async def resilient_fetch(
    url: str,
    retries: int = 3,
    backoff: float = 1.0
) -> Response:
    """Fetch with exponential backoff retry."""
    last_error: Exception | None = None
    
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return response
        except httpx.HTTPError as e:
            last_error = e
            if attempt < retries - 1:
                await asyncio.sleep(backoff * (2 ** attempt))
    
    raise AsyncOperationError(f"Failed after {retries} attempts", last_error)
```

## Resource Management

### Connection Pooling
```python
from contextlib import asynccontextmanager

class ConnectionPool:
    def __init__(self, dsn: str, min_size: int = 5, max_size: int = 20) -> None:
        self._dsn = dsn
        self._min_size = min_size
        self._max_size = max_size
        self._pool: asyncpg.Pool | None = None

    async def initialize(self) -> None:
        self._pool = await asyncpg.create_pool(
            self._dsn,
            min_size=self._min_size,
            max_size=self._max_size
        )

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[Connection, None]:
        if not self._pool:
            raise RuntimeError("Pool not initialized")
        async with self._pool.acquire() as conn:
            yield conn
```

## Performance Optimization

### Batching Requests
```python
async def process_batch(
    items: list[str],
    batch_size: int = 100,
    max_concurrent: int = 5
) -> list[Result]:
    semaphore = asyncio.Semaphore(max_concurrent)
    results: list[Result] = []
    
    async def process_one_batch(batch: list[str]) -> list[Result]:
        async with semaphore:
            return await api_call(batch)
    
    batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
    batch_results = await asyncio.gather(*[process_one_batch(b) for b in batches])
    
    for batch_result in batch_results:
        results.extend(batch_result)
    
    return results
```

### CPU-Bound Work with ProcessPoolExecutor
```python
from concurrent.futures import ProcessPoolExecutor
import asyncio

def cpu_intensive_task(data: bytes) -> bytes:
    """CPU-bound work that should run in a process."""
    return heavy_computation(data)

async def process_with_pool(
    items: list[bytes],
    max_workers: int = 4
) -> list[bytes]:
    loop = asyncio.get_running_loop()
    
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futures = [
            loop.run_in_executor(pool, cpu_intensive_task, item)
            for item in items
        ]
        return await asyncio.gather(*futures)
```
