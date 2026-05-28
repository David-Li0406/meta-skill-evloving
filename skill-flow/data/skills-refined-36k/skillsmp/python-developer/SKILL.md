---
name: python-developer
description: Expert Python development guidance for this codebase. Use when writing Python code, implementing features, or following project coding standards and patterns.
---

# Python Developer Skill

You are an expert Python developer for this codebase. Apply these coding patterns and guidelines when writing Python code.

> **Team Guide**: See `.claude/skills/python-standards/SKILL.md` for priority-ordered rules.
>
> | Priority | Category | Action |
> |----------|----------|--------|
> | 1 | Security | MUST FIX before merge |
> | 2 | Style & Readability | MUST ADHERE to standards |
> | 3 | Performance | SUGGESTED optimizations |

---

## Tech Stack Context

This project uses:

- **Python 3.12+** with modern type hints (`X | None`, `dict[str, Any]`)
- **LangGraph** for multi-agent orchestration
- **FastAPI** for web services
- **Pydantic v2** and **SQLModel** for data modeling
- **SQLAlchemy 2.0** with async support
- **asyncio/anyio** for async operations
- **pytest** with `pytest-asyncio` for testing
- **AWS Bedrock** for LLM models
- **MCP (Model Context Protocol)** for tool integration

---

## Development Guidelines

### Type Hints (Python 3.10+ Style)

```python
# Use modern union syntax
def process(data: dict[str, Any]) -> str | None:
    ...

# Use collections.abc for abstract types
from collections.abc import Mapping, Sequence, Iterable

def handle_items(items: Sequence[str]) -> Mapping[str, int]:
    ...

# Fully type public APIs
async def fetch_user(user_id: str) -> User | None:
    ...
```

### Type Hints (Python 3.12+ Style)

```python
# New generic class syntax (preferred in 3.12+)
class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

# Generic functions
def first[T](items: list[T]) -> T:
    return items[0]

# Type aliases with `type` keyword
type Vector[T] = list[tuple[T, T]]
type JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]

# @override decorator for method overrides
from typing import override

class Child(Parent):
    @override
    def process(self) -> str:
        return "child"
```

### Async Patterns

```python
# Always use async libraries in async context
async def fetch_data(url: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Python 3.11+ - Use TaskGroup for structured concurrency (preferred)
async def fetch_all(urls: list[str]) -> list[dict]:
    results = []
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(client.get(url)) for url in urls]
        results = [t.result().json() for t in tasks]
    return results

# Legacy style with asyncio.gather (still valid)
async def fetch_all_legacy(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return [r.json() for r in responses if not isinstance(r, Exception)]

# Proper task cancellation handling
async def cancellable_operation():
    try:
        await long_running_task()
    except asyncio.CancelledError:
        await cleanup()
        raise  # Always re-raise CancelledError
```

### Pydantic Model Design

```python
from pydantic import BaseModel, Field, field_validator

class UserRequest(BaseModel):
    """Request model for user creation."""

    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    role: str = "member"

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip()

# Use model_config for settings
class Config(BaseModel):
    model_config = {"frozen": True, "extra": "forbid"}
```

### FastAPI Endpoint Patterns

```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Create a new user."""
    try:
        user = await user_service.create(db, request)
        return UserResponse.model_validate(user)
    except DuplicateEmailError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
```

### SQLAlchemy/SQLModel Patterns

```python
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.ext.asyncio import AsyncSession

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    owner_id: str = Field(index=True)  # Multi-tenancy

    # Relationships
    messages: list["Message"] = Relationship(back_populates="user")

# Always use async sessions
async def get_user(db: AsyncSession, user_id: int, owner_id: str) -> User | None:
    stmt = select(User).where(User.id == user_id, User.owner_id == owner_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Batch queries to avoid N+1
async def get_users(db: AsyncSession, user_ids: list[int]) -> list[User]:
    stmt = select(User).where(User.id.in_(user_ids))
    result = await db.execute(stmt)
    return list(result.scalars().all())
```

### LangGraph Node Patterns

```python
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

class AgentState(BaseModel):
    """State passed between nodes."""
    messages: list[dict]
    intent: str | None = None
    context: dict[str, Any] = {}

async def classify_intent(state: AgentState) -> dict[str, Any]:
    """Node: Classify user intent."""
    # Return only changed fields - LangGraph merges automatically
    intent = await classifier.classify(state.messages[-1])
    return {"intent": intent}

def route_by_intent(state: AgentState) -> str:
    """Conditional edge: Route based on intent."""
    match state.intent:
        case "data":
            return "genie_agent"
        case "platform":
            return "platform_agent"
        case _:
            return "default_response"

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("classify", classify_intent)
workflow.add_conditional_edges("classify", route_by_intent)
```

### Error Handling Patterns

```python
# Define specific exceptions
class ServiceError(Exception):
    """Base exception for service errors."""
    pass

class NotFoundError(ServiceError):
    """Resource not found."""
    pass

class ValidationError(ServiceError):
    """Input validation failed."""
    pass

# Use exception chaining
async def get_user_or_fail(db: AsyncSession, user_id: int, owner_id: str) -> User:
    try:
        user = await get_user(db, user_id, owner_id)  # Always scope by owner_id
        if not user:
            raise NotFoundError(f"User {user_id} not found")
        return user
    except SQLAlchemyError as e:
        logger.error("Database error fetching user %s: %s", user_id, e)
        raise ServiceError("Failed to fetch user") from e

# HTTP error responses
@router.get("/{user_id}")
async def get_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    try:
        user = await get_user_or_fail(db, user_id, current_user.owner_id)
        return UserResponse.model_validate(user)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ServiceError as e:
        raise HTTPException(status_code=500, detail="Internal error") from e
```

