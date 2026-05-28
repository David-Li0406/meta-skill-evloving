# Backend Implementation Workflow

## Purpose

This workflow guides implementation of backend services, business logic, and utilities that support API endpoints but aren't direct HTTP handlers.

Use this workflow when implementing:
- Service layer business logic
- Repository patterns and data access
- Utility functions and helpers
- Background jobs and workers
- Middleware and interceptors

## When to Use This vs implement-api.md

| Use implement-api.md | Use implement-backend.md |
|---------------------|-------------------------|
| HTTP endpoint handlers | Service layer business logic |
| Request/response handling | Repository/data access patterns |
| API route definitions | Utility functions |
| REST/GraphQL resolvers | Background workers |
| - | Middleware logic |

Often you'll use both: implement-api.md for endpoints, this workflow for the services they call.

## Prerequisites

1. **Design Documentation**
   - Architecture document with service layer design
   - API specification (if services support APIs)
   - Business rules documented

2. **Dependencies**
   - Database models defined (if data access needed)
   - Required libraries installed
   - Configuration available

## Phase 0: Start Task Tracking

Before beginning implementation, start task tracking:

```bash
# Start the task to update status and track progress
shark task start <task-id>

# Example:
shark task start T-E04-F02-001
```

This:
- Updates task status to "in-progress" in the database
- Tracks when implementation began
- Provides visibility to the team
- Enables accurate progress reporting

## Phase 1: Design Service Interface

### Step 1.1: Define Service Responsibilities

Before writing code, clarify what the service does:

```python
# Example: UserService responsibilities
"""
UserService handles user management business logic:
1. User creation with validation and uniqueness checks
2. User retrieval by various criteria
3. User updates with conflict detection
4. User deletion with cascade handling

NOT responsible for:
- HTTP request/response handling (API layer)
- Database schema (models layer)
- Authentication tokens (auth service)
"""
```

**Principle:** Single Responsibility. If service description has "and" in multiple places, consider splitting.

### Step 1.2: Define Method Signatures

Create interface with types, no implementation:

```python
# File: app/services/user_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import CreateUserRequest, UpdateUserRequest

class UserService:
    """Service layer for user management business logic."""

    def __init__(self, db: Session):
        """
        Initialize service with database session.

        Args:
            db: SQLAlchemy database session for data access
        """
        self.db = db

    async def create_user(self, request: CreateUserRequest) -> User:
        """
        Create a new user with validation.

        Args:
            request: User creation data (validated DTO)

        Returns:
            Created user entity

        Raises:
            ValueError: If email already exists or validation fails
        """
        raise NotImplementedError("Implemented in Phase 2")

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve user by ID.

        Args:
            user_id: UUID of user to retrieve

        Returns:
            User if found, None otherwise
        """
        raise NotImplementedError("Implemented in Phase 2")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        raise NotImplementedError("Implemented in Phase 2")

    async def update_user(self, user_id: str, request: UpdateUserRequest) -> User:
        """
        Update user information.

        Raises:
            ValueError: If user not found
        """
        raise NotImplementedError("Implemented in Phase 2")

    async def delete_user(self, user_id: str) -> None:
        """
        Delete user and cascade related entities.

        Raises:
            ValueError: If user not found
        """
        raise NotImplementedError("Implemented in Phase 2")
```

**Why stub first?**
- Clarifies service contract
- Enables test writing (TDD)
- Documents expected behavior
- Allows API layer to reference before implementation

## Phase 2: Test-Driven Implementation

Follow TDD workflow (see `test-driven-development` skill).

### Step 2.1: Write Test First (RED)

```python
# File: tests/unit/services/test_user_service.py
import pytest
from app.services.user_service import UserService
from app.schemas.user_schema import CreateUserRequest

def test_create_user_success(db_session):
    """Test successful user creation."""
    # Arrange
    service = UserService(db_session)
    request = CreateUserRequest(
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )

    # Act
    user = await service.create_user(request)

    # Assert
    assert user.email == "john@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.id is not None
    assert user.created_at is not None
```

**Run test - verify it fails:**
```bash
uv run pytest tests/unit/services/test_user_service.py::test_create_user_success -v
# Expected: FAILED (NotImplementedError or assertion failure)
```

### Step 2.2: Implement Minimal Code (GREEN)

