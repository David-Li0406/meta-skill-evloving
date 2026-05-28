---
name: python-async-concurrency
description: Modern Python asyncio, aiohttp, and concurrency patterns.
---

# Python Async & Concurrency

## When to use this skill
- Writing high-concurrency I/O bound applications (FastAPI, bots, scrapers).
- Using `asyncio`, `aiohttp`, or `httpx`.
- Managing background tasks or task queues.

## 1. Asyncio Basics
- **Entry Point**: Use `asyncio.run(main())` for the entry point.
- **TaskGroups**: Use `async with asyncio.TaskGroup() as tg` (Python 3.11+) instead of `gather()` for better error handling/cancellation.
- **Blocking Code**: Run blocking (CPU-bound) code in `await asyncio.to_thread(...)`.

## 2. HTTP Clients
- **HTPX/AIOHTTP**: Use `httpx.AsyncClient` or `aiohttp.ClientSession` as a context manager.
- **Singleton**: Reuse the client session across requests; do not create a new one per request.

## 3. Pitfalls
- **Sync in Async**: Never call blocking sync functions (requests, time.sleep) inside async functions.
- **Fire and Forget**: Avoid unreferenced background tasks; keep a reference to prevent garbage collection (or use `TaskGroup`).
