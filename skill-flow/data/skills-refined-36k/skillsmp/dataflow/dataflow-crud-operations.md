---
name: dataflow-crud-operations
description: "Use 11 auto-generated DataFlow nodes for CRUD operations. Use when DataFlow CRUD, generated nodes, UserCreateNode, UserReadNode, create read update delete, basic operations, or single record operations."
---

# DataFlow CRUD Operations

Use the 11 automatically generated workflow nodes for Create, Read, Update, Delete, List, Upsert, and Count operations on DataFlow models.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> Related Skills: [`dataflow-models`](#), [`dataflow-queries`](#), [`dataflow-bulk-operations`](#), [`workflow-quickstart`](#)
> Related Subagents: `dataflow-specialist` (complex operations, troubleshooting)

## Quick Reference

- **11 Generated Nodes**: Create, Read, Update, Delete, List, Upsert, Count, BulkCreate, BulkUpdate, BulkDelete, BulkUpsert
- **Naming Pattern**: `{Model}{Operation}Node` (e.g., `UserCreateNode`)
- **Performance**: <1ms for single operations
- **String IDs**: Fully supported
- **Datetime Auto-Conversion**: ISO 8601 strings → datetime objects

## ⚠️ CRITICAL WARNING: CreateNode vs UpdateNode Patterns

**CreateNode and UpdateNode use FUNDAMENTALLY DIFFERENT parameter structures.** This is the #1 cause of 4+ hour debugging sessions for new DataFlow developers.

### Pattern Comparison

| Node Type | Pattern | Example |
|-----------|---------|---------|
| **CreateNode** | **FLAT** individual fields | `{"name": "Alice", "email": "alice@example.com"}` |
| **UpdateNode** | **NESTED** filter + fields | `{"filter": {"id": 1}, "fields": {"name": "Alice Updated"}}` |
| **BulkUpdateNode** | **NESTED** filter + fields | `{"filter": {"active": True}, "fields": {"status": "verified"}}` |

### CreateNode: FLAT Individual Fields

```python
# ✅ CORRECT - All fields at top level
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",            # ← Individual field 1
    "email": "alice@example.com", # ← Individual field 2
    "age": 30                   # ← Individual field 3
})

# ❌ WRONG - Do NOT nest under 'data'
workflow.add_node("UserCreateNode", "create", {
    "data": {  # ← This creates a FIELD named "data"!
        "name": "Alice",
        "email": "alice@example.com"
    }
})
# Error: "missing required inputs: name, email, age"
```

### UpdateNode: NESTED filter + fields

```python
# ✅ CORRECT - Nested structure with filter + fields
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": 1},  # ← Which records to update
    "fields": {            # ← What to change
        "name": "Alice Updated",
        "age": 31
    }
})

# ❌ WRONG - Do NOT use flat fields like CreateNode
workflow.add_node("UserUpdateNode", "update", {
    "id": 1,          # ← Wrong! This is CreateNode pattern
    "name": "Alice"
})
# Error: "UpdateNode requires 'filter' and 'fields' parameters"
```

### Why Different?

- **CreateNode**: You're providing ALL data for a NEW record
  → Flat structure makes sense (like object construction)

- **UpdateNode**: You need to specify:
  1. **WHICH** records to update (`filter`)
  2. **WHAT** to change (`fields`)
  → Nested structure separates concerns

### Auto-Managed Fields

⚠️ **IMPORTANT**: DataFlow automatically manages these fields:
- `created_at` - Set automatically on create
- `updated_at` - Updated automatically on update

**Do NOT include them in your parameters!**

```python
# ❌ WRONG
fields = {
    "name": "Alice",
    "updated_at": datetime.now()  # ← Remove this!
}

# ✅ CORRECT
fields = {
    "name": "Alice"
    # updated_at is set automatically
}
```

## Core Pattern

```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

db = DataFlow()

@db.model
class User:
    name: str
    email: str
    active: bool = True

# Automatically generates 11 nodes:
# CRUD: UserCreateNode, UserReadNode, UserUpdateNode, UserDeleteNode, UserListNode, UserUpsertNode, UserCountNode
# Bulk: UserBulkCreateNode, UserBulkUpdateNode, UserBulkDeleteNode, UserBulkUpsertNode

workflow = WorkflowBuilder()

# CREATE - Single record
workflow.add_node("UserCreateNode", "create_user", {
    "name": "Alice",
    "email": "alice@example.com"
})

# READ - Single record by ID
workflow.add_node("UserReadNode", "read_user", {
    "filter": {"id": 1}
})

# UPDATE - Single record
workflow.add_node("UserUpdateNode", "update_user", {
    "filter": {"id": 1},
    "fields": {"active": False}
})

# DELETE - Single record
workflow.add_node("UserDeleteNode", "delete_user", {
    "filter": {"id": 1}
})

# LIST - Query with filters
workflow.add_node("UserListNode", "list_users", {
    "filter": {"active": True},
    "limit": 10
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Common Use Cases

- **User Registration**: Create user account with validation
- **Profile Lookup**: Read user by ID or email
- **Account Updates**: Update user profile fields
- **Account Deletion**: Soft or hard delete users
- **User Search**: List users with filters and pagination
- **Timestamp Handling**: Seamless datetime integration with PythonCodeNode

## Generated Nodes Reference

### Basic CRUD Nodes (5)

| Node | Purpose | Performance | Parameters |
|------|---------|-------------|------------|
| `{Model}CreateNode` | Insert single record | <1ms | All model fields |
| `{Model}ReadNode` | Select by ID | <1ms | `id` or `conditions` |
| `{Model}UpdateNode` | Update single record | <1ms | `id`, `updates` |
| `{Model}DeleteNode` | Delete single record | <1ms | `id`, `soft_delete` |
| `{Model}ListNode` | Query with filters | <10ms | `filter`, `limit`, `order_by` |

### Bulk Operation Nodes (4)

| Node | Purpose | Performance | Parameters |
|------|---------|-------------|------------|
| `{Model}BulkCreateNode` | Insert multiple records | 1000+/sec | `data`, `batch_size` |
| `{Model}BulkUpdateNode` | Update multiple records | 5000+/sec | `filter`, `updates` |
| `{Model}BulkDeleteNode` | Delete multiple records | 10000+/sec | `filter`, `soft_delete` |
| `{Model}BulkUpsertNode` | Insert or update | 3000+/sec | `data`, `unique_fields` |

## Key Parameters / Options

### CreateNode Parameters

```python
workflow.add_node("UserCreateNode", "create", {
    # Required: Model fields
    "name": "John Doe",
    "email": "john@example.com",

    # Optional: Control behavior
    "return_id": True,  # Return created ID (default: True)
    "validate": True    # Validate before insert (default: True)
})
```

### ReadNode Parameters

```python
# Option 1: By ID (recommended)
workflow.add_node("UserReadNode", "read", {
    "filter": {"id": 123}
})

# Option 2: By other conditions
workflow.add_node("UserReadNode", "read", {
    "filter": {"email": "john@example.com"},
    "raise_on_not_found": True  # Error if not found
})

# Option 3: String IDs
workflow.add_node("SessionReadNode", "read_session", {
    "filter": {"id": "session-uuid-string"}  # String IDs preserved
})
```

### UpdateNode Parameters

```python
workflow.add_node("UserUpdateNode", "update", {
    # Target record(s) - REQUIRED
    "filter": {"id": 123},
    # OR multiple conditions
    # "filter": {"email": "john@example.com", "active": True},

    # Fields to update - REQUIRED
    "fields": {
        "active": False
        # NOTE: Do NOT include updated_at - it's automatic!
    },

    # Options
    "return_updated": True,  # Return updated record
    "validate": True         # Validate before update
})
```

### DeleteNode Parameters

```python
workflow.add_node("UserDeleteNode", "delete", {
    # Target record - REQUIRED
    "filter": {"id": 123},

    # Soft delete (preserve data)
    "soft_delete": True,  # Sets deleted_at, doesn't remove

    # Hard delete (permanent)
    "hard_delete": False  # Permanently removes
})
```

### ListNode Parameters

```python
workflow.add_node("UserListNode", "list", {
    # Filters (MongoDB-style)
    "filter": {
        "active": True,
        "age": {"$gt": 18}
    },

    # Sorting
    "order_by": ["-created_at"],  # Descending by created_at

    # Pagination
    "limit": 10,
    "offset": 0,

    # Field selection
    "fields": ["id", "name", "email"],  # Only return these fields

    # Count only
    "count_only": False  # Set True to just count matches
})
```

## Common Mistakes

### Mistake 1: Wrapping CreateNode Fields in 'data'

```python
# ❌ WRONG - 'data' is treated as a field name
workflow.add_node("UserCreateNode", "create", {
    "data": {  # This creates a FIELD named "data"
        "name": "Alice",
        "email": "alice@example.com"
    }
})
# Error: "missing required inputs: name, email"
```

**Fix: Use Flat Fields**

```python
# ✅ CORRECT - Fields at top level
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com"
})
```

### Mistake 2: Using CreateNode Pattern on UpdateNode

```python
# ❌ WRONG - Flat fields on UpdateNode
workflow.add_node("UserUpdateNode", "update", {
    "id": 1,          # This is CreateNode pattern!
    "name": "Alice"
})
# Error: "UpdateNode requires 'filter' and 'fields' parameters"
```

**Fix: Use Nested filter + fields**

```python
# ✅ CORRECT - Nested structure for UpdateNode
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": 1},
    "fields": {"name": "Alice"}
})
```

### Mistake 3: Including Auto-Managed Fields

```python
# ❌ WRONG - Manually setting updated_at
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": 1},
    "fields": {
        "name": "Alice",
        "updated_at": datetime.now()  # Don't do this!
    }
})
# Error: "multiple assignments to same column 'updated_at'"
```

**Fix: Remove Auto-Managed Fields**

```python
# ✅ CORRECT - Let DataFlow handle updated_at
workflow.add_node("UserUpdateNode", "update", {
    "filter": {"id": 1},
    "fields": {
        "name": "Alice"
        # updated_at is automatic
    }
})
```

### Mistake 4: Missing .build() Call

```python
# ❌ WRONG - missing .build()
workflow.add_node("UserCreateNode", "create", {...})
results, run_id = runtime.execute(workflow)  # ERROR
```

**Fix: Always Call .build()**

```python
# ✅ CORRECT
workflow.add_node("UserCreateNode", "create", {...})
results, run_id = runtime.execute(workflow.build())
```

### Mistake 5: Using Template Syntax for Parameters

```python
# ❌ WRONG - ${} conflicts with PostgreSQL
workflow.add_node("OrderCreateNode", "create", {
    "customer_id": "${create_customer.id}"  # FAILS
})
```

**Fix: Use Workflow Connections**

```python
# ✅ CORRECT - use connections for dynamic values
workflow.add_node("OrderCreateNode", "create", {
    "total": 100.0
})
workflow.add_connection("create_customer", "id", "create", "customer_id")
```

## Automatic Datetime Conversion

DataFlow automatically converts ISO 8601 datetime strings to Python datetime objects for all datetime fields. This enables seamless integration with PythonCodeNode and external data sources.

### Supported ISO 8601 Formats

- **Basic**: `2024-01-01T12:00:00`
- **With microseconds**: `2024-01-01T12:00:00.123456`
- **With timezone Z**: `2024-01-01T12:00:00Z`
- **With timezone offset**: `2024-01-01T12:00:00+05:30`

### Example: PythonCodeNode → CreateNode

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()

# PythonCodeNode generates ISO 8601 string
workflow.add_node("PythonCodeNode", "generate_timestamp", {
    "code": """
from datetime import datetime
result = {"registration_date": datetime.now().isoformat()}
    """
})

# CreateNode automatically converts to datetime
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com",
    "registration_date": "{{generate_timestamp.registration_date}}"  # ISO string → datetime
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())

# Database stores as proper datetime type
created_user = results["create"]["result"]
print(f"User registered at: {created_user['registration_date']}")
```