```python
# File: app/services/user_service.py
from uuid import uuid4
from datetime import datetime

class UserService:
    # ... __init__ and other stubs ...

    async def create_user(self, request: CreateUserRequest) -> User:
        """Create a new user with validation."""

        # Check for duplicate email
        existing = self.db.query(User).filter(User.email == request.email).first()
        if existing:
            raise ValueError(f"User with email {request.email} already exists")

        # Create user entity
        user = User(
            id=uuid4(),
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Persist to database
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
```

**Run test - verify it passes:**
```bash
uv run pytest tests/unit/services/test_user_service.py::test_create_user_success -v
# Expected: PASSED
```

### Step 2.3: Test Error Cases

```python
def test_create_user_duplicate_email(db_session):
    """Test error when creating user with duplicate email."""
    service = UserService(db_session)
    request = CreateUserRequest(
        email="john@example.com",
        first_name="John",
        last_name="Doe"
    )

    # Create first user
    await service.create_user(request)

    # Attempt to create duplicate
    with pytest.raises(ValueError, match="already exists"):
        await service.create_user(request)

def test_create_user_empty_name(db_session):
    """Test validation of required fields."""
    service = UserService(db_session)
    request = CreateUserRequest(
        email="john@example.com",
        first_name="",  # Invalid
        last_name="Doe"
    )

    with pytest.raises(ValueError, match="first_name"):
        await service.create_user(request)
```

### Step 2.4: Refactor (REFACTOR)

Extract common patterns:

```python
class UserService:
    # ... existing methods ...

    def _check_user_exists(self, user_id: str) -> User:
        """
        Internal helper to verify user exists.

        Raises:
            ValueError: If user not found
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError(f"User {user_id} not found")
        return user

    async def update_user(self, user_id: str, request: UpdateUserRequest) -> User:
        """Update user information."""
        # Reuse helper
        user = self._check_user_exists(user_id)

        # Apply updates
        if request.first_name is not None:
            user.first_name = request.first_name
        if request.last_name is not None:
            user.last_name = request.last_name

        user.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        return user
```

**Re-run all tests:**
```bash
uv run pytest tests/unit/services/test_user_service.py -v
# All tests must still pass after refactoring
```

## Phase 3: Repository Pattern (Optional)

For complex data access, separate data layer from business logic:

### Step 3.1: Create Repository

```python
# File: app/repositories/user_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    """Data access layer for User entities."""

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Find all users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def save(self, user: User) -> User:
        """Save user to database."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Delete user from database."""
        self.db.delete(user)
        self.db.commit()
```

### Step 3.2: Use Repository in Service

```python
# File: app/services/user_service.py
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)  # Use repository for data access

    async def create_user(self, request: CreateUserRequest) -> User:
        """Create a new user with validation."""
        # Check duplicate via repository
        existing = self.repository.find_by_email(request.email)
        if existing:
            raise ValueError(f"User with email {request.email} already exists")

        # Create entity (business logic)
        user = User(
            id=uuid4(),
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            created_at=datetime.utcnow()
        )

        # Persist via repository
        return self.repository.save(user)
```

**Benefits:**
- Service focuses on business logic
- Repository handles data access
- Easier to mock in tests
- Database changes isolated to repository

## Phase 4: Error Handling

Follow `../context/error-handling.md` patterns.

### Step 4.1: Define Service Exceptions

```python
# File: app/services/exceptions.py
class ServiceException(Exception):
    """Base exception for service layer errors."""
    pass

class EntityNotFoundError(ServiceException):
    """Raised when entity not found."""
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} {entity_id} not found")

class DuplicateEntityError(ServiceException):
    """Raised when entity already exists."""
    def __init__(self, entity_type: str, field: str, value: str):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} with {field}={value} already exists")

class ValidationError(ServiceException):
    """Raised when validation fails."""
    pass
```

### Step 4.2: Use Service Exceptions

```python
from app.services.exceptions import EntityNotFoundError, DuplicateEntityError

class UserService:
    async def create_user(self, request: CreateUserRequest) -> User:
        """Create a new user with validation."""
        existing = self.repository.find_by_email(request.email)
        if existing:
            raise DuplicateEntityError("User", "email", request.email)

        # ... create user ...

    async def get_user_by_id(self, user_id: str) -> User:
        """Retrieve user by ID."""
        user = self.repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", user_id)
        return user
```

### Step 4.3: Handle in API Layer

