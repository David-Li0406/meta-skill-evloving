---
name: best-practices
description: Python FastAPI performance optimization and best practices guidelines
license: MIT
metadata:
  author: devnogari
  project_type: python-fastapi
  rule_count: 48
  categories: 8
---

# Python FastAPI Best Practices

Comprehensive performance optimization and best practices for FastAPI applications. **48 rules across 8 categories** based on FastAPI official documentation (benchmark score 96.8), Pydantic V2, and SQLAlchemy async patterns.

## Activation Triggers

This skill activates when:
- Writing new endpoints, routers, or dependencies
- Implementing async patterns and database operations
- Optimizing API performance
- Reviewing or refactoring FastAPI code
- Debugging async, validation, or database issues
- Implementing authentication/authorization
- Writing tests for FastAPI applications

## Rule Categories

| # | Category | Priority | Prefix | Rule Count | Focus |
|---|----------|----------|--------|------------|-------|
| 1 | Async Patterns | CRITICAL | `async-` | 6 | Event loop, blocking I/O |
| 2 | Dependency Injection | CRITICAL | `di-` | 6 | Dependencies, lifecycle, scopes |
| 3 | Pydantic Models | HIGH | `pydantic-` | 6 | Validation, serialization |
| 4 | Database Patterns | HIGH | `db-` | 6 | SQLAlchemy async, sessions |
| 5 | Error Handling | MEDIUM | `err-` | 6 | HTTPException, handlers |
| 6 | Security | MEDIUM | `sec-` | 6 | Auth, CORS, rate limiting |
| 7 | Performance | MEDIUM | `perf-` | 6 | Response, caching, background |
| 8 | Testing | LOW | `test-` | 6 | pytest-asyncio, fixtures |

## Quick Reference - All 48 Rules

### Async Patterns (CRITICAL) - `async-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `async-block` | Never block the event loop | Prevents server freeze |
| `async-gather` | Use asyncio.gather for parallel I/O | 2-10x speedup |
| `async-timeout` | Always set async operation timeouts | Prevents hung requests |
| `async-context` | Use async context managers | Proper resource cleanup |
| `async-driver` | Use async database/HTTP drivers | Full async stack |
| `async-executor` | Run blocking code in thread pool | CPU-bound isolation |

### Dependency Injection (CRITICAL) - `di-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `di-depends` | Use Depends() for shared logic | Code reuse, testability |
| `di-yield` | Use yield for cleanup | Proper resource lifecycle |
| `di-cache` | Cache expensive dependencies | Reduce redundant computation |
| `di-scope` | Understand dependency scopes | Request vs app lifetime |
| `di-override` | Use dependency_overrides for testing | Clean test isolation |
| `di-annotated` | Use Annotated for cleaner signatures | Type-safe DI |

### Pydantic Models (HIGH) - `pydantic-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `pydantic-field` | Use Field() with constraints | Automatic validation |
| `pydantic-validator` | Use @field_validator for custom logic | Complex validation |
| `pydantic-config` | Configure model behavior | Performance tuning |
| `pydantic-orm` | Use from_attributes for ORM | Clean serialization |
| `pydantic-generic` | Use Generic models for reuse | DRY response models |
| `pydantic-alias` | Use alias for API compatibility | Clean external APIs |

### Database Patterns (HIGH) - `db-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `db-async` | Use async SQLAlchemy engine | Non-blocking DB |
| `db-session` | Use async session context manager | Connection safety |
| `db-n-plus-one` | Avoid N+1 with eager loading | Query optimization |
| `db-transaction` | Use explicit transactions | Data consistency |
| `db-migration` | Use Alembic async migrations | Schema management |
| `db-pool` | Configure connection pool properly | Resource efficiency |

### Error Handling (MEDIUM) - `err-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `err-http` | Use HTTPException with status codes | Proper HTTP semantics |
| `err-handler` | Register global exception handlers | Centralized errors |
| `err-validation` | Handle RequestValidationError | User-friendly messages |
| `err-middleware` | Use middleware for cross-cutting | Consistent error format |
| `err-logging` | Log errors with context | Debugging support |
| `err-retry` | Implement retry with backoff | Resilience |

### Security (MEDIUM) - `sec-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `sec-oauth2` | Use OAuth2PasswordBearer | Standard auth flow |
| `sec-jwt` | Implement JWT properly | Stateless auth |
| `sec-cors` | Configure CORS correctly | Cross-origin security |
| `sec-rate-limit` | Implement rate limiting | DoS protection |
| `sec-input` | Validate and sanitize input | Injection prevention |
| `sec-headers` | Set security headers | Browser protection |

