---
name: dataflow-express
description: "High-performance direct node invocation for DataFlow operations. Use when asking 'ExpressDataFlow', 'db.express', 'direct node invocation', 'fast CRUD', 'simple database operations', 'skip workflow overhead', or 'high-performance DataFlow'."
---

# ExpressDataFlow - High-Performance Direct Node Invocation

High-performance wrapper providing ~23x faster execution by bypassing workflow overhead for simple database operations.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> Related Skills: [`dataflow-quickstart`](dataflow-quickstart.md), [`dataflow-crud-operations`](dataflow-crud-operations.md), [`dataflow-bulk-operations`](dataflow-bulk-operations.md)
> Related Subagents: `dataflow-specialist` (enterprise features)

## Quick Reference
- **Access**: `db.express.<operation>()` after `await db.create_tables_async()`
- **Performance**: ~23x faster than workflow-based operations
- **Operations**: create, read, find_one, update, delete, list, count, bulk_create, bulk_update, bulk_delete, bulk_upsert
- **Best For**: Simple CRUD operations, high-throughput scenarios, API endpoints
- **NOT For**: Multi-node workflows, conditional execution, transactions

## Docker/FastAPI Quick Start (RECOMMENDED)

For Docker/FastAPI deployment, use `auto_migrate=False` + `create_tables_async()` to avoid async/sync conflicts:

```python
from dataflow import DataFlow
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Step 1: Initialize with auto_migrate=False for Docker
db = DataFlow(
    "postgresql://user:password@postgres:5432/mydb",
    auto_migrate=False  # CRITICAL for Docker - prevents DF-501 errors
)

# Step 2: Register models
@db.model
class User:
    id: str
    name: str
    email: str
    active: bool = True

# Step 3: Create tables in lifespan (event loop is ready)
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables_async()  # Safe - event loop ready
    yield
    await db.close_async()          # Cleanup connections

app = FastAPI(lifespan=lifespan)

# Step 4: Use Express for endpoints - 23x faster than workflows!
@app.post("/users")
async def create_user(data: dict):
    return await db.express.create("User", data)

@app.get("/users/{id}")
async def get_user(id: str):
    return await db.express.read("User", id)

@app.put("/users/{id}")
async def update_user(id: str, data: dict):
    return await db.express.update("User", {"id": id}, data)

@app.delete("/users/{id}")
async def delete_user(id: str):
    return await db.express.delete("User", id)

@app.get("/users")
async def list_users(skip: int = 0, limit: int = 100):
    return await db.express.list("User", limit=limit, offset=skip)
```

## CLI/Script Quick Start

For CLI scripts (no running event loop), the simpler pattern works:

```python
from dataflow import DataFlow

db = DataFlow("postgresql://user:password@localhost/mydb")

@db.model
class User:
    id: str
    name: str
    email: str
    active: bool = True

# Initialize before using express
await db.initialize()

# Direct node invocation - ~23x faster than workflows
user = await db.express.create("User", {
    "id": "user-001",
    "name": "Alice",
    "email": "alice@example.com"
})

# Read
user = await db.express.read("User", "user-001")

# Update
updated = await db.express.update("User", {"id": "user-001"}, {"name": "Alice Updated"})

# Delete
success = await db.express.delete("User", "user-001")

# List with filter
users = await db.express.list("User", filter={"active": True})

# Count
total = await db.express.count("User")

# Find One - single record by filter (non-PK lookup)
user = await db.express.find_one("User", {"email": "alice@example.com"})
```

## Complete API Reference

### CRUD Operations

```python
# Create
result = await db.express.create("ModelName", {
    "id": "record-001",
    "field1": "value1",
    "field2": "value2"
})
# Returns: {"id": "record-001", "field1": "value1", "field2": "value2", ...}

# Read (by primary key)
result = await db.express.read("ModelName", "record-001")
result = await db.express.read("ModelName", "record-001", raise_on_not_found=True)
# Returns: dict or None

# Find One (by filter - non-PK lookup)
result = await db.express.find_one("ModelName", {"email": "user@example.com"})
result = await db.express.find_one("ModelName", {"status": "active", "role": "admin"})
# Returns: dict or None (first matching record)
# NOTE: Filter MUST be non-empty. For unfiltered queries, use list() with limit=1

# Update
result = await db.express.update(
    "ModelName",
    filter={"id": "record-001"},  # Find record
    fields={"field1": "new_value"}  # Update fields
)
# Returns: {"id": "record-001", "field1": "new_value", ...}

# Delete
success = await db.express.delete("ModelName", "record-001")
# Returns: True or False

# List
results = await db.express.list("ModelName", filter={"active": True}, limit=100, offset=0)
# Returns: [{"id": "...", ...}, ...]

# Count
total = await db.express.count("ModelName", filter={"active": True})
# Returns: int
```

### Bulk Operations

