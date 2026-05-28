---
name: dataflow-quickstart
description: "Get started with Kailash DataFlow zero-config database framework. Use when asking 'DataFlow tutorial', 'DataFlow quick start', '@db.model', 'DataFlow setup', 'database framework', or 'how to use DataFlow'."
---

# DataFlow Quick Start

Zero-config database framework built on Core SDK with automatic node generation from models.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `CRITICAL`
> Related Skills: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md), [`dataflow-models`](dataflow-models.md), [`dataflow-queries`](dataflow-queries.md)
> Related Subagents: `dataflow-specialist` (enterprise features, migrations), `nexus-specialist` (DataFlow+Nexus integration)

## Quick Reference

- **Install**: `pip install kailash-dataflow`
- **Import**: `from dataflow import DataFlow`
- **Pattern**: `DataFlow() → @db.model → 9 nodes generated automatically`
- **NOT an ORM**: Workflow-native database framework
- **SQL Databases**: PostgreSQL, MySQL, SQLite (100% feature parity, 9 nodes per @db.model)
- **Document Database**: MongoDB (flexible schema, 8 specialized nodes)
- **Vector Search**: PostgreSQL pgvector (semantic search, 3 vector nodes)
- **Key Feature**: Automatic node generation from models or schema

## 30-Second Quick Start

```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

# 1. Zero-config initialization
db = DataFlow()  # Auto-detects: SQLite (dev) or PostgreSQL (prod via DATABASE_URL)

# 2. Define model - automatically generates 9 node types
@db.model
class User:
    name: str
    email: str
    active: bool = True

# 3. Use generated nodes immediately
workflow = WorkflowBuilder()

# UserCreateNode, UserReadNode, UserUpdateNode, UserDeleteNode, UserListNode,
# UserBulkCreateNode, UserBulkUpdateNode, UserBulkDeleteNode, UserBulkUpsertNode
# All created automatically!

workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com"
})

workflow.add_node("UserListNode", "list", {
    "filter": {"active": True},
    "limit": 10
})

# 4. Execute
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
print(f"Created user ID: {results['create']['id']}")
```

## What is DataFlow?

**DataFlow is NOT an ORM** - it's a workflow-native database framework that generates Kailash workflow nodes from Python models.

### DataFlow vs Traditional ORM

| Feature | Traditional ORM | DataFlow |
|---------|----------------|----------|
| **Usage** | Direct instantiation (`User()`) | Workflow nodes (`UserCreateNode`) |
| **Operations** | Method calls (`user.save()`) | Workflow execution |
| **Transactions** | Manual management | Distributed transactions built-in |
| **Caching** | External integration | Enterprise caching included |
| **Multi-tenancy** | Custom code | Automatic isolation |
| **Scalability** | Vertical scaling | Horizontal scaling built-in |

## Generated Node Types (9 per Model)

Each `@db.model` automatically creates:

| Node | Purpose | Example Config |
|------|---------|----------------|
| **{Model}CreateNode** | Single insert | `{"name": "John", "email": "john@example.com"}` |
| **{Model}ReadNode** | Single select | `{"id": 123}` or `{"filter": {"email": "alice@example.com"}}` |
| **{Model}UpdateNode** | Single update | `{"id": 123, "name": "Jane"}` |
| **{Model}DeleteNode** | Single delete | `{"id": 123}` or `{"soft_delete": True}` |
| **{Model}ListNode** | Query with filters | `{"filter": {"age": {"$gt": 18}}, "limit": 10}` |
| **{Model}BulkCreateNode** | Bulk insert | `{"data": [...], "batch_size": 1000}` |
| **{Model}BulkUpdateNode** | Bulk update | `{"filter": {...}, "fields": {...}}` |
| **{Model}BulkDeleteNode** | Bulk delete | `{"filter": {...}}` |
| **{Model}BulkUpsertNode** | Insert or update | `{"data": [...], "match_fields": ["email"]}` |

## Database Connection Patterns

### Option 1: Zero-Config (Development)
```python
db = DataFlow()  # Defaults to SQLite in-memory
```

### Option 2: SQLite File (Development/Testing)
```python
db = DataFlow("sqlite:///app.db")
```

### Option 3: PostgreSQL or MySQL (Production)
```python
# PostgreSQL (recommended for production)
db = DataFlow("postgresql://user:password@localhost:5432/database")

# MySQL (web hosting, existing infrastructure)
db = DataFlow("mysql://user:password@localhost:3306/database")

# Special characters in passwords supported
db = DataFlow("postgresql://admin:MySecret#123$@localhost/db")
```

### Option 4: Environment Variable (Recommended)
```bash
# Set environment variable
export DATABASE_URL="postgresql://user:pass@localhost/db"
```
```python
# DataFlow reads automatically
db = DataFlow()
```

## MongoDB-Style Queries

DataFlow uses MongoDB query syntax that works across all SQL databases (PostgreSQL, MySQL, SQLite):