### Performance (MEDIUM) - `perf-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `perf-response` | Use response_model for filtering | Reduce payload size |
| `perf-cache` | Implement caching strategies | Reduce DB load |
| `perf-background` | Use BackgroundTasks for async work | Faster responses |
| `perf-streaming` | Use StreamingResponse for large data | Memory efficiency |
| `perf-compression` | Enable response compression | Network efficiency |
| `perf-middleware` | Order middleware by frequency | Reduce overhead |

### Testing (LOW) - `test-*`

| Rule ID | Rule Name | Impact |
|---------|-----------|--------|
| `test-client` | Use TestClient or httpx.AsyncClient | Proper API testing |
| `test-override` | Use dependency_overrides | Clean mocking |
| `test-async` | Use pytest-asyncio properly | Async test support |
| `test-fixture` | Create reusable fixtures | Test organization |
| `test-mock` | Mock external services | Test isolation |
| `test-coverage` | Maintain test coverage | Quality assurance |

---

## Detailed Rules by Category

### 1. Async Patterns (CRITICAL)

#### `async-block` - Never Block the Event Loop

**Impact**: Server freeze, request timeouts, degraded throughput

```python
# ❌ INCORRECT - blocking I/O in async function
import time
import requests

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    time.sleep(1)  # BLOCKS entire server!
    response = requests.get(f"http://api/users/{user_id}")  # BLOCKS!
    return response.json()

# ✅ CORRECT - use async alternatives
import asyncio
import httpx

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    await asyncio.sleep(1)  # non-blocking
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api/users/{user_id}")
    return response.json()
```

#### `async-gather` - Use asyncio.gather for Parallel I/O

**Impact**: 2-10x speedup for independent operations

```python
# ❌ INCORRECT - sequential fetches (3 round trips)
@app.get("/dashboard")
async def get_dashboard(user_id: int):
    user = await get_user(user_id)         # 100ms
    orders = await get_orders(user_id)     # 100ms
    notifications = await get_notifications(user_id)  # 100ms
    return {"user": user, "orders": orders, "notifications": notifications}
    # Total: ~300ms

# ✅ CORRECT - parallel fetches (1 round trip)
@app.get("/dashboard")
async def get_dashboard(user_id: int):
    user, orders, notifications = await asyncio.gather(
        get_user(user_id),
        get_orders(user_id),
        get_notifications(user_id)
    )
    return {"user": user, "orders": orders, "notifications": notifications}
    # Total: ~100ms (max of all)
```

#### `async-timeout` - Always Set Async Operation Timeouts

**Impact**: Prevents hung requests and resource exhaustion

```python
# ❌ INCORRECT - no timeout
@app.get("/external-api")
async def call_external():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://slow-api.com/data")
    return response.json()

# ✅ CORRECT - explicit timeouts
from asyncio import timeout

@app.get("/external-api")
async def call_external():
    async with httpx.AsyncClient(timeout=10.0) as client:
        async with timeout(15.0):  # overall timeout
            response = await client.get("http://slow-api.com/data")
    return response.json()
```

#### `async-context` - Use Async Context Managers

**Impact**: Proper resource cleanup, connection management

```python
# ❌ INCORRECT - manual resource management
@app.get("/data")
async def get_data():
    client = httpx.AsyncClient()
    response = await client.get("http://api/data")
    # client never closed!
    return response.json()

# ✅ CORRECT - async context manager
@app.get("/data")
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://api/data")
        return response.json()
    # client properly closed
```

#### `async-driver` - Use Async Database/HTTP Drivers

**Impact**: Full async stack, maximum concurrency

```python
# ❌ INCORRECT - sync database driver blocks event loop
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")

# ✅ CORRECT - async database driver
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

# ❌ INCORRECT - sync HTTP client
import requests
response = requests.get(url)

# ✅ CORRECT - async HTTP client
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

#### `async-executor` - Run Blocking Code in Thread Pool

**Impact**: Isolates CPU-bound work from async event loop

```python
# ❌ INCORRECT - CPU-bound work blocks event loop
import hashlib

@app.post("/hash")
async def compute_hash(data: bytes):
    result = hashlib.pbkdf2_hmac('sha256', data, b'salt', 100000)
    return {"hash": result.hex()}

# ✅ CORRECT - run in thread pool executor
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def blocking_hash(data: bytes) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', data, b'salt', 100000)

