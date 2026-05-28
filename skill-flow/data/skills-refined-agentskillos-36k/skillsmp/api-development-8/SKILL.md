---
name: api-development
description: Guide for developing the API service using Python, FastAPI, Pydantic, and Docker. Use this when creating or modifying API endpoints, models, routers, or backend logic.
---

# API Service Development

This skill covers development of the FastAPI backend services located in `/api` (main API) and `/api_diagnostics` (system diagnostics API). Both services follow the same patterns and conventions.

## Technology Stack

- **Python 3.14** - Core language
- **FastAPI** - Web framework for building APIs
- **Pydantic** - Data validation and settings management
- **Docker** - Containerization
- **Redis** - Caching layer (via `redis.asyncio`)
- **uvicorn** - ASGI server

## Project Structure

```
api/
├── main.py              # FastAPI app entry point, router registration, middleware
├── config.py            # Settings and configuration
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build configuration
├── cache/               # Redis cache utilities
│   └── router.py
├── github/              # GitHub integration
│   ├── models.py
│   ├── router.py
│   └── retrieval.py
├── pihole/              # Pi-hole integration
│   ├── models.py
│   ├── router.py
│   ├── authentication.py
│   └── retrieval.py
├── nas/                 # Synology NAS integration
│   ├── models.py
│   ├── router.py
│   ├── authentication.py
│   ├── constants.py
│   └── retrieval.py
└── [other services]/    # Similar structure for each service
```

## Creating New Endpoints

### 1. Create Pydantic Models

Define request/response models in `models.py`:

```python
from pydantic import BaseModel, Field
from typing import Literal

class MyResponseData(BaseModel):
    name: str
    value: int
    status: Literal["active", "inactive"]

class MyResponse(BaseModel):
    data: MyResponseData
    success: Literal[True]
```

### 2. Create Router

Create a router in `router.py`:

```python
import logging
from fastapi import APIRouter, HTTPException, Request, status

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/myservice",
    tags=["MyService"],
)

@router.get("/", tags=["Ping"])
async def get_health(request: Request):
    return {"status": "ok"}

@router.get("/data/")
async def get_data(request: Request):
    try:
        # Implement data retrieval
        return {"data": "..."}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 3. Register Router

Add the router in `main.py`:

```python
from api.myservice.router import router as myservice_router

api.include_router(myservice_router)
```

### 4. Add Tags Metadata (Optional)

Add to `tags_metadata` in `main.py` for OpenAPI documentation:

```python
tags_metadata = [
    # ... existing tags
    {
        "name": "MyService",
        "description": "Description of my service",
    },
]
```

## Available Tools

### Linting and Formatting

Run these commands from the repository root:

```bash
# Format Python code with Black
black api/

# Sort imports with isort
isort api/

# Lint with flake8
flake8 api/
```

### Docker Operations

```bash
# Build the API container
docker compose -f compose.dev.yml build api

# Run the API in development mode
docker compose -f compose.dev.yml up api

# View API logs
docker compose -f compose.dev.yml logs -f api
```

### Dependency Management

```bash
# Install dependencies
pip install -r api/requirements.txt

# Add new dependency (update requirements.txt manually)
# Format: package>=min_version,<max_version
```

## Best Practices

1. **Use Type Hints**: Always use Python type hints for function parameters and return values
2. **Pydantic Validation**: Use Pydantic models for all request/response data
3. **Async Functions**: Use `async def` for endpoint handlers to support async operations
4. **Error Handling**: Use `HTTPException` with appropriate status codes
5. **Logging**: Use the module logger (`logger = logging.getLogger(__name__)`)
6. **Redis Caching**: Access Redis via `request.app.state.redis`
7. **Router Organization**: Each service module should have its own router with a unique prefix

## Patterns Used in This Codebase

### Authentication Pattern

For services requiring authentication (see `nas/authentication.py`, `pihole/authentication.py`):

```python
async def authenticate(credentials: dict) -> str:
    # Return session/token
    pass

async def logout(session: str) -> None:
    pass
```

### Data Retrieval Pattern

Separate retrieval logic from routers (see `retrieval.py` files):

```python
async def retrieve_data(request: Request) -> dict:
    # Fetch and process data
    redis = request.app.state.redis
    # Check cache, fetch if needed, cache result
    return data
```
