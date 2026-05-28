---
name: python-fastapi
description: FastAPI framework, pydantic models, dependency injection, API design
license: MIT
compatibility: opencode
metadata:
  audience: python-developers
  focus: web-frameworks
---

## What I do

I provide guidance on building APIs with FastAPI, including:

- Pydantic models for validation
- Dependency injection patterns
- Route organization and tags
- API versioning strategies
- Error handling and exception handlers
- Background tasks and async endpoints
- Testing FastAPI apps with TestClient
- OpenAPI/Swagger documentation
- Security and authentication
- Middleware and CORS
- WebSockets and streaming

## When to use me

Use me when:
- Building RESTful APIs with FastAPI
- Designing pydantic models and schemas
- Implementing dependency injection
- Setting up authentication and authorization
- Writing API tests
- Configuring OpenAPI documentation
- Handling async endpoints
- Implementing middleware
- Working with websockets

## Best Practices

### ✅ Use Pydantic Models for Validation

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Schema for user creation."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)

    @validator("name")
    def name_must_not_contain_numbers(cls, v: str) -> str:
        """Validate name doesn't contain numbers."""
        if any(c.isdigit() for c in v):
            raise ValueError("name cannot contain numbers")
        return v

class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    name: str
    email: str
    age: Optional[int] = None
    created_at: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True
```

### ✅ Dependency Injection with Type Hints

```python
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Protocol, Annotated

app = FastAPI()

class UserRepository(Protocol):
    """Protocol for user repository."""
    async def get_user(self, user_id: int) -> Optional[User]: ...

async def get_db_session() -> AsyncSession:
    """Dependency for database session."""
    async with async_session() as session:
        yield session

async def get_user_repository(
    session: AsyncSession = Depends(get_db_session)
) -> UserRepository:
    """Dependency for user repository."""
    return SQLUserRepository(session)

# Use Annotated for cleaner dependencies
from fastapi import Depends
from typing import Annotated

DB = Annotated[AsyncSession, Depends(get_db_session)]
UserRepo = Annotated[UserRepository, Depends(get_user_repository)]

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    repo: UserRepo
) -> UserResponse:
    """Get a user by ID with dependency injection."""
    user = await repo.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.from_orm(user)
```

### ✅ Route Organization and Tags

```python
from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    repo: UserRepo
) -> UserResponse:
    """Create a new user."""
    user = await repo.create_user(user_data)
    return UserResponse.from_orm(user)

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    repo: UserRepo
) -> List[UserResponse]:
    """List all users with pagination."""
    users = await repo.list_users(skip=skip, limit=limit)
    return [UserResponse.from_orm(u) for u in users]

# Include router in main app
app = FastAPI()
app.include_router(router)
```

### ✅ Proper Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class UserNotFoundError(Exception):
    """Exception for user not found."""
    pass

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError
) -> JSONResponse:
    """Handle user not found exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found"},
    )

@app.get("/users/{user_id}")
async def get_user(user_id: int, repo: UserRepo) -> UserResponse:
    """Get user with custom exception."""
    user = await repo.get_user(user_id)
    if user is None:
        raise UserNotFoundError()
    return UserResponse.from_orm(user)
```

### ✅ Async Endpoints with Background Tasks

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str, name: str) -> None:
    """Send welcome email (background task)."""
    # Send email synchronously (runs in background)
    send_email(email, f"Welcome, {name}!")

@app.post("/users/")
async def create_user(
    user_data: UserCreate,
    repo: UserRepo,
    background_tasks: BackgroundTasks
) -> UserResponse:
    """Create user and send welcome email in background."""
    user = await repo.create_user(user_data)

    # Schedule background task
    background_tasks.add_task(
        send_welcome_email,
        user_data.email,
        user_data.name
    )

    return UserResponse.from_orm(user)
```

### ✅ API Versioning

```python
from fastapi import APIRouter

# Version 1
v1_router = APIRouter(prefix="/api/v1", tags=["v1"])

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: int, repo: UserRepo) -> UserResponseV1:
    """Get user (v1)."""
    user = await repo.get_user(user_id)
    return UserResponseV1.from_orm(user)

# Version 2
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])

@v2_router.get("/users/{user_id}")
async def get_user_v2(user_id: int, repo: UserRepo) -> UserResponseV2:
    """Get user (v2 with additional fields)."""
    user = await repo.get_user(user_id)
    return UserResponseV2.from_orm(user)

app.include_router(v1_router)
app.include_router(v2_router)
```

### ✅ Testing FastAPI Apps

```python
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_create_user() -> None:
    """Test user creation."""
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data

def test_get_user_not_found() -> None:
    """Test getting non-existent user."""
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_async_endpoint() -> None:
    """Test async endpoint."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### ✅ Authentication and Security

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    repo: UserRepo = Depends()
) -> User:
    """Get current user from authorization header."""
    token = credentials.credentials
    user = await repo.verify_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user

@app.get("/me")
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get current user."""
    return UserResponse.from_orm(current_user)
```

### ✅ WebSocket Support

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    finally:
        await websocket.close()
```

### ✅ Custom Middleware

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to time requests."""

    async def dispatch(self, request: Request, call_next):
        """Time the request."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(TimingMiddleware)
```

## OpenAPI Configuration

### ✅ Customize OpenAPI Documentation

```python
app = FastAPI(
    title="My API",
    description="A comprehensive API with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/users/{user_id}", include_in_schema=False)
async def internal_endpoint(user_id: int) -> dict:
    """Internal endpoint (excluded from docs)."""
    return {"internal": True}
```

## Common Pitfalls

### ❌ Don't Run Blocking Code in Async Endpoints

```python
# BAD: Blocking I/O in async endpoint
@app.get("/heavy")
async def heavy_computation():
    result = blocking_function()  # Blocks event loop
    return {"result": result}

# GOOD: Offload to executor
@app.get("/heavy")
async def heavy_computation():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_function)
    return {"result": result}
```

### ❌ Don't Forget Response Models

```python
# BAD: Missing response model (no validation)
@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    user = await repo.get_user(user_id)
    return {"id": user.id, "name": user.name}

# GOOD: Use response model for validation
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    user = await repo.get_user(user_id)
    return UserResponse.from_orm(user)
```

### ❌ Don't Mix Sync and Async Database Calls

```python
# BAD: Mixing sync and async
@app.get("/users")
async def get_users():
    users = db.session.query(User).all()  # Sync call in async context
    return users

# GOOD: Use async database
@app.get("/users")
async def get_users(session: DB):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users
```

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI app setup
├── dependencies.py      # Dependency injection
├── models/              # Pydantic models
│   ├── __init__.py
│   ├── user.py
│   └── product.py
├── routes/              # API routes
│   ├── __init__.py
│   ├── users.py
│   └── products.py
├── services/            # Business logic
│   ├── __init__.py
│   ├── user_service.py
│   └── product_service.py
├── repositories/        # Database access
│   ├── __init__.py
│   ├── user_repository.py
│   └── product_repository.py
└── utils/               # Utilities
    ├── __init__.py
    ├── security.py
    └── validators.py
```

## References

- FastAPI documentation: https://fastapi.tiangolo.com/
- Pydantic documentation: https://docs.pydantic.dev/
- Real Python FastAPI tutorial: https://realpython.com/fastapi-python-web-apis/
- FastAPI best practices: https://fastapi.tiangolo.com/tutorial/