@app.post("/hash")
async def compute_hash(data: bytes):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, blocking_hash, data)
    return {"hash": result.hex()}
```

---

### 2. Dependency Injection (CRITICAL)

#### `di-depends` - Use Depends() for Shared Logic

**Impact**: Code reuse, testability, separation of concerns

```python
# ❌ INCORRECT - repeated code
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10, db: AsyncSession = ...):
    # pagination logic repeated everywhere
    pass

@app.get("/users/")
async def get_users(skip: int = 0, limit: int = 10, db: AsyncSession = ...):
    # same pagination logic again
    pass

# ✅ CORRECT - extracted dependency
from fastapi import Depends, Query

async def pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> dict:
    return {"skip": skip, "limit": limit}

@app.get("/items/")
async def get_items(pagination: dict = Depends(pagination)):
    pass

@app.get("/users/")
async def get_users(pagination: dict = Depends(pagination)):
    pass
```

#### `di-yield` - Use yield for Cleanup

**Impact**: Proper resource lifecycle, no leaks

```python
# ❌ INCORRECT - no cleanup
async def get_db():
    db = SessionLocal()
    return db  # never closed!

# ✅ CORRECT - yield for cleanup
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@app.get("/items/")
async def get_items(db: AsyncSession = Depends(get_db)):
    # session automatically cleaned up after request
    pass
```

#### `di-cache` - Cache Expensive Dependencies

**Impact**: Reduce redundant computation, faster startup

```python
# ❌ INCORRECT - expensive operation every request
async def get_settings():
    return Settings()  # parsed from env every time

# ✅ CORRECT - cached dependency (use_cache=True is default)
from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    return Settings()  # parsed once, cached

# For async dependencies that should be called once per request
# but cached within that request (FastAPI default behavior)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # called only once per request even if used in multiple places
    return await decode_token(token)
```

#### `di-scope` - Understand Dependency Scopes

**Impact**: Correct resource management per lifetime

```python
# App-scoped (singleton): created once at startup
@lru_cache()
def get_redis_pool() -> redis.ConnectionPool:
    return redis.ConnectionPool(host='localhost', port=6379)

# Request-scoped: created per request (default for async generators)
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# No scope (fresh every call): for dependencies with side effects
def get_request_id() -> str:
    return str(uuid.uuid4())
```

#### `di-override` - Use dependency_overrides for Testing

**Impact**: Clean test isolation without modifying code

```python
# Production dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Test override
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as session:
        yield session
        await session.rollback()  # rollback for test isolation

# In tests
def test_get_items():
    app.dependency_overrides[get_db] = override_get_db
    try:
        client = TestClient(app)
        response = client.get("/items/")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()
```

#### `di-annotated` - Use Annotated for Cleaner Signatures

**Impact**: Type-safe DI, cleaner function signatures

```python
# ❌ INCORRECT - verbose signatures
@app.get("/items/")
async def get_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(pagination)
):
    pass

# ✅ CORRECT - Annotated for reusable dependencies
from typing import Annotated

DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Pagination = Annotated[dict, Depends(pagination)]

@app.get("/items/")
async def get_items(
    db: DBSession,
    current_user: CurrentUser,
    pagination: Pagination
):
    pass
```

---

### 3. Pydantic Models (HIGH)

#### `pydantic-field` - Use Field() with Constraints

**Impact**: Automatic validation, clear API contracts

```python
# ❌ INCORRECT - no validation
class UserCreate(BaseModel):
    email: str
    age: int
    name: str

# ✅ CORRECT - with validation constraints
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=150, description="User age in years")
    name: str = Field(min_length=1, max_length=100, pattern=r'^[a-zA-Z\s]+$')
    password: str = Field(min_length=8, max_length=100)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "age": 25,
                "name": "John Doe",
                "password": "securepass123"
            }
        }
    )
```

#### `pydantic-validator` - Use @field_validator for Custom Logic

**Impact**: Complex validation, business rules enforcement

```python
from pydantic import BaseModel, field_validator, model_validator

class OrderCreate(BaseModel):
    quantity: int
    price: float
    discount: float = 0.0

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('quantity must be positive')
        return v

    @field_validator('discount')
    @classmethod
    def discount_in_range(cls, v: float) -> float:
        if not 0 <= v <= 1:
            raise ValueError('discount must be between 0 and 1')
        return v

    @model_validator(mode='after')
    def validate_total(self) -> 'OrderCreate':
        total = self.quantity * self.price * (1 - self.discount)
        if total < 0:
            raise ValueError('total cannot be negative')
        return self
