# Database Implementation Workflow

## Purpose

This workflow guides implementation of database schemas, migrations, and data access patterns.

Use this workflow when:
- Creating database migrations
- Defining database models/entities
- Implementing database queries
- Optimizing database performance

## Prerequisites

1. **Design Documentation**
   - Data model diagram
   - Entity relationships documented
   - Business rules clear

2. **Migration Tool Available**
   - Alembic (Python/SQLAlchemy)
   - Prisma (TypeScript)
   - TypeORM migrations (TypeScript)
   - Django migrations (Python)

3. **Database Running**
   - Development database accessible
   - Test database configured
   - Migration tracking table exists

## Phase 0: Start Task Tracking

Before beginning implementation, start task tracking:

```bash
# Start the task to update status and track progress
shark task start <task-id>

# Example:
shark task start T-E04-F04-001
```

This:
- Updates task status to "in-progress" in the database
- Tracks when implementation began
- Provides visibility to the team
- Enables accurate progress reporting

## Phase 1: Design Data Model

### Step 1.1: Define Entities

Before writing migrations, design entities clearly:

```python
# Example: User entity design

"""
User Entity
-----------
Purpose: Store user account information

Fields:
- id: UUID, primary key
- email: string, unique, required
- first_name: string, required
- last_name: string, required
- password_hash: string, required
- status: enum (active, inactive, suspended)
- created_at: datetime, auto
- updated_at: datetime, auto

Relationships:
- one-to-many with UserProfile
- many-to-many with Role

Business Rules:
- Email must be unique across all users
- Status defaults to 'active'
- Soft delete (status = 'inactive') preferred over hard delete

Indexes:
- email (unique)
- status (for filtering active users)
- created_at (for sorting)
"""
```

### Step 1.2: Define Relationships

```
User ──1:N── UserProfile    (one user has one profile)
User ──M:N── Role           (users have multiple roles)
User ──1:N── Post           (one user authors many posts)
Post ──M:N── Tag            (posts have multiple tags)
```

### Step 1.3: Consider Indexes

Index fields that are:
- Frequently queried (`WHERE`, `JOIN`)
- Used for sorting (`ORDER BY`)
- Used for uniqueness constraints

**Don't over-index:**
- Indexes slow down writes
- Indexes consume storage
- Only index what's actually queried

## Phase 2: Create Database Models

### Step 2.1: Define SQLAlchemy Models (Python)

```python
# File: app/models/user.py
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
import enum

from app.db.base_class import Base

class UserStatus(str, enum.Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(Base):
    """User entity."""
    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # User data
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Status
    status = Column(
        SQLEnum(UserStatus, name="user_status"),
        nullable=False,
        default=UserStatus.ACTIVE,
        index=True
    )

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    posts = relationship("Post", back_populates="author")
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
```

### Step 2.2: Define TypeORM Entities (TypeScript)

```typescript
// File: src/entities/User.ts
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToOne,
  OneToMany,
  ManyToMany,
  JoinTable,
  Index,
} from 'typeorm';
import { UserProfile } from './UserProfile';
import { Post } from './Post';
import { Role } from './Role';

export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended',
}

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'varchar', length: 255, unique: true })
  @Index()
  email: string;

  @Column({ type: 'varchar', length: 255 })
  first_name: string;

  @Column({ type: 'varchar', length: 255 })
  last_name: string;

  @Column({ type: 'varchar', length: 255 })
  password_hash: string;

  @Column({
    type: 'enum',
    enum: UserStatus,
    default: UserStatus.ACTIVE,
  })
  @Index()
  status: UserStatus;

  @CreateDateColumn()
  @Index()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;

  // Relationships
  @OneToOne(() => UserProfile, profile => profile.user)
  profile: UserProfile;

  @OneToMany(() => Post, post => post.author)
  posts: Post[];

  @ManyToMany(() => Role, role => role.users)
  @JoinTable({ name: 'user_roles' })
  roles: Role[];
}
```

## Phase 3: Create Migrations

### Step 3.1: Generate Migration (Alembic)

```bash
# Auto-generate migration from model changes
uv run alembic revision --autogenerate -m "create_users_table"

# Output: migrations/versions/001_create_users_table.py
```

### Step 3.2: Review and Edit Migration

**ALWAYS review autogenerated migrations:**

```python
# File: migrations/versions/001_create_users_table.py
"""create users table

Revision ID: 001
Revises:
Create Date: 2024-01-15 10:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """Create users table."""
    # Create enum type
    user_status = postgresql.ENUM('active', 'inactive', 'suspended', name='user_status')
    user_status.create(op.get_bind())

    # Create table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('status', user_status, nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # Create indexes
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_status', 'users', ['status'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])

def downgrade():
    """Drop users table."""
    op.drop_index('ix_users_created_at', 'users')
    op.drop_index('ix_users_status', 'users')
    op.drop_index('ix_users_email', 'users')
    op.drop_table('users')

    # Drop enum type
    user_status = postgresql.ENUM('active', 'inactive', 'suspended', name='user_status')
    user_status.drop(op.get_bind())
```

