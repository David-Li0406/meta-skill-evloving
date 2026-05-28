# FastAPI Dependency Injection

## Overview

FastAPI's dependency injection system allows you to share logic, manage database sessions, handle authentication, and more.

## Basic Dependency

```python
from fastapi import Depends

def get_query_params(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

@app.get("/items")
async def get_items(params: dict = Depends(get_query_params)):
    return {"skip": params["skip"], "limit": params["limit"]}
```

## Class Dependencies

```python
from dataclasses import dataclass

@dataclass
class Pagination:
    skip: int = 0
    limit: int = 100

@app.get("/items")
async def get_items(pagination: Pagination = Depends()):
    return {"skip": pagination.skip, "limit": pagination.limit}
```

## Database Session

```python
from sqlmodel import Session
from app.database import engine

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/items")
async def get_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()
```

## Async Database Session

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session

@app.get("/items")
async def get_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item))
    return result.scalars().all()
```

## Authentication

```python
from fastapi import Depends, HTTPException, Header, status

async def get_current_user(
    authorization: str = Header(..., alias="Authorization")
) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization[7:]
    user = await verify_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

## Role-Based Access

```python
def require_role(allowed_roles: list[str]):
    async def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker

@app.get("/admin")
async def admin_only(user: User = Depends(require_role(["admin"]))):
    return {"message": "Welcome, admin!"}

@app.get("/moderator")
async def mod_or_admin(user: User = Depends(require_role(["admin", "moderator"]))):
    return {"message": "Welcome!"}
```

## Chained Dependencies

```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return await verify_token(token)

async def get_current_active_user(
    user: User = Depends(get_current_user)
) -> User:
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

@app.get("/me")
async def get_me(user: User = Depends(get_current_active_user)):
    return user
```

## Dependencies in Router

```python
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)],  # Applied to all routes
)

@router.get("")
async def get_tasks():
    # User is already authenticated
    pass
```

## Global Dependencies

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])

# All routes now require API key
```

## Dependency with Cleanup

```python
async def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
```

## Optional Dependencies

```python
from typing import Optional

async def get_optional_user(
    authorization: Optional[str] = Header(None)
) -> Optional[User]:
    if not authorization:
        return None

    try:
        return await verify_token(authorization[7:])
    except:
        return None

@app.get("/posts")
async def get_posts(user: Optional[User] = Depends(get_optional_user)):
    if user:
        return get_user_posts(user.id)
    return get_public_posts()
```

## Configuration Dependency

```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str

    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {"database": settings.database_url[:20] + "..."}
```

## Testing with Dependencies

```python
from fastapi.testclient import TestClient

def override_get_current_user():
    return User(id="test_user", email="test@example.com")

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_protected_route():
    response = client.get("/me")
    assert response.status_code == 200
```
