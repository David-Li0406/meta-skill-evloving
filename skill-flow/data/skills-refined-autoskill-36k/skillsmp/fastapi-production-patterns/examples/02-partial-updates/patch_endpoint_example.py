"""
FastAPI PATCH Endpoint Example - Partial User Updates

This example demonstrates how to create a PATCH endpoint that updates only the
fields provided in the request, leaving other fields unchanged.

WARNING: This is example code that uses global state (fake_db, next_id)
for simplicity. In production applications:
- Use a proper database (PostgreSQL, MongoDB, etc.)
- Replace global variables with proper dependency injection
- Consider using SQLAlchemy ORM with async support
- Add proper validation, error handling, and transaction support
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, HTTPException, status


# ========================================
# 1. THE USER MODELS
# ========================================

class UserBase(BaseModel):
    """Base user fields shared across models"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)


class User(UserBase):
    """Full user model with id"""
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30
            }
        }


class UserCreate(UserBase):
    """Model for creating a new user"""
    pass


class UserUpdate(BaseModel):
    """
    Model for partial user updates.

    KEY FEATURE: All fields are Optional, allowing partial updates.
    This is the Pydantic model that makes PATCH work properly.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "age": 25
            }
        }


# ========================================
# 2. IN-MEMORY DATABASE (SIMULATION)
# ========================================

# Simulated database
fake_db: dict[int, User] = {
    1: User(id=1, name="John Doe", email="john@example.com", age=30),
    2: User(id=2, name="Jane Smith", email="jane@example.com", age=25),
    3: User(id=3, name="Bob Johnson", email="bob@example.com", age=35),
}
next_id = 4


# ========================================
# 3. FASTAPI APP WITH PATCH ENDPOINT
# ========================================

app = FastAPI(title="User Management API", version="1.0.0")


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a user by ID"""
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return fake_db[user_id]


@app.get("/users", response_model=list[User])
async def list_users():
    """List all users"""
    return list(fake_db.values())


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """Create a new user"""
    global next_id

    new_user = User(id=next_id, **user_data.model_dump())
    fake_db[next_id] = new_user
    next_id += 1

    return new_user


@app.patch("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    PATCH endpoint for partial user updates.

    KEY FEATURES:
    1. Only updates fields that are provided in the request
    2. Ignores fields that are None (not provided)
    3. Preserves existing values for fields not in the request

    BEHAVIOR:
    - If request body is {"name": "New Name"}, only name is updated
    - If request body is {"age": 40}, only age is updated
    - If request body is {"name": "New", "email": "new@email.com"}, both are updated
    - Unprovided fields remain unchanged
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


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    del fake_db[user_id]
    return None


# ========================================
# 4. USAGE EXAMPLES
# ========================================

if __name__ == "__main__":
    import uvicorn

    print("""
    ========================================
    FastAPI PATCH Endpoint - Usage Examples
    ========================================

    Example 1: Update only the name
    curl -X PATCH http://localhost:8000/users/1 \\
      -H "Content-Type: application/json" \\
      -d '{"name": "John Updated"}'

    Example 2: Update only the age
    curl -X PATCH http://localhost:8000/users/1 \\
      -H "Content-Type: application/json" \\
      -d '{"age": 35}'

    Example 3: Update multiple fields
    curl -X PATCH http://localhost:8000/users/1 \\
      -H "Content-Type: application/json" \\
      -d '{"name": "John Updated", "email": "john.updated@example.com"}'

    Example 4: Empty update (no changes)
    curl -X PATCH http://localhost:8000/users/1 \\
      -H "Content-Type: application/json" \\
      -d '{}'

    ========================================

    Starting server on http://localhost:8000
    """)

    uvicorn.run(app, host="0.0.0.0", port=8000)
