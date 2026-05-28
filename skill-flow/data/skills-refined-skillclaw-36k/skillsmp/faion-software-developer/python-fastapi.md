---
id: python-fastapi
name: "FastAPI Standards"
domain: DEV
skill: faion-software-developer
category: "development"
---

# FastAPI Standards

## Overview

FastAPI is a modern, high-performance Python web framework for building APIs. This methodology covers project structure, dependency injection, Pydantic models, async patterns, and best practices for production-grade FastAPI applications.

## When to Use

- Building new REST APIs in Python
- Microservices requiring high performance
- APIs needing automatic OpenAPI documentation
- Projects requiring async/await patterns
- Replacing Flask or Django REST APIs

## Key Principles

1. **Type hints everywhere** - FastAPI leverages Pydantic for validation
2. **Dependency injection** - Clean, testable code through Depends()
3. **Async by default** - Use async/await for I/O operations
4. **Schema-first** - Pydantic models define API contracts
5. **Separation of concerns** - Routes, services, repositories pattern

## Best Practices

### Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── config.py            # Settings with Pydantic
│   ├── dependencies.py      # Shared dependencies
│   │
│   ├── routers/             # API routes by domain
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── orders.py
│   │
│   ├── schemas/             # Pydantic models
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── orders.py
│   │
│   ├── models/              # SQLAlchemy/ORM models
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── users.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── database.py      # DB connection
│       └── repositories/    # Data access layer
│
├── tests/
├── pyproject.toml
└── Dockerfile
```

### Main Application Setup

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db, close_db
from app.routers import users, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production API",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
```

### Configuration with Pydantic

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "My API"
    debug: bool = False
    secret_key: str

    # Database
    database_url: str
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()
```

### Pydantic Schemas

```python
# app/schemas/users.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """User creation request."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """User update request - all fields optional."""
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """User response schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    """Paginated user list."""
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
```

### Dependency Injection

```python
# app/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.config import settings
from app.db.database import async_session
from app.models.user import User
from app.services import users as user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_db() -> AsyncSession:
    """Database session dependency."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


# Type aliases for cleaner signatures
DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
```

### Router Implementation

```python
# app/routers/users.py
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Query

from app.dependencies import DBSession, CurrentUser
from app.schemas.users import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.services import users as user_service

router = APIRouter()


@router.get("", response_model=UserListResponse)
async def list_users(
    db: DBSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """List all users with pagination."""
    users, total = await user_service.get_users(db, page=page, size=size)
    return UserListResponse(
        items=users,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    db: DBSession,
    user_data: UserCreate,
):
    """Create a new user."""
    existing = await user_service.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = await user_service.create_user(db, user_data)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    db: DBSession,
    current_user: CurrentUser,
    user_id: UUID,
):
    """Get user by ID."""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    db: DBSession,
    current_user: CurrentUser,
    user_id: UUID,
    user_data: UserUpdate,
):
    """Update user fields."""
    user = await user_service.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
```

### Service Layer

```python
# app/services/users.py
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate
from app.utils.security import hash_password


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    """Get user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_users(
    db: AsyncSession,
    *,
    page: int = 1,
    size: int = 20,
) -> tuple[list[User], int]:
    """Get paginated users."""
    # Count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar_one()

    # Fetch
    offset = (page - 1) * size
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    users = result.scalars().all()

    return list(users), total


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    """Create new user."""
    user = User(
        email=data.email,
        name=data.name,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def update_user(
    db: AsyncSession,
    user_id: UUID,
    data: UserUpdate,
) -> User | None:
    """Update user fields."""
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return user
```

## Anti-patterns

### Avoid: Sync Operations in Async Routes

```python
# BAD - blocks event loop
@router.get("/data")
async def get_data():
    data = requests.get("https://api.example.com")  # Sync!
    return data.json()

# GOOD - use async client
@router.get("/data")
async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()
```

### Avoid: Business Logic in Routes

```python
# BAD
@router.post("/orders")
async def create_order(db: DBSession, data: OrderCreate):
    # Validation logic here...
    # Inventory check here...
    # Payment processing here...
    pass

# GOOD - delegate to service
@router.post("/orders")
async def create_order(db: DBSession, data: OrderCreate):
    return await order_service.create_order(db, data)
```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