```python
# File: app/api/v1/users.py
from fastapi import HTTPException, status
from app.services.exceptions import EntityNotFoundError, DuplicateEntityError

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    """Create a new user."""
    service = UserService(db)

    try:
        user = await service.create_user(request)
        return UserResponse.from_orm(user)
    except DuplicateEntityError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Phase 5: Validation Gates

### Gate 1: Linting
```bash
uv run flake8 app/services/ app/repositories/
uv run black --check app/services/ app/repositories/
```

### Gate 2: Type Checking
```bash
uv run mypy app/services/ app/repositories/
```

### Gate 3: Unit Tests
```bash
uv run pytest tests/unit/services/ -v
uv run pytest tests/unit/repositories/ -v
```

### Gate 4: Coverage
```bash
uv run pytest tests/unit/services/ --cov=app/services --cov-report=term-missing
# Target: >= 90% for service layer
```

**All gates must pass.**

## Phase 6: Documentation

### Document Service Layer

```markdown
# File: /docs/plan/{epic}/{feature}/IMPLEMENTATION.md

## Service Layer

### UserService
**Purpose:** User management business logic

**Methods:**
- `create_user(request)` - Create user with duplicate email check
- `get_user_by_id(user_id)` - Retrieve user by ID
- `update_user(user_id, request)` - Update user information
- `delete_user(user_id)` - Delete user with cascade

**Business Rules:**
- Email must be unique
- Names must be non-empty
- Updates use optimistic locking (updated_at check)

**Error Handling:**
- DuplicateEntityError - Email already exists
- EntityNotFoundError - User not found
- ValidationError - Invalid input

**Tests:**
- Unit tests: 18/18 passed
- Coverage: 94%
```

## Common Patterns

### Pagination

```python
from typing import List, Tuple

class UserService:
    async def list_users(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[User], int]:
        """
        List users with pagination.

        Returns:
            Tuple of (users, total_count)
        """
        users = self.repository.find_all(skip=skip, limit=limit)
        total = self.db.query(User).count()
        return users, total
```

### Filtering

```python
from typing import Optional, Dict, Any

class UserService:
    async def search_users(self, filters: Dict[str, Any]) -> List[User]:
        """Search users with dynamic filters."""
        query = self.db.query(User)

        if 'email' in filters:
            query = query.filter(User.email.contains(filters['email']))

        if 'status' in filters:
            query = query.filter(User.status == filters['status'])

        return query.all()
```

### Transactions

```python
from sqlalchemy.exc import IntegrityError

class UserService:
    async def create_user_with_profile(
        self,
        user_request: CreateUserRequest,
        profile_request: CreateProfileRequest
    ) -> User:
        """Create user and profile in single transaction."""
        try:
            # Both operations in same session = same transaction
            user = await self.create_user(user_request)

            profile = Profile(
                user_id=user.id,
                bio=profile_request.bio
            )
            self.db.add(profile)
            self.db.commit()

            return user
        except IntegrityError:
            self.db.rollback()
            raise
```

## Completion Checklist

- [ ] Service interface defined with type signatures
- [ ] Method signatures documented with docstrings
- [ ] TDD followed (tests written first)
- [ ] All methods implemented
- [ ] Repository pattern used (if applicable)
- [ ] Service exceptions defined
- [ ] Error handling comprehensive
- [ ] Unit tests passing (90%+ coverage)
- [ ] All validation gates passed
- [ ] Service layer documented
- [ ] **Task completed:** `shark task complete <task-id>`

**Final Step:** Mark the task as complete:
```bash
shark task complete T-E04-F02-001
```

This updates the task status to "completed" and records completion time in the database.

## Common Issues

| Issue | Solution |
|-------|----------|
| Tests fail after refactoring | Refactor broke behavior - revert and refactor smaller |
| Service has too many methods | Split into multiple services (SRP) |
| Hard to test | Too many dependencies - use dependency injection |
| Duplicate code across services | Extract shared logic to utility module |
| Database errors | Check transaction boundaries, use rollback |

## Reference

- Test-driven development: `../../test-driven-development/SKILL.md`
- Error handling: `../context/error-handling.md`
- Testing requirements: `../context/testing-requirements.md`
- Coding standards: `../context/coding-standards.md`

---

**Remember:** Service layer is where business logic lives. Keep it pure, testable, and separate from HTTP and database concerns.
