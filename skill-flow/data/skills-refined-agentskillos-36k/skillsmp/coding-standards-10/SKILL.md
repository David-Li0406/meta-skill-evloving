---
name: coding-standards
description: Universal coding standards, best practices, and patterns for Python development.
---

# Coding Standards & Best Practices

Universal coding standards applicable across all projects.

## Code Quality Principles

### 1. Readability First
- Code is read more than written
- Clear variable and function names
- Self-documenting code preferred over comments
- Consistent formatting

### 2. KISS (Keep It Simple, Stupid)
- Simplest solution that works
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions
- Create reusable components
- Share utilities across modules
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

### 5. SOLID Principles
- A set of five design guidelines for maintainable, scalable, and testable code
- Encourages separation of responsibilities and clear abstractions
- Helps avoid tightly coupled, fragile architectures
- Supports long‑term evolution of the codebase without breaking existing behavior

## Python Standards

### Variable Naming

```python
# ✅ GOOD: Descriptive names (snake_case)
market_search_query = 'election'
is_user_authenticated = True
total_revenue = 1000

# ❌ BAD: Unclear names
q = 'election'
flag = True
x = 1000
```

### Function Naming

```python
# ✅ GOOD: Verb-noun pattern (snake_case)
async def fetch_market_data(market_id: str) -> dict:
    pass

def calculate_similarity(a: list[float], b: list[float]) -> float:
    pass

def is_valid_email(email: str) -> bool:
    pass

# ❌ BAD: Unclear or noun-only
async def market(id: str) -> dict:
    pass

def similarity(a, b):
    pass

def email(e):
    pass
```

### Immutability Pattern (CRITICAL)

```python
# ✅ GOOD: Create new objects/dicts instead of mutating
from copy import deepcopy

updated_user = {**user, 'name': 'New Name'}
updated_list = [*items, new_item]

updated_user = deepcopy(user)
updated_user['name'] = 'New Name'

# ❌ BAD: Mutate directly
user['name'] = 'New Name'  # BAD
items.append(new_item)     # BAD (unless items is meant to be mutable)
```

### Error Handling

```python
# ✅ GOOD: Comprehensive error handling
import httpx
import logging

logger = logging.getLogger(__name__)

async def fetch_data(url: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP error {e.response.status_code}: {e.response.text}')
        raise ValueError(f'HTTP {e.response.status_code}: {e.response.text}')
    except httpx.RequestError as e:
        logger.error(f'Request failed: {e}')
        raise ValueError('Failed to fetch data') from e

# ❌ BAD: No error handling
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Async/Await Best Practices

```python
# ✅ GOOD: Parallel execution when possible
import asyncio

users, markets, stats = await asyncio.gather(
    fetch_users(),
    fetch_markets(),
    fetch_stats()
)

# ❌ BAD: Sequential when unnecessary
users = await fetch_users()
markets = await fetch_markets()
stats = await fetch_stats()
```

### Type Safety

```python
# ✅ GOOD: Proper type hints
from typing import Literal
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Market:
    id: str
    name: str
    status: Literal['active', 'resolved', 'closed']
    created_at: datetime

async def get_market(market_id: str) -> Market:
    pass

# ❌ BAD: No type hints or using Any
from typing import Any

async def get_market(market_id: Any) -> Any:
    pass
```

## Class and Function Design

### Class Structure

```python
# ✅ GOOD: Well-structured class with type hints
from typing import Optional, Literal
from dataclasses import dataclass

@dataclass
class ButtonConfig:
    label: str
    disabled: bool = False
    variant: Literal['primary', 'secondary'] = 'primary'

class Button:
    def __init__(self, config: ButtonConfig, on_click: callable):
        self.config = config
        self.on_click = on_click

    def render(self) -> str:
        variant_class = f'btn-{self.config.variant}'
        disabled_attr = 'disabled' if self.config.disabled else ''
        return f'<button class="btn {variant_class}" {disabled_attr}>{self.config.label}</button>'

# ❌ BAD: No types, unclear structure
class Button:
    def __init__(self, props):
        self.props = props
