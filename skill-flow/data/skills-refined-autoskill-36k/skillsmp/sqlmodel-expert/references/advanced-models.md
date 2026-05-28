# Advanced SQLModel Patterns

Comprehensive guide on SQLModel patterns for Python applications.

## Table of Contents

1. Model Definition Patterns
2. Relationships
3. Inheritance
4. Composite Keys and Constraints
5. Custom Field Types
6. Index Strategies

---

## 1. Model Definition Patterns

### Separate Read/Write Models

Prevents accidental exposure of sensitive fields and allows distinct validation approaches.

```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

# Base with shared fields
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(unique=True)
    full_name: str

# Create model (input)
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Database model
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Read model (output) - excludes sensitive fields
class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

# Update model - all fields optional
class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
```

### Mixins for Common Fields

```python
class TimestampMixin(SQLModel):
    """Add created_at and updated_at to any model"""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class SoftDeleteMixin(SQLModel):
    """Add soft delete capability"""
    deleted_at: Optional[datetime] = Field(default=None)
    is_deleted: bool = Field(default=False)

# Usage
class Task(TimestampMixin, SoftDeleteMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
```

### Pydantic Validators

```python
from pydantic import field_validator, EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    username: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()
```

---

## 2. Relationships

### One-to-Many

```python
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # One team has many heroes
    heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    # Many heroes belong to one team
    team: Optional[Team] = Relationship(back_populates="heroes")
```

### Many-to-Many with Link Table

```python
class HeroTeamLink(SQLModel, table=True):
    """Link table for many-to-many relationship"""
    hero_id: int = Field(foreign_key="hero.id", primary_key=True)
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    role: Optional[str] = None  # Extra data on the relationship
    joined_at: datetime = Field(default_factory=datetime.utcnow)

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    teams: List["Team"] = Relationship(
        back_populates="heroes",
        link_model=HeroTeamLink
    )

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    heroes: List[Hero] = Relationship(
        back_populates="teams",
        link_model=HeroTeamLink
    )
```

### Self-Referential Relationships

```python
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    manager_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    # Self-referential relationship
    manager: Optional["Employee"] = Relationship(
        back_populates="direct_reports",
        sa_relationship_kwargs={"remote_side": "Employee.id"}
    )
    direct_reports: List["Employee"] = Relationship(back_populates="manager")
```

### Cascade Delete

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Cascade delete: when user is deleted, delete all posts
    posts: List["Post"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(foreign_key="user.id", ondelete="CASCADE")
    author: User = Relationship(back_populates="posts")
```

---

## 3. Inheritance

### Single Table Inheritance

```python
class Content(SQLModel, table=True):
    """Base content class - all types in one table"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content_type: str = Field(index=True)  # Discriminator

    # Article-specific fields (nullable for other types)
    author: Optional[str] = None
    word_count: Optional[int] = None

    # Video-specific fields
    duration: Optional[int] = None
    resolution: Optional[str] = None
```

### Joined Table Inheritance (Recommended)

```python
from sqlalchemy import Column, Integer, ForeignKey

class Content(SQLModel, table=True):
    """Base table with common fields"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    content_type: str = Field(index=True)

class Article(SQLModel, table=True):
    """Article-specific fields in separate table"""
    id: int = Field(
        sa_column=Column(Integer, ForeignKey("content.id"), primary_key=True)
    )
    author: str
    word_count: int

class Video(SQLModel, table=True):
    """Video-specific fields in separate table"""
    id: int = Field(
        sa_column=Column(Integer, ForeignKey("content.id"), primary_key=True)
    )
    duration: int
    resolution: str
```

---

## 4. Composite Keys and Constraints

### Composite Primary Key

```python
from sqlmodel import SQLModel, Field

class OrderItem(SQLModel, table=True):
    """Composite primary key example"""
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    quantity: int
    price: float
```

### Unique Constraints

```python
from sqlalchemy import UniqueConstraint

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    organization_id: int

    __table_args__ = (
        # Unique email within each organization
        UniqueConstraint('email', 'organization_id', name='uq_user_email_org'),
    )
```

### Check Constraints

```python
from sqlalchemy import CheckConstraint

class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    balance: float

    __table_args__ = (
        CheckConstraint('balance >= 0', name='ck_account_balance_positive'),
    )
```

---

## 5. Custom Field Types

### Enums

```python
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
```

### JSON Fields

```python
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    preferences: dict = Field(default={}, sa_column=Column(JSONB))
    metadata: dict = Field(default={}, sa_column=Column(JSONB))
```

### PostgreSQL Array Types

```python
from sqlalchemy import Column, ARRAY, String

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    tags: List[str] = Field(default=[], sa_column=Column(ARRAY(String)))
```

---

## 6. Index Strategies

### Single Column Index

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True)
```

### Composite Index

```python
from sqlalchemy import Index

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: str
    created_at: datetime

    __table_args__ = (
        # Composite index for common query pattern
        Index('idx_order_user_status', 'user_id', 'status'),
        Index('idx_order_created', 'created_at'),
    )
```

### Partial Index (PostgreSQL)

```python
from sqlalchemy import Index, text

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_active: bool = Field(default=True)

    __table_args__ = (
        # Index only active tasks
        Index(
            'idx_task_active',
            'title',
            postgresql_where=text('is_active = true')
        ),
    )
```

---

## Best Practices Summary

1. **Always use type hints** for all fields
2. **Index foreign keys** and frequently queried columns
3. **Separate API models** from database models
4. **Use lazy loading as default** with selective eager loading
5. **Follow naming conventions**: plural tables, lowercase with underscores
6. **Use mixins** for common patterns (timestamps, soft delete)
7. **Validate at the model level** using Pydantic validators
8. **Consider cascade behavior** carefully for relationships
