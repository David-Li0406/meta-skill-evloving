# Common FastAPI Errors and Solutions

This document catalogs common errors encountered in FastAPI development and their solutions.

## Import Errors

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Cause**: FastAPI not installed or virtual environment not activated.

**Solution**:
```bash
pip install fastapi uvicorn
```

### Error: "ImportError: cannot import name 'X' from 'app.models'"

**Cause**: Circular import or module not properly initialized.

**Solution**:
1. Check for circular imports between modules
2. Ensure all `__init__.py` files exist
3. Use absolute imports instead of relative imports
4. Move imports inside functions if circular dependency exists

### Error: "ModuleNotFoundError: No module named 'app'"

**Cause**: Running from wrong directory or PYTHONPATH not set.

**Solution**:
```bash
# Run from project root
uvicorn app.main:app --reload

# Or set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## Pydantic Validation Errors

### Error: "validation error for UserCreate"

**Cause**: Request body doesn't match Pydantic schema.

**Solution**:
1. Check field types match schema
2. Ensure required fields are present
3. Validate email format for EmailStr
4. Check min/max length constraints

**Example Fix**:
```python
# Before (incorrect)
class UserCreate(BaseModel):
    email: str  # Should be EmailStr
    age: str    # Should be int

# After (correct)
class UserCreate(BaseModel):
    email: EmailStr
    age: int
```

### Error: "field required"

**Cause**: Required field missing from request.

**Solution**:
Make field optional or provide default:
```python
# Option 1: Make optional
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

# Option 2: Provide default
class UserCreate(BaseModel):
    is_active: bool = True
```

### Error: "value is not a valid email address"

**Cause**: Invalid email format.

**Solution**:
Use `EmailStr` from Pydantic and ensure input is valid email:
```python
from pydantic import EmailStr

class User(BaseModel):
    email: EmailStr  # Automatically validates email format
```

## Database Errors

### Error: "sqlalchemy.exc.OperationalError: no such table"

**Cause**: Database tables not created.

**Solution**:
```python
# In your main.py or startup script
from app.models.database import Base, engine

Base.metadata.create_all(bind=engine)
```

Or use Alembic migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Error: "sqlalchemy.exc.IntegrityError: UNIQUE constraint failed"

**Cause**: Trying to insert duplicate unique value.

**Solution**:
Check if record exists before creating:
```python
existing_user = db.query(User).filter(User.email == email).first()
if existing_user:
    raise HTTPException(status_code=409, detail="Email already registered")
```

### Error: "sqlalchemy.exc.InvalidRequestError: Object is already attached to session"

**Cause**: Trying to add object from different session.

**Solution**:
Use merge or create new object:
```python
# Option 1: Use merge
db.merge(user)
db.commit()

# Option 2: Create new object
new_user = User(**user_dict)
db.add(new_user)
db.commit()
```

### Error: "DetachedInstanceError: Instance is not bound to a Session"

**Cause**: Accessing lazy-loaded relationship after session closed.

**Solution**:
```python
# Option 1: Eager load relationships
user = db.query(User).options(joinedload(User.items)).first()

# Option 2: Access relationships before session closes
items = user.items  # Access within session context

# Option 3: Use expire_on_commit=False
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)
```

## Dependency Injection Errors

### Error: "FastAPI: Could not validate credentials"

**Cause**: JWT token invalid, expired, or missing.

**Solution**:
1. Check token is being sent in Authorization header
2. Verify token hasn't expired
3. Ensure SECRET_KEY matches between generation and validation
4. Check ALGORITHM is correct

```python
# Verify header format
Authorization: Bearer <token>

# Check token expiration
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
exp = payload.get("exp")
if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
    raise HTTPException(status_code=401, detail="Token expired")
```

### Error: "TypeError: get_db() takes 0 positional arguments but 1 was given"

**Cause**: Dependency function signature incorrect.

**Solution**:
Dependency functions should be generators:
```python
# Incorrect
def get_db():
    return SessionLocal()

# Correct
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Error: "RuntimeError: asyncio.run() cannot be called from a running event loop"

**Cause**: Mixing sync and async code incorrectly.

**Solution**:
```python
# If route is async, dependencies should be async
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # async implementation
    pass

# Use sync or async consistently
@router.get("/")
async def read_items(db: Session = Depends(get_db)):  # async route
    return await some_async_operation(db)
```

## Response Model Errors

### Error: "response_model field 'password' not found in response"

**Cause**: Response model includes fields not in returned object.

**Solution**:
Use `response_model_exclude` or separate response schema:
```python
# Option 1: Exclude fields
@router.get("/users/me", response_model=User, response_model_exclude={"password"})
async def read_user_me():
    pass

# Option 2: Separate response schema (preferred)
class UserResponse(BaseModel):
    id: int
    email: str
    # Exclude password field

@router.get("/users/me", response_model=UserResponse)
async def read_user_me():
    pass
```