```

#### `pydantic-config` - Configure Model Behavior

**Impact**: Performance tuning, serialization control

```python
from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    model_config = ConfigDict(
        # ORM mode for SQLAlchemy models
        from_attributes=True,
        # Strip whitespace from strings
        str_strip_whitespace=True,
        # Use enum values instead of names
        use_enum_values=True,
        # Validate on assignment (not just creation)
        validate_assignment=True,
        # Forbid extra fields
        extra='forbid',
        # Populate by field name, not alias
        populate_by_name=True,
        # Serialize datetime as ISO format
        json_encoders={datetime: lambda v: v.isoformat()}
    )
```

#### `pydantic-orm` - Use from_attributes for ORM

**Impact**: Clean serialization from SQLAlchemy models

```python
# ❌ INCORRECT - manual conversion
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: DBSession):
    user = await db.get(User, user_id)
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name
    }

# ✅ CORRECT - automatic ORM conversion
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    posts: list['PostResponse'] = []

    model_config = ConfigDict(from_attributes=True)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DBSession):
    user = await db.get(User, user_id)
    return user  # automatic conversion via from_attributes
```

#### `pydantic-generic` - Use Generic Models for Reuse

**Impact**: DRY response models, consistent API format

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: list[T], total: int, page: int, size: int):
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    error: str | None = None

# Usage
@app.get("/users/", response_model=PaginatedResponse[UserResponse])
async def list_users(pagination: Pagination, db: DBSession):
    users, total = await get_users_paginated(db, pagination)
    return PaginatedResponse.create(users, total, pagination['skip'], pagination['limit'])
```

#### `pydantic-alias` - Use Alias for API Compatibility

**Impact**: Clean external APIs, internal naming freedom

```python
from pydantic import BaseModel, Field

# External API uses camelCase, internal uses snake_case
class UserCreate(BaseModel):
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    email_address: str = Field(alias='emailAddress')

    model_config = ConfigDict(
        populate_by_name=True,  # accept both alias and field name
        json_schema_extra={
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "emailAddress": "john@example.com"
            }
        }
    )

class UserResponse(BaseModel):
    first_name: str = Field(serialization_alias='firstName')
    last_name: str = Field(serialization_alias='lastName')

    model_config = ConfigDict(
        from_attributes=True,
        by_alias=True  # serialize using alias
    )
```

---

### 4. Database Patterns (HIGH)

#### `db-async` - Use Async SQLAlchemy Engine

**Impact**: Non-blocking database operations

```python
# ❌ INCORRECT - sync engine blocks event loop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:pass@localhost/db")
SessionLocal = sessionmaker(bind=engine)

# ✅ CORRECT - async engine with asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

#### `db-session` - Use Async Session Context Manager

**Impact**: Connection safety, automatic cleanup

```python
# ❌ INCORRECT - manual session management
async def get_users():
    session = async_session()
    users = await session.execute(select(User))
    # session never closed, connection leak!
    return users.scalars().all()

# ✅ CORRECT - async context manager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/users/")
async def get_users(db: DBSession):
    result = await db.execute(select(User))
    return result.scalars().all()
```

#### `db-n-plus-one` - Avoid N+1 with Eager Loading

**Impact**: Query optimization, reduced database round trips

```python
# ❌ INCORRECT - N+1 query problem
@app.get("/users/")
async def get_users_with_posts(db: DBSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    for user in users:
        # This triggers N additional queries!
        posts = user.posts  # lazy load for each user
    return users

# ✅ CORRECT - eager loading with selectinload
from sqlalchemy.orm import selectinload, joinedload

@app.get("/users/")
async def get_users_with_posts(db: DBSession):
    # selectinload: separate IN query (good for large collections)
    stmt = select(User).options(selectinload(User.posts))

    # joinedload: single JOIN query (good for small collections)
    # stmt = select(User).options(joinedload(User.posts))

    result = await db.execute(stmt)
    return result.scalars().unique().all()

# For nested relationships
stmt = select(User).options(
    selectinload(User.posts).selectinload(Post.comments)
)
```

#### `db-transaction` - Use Explicit Transactions

**Impact**: Data consistency, atomicity

```python
# ❌ INCORRECT - implicit transaction, partial failure possible
@app.post("/transfer/")
async def transfer_money(from_id: int, to_id: int, amount: float, db: DBSession):
    from_account = await db.get(Account, from_id)
    from_account.balance -= amount
    await db.commit()  # committed

    to_account = await db.get(Account, to_id)
    to_account.balance += amount  # if this fails, money is lost!
    await db.commit()

# ✅ CORRECT - explicit transaction
@app.post("/transfer/")
async def transfer_money(from_id: int, to_id: int, amount: float, db: DBSession):
    async with db.begin():  # explicit transaction
        from_account = await db.get(Account, from_id)
        to_account = await db.get(Account, to_id)

        if from_account.balance < amount:
            raise HTTPException(400, "Insufficient funds")

        from_account.balance -= amount
        to_account.balance += amount
        # both changes committed together or both rolled back
```

#### `db-migration` - Use Alembic Async Migrations

**Impact**: Schema management, version control

```python
# alembic/env.py - async migration configuration
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

def run_migrations_online():
    connectable = create_async_engine(settings.database_url)

    def do_run_migrations_sync(connection):
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,
            compare_server_default=True
        )
        with context.begin_transaction():
            context.run_migrations()

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations_sync)
        await connectable.dispose()

    asyncio.run(run_async_migrations())
