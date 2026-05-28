---
name: fastapi-best-practices
description: Use this skill when developing high-performance APIs with FastAPI, focusing on best practices, async operations, and modular code structure.
---

# FastAPI Best Practices

This skill provides expert guidance on developing FastAPI applications, emphasizing performance optimization, best practices, and effective use of async features.

## Core Concepts

### FastAPI Features
- Fast performance with Starlette and Pydantic
- Automatic OpenAPI/Swagger documentation
- Type hints and validation
- Async/await support
- Dependency injection
- OAuth2 and JWT authentication
- WebSocket support

### Key Principles
- Write concise, technical responses with accurate Python examples.
- Favor functional, declarative programming over class-based approaches.
- Prioritize modularization to eliminate code duplication.
- Use descriptive variable names and follow naming conventions (e.g., lowercase with underscores).

## Best Practices

### Performance Optimization
- Minimize blocking I/O; use async for all database and API calls.
- Implement caching strategies (e.g., Redis, in-memory).
- Optimize Pydantic serialization/deserialization.
- Use lazy loading for large datasets.

### Dependency Injection
- Use FastAPI's `Depends()` for shared logic to enhance code reuse and testability.
- Cache expensive dependencies to reduce redundant computation.

### Error Handling
- Handle edge cases at function entry points with early returns for error conditions.
- Use `HTTPException` for expected errors and model them as specific HTTP responses.

### Testing
- Write tests using `pytest` and `pytest-asyncio` for asynchronous code.
- Ensure proper resource cleanup with context managers.

## Example FastAPI Application

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

## Activation Triggers
This skill activates when:
- Writing new endpoints, routers, or dependencies.
- Implementing async patterns and database operations.
- Optimizing API performance.
- Reviewing or refactoring FastAPI code.
- Debugging async, validation, or database issues.
- Implementing authentication/authorization.
- Writing tests for FastAPI applications.