```python
workflow.add_node("UserListNode", "search", {
    "filter": {
        "age": {"$gt": 18, "$lt": 65},           # age BETWEEN 18 AND 65
        "name": {"$regex": "^John"},              # name LIKE 'John%'
        "department": {"$in": ["eng", "sales"]},  # department IN (...)
        "status": {"$ne": "inactive"}             # status != 'inactive'
    },
    "order_by": ["-created_at"],  # Sort descending
    "limit": 10,
    "offset": 0
})
```

## Common Use Cases

- **CRUD Applications**: Automatic node generation for create/read/update/delete
- **Data Import**: Bulk operations for high-speed data loading (10k+ records/sec)
- **SaaS Platforms**: Built-in multi-tenancy and tenant isolation
- **Analytics**: Complex queries with MongoDB-style syntax
- **Existing Databases**: Connect safely with `existing_schema_mode=True`

## Working with Existing Databases

### Safe Connection Mode
```python
# Connect to existing database WITHOUT modifying schema
db = DataFlow(
    database_url="postgresql://user:pass@localhost/existing_db",
    auto_migrate=False,          # Don't create/modify tables
    existing_schema_mode=True    # Maximum safety
)

# Discover existing tables
schema = db.discover_schema(use_real_inspection=True)
print(f"Found tables: {list(schema.keys())}")

# Register existing tables as models (no @db.model needed)
result = db.register_schema_as_models(tables=['users', 'orders'])

# Use generated nodes immediately
workflow = WorkflowBuilder()
user_nodes = result['generated_nodes']['users']

workflow.add_node(user_nodes['list'], "get_users", {
    "filter": {"active": True},
    "limit": 10
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Common Mistakes

### ❌ Mistake 1: Direct Model Instantiation
```python
# Wrong - models are NOT instantiable
user = User(name="John")  # ERROR!
```

### ✅ Fix: Use Generated Nodes
```python
# Correct - use workflow nodes
workflow.add_node("UserCreateNode", "create", {
    "name": "John",
    "email": "john@example.com"
})
```

### ❌ Mistake 2: Wrong Template Syntax
```python
# Wrong - DataFlow uses ${} syntax in connections, not {{}
}
workflow.add_node("OrderCreateNode", "create", {
    "customer_id": "{{customer.id}}"  # ERROR!
})
```

### ✅ Fix: Use Connections
```python
# Correct - use explicit connections
workflow.add_connection("customer", "id", "create_order", "customer_id")
```

### ❌ Mistake 3: String Datetime Values
```python
# Wrong - datetime as string
workflow.add_node("OrderCreateNode", "create", {
    "due_date": datetime.now().isoformat()  # ERROR!
})
```

### ✅ Fix: Native Datetime Objects
```python
# Correct - use native datetime
from datetime import datetime

workflow.add_node("OrderCreateNode", "create", {
    "due_date": datetime.now()  # ✓
})
```

## Async Usage (FastAPI, Async Workflows)

### Basic Pattern

```python
from dataflow import DataFlow
from kailash.runtime import AsyncLocalRuntime
from kailash.workflow.builder import WorkflowBuilder

# Initialize DataFlow
db = DataFlow("postgresql://localhost:5432/mydb")

@db.model
class User:
    id: str
    name: str
    email: str

# IMPORTANT: Use AsyncLocalRuntime in async contexts
async def create_user():
    workflow = WorkflowBuilder()
    workflow.add_node("UserCreateNode", "create", {
        "id": "user-123",
        "name": "Alice",
        "email": "alice@example.com"
    })

    # ✅ Use AsyncLocalRuntime for async contexts
    runtime = AsyncLocalRuntime()
    results, run_id = await runtime.execute_workflow_async(workflow.build(), inputs={})
    return results["create"]["id"]
```

### FastAPI Integration

**⚠️ Docker/FastAPI Requires `auto_migrate=False`**: Due to event loop boundary issues, you must use the lifespan pattern.

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dataflow import DataFlow
from kailash.runtime import AsyncLocalRuntime
from kailash.workflow.builder import WorkflowBuilder
import uuid

# ⚠️ CRITICAL: auto_migrate=False is REQUIRED for Docker/FastAPI
db = DataFlow(
    "postgresql://localhost:5432/mydb",
    auto_migrate=False  # REQUIRED - auto_migrate=True fails in Docker/FastAPI
)

@db.model
class User:
    id: str
    name: str
    email: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_tables_async()  # Create tables in FastAPI's event loop
    yield
    await db.close_async()

app = FastAPI(lifespan=lifespan)

@app.post("/users")
async def create_user(name: str, email: str):
    workflow = WorkflowBuilder()
    workflow.add_node("UserCreateNode", "create", {
        "id": f"user-{uuid.uuid4()}",
        "name": name,
        "email": email
    })

    runtime = AsyncLocalRuntime()
    results, _ = await runtime.execute_workflow_async(workflow.build(), inputs={})
    return results["create"]
```