```python
# Bulk Create
records = [
    {"id": "1", "name": "Alice"},
    {"id": "2", "name": "Bob"},
    {"id": "3", "name": "Charlie"}
]
created = await db.express.bulk_create("ModelName", records)
# Returns: [{"id": "1", ...}, {"id": "2", ...}, {"id": "3", ...}]

# Bulk Update
result = await db.express.bulk_update(
    "ModelName",
    filter={"active": True},
    data={"active": False}
)
# Returns: {"success": True, "updated": 5}

# Bulk Delete
success = await db.express.bulk_delete("ModelName", ["id-1", "id-2", "id-3"])
# Returns: True or False

# Bulk Upsert
result = await db.express.bulk_upsert(
    "ModelName",
    records=[{"id": "1", "name": "Alice"}, {"id": "4", "name": "Diana"}],
    conflict_on=["id"]
)
# Returns: {"success": True, "upserted": 2, "created": 1, "updated": 1}
```

## Performance Comparison

| Operation | Workflow Time | Express Time | Speedup |
|-----------|--------------|--------------|---------|
| Create | 2.3ms | 0.1ms | **23x** |
| Read | 2.1ms | 0.09ms | **23x** |
| Update | 2.4ms | 0.11ms | **22x** |
| Delete | 2.2ms | 0.1ms | **22x** |
| List | 2.5ms | 0.12ms | **21x** |
| Bulk Create (100) | 25ms | 1.2ms | **21x** |

## When to Use ExpressDataFlow

### Use ExpressDataFlow

- Simple CRUD operations without workflow complexity
- High-throughput applications needing maximum performance
- Cleaner code for straightforward database operations
- Single-node operations

### Use Traditional Workflows Instead

- Multi-node operations with data flow between nodes
- Conditional execution or branching logic
- Transaction management across operations
- Cycle execution patterns
- Error recovery and retry logic

## Common Patterns

### Pattern 1: User Registration (using find_one)

```python
async def register_user(email: str, name: str) -> dict:
    import uuid

    # Check if user exists using find_one (cleaner than list with limit=1)
    existing = await db.express.find_one("User", {"email": email})
    if existing:
        return {"error": "Email already registered", "user": existing}

    # Create new user
    user = await db.express.create("User", {
        "id": str(uuid.uuid4()),
        "email": email,
        "name": name,
        "active": True
    })
    return {"success": True, "user": user}
```

### Pattern 2: Paginated API

```python
async def get_users_paginated(page: int = 1, per_page: int = 20) -> dict:
    offset = (page - 1) * per_page

    total = await db.express.count("User")
    users = await db.express.list("User", limit=per_page, offset=offset)

    return {
        "data": users,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": (total + per_page - 1) // per_page
    }
```

### Pattern 3: Batch Import

```python
async def import_users(csv_data: list[dict]) -> dict:
    import uuid

    records = [
        {"id": str(uuid.uuid4()), "name": row["name"], "email": row["email"]}
        for row in csv_data
    ]

    result = await db.express.bulk_upsert(
        "User", records=records, conflict_on=["email"]
    )

    return {
        "imported": result.get("upserted", 0),
        "created": result.get("created", 0),
        "updated": result.get("updated", 0)
    }
```

## Troubleshooting

### "Model not found: ModelName"

Use exact class name (case-sensitive):

```python
@db.model
class UserAccount:
    id: str

# WRONG
await db.express.create("useraccount", {...})

# CORRECT
await db.express.create("UserAccount", {...})
```

### "DataFlow not initialized"

Always initialize before using express:

```python
db = DataFlow("postgresql://...")

@db.model
class User:
    id: str

# REQUIRED
await db.initialize()

# Now express works
await db.express.create("User", {...})
```

### Empty list returned

If using custom `__tablename__`, ensure you're on v0.10.6+:

```python
@db.model
class User:
    id: str
    __tablename__ = "custom_users"

# Fixed in v0.10.6 - uses correct table name
users = await db.express.list("User")
```

### Pattern 4: Get User by Email (find_one vs read)

```python
# Use read() for primary key lookups
user = await db.express.read("User", "user-001")

# Use find_one() for non-primary key lookups
user = await db.express.find_one("User", {"email": "alice@example.com"})
user = await db.express.find_one("User", {"username": "alice"})
user = await db.express.find_one("User", {"status": "active", "role": "admin"})

# find_one() requires non-empty filter (raises ValueError otherwise)
# For unfiltered single record, use list() with limit=1
first_user = (await db.express.list("User", limit=1))[0] if await db.express.count("User") > 0 else None
```

## Related Documentation

- **User Guide**: `sdk-users/apps/dataflow/guides/express-dataflow.md`
- **CRUD Operations**: `dataflow-crud-operations.md`
- **Bulk Operations**: `dataflow-bulk-operations.md`
- **Performance Guide**: `dataflow-performance.md`

## Version History

- **v0.10.13**: Added `find_one()` method for single-record non-PK lookups
- **v0.10.6**: Initial ExpressDataFlow release with full CRUD and bulk operations
