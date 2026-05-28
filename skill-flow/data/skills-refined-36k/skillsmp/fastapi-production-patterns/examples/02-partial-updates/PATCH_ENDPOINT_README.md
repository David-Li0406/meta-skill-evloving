# FastAPI PATCH Endpoint - Partial Updates Implementation

## Overview

This implementation demonstrates how to create a PATCH endpoint for updating users that only updates the fields provided in the request, leaving other fields unchanged.

## Key Components

### 1. Pydantic Model for Updates

```python
class UserUpdate(BaseModel):
    """
    Model for partial user updates.

    KEY FEATURE: All fields are Optional, allowing partial updates.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)
```

**Why this works:**
- All fields are `Optional[T]` with default value `None`
- Clients can provide any subset of fields
- Unprovided fields default to `None`

### 2. The PATCH Endpoint Implementation

```python
@app.patch("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    PATCH endpoint for partial user updates.
    """
    # Get existing user
    existing_user = fake_db[user_id]

    # KEY: Get only fields that were actually provided
    update_data = user_update.model_dump(exclude_unset=True)

    # If no fields provided, return unchanged
    if not update_data:
        return existing_user

    # Apply updates using model_copy
    updated_user = existing_user.model_copy(update=update_data)

    # Save and return
    fake_db[user_id] = updated_user
    return updated_user
```

**Key mechanisms:**

1. **`exclude_unset=True`** - Returns only fields that were explicitly set in the request
   - `{"name": "John"}` → `{"name": "John"}`
   - `{}` → `{}` (empty dict)
   - Excludes fields that weren't provided (instead of including them as `None`)

2. **`model_copy(update=...)`** - Creates a copy with only specified fields updated
   - Preserves existing values for fields not in `update_data`
   - Returns a new instance without modifying the original

3. **Empty check** - Returns user unchanged if no fields provided

### 3. Handling Different Request Scenarios

#### Scenario 1: Update Only Name
**Request:**
```json
PATCH /users/1
{
  "name": "John Updated"
}
```

**Result:**
- `name` is updated to "John Updated"
- `email` and `age` remain unchanged
- `exclude_unset=True` → `{"name": "John Updated"}`
- `model_copy(update=...)` updates only name

#### Scenario 2: Update Only Age
**Request:**
```json
PATCH /users/1
{
  "age": 35
}
```

**Result:**
- `age` is updated to 35
- `name` and `email` remain unchanged
- `exclude_unset=True` → `{"age": 35}`

#### Scenario 3: Update Multiple Fields
**Request:**
```json
PATCH /users/1
{
  "name": "John Updated",
  "email": "john.new@example.com"
}
```

**Result:**
- `name` and `email` are updated
- `age` remains unchanged
- `exclude_unset=True` → `{"name": "John Updated", "email": "john.new@example.com"}`

#### Scenario 4: Empty Request
**Request:**
```json
PATCH /users/1
{}
```

**Result:**
- User is returned unchanged
- `exclude_unset=True` → `{}`
- Empty dict check returns early

## Complete Example

### Model Definitions

```python
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    """Full user model"""
    id: int
    name: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    """Update model with all optional fields"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
```

### Endpoint Implementation

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Simulated database
fake_db = {1: User(id=1, name="John", email="john@example.com", age=30)}

@app.patch("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate):
    # Check if user exists
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    # Get existing user
    existing_user = fake_db[user_id]

    # Get only provided fields
    update_data = user_update.model_dump(exclude_unset=True)

    # Return unchanged if no fields provided
    if not update_data:
        return existing_user

    # Apply partial updates
    updated_user = existing_user.model_copy(update=update_data)

    # Save
    fake_db[user_id] = updated_user
    return updated_user
```

## Testing

Run the test file to see all scenarios in action:

```bash
python test_patch_endpoint.py
```

This will demonstrate:
- Partial updates (single field)
- Partial updates (multiple fields)
- Empty updates
- Full updates
- How `exclude_unset=True` works
- How `model_copy(update=...)` works

## Why This Approach is Better

### Compared to PUT:
- **PUT**: Requires ALL fields, replaces entire resource
- **PATCH**: Updates only provided fields, preserves others

### Example:
To change only the user's name:

**PUT (requires all fields):**
```json
PUT /users/1
{
  "name": "New Name",
  "email": "john@example.com",  // Must include even if not changing
  "age": 30                       // Must include even if not changing
}
```

**PATCH (only changed fields):**
```json
PATCH /users/1
{
  "name": "New Name"
}
```

## Key Takeaways

1. **Use `Optional` fields** in update models to allow partial updates
2. **Use `exclude_unset=True`** to get only provided fields (not all fields with None)
3. **Use `model_copy(update=...)`** to apply updates while preserving existing values
4. **Handle empty updates** by checking if the update dict is empty
5. **Return early** if no fields need updating (avoid unnecessary database writes)

## Common Mistakes to Avoid

### Mistake 1: Using `model_dump()` without `exclude_unset`
```python
# WRONG - includes all fields as None
update_data = user_update.model_dump()
# Result: {"name": None, "email": None, "age": None}
# This would overwrite all fields with None!
```

### Mistake 2: Not using Optional fields
```python
# WRONG - all fields required
class UserUpdate(BaseModel):
    name: str  # Required! Can't do partial updates
    email: EmailStr  # Required!
    age: int  # Required!
```

### Mistake 3: Not handling empty updates
```python
# WRONG - unnecessary database write
update_data = user_update.model_dump(exclude_unset=True)
updated_user = existing_user.model_copy(update=update_data)
# Even if update_data is empty, this still creates a copy
```

## Files

- `patch_endpoint_example.py` - Complete working FastAPI app with PATCH endpoint
- `test_patch_endpoint.py` - Comprehensive tests and demonstrations
- `PATCH_ENDPOINT_README.md` - This documentation

## Running the Example

```bash
# Run the server
python patch_endpoint_example.py

# In another terminal, test the endpoint
curl -X PATCH http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Or run the test suite
python test_patch_endpoint.py
```
