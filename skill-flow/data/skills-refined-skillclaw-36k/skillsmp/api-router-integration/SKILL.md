---
name: api-router-integration
description: Patterns for creating and registering API routers in GUTTERS. Ensures consistent auth, response models, and proper wiring.
---

# API Router Integration

Standard patterns for adding new API endpoints to GUTTERS.

## Router Creation

### File Location
```
src/app/api/v1/{feature}.py
```

### Basic Template
```python
"""
{Feature} API Endpoints

{Brief description of what these endpoints do}
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.db.database import async_get_db
from app.models.user_profile import UserProfile

router = APIRouter(prefix="/{feature}", tags=["{feature}"])


@router.get("/")
async def get_{feature}(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    """
    Get {feature} for authenticated user.
    """
    user_id = current_user["id"]
    # Implementation
    return {"status": "ok"}
```

---

## Router Registration

### CRITICAL: Register in `api/v1/__init__.py`

```python
# File: src/app/api/v1/__init__.py

from fastapi import APIRouter

# Existing imports
from .users import router as users_router
from .login import router as login_router
from .tiers import router as tiers_router

# ADD YOUR ROUTER
from .{feature} import router as {feature}_router

router = APIRouter(prefix="/v1")

# Existing includes
router.include_router(users_router)
router.include_router(login_router)
router.include_router(tiers_router)

# ADD YOUR INCLUDE
router.include_router({feature}_router)
```

### Common Mistake
❌ Forgetting to register → Endpoints return 404
❌ Wrong prefix → Routes clash

---

## Authentication Patterns

### Standard Auth (Required for most endpoints)
```python
from app.api.dependencies import get_current_user

@router.get("/data")
async def get_data(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    user_id = current_user["id"]
    is_superuser = current_user.get("is_superuser", False)
```

### Optional Auth (Public with enhanced authenticated)
```python
from app.api.dependencies import get_optional_user

@router.get("/public")
async def get_public(
    current_user: Annotated[dict | None, Depends(get_optional_user)],
):
    if current_user:
        # Enhanced response for authenticated
        pass
    else:
        # Basic response for public
        pass
```

### Superuser Required
```python
@router.post("/admin")
async def admin_action(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if not current_user.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Superuser required")
```

---

## Response Models

### Always Use Pydantic Response Models
```python
from pydantic import BaseModel

class FeatureResponse(BaseModel):
    id: int
    status: str
    data: dict
    
    model_config = ConfigDict(from_attributes=True)

@router.get("/data", response_model=FeatureResponse)
async def get_data() -> FeatureResponse:
    ...
```

### List Responses
```python
@router.get("/items", response_model=list[ItemResponse])
async def get_items() -> list[ItemResponse]:
    ...
```

---

## Background Tasks

### For Expensive Operations
```python
from fastapi import BackgroundTasks

@router.post("/trigger")
async def trigger_operation(
    background_tasks: BackgroundTasks,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    user_id = current_user["id"]
    
    # Queue background task
    background_tasks.add_task(
        expensive_function,
        user_id=user_id,
        # other params
    )
    
    return {"status": "queued", "user_id": user_id}
```

---

## Query Parameters

### Optional with Defaults
```python
@router.get("/search")
async def search(
    q: str | None = None,
    limit: int = 10,
    offset: int = 0,
):
    ...
```

### Enum Validation
```python
from enum import Enum

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

@router.get("/items")
async def get_items(sort: SortOrder = SortOrder.DESC):
    ...
```

---

## Error Handling

### Standard HTTP Exceptions
```python
from fastapi import HTTPException

# 400 Bad Request
raise HTTPException(status_code=400, detail="Invalid input")

# 403 Forbidden
raise HTTPException(status_code=403, detail="Not authorized")

# 404 Not Found
raise HTTPException(status_code=404, detail="Resource not found")

# 422 Validation Error (usually automatic from Pydantic)
raise HTTPException(status_code=422, detail="Validation failed")
```

---

## Common Patterns

### Get User's Resource
```python
@router.get("/profile/synthesis")
async def get_synthesis(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    user_id = current_user["id"]
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(404, "Profile not found")
    
    return profile.data.get("synthesis")
```

### Create/Update Resource
```python
@router.post("/preferences/model")
async def set_model_preference(
    model: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    if model not in ALLOWED_MODELS:
        raise HTTPException(400, f"Invalid model. Allowed: {ALLOWED_MODELS}")
    
    user_id = current_user["id"]
    await update_user_preference(user_id, "llm_model", model, db)
    
    return {"status": "updated", "model": model}
```

---

## Checklist

- [ ] Router created in `api/v1/{feature}.py`
- [ ] Router registered in `api/v1/__init__.py`
- [ ] All endpoints have `current_user` dependency (if authenticated)
- [ ] All endpoints have `response_model` defined
- [ ] Error responses use proper HTTP status codes
- [ ] Background tasks for expensive operations
- [ ] Tests cover auth, happy path, and error cases
