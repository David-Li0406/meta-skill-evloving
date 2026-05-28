# Performance Optimization

Advanced patterns for high-performance SQLModel applications.

---

## N+1 Query Problem

The most common performance issue with ORMs.

### The Problem

```python
# BAD: N+1 queries
users = session.exec(select(User)).all()
for user in users:
    print(user.orders)  # Each access triggers a new query!

# Results in:
# Query 1: SELECT * FROM user
# Query 2: SELECT * FROM order WHERE user_id = 1
# Query 3: SELECT * FROM order WHERE user_id = 2
# ... N more queries
```

### The Solution: Eager Loading

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload

# GOOD: 2 queries total with selectinload
statement = select(User).options(selectinload(User.orders))
users = session.exec(statement).all()

# Results in:
# Query 1: SELECT * FROM user
# Query 2: SELECT * FROM order WHERE user_id IN (1, 2, 3, ...)

# GOOD: 1 query with joinedload (for single relations)
statement = select(Order).options(joinedload(Order.user))
orders = session.exec(statement).all()
```

### Choosing Loading Strategy

| Scenario | Strategy | Why |
|----------|----------|-----|
| Loading collection (many children) | `selectinload` | Efficient IN query |
| Loading single object | `joinedload` | Single JOIN query |
| Nested collections | `selectinload` chained | Avoids cartesian product |
| Optional relation | `joinedload` + `isouter=True` | LEFT JOIN |

```python
# Nested eager loading
statement = select(User).options(
    selectinload(User.orders).selectinload(Order.items)
)

# Multiple relations
statement = select(User).options(
    joinedload(User.profile),
    selectinload(User.orders),
)
```

---

## Indexing Strategy

### When to Add Indexes

| Column Type | Index? | Reason |
|-------------|--------|--------|
| Primary key | Automatic | Always indexed |
| Foreign key | **Yes** | JOIN performance |
| Unique constraint | Automatic | Uniqueness enforced |
| WHERE clause columns | **Yes** | Filter performance |
| ORDER BY columns | Consider | Sort performance |
| Columns in JOINs | **Yes** | Join performance |
| Low cardinality | Usually no | Little benefit |

### Index Types

```python
from sqlmodel import Field, SQLModel
from sqlalchemy import Index

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Single column index
    sku: str = Field(index=True, unique=True)

    # Index for filtering
    category: str = Field(index=True)
    status: str = Field(index=True)

    # Price for range queries
    price: float = Field(index=True)

    # Composite index (defined at class level)
    __table_args__ = (
        Index("ix_product_category_status", "category", "status"),
        Index("ix_product_price_category", "price", "category"),
    )
```

### Composite Index Guidelines

- Column order matters: put most selective first
- Match query patterns: `WHERE category = ? AND status = ?`
- Consider covering indexes for read-heavy queries

---

## Query Optimization

### Select Only Needed Columns

```python
from sqlmodel import select, col

# BAD: Selects all columns
users = session.exec(select(User)).all()

# GOOD: Select specific columns
statement = select(User.id, User.name, User.email)
results = session.exec(statement).all()

# Returns tuples, not User objects
for user_id, name, email in results:
    print(f"{name}: {email}")
```

### Pagination

```python
from sqlmodel import select

# Offset pagination (simple but slow for large offsets)
statement = select(User).offset(100).limit(20)
users = session.exec(statement).all()

# Keyset pagination (more efficient for large datasets)
last_id = 100
statement = (
    select(User)
    .where(User.id > last_id)
    .order_by(User.id)
    .limit(20)
)
users = session.exec(statement).all()
```

### Efficient Counting

```python
from sqlmodel import select, func

# BAD: Loads all objects just to count
count = len(session.exec(select(User)).all())

# GOOD: Database-side count
statement = select(func.count()).select_from(User)
count = session.exec(statement).one()

# With filter
statement = select(func.count()).select_from(User).where(User.status == "active")
active_count = session.exec(statement).one()
```

### Exists Check

```python
from sqlmodel import select
from sqlalchemy import exists

# BAD: Loads object to check existence
user = session.exec(select(User).where(User.email == email)).first()
if user:
    ...

# GOOD: EXISTS query
statement = select(exists().where(User.email == email))
email_exists = session.exec(statement).one()
```

---

## Bulk Operations

### Bulk Insert

```python
from sqlmodel import Session

