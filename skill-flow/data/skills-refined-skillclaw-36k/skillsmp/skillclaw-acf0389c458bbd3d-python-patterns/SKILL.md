---
name: python-patterns
description: Use this skill when you need to make informed decisions about Python development, including framework selection, async patterns, and project structure.
---

# Python Patterns

> Python development principles and decision-making for 2025.
> **Learn to THINK, not memorize patterns.**

## ⚠️ How to Use This Skill

This skill teaches **decision-making principles**, not fixed code to copy.

- ASK user for framework preference when unclear.
- Choose async vs sync based on CONTEXT.
- Don't default to the same framework every time.

## 1. Framework Selection (2025)

### Decision Tree

```
What are you building?
│
├── API-first / Microservices
│   └── FastAPI (async, modern, fast)
│
├── Full-stack web / CMS / Admin
│   └── Django (batteries-included)
│
├── Simple / Script / Learning
│   └── Flask (minimal, flexible)
│
├── AI/ML API serving
│   └── FastAPI (Pydantic, async, uvicorn)
│
└── Background workers
    └── Celery + any framework
```

### Comparison Principles

| Factor             | FastAPI             | Django          | Flask            |
| ------------------ | ------------------- | --------------- | ---------------- |
| **Best for**       | APIs, microservices | Full-stack, CMS | Simple, learning |
| **Async**          | Native              | Django 5.0+     | Via extensions   |
| **Admin**          | Manual              | Built-in        | Via extensions   |
| **ORM**            | Choose your own     | Django ORM      | Choose your own  |
| **Learning curve** | Low                 | Medium          | Low              |

### Selection Questions to Ask:

1. Is this API-only or full-stack?
2. Need admin interface?
3. Team familiar with async?
4. Existing infrastructure?

## 2. Async vs Sync Decision

### When to Use Async

```
async def is better when:
├── I/O-bound operations (database, HTTP, file)
├── Many concurrent connections
├── Real-time features
├── Microservices communication
└── FastAPI/Starlette/Django ASGI

def (sync) is better when:
├── CPU-bound operations
├── Simple scripts
├── Legacy codebase
├── Team unfamiliar with async
└── Blocking libraries (no async version)
```

### The Golden Rule

```
I/O-bound → async (waiting for external)
CPU-bound → sync + multiprocessing (computing)

Don't:
├── Mix sync and async carelessly
├── Use sync libraries in async code
└── Force async for CPU work
```

### Async Library Selection

| Need         | Async Library         |
|--------------|-----------------------|
| HTTP client  | httpx                 |
| PostgreSQL   | asyncpg               |
| Redis        | aioredis / redis-py async |
| File I/O     | aiofiles              |
| Database ORM | SQLAlchemy 2.0 async, Tortoise |

## 3. Type Hints Strategy

### When to Use Type Hints

- Use type hints to improve code readability and maintainability.
- Helps with static type checking and IDE support.

### Example

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```