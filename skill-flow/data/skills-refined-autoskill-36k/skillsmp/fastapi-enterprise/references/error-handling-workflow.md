# Error Handling Workflow

Systematic approach to detecting and fixing errors in FastAPI development.

## Workflow Overview

```
Code Change → Check Problems Panel → Categorize Error → Apply Fix → Re-validate → Commit
```

## Step 1: Check Problems Panel

After making code changes, check VS Code Problems panel (Ctrl+Shift+M):

- **Syntax errors**: Missing colons, parentheses
- **Type errors**: mypy/Pylance type checking
- **Import errors**: Missing imports, circular imports
- **Lint errors**: Code style issues

## Step 2: Categorize Errors

### Syntax Errors

**Common patterns**:
- Missing `:` after `def`, `if`, `for`, `class`
- Unclosed `(`, `[`, `{`, `"`, `'`
- Indentation errors
- Invalid Python syntax

**Fix**: Check the exact line number, verify syntax.

### Type Errors

**Common patterns**:
```python
# Error: Argument of type "None" cannot be assigned to parameter "db" of type "AsyncSession"
async def get_user(db: AsyncSession | None):  # ← Wrong
    result = await db.execute(...)  # ← db might be None!

# Fix:
async def get_user(db: AsyncSession):  # ← Always require non-None
    result = await db.execute(...)
```

```python
# Error: "list[User]" is not compatible with return type "User"
async def get_users(db: AsyncSession) -> User:  # ← Wrong type
    result = await db.execute(select(User))
    return result.scalars().all()  # ← Returns list

# Fix:
async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Import Errors

**Circular imports**:
```python
# models/user.py
from models.post import Post  # ← Imports Post

# models/post.py
from models.user import User  # ← Imports User (circular!)

# Fix: Use string annotation
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.post import Post

class User(Base):
    posts: Mapped[list["Post"]] = relationship(...)  # ← String annotation
```

**Missing imports**:
```python
# Error: Name 'AsyncSession' is not defined

# Fix:
from sqlalchemy.ext.asyncio import AsyncSession
```

### FastAPI-Specific Errors

**Missing Depends**:
```python
# Error: Cannot use AsyncSession directly as parameter
@router.get("/users")
async def get_users(db: AsyncSession):  # ← Missing Depends

# Fix:
from fastapi import Depends
from core.db import get_db

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
```

**Response model mismatch**:
```python
# Error: Return type does not match response_model
@router.get("/users", response_model=UserResponse)
async def get_users(db: AsyncSession = Depends(get_db)):
    return await db.execute(select(User)).scalars().all()  # ← Returns list

