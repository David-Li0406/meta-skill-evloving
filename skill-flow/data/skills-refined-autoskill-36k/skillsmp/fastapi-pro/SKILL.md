---
name: fastapi-pro
description: Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master microservices, WebSockets, and modern Python async patterns. Use PROACTIVELY for FastAPI development, async optimization, or API architecture.
---

# FastAPI Pro

Expert FastAPI developer specializing in high-performance, async-first API development with modern Python patterns.

## When to Use

- Building REST APIs with FastAPI
- Implementing async database operations
- Designing API architecture and endpoints
- Adding authentication/authorization
- Optimizing API performance
- Writing API tests

## Core Capabilities

### FastAPI Expertise

- FastAPI 0.100+ with Annotated types and modern dependency injection
- Async/await patterns for high-concurrency
- Pydantic V2 for validation and serialization
- Automatic OpenAPI/Swagger documentation
- Background tasks with BackgroundTasks
- File uploads and streaming responses
- Custom middleware and interceptors

### Data Management

- SQLAlchemy 2.0+ with async support
- Alembic for database migrations
- Repository pattern implementations
- Connection pooling and session management
- Query optimization and N+1 prevention
- Transaction management

### API Design

- RESTful API design principles
- API versioning strategies
- Rate limiting and throttling
- Pagination patterns (offset, cursor-based)
- Error handling and responses

### Authentication & Security

- OAuth2 with JWT tokens
- API key authentication
- Role-based access control (RBAC)
- CORS configuration
- Input sanitization
- Rate limiting per user/IP

## Vibe4Vets API Patterns

### Standard Endpoint Structure

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional

from app.core.database import get_session
from app.models.resource import Resource, ResourceRead, ResourceCreate

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])

@router.get("", response_model=list[ResourceRead])
async def list_resources(
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    category: Optional[str] = None,
    state: Optional[str] = None,
):
    """List resources with pagination and filters."""
    statement = select(Resource)

    if category:
        statement = statement.where(Resource.category == category)
    if state:
        statement = statement.where(Resource.state == state)

    statement = statement.offset(offset).limit(limit)
    resources = session.exec(statement).all()
    return resources


@router.get("/{resource_id}", response_model=ResourceRead)
async def get_resource(
    resource_id: int,
    session: Session = Depends(get_session),
):
    """Get a single resource by ID."""
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.post("", response_model=ResourceRead, status_code=201)
async def create_resource(
    resource: ResourceCreate,
    session: Session = Depends(get_session),
):
    """Create a new resource."""
    db_resource = Resource.model_validate(resource)
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource
```

### Search Endpoint with Full-Text Search

```python
from sqlalchemy import text

@router.get("/search", response_model=list[ResourceRead])
async def search_resources(
    q: str = Query(..., min_length=2),
    session: Session = Depends(get_session),
    limit: int = Query(default=20, le=100),
):
    """Full-text search across resources."""
    statement = text("""
        SELECT * FROM resource
        WHERE search_vector @@ plainto_tsquery('english', :query)
        ORDER BY ts_rank(search_vector, plainto_tsquery('english', :query)) DESC
        LIMIT :limit
    """)
    results = session.exec(statement, {"query": q, "limit": limit}).all()
    return results
```

### Admin Endpoints with Auth

```python
from app.core.auth import get_current_admin_user

@router.post("/admin/review/{resource_id}")
async def review_resource(
    resource_id: int,
    approved: bool,
    current_user = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    """Admin endpoint to approve/reject resource changes."""
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    resource.review_state = "approved" if approved else "rejected"
    resource.reviewed_by = current_user.id
    resource.reviewed_at = datetime.utcnow()

    session.add(resource)
    session.commit()
    return {"status": "success", "approved": approved}
```

### Background Tasks for ETL

```python
from fastapi import BackgroundTasks

@router.post("/admin/jobs/{connector_name}/run")
async def run_connector(
    connector_name: str,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_admin_user),
):
    """Trigger a connector job in the background."""
    background_tasks.add_task(run_connector_job, connector_name)
    return {"status": "started", "connector": connector_name}


async def run_connector_job(connector_name: str):
    """Background task to run connector."""
    from backend.connectors import get_connector
    connector = get_connector(connector_name)
    await connector.run()
```

## Pydantic Models

### Separate Read/Create/Update Models

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ResourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str
    state: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

class ResourceCreate(ResourceBase):
    """Used for POST requests."""
    pass

class ResourceUpdate(BaseModel):
    """Used for PATCH requests - all fields optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

class ResourceRead(ResourceBase):
    """Used for GET responses."""
    id: int
    trust_score: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
```

## Error Handling

```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

class ResourceNotFoundError(Exception):
    def __init__(self, resource_id: int):
        self.resource_id = resource_id

@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "resource_not_found",
            "message": f"Resource {exc.resource_id} not found",
        }
    )
```

## Testing Patterns

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_resources():
    response = client.get("/api/v1/resources")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_resource_not_found():
    response = client.get("/api/v1/resources/99999")
    assert response.status_code == 404

def test_create_resource():
    resource_data = {
        "name": "Test Resource",
        "category": "employment",
        "description": "Test description"
    }
    response = client.post("/api/v1/resources", json=resource_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Resource"
```

## Best Practices

### DO
- Use async/await for I/O operations
- Validate all inputs with Pydantic
- Use dependency injection for sessions
- Return proper HTTP status codes
- Document endpoints with docstrings
- Use type hints everywhere
- Implement proper error handling

### DON'T
- Block the event loop with sync operations
- Skip input validation
- Hardcode database connections
- Return 200 for errors
- Skip API documentation
- Use `Any` types
- Catch all exceptions silently

## Response Approach

1. **Analyze requirements** for async opportunities
2. **Design API contracts** with Pydantic models first
3. **Implement endpoints** with proper error handling
4. **Add comprehensive validation** using Pydantic
5. **Write tests** covering edge cases
6. **Optimize for performance** with caching
7. **Document with OpenAPI** annotations
