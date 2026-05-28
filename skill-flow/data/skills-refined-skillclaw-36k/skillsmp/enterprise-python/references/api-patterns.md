# API Patterns

Best practices for building APIs with FastAPI and Flask.

## Table of Contents
- [FastAPI Patterns](#fastapi-patterns)
- [Request Validation](#request-validation)
- [Error Handling](#error-handling)
- [Authentication](#authentication)
- [Dependency Injection](#dependency-injection)
- [Performance](#performance)

## FastAPI Patterns

### Route Organization
```python
# app/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User, CreateUserRequest, UserResponse
from app.services import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(get_user_service)
) -> User:
    return await service.create(request)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
) -> User:
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Application Factory
```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    await database.connect()
    await cache.connect()
    yield
    # Shutdown
    await database.disconnect()
    await cache.disconnect()

def create_app() -> FastAPI:
    app = FastAPI(
        title="My API",
        version="1.0.0",
        lifespan=lifespan
    )
    
    app.include_router(users.router)
    app.include_router(products.router)
    
    return app

app = create_app()
```

## Request Validation

### Pydantic Models
```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime
    
    model_config = {"from_attributes": True}
```

### Query Parameters
```python
from fastapi import Query
from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@router.get("/")
async def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    order: SortOrder = Query(default=SortOrder.desc),
    search: str | None = Query(default=None, min_length=1)
) -> list[UserResponse]:
    return await service.list(
        skip=skip, limit=limit, sort_by=sort_by, order=order, search=search
    )
```

## Error Handling

### Custom Exception Handlers
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str) -> None:
        super().__init__(
            message=f"{resource} with id '{id}' not found",
            code="NOT_FOUND",
            status_code=404
        )

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}}
    )
```

## Authentication

### JWT Authentication
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await user_service.get(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
async def get_current_user_profile(
    user: User = Depends(get_current_user)
) -> UserResponse:
    return user
```

### API Key Authentication
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)) -> str:
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
```

## Dependency Injection

### Service Dependencies
```python
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_database(settings: Settings = Depends(get_settings)) -> Database:
    return Database(settings.database_url)

def get_user_repository(db: Database = Depends(get_database)) -> UserRepository:
    return UserRepository(db)

def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    cache: Cache = Depends(get_cache)
) -> UserService:
    return UserService(repo=repo, cache=cache)
```

### Request-Scoped Dependencies
```python
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id")

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request_id_var.set(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

def get_request_id() -> str:
    return request_id_var.get()
```

## Performance

### Background Tasks
```python
from fastapi import BackgroundTasks

@router.post("/users")
async def create_user(
    request: CreateUserRequest,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    user = await service.create(request)
    background_tasks.add_task(send_welcome_email, user.email)
    return user
```

### Caching
```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend

@router.get("/{user_id}")
@cache(expire=300)  # Cache for 5 minutes
async def get_user(user_id: str) -> UserResponse:
    return await service.get(user_id)
```

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/")
@limiter.limit("10/minute")
async def create_resource(request: Request) -> Response:
    ...
```