```

#### `db-pool` - Configure Connection Pool Properly

**Impact**: Resource efficiency, connection management

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    poolclass=AsyncAdaptedQueuePool,
    pool_size=5,           # base pool size
    max_overflow=10,       # additional connections allowed
    pool_timeout=30,       # wait timeout for connection
    pool_recycle=1800,     # recycle connections after 30 min
    pool_pre_ping=True,    # test connections before use
    echo=False,            # disable SQL logging in production
    echo_pool="debug",     # pool event logging for debugging
)

# Graceful shutdown
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
```

---

### 5. Error Handling (MEDIUM)

#### `err-http` - Use HTTPException with Status Codes

**Impact**: Proper HTTP semantics, clear error messages

```python
# ❌ INCORRECT - generic exception
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await get_item_from_db(item_id)
    if not item:
        raise Exception("Not found")  # returns 500

# ✅ CORRECT - HTTPException with proper status
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await get_item_from_db(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
            headers={"X-Error": "Item not found"}
        )
    return item
```

#### `err-handler` - Register Global Exception Handlers

**Impact**: Centralized error handling, consistent format

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )
```

#### `err-validation` - Handle RequestValidationError

**Impact**: User-friendly validation messages

```python
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors
            }
        }
    )
```

#### `err-middleware` - Use Middleware for Cross-Cutting

**Impact**: Consistent error format across all endpoints

```python
from starlette.middleware.base import BaseHTTPMiddleware
import traceback

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Request failed: {traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": str(exc) if settings.DEBUG else "Internal server error",
                        "request_id": request.state.request_id
                    }
                }
            )

app.add_middleware(ErrorHandlingMiddleware)
```

#### `err-logging` - Log Errors with Context

**Impact**: Debugging support, error tracking

```python
import logging
import structlog
from uuid import uuid4

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
)

logger = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id

    with structlog.contextvars.bound_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path
    ):
        try:
            response = await call_next(request)
            logger.info("request_completed", status_code=response.status_code)
            return response
        except Exception as exc:
            logger.exception("request_failed", error=str(exc))
            raise
```

#### `err-retry` - Implement Retry with Backoff

**Impact**: Resilience for transient failures

```python
import asyncio
from functools import wraps
from typing import Type

def retry_async(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,)
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor ** attempt
                        logger.warning(
                            f"Retry {attempt + 1}/{max_retries} after {wait_time}s",
                            error=str(exc)
                        )
                        await asyncio.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator

@retry_async(max_retries=3, exceptions=(httpx.RequestError,))
async def call_external_api(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

---

### 6. Security (MEDIUM)

#### `sec-oauth2` - Use OAuth2PasswordBearer

**Impact**: Standard auth flow, OpenAPI integration

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user
```

#### `sec-jwt` - Implement JWT Properly

**Impact**: Stateless authentication, secure token handling

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = settings.SECRET_KEY  # from environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

#### `sec-cors` - Configure CORS Correctly

**Impact**: Cross-origin security, frontend integration

```python
from fastapi.middleware.cors import CORSMiddleware

# ❌ INCORRECT - overly permissive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows any origin!
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CORRECT - restrictive CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myapp.com",
        "https://staging.myapp.com",
        "http://localhost:3000" if settings.DEBUG else None
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Total-Count", "X-Page-Count"],
    max_age=600,  # cache preflight for 10 minutes
)
```

#### `sec-rate-limit` - Implement Rate Limiting

**Impact**: DoS protection, resource management

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Per-route rate limiting
@app.get("/api/items/")
@limiter.limit("100/minute")
async def get_items(request: Request):
    return items

# Per-user rate limiting
def get_user_identifier(request: Request) -> str:
    if hasattr(request.state, "user"):
        return f"user:{request.state.user.id}"
    return get_remote_address(request)

@app.post("/api/expensive-operation/")
@limiter.limit("10/hour", key_func=get_user_identifier)
async def expensive_operation(request: Request):
    pass
```