### Step 3.3: Add Data Migration (if needed)

```python
# File: migrations/versions/002_seed_admin_user.py
"""seed admin user

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 11:00:00
"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from datetime import datetime

revision = '002'
down_revision = '001'

def upgrade():
    """Create default admin user."""
    users_table = sa.table(
        'users',
        sa.column('id', postgresql.UUID),
        sa.column('email', sa.String),
        sa.column('first_name', sa.String),
        sa.column('last_name', sa.String),
        sa.column('password_hash', sa.String),
        sa.column('status', sa.String),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )

    op.bulk_insert(
        users_table,
        [
            {
                'id': uuid4(),
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'password_hash': '$2b$12$...',  # Pre-hashed password
                'status': 'active',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
            }
        ]
    )

def downgrade():
    """Remove admin user."""
    op.execute("DELETE FROM users WHERE email = 'admin@example.com'")
```

### Step 3.4: Test Migration

```bash
# Run migration on test database
uv run alembic upgrade head

# Verify table created
psql -d testdb -c "\d users"

# Test downgrade
uv run alembic downgrade -1

# Verify table dropped
psql -d testdb -c "\d users"

# Re-apply
uv run alembic upgrade head
```

## Phase 4: Implement Queries

### Step 4.1: Basic CRUD Operations

```python
# File: app/repositories/user_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.user import User, UserStatus
from uuid import UUID

class UserRepository:
    """Data access layer for User entities."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """Create new user."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[UserStatus] = None
    ) -> List[User]:
        """Find all users with optional filtering."""
        query = self.db.query(User)

        if status:
            query = query.filter(User.status == status)

        return query.offset(skip).limit(limit).all()

    def update(self, user: User) -> User:
        """Update existing user."""
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Delete user (hard delete)."""
        self.db.delete(user)
        self.db.commit()

    def soft_delete(self, user: User) -> User:
        """Soft delete user (mark as inactive)."""
        user.status = UserStatus.INACTIVE
        return self.update(user)
```

### Step 4.2: Complex Queries

```python
class UserRepository:
    # ... basic CRUD ...

    def search(
        self,
        query: Optional[str] = None,
        status: Optional[UserStatus] = None,
        created_after: Optional[datetime] = None,
        order_by: str = 'created_at',
        descending: bool = True
    ) -> List[User]:
        """Advanced search with multiple filters."""
        db_query = self.db.query(User)

        # Text search
        if query:
            search_filter = or_(
                User.email.ilike(f"%{query}%"),
                User.first_name.ilike(f"%{query}%"),
                User.last_name.ilike(f"%{query}%")
            )
            db_query = db_query.filter(search_filter)

        # Status filter
        if status:
            db_query = db_query.filter(User.status == status)

        # Date filter
        if created_after:
            db_query = db_query.filter(User.created_at >= created_after)

        # Ordering
        order_column = getattr(User, order_by)
        if descending:
            db_query = db_query.order_by(order_column.desc())
        else:
            db_query = db_query.order_by(order_column.asc())

        return db_query.all()

    def count_by_status(self) -> dict:
        """Count users grouped by status."""
        from sqlalchemy import func

        results = (
            self.db.query(User.status, func.count(User.id))
            .group_by(User.status)
            .all()
        )

        return {status: count for status, count in results}
```

### Step 4.3: Relationship Queries

```python
class UserRepository:
    # ... other methods ...

    def find_with_profile(self, user_id: UUID) -> Optional[User]:
        """Find user with profile eager-loaded."""
        from sqlalchemy.orm import joinedload

        return (
            self.db.query(User)
            .options(joinedload(User.profile))
            .filter(User.id == user_id)
            .first()
        )

    def find_with_posts(self, user_id: UUID) -> Optional[User]:
        """Find user with all posts."""
        from sqlalchemy.orm import selectinload

        return (
            self.db.query(User)
            .options(selectinload(User.posts))
            .filter(User.id == user_id)
            .first()
        )

    def find_users_with_role(self, role_name: str) -> List[User]:
        """Find all users with specific role."""
        from app.models.role import Role

        return (
            self.db.query(User)
            .join(User.roles)
            .filter(Role.name == role_name)
            .all()
        )
```

## Phase 5: Query Optimization

### Step 5.1: Add Indexes

```python
# File: migrations/versions/003_add_performance_indexes.py
"""add performance indexes

Revision ID: 003
Revises: 002
"""
from alembic import op

def upgrade():
    """Add indexes for common queries."""
    # Composite index for filtering active users by creation date
    op.create_index(
        'ix_users_status_created_at',
        'users',
        ['status', 'created_at']
    )

    # Index for name searches
    op.create_index(
        'ix_users_names',
        'users',
        ['first_name', 'last_name']
    )

def downgrade():
    """Remove indexes."""
    op.drop_index('ix_users_names', 'users')
    op.drop_index('ix_users_status_created_at', 'users')
```

