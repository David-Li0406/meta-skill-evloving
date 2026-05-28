# Database Patterns with Async SQLAlchemy

Async database operations with SQLAlchemy and PostgreSQL.

## Core Setup (core/db.py)

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

# Async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before using
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    """Base for all models."""
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## Creating Models

```python
# models/user.py
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
```

## CRUD Operations

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Create
async def create_user(db: AsyncSession, email: str, name: str):
    user = User(email=email, name=name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Read
async def get_user(db: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Update
async def update_user(db: AsyncSession, user_id: int, name: str):
    user = await get_user(db, user_id)
    if user:
        user.name = name
        await db.commit()
        await db.refresh(user)
    return user

# Delete
async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user is not None
```

## PostgreSQL-Specific Features

### JSONB Columns

```python
from sqlalchemy.dialects.postgresql import JSONB

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    metadata: Mapped[dict] = mapped_column(JSONB, default={})
```

**Fallback for other DBs**:
```python
from sqlalchemy import JSON
metadata: Mapped[dict] = mapped_column(JSON, default={})
```

### Array Columns

```python
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String

class User(Base):
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])
```

## Relationships

```python
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
```

## Transaction Management

```python
async def transfer_funds(db: AsyncSession, from_id: int, to_id: int, amount: float):
    """Example of transaction with rollback on error."""
    try:
        # Deduct from sender
        sender = await get_account(db, from_id)
        sender.balance -= amount
        
        # Add to receiver
        receiver = await get_account(db, to_id)
        receiver.balance += amount
        
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise
```

## Next Steps

- [Alembic Setup](alembic-setup.md) - Database migrations
- [Clean Code Standards](clean-code-standards.md) - Model organization