#### `sec-input` - Validate and Sanitize Input

**Impact**: Injection prevention, data integrity

```python
import re
import bleach
from pydantic import field_validator

class CommentCreate(BaseModel):
    content: str = Field(max_length=10000)

    @field_validator('content')
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        # Remove potentially dangerous HTML
        return bleach.clean(
            v,
            tags=['p', 'br', 'strong', 'em', 'a'],
            attributes={'a': ['href']},
            protocols=['http', 'https']
        )

class SearchQuery(BaseModel):
    q: str = Field(max_length=200)

    @field_validator('q')
    @classmethod
    def validate_query(cls, v: str) -> str:
        # Remove SQL injection patterns
        dangerous_patterns = [
            r"'.*--",
            r";\s*DROP",
            r";\s*DELETE",
            r"UNION\s+SELECT"
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Invalid search query")
        return v.strip()
```

#### `sec-headers` - Set Security Headers

**Impact**: Browser protection, security hardening

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Enable XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
        )

        # HSTS (only in production)
        if not settings.DEBUG:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

---

### 7. Performance (MEDIUM)

#### `perf-response` - Use response_model for Filtering

**Impact**: Reduce payload size, prevent data leaks

```python
# ❌ INCORRECT - returns entire ORM object
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: DBSession):
    return await db.get(User, user_id)  # includes password_hash!

# ✅ CORRECT - filtered response
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    # password_hash not included!

    model_config = ConfigDict(from_attributes=True)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DBSession):
    user = await db.get(User, user_id)
    return user  # only fields in UserResponse are serialized

# For excluding specific fields dynamically
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: DBSession,
    include_email: bool = False
) -> UserResponse:
    user = await db.get(User, user_id)
    response = UserResponse.model_validate(user)
    if not include_email:
        response.email = None
    return response
```

#### `perf-cache` - Implement Caching Strategies

**Impact**: Reduce database load, faster responses

```python
import redis.asyncio as redis
from functools import wraps
import json

redis_client = redis.from_url("redis://localhost:6379")

def cache_response(ttl: int = 300, key_prefix: str = "cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Call function and cache result
            result = await func(*args, **kwargs)
            await redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result, default=str)
            )
            return result
        return wrapper
    return decorator

@app.get("/products/{product_id}")
@cache_response(ttl=600)
async def get_product(product_id: int, db: DBSession):
    return await db.get(Product, product_id)

# Cache invalidation
async def invalidate_product_cache(product_id: int):
    pattern = f"cache:get_product:*{product_id}*"
    async for key in redis_client.scan_iter(match=pattern):
        await redis_client.delete(key)
```

#### `perf-background` - Use BackgroundTasks for Async Work

**Impact**: Faster responses, deferred processing

```python
from fastapi import BackgroundTasks

async def send_email_notification(email: str, message: str):
    # Slow email sending operation
    await email_client.send(email, message)

async def update_analytics(user_id: int, action: str):
    # Analytics tracking that doesn't need immediate response
    await analytics.track(user_id, action)

@app.post("/orders/")
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: DBSession,
    current_user: CurrentUser
):
    # Create order immediately
    new_order = await create_order_in_db(db, order, current_user.id)

    # Schedule background tasks (don't block response)
    background_tasks.add_task(
        send_email_notification,
        current_user.email,
        f"Order {new_order.id} confirmed!"
    )
    background_tasks.add_task(
        update_analytics,
        current_user.id,
        "order_created"
    )

    return new_order  # returns immediately
```

#### `perf-streaming` - Use StreamingResponse for Large Data

**Impact**: Memory efficiency, better UX for large files