# BAD: Individual inserts
for data in items_data:
    item = Item(**data)
    session.add(item)
    session.commit()  # N commits!

# GOOD: Batch insert
items = [Item(**data) for data in items_data]
session.add_all(items)
session.commit()  # Single commit

# BETTER: Bulk insert (bypasses ORM)
from sqlalchemy import insert

session.exec(
    insert(Item),
    [{"name": "A", "price": 10}, {"name": "B", "price": 20}]
)
session.commit()
```

### Bulk Update

```python
from sqlmodel import select, update

# BAD: Load and update individually
users = session.exec(select(User).where(User.status == "pending")).all()
for user in users:
    user.status = "active"
session.commit()

# GOOD: Bulk update
statement = (
    update(User)
    .where(User.status == "pending")
    .values(status="active")
)
session.exec(statement)
session.commit()
```

### Bulk Delete

```python
from sqlmodel import delete

# BAD: Load and delete individually
users = session.exec(select(User).where(User.deleted == True)).all()
for user in users:
    session.delete(user)

# GOOD: Bulk delete
statement = delete(User).where(User.deleted == True)
session.exec(statement)
session.commit()
```

---

## Connection Pool Tuning

### Pool Size Calculation

```
Optimal pool_size = (Number of concurrent requests) / (Average query time in seconds * Requests per second)
```

### Monitoring Pool Health

```python
from sqlalchemy import event

# Log pool statistics
@event.listens_for(engine, "checkout")
def log_checkout(dbapi_conn, connection_rec, connection_proxy):
    print(f"Pool size: {engine.pool.size()}")
    print(f"Checked out: {engine.pool.checkedout()}")
    print(f"Overflow: {engine.pool.overflow()}")
```

### Pool Configuration by Workload

```python
# High-throughput API
engine = create_engine(
    url,
    pool_size=20,
    max_overflow=30,
    pool_timeout=10,  # Fail fast
)

# Background workers
engine = create_engine(
    url,
    pool_size=2,
    max_overflow=3,
    pool_timeout=60,  # Can wait
)

# Read replicas
read_engine = create_engine(
    read_replica_url,
    pool_size=30,
    max_overflow=20,
)
```

---

## Caching Strategies

### Query Result Caching

```python
from functools import lru_cache
import hashlib

# Simple in-memory cache
@lru_cache(maxsize=100)
def get_user_by_id(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)

# Redis caching (production)
import redis
import json

redis_client = redis.Redis()

def get_user_cached(user_id: int) -> User | None:
    cache_key = f"user:{user_id}"

    # Try cache
    cached = redis_client.get(cache_key)
    if cached:
        return User(**json.loads(cached))

    # Query database
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            redis_client.setex(
                cache_key,
                300,  # 5 min TTL
                user.model_dump_json()
            )
        return user
```

### Cache Invalidation

```python
def update_user(user_id: int, data: dict):
    with Session(engine) as session:
        user = session.get(User, user_id)
        for key, value in data.items():
            setattr(user, key, value)
        session.commit()

        # Invalidate cache
        redis_client.delete(f"user:{user_id}")
```

---

## Query Analysis

### Enable SQL Logging

```python
# Development only
engine = create_engine(url, echo=True)

# Or per-query
import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
```

### EXPLAIN Queries

```python
from sqlalchemy import text

# PostgreSQL
result = session.exec(text("EXPLAIN ANALYZE SELECT * FROM user WHERE status = 'active'"))
for row in result:
    print(row)

# Check for sequential scans on large tables
# Add indexes if Seq Scan on large tables
```

### Query Timing

```python
import time
from contextlib import contextmanager

@contextmanager
def query_timer(label: str):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.3f}s")

# Usage
with query_timer("Load users with orders"):
    users = session.exec(
        select(User).options(selectinload(User.orders))
    ).all()
```

---

## Anti-Patterns Summary

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| N+1 queries | Exponential queries | Eager loading |
| SELECT * | Excess data transfer | Select specific columns |
| No indexes on FKs | Slow JOINs | Add indexes |
| Large offset pagination | Full table scan | Keyset pagination |
| Individual commits | Transaction overhead | Batch commits |
| Missing pool_pre_ping | Stale connections | Enable pre-ping |
| Unbounded queries | Memory exhaustion | Always use LIMIT |
