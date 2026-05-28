---
name: sqlmodel-expert
description: Advanced SQLModel patterns and comprehensive database migrations with Alembic. Use when creating SQLModel models, defining relationships (one-to-many, many-to-many, self-referential), setting up database migrations, optimizing queries, solving N+1 problems, implementing inheritance patterns, working with composite keys, creating indexes, performing data migrations, or troubleshooting Alembic issues. Triggers include "SQLModel", "Alembic migration", "database model", "relationship", "foreign key", "migration", "N+1 query", "query optimization", "database schema", or questions about ORM patterns.
---

# SQLModel Expert

Advanced SQLModel patterns and comprehensive Alembic migrations for production databases.

## Quick Start

### Define a Basic Model

```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Initialize Database

```bash
# Using Alembic
cd backend
alembic upgrade head

# Or manually
from sqlmodel import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")
SQLModel.metadata.create_all(engine)
```

### Create Migration

```bash
cd backend
alembic revision --autogenerate -m "add user table"
alembic upgrade head
```

## Core Topics

### 1. Advanced Model Patterns

- **Relationships**: One-to-many, many-to-many, self-referential
- **Inheritance**: Single table, joined table, polymorphism
- **Validation**: Pydantic validators, custom constraints
- **Mixins**: Timestamp, soft delete, reusable patterns
- **Field Types**: Enums, JSON, arrays, custom types
- **Indexes**: Single, composite, partial indexes
- **Constraints**: Unique, check, foreign key cascades

### 2. Comprehensive Migrations

- **Alembic Setup**: Configuration, env.py for SQLModel
- **Creating Migrations**: Autogenerate vs manual
- **Schema Changes**: Add/drop columns, rename, change types
- **Data Migrations**: Complex data transformations
- **Production Workflow**: Zero-downtime migrations
- **Rollback Strategies**: Safe downgrade patterns
- **Troubleshooting**: Common issues and solutions

### 3. Query Optimization

- **N+1 Problem**: Solutions with eager loading
- **Query Patterns**: Joins, aggregations, subqueries
- **Performance**: Indexes, batch operations, profiling
- **Advanced Queries**: Window functions, CTEs
- **Bulk Operations**: Insert, update, delete at scale

## Common Patterns

### One-to-Many Relationship

```python
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # One organization has many resources
    resources: List["Resource"] = Relationship(back_populates="organization")

class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    organization_id: Optional[int] = Field(foreign_key="organization.id")

    # Many resources belong to one organization
    organization: Optional[Organization] = Relationship(back_populates="resources")
```

### Many-to-Many with Link Table

```python
class ResourceCategoryLink(SQLModel, table=True):
    resource_id: int = Field(foreign_key="resource.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)

class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    categories: List["Category"] = Relationship(
        back_populates="resources",
        link_model=ResourceCategoryLink
    )

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    resources: List[Resource] = Relationship(
        back_populates="categories",
        link_model=ResourceCategoryLink
    )
```

### Solving N+1 Query Problem

```python
from sqlalchemy.orm import selectinload

# BAD - N+1 queries
resources = session.exec(select(Resource)).all()
for resource in resources:
    org = resource.organization  # Each triggers a query!

# GOOD - Eager loading (2 queries total)
statement = select(Resource).options(selectinload(Resource.organization))
resources = session.exec(statement).all()
for resource in resources:
    org = resource.organization  # No additional query!
```

### Creating a Migration

```python
# 1. Modify your model
class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str  # New field added

# 2. Generate migration
# alembic revision --autogenerate -m "add phone to resource"

# 3. Review generated migration
def upgrade() -> None:
    op.add_column('resource', sa.Column('phone', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('resource', 'phone')

# 4. Apply migration
# alembic upgrade head
```

## Vibe4Vets Specific Patterns

### Trust Score Calculation

```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    source_id: Optional[int] = Field(foreign_key="source.id")
    last_verified: Optional[datetime] = None

    @property
    def trust_score(self) -> float:
        """Calculate trust = reliability * freshness"""
        if not self.source or not self.last_verified:
            return 0.0

        reliability = self.source.reliability_score
        days_since_verified = (datetime.utcnow() - self.last_verified).days
        freshness = max(0, 1 - (days_since_verified / 365))

        return reliability * freshness
```

### Full-Text Search with PostgreSQL

```python
from sqlalchemy import Index, text
from sqlmodel import Field, SQLModel

class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    __table_args__ = (
        Index(
            'ix_resource_search',
            text("to_tsvector('english', name || ' ' || COALESCE(description, ''))"),
            postgresql_using='gin'
        ),
    )
```

## Best Practices Checklist

### Model Design
- [ ] Use type hints for all fields
- [ ] Separate read/write/update models
- [ ] Use mixins for common fields (timestamps, soft delete)
- [ ] Define indexes on foreign keys and frequently queried columns
- [ ] Use enums for constrained choices (categories, source tiers)

### Relationships
- [ ] Use `back_populates` for bidirectional relationships
- [ ] Create explicit link tables for many-to-many
- [ ] Consider cascade delete behavior
- [ ] Use eager loading to prevent N+1 queries
- [ ] Index foreign key columns

### Migrations
- [ ] Always review autogenerated migrations
- [ ] One logical change per migration
- [ ] Test both upgrade and downgrade
- [ ] Use descriptive migration names
- [ ] Never edit applied migrations
- [ ] Add data migrations when changing schemas
- [ ] Backup database before production migrations

## Troubleshooting Guide

### Migration Issues

**Problem**: Alembic doesn't detect model changes
```python
# Solution: Ensure models are imported in env.py
from app.models import Resource, Organization, Source  # Import all models
target_metadata = SQLModel.metadata
```

**Problem**: Failed migration
```bash
# Check current state
alembic current

# Manually fix issue, then stamp
alembic stamp head

# Or downgrade and retry
alembic downgrade -1
alembic upgrade head
```

### Query Performance

**Problem**: Slow queries
```python
# Enable query logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Use EXPLAIN ANALYZE
explain = session.exec(text("EXPLAIN ANALYZE SELECT ...")).all()
```

## Production Workflow

### Development
1. Modify SQLModel models
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration file
4. Test migration locally
5. Commit migration file

### Production
1. Backup database: `pg_dump mydb > backup.sql`
2. Deploy in maintenance window
3. Run migrations: `alembic upgrade head`
4. Monitor logs and metrics
5. Verify application functionality