```python
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

async def generate_large_csv(db: DBSession) -> AsyncGenerator[str, None]:
    yield "id,name,email\n"  # header

    async with db.stream(select(User)) as result:
        async for user in result.scalars():
            yield f"{user.id},{user.name},{user.email}\n"

@app.get("/export/users")
async def export_users(db: DBSession):
    return StreamingResponse(
        generate_large_csv(db),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )

# For file downloads
@app.get("/files/{file_id}")
async def download_file(file_id: str):
    file_path = get_file_path(file_id)

    async def file_iterator():
        async with aiofiles.open(file_path, 'rb') as f:
            while chunk := await f.read(64 * 1024):  # 64KB chunks
                yield chunk

    return StreamingResponse(
        file_iterator(),
        media_type="application/octet-stream"
    )
```

#### `perf-compression` - Enable Response Compression

**Impact**: Network efficiency, faster transfers

```python
from fastapi.middleware.gzip import GZipMiddleware

# Enable GZip compression for responses > 500 bytes
app.add_middleware(GZipMiddleware, minimum_size=500)

# For fine-grained control with Brotli
from starlette_compress import CompressMiddleware

app.add_middleware(
    CompressMiddleware,
    minimum_size=500,
    gzip_level=6,  # 1-9, higher = more compression
    brotli_quality=4,  # 0-11, higher = more compression
)

# Skip compression for already compressed content
@app.get("/images/{image_id}")
async def get_image(image_id: str):
    # Images are already compressed, skip middleware
    return FileResponse(
        f"images/{image_id}.png",
        media_type="image/png",
        headers={"Content-Encoding": "identity"}
    )
```

#### `perf-middleware` - Order Middleware by Frequency

**Impact**: Reduce overhead, optimize hot paths

```python
# ❌ INCORRECT - inefficient middleware order
app.add_middleware(LoggingMiddleware)      # runs every request
app.add_middleware(AuthMiddleware)         # runs every request
app.add_middleware(RateLimitMiddleware)    # should reject early
app.add_middleware(CORSMiddleware)         # should handle preflight early

# ✅ CORRECT - optimized middleware order (last added = first executed)
# 1. CORS - handle preflight requests immediately
app.add_middleware(CORSMiddleware, ...)

# 2. Rate limiting - reject excessive requests early
app.add_middleware(RateLimitMiddleware)

# 3. Compression - wrap response (must be after content is generated)
app.add_middleware(GZipMiddleware)

# 4. Request ID - add early for logging
app.add_middleware(RequestIDMiddleware)

# 5. Logging - track all requests
app.add_middleware(LoggingMiddleware)

# 6. Error handling - catch errors from all layers
app.add_middleware(ErrorHandlingMiddleware)

# 7. Authentication - validate tokens
app.add_middleware(AuthMiddleware)
```

---

### 8. Testing (LOW)

#### `test-client` - Use TestClient or httpx.AsyncClient

**Impact**: Proper API testing, realistic requests

```python
from fastapi.testclient import TestClient
import pytest

# Sync testing with TestClient
def test_get_items():
    client = TestClient(app)
    response = client.get("/items/")
    assert response.status_code == 200
    assert "items" in response.json()

# Async testing with httpx
import httpx
import pytest_asyncio

@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_items_async(async_client: httpx.AsyncClient):
    response = await async_client.get("/items/")
    assert response.status_code == 200
```

#### `test-override` - Use dependency_overrides

**Impact**: Clean mocking, test isolation

```python
import pytest
from unittest.mock import AsyncMock

# Create test database session
@pytest_asyncio.fixture
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_async_session() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

# Mock external services
@pytest.fixture
def mock_email_service():
    mock = AsyncMock()
    mock.send.return_value = True

    app.dependency_overrides[get_email_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()
```

#### `test-async` - Use pytest-asyncio Properly

**Impact**: Async test support, event loop management

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

# Use session-scoped event loop for better performance
@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/users/",
        json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
```

#### `test-fixture` - Create Reusable Fixtures

**Impact**: Test organization, DRY testing

```python
import pytest
from typing import AsyncGenerator
from faker import Faker

fake = Faker()

