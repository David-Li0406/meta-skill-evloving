---
name: fastapi-development
description: Enforces best practices for FastAPI development, ensuring scalable, high-performance, and maintainable APIs. Use when working on server-side Python code involving FastAPI.
---

# FastAPI Development Standards

## Key Principles
- **Concise & Technical**: Write accurate, functional code.
- **Functional Style**: Prefer pure functions over classes for routes and logic.
- **RORO Pattern**: "Receive an Object, Return an Object". Use Pydantic models for all inputs and outputs.

## Architecture & Structure
- **File Naming**: Lowercase with underscores (e.g., `routers/user_routes.py`).
- **Exports**: Favor named exports.
- **Organization**: Separate exported routers, sub-routes, utilities, static content, and types (models/schemas).

## Coding Standards
- **Type Hints**: Mandatory for all function signatures.
- **Validation**: Use Pydantic models (v2) instead of raw dictionaries.
- **Conditionals**: Avoid unnecessary curly braces. Use one-line syntax for simple conditionals.
- **Async/Sync**:
  - Use `async def` for I/O-bound operations (DB, external APIs).
  - Use `def` for CPU-bound synchronous tasks.

## Error Handling
- **Early Returns**: Handle errors/edge cases first. Happy path goes last.
- **Guard Clauses**: Validate preconditions early.
- **HTTPExceptions**: Use `HTTPException` for expected errors.
- **No Nested Ifs**: Avoid deep nesting.

## Performance
- **Non-blocking**: Minimize blocking I/O. Use async libraries (asyncpg, aiomysql).
- **Caching**: Implement strategies for frequent data.
- **Lazy Loading**: Use for large datasets.

## Dependencies
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 (if ORM used)
