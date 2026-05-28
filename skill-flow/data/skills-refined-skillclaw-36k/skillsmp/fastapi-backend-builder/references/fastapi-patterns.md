# FastAPI Common Patterns

This document provides common patterns and examples for FastAPI development.

## Router Patterns

### Basic Router

```python
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[ItemResponse])
async def get_items(skip: int = 0, limit: int = 100):
    """Retrieve a list of items."""
    return items[skip : skip + limit]

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Retrieve a single item by ID."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    new_item = create_item_in_db(item)
    return new_item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = update_item_in_db(item_id, item)
    return updated_item

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_item_from_db(item_id)
```

### Router with Dependencies

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the current user's profile."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the current user's profile."""
    user_service = UserService(db)
    updated_user = user_service.update(current_user.id, user_update)
    return updated_user
```

## Service Layer Pattern

### Basic Service

```python
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
    
    def get_by_id(self, user_id: int) -> User:
        """Get user by ID."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Email already registered")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = self.repository.create({
            **user_data.dict(exclude={"password"}),
            "hashed_password": hashed_password
        })
        return user
    
    def update(self, user_id: int, user_data: UserUpdate) -> User:
        """Update a user."""
        user = self.get_by_id(user_id)
        
        # Update fields
        update_data = user_data.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        updated_user = self.repository.update(user_id, update_data)
        return updated_user
    
    def delete(self, user_id: int) -> None:
        """Delete a user."""
        user = self.get_by_id(user_id)
        self.repository.delete(user_id)
```

## Repository Pattern

### Basic Repository

```python
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create(self, user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: int, user_data: Dict[str, Any]) -> User:
        """Update a user."""
        user = self.get_by_id(user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> None:
        """Delete a user."""
        user = self.get_by_id(user_id)
        self.db.delete(user)
        self.db.commit()
```

## Database Models (SQLAlchemy)

### Basic Model

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="items")
```

## Pydantic Schemas

### Request/Response Schemas

```python
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    is_active: bool = True

# Creation schema (includes password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Update schema (all fields optional)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

# Response schema (includes ID, no password)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Detailed response with relationships
class UserDetailResponse(UserResponse):
    items: List["ItemResponse"] = []

class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class ItemResponse(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
```

## Authentication Patterns

### JWT Authentication

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Login Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login to get access token."""
    user_service = UserService(db)
    user = user_service.authenticate(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    user_service = UserService(db)
    user = user_service.create(user_data)
    return user
```

## Error Handling Patterns

### Custom Exceptions

```python
class AppException(Exception):
    """Base app exception."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(AppException):
    """Resource not found exception."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class UnauthorizedException(AppException):
    """Unauthorized exception."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)

class ForbiddenException(AppException):
    """Forbidden exception."""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)

class ConflictException(AppException):
    """Conflict exception."""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, 409)
```

### Global Exception Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )
```

## Main Application Setup

### Complete main.py Example

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, items, auth
from .config import settings

app = FastAPI(
    title="My API",
    description="A comprehensive API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Startup event
@app.on_event("startup")
async def startup_event():
    print("Application starting up...")
    # Initialize database, create tables, etc.

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutting down...")
    # Close connections, cleanup, etc.
```

## Configuration Pattern

### Using Pydantic Settings

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "My API"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

## Database Connection Pattern

### Database Setup

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