@pytest_asyncio.fixture
async def test_user(test_db: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        email=fake.email(),
        name=fake.name(),
        password_hash=get_password_hash("testpass123")
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user

@pytest_asyncio.fixture
async def auth_headers(test_user: User) -> dict:
    """Get authentication headers for test user."""
    token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def test_items(test_db: AsyncSession, test_user: User) -> list[Item]:
    """Create multiple test items."""
    items = [
        Item(name=fake.word(), price=fake.pyfloat(min_value=1, max_value=100), owner_id=test_user.id)
        for _ in range(5)
    ]
    test_db.add_all(items)
    await test_db.commit()
    return items

# Composable fixtures
@pytest.mark.asyncio
async def test_user_items(async_client: AsyncClient, auth_headers: dict, test_items: list[Item]):
    response = await async_client.get("/users/me/items", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 5
```

#### `test-mock` - Mock External Services

**Impact**: Test isolation, deterministic tests

```python
from unittest.mock import AsyncMock, patch, MagicMock
import pytest

@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    mock = AsyncMock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.delete.return_value = 1
    return mock

@pytest.fixture
def mock_http_client():
    """Mock httpx client for external API calls."""
    mock = AsyncMock()
    mock.get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"data": "mocked"}
    )
    return mock

@pytest.mark.asyncio
async def test_cached_endpoint(async_client: AsyncClient, mock_redis: AsyncMock):
    with patch("app.dependencies.redis_client", mock_redis):
        # First call - cache miss
        mock_redis.get.return_value = None
        response = await async_client.get("/products/1")
        assert response.status_code == 200
        mock_redis.set.assert_called_once()

        # Second call - cache hit
        mock_redis.get.return_value = '{"id": 1, "name": "Product"}'
        response = await async_client.get("/products/1")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_external_api_failure(async_client: AsyncClient, mock_http_client: AsyncMock):
    mock_http_client.get.side_effect = httpx.RequestError("Connection failed")

    with patch("app.services.external.http_client", mock_http_client):
        response = await async_client.get("/external-data")
        assert response.status_code == 503
```

#### `test-coverage` - Maintain Test Coverage

**Impact**: Quality assurance, confidence in changes

```python
# pyproject.toml configuration
"""
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = [
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80"
]

[tool.coverage.run]
source = ["app"]
omit = ["app/migrations/*", "app/tests/*"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:"
]
"""

# conftest.py for coverage with async
import pytest
import coverage

@pytest.fixture(scope="session", autouse=True)
def coverage_setup():
    """Ensure coverage captures async code."""
    cov = coverage.Coverage()
    cov.start()
    yield
    cov.stop()
    cov.save()
```

---

## Project Structure

```
app/
├── main.py                 # FastAPI app, routers, startup
├── dependencies.py         # Shared dependencies (DI)
├── config.py              # Settings (pydantic-settings)
├── models/                # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py           # Base model class
│   └── user.py
├── schemas/               # Pydantic request/response models
│   ├── __init__.py
│   ├── common.py         # Generic models (pagination, etc.)
│   └── user.py
├── routers/               # API routers by domain
│   ├── __init__.py
│   └── users.py
├── services/              # Business logic layer
│   ├── __init__.py
│   └── user_service.py
├── repositories/          # Data access layer
│   ├── __init__.py
│   └── user_repository.py
├── core/
│   ├── security.py       # Auth utilities, JWT
│   ├── exceptions.py     # Custom exceptions
│   └── middleware.py     # Custom middleware
└── tests/
    ├── conftest.py       # Fixtures
    ├── test_users.py
    └── factories/        # Test data factories
```

## Integration Workflow

When implementing FastAPI features:

1. **Before implementation**: Review relevant rule categories
2. **During development**: Apply patterns from quick reference
3. **Code review**: Verify against rule checklist
4. **Performance issues**: Consult detailed rules for solutions

```
async-* rules → Ensure non-blocking operations
    ↓
di-* rules → Proper dependency injection
    ↓
pydantic-* rules → Validation and serialization
    ↓
db-* rules → Efficient database access
    ↓
err-* rules → Consistent error handling
    ↓
sec-* rules → Security hardening
    ↓
perf-* rules → Performance optimization
    ↓
test-* rules → Quality assurance
```

## Compliance Checklist

Before submitting FastAPI code:

- [ ] No blocking I/O in async functions (`async-block`)
- [ ] Parallel I/O with `asyncio.gather` (`async-gather`)
- [ ] Dependencies use `Depends()` and `yield` (`di-depends`, `di-yield`)
- [ ] Pydantic models with proper validation (`pydantic-field`)
- [ ] Async database operations with SQLAlchemy (`db-async`)
- [ ] N+1 queries prevented with eager loading (`db-n-plus-one`)
- [ ] HTTPException with proper status codes (`err-http`)
- [ ] Authentication via OAuth2/JWT (`sec-oauth2`, `sec-jwt`)
- [ ] Response models filter sensitive data (`perf-response`)
- [ ] Tests use dependency_overrides (`test-override`)