### Step 5.2: Use Query Optimization

```python
# Eager loading to avoid N+1 queries
users = (
    db.query(User)
    .options(joinedload(User.profile))
    .options(selectinload(User.posts))
    .all()
)

# Select only needed columns
from sqlalchemy import select

user_emails = db.execute(
    select(User.email)
    .where(User.status == UserStatus.ACTIVE)
).scalars().all()

# Batch operations
from sqlalchemy import update

# Update multiple rows in one query
db.execute(
    update(User)
    .where(User.status == UserStatus.INACTIVE)
    .values(status=UserStatus.SUSPENDED)
)
db.commit()
```

## Phase 6: Testing

### Step 6.1: Test Migrations

```python
# File: tests/integration/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config

def test_migrations_run_successfully():
    """Test that all migrations run without errors."""
    config = Config("alembic.ini")

    # Run migrations
    command.upgrade(config, "head")

    # Verify success
    # (if this doesn't raise, migrations succeeded)

def test_migrations_are_reversible():
    """Test that migrations can be downgraded."""
    config = Config("alembic.ini")

    # Upgrade
    command.upgrade(config, "head")

    # Downgrade one step
    command.downgrade(config, "-1")

    # Upgrade again
    command.upgrade(config, "head")
```

### Step 6.2: Test Repository

```python
# File: tests/unit/repositories/test_user_repository.py
import pytest
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserStatus

class TestUserRepository:
    def test_create_user(self, db_session):
        """Test creating user."""
        repo = UserRepository(db_session)

        user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password_hash="hashed",
        )

        created = repo.create(user)

        assert created.id is not None
        assert created.email == "test@example.com"

    def test_find_by_email(self, db_session):
        """Test finding user by email."""
        repo = UserRepository(db_session)

        # Create user
        user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password_hash="hashed",
        )
        repo.create(user)

        # Find by email
        found = repo.find_by_email("test@example.com")

        assert found is not None
        assert found.email == "test@example.com"

    def test_soft_delete(self, db_session):
        """Test soft delete sets status to inactive."""
        repo = UserRepository(db_session)

        user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password_hash="hashed",
        )
        created = repo.create(user)

        # Soft delete
        repo.soft_delete(created)

        # Verify status changed
        found = repo.find_by_id(created.id)
        assert found.status == UserStatus.INACTIVE
```

## Phase 7: Validation Gates

### Gate 1: Migration Linting
```bash
# Verify migration files are valid Python
uv run flake8 migrations/versions/
```

### Gate 2: Migration Testing
```bash
# Test migrations run successfully
uv run pytest tests/integration/test_migrations.py -v
```

### Gate 3: Repository Testing
```bash
# Test repository methods
uv run pytest tests/unit/repositories/ -v
```

### Gate 4: Integration Testing
```bash
# Test database operations end-to-end
uv run pytest tests/integration/ -v
```

## Common Patterns

### Soft Delete
```python
# Mark as deleted instead of removing
user.status = UserStatus.INACTIVE
user.deleted_at = datetime.utcnow()
```

### Optimistic Locking
```python
# Prevent concurrent update conflicts
class User(Base):
    # ... other columns ...
    version = Column(Integer, nullable=False, default=1)

# On update
user.version += 1
db.commit()  # Raises if another transaction updated first
```

### Audit Trail
```python
class AuditMixin:
    """Mixin for audit fields."""
    created_by = Column(UUID, nullable=True)
    updated_by = Column(UUID, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base, AuditMixin):
    # ... user fields ...
```

## Completion Checklist

- [ ] Data model designed with clear relationships
- [ ] Database models/entities defined
- [ ] Migrations created and tested
- [ ] Indexes added for common queries
- [ ] Repository layer implemented
- [ ] Complex queries optimized
- [ ] Migrations tested (upgrade and downgrade)
- [ ] Repository unit tests passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] **Task completed:** `shark task complete <task-id>`

**Final Step:** Mark the task as complete:
```bash
shark task complete T-E04-F04-001
```

This updates the task status to "completed" and records completion time in the database.

## Common Issues

| Issue | Solution |
|-------|----------|
| Migration conflicts | Use `alembic heads` to find branches, merge manually |
| N+1 query problem | Use eager loading (`joinedload`, `selectinload`) |
| Slow queries | Check `EXPLAIN ANALYZE`, add indexes |
| Foreign key violations | Ensure migrations create tables in dependency order |
| Unique constraint errors | Handle in service layer with try/except |

## Reference

- Error handling: `../context/error-handling.md`
- Testing requirements: `../context/testing-requirements.md`
- Coding standards: `../context/coding-standards.md`

---

**Remember:** Migrations are irreversible in production. Test thoroughly, review carefully, and always provide downgrade paths.
