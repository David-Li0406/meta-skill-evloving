---
name: async-python-patterns
description: Use this skill when building asynchronous Python applications with asyncio, implementing concurrent I/O operations, or creating high-performance non-blocking systems.
---

# Async Python Patterns

Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.

## When to Use This Skill

- Building async web APIs (FastAPI, aiohttp, Sanic)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication
- Optimizing I/O-bound workloads
- Implementing async background tasks and queues

## Core Concepts

### 1. Event Loop

The event loop is the heart of asyncio, managing and scheduling asynchronous tasks.

**Key characteristics:**

- Single-threaded cooperative multitasking
- Schedules coroutines for execution
- Handles I/O operations without blocking
- Manages callbacks and futures

### 2. Coroutines

Functions defined with `async def` that can be paused and resumed.

**Syntax:**

```python
async def my_coroutine():
    result = await some_async_operation()
    return result
```

### 3. Tasks

Scheduled coroutines that run concurrently on the event loop.

### 4. Futures

Low-level objects representing eventual results of async operations.

### 5. Async Context Managers

Resources that support `async with` for proper cleanup.

### 6. Async Iterators

Objects that support `async for` for iterating over async data sources.

## Quick Start

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Python 3.7+
asyncio.run(main())
```

## Fundamental Patterns

### Pattern 1: Basic Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data from URL asynchronously."""
    await asyncio.sleep(1)  # Simulate I/O
    return {"url": url, "data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

### Pattern 2: Concurrent Execution with gather()

```python
import asyncio

async def fetch_user(user_id: int) -> dict:
    """Fetch user data."""
    await asyncio.sleep(1)  # Simulate I/O
    return {"user_id": user_id, "data": "user_data"}

async def main():
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )
    print(users)

asyncio.run(main())
```

### Pattern 3: Using aiohttp for HTTP Requests

```python
import aiohttp
import asyncio

async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()

async def main():
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