**⚠️ Docker/FastAPI REQUIRES Manual Pattern**:
`auto_migrate=False` + `create_tables_async()` in lifespan is **REQUIRED** for Docker/FastAPI due to event loop boundary limitations. Database connections are bound to the event loop they're created in - connections from async_safe_run's thread pool cannot be used in uvicorn's main loop.

## DataFlow + Nexus Integration

**CRITICAL**: Use these settings to avoid blocking/slow startup:

```python
from dataflow import DataFlow
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

# Step 1: Create Nexus FIRST with auto_discovery=False
app = Nexus(auto_discovery=False)  # CRITICAL: Prevents blocking

# Step 2: Create DataFlow with enable_model_persistence=False
db = DataFlow(
    "postgresql://user:pass@localhost/db",
    enable_model_persistence=False,  # CRITICAL: Prevents 5-10s delay, fast startup
    auto_migrate=False,              # v0.9.1: Prevents async deadlock
    migration_enabled=False          # v0.9.1: Prevents async deadlock
)

# Step 3: Define models
@db.model
class User:
    name: str
    email: str

# Step 4: Register workflows manually
workflow = WorkflowBuilder()
workflow.add_node("UserCreateNode", "create", {"name": "Alice", "email": "alice@example.com"})
app.register("create_user", workflow.build())

# Fast startup: <2 seconds!
app.start()
```

## Related Patterns

- **Model definition**: [`dataflow-models`](dataflow-models.md)
- **Query patterns**: [`dataflow-queries`](dataflow-queries.md)
- **Bulk operations**: [`dataflow-bulk-ops`](dataflow-bulk-ops.md)
- **Nexus integration**: [`dataflow-nexus-integration`](../../5-cross-cutting/integrations/dataflow-nexus-integration.md)
- **Migration guide**: [`dataflow-migration-quick`](dataflow-migration-quick.md)

## When to Escalate to Subagent

Use `dataflow-specialist` subagent when:
- Implementing enterprise migration system (8 components)
- Setting up multi-tenant architecture
- Configuring distributed transactions
- Production deployment and optimization
- Complex foreign key relationships
- Performance tuning and caching strategies

Use `nexus-specialist` when:
- Integrating DataFlow with Nexus platform
- Troubleshooting blocking/slow startup issues
- Multi-channel deployment (API/CLI/MCP)

## Documentation References

### Primary Sources
- **DataFlow README**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md)
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md)
- **Quick Start Guide**: [`sdk-users/apps/dataflow/docs/getting-started/quickstart.md`](../../../../sdk-users/apps/dataflow/docs/getting-started/quickstart.md)

### Related Documentation
- **User Guide**: [`sdk-users/apps/dataflow/docs/USER_GUIDE.md`](../../../../sdk-users/apps/dataflow/docs/USER_GUIDE.md)
- **Query Patterns**: [`sdk-users/apps/dataflow/docs/development/query-patterns.md`](../../../../sdk-users/apps/dataflow/docs/development/query-patterns.md)
- **Model Definition**: [`sdk-users/apps/dataflow/docs/development/models.md`](../../../../sdk-users/apps/dataflow/docs/development/models.md)
- **Bulk Operations**: [`sdk-users/apps/dataflow/docs/development/bulk-operations.md`](../../../../sdk-users/apps/dataflow/docs/development/bulk-operations.md)

### Examples
- **Basic CRUD**: [`sdk-users/apps/dataflow/examples/01_basic_crud.py`](../../../../sdk-users/apps/dataflow/examples/01_basic_crud.py)
- **Advanced Features**: [`sdk-users/apps/dataflow/examples/02_advanced_features.py`](../../../../sdk-users/apps/dataflow/examples/02_advanced_features.py)

## Quick Tips

- 💡 **Zero-config first**: Start with `DataFlow()` - no configuration needed
- 💡 **9 nodes per model**: Remember - Create, Read, Update, Delete, List, Bulk(Create/Update/Delete/Upsert)
- 💡 **MongoDB queries**: Use familiar syntax that works across all SQL databases (PostgreSQL/MySQL/SQLite)
- 💡 **String IDs**: Fully supported - no forced integer conversion
- 💡 **Existing databases**: Use `existing_schema_mode=True` for safety
- 💡 **Nexus integration**: Set `enable_model_persistence=False` + `auto_discovery=False` to avoid blocking
- 💡 **Clean logs (v0.10.12+)**: Use `LoggingConfig.production()` for production, `LoggingConfig.development()` for debugging

<!-- Trigger Keywords: DataFlow tutorial, DataFlow quick start, @db.model, DataFlow setup, database framework, how to use DataFlow, DataFlow installation, DataFlow guide, zero-config database, automatic node generation, DataFlow example, start with DataFlow -->
