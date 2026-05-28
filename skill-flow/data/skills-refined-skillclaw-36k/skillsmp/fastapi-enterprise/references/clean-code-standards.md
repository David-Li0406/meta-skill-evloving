# Clean Code Standards

DDD principles, no duplication, helpers, and readable code.

## Domain-Driven Design (DDD)

Organize by business domain, not technical layers.

### ✅ Good Structure

```
services/
├── user/
│   ├── profile.py
│   ├── authentication.py
│   └── role.py
├── product/
│   ├── category.py
│   └── inventory.py
└── order/
    ├── cart.py
    └── checkout.py
```

### ❌ Bad Structure

```
services/
├── crud_service.py
├── helper_service.py
└── business_logic.py
```

## No Code Duplication (DRY)

Use `helpers/` for shared code.

### ❌ Bad (Duplicated)

```python
# In multiple files
def validate_email(email: str) -> bool:
    return "@" in email and "." in email

def format_phone(phone: str) -> str:
    return phone.replace(" ", "").replace("-", "")
```

### ✅ Good (Helper)

```python
# helpers/validation.py
def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number."""
    clean = phone.replace(" ", "").replace("-", "").replace("+", "")
    return clean.isdigit() and 10 <= len(clean) <= 15
```

```python
# helpers/formatting.py
def format_phone(phone: str) -> str:
    """Format phone number to clean format."""
    return phone.replace(" ", "").replace("-", "")

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency."""
    return f"{currency} {amount:,.2f}"
```

**Usage**:
```python
from helpers.validation import validate_email
from helpers.formatting import format_phone

if not validate_email(email):
    raise ValueError("Invalid email")

clean_phone = format_phone(phone_input)
```

## Helpers Organization

```
helpers/
├── __init__.py
├── validation.py      # Input validation
├── formatting.py      # Data formatting
├── security.py        # Password hashing, token generation
├── pagination.py      # Pagination logic
└── datetime_utils.py  # Date/time helpers
```

## Enum Organization

Business constants in `enums/`.

```python
# enums/user_status.py
from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"
```

```python
# enums/product_category.py
from enum import Enum

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
```

**Usage**:
```python
from enums.user_status import UserStatus

user.status = UserStatus.ACTIVE
```

## Readable Code

Write for non-developers to understand business logic.

### ❌ Bad

```python
def p(u, d):
    r = db.execute(select(U).where(U.id == u)).scalar()
    if r:
        for k, v in d.items():
            setattr(r, k, v)
        db.commit()
    return r
```

### ✅ Good

```python
async def update_user_profile(
    db: AsyncSession,
    user_id: int,
    updates: dict,
) -> Optional[User]:
    """
    Update user profile with provided data.
    
    Args:
        db: Database session
        user_id: ID of user to update
        updates: Dictionary of fields to update
    
    Returns:
        Updated user or None if not found
    """
    # Find user
    user_query = select(User).where(User.id == user_id)
    result = await db.execute(user_query)
    user = result.scalar_one_or_none()
    
    if not user:
        logger.warning("User not found", user_id=user_id)
        return None
    
    # Apply updates
    for field_name, new_value in updates.items():
        setattr(user, field_name, new_value)
    
    # Save to database
    await db.commit()
    await db.refresh(user)
    
    logger.info("User profile updated", user_id=user_id, fields=list(updates.keys()))
    return user
```

## Schema Organization

Group schemas by domain and purpose.

```
schemas/
├── user/
│   ├── __init__.py
│   ├── profile.py      # UserProfileCreate, UserProfileResponse
│   └── authentication.py  # LoginRequest, TokenResponse
└── product/
    └── category.py     # CategoryCreate, CategoryResponse
```

```python
# schemas/user/profile.py
from pydantic import BaseModel, EmailStr

class UserProfileCreate(BaseModel):
    """Schema for creating user profile."""
    email: EmailStr
    name: str
    phone: Optional[str] = None

class UserProfileResponse(BaseModel):
    """Schema for user profile response."""
    id: int
    email: str
    name: str
    phone: Optional[str]
    created_at: datetime
    
    model_config = {"from_attributes": True}
```

## Service Layer Pattern

Keep business logic in services, not endpoints.

### ❌ Bad (Logic in endpoint)

```python
@router.post("/users")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Business logic in endpoint
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Email already exists")
    
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    return user
```

### ✅ Good (Logic in service)

```python
# services/user/profile.py
class UserProfileService:
    async def create(self, db: AsyncSession, data: UserCreate) -> User:
        """Create new user with validation."""
        # Check if email exists
        existing = await self.get_by_email(db, data.email)
        if existing:
            raise ValueError("Email already exists")
        
        # Create user
        user = User(**data.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        logger.info("User created", user_id=user.id, email=user.email)
        return user

user_service = UserProfileService()
```

```python
# Endpoint uses service
@router.post("/users", status_code=201)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        user = await user_service.create(db, data)
        return user
    except ValueError as e:
        raise HTTPException(400, str(e))
```

## Type Hints Everywhere

```python
# ✅ Good
async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    ...

def calculate_total(items: list[dict], tax_rate: float) -> float:
    ...

# ❌ Bad
async def get_user(db, id):
    ...
```

## Documentation

```python
def complex_business_logic(
    user_id: int,
    options: dict,
) -> dict:
    """
    Perform complex business operation.
    
    This function handles [business requirement explanation]
    that even non-technical stakeholders can understand.
    
    Args:
        user_id: ID of the user performing the action
        options: Configuration options including:
            - threshold: Minimum value (default: 100)
            - notify: Whether to send notifications (default: True)
    
    Returns:
        Dictionary containing:
            - success: Whether operation succeeded
            - result: Operation result data
            - notifications_sent: Number of notifications sent
    
    Raises:
        ValueError: If user_id is invalid
        PermissionError: If user lacks required permissions
    """
    ...
```

## Testing Standards

```python
# tests/services/test_user_profile.py
import pytest
from services.user.profile import user_service

@pytest.mark.asyncio
async def test_create_user_success(db_session):
    """Test successful user creation."""
    data = UserCreate(email="test@example.com", name="Test User")
    
    user = await user_service.create(db_session, data)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"

@pytest.mark.asyncio
async def test_create_user_duplicate_email(db_session):
    """Test that duplicate email raises error."""
    data = UserCreate(email="test@example.com", name="Test User")
    
    # Create first user
    await user_service.create(db_session, data)
    
    # Attempt duplicate
    with pytest.raises(ValueError, match="Email already exists"):
        await user_service.create(db_session, data)
```

## Code Review Checklist

- [ ] No duplicated code (check helpers)
- [ ] Business logic in services, not endpoints
- [ ] Type hints on all functions
- [ ] Docstrings on complex functions
- [ ] Enums for business constants
- [ ] Schemas organized by domain
- [ ] Helpers organized by category
- [ ] Code readable by non-developers
- [ ] Tests for business logic
- [ ] DDD structure (domain-based folders)

## Next Steps

- [Project Structure](project-structure.md) - File organization
- [Error Handling Workflow](error-handling-workflow.md) - Fixing code issues
- [Database Patterns](database-patterns.md) - Model best practices
