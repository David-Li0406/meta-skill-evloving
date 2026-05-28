# FastAPI PATCH Endpoint - Quick Reference

## TL;DR

```python
from typing import Optional
from pydantic import BaseModel

# 1. Update model - ALL Optional fields
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

# 2. PATCH endpoint
@app.patch("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
    existing_user = get_user(user_id)

    # Extract only provided fields
    update_data = user_update.model_dump(exclude_unset=True)

    # Handle empty update
    if not update_data:
        return existing_user

    # Apply partial updates
    updated_user = existing_user.model_copy(update=update_data)

    return save_user(updated_user)
```

---

## The Three Key Steps

### 1. Create Update Model with Optional Fields
```python
class UserUpdate(BaseModel):
    name: Optional[str] = None      # ← Optional + None default
    email: Optional[EmailStr] = None
    age: Optional[int] = None
```

### 2. Extract Only Provided Fields
```python
update_data = user_update.model_dump(exclude_unset=True)
# {"name": "John"} if only name provided
# {} if nothing provided
```

### 3. Apply Partial Updates
```python
updated_user = existing_user.model_copy(update=update_data)
# Only updates fields in update_data
# Preserves all other fields
```

---

## Request → Response Examples

### Update Name Only
**Request:** `{"name": "John"}`

**Result:**
- name: CHANGED
- email: UNCHANGED
- age: UNCHANGED

### Update Multiple Fields
**Request:** `{"name": "John", "age": 25}`

**Result:**
- name: CHANGED
- email: UNCHANGED
- age: CHANGED

### Empty Request
**Request:** `{}`

**Result:** ALL UNCHANGED

---

## Common Mistakes

### ❌ Wrong: Using model_dump() without exclude_unset
```python
update_data = user_update.model_dump()
# Returns: {"name": "John", "email": None, "age": None}
# Will overwrite email and age with None!
```

### ✅ Right: Using exclude_unset=True
```python
update_data = user_update.model_dump(exclude_unset=True)
# Returns: {"name": "John"}
# Only updates provided fields!
```

### ❌ Wrong: Required fields in update model
```python
class UserUpdate(BaseModel):
    name: str  # Required! Can't do partial updates
```

### ✅ Right: Optional fields
```python
class UserUpdate(BaseModel):
    name: Optional[str] = None  # Optional!
```

---

## PUT vs PATCH

### PUT (Complete Replacement)
```json
PUT /users/1
{
  "name": "John",
  "email": "john@example.com",  // Must include ALL fields
  "age": 30
}
```

### PATCH (Partial Update)
```json
PATCH /users/1
{
  "name": "John"    // Only changed fields
}
```

---

## File Locations

All files in:
```
/Volumes/Samsung-SSD-T7/Workspaces/Github/qredence/agent-framework/v0.5/_WORLD/skills-fleet/skills/technical_skills/programming/web_frameworks/python/fastapi/examples/
```

- `patch_endpoint_example.py` - Complete working example
- `test_patch_endpoint.py` - Test suite
- `visual_guide.py` - Visual explanation
- `PATCH_ENDPOINT_README.md` - Full documentation
- `IMPLEMENTATION_SUMMARY.md` - Detailed summary
- `QUICK_REFERENCE.md` - This file

---

## Run It

```bash
# Navigate to the examples directory from the repository root
cd skills/technical_skills/programming/web_frameworks/python/fastapi/examples

# Run server
uv run python patch_endpoint_example.py

# Run tests
uv run python test_patch_endpoint.py

# View visual guide
uv run python visual_guide.py
```

---

## The Pattern (Copy & Paste)

```python
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Update model
class ModelUpdate(BaseModel):
    field1: Optional[str] = None
    field2: Optional[int] = None
    field3: Optional[bool] = None

# PATCH endpoint
@app.patch("/items/{item_id}")
async def update_item(item_id: int, item_update: ModelUpdate):
    # Get existing item
    existing_item = get_item(item_id)
    if not existing_item:
        raise HTTPException(404, "Item not found")

    # Extract provided fields
    update_data = item_update.model_dump(exclude_unset=True)

    # Handle empty update
    if not update_data:
        return existing_item

    # Apply partial updates
    updated_item = existing_item.model_copy(update=update_data)

    # Save and return
    return save_item(updated_item)
```

---

**That's it! Three simple steps to implement PATCH endpoints in FastAPI.**
