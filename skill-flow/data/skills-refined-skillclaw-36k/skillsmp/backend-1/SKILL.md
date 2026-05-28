---
name: backend
description: FastAPI backend development patterns. Use when creating API endpoints, authentication, database models, or backend logic.
tools:
  - read
  - write
  - bash
metadata:
  version: "1.0"
  category: development
  framework: fastapi
---

# Backend Development Skill

This skill provides patterns and guidance for developing the FastAPI backend.

## Route Creation Pattern

When creating a new API route:

### 1. Create Route File

```python
# backend/app/routes/example.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.auth import get_current_user, require_roles
from app.schemas.schemas import ExampleCreate, ExampleResponse
from app.models.store import example_store

router = APIRouter(prefix="/api/v1/example", tags=["Example"])

@router.get("")
async def get_all(
    current_user: dict = Depends(get_current_user)
):
    """Get all examples with role-based filtering."""
    if current_user["role"] == "admin":
        return {"examples": example_store.get_all()}
    return {"examples": example_store.get_by_user(current_user["id"])}

@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    data: ExampleCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new example."""
    item = example_store.create({
        **data.dict(),
        "created_by": current_user["id"]
    })
    return {"example": item, "message": "Created successfully"}

@router.put("/{item_id}")
async def update(
    item_id: str,
    data: ExampleCreate,
    current_user: dict = Depends(require_roles("admin"))
):
    """Update example (admin only)."""
    item = example_store.update(item_id, data.dict())
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return {"example": item}

@router.delete("/{item_id}")
async def delete(
    item_id: str,
    current_user: dict = Depends(require_roles("admin"))
):
    """Delete example (admin only)."""
    if not example_store.delete(item_id):
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted successfully"}
```

### 2. Register Route in main.py

```python
from app.routes import example
app.include_router(example.router)
```

## Authentication Decorators

```python
# Public endpoint (no auth)
@router.get("/public")
async def public_endpoint():
    pass

# Authenticated (any role)
@router.get("/protected")
async def protected(current_user: dict = Depends(get_current_user)):
    pass

# Role-restricted
@router.get("/admin-only")
async def admin_only(current_user: dict = Depends(require_roles("admin"))):
    pass

# Multiple roles
@router.get("/staff")
async def staff(current_user: dict = Depends(require_roles("admin", "supplier"))):
    pass
```

## Pydantic Schema Pattern

```python
# backend/app/schemas/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class ExampleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., ge=0)
    category_id: Optional[str] = None
    
class ExampleResponse(BaseModel):
    id: str
    name: str
    amount: float
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## Store Pattern (In-Memory Database)

```python
# backend/app/models/store.py
from datetime import datetime
import uuid

class ExampleStore:
    def __init__(self):
        self._data = {}
    
    def create(self, data: dict) -> dict:
        item_id = str(uuid.uuid4())
        item = {
            "id": item_id,
            **data,
            "created_at": datetime.utcnow().isoformat()
        }
        self._data[item_id] = item
        return item
    
    def get_all(self) -> list:
        return list(self._data.values())
    
    def get_by_id(self, item_id: str) -> dict | None:
        return self._data.get(item_id)
    
    def update(self, item_id: str, data: dict) -> dict | None:
        if item_id not in self._data:
            return None
        self._data[item_id].update(data)
        self._data[item_id]["updated_at"] = datetime.utcnow().isoformat()
        return self._data[item_id]
    
    def delete(self, item_id: str) -> bool:
        return self._data.pop(item_id, None) is not None

example_store = ExampleStore()
```

## Cross-Role Notifications

When an action affects multiple roles, create notifications:

```python
from app.models.store import notification_store

def notify_payment_completed(payment: dict):
    """Notify all relevant parties when payment is completed."""
    
    # Notify admin
    notification_store.create({
        "type": "payment_completed",
        "title": "Payment Confirmed",
        "message": f"Payment of ${payment['amount']} has been completed",
        "target_role": "admin"
    })
    
    # Notify supplier if assigned
    if payment.get("supplier_id"):
        notification_store.create({
            "type": "payment_completed",
            "title": "Payment Received",
            "message": f"Your payment of ${payment['amount']} has been processed",
            "user_id": payment["supplier_id"]
        })
```

## Error Handling

```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# 401 Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials"
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permission denied"
)

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)
```

## Testing Endpoints

```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@logiaccounting.demo","password":"Demo2024!Admin"}' \
  | jq -r '.token')

# Use token
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/example
```
