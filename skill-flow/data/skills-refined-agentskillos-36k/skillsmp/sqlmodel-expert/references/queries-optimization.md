# SQLModel Query Patterns and Optimization

## Table of Contents
1. Basic Query Patterns
2. Advanced Queries
3. N+1 Query Problem Solutions
4. Query Optimization Techniques
5. Bulk Operations
6. Raw SQL and Performance
7. Testing and Profiling

---

## 1. Basic Query Patterns

### Simple Queries

```python
from sqlmodel import Session, select
from app.models import User

# Get all users
statement = select(User)
users = session.exec(statement).all()

# Get one user
statement = select(User).where(User.id == 1)
user = session.exec(statement).first()

# Get or 404
user = session.get(User, user_id)
if not user:
    raise HTTPException(status_code=404, detail="User not found")
```

### Filtering

```python
# Simple filter
statement = select(User).where(User.is_active == True)

# Multiple conditions (AND)
statement = select(User).where(
    User.is_active == True,
    User.email_verified == True
)

# OR conditions
from sqlalchemy import or_
statement = select(User).where(
    or_(User.email == "user@example.com", User.username == "user123")
)

# IN clause
user_ids = [1, 2, 3, 4]
statement = select(User).where(User.id.in_(user_ids))

# LIKE clause
statement = select(User).where(User.username.like("%john%"))

# IS NULL / IS NOT NULL
statement = select(User).where(User.deleted_at.is_(None))
```

### Ordering

```python
# Order by single column
statement = select(User).order_by(User.created_at.desc())

# Order by multiple columns
statement = select(User).order_by(User.is_active.desc(), User.created_at.desc())
```

### Pagination

```python
# Offset-based pagination
def get_users(skip: int = 0, limit: int = 100):
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()

# Cursor-based pagination (better for large datasets)
def get_users_cursor(cursor_id: int = None, limit: int = 100):
    statement = select(User)
    if cursor_id:
        statement = statement.where(User.id > cursor_id)
    statement = statement.order_by(User.id).limit(limit)
    return session.exec(statement).all()
```

---

## 2. Advanced Queries

### Joins

```python
# Inner join
statement = select(User, Post).join(Post, User.id == Post.user_id)
results = session.exec(statement).all()

# Left outer join
statement = select(User, Post).outerjoin(Post, User.id == Post.user_id)

# Join with filtering
statement = (
    select(User, Post)
    .join(Post)
    .where(Post.published == True)
    .where(User.is_active == True)
)
```

### Aggregations

```python
from sqlalchemy import func

# Count
statement = select(func.count(User.id))
count = session.exec(statement).one()

# Group by
statement = (
    select(User.country, func.count(User.id))
    .group_by(User.country)
)

# Having clause
statement = (
    select(User.country, func.count(User.id))
    .group_by(User.country)
    .having(func.count(User.id) > 10)
)

# Multiple aggregations
statement = select(
    User.country,
    func.count(User.id).label('user_count'),
    func.avg(User.age).label('avg_age'),
)
.group_by(User.country)
```

### Subqueries

```python
# Scalar subquery
subquery = (
    select(func.count(Post.id))
    .where(Post.user_id == User.id)
    .scalar_subquery()
)
statement = select(User, subquery.label('post_count'))

# Subquery in WHERE
active_user_ids = select(User.id).where(User.is_active == True).subquery()
statement = select(Post).where(Post.user_id.in_(active_user_ids))
```

### Window Functions

```python
from sqlalchemy import func, over

# Row number
statement = select(
    User.username,
    User.country,
    func.row_number().over(
        partition_by=User.country,
        order_by=User.created_at.desc()
    ).label('row_num')
)
```

---

## 3. N+1 Query Problem Solutions

### The Problem

```python
# BAD - N+1 query problem
users = session.exec(select(User)).all()
for user in users:
    posts = user.posts  # Each triggers a new query!
```

### Solution 1: Eager Loading with selectinload

```python
from sqlalchemy.orm import selectinload

# GOOD - Only 2 queries total
statement = select(User).options(selectinload(User.posts))
users = session.exec(statement).all()

for user in users:
    posts = user.posts  # No additional query!
```

### Solution 2: Joined Load

```python
from sqlalchemy.orm import joinedload

# Single query with JOIN
statement = select(User).options(joinedload(User.posts))
users = session.exec(statement).unique().all()
```

### Solution 3: Nested Eager Loading

```python
# Load users with posts and post comments
statement = (
    select(User)
    .options(selectinload(User.posts).selectinload(Post.comments))
)
```

---

## 4. Query Optimization Techniques

### Use Indexes

```python
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True)

    __table_args__ = (
        Index('idx_active_created', 'is_active', 'created_at'),
    )
```

### Select Only Needed Columns

```python
# BAD - loads entire object
users = session.exec(select(User)).all()

# GOOD - select only needed columns
statement = select(User.id, User.username, User.email)
results = session.exec(statement).all()
```

### Use Exists for Checking

```python
from sqlalchemy import exists

# BAD - loads all data
user = session.exec(select(User).where(User.email == email)).first()
if user: ...

# GOOD - only checks existence
statement = select(exists(select(User).where(User.email == email)))
exists_result = session.exec(statement).one()
```

### Batch Queries

```python
# BAD - multiple individual queries
for user_id in user_ids:
    user = session.get(User, user_id)

# GOOD - single batch query
statement = select(User).where(User.id.in_(user_ids))
users = session.exec(statement).all()
```

---

## 5. Bulk Operations

### Bulk Insert

```python
# Add all at once
users = [User(username=f"user{i}") for i in range(1000)]
session.add_all(users)
session.commit()

# Or use bulk_insert_mappings (faster)
user_dicts = [{"username": f"user{i}"} for i in range(1000)]
session.bulk_insert_mappings(User, user_dicts)
session.commit()
```

### Bulk Update

```python
from sqlalchemy import update

statement = (
    update(User)
    .where(User.is_active == False)
    .values(deleted_at=datetime.utcnow())
)
session.exec(statement)
session.commit()
```

### Bulk Delete

```python
from sqlalchemy import delete

statement = delete(User).where(User.deleted_at.isnot(None))
session.exec(statement)
session.commit()
```

---

## 6. Raw SQL

### Execute Raw SQL

```python
from sqlalchemy import text

# Read query
statement = text("SELECT * FROM users WHERE is_active = :is_active")
results = session.exec(statement, {"is_active": True}).all()

# Write query
statement = text("UPDATE users SET last_login = :ts WHERE id = :id")
session.exec(statement, {"ts": datetime.utcnow(), "id": 1})
session.commit()
```

---

## 7. Testing and Profiling

### Query Logging

```python
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Query Profiling

```python
from sqlalchemy import event
from time import time

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time() - conn.info['query_start_time'].pop(-1)
    if total > 0.1:  # Log queries slower than 100ms
        print(f"Slow query ({total:.2f}s): {statement}")
```

### Explain Analyze

```python
# PostgreSQL EXPLAIN ANALYZE
explain = session.exec(text("EXPLAIN ANALYZE SELECT * FROM users WHERE is_active = true")).all()
for row in explain:
    print(row)
```

---

## Best Practices Summary

1. **Always use indexes** on foreign keys and frequently queried columns
2. **Use eager loading** (selectinload/joinedload) to prevent N+1 queries
3. **Select only needed columns** when possible
4. **Use pagination** for large result sets
5. **Batch operations** instead of loops
6. **Profile queries** in development
7. **Use connection pooling** in production
8. **Monitor slow queries** with logging
9. **Cache expensive queries** when appropriate
10. **Test query counts** in integration tests