### Example: UpdateNode with Datetime

```python
# PythonCodeNode generates timestamp
workflow.add_node("PythonCodeNode", "generate_last_login", {
    "code": """
from datetime import datetime
result = {"last_login": datetime.now().isoformat()}
    """
})

# UpdateNode automatically converts
workflow.add_node("UserUpdateNode", "update_last_login", {
    "filter": {"id": 1},
    "fields": {
        "last_login": "{{generate_last_login.last_login}}"  # ISO string → datetime
    }
})
```

### Example: BulkCreateNode with Datetime

```python
# Prepare bulk data with ISO strings
workflow.add_node("PythonCodeNode", "generate_bulk_data", {
    "code": """
from datetime import datetime, timedelta
import json

users = []
for i in range(100):
    users.append({
        "name": f"User {i}",
        "email": f"user{i}@example.com",
        "joined_at": (datetime.now() - timedelta(days=i)).isoformat()
    })

result = {"users": json.dumps(users)}
    """
})

# BulkCreateNode automatically converts all datetime strings
workflow.add_node("UserBulkCreateNode", "bulk_import", {
    "data": "{{generate_bulk_data.users}}"  # All ISO strings → datetime
})
```

### Backward Compatibility

Existing code passing datetime objects continues to work without changes:

```python
from datetime import datetime

# Still works - datetime objects accepted
workflow.add_node("UserCreateNode", "create", {
    "name": "Bob",
    "email": "bob@example.com",
    "registration_date": datetime.now()  # Direct datetime object
})

# Also works - ISO strings now auto-converted
workflow.add_node("UserCreateNode", "create_from_string", {
    "name": "Charlie",
    "email": "charlie@example.com",
    "registration_date": "2024-01-15T10:30:00"  # ISO string → datetime
})
```