```

### Decorators and Utilities

```python
# ✅ GOOD: Reusable decorator for debouncing
from functools import wraps
import asyncio
from typing import TypeVar, Callable

T = TypeVar('T')

def debounce(delay: float):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        task: Optional[asyncio.Task] = None

        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            nonlocal task
            if task:
                task.cancel()
            task = asyncio.create_task(asyncio.sleep(delay))
            await task
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@debounce(0.5)
async def search_markets(query: str):
    pass
```

### State Management

```python
# ✅ GOOD: Immutable state updates
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class AppState:
    count: int
    user: Optional[dict] = None

def increment_count(state: AppState) -> AppState:
    return replace(state, count=state.count + 1)

# ❌ BAD: Direct mutation
def increment_count(state: AppState):
    state.count += 1  # BAD: mutates state
```

### Conditional Logic

```python
# ✅ GOOD: Clear conditional logic
if isLoading:
    render_spinner()
elif error:
    render_error(error)
elif data:
    render_data(data)

# ❌ BAD: Deeply nested conditionals
if isLoading:
    render_spinner()
else:
    if error:
        render_error(error)
    else:
        if data:
            render_data(data)
```

## API Design Standards

### REST API Conventions

```
GET    /api/markets              # List all markets
GET    /api/markets/:id          # Get specific market
POST   /api/markets              # Create new market
PUT    /api/markets/:id          # Update market (full)
PATCH  /api/markets/:id          # Update market (partial)
DELETE /api/markets/:id          # Delete market

# Query parameters for filtering
GET /api/markets?status=active&limit=10&offset=0
```

### Response Format

```python
# ✅ GOOD: Consistent response structure
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class Meta(BaseModel):
    total: int
    page: int
    limit: int

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    meta: Optional[Meta] = None

from fastapi.responses import JSONResponse

return JSONResponse(
    content=ApiResponse(
        success=True,
        data=markets,
        meta=Meta(total=100, page=1, limit=10)
    ).model_dump()
)

return JSONResponse(
    content=ApiResponse(success=False, error='Invalid request').model_dump(),
    status_code=400
)
```

### Input Validation

```python
# ✅ GOOD: Schema validation with Pydantic
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List

class CreateMarketSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    end_date: datetime
    categories: List[str] = Field(..., min_length=1)

    @field_validator('categories')
    @classmethod
    def validate_categories(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError('At least one category is required')
        return v

from fastapi import HTTPException

@app.post('/api/markets')
async def create_market(data: CreateMarketSchema):
    try:
        validated = data
        return {'success': True, 'data': validated.model_dump()}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={'success': False, 'error': 'Validation failed', 'details': str(e)}
        )
```

## File Organization

### Project Structure

```
project/
├── app/                    # FastAPI/Django application
│   ├── api/               # API routes/views
│   │   ├── markets.py     # Market endpoints
│   │   └── auth.py        # Auth endpoints
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── repositories/      # Data access layer
│   └── middleware/        # Custom middleware
├── core/                  # Core utilities
│   ├── config.py          # Configuration
│   ├── exceptions.py      # Custom exceptions
│   └── dependencies.py    # Dependency injection
├── utils/                 # Helper functions
│   ├── validators.py      # Validation utilities
│   ├── formatters.py      # Formatting utilities
│   └── constants.py       # Constants
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
└── requirements.txt       # Dependencies
```

### File Naming

```
app/api/markets.py          # snake_case for modules
app/models/market.py        # snake_case for modules
utils/format_date.py        # snake_case for utilities
core/exceptions.py          # snake_case for modules
tests/test_markets.py       # test_ prefix for test files
```

## Comments & Documentation

### When to Comment

```python
# ✅ GOOD: Explain WHY, not WHAT
# Use exponential backoff to avoid overwhelming the API during outages
delay = min(1000 * (2 ** retry_count), 30000)

# Deliberately using list mutation here for performance with large arrays
items.append(new_item)

# ❌ BAD: Stating the obvious
# Increment counter by 1
count += 1