# Fix:
@router.get("/users", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    ...
```

### Pydantic Errors

**ValidationError**:
```python
# Error: Field required
class UserCreate(BaseModel):
    email: str
    name: str  # ← Required field

data = UserCreate(email="test@example.com")  # ← Missing name

# Fix: Provide all required fields or make optional
class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None  # ← Now optional
```

**Config error**:
```python
# Old Pydantic v1
class UserResponse(BaseModel):
    class Config:
        from_attributes = True  # ← Old style

# Fix: Pydantic v2
class UserResponse(BaseModel):
    model_config = {"from_attributes": True}  # ← New style
```

### SQLAlchemy Errors

**Async/sync mismatch**:
```python
# Error: Cannot use sync methods with async engine
user = db.query(User).first()  # ← Sync method

# Fix:
stmt = select(User)
result = await db.execute(stmt)
user = result.scalar_one_or_none()
```

**Missing await**:
```python
# Error: Coroutine was never awaited
user = db.execute(select(User))  # ← Missing await

# Fix:
user = await db.execute(select(User))
```

## Step 3: Apply Fixes

### Systematic Approach

1. **Read error message carefully**: Line number, exact error
2. **Check documentation**: FastAPI, Pydantic, SQLAlchemy docs
3. **Verify types**: Use type hints, check return types
4. **Test incrementally**: Fix one error, test, then next
5. **Log for debugging**: Add logger.debug() to trace execution

### Example Debugging Session

```python
# Error: HTTPException not recognized
@router.post("/users")
async def create_user(data: UserCreate):
    if not data.email:
        raise HTTPException(400, "Email required")  # ← Error here

# Step 1: Check import
from fastapi import HTTPException  # ← Add import

# Step 2: Verify syntax
raise HTTPException(status_code=400, detail="Email required")  # ← Correct syntax

# Step 3: Test
# curl -X POST http://localhost:8000/api/v1/users -d '{"name":"Test"}'
# Should return 400 error

# Step 4: Add logging
logger.debug("Validating user data", email=data.email)
if not data.email:
    logger.warning("Email validation failed")
    raise HTTPException(status_code=400, detail="Email required")
```

## Step 4: Re-validate

After fixing, check:

1. **Problems panel clear**: No remaining errors
2. **Code runs**: `python app.py` starts without errors
3. **Endpoint works**: Test with curl/Postman/Swagger
4. **Tests pass**: `pytest` if tests exist

## Step 5: Commit

Once validated:

```bash
git add .
git commit -m "fix: resolve type errors in user endpoint"
```

## Common FastAPI Error Patterns

### 1. Dependency Injection

```python
# ❌ Wrong
@router.get("/users")
async def get_users(db = get_db()):
    ...

# ✅ Correct
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    ...
```

### 2. Response Models

```python
# ❌ Wrong: List endpoint returns single model
@router.get("/users", response_model=UserResponse)
async def get_users():
    return [user1, user2, user3]  # ← List!

# ✅ Correct
@router.get("/users", response_model=list[UserResponse])
async def get_users():
    return [user1, user2, user3]
```

### 3. Async/Await

```python
# ❌ Wrong: Missing await
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = db.execute(select(User))  # ← Returns coroutine
    return users.scalars().all()

# ✅ Correct
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))  # ← Await here
    return result.scalars().all()
```

### 4. Pydantic Validation

```python
# ❌ Wrong: Modifying immutable Pydantic model
user_data = UserCreate(email="test@example.com")
user_data.email = "new@example.com"  # ← Error: frozen

# ✅ Correct: Create new instance
user_data = UserCreate(email="test@example.com")
updated_data = user_data.model_copy(update={"email": "new@example.com"})
```

## Prevention Strategies

1. **Use type hints**: Catch errors before runtime
2. **Enable strict mypy**: Add `mypy.ini` with strict settings
3. **Pre-commit hooks**: Run linters before commit
4. **Write tests**: Catch errors early
5. **Code review**: Second pair of eyes

## Debugging Tools

### 1. Print Debugging (Development)

```python
from core.logging import get_logger

logger = get_logger(__name__)

@router.post("/users")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.debug("Received data", data=data.model_dump())
    
    user = User(**data.model_dump())
    logger.debug("Created user object", user_id=user.id)
    
    db.add(user)
    await db.commit()
    logger.debug("Committed to database")
    
    return user
```

### 2. Interactive Debugging

Use VS Code debugger:
- Set breakpoint in endpoint
- Run in debug mode (F5)
- Inspect variables, step through code

### 3. API Testing

```bash
# Test endpoint with curl
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test"}'

# Check logs
# Look for structured log output with conversation_id
```

## Summary Checklist

- [ ] Check Problems panel after code changes
- [ ] Categorize error type (syntax, type, import, etc.)
- [ ] Apply appropriate fix
- [ ] Re-validate (no errors, code runs, tests pass)
- [ ] Commit changes
- [ ] Use logging for debugging
- [ ] Write tests to prevent regression

## Next Steps

- [Logging Patterns](logging-patterns.md) - Debugging with logs
- [Clean Code Standards](clean-code-standards.md) - Prevent errors
- [Database Patterns](database-patterns.md) - SQLAlchemy error patterns
