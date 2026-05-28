# FastAPI Best Practices Reference

Comprehensive guide for reviewing FastAPI projects. Each section includes the best practice, detection patterns, and refactor guidance.

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Async/Sync Patterns](#2-asyncsync-patterns)
3. [Pydantic Usage](#3-pydantic-usage)
4. [Dependency Injection](#4-dependency-injection)
5. [API Design](#5-api-design)
6. [Database Patterns](#6-database-patterns)
7. [Testing Patterns](#7-testing-patterns)
8. [Configuration Management](#8-configuration-management)
9. [Performance Optimizations](#9-performance-optimizations)
10. [Documentation](#10-documentation)

---

## 1. Project Structure

### Best Practice: Domain-Based Organization

Organize by domain/feature rather than file type for scalable projects.

**Recommended Structure:**

```
project/
├── alembic/
├── src/
│   ├── auth/
│   │   ├── router.py
│   │   ├── schemas.py      # Pydantic models
│   │   ├── models.py       # DB models
│   │   ├── dependencies.py
│   │   ├── service.py      # Business logic
│   │   ├── config.py       # Module config
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   ├── posts/
│   │   └── [same structure]
│   ├── config.py           # Global config
│   ├── models.py           # Global models
│   ├── exceptions.py       # Global exceptions
│   ├── database.py
│   └── main.py
├── tests/
│   ├── auth/
│   └── posts/
├── .env
└── alembic.ini
```

**Detection Patterns (Violations):**

- `crud/`, `routers/`, `models/` top-level directories (file-type organization)
- Single `models.py` with 500+ lines
- Single `router.py` handling multiple unrelated domains

**Refactor Action:**

1. Group related functionality by domain
2. Each domain gets: router, schemas, models, service, dependencies
3. Use explicit imports: `from src.auth import constants as auth_constants`

---

## 2. Async/Sync Patterns

### Best Practice: Correct Async Usage

FastAPI handles sync and async routes differently. Misuse blocks the event loop.

**Critical Rule:** Never use blocking I/O in async routes.

```python
# ❌ CRITICAL VIOLATION: Blocks event loop
@router.get("/bad")
async def bad_endpoint():
    time.sleep(10)  # Blocks entire server
    return {"status": "done"}

# ✅ CORRECT: Sync route runs in threadpool
@router.get("/good-sync")
def good_sync_endpoint():
    time.sleep(10)  # Runs in threadpool, doesn't block
    return {"status": "done"}

# ✅ CORRECT: Async route with async sleep
@router.get("/good-async")
async def good_async_endpoint():
    await asyncio.sleep(10)  # Non-blocking
    return {"status": "done"}
```

**Detection Patterns (Violations):**

- `time.sleep()` in `async def` routes
- `requests.get/post()` in `async def` routes (use `httpx.AsyncClient`)
- Sync database drivers (psycopg2) in async routes (use asyncpg)
- `open()` file operations in async routes (use `aiofiles`)

**Refactor Action:**

- Replace `time.sleep()` with `await asyncio.sleep()`
- Replace `requests` with `httpx.AsyncClient`
- Use async database drivers or `run_in_threadpool()`
- For sync SDKs: `await run_in_threadpool(sync_function, args)`

### Best Practice: Async Dependencies

Prefer async dependencies to avoid unnecessary thread usage.

```python
# ❌ Runs in thread unnecessarily
def get_client(request: Request) -> AsyncClient:
    return request.state.client

# ✅ Runs in event loop
async def get_client(request: Request) -> AsyncClient:
    return request.state.client
```

**Detection:** `def` (not `async def`) dependencies that don't perform blocking I/O.

---

## 3. Pydantic Usage

### Best Practice: Use Pydantic Extensively

Leverage Pydantic's built-in validators instead of manual validation.

```python
# ✅ Rich validation with Pydantic
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    email: EmailStr
    age: int = Field(ge=18)
```

**Detection Patterns (Violations):**

- Manual regex validation that Pydantic handles (`EmailStr`, `AnyUrl`)
- Missing `Field()` constraints (min_length, max_length, ge, le, pattern)
- Raw dicts instead of Pydantic models for request/response

### Best Practice: Custom Base Model

Create a global base model for consistent behavior.

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict

def datetime_to_gmt_str(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")

class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
    )
```

**Detection:** No custom base model; inconsistent datetime serialization.

### Best Practice: Decoupled BaseSettings

Split configuration into domain-specific settings classes.

```python
# ✅ Decoupled settings
# src/auth/config.py
class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5

auth_settings = AuthConfig()

# src/config.py
class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    ENVIRONMENT: str = "production"

settings = Config()
```

**Detection:** Single monolithic `Settings` class with 20+ fields.

---

## 4. Dependency Injection

### Best Practice: Validation via Dependencies

Use dependencies for database-backed validation, not just DI.

```python
# ✅ Validation dependency
async def valid_post_id(post_id: UUID4) -> dict:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()
    return post

@router.get("/posts/{post_id}")
async def get_post(post: dict = Depends(valid_post_id)):
    return post
```

**Detection:** Repeated validation logic in multiple endpoints instead of shared dependency.

### Best Practice: Chain Dependencies

Compose complex validations from simple dependencies.

```python
async def parse_jwt_data(token: str = Depends(oauth2_scheme)) -> dict:
    # ... validate token
    return {"user_id": payload["id"]}

async def valid_owned_post(
    post: dict = Depends(valid_post_id),
    token_data: dict = Depends(parse_jwt_data),
) -> dict:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()
    return post
```

**Detection:** Flat dependency structures; repeated auth + resource validation.

### Best Practice: Dependencies Are Cached

FastAPI caches dependency results per request. Design for reuse.

```python
# parse_jwt_data is called once even if used by multiple dependencies
async def valid_active_creator(token_data: dict = Depends(parse_jwt_data)): ...
async def valid_owned_post(token_data: dict = Depends(parse_jwt_data)): ...
```

---

## 5. API Design

### Best Practice: Follow REST Conventions

Use consistent path parameter names to enable dependency reuse.

```python
# ✅ Consistent naming enables dependency reuse
@router.get("/profiles/{profile_id}")
async def get_profile(profile: dict = Depends(valid_profile_id)): ...

@router.get("/creators/{profile_id}")  # Same param name!
async def get_creator(creator: dict = Depends(valid_creator_id)): ...
```

**Detection:** Inconsistent path parameter names for same resource type.

### Best Practice: Proper Response Documentation

Document responses for OpenAPI generation.

```python
@router.post(
    "/endpoints",
    response_model=DefaultResponse,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new resource",
    responses={
        status.HTTP_200_OK: {"model": OkResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
    },
)
async def create_endpoint(): ...
```

**Detection:** Missing `response_model`, `status_code`, or `responses` kwargs.

---

## 6. Database Patterns

### Best Practice: Naming Conventions

Set explicit naming conventions for database constraints.

```python
from sqlalchemy import MetaData

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
```

### Best Practice: SQL-First for Complex Queries

Use SQL for complex joins and aggregations; avoid N+1 queries.

```python
# ✅ SQL aggregation
select_query = (
    select(
        posts.c.id,
        func.json_build_object(
            text("'id', profiles.id"),
            text("'username', profiles.username"),
        ).label("creator"),
    )
    .select_from(posts.join(profiles, posts.c.owner_id == profiles.c.id))
    .where(posts.c.owner_id == creator_id)
)
```

**Detection Patterns (Violations):**

- `SELECT *` queries
- Multiple queries in loops (N+1)
- Python-side joins/aggregations that SQL handles better

### Best Practice: Descriptive Migrations

Use descriptive Alembic migration names.

```ini
# alembic.ini
file_template = %%(year)d-%%(month).2d-%%(day).2d_%%(slug)s
```

**Detection:** Generic migration names like `abc123_auto.py`.

---

## 7. Testing Patterns

### Best Practice: Async Test Client from Day 0

Use async test client to avoid event loop issues.

```python
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.anyio
async def test_create_post(client: AsyncClient):
    resp = await client.post("/posts", json={...})
    assert resp.status_code == 201
```

**Detection Patterns (Violations):**

- Using `TestClient` (sync) with async app
- `pytest.mark.asyncio` instead of `pytest.mark.anyio`
- Missing `anyio_backend` fixture

### Best Practice: Use pytest.mark.anyio

Prefer `anyio` marker (already installed via Starlette).

```python
@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
async def test_async_function(): ...
```

---

## 8. Configuration Management

### Best Practice: Environment-Based Doc Visibility

Hide docs in production.

```python
ENVIRONMENT = config("ENVIRONMENT")
SHOW_DOCS_ENVIRONMENT = ("local", "staging")

app_configs = {"title": "My API"}
if ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = None

app = FastAPI(**app_configs)
```

**Detection:** Docs exposed in production (`/docs`, `/redoc` accessible).

### Best Practice: Lifespan State over app.state

Use lifespan state for request-scoped resources.

```python
from typing import TypedDict

class State(TypedDict):
    client: AsyncClient

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    async with AsyncClient() as client:
        yield {"client": client}

@app.get("/")
async def read_root(request: Request):
    client = request.state.client  # Type-safe access
```

**Detection:** Using `app.state.x = y` pattern instead of lifespan state.

---

## 9. Performance Optimizations

### Best Practice: Install uvloop and httptools

Faster event loop and HTTP parser.

```bash
pip install uvloop httptools
```

**Detection:** Missing from requirements; `uvloop; sys_platform != 'win32'` for cross-platform.

### Best Practice: Thread Pool Awareness

Default thread pool is 40 threads. Increase if needed.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 100
    yield
```

**Detection:** High sync dependency usage without increased thread pool.

### Best Practice: Pure ASGI Middleware

Avoid `BaseHTTPMiddleware` for performance-critical paths.

```python
# ❌ Performance penalty
@app.middleware("http")
async def my_middleware(request, call_next): ...

# ✅ Pure ASGI middleware for critical paths
class PureMiddleware:
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        # ... pure ASGI implementation
        await self.app(scope, receive, send)
```

**Detection:** Multiple `BaseHTTPMiddleware` instances; use sparingly.

### Best Practice: Enable AsyncIO Debug Mode

Find blocking calls during development.

```bash
PYTHONASYNCIODEBUG=1 python main.py
```

---

## 10. Documentation

### Best Practice: Use Ruff

Modern, fast linter replacing black, isort, autoflake.

```bash
#!/bin/sh -e
ruff check --fix src
ruff format src
```

**Detection:** Using black + isort + flake8 separately; no linter configured.

### Best Practice: WebSocket async for

Use `async for` instead of `while True` for WebSockets.

```python
# ❌ Old pattern
while True:
    data = await websocket.receive_text()

# ✅ Modern pattern
async for data in websocket.iter_text():
    await websocket.send_text(f"Echo: {data}")
```

---

## Severity Classification

| Severity | Description | Examples |
|----------|-------------|----------|
| **Critical** | Blocks event loop, causes outages | `time.sleep()` in async, sync DB in async |
| **High** | Performance/security issues | N+1 queries, hardcoded secrets, no rate limiting |
| **Medium** | Maintainability concerns | Poor structure, missing types, no base model |
| **Low** | Polish and conventions | Missing docs, inconsistent naming, no ruff |
