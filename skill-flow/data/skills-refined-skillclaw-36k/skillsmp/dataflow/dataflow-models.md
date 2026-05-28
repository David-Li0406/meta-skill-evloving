---
name: dataflow-models
description: "Define DataFlow models with @db.model decorator. Use when creating DataFlow models, defining database schemas, model setup, @db.model, table definitions, or field types."
---

# DataFlow Model Definition

Define database models using the `@db.model` decorator that automatically generates 11 workflow nodes for CRUD operations.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `CRITICAL`
> Related Skills: [`dataflow-quickstart`](#), [`dataflow-crud-operations`](#), [`dataflow-queries`](#), [`dataflow-bulk-operations`](#)
> Related Subagents: `dataflow-specialist` (complex models, enterprise features)

## Quick Reference

- **Decorator**: `@db.model` on Python class
- **Type Hints**: Required for all fields (`name: str`, `age: int`)
- **Generated Nodes**: 11 per model (Create, Read, Update, Delete, List, Upsert, Count, BulkCreate, BulkUpdate, BulkDelete, BulkUpsert)
- **String IDs**: Fully supported (no integer conversion)
- **Field Config**: Use `__dataflow__` dict for features

## Core Pattern

```python
from dataflow import DataFlow
from typing import Optional
from datetime import datetime
from decimal import Decimal

db = DataFlow()

# Basic model definition
@db.model
class User:
    # Required fields (no default)
    name: str
    email: str

    # Optional fields (with defaults)
    active: bool = True
    role: str = "user"

    # Auto-populated timestamps
    created_at: datetime = None
    updated_at: datetime = None

# String ID model
@db.model
class Session:
    id: str  # String IDs preserved throughout
    user_id: str
    state: str = 'active'

# Automatically generates 11 nodes:
# CRUD: UserCreateNode, UserReadNode, UserUpdateNode, UserDeleteNode, UserListNode, UserUpsertNode, UserCountNode
# Bulk: UserBulkCreateNode, UserBulkUpdateNode, UserBulkDeleteNode, UserBulkUpsertNode
```

## Common Use Cases

- **User Management**: Authentication, profiles, permissions
- **Product Catalog**: E-commerce products, inventory, pricing
- **Order Processing**: Orders, transactions, fulfillment
- **Content Management**: Articles, posts, media
- **Analytics**: Events, metrics, logs

## Step-by-Step Guide

1. **Import DataFlow**: `from dataflow import DataFlow`
2. **Initialize**: `db = DataFlow()`
3. **Define Class**: Python class with type hints
4. **Add Decorator**: `@db.model` above class
5. **Configure Fields**: Type hints + defaults
6. **Optional Config**: Add `__dataflow__` dict for features
7. **Use Nodes**: 11 nodes automatically available

## Key Parameters / Options

### Supported Python Types

| Python Type | SQL Type | Notes |
|------------|----------|-------|
| `str` | VARCHAR/TEXT | Use TEXT for unlimited content |
| `int` | INTEGER/BIGINT | Auto-detect size |
| `float` | FLOAT/DOUBLE | Precision configurable |
| `bool` | BOOLEAN | INTEGER in SQLite |
| `datetime` | TIMESTAMP | Auto timezone handling |
| `date` | DATE | Date only |
| `Decimal` | DECIMAL | Precise numbers (currency) |
| `dict` | JSON/JSONB | Structured data |
| `List[T]` | JSON/JSONB | Array data |
| `UUID` | UUID | Unique identifiers |

### Model Configuration (`__dataflow__`)

```python
@db.model
class Order:
    customer_id: int
    total: Decimal
    status: str = 'pending'

    __dataflow__ = {
        # Enterprise features
        'multi_tenant': True,     # Adds tenant_id field
        'soft_delete': True,      # Adds deleted_at field
        'versioned': True,        # Adds version field (optimistic locking)
        'audit_log': True,        # Tracks all changes

        # Table configuration
        'table_name': 'orders',   # Custom table name

        # Performance
        'cache_enabled': True,
        'cache_ttl': 300  # 5 minutes
    }
```

## Common Mistakes

### Mistake 1: Missing Type Hints

```python
# Wrong - no type hints
@db.model
class User:
    name = ""  # Missing type hint
    age = 0    # Missing type hint
```

**Fix: Always Use Type Hints**

```python
# Correct - explicit types
@db.model
class User:
    name: str
    age: int
```

### Mistake 2: Forcing Integer IDs for String Data

```python
# Wrong - trying to force string ID to int
@db.model
class Session:
    id: int = None  # Will fail for string IDs like "session-uuid"
```

**Fix: Use String Type for String IDs**

```python
# Correct - string IDs fully supported
@db.model
class Session:
    id: str  # Preserves string IDs throughout workflow
    user_id: str
```

### Mistake 3: Wrong Type for Currency

```python
# Wrong - float loses precision
@db.model
class Product:
    price: float  # Precision errors for currency
```

**Fix: Use Decimal for Currency**

```python
# Correct - precise currency handling
from decimal import Decimal

@db.model
class Product:
    price: Decimal  # Exact precision
```

### Mistake 4: Unlimited Text in VARCHAR

```python
# Wrong - would limit content
@db.model
class Article:
    content: str  # Was VARCHAR(255), now TEXT
```

**Fix: Now Automatic - TEXT Type**

```python
# Correct - TEXT with unlimited content
@db.model
class Article:
    content: str  # Automatically TEXT (no length limit)
```

## Related Patterns

- **For CRUD operations**: See [`dataflow-crud-operations`](#)
- **For queries**: See [`dataflow-queries`](#)
- **For bulk operations**: See [`dataflow-bulk-operations`](#)
- **For existing databases**: See [`dataflow-existing-database`](#)
- **For enterprise features**: See [`dataflow-multi-tenancy`](#)

## When to Escalate to Subagent

Use `dataflow-specialist` subagent when:
- Designing complex multi-table relationships
- Implementing advanced indexing strategies
- Setting up multi-tenant isolation
- Configuring enterprise audit trails
- Optimizing for high-performance scenarios
- Troubleshooting migration issues

## Documentation References

### Primary Sources
- **Model Guide**: [`sdk-users/apps/dataflow/docs/development/models.md`](../../../../sdk-users/apps/dataflow/docs/development/models.md)
- **README**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md)
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md)

### Related Documentation
- **Query Patterns**: [`sdk-users/apps/dataflow/docs/development/query-patterns.md`](../../../../sdk-users/apps/dataflow/docs/development/query-patterns.md)
- **Bulk Operations**: [`sdk-users/apps/dataflow/docs/development/bulk-operations.md`](../../../../sdk-users/apps/dataflow/docs/development/bulk-operations.md)
- **Relationships**: [`sdk-users/apps/dataflow/docs/development/relationships.md`](../../../../sdk-users/apps/dataflow/docs/development/relationships.md)

### Specialist Reference
- **DataFlow Specialist**: [`.claude/skills/dataflow-specialist.md`](../../dataflow-specialist.md)

## Examples

### Example 1: E-commerce Product Model

```python
from dataflow import DataFlow
from decimal import Decimal
from typing import List, Optional

db = DataFlow()

@db.model
class Product:
    # Identity
    sku: str  # Unique product code
    name: str

    # Pricing (use Decimal for currency)
    price: Decimal
    cost: Decimal

    # Inventory
    stock: int = 0

    # Metadata (stored as JSON)
    attributes: dict = {}
    tags: List[str] = []

    # Status
    active: bool = True
    featured: bool = False

# Use generated nodes
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()
workflow.add_node("ProductCreateNode", "create_product", {
    "sku": "LAPTOP-001",
    "name": "Gaming Laptop",
    "price": Decimal("1299.99"),
    "cost": Decimal("899.99"),
    "stock": 50,
    "tags": ["gaming", "electronics"]
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### Example 2: Multi-Tenant Order Model

```python
@db.model
class Order:
    customer_id: int
    total: Decimal
    status: str = 'pending'

    # Enterprise features
    __dataflow__ = {
        'multi_tenant': True,     # Automatic tenant isolation
        'soft_delete': True,      # Preserve deleted data
        'versioned': True,        # Prevent concurrent modifications
        'audit_log': True         # Track all changes
    }

# Automatically adds:
# - tenant_id field (for multi-tenancy)
# - deleted_at field (for soft deletes)
# - version field (for optimistic locking)
# - Audit trail logging

workflow = WorkflowBuilder()
workflow.add_node("OrderCreateNode", "create_order", {
    "customer_id": 123,
    "total": Decimal("250.00"),
    "tenant_id": "tenant_abc"  # Automatic isolation
})
```

### Example 3: String ID Session Model

```python
@db.model
class SsoSession:
    id: str  # String IDs fully supported
    user_id: str
    provider: str
    state: str = 'active'
    expires_at: datetime = None

workflow = WorkflowBuilder()

# String IDs preserved throughout
session_id = "session-80706348-0456-468b-8851-329a756a3a93"
workflow.add_node("SsoSessionReadNode", "read_session", {
    "id": session_id  # No conversion - preserved as string
})

# Alternative: Use conditions for explicit control
workflow.add_node("SsoSessionReadNode", "read_session_alt", {
    "filter": {"id": session_id},
    "raise_on_not_found": True
})
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `AttributeError: 'User' object has no attribute...` | Missing type hint | Add type hint to field: `name: str` |
| `ValueError: String ID cannot be converted to int` | Model defined with wrong ID type | Use `id: str` for string IDs |
| `DataError: value too long for type character varying(255)` | Text field size limitation | DataFlow now uses TEXT type automatically for unlimited content |
| `Model not found in registry` | Model defined after initialization | Define models before using in workflows |
| `TypeError: Field() missing required positional argument` | Incorrect Field syntax | Use `Field(...)` not `field(...)` |

## Quick Tips

- Always use type hints for all fields
- Use `Decimal` for currency, not `float`
- String IDs fully supported - no conversion
- TEXT type now default - unlimited content
- Add `__dataflow__` for enterprise features
- Default values make fields optional
- `None` default for auto-populated fields
- Use `List[T]` and `dict` for complex data

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow model, @db.model, define model, model fields, database schema, model definition, table definition, DataFlow class, model decorator, database model, schema definition, model setup, field types, model configuration -->