### Applies To All CRUD Nodes

Datetime auto-conversion works on:
- ✅ `UserCreateNode` - Single record creation
- ✅ `UserUpdateNode` - Single record updates
- ✅ `UserBulkCreateNode` - Bulk record creation
- ✅ `UserBulkUpdateNode` - Bulk record updates
- ✅ `UserBulkUpsertNode` - Bulk upsert operations

### Common Use Cases

**External API Integration:**
```python
# API returns ISO 8601 strings
workflow.add_node("PythonCodeNode", "fetch_api_data", {
    "code": """
import requests
response = requests.get("https://api.example.com/users")
result = response.json()  # Contains ISO datetime strings
    """
})

# Automatically converted to datetime
workflow.add_node("UserBulkCreateNode", "import_api_users", {
    "data": "{{fetch_api_data.users}}"
})
```

**CSV Import:**
```python
# CSV contains date strings
workflow.add_node("PythonCodeNode", "parse_csv", {
    "code": """
import csv
from datetime import datetime

users = []
with open('users.csv') as f:
    for row in csv.DictReader(f):
        users.append({
            "name": row["name"],
            "email": row["email"],
            "registered": datetime.fromisoformat(row["registered_date"]).isoformat()
        })

result = {"users": users}
    """
})

workflow.add_node("UserBulkCreateNode", "import_csv", {
    "data": "{{parse_csv.users}}"  # ISO strings auto-converted
})
```

