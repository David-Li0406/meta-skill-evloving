# Pydantic Partial Updates

## Overview
Implementing PATCH endpoints that correctly update only provided fields, avoiding data corruption from `None` overwrites.

## Problem Statement
**The partial update trap:**
- Naive implementations overwrite all fields, even unprovided ones become `None`
- Data silently corrupted when optional fields are missing from requests
- Frontend cannot send partial updates without destroying data

## Pattern

### ❌ Broken (None Overwrites)
```python
@app.patch("/users/{user_id}")
async def update_user(user_id: int, update: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    # ❌ This sets unprovided fields to None!
    user.name = update.name  # None if not provided
    user.email = update.email  # None if not provided
    await db.commit()
    return user
```

### ✅ Production Pattern
```python
from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

@app.patch("/users/{user_id}")
async def update_user(
    user_id: int,
    update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # CRITICAL: Only update provided fields
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user
```

## Key Mechanism

`model_dump(exclude_unset=True)` - Only includes fields that were explicitly set in the request, ignoring default `None` values.

## Example Flow

```python
# Request: {"name": "New Name"}
update_data = update.model_dump(exclude_unset=True)
# Result: {"name": "New Name"}
# email and age are NOT included, so they won't be overwritten

# Request: {}
update_data = update.model_dump(exclude_unset=True)
# Result: {}
# No fields updated, user remains unchanged
```

## Testing

```python
@pytest.mark.asyncio
async def test_partial_update(async_client: AsyncClient):
    # Create user with all fields
    response = await async_client.post("/users", json={
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30
    })
    user_id = response.json()["id"]

    # Update only name
    response = await async_client.patch(f"/users/{user_id}", json={
        "name": "Alice Updated"
    })

    # Verify only name changed
    data = response.json()
    assert data["name"] == "Alice Updated"
    assert data["email"] == "alice@example.com"  # Unchanged
    assert data["age"] == 30  # Unchanged
```

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Empty request body `{}` | Return unchanged user |
| All fields provided | Update all fields |
| Some fields provided | Update only those fields |
| Invalid field type | Return 422 validation error |

## Pydantic v1 vs v2

| Version | Method |
|---------|--------|
| Pydantic v1 | `dict(exclude_unset=True)` |
| Pydantic v2 | `model_dump(exclude_unset=True)` |

## See Also
- [Request Validation Capability](request_validation.md)
- [Python to API Conversion Capability](python-to-api-conversion.md)
