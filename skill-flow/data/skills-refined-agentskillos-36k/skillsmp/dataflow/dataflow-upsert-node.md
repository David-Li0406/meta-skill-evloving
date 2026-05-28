---
name: dataflow-upsert-node
description: "UpsertNode with custom conflict fields (conflict_on parameter) for natural keys and composite unique constraints. Use when insert-or-update, atomic upsert, natural key conflicts, email-based upsert, or conflict resolution."
---

# DataFlow UpsertNode - Custom Conflict Fields

Atomic insert-or-update operations with custom conflict detection using the `conflict_on` parameter.

> **Skill Metadata**
> Category: `dataflow/nodes`
> Priority: `HIGH`
> Related Skills: [`dataflow-crud-operations`](#), [`dataflow-bulk-operations`](#)
> Related Subagents: `dataflow-specialist` (complex upserts)

## Quick Reference

- **conflict_on Parameter**: Specify custom conflict detection fields
- **Natural Keys**: Use business identifiers like email, username, SKU
- **Composite Keys**: Multiple fields for unique constraints
- **Atomic Operation**: Single database round-trip
- **PostgreSQL/MySQL/SQLite**: Full support across all SQL databases

## ⚠️ CRITICAL: conflict_on Parameter

Use `conflict_on` to specify custom fields for conflict detection beyond the default `id` field.

```python
# ✅ CORRECT - Custom conflict field
workflow.add_node("UserUpsertNode", "upsert", {
    "where": {"email": "alice@example.com"},
    "conflict_on": ["email"],  # ← Detect conflicts on email
    "update": {"name": "Alice Updated"},
    "create": {
        "id": "user-123",
        "email": "alice@example.com",
        "name": "Alice"
    }
})

# ❌ WRONG - Missing conflict_on when using non-id field
workflow.add_node("UserUpsertNode", "upsert", {
    "where": {"id": "user-123"},  # ← Must use id
    "update": {"name": "Alice Updated"},
    "create": {
        "id": "user-123",
        "name": "Alice"
    }
})
```

## Single Field Conflicts

### Email-Based Upsert
```python
# Upsert user by email (natural key)
workflow.add_node("UserUpsertNode", "upsert_alice", {
    "where": {"email": "alice@example.com"},
    "conflict_on": ["email"],
    "update": {"name": "Alice Updated", "last_login": "2024-01-15"},
    "create": {
        "id": "user-123",
        "email": "alice@example.com",
        "name": "Alice",
        "last_login": "2024-01-15"
    }
})

# Database behavior:
# 1. If email exists → UPDATE name, last_login
# 2. If email doesn't exist → INSERT new record
```

### Username-Based Upsert
```python
workflow.add_node("UserUpsertNode", "upsert_user", {
    "where": {"username": "alice"},
    "conflict_on": ["username"],
    "update": {"profile_updated_at": "2024-01-15"},
    "create": {
        "id": "user-123",
        "username": "alice",
        "email": "alice@example.com"
    }
})
```

### SKU-Based Upsert (Inventory)
```python
workflow.add_node("ProductUpsertNode", "upsert_product", {
    "where": {"sku": "WIDGET-001"},
    "conflict_on": ["sku"],
    "update": {"stock_quantity": 100, "price": 29.99},
    "create": {
        "id": "prod-456",
        "sku": "WIDGET-001",
        "name": "Premium Widget",
        "stock_quantity": 100,
        "price": 29.99
    }
})
```

## Composite Key Conflicts

### Order Line Items (order_id + product_id)
```python
workflow.add_node("OrderItemUpsertNode", "upsert_item", {
    "where": {
        "order_id": "order-123",
        "product_id": "prod-456"
    },
    "conflict_on": ["order_id", "product_id"],  # ← Composite key
    "update": {"quantity": 10, "updated_at": "2024-01-15"},
    "create": {
        "id": "item-789",
        "order_id": "order-123",
        "product_id": "prod-456",
        "quantity": 5,
        "created_at": "2024-01-15"
    }
})
```

### User Roles (user_id + role_id)
```python
workflow.add_node("UserRoleUpsertNode", "assign_role", {
    "where": {
        "user_id": "user-123",
        "role_id": "role-admin"
    },
    "conflict_on": ["user_id", "role_id"],
    "update": {"granted_at": "2024-01-15"},
    "create": {
        "id": "ur-789",
        "user_id": "user-123",
        "role_id": "role-admin",
        "granted_at": "2024-01-15"
    }
})
```

### Time Series Data (sensor_id + timestamp)
```python
workflow.add_node("SensorReadingUpsertNode", "record_reading", {
    "where": {
        "sensor_id": "sensor-A1",
        "timestamp": "2024-01-15T10:00:00Z"
    },
    "conflict_on": ["sensor_id", "timestamp"],
    "update": {"value": 23.5, "corrected": True},
    "create": {
        "id": "reading-001",
        "sensor_id": "sensor-A1",
        "timestamp": "2024-01-15T10:00:00Z",
        "value": 23.5
    }
})
```

## Common Patterns

### 1. Idempotent API Requests
```python
# Handle duplicate API calls gracefully
workflow.add_node("OrderUpsertNode", "create_order", {
    "where": {"external_id": api_request_id},
    "conflict_on": ["external_id"],
    "update": {},  # No updates - just skip if exists
    "create": {
        "id": order_id,
        "external_id": api_request_id,
        "amount": 100.0,
        "status": "pending"
    }
})
# Result: First call creates, subsequent calls return existing order
```

### 2. Email-Based User Registration
```python
# Register or update user by email
workflow.add_node("UserUpsertNode", "register", {
    "where": {"email": user_email},
    "conflict_on": ["email"],
    "update": {"last_login": datetime.now()},
    "create": {
        "id": generate_id(),
        "email": user_email,
        "name": user_name,
        "created_at": datetime.now(),
        "last_login": datetime.now()
    }
})
```

### 3. Inventory Stock Updates
```python
# Update stock by SKU
workflow.add_node("ProductUpsertNode", "update_stock", {
    "where": {"sku": product_sku},
    "conflict_on": ["sku"],
    "update": {"stock_quantity": new_quantity},
    "create": {
        "id": generate_id(),
        "sku": product_sku,
        "name": product_name,
        "stock_quantity": new_quantity
    }
})
```

### 4. Configuration Settings
```python
# Upsert configuration by key
workflow.add_node("ConfigUpsertNode", "set_config", {
    "where": {"key": "feature_flag_x"},
    "conflict_on": ["key"],
    "update": {"value": "enabled", "updated_at": datetime.now()},
    "create": {
        "id": generate_id(),
        "key": "feature_flag_x",
        "value": "enabled",
        "created_at": datetime.now()
    }
})
```

### 5. Multi-Tenant Data
```python
# Upsert with tenant isolation
workflow.add_node("TenantConfigUpsertNode", "set_tenant_config", {
    "where": {
        "tenant_id": current_tenant_id,
        "key": "api_quota"
    },
    "conflict_on": ["tenant_id", "key"],  # ← Composite natural key
    "update": {"value": "10000"},
    "create": {
        "id": generate_id(),
        "tenant_id": current_tenant_id,
        "key": "api_quota",
        "value": "10000"
    }
})
```

## Database Behavior

### PostgreSQL
```sql
-- Generated SQL for conflict_on: ["email"]
INSERT INTO users (id, email, name)
VALUES ('user-123', 'alice@example.com', 'Alice')
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name, updated_at = CURRENT_TIMESTAMP
RETURNING *;
```

### MySQL
```sql
-- Generated SQL for conflict_on: ["email"]
INSERT INTO users (id, email, name)
VALUES ('user-123', 'alice@example.com', 'Alice')
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    updated_at = CURRENT_TIMESTAMP;
```

### SQLite
```sql
-- Generated SQL for conflict_on: ["email"]
INSERT INTO users (id, email, name)
VALUES ('user-123', 'alice@example.com', 'Alice')
ON CONFLICT (email)
DO UPDATE SET
    name = excluded.name,
    updated_at = CURRENT_TIMESTAMP;
```

## Best Practices

### 1. Use Natural Keys
```python
# ✅ CORRECT - Natural key (email)
workflow.add_node("UserUpsertNode", "upsert", {
    "where": {"email": "alice@example.com"},
    "conflict_on": ["email"],
    ...
})

# ❌ WRONG - Technical ID (defeats purpose of custom conflict_on)
workflow.add_node("UserUpsertNode", "upsert", {
    "where": {"id": "user-123"},
    "conflict_on": ["id"],  # ← Just use id-based upsert
    ...
})
```

### 2. Match Database Constraints
```python
# Ensure conflict_on matches UNIQUE constraint
@db.model
class User:
    id: str
    email: str
    name: str

    __dataflow__ = {
        'unique_constraints': [['email']]  # ← Must match conflict_on
    }

workflow.add_node("UserUpsertNode", "upsert", {
    "where": {"email": "alice@example.com"},
    "conflict_on": ["email"],  # ← Matches unique constraint
    ...
})
```

### 3. Composite Keys for Associations
```python
# ✅ CORRECT - Composite key for many-to-many
workflow.add_node("UserRoleUpsertNode", "assign", {
    "where": {"user_id": "user-123", "role_id": "role-admin"},
    "conflict_on": ["user_id", "role_id"],
    ...
})

# ❌ WRONG - Single field doesn't prevent duplicates
workflow.add_node("UserRoleUpsertNode", "assign", {
    "where": {"user_id": "user-123"},
    "conflict_on": ["user_id"],  # ← Can create duplicate roles!
    ...
})
```

## Troubleshooting

### ❌ Error: Unique constraint violation
**Cause:** Missing conflict_on parameter or mismatched fields

**Solution:**
```python
# ✅ Add conflict_on matching your unique constraint
workflow.add_node("UserUpsertNode", "upsert", {
    "where": {"email": "alice@example.com"},
    "conflict_on": ["email"],  # ← Required
    ...
})
```

### ❌ Error: conflict_on field not in where clause
**Cause:** Fields in conflict_on must be in where clause

**Solution:**
```python
# ✅ CORRECT - All conflict_on fields in where
workflow.add_node("OrderItemUpsertNode", "upsert", {
    "where": {
        "order_id": "order-123",
        "product_id": "prod-456"
    },
    "conflict_on": ["order_id", "product_id"],
    ...
})

# ❌ WRONG - Missing fields in where
workflow.add_node("OrderItemUpsertNode", "upsert", {
    "where": {"order_id": "order-123"},  # ← Missing product_id
    "conflict_on": ["order_id", "product_id"],
    ...
})
```

## Related Resources

- **[upsert-node.md](../../../sdk-users/apps/dataflow/guides/upsert-node.md)** - Comprehensive UpsertNode guide
- **[dataflow-crud-operations](dataflow-crud-operations.md)** - CRUD operation patterns
- **[dataflow-bulk-operations](dataflow-bulk-operations.md)** - BulkUpsertNode patterns

## When to Use This Skill

Use UpsertNode with conflict_on when you:
- Upsert based on natural keys (email, username, SKU)
- Handle composite unique constraints
- Implement idempotent API operations
- Sync external data with natural identifiers
- Update inventory/configuration by key
- Manage multi-tenant data with composite keys