## Related Patterns

- **For model definition**: See [`dataflow-models`](#)
- **For query filters**: See [`dataflow-queries`](#)
- **For bulk operations**: See [`dataflow-bulk-operations`](#)
- **For result access**: See [`dataflow-result-access`](#)
- **For Nexus integration**: See [`dataflow-nexus-integration`](#)

## When to Escalate to Subagent

Use `dataflow-specialist` subagent when:
- Designing complex multi-step CRUD workflows
- Implementing custom validation logic
- Troubleshooting node execution errors
- Optimizing query performance
- Setting up advanced filtering patterns
- Working with relationships between models

## Documentation References

### Primary Sources
- **README**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L304-L381)
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md#L83-L234)
- **Node API**: [`sdk-users/apps/dataflow/docs/api/nodes.md`](../../../../sdk-users/apps/dataflow/docs/api/nodes.md)

### Related Documentation
- **Query Patterns**: [`sdk-users/apps/dataflow/docs/development/query-patterns.md`](../../../../sdk-users/apps/dataflow/docs/development/query-patterns.md)
- **CRUD Guide**: [`sdk-users/apps/dataflow/docs/development/crud.md`](../../../../sdk-users/apps/dataflow/docs/development/crud.md)
- **Workflow Nodes**: [`sdk-users/apps/dataflow/docs/workflows/nodes.md`](../../../../sdk-users/apps/dataflow/docs/workflows/nodes.md)

### Specialist Reference
- **DataFlow Specialist**: [`.claude/skills/dataflow-specialist.md`](../../dataflow-specialist.md#L211-L224)

## Examples

### Example 1: Complete User CRUD Workflow

```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

db = DataFlow()

@db.model
class User:
    name: str
    email: str
    active: bool = True

workflow = WorkflowBuilder()

# Create user
workflow.add_node("UserCreateNode", "create", {
    "name": "Alice",
    "email": "alice@example.com"
})

# Read created user
workflow.add_node("UserReadNode", "read", {
    "filter": {}  # Will be provided via connection
})
workflow.add_connection("create", "id", "read", "filter.id")

# Update user
workflow.add_node("UserUpdateNode", "update", {
    "filter": {},  # Will be provided via connection
    "fields": {"active": False}
})
workflow.add_connection("read", "id", "update", "filter.id")

# List all inactive users
workflow.add_node("UserListNode", "list_inactive", {
    "filter": {"active": False}
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())

# Access results
created_user = results["create"]["result"]
print(f"Created user: {created_user['name']}")

inactive_users = results["list_inactive"]["result"]
print(f"Found {len(inactive_users)} inactive users")
```

### Example 2: String ID Operations

```python
@db.model
class SsoSession:
    id: str
    user_id: str
    state: str = 'active'

workflow = WorkflowBuilder()

# Create with string ID
session_id = "session-80706348-0456-468b-8851-329a756a3a93"
workflow.add_node("SsoSessionCreateNode", "create_session", {
    "id": session_id,  # String ID preserved
    "user_id": "user-123",
    "state": "active"
})

# Read by string ID
workflow.add_node("SsoSessionReadNode", "read_session", {
    "filter": {"id": session_id}  # No conversion needed
})

# Update by string ID
workflow.add_node("SsoSessionUpdateNode", "update_session", {
    "filter": {"id": session_id},
    "fields": {"state": "expired"}
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### Example 3: Soft Delete Pattern

```python
@db.model
class Customer:
    name: str
    email: str

    __dataflow__ = {
        'soft_delete': True  # Enable soft deletes
    }

workflow = WorkflowBuilder()

# Soft delete (preserves data)
workflow.add_node("CustomerDeleteNode", "soft_delete_customer", {
    "filter": {"id": 123},
    "soft_delete": True  # Sets deleted_at timestamp
})

# List active customers (excludes soft-deleted)
workflow.add_node("CustomerListNode", "active_customers", {
    "filter": {"active": True}
    # Soft-deleted records automatically excluded
})

# List including soft-deleted
workflow.add_node("CustomerListNode", "all_customers", {
    "filter": {},
    "include_deleted": True  # Include soft-deleted records
})
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Node 'UserCreateNode' not found` | Model not defined with @db.model | Add @db.model decorator to class |
| `KeyError: 'id'` in results | Wrong result access pattern | Use `results["node"]["result"]["id"]` |
| `ValidationError: Missing required field` | Field without default | Provide value or add default to model |
| `IntegrityError: duplicate key` | Unique constraint violation | Check for existing record before creating |
| `NotFoundError: Record not found` | Invalid ID or deleted record | Verify ID exists and isn't soft-deleted |

## Quick Tips

- String IDs fully supported - no conversion needed
- Use connections for dynamic parameters, NOT template syntax
- Access results via `results["node"]["result"]` pattern
- Soft deletes preserve data with `deleted_at` timestamp
- ListNode excludes soft-deleted by default
- Use `count_only=True` for pagination counts
- ReadNode can use ID or conditions
- UpdateNode returns updated record if `return_updated=True`


## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow CRUD, generated nodes, UserCreateNode, UserReadNode, UserUpdateNode, UserDeleteNode, UserListNode, create read update delete, basic operations, single record, DataFlow operations, database operations, CRUD patterns, node operations -->
