# Database Integration Patterns

Comprehensive guide for integrating different databases with FastAPI.

## Table of Contents

1. [PostgreSQL with SQLAlchemy](#postgresql-with-sqlalchemy)
2. [MySQL with SQLAlchemy](#mysql-with-sqlalchemy)
3. [SQLite with SQLAlchemy](#sqlite-with-sqlalchemy)
4. [MongoDB with Beanie](#mongodb-with-beanie)
5. [Database Session Management](#database-session-management)
6. [Async vs Sync Database Operations](#async-vs-sync-database-operations)

---

## PostgreSQL with SQLAlchemy

### Installation

```bash
pip install sqlalchemy psycopg2-binary alembic
```

### Database Configuration

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Async PostgreSQL

```bash
pip install sqlalchemy[asyncio] asyncpg
```

```python
# app/core/database.py (Async version)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Model Definition

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### CRUD Operations

```python
# app/services/user_service.py
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate


# Sync version
def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, email: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.email = email
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Async version
async def create_user_async(db: AsyncSession, user: UserCreate):
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_async(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


async def get_users_async(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
```

### Endpoint Usage

```python
# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import user_service
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

### Database Migrations with Alembic

```bash
# Initialize Alembic
alembic init alembic

# Configure alembic.ini
# sqlalchemy.url = postgresql://user:password@localhost/dbname

# Generate migration
alembic revision --autogenerate -m "Create users table"

# Apply migration
alembic upgrade head
```

---

## MySQL with SQLAlchemy

### Installation

```bash
pip install sqlalchemy pymysql alembic
```

### Database Configuration

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

The models, CRUD operations, and migrations work identically to PostgreSQL. Only the connection string changes.

---

## SQLite with SQLAlchemy

### Installation

```bash
pip install sqlalchemy alembic
```

### Database Configuration

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# SQLite requires check_same_thread=False for FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
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

### Create Tables on Startup

```python
# app/main.py
from app.core.database import engine, Base
from app.models import user  # Import all models

# Create tables
Base.metadata.create_all(bind=engine)
```

---

## MongoDB with Beanie

### Installation

```bash
pip install motor beanie
```

### Database Configuration

```python
# app/core/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.core.config import settings


async def init_db():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    database = client.get_database("dbname")

    await init_beanie(
        database=database,
        document_models=[User]  # Add all document models
    )
```

### Model Definition

```python
# app/models/user.py
from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional


class User(Document):
    email: EmailStr = Field(..., unique=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "users"  # Collection name
        indexes = ["email"]
```

### CRUD Operations

```python
# app/services/user_service.py
from app.models.user import User
from app.schemas.user import UserCreate
from typing import List


async def create_user(user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        hashed_password=user.password
    )
    await db_user.insert()
    return db_user


async def get_user(user_id: str) -> Optional[User]:
    return await User.get(user_id)


async def get_user_by_email(email: str) -> Optional[User]:
    return await User.find_one(User.email == email)


async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    return await User.find_all().skip(skip).limit(limit).to_list()


async def update_user(user_id: str, email: str) -> Optional[User]:
    user = await User.get(user_id)
    if user:
        user.email = email
        user.updated_at = datetime.utcnow()
        await user.save()
    return user


async def delete_user(user_id: str) -> bool:
    user = await User.get(user_id)
    if user:
        await user.delete()
        return True
    return False
```

### Endpoint Usage

```python
# app/api/endpoints/users.py
from fastapi import APIRouter, HTTPException
from app.services import user_service
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    return await user_service.create_user(user)


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str):
    db_user = await user_service.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

### Application Startup

```python
# app/main.py
from fastapi import FastAPI
from app.core.database import init_db

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()
```

---

## Database Session Management

### Dependency Injection Pattern

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db


@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    # db session automatically managed
    items = db.query(Item).all()
    return items
```

### Context Manager Pattern

```python
from app.core.database import SessionLocal


def some_function():
    with SessionLocal() as db:
        # db session automatically closed
        return db.query(User).all()
```

---

## Async vs Sync Database Operations

### When to Use Async

- High concurrency requirements
- I/O-bound operations
- Microservices with multiple database calls
- Real-time applications

### When to Use Sync

- Simple CRUD applications
- Low traffic applications
- When using libraries without async support
- Simpler debugging and testing

### Example Comparison

**Sync:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

**Async:**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()
```

---

## Best Practices

1. **Use dependency injection** for database sessions
2. **Always close sessions** (use context managers or Depends)
3. **Use migrations** for schema changes (Alembic for SQL)
4. **Index frequently queried fields**
5. **Use async** for high-concurrency applications
6. **Validate data** with Pydantic schemas before database operations
7. **Handle database errors** with try-except blocks
8. **Use connection pooling** for production (configured in engine)
9. **Separate models and schemas** (SQLAlchemy models vs Pydantic schemas)
10. **Use environment variables** for database credentials
