# SQLModel Relationships

Complete patterns for defining relationships between models.

---

## One-to-Many Relationship

The most common relationship pattern.

### Example: User has many Orders

```python
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)

    # One-to-Many: User has many orders
    orders: List["Order"] = Relationship(back_populates="user")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    total: float
    status: str = Field(default="pending")

    # Foreign key
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)

    # Many-to-One: Order belongs to User
    user: Optional["User"] = Relationship(back_populates="orders")
```

### Key Points
- Parent side: `List["Child"]` with `Relationship(back_populates="parent_field")`
- Child side: `Optional["Parent"]` with `Relationship(back_populates="children_field")`
- Foreign key on child side: `Field(foreign_key="parent_table.id")`
- Always index foreign keys for query performance

---

## One-to-One Relationship

Use `uselist=False` on the parent side.

### Example: User has one Profile

```python
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # One-to-One: User has one profile
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    # Foreign key (unique ensures one-to-one)
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        unique=True,
        index=True
    )

    # Back reference
    user: Optional["User"] = Relationship(back_populates="profile")
```

### Key Points
- Use `uselist=False` in `sa_relationship_kwargs` on parent
- Add `unique=True` to foreign key for database-level enforcement
- Both sides use `Optional["Model"]` (not List)

---

## Many-to-Many Relationship

Requires a link/association table.

### Example: Students enrolled in Courses

```python
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# Link table (association table)
class StudentCourseLink(SQLModel, table=True):
    student_id: Optional[int] = Field(
        default=None, foreign_key="student.id", primary_key=True
    )
    course_id: Optional[int] = Field(
        default=None, foreign_key="course.id", primary_key=True
    )

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)

    # Many-to-Many via link table
    courses: List["Course"] = Relationship(
        back_populates="students",
        link_model=StudentCourseLink
    )

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    code: str = Field(unique=True, index=True)

    # Many-to-Many via link table
    students: List["Student"] = Relationship(
        back_populates="courses",
        link_model=StudentCourseLink
    )
```

### Link Table with Extra Fields

When the relationship has attributes (e.g., enrollment date, grade):

```python
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Enrollment(SQLModel, table=True):
    """Link table with additional fields"""
    student_id: Optional[int] = Field(
        default=None, foreign_key="student.id", primary_key=True
    )
    course_id: Optional[int] = Field(
        default=None, foreign_key="course.id", primary_key=True
    )

    # Extra fields on the relationship
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    grade: Optional[str] = None

    # Relationships to access parent objects
    student: Optional["Student"] = Relationship(back_populates="enrollments")
    course: Optional["Course"] = Relationship(back_populates="enrollments")

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    enrollments: List["Enrollment"] = Relationship(back_populates="student")

    @property
    def courses(self) -> List["Course"]:
        return [e.course for e in self.enrollments]

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    enrollments: List["Enrollment"] = Relationship(back_populates="course")

    @property
    def students(self) -> List["Student"]:
        return [e.student for e in self.enrollments]
```

---

## Self-Referential Relationship

For hierarchical data (e.g., categories, org charts).

### Example: Category with Subcategories

```python
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Self-referential foreign key
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id", index=True)

    # Parent reference
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"}
    )

    # Children collection
    children: List["Category"] = Relationship(back_populates="parent")
```

### Example: Employee Manager Hierarchy

```python
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    title: str

    manager_id: Optional[int] = Field(default=None, foreign_key="employee.id", index=True)

    manager: Optional["Employee"] = Relationship(
        back_populates="direct_reports",
        sa_relationship_kwargs={"remote_side": "Employee.id"}
    )

    direct_reports: List["Employee"] = Relationship(back_populates="manager")
```

---

## Cascade Behaviors

Control what happens when parent is deleted.

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Cascade delete: when user deleted, delete all orders
    orders: List["Order"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Soft cascade: set to null on delete (requires nullable FK)
    comments: List["Comment"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "save-update, merge"}
    )
```

### Cascade Options

| Option | Behavior |
|--------|----------|
| `save-update` | Cascade save/update (default) |
| `merge` | Cascade merge operations |
| `delete` | Delete children when parent deleted |
| `delete-orphan` | Delete children when removed from collection |
| `all` | All of the above |
| `none` | No cascading |

---

## Lazy Loading Strategies

Configure how related objects are loaded.

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Lazy load (default) - query when accessed
    orders: List["Order"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "select"}
    )

    # Eager load with selectin - efficient for collections
    reviews: List["Review"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    # Eager load with join - efficient for single objects
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "joined", "uselist": False}
    )
```

### Loading Strategy Guide

| Strategy | SQL Queries | Best For |
|----------|-------------|----------|
| `select` | N+1 | Rarely accessed relations |
| `selectin` | 2 | Collections, batch loading |
| `joined` | 1 (with JOIN) | Single objects, always needed |
| `subquery` | 2 | Complex nested collections |
| `raise` | Error | Prevent accidental lazy loads |

---

## Query-Time Loading Override

Override lazy loading at query time:

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload

# Load users with their orders (override lazy setting)
statement = select(User).options(selectinload(User.orders))
users = session.exec(statement).all()

# Nested eager loading
statement = select(User).options(
    selectinload(User.orders).selectinload(Order.items)
)

# Multiple relations
statement = select(User).options(
    joinedload(User.profile),
    selectinload(User.orders)
)
```
