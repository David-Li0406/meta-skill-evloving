---
name: api-designer
description: Design and implement REST API endpoints for NutriProfile. Use this skill when creating new endpoints, modifying API schemas, working with Pydantic models, or ensuring OpenAPI compliance. Follows FastAPI best practices.
allowed-tools: Read,Write,Edit,Grep,Glob,Bash
---

# NutriProfile API Designer Skill

You are a REST API design expert for the NutriProfile application. This skill helps you create well-structured, documented, and secure API endpoints using FastAPI and Pydantic.

## API Architecture

### Base URL
- **Production**: `https://nutriprofile-api.fly.dev/api/v1`
- **Development**: `http://localhost:8000/api/v1`

### API Structure
```
backend/app/api/v1/
├── __init__.py
├── auth.py          # Authentication (login, register, refresh)
├── users.py         # User management
├── profiles.py      # Nutritional profiles
├── vision.py        # Food photo analysis
├── recipes.py       # Recipe generation
├── tracking.py      # Activity & weight tracking
├── dashboard.py     # Statistics & achievements
├── coaching.py      # AI coaching
├── subscriptions.py # Subscription management
├── webhooks.py      # Lemon Squeezy webhooks
└── health.py        # Health checks
```

## Endpoint Design Patterns

### Standard CRUD Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/recipes", tags=["recipes"])

# LIST
@router.get("/", response_model=list[RecipeResponse])
async def list_recipes(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all recipes for the current user."""
    recipes = await recipe_service.get_user_recipes(db, current_user.id, skip, limit)
    return recipes

# CREATE
@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe_data: RecipeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new recipe."""
    return await recipe_service.create(db, current_user.id, recipe_data)

# READ
@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific recipe by ID."""
    recipe = await recipe_service.get(db, recipe_id, current_user.id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    return recipe

# UPDATE
@router.patch("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a recipe."""
    recipe = await recipe_service.update(db, recipe_id, current_user.id, recipe_data)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    return recipe

# DELETE
@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    recipe_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a recipe."""
    success = await recipe_service.delete(db, recipe_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
```

## Pydantic Schemas

### Schema Design Patterns

```python
# backend/app/schemas/recipe.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# Base schema (shared fields)
class RecipeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    prep_time: int = Field(..., ge=0, le=480)  # minutes
    cook_time: int = Field(..., ge=0, le=480)
    servings: int = Field(..., ge=1, le=50)

# Create schema (input for POST)
class RecipeCreate(RecipeBase):
    ingredients: List[IngredientCreate]
    instructions: List[str] = Field(..., min_items=1)

    @validator('instructions')
    def validate_instructions(cls, v):
        if any(len(i) > 500 for i in v):
            raise ValueError('Each instruction must be under 500 characters')
        return v

# Update schema (input for PATCH)
class RecipeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    prep_time: Optional[int] = Field(None, ge=0, le=480)
    cook_time: Optional[int] = Field(None, ge=0, le=480)
    servings: Optional[int] = Field(None, ge=1, le=50)
    ingredients: Optional[List[IngredientCreate]] = None
    instructions: Optional[List[str]] = None

# Response schema (output)
class RecipeResponse(RecipeBase):
    id: int
    user_id: int
    ingredients: List[IngredientResponse]
    instructions: List[str]
    calories_per_serving: float
    protein_per_serving: float
    carbs_per_serving: float
    fat_per_serving: float
    confidence_score: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Pydantic v2

# Nested schema
class IngredientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    quantity: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=20)

class IngredientResponse(IngredientCreate):
    id: int
    calories: float
    protein: float
    carbs: float
    fat: float
```

## Authentication

### JWT Token Flow

```python
# backend/app/services/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Validate JWT token and return current user."""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = await db.get(User, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

### Protected Endpoints

```python
# All endpoints requiring authentication
@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user)
):
    return {"user_id": current_user.id}

# Optional authentication
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    if not credentials:
        return None
    # ... validate token
```

## Freemium Limits

### Checking Usage Limits

```python
from app.services.subscription import SubscriptionService

@router.post("/vision/analyze")
async def analyze_food(
    image_data: ImageUpload,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze food photo with tier limits."""
    subscription_service = SubscriptionService(db)

    # Check usage limit
    can_use = await subscription_service.check_limit(
        current_user.id,
        "vision_analyses"
    )

    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Daily analysis limit reached. Upgrade to Premium for unlimited analyses."
        )

    # Proceed with analysis
    result = await vision_agent.analyze(image_data)

    # Track usage
    await subscription_service.increment_usage(
        current_user.id,
        "vision_analyses"
    )

    return result
```

## Error Handling

### Standard Error Responses

```python
from fastapi import HTTPException, status

# 400 Bad Request - Invalid input
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid email format"
)

# 401 Unauthorized - Not authenticated
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token"
)

# 403 Forbidden - Not authorized
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have permission to access this resource"
)

# 404 Not Found - Resource doesn't exist
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Recipe not found"
)

# 422 Unprocessable Entity - Validation error (automatic with Pydantic)

# 429 Too Many Requests - Rate limit
raise HTTPException(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Rate limit exceeded. Try again later."
)
```

### Custom Exception Handler

```python
# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

## Response Formats

### Success Response
```json
{
  "id": 1,
  "name": "Bowl Méditerranéen",
  "calories_per_serving": 450,
  "created_at": "2026-01-15T10:00:00Z"
}
```

### List Response with Pagination
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

### Error Response
```json
{
  "detail": "Recipe not found"
}
```

### Validation Error Response
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## API Documentation

### OpenAPI Tags

```python
# backend/app/main.py
app = FastAPI(
    title="NutriProfile API",
    description="API for nutritional profiling and AI-powered food analysis",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication operations"},
        {"name": "users", "description": "User management"},
        {"name": "profiles", "description": "Nutritional profiles"},
        {"name": "vision", "description": "Food photo analysis"},
        {"name": "recipes", "description": "AI recipe generation"},
        {"name": "tracking", "description": "Activity and weight tracking"},
        {"name": "coaching", "description": "AI coaching"},
        {"name": "subscriptions", "description": "Subscription management"},
    ]
)
```

### Endpoint Documentation

```python
@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyze food photo",
    description="""
    Analyze a food photo using AI vision models.

    **Requires authentication.**

    **Tier limits:**
    - Free: 3 analyses/day
    - Premium: Unlimited
    - Pro: Unlimited

    Returns detected food items with nutritional estimates.
    """,
    responses={
        200: {"description": "Analysis completed successfully"},
        400: {"description": "Invalid image data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Daily limit reached"},
    }
)
async def analyze_food(...):
    ...
```

## Best Practices

1. **Always use Pydantic** for request/response validation
2. **Type hint everything** - FastAPI uses types for validation
3. **Use status codes correctly** - 201 for create, 204 for delete
4. **Document endpoints** - Include summaries and descriptions
5. **Handle errors gracefully** - Return meaningful error messages
6. **Check tier limits** - Before expensive operations
7. **Validate user ownership** - Don't leak other users' data
8. **Use async** - For database and external API calls

## Testing API Endpoints

```python
# tests/test_recipes.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_recipe(async_client: AsyncClient, auth_headers: dict):
    response = await async_client.post(
        "/api/v1/recipes",
        headers=auth_headers,
        json={
            "name": "Test Recipe",
            "prep_time": 15,
            "cook_time": 30,
            "servings": 4,
            "ingredients": [
                {"name": "poulet", "quantity": 500, "unit": "g"}
            ],
            "instructions": ["Step 1", "Step 2"]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Recipe"
    assert "id" in data
```
