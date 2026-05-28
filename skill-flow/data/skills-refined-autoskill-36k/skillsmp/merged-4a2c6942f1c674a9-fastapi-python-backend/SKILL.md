---
name: fastapi-python-backend
description: Use this skill when building high-performance Python backend APIs with FastAPI, implementing authentication, database integration, and data processing.
---

# FastAPI Python Backend Development

You are an expert in building Python backend applications using FastAPI, SQLAlchemy, and Pydantic, focusing on async operations, authentication, and data processing.

## Core Principles

- **Async-First**: Use async/await for all I/O operations.
- **Type Safety**: Utilize Pydantic models for request and response validation.
- **Dependency Injection**: Implement shared logic using FastAPI's `Depends()`.
- **OpenAPI-Driven**: Automatically generate API documentation.
- **Separation of Concerns**: Structure your application into routes, services, and repositories.

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── config.py            # Settings with pydantic-settings
│   ├── dependencies.py      # Shared dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py    # API v1 router
│   │   │   └── endpoints/
│   │   │       ├── users.py
│   │   │       └── items.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py      # JWT, OAuth2
│   │   └── exceptions.py    # Custom exceptions
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py       # Async session factory
│   │   └── base.py          # SQLAlchemy base
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   └── services/            # Business logic
│       ├── __init__.py
│       └── user_service.py
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── alembic/                 # Migrations
├── pyproject.toml
└── .env
```

## Application Setup

### Main Application

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
```

### Configuration with pydantic-settings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
```

## Async Endpoints

### Basic CRUD Endpoints

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.create(user_in)
```

## Authentication (JWT)

### Security Module

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Database Operations

### SQLAlchemy Async

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

### Migrations with Alembic

```bash
# Create migration
alembic revision --autogenerate -m "add users table"

# Apply migrations
alembic upgrade head
```

## Data Processing

### Using pandas for Data Validation

```python
import pandas as pd
from fastapi import UploadFile

@app.post("/api/upload-csv")
async def process_csv(file: UploadFile):
    df = pd.read_csv(file.file)
    # Validate and process data
    return {"total_rows": len(df)}
```

## Background Tasks

### Using Celery

```python
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def send_email_task(user_id: int):
    # Long-running email task
    send_email(user_id)
```

## Testing with pytest

### Test Configuration

```python
import pytest
from httpx import AsyncClient

@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app) as ac:
        yield ac
```

### Writing Tests

```python
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/v1/users/", json={"email": "test@example.com", "password": "securepass"})
    assert response.status_code == 201
```

## Best Practices

- Use async/await for I/O operations.
- Type hints for all function signatures.
- Pydantic models for validation.
- Environment variables via pydantic-settings.
- Alembic for database migrations.
- pytest for testing.

This skill provides a comprehensive guide for developing robust Python backend applications using FastAPI, ensuring best practices and efficient patterns are followed throughout the development process.