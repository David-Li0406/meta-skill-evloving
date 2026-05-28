# FastAPI PATCH Endpoint Implementation - Complete Summary

## What Was Implemented

A complete FastAPI application demonstrating a PATCH endpoint for partial user updates, including:

1. **Pydantic Models** - For user data and updates
2. **PATCH Endpoint** - Handling partial updates correctly
3. **Comprehensive Tests** - Demonstrating all scenarios
4. **Documentation** - Visual guides and detailed explanations

---

## 1. The Pydantic Model for Updates

### Location
`skills/technical_skills/programming/web_frameworks/python/fastapi/examples/patch_endpoint_example.py`

### Code
```python
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserUpdate(BaseModel):
    """
    Model for partial user updates.

    KEY FEATURE: All fields are Optional, allowing partial updates.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)
```

### Why This Works
- **All fields are `Optional[T]`** - Clients can omit any field
- **Default value `None`** - Unprovided fields default to None
- **Validation preserved** - Fields still validated when provided

---

## 2. The PATCH Endpoint Implementation

### Location
Same file as above

### Code
```python
from fastapi import FastAPI, HTTPException, status

@app.patch("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    PATCH endpoint for partial user updates.

    KEY FEATURES:
    1. Only updates fields that are provided in the request
    2. Ignores fields that are None (not provided)
    3. Preserves existing values for fields not in the request
    """
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    # Get the existing user
    existing_user = fake_db[user_id]

    # Get the update data as a dictionary, excluding None values
    # This is the key to partial updates!
    update_data = user_update.model_dump(exclude_unset=True)

    # If no fields were provided, return the user unchanged
    if not update_data:
        return existing_user

    # Update only the fields that were provided
    # The ** operator unpacks the dictionary as keyword arguments
    updated_user = existing_user.model_copy(update=update_data)

    # Save to "database"
    fake_db[user_id] = updated_user

    return updated_user
```

### Key Mechanisms

1. **`model_dump(exclude_unset=True)`**
   - Returns only fields that were explicitly set in the request
   - Excludes fields that weren't provided (not just None values)
   - Example: `{"name": "John"}` → `{"name": "John"}` (not `{"name": "John", "email": None, "age": None}`)

2. **`model_copy(update=...)`**
   - Creates a new Pydantic model instance
   - Only updates fields specified in the update dict
   - Preserves existing values for all other fields
   - Immutable: doesn't modify the original object

3. **Empty check (`if not update_data`)**
   - Returns early if no fields provided
   - Avoids unnecessary database operations
   - Returns user unchanged

---

## 3. How It Handles Different Scenarios

### Scenario 1: Update Only Name
**Request:**
```bash
curl -X PATCH http://localhost:8000/users/1 \\
  -H "Content-Type: application/json" \\
  -d '{"name": "John Updated"}'
```

**Result:**
```json
{
  "id": 1,
  "name": "John Updated",        // CHANGED
  "email": "john@example.com",   // UNCHANGED
  "age": 30                      // UNCHANGED
}
```

**What happens:**
1. Pydantic parses: `UserUpdate(name="John Updated", email=None, age=None)`
2. `exclude_unset=True` → `{"name": "John Updated"}`
3. `model_copy(update={"name": "John Updated"})`
4. Only name is updated, other fields preserved

### Scenario 2: Update Multiple Fields
**Request:**
```bash
curl -X PATCH http://localhost:8000/users/1 \\
  -H "Content-Type: application/json" \\
  -d '{"name": "John", "age": 35}'
```

**Result:**
```json
{
  "id": 1,
  "name": "John",                // CHANGED
  "email": "john@example.com",   // UNCHANGED
  "age": 35                      // CHANGED
}
```

### Scenario 3: Empty Request
**Request:**
```bash
curl -X PATCH http://localhost:8000/users/1 \\
  -H "Content-Type: application/json" \\
  -d '{}'
```

**Result:**
- User returned unchanged
- Early return from empty check
- No database write

---

## 4. Testing

### Run Tests
```bash
# Navigate to the examples directory from the repository root
cd skills/technical_skills/programming/web_frameworks/python/fastapi/examples

uv run python test_patch_endpoint.py
```

### Test Coverage
- ✅ Partial update (name only)
- ✅ Partial update (age only)
- ✅ Partial update (multiple fields)
- ✅ Empty update (no fields)
- ✅ Full update (all fields)
- ✅ Pydantic `exclude_unset=True` demonstration
- ✅ Pydantic `model_copy(update=...)` demonstration

### Run Visual Guide
```bash
uv run python visual_guide.py
```

Shows step-by-step flow of how partial updates work.

---

## 5. Key Takeaways

### Essential Pattern for PATCH Endpoints

```python
# 1. Update model with all Optional fields
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

# 2. Extract only provided fields
update_data = user_update.model_dump(exclude_unset=True)

# 3. Handle empty updates
if not update_data:
    return existing_user

# 4. Apply partial updates
updated_user = existing_user.model_copy(update=update_data)
```

### Common Mistakes to Avoid

1. **Don't use `model_dump()` without `exclude_unset=True`**
   - Will include all fields as None
   - Would overwrite existing data with None

2. **Don't use required fields in update model**
   - Defeats the purpose of PATCH
   - Clients must provide all fields

3. **Don't mutate the original object**
   - Use `model_copy()` instead of `setattr()`
   - Maintains immutability (idiomatic Pydantic)

---

## 6. Files Created

1. **patch_endpoint_example.py**
   - Complete FastAPI application
   - Pydantic models (User, UserCreate, UserUpdate)
   - CRUD endpoints (GET, POST, PATCH, DELETE)
   - In-memory database simulation
   - Can be run as a server

2. **test_patch_endpoint.py**
   - Comprehensive test suite
   - Demonstrates all scenarios
   - Shows Pydantic mechanics
   - All tests pass

3. **visual_guide.py**
   - Step-by-step visual explanation
   - Shows request/response flow
   - Compares PUT vs PATCH
   - Explains key mechanisms

4. **PATCH_ENDPOINT_README.md**
   - Detailed documentation
   - Code examples
   - Common mistakes
   - Usage instructions

5. **IMPLEMENTATION_SUMMARY.md** (this file)
   - Executive summary
   - Quick reference
   - All file locations

---

## 7. Quick Reference

### Run the Server
```bash
# Navigate to the examples directory from the repository root
cd skills/technical_skills/programming/web_frameworks/python/fastapi/examples

uv run python patch_endpoint_example.py
```

### Run Tests
```bash
uv run python test_patch_endpoint.py
```

### View Visual Guide
```bash
uv run python visual_guide.py
```

### Test with curl
```bash
# Update only name
curl -X PATCH http://localhost:8000/users/1 \\
  -H "Content-Type: application/json" \\
  -d '{"name": "Updated Name"}'

# Update only age
curl -X PATCH http://localhost:8000/users/1 \\
  -H "Content-Type: application/json" \\
  -d '{"age": 35}'

# Update multiple fields
curl -X PATCH http://localhost:8000/users/1 \\
  -H "Content-Type: application/json" \\
  -d '{"name": "New Name", "email": "new@example.com"}'
```

---

## Conclusion

This implementation demonstrates the **idiomatic FastAPI/Pydantic way** to handle PATCH requests with partial updates:

- Clean, type-safe code
- Proper handling of all edge cases
- Comprehensive test coverage
- Clear documentation

The pattern is reusable for any PATCH endpoint in FastAPI applications.