### Error: "Unable to serialize response"

**Cause**: Response contains unserializable objects (like datetime, Decimal).

**Solution**:
```python
# Use Pydantic model with proper field types
from datetime import datetime
from decimal import Decimal

class ItemResponse(BaseModel):
    id: int
    created_at: datetime
    price: Decimal
    
    model_config = ConfigDict(from_attributes=True)
```

## CORS Errors

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Cause**: CORS middleware not configured or incorrectly configured.

**Solution**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Authentication Errors

### Error: "passlib.exc.UnknownHashError: hash could not be identified"

**Cause**: Password not hashed or wrong hash format.

**Solution**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password on creation
hashed_password = pwd_context.hash(plain_password)

# Verify password
is_valid = pwd_context.verify(plain_password, hashed_password)
```

### Error: "JWTError: Invalid token"

**Cause**: Token malformed, expired, or signed with different key.

**Solution**:
1. Verify token structure (header.payload.signature)
2. Check SECRET_KEY is consistent
3. Verify token hasn't expired
4. Ensure ALGORITHM matches

```python
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expired")
except jwt.JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")
```

## Async/Await Errors

### Error: "RuntimeWarning: coroutine was never awaited"

**Cause**: Calling async function without await.

**Solution**:
```python
# Incorrect
result = async_function()

# Correct
result = await async_function()
```

### Error: "TypeError: object NoneType can't be used in 'await' expression"

**Cause**: Awaiting a non-async function.

**Solution**:
```python
# Don't await sync functions
result = sync_function()  # No await

# Do await async functions
result = await async_function()  # With await
```

### Error: "SyntaxError: 'await' outside async function"

**Cause**: Using await in non-async function.

**Solution**:
```python
# Incorrect
def my_function():
    result = await async_call()

# Correct
async def my_function():
    result = await async_call()
```

## File Upload Errors

### Error: "AttributeError: 'str' object has no attribute 'read'"

**Cause**: Wrong type hint for file upload.

**Solution**:
```python
from fastapi import UploadFile, File

# Correct type hint
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename}
```

## Configuration Errors

### Error: "ValidationError in Settings"

**Cause**: Required environment variables not set.

**Solution**:
```python
# Create .env file
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key-here

# Or provide defaults
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "dev-secret-key"
    
    class Config:
        env_file = ".env"
```

### Error: "ModuleNotFoundError: No module named 'pydantic_settings'"

**Cause**: Using old Pydantic or wrong import.

**Solution**:
```bash
# Install pydantic-settings
pip install pydantic-settings

# Use correct import
from pydantic_settings import BaseSettings  # Pydantic v2
# or
from pydantic import BaseSettings  # Pydantic v1
```

## Router Registration Errors

### Error: "Route already exists"

**Cause**: Duplicate route path and method.

**Solution**:
```python
# Check for duplicate routes
@router.get("/items")  # First definition
async def get_items():
    pass

@router.get("/items")  # Duplicate - will error
async def get_all_items():
    pass

# Fix: Use different paths or methods
@router.get("/items")
async def get_items():
    pass

@router.get("/items/all")  # Different path
async def get_all_items():
    pass
```

### Error: "Router not included in app"

**Cause**: Forgot to include router in FastAPI app.

**Solution**:
```python
from fastapi import FastAPI
from .routers import users, items

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(items.router)
```

## Startup Errors

### Error: "Application startup failed"

**Cause**: Error in startup event handler.

**Solution**:
```python
@app.on_event("startup")
async def startup_event():
    try:
        # Your startup code
        print("Starting up...")
    except Exception as e:
        print(f"Startup error: {e}")
        # Don't raise - let app start even if startup tasks fail
```

## Testing Errors

### Error: "fixture 'client' not found"

**Cause**: Missing test client fixture.

**Solution**:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
```

## Common Error Resolution Workflow

1. **Read the full error message** - Don't skip the stack trace
2. **Identify the error type** - ImportError, ValidationError, etc.
3. **Check the line number** - Go to the exact location
4. **Review recent changes** - What did you change last?
5. **Check common causes** for that error type
6. **Test the fix** - Verify it works
7. **Add prevention** - Add validation, tests, etc.

## Prevention Strategies

### Type Hints Everywhere
```python
def get_user(user_id: int, db: Session) -> User:
    return db.query(User).filter(User.id == user_id).first()
```

### Proper Error Handling
```python
try:
    user = get_user(user_id, db)
    if not user:
        raise NotFoundException("User not found")
except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail="Database error")
```

### Input Validation
```python
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
```

### Comprehensive Logging
```python
import logging

logger = logging.getLogger(__name__)

try:
    user = create_user(user_data)
except Exception as e:
    logger.error(f"Error creating user: {e}", exc_info=True)
    raise
```

### Testing
```python
def test_create_user():
    response = client.post("/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 201
```
