---
name: fastapi-development
description: Use this skill for expert-level FastAPI development, focusing on best practices, performance optimization, and async operations.
---

# FastAPI Development

This skill provides expert guidance for developing high-performance Python APIs using FastAPI, emphasizing best practices, async support, and modular design.

## Core Concepts

### FastAPI Features
- Fast performance (Starlette + Pydantic)
- Automatic OpenAPI/Swagger documentation
- Type hints and validation
- Async/await support
- Dependency injection
- OAuth2 and JWT authentication
- WebSocket support

### Key Components
- Path operations (routes)
- Request/response models (Pydantic)
- Dependency injection
- Middleware
- Background tasks
- Testing with TestClient

## Best Practices

### General Guidelines
- Write concise, technical responses with accurate Python examples.
- Favor functional, declarative programming over class-based approaches.
- Prioritize modularization to eliminate code duplication.
- Use descriptive variable names with auxiliary verbs (e.g., `is_active`, `has_permission`).
- Employ lowercase with underscores for file/directory naming (e.g., `routers/user_routes.py`).
- Export routes and utilities explicitly.
- Follow the RORO (Receive an Object, Return an Object) pattern.

### Error Handling
- Handle edge cases at function entry points.
- Employ early returns for error conditions.
- Place happy path logic last.
- Avoid unnecessary else statements; use if-return patterns.
- Implement guard clauses for preconditions.
- Provide proper error logging and user-friendly messaging.

### Performance Optimization
- Minimize blocking I/O; use async for all database and API calls.
- Implement caching with Redis or in-memory stores.
- Optimize Pydantic serialization/deserialization.
- Use lazy loading for large datasets.

## Basic FastAPI Application

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="My API",
    description="Production-ready FastAPI",
    version="1.0.0"
)

# Models
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True

# Routes
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # Create user in database
    db_user = await db.users.create(**user.dict())
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await db.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100):
    return await db.users.find_many(skip=skip, limit=limit)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# Database dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Auth dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user

# Use dependencies
@app.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Authentication

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
```

## Database Integration (SQLAlchemy)

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

# CRUD operations
async def get_user(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

## Testing

```python
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test User"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert "email" in response.json()

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
```

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Redis: https://redis.io/

## Compliance Checklist

Before submitting FastAPI code:

- [ ] No blocking I/O in async functions.
- [ ] Dependencies use `Depends()` and `yield`.
- [ ] Pydantic models with proper validation.
- [ ] HTTPException with proper status codes.
- [ ] Tests use dependency_overrides.