# Set name to user's name
name = user['name']
```

### Docstrings for Public APIs

```python
def search_markets(
    query: str,
    limit: int = 10
) -> list[Market]:
    """
    Searches markets using semantic similarity.

    Args:
        query: Natural language search query
        limit: Maximum number of results (default: 10)

    Returns:
        List of markets sorted by similarity score

    Raises:
        ValueError: If OpenAI API fails or Redis unavailable

    Example:
        >>> results = await search_markets('election', 5)
        >>> print(results[0].name)  # "Trump vs Biden"
    """
    # Implementation
    pass
```

## Performance Best Practices

### Memoization

```python
from functools import lru_cache, cache
from typing import List

# ✅ GOOD: Cache expensive computations
@lru_cache(maxsize=128)
def calculate_similarity(vector1: tuple, vector2: tuple) -> float:
    # Expensive computation
    pass

# ✅ GOOD: Cache function results
@cache
def get_market_by_id(market_id: str) -> dict:
    # Database query
    pass

# ✅ GOOD: Memoize expensive list operations
def get_sorted_markets(markets: List[dict]) -> List[dict]:
    # Create new sorted list instead of mutating
    return sorted(markets, key=lambda m: m['volume'], reverse=True)
```

### Lazy Loading

```python
# ✅ GOOD: Lazy import heavy modules
def get_heavy_module():
    # Only import when needed
    import heavy_ml_library
    return heavy_ml_library

# ✅ GOOD: Lazy evaluation with generators
def process_large_dataset():
    for item in large_dataset:  # Generator, not loaded all at once
        yield process_item(item)
```

### Database Queries

```python
# ✅ GOOD: Select only needed columns (Django)
from django.db.models import QuerySet

markets = Market.objects.only('id', 'name', 'status')[:10]

# ✅ GOOD: Select only needed columns (SQLAlchemy)
from sqlalchemy import select

markets = session.execute(
    select(Market.id, Market.name, Market.status)
    .limit(10)
).all()

# ❌ BAD: Select everything
markets = Market.objects.all()[:10]  # Loads all columns
```

## Testing Standards

### Test Structure (AAA Pattern)

```python
import pytest

def test_calculates_similarity_correctly():
    vector1 = [1, 0, 0]
    vector2 = [0, 1, 0]
    similarity = calculate_cosine_similarity(vector1, vector2)
    assert similarity == 0
```

### Test Naming

```python
# ✅ GOOD: Descriptive test names
def test_returns_empty_list_when_no_markets_match_query():
    pass

def test_raises_error_when_openai_api_key_is_missing():
    pass

def test_falls_back_to_substring_search_when_redis_unavailable():
    pass

# ❌ BAD: Vague test names
def test_works():
    pass

def test_search():
    pass
```

## Code Smell Detection

Watch for these anti-patterns:

### 1. Long Functions
```python
# ❌ BAD: Function > 50 lines
def process_market_data():
    # 100 lines of code
    pass

# ✅ GOOD: Split into smaller functions
def process_market_data():
    validated = validate_data()
    transformed = transform_data(validated)
    return save_data(transformed)
```

### 2. Deep Nesting
```python
# ❌ BAD: 5+ levels of nesting
if user:
    if user.is_admin:
        if market:
            if market.is_active:
                if has_permission:
                    # Do something
                    pass

# ✅ GOOD: Early returns
if not user:
    return
if not user.is_admin:
    return
if not market:
    return
if not market.is_active:
    return
if not has_permission:
    return

# Do something
```

### 3. Magic Numbers
```python
# ❌ BAD: Unexplained numbers
if retry_count > 3:
    pass
time.sleep(0.5)

# ✅ GOOD: Named constants
MAX_RETRIES = 3
DEBOUNCE_DELAY_SECONDS = 0.5

if retry_count > MAX_RETRIES:
    pass
time.sleep(DEBOUNCE_DELAY_SECONDS)
```

**Remember**: Code quality is not negotiable. Clear, maintainable code enables rapid development and confident refactoring.