### Testing Approach

```python
import pytest
from unittest.mock import AsyncMock, patch

# Mark async tests
@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    request = UserRequest(name="Test", email="test@example.com")
    user = await user_service.create(db_session, request)

    assert user.name == "Test"
    assert user.email == "test@example.com"

# Use fixtures appropriately
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.rollback()

# Mock external dependencies, not internal logic
@pytest.mark.asyncio
async def test_fetch_external_data():
    with patch("module.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=Mock(json=lambda: {"data": "test"})
        )
        result = await fetch_data("http://example.com")
        assert result == {"data": "test"}

# Test error cases
@pytest.mark.asyncio
async def test_get_user_not_found(db_session: AsyncSession):
    with pytest.raises(NotFoundError, match="User 999 not found"):
        await get_user_or_fail(db_session, user_id=999, owner_id="test-owner")
```

### Code Organization

```python
# Import ordering: stdlib, third-party, local
import asyncio
from collections.abc import Sequence
from typing import Any

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from .models import User
from .services import user_service

# Constants at module level
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Keep functions focused (<50 lines)
# Use dataclasses/Pydantic for >4 parameters
# Prefer early returns to reduce nesting
```

---

## Project-Specific Patterns

### Multi-Agent Architecture

- Agents don't directly call each other - use intent routing
- Each agent has specialized tools and knowledge domains
- WiliBot synthesizes responses from agent outputs
- State flows through nodes using Pydantic models

### State Management

- Use Pydantic models for all state (defined in `core/state.py`, `core/schema/`)
- State is immutable - return new state objects from nodes
- Include `owner_id` and `user_id` for multi-tenancy

### MCP Tool Patterns

- Extract auth from request headers (no local token storage)
- Tokens expire every 15 minutes - handle refresh
- Tools should be stateless and idempotent where possible

### Database Patterns

- Use Flyway for migrations (never manual schema changes)
- All queries scoped by `owner_id` for tenant isolation
- Use async sessions with `asyncpg`
- Connection pooling via SQLAlchemy engine

---

## Advanced Patterns

### Async Context Managers

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

@asynccontextmanager
async def managed_resource() -> AsyncGenerator[Resource, None]:
    """Properly manage async resources with cleanup."""
    resource = await acquire_resource()
    try:
        yield resource
    finally:
        await resource.close()

# Usage in FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    await init_database()
    yield
    # Shutdown
    await close_database()
```

### Timeout Handling

```python
import asyncio

async def fetch_with_timeout(url: str, timeout: float = 10.0) -> dict[str, Any]:
    """Fetch with timeout - raises TimeoutError on timeout."""
    async with asyncio.timeout(timeout):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()

# With fallback
async def fetch_with_fallback(url: str, default: dict[str, Any]) -> dict[str, Any]:
    """Fetch with graceful fallback on timeout."""
    try:
        async with asyncio.timeout(5.0):
            return await do_fetch(url)
    except TimeoutError:
        logger.warning("Request to %s timed out, using default", url)
        return default
```

### Advanced Pydantic Validation

```python
from pydantic import BaseModel, Field, field_validator, model_validator

class QueryRequest(BaseModel):
    """Request with complex validation logic."""

    start_date: datetime
    end_date: datetime
    filters: dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(default=100, ge=1, le=1000)

    @field_validator("filters")
    @classmethod
    def validate_filters(cls, v: dict[str, Any]) -> dict[str, Any]:
        # Sanitize filter keys
        allowed = {"status", "type", "owner_id"}
        return {k: v for k, v in v.items() if k in allowed}

    @model_validator(mode="after")
    def validate_date_range(self) -> "QueryRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

async def process_request(request_id: str, user_id: str) -> Result:
    """Use structured logging with context."""
    log = logger.bind(request_id=request_id, user_id=user_id)

    log.info("processing_started")
    try:
        result = await do_processing()
        log.info("processing_completed", result_id=result.id)
        return result
    except ProcessingError as e:
        log.error("processing_failed", error=str(e), error_type=type(e).__name__)
        raise
```

### Retry Pattern with Backoff

```python
import asyncio
from collections.abc import Callable, Awaitable
from typing import TypeVar

T = TypeVar("T")

async def retry_with_backoff[T](
    func: Callable[[], Awaitable[T]],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> T:
    """Retry async function with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return await func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(
                "Attempt %d failed, retrying in %.1fs: %s",
                attempt + 1, delay, e
            )
            await asyncio.sleep(delay)
    raise RuntimeError("Unreachable")  # For type checker
```

### Dependency Injection Pattern

```python
from functools import lru_cache
from typing import Annotated
from fastapi import Depends

class Settings(BaseModel):
    """Application settings from environment."""
    database_url: str
    redis_url: str
    debug: bool = False

    model_config = {"env_prefix": "APP_"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Type alias for cleaner signatures
SettingsDep = Annotated[Settings, Depends(get_settings)]

@router.get("/health")
async def health(settings: SettingsDep) -> dict[str, str]:
    return {"status": "ok", "debug": str(settings.debug)}
```
