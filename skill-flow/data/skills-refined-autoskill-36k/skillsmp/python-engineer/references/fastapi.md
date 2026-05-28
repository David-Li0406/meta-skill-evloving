# FastAPI Development

## Project Structure

```
app/
├── main.py              # FastAPI app initialization
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── users.py
│   │   └── items.py
│   └── dependencies.py
├── core/
│   ├── config.py        # Settings with pydantic-settings
│   └── security.py
├── models/
│   ├── user.py          # SQLAlchemy models
│   └── item.py
├── schemas/
│   ├── user.py          # Pydantic schemas
│   └── item.py
└── services/
    ├── user_service.py
    └── item_service.py
```

## Request/Response Schemas

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}

class UserList(BaseModel):
    items: list[UserResponse]
    total: int
```

## Route Handlers

```python
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    if await service.exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    return await service.create(user)

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    user = await service.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("")
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> UserList:
    users, total = await service.list(skip=skip, limit=limit)
    return UserList(items=users, total=total)
```

## Dependency Injection

```python
from fastapi import Depends
from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserService:
    return UserService(UserRepository(db))

# Usage with Annotated for cleaner syntax
DbSession = Annotated[AsyncSession, Depends(get_db)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@router.get("/{user_id}")
async def get_user(user_id: str, service: UserServiceDep) -> UserResponse:
    ...
```

## Error Handling

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f"{resource} with id '{id}' not found",
            code="NOT_FOUND",
            status_code=404
        )

app = FastAPI()

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )
```

## Settings with pydantic-settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    database_url: str
    secret_key: str
    debug: bool = False

settings = Settings()
```

## Background Tasks

```python
from fastapi import BackgroundTasks

async def send_notification(user_id: str, message: str) -> None:
    # Async notification logic
    ...

@router.post("/{user_id}/notify")
async def notify_user(
    user_id: str,
    message: str,
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    background_tasks.add_task(send_notification, user_id, message)
    return {"status": "notification queued"}
```

## Testing FastAPI

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    response = await client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_404(client: AsyncClient) -> None:
    response = await client.get("/users/nonexistent-id")
    assert response.status_code == 404
```
