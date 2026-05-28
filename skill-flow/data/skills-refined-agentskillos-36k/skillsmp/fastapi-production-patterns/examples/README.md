# FastAPI Production Examples

This directory contains production-ready examples demonstrating the patterns from the FastAPI Production Patterns skill.

## Structure

```
examples/
├── README.md                  # This file
├── 01-database-lifecycle/     # Database lifecycle management
├── 02-partial-updates/        # Pydantic partial updates (PATCH)
├── 03-async-conversion/       # Sync to async conversion
├── 04-dependency-injection/   # Dependency injection patterns
├── 05-async-testing/          # Async testing patterns
├── 06-file-uploads/           # File upload handling
├── 07-background-tasks/       # Background task patterns
└── 08-python-to-api/          # Converting Python utilities to APIs
```

## Quick Start

Each example is self-contained and can be run independently:

```bash
# Navigate to example directory
cd examples/02-partial-updates

# Install dependencies (from skill root)
cd ../.. && uv sync

# Run the example
uv run python 02-partial-updates/patch_endpoint_example.py
```

## Examples Overview

### 01. Database Lifecycle Management
Demonstrates proper database engine lifecycle with lifespan context manager, connection pooling, and shutdown handling.

**Key patterns:**
- Engine creation in lifespan (not at import)
- Connection pool configuration (`pool_size`, `max_overflow`, `pool_recycle`)
- Proper shutdown with `engine.dispose()`

### 02. Partial Updates (PATCH) ✅
Shows how to implement PATCH endpoints that only update provided fields using `exclude_unset=True`.

**Key patterns:**
- `Optional` fields in Pydantic models
- `model_dump(exclude_unset=True)`
- Preventing `None` overwrites

**Location:** `02-partial-updates/`
**Run:** `uv run python 02-partial-updates/patch_endpoint_example.py`

### 03. Async Conversion
Converts synchronous code to async, replacing blocking libraries with async equivalents.

**Key patterns:**
- `requests` → `httpx.AsyncClient`
- Sync SQLAlchemy → Async SQLAlchemy
- Proper async/await usage

### 04. Dependency Injection
Demonstrates FastAPI's dependency injection for shared resources, caching, and testing.

**Key patterns:**
- Basic dependencies with `Depends()`
- Cached dependencies with `lru_cache`
- Dependency overrides for testing

### 05. Async Testing
Shows how to properly test async endpoints using `httpx.AsyncClient` and async fixtures.

**Key patterns:**
- `AsyncClient` instead of `TestClient`
- Async fixtures with proper cleanup
- Database isolation between tests

### 06. File Uploads
Demonstrates streaming file uploads without loading entire files into memory.

**Key patterns:**
- Streaming file processing
- File validation (type, size)
- Async file I/O with `aiofiles`

### 07. Background Tasks
Shows handling of long-running operations using FastAPI `BackgroundTasks` and Celery.

**Key patterns:**
- Fire-and-forget tasks
- Task status tracking
- Celery integration for production

### 08. Python to API Conversion
Demonstrates converting existing Python utilities to FastAPI endpoints.

**Key patterns:**
- Adding Pydantic validation
- Making functions async
- Replacing exceptions with `HTTPException`

## Testing Examples

```bash
# Test partial updates example
cd examples/02-partial-updates
uv run python test_patch_endpoint.py

# Run with pytest (when available)
uv run pytest
```

## Common Requirements

All examples share common requirements:

```bash
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
pydantic>=2.0.0
httpx>=0.25.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

## See Also

- [SKILL.md](../SKILL.md) - Main skill documentation
- [capabilities/](../capabilities/) - Detailed capability documentation
- [resources/](../resources/) - Additional resources and reference materials
