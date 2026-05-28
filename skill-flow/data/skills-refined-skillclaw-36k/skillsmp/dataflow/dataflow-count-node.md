---
name: dataflow-count-node
description: "CountNode for efficient COUNT(*) queries with 10-50x performance improvement over ListNode. Use when counting records, pagination metadata, existence checks, dashboard metrics, or performance-critical counts."
---

# DataFlow CountNode - Efficient Counting

11th auto-generated node for efficient `COUNT(*)` queries with 10-50x performance improvement over ListNode.

> **Skill Metadata**
> Category: `dataflow/nodes`
> Priority: `HIGH`
> Related Skills: [`dataflow-crud-operations`](#), [`dataflow-queries`](#), [`dataflow-performance`](#)
> Related Subagents: `dataflow-specialist` (performance optimization)

## Quick Reference

- **Performance**: 10-50x faster than ListNode workaround
- **Query Type**: Uses `SELECT COUNT(*)` instead of fetching all records
- **Auto-Generated**: 11th node per @db.model
- **MongoDB Support**: Optimized `.count_documents()` for MongoDB
- **Filter Support**: All MongoDB-style operators ($eq, $ne, $gt, $in, etc.)

## ⚠️ CRITICAL: Performance Comparison

### Before CountNode
```python
# ❌ SLOW - Fetches all records to count (20-50ms for 10,000 records)
workflow.add_node("UserListNode", "count_users", {
    "filter": {"active": True},
    "limit": 10000  # Must fetch all to count
})

# In node output:
count = len(results["count_users"])  # Retrieved 10,000 records!
```

### After CountNode
```python
# ✅ FAST - Uses COUNT(*) query (1-5ms regardless of record count)
workflow.add_node("UserCountNode", "count_users", {
    "filter": {"active": True}
})

# In node output:
count = results["count_users"]["count"]  # Only count value (99% faster!)
```

## Basic Usage

### Simple Count
```python
# Count all users
workflow.add_node("UserCountNode", "count_all", {})

# Result: {"count": 1000}
```

### Count with Filter
```python
# Count active users
workflow.add_node("UserCountNode", "count_active", {
    "filter": {"active": True}
})

# Result: {"count": 847}
```

### Complex Filter
```python
# Count premium users created in last 30 days
workflow.add_node("UserCountNode", "count_recent_premium", {
    "filter": {
        "subscription_tier": "premium",
        "created_at": {"$gte": "2024-01-01"}
    }
})

# Result: {"count": 23}
```

## Common Patterns

### 1. Pagination Metadata
```python
# Get total count for pagination
workflow.add_node("UserCountNode", "total_users", {
    "filter": {"active": True}
})

workflow.add_node("UserListNode", "page_users", {
    "filter": {"active": True},
    "offset": 0,
    "limit": 20
})

# Results:
# total_users: {"count": 1000}
# page_users: [...20 records...]
# Pagination: Page 1 of 50 (1000 / 20)
```

### 2. Existence Checks
```python
# Check if any records exist matching criteria
workflow.add_node("OrderCountNode", "pending_orders", {
    "filter": {
        "user_id": "user-123",
        "status": "pending"
    }
})

# Result: {"count": 0} → No pending orders
# Result: {"count": 3} → Has pending orders
```

### 3. Dashboard Metrics
```python
# Dashboard: Active vs Inactive users
workflow.add_node("UserCountNode", "active_count", {
    "filter": {"active": True}
})

workflow.add_node("UserCountNode", "inactive_count", {
    "filter": {"active": False}
})

# Results:
# active_count: {"count": 847}
# inactive_count: {"count": 153}
# Total: 1000 users (84.7% active)
```

### 4. Conditional Logic Based on Count
```python
# Count items in cart before checkout
workflow.add_node("CartItemCountNode", "item_count", {
    "filter": {"cart_id": "cart-123"}
})

workflow.add_node("SwitchNode", "check_empty", {
    "condition": results["item_count"]["count"] > 0,
    "true_output": "proceed_checkout",
    "false_output": "show_empty_cart"
})
```

### 5. Multi-Tenant Counts
```python
# Count records per tenant
workflow.add_node("OrderCountNode", "tenant_orders", {
    "filter": {"tenant_id": current_tenant_id}
})

# Result: {"count": 456}  # This tenant's order count
```

### 6. Time Series Counts
```python
# Count events in last hour
workflow.add_node("EventCountNode", "recent_events", {
    "filter": {
        "timestamp": {
            "$gte": datetime.now() - timedelta(hours=1)
        }
    }
})

# Result: {"count": 1247}  # Events in last hour
```

## MongoDB-Style Filters

CountNode supports all MongoDB-style filter operators:

### Comparison Operators
```python
# Greater than
workflow.add_node("UserCountNode", "adults", {
    "filter": {"age": {"$gte": 18}}
})

# Not equal
workflow.add_node("UserCountNode", "not_admin", {
    "filter": {"role": {"$ne": "admin"}}
})

# In list
workflow.add_node("ProductCountNode", "active_categories", {
    "filter": {"category": {"$in": ["electronics", "books"]}}
})

# Not in list
workflow.add_node("ProductCountNode", "exclude_categories", {
    "filter": {"category": {"$nin": ["archived", "deleted"]}}
})
```

### Complex Filters
```python
# Multiple conditions
workflow.add_node("OrderCountNode", "high_value_recent", {
    "filter": {
        "amount": {"$gte": 1000},
        "status": "completed",
        "created_at": {"$gte": "2024-01-01"}
    }
})
```

## Performance Optimization

### Index Usage
```python
# Ensure indexes on filtered fields for optimal performance
@db.model
class Order:
    id: str
    status: str
    created_at: datetime

    __dataflow__ = {
        'indexes': [
            ['status'],           # Single-field index
            ['status', 'created_at']  # Composite index
        ]
    }

# Query uses index for fast counting
workflow.add_node("OrderCountNode", "count", {
    "filter": {
        "status": "pending",
        "created_at": {"$gte": "2024-01-01"}
    }
})
# Performance: <1ms with index, 5-50ms without
```

### Avoiding Full Table Scans
```python
# ✅ GOOD - Uses index on 'status'
workflow.add_node("OrderCountNode", "pending", {
    "filter": {"status": "pending"}
})

# ❌ SLOW - No index, full table scan
workflow.add_node("OrderCountNode", "search_notes", {
    "filter": {"notes": {"$regex": "important"}}
})
# Solution: Add text search index or use dedicated search node
```

## Database Behavior

### PostgreSQL
```sql
-- Generated SQL
SELECT COUNT(*) FROM users WHERE active = true;
-- Performance: <1ms for indexed fields, <5ms for 10K records
```

### MySQL
```sql
-- Generated SQL
SELECT COUNT(*) FROM users WHERE active = 1;
-- Performance: <1ms for indexed fields
```

### SQLite
```sql
-- Generated SQL
SELECT COUNT(*) FROM users WHERE active = 1;
-- Performance: <2ms for indexed fields, <10ms for 100K records
```

### MongoDB
```python
# Generated MongoDB query
collection.count_documents({"active": True})
# Performance: <1ms with index
```

## Best Practices

### 1. Use CountNode Instead of ListNode for Counts
```python
# ✅ CORRECT - Use CountNode (99% faster)
workflow.add_node("UserCountNode", "count", {
    "filter": {"active": True}
})
count = results["count"]["count"]

# ❌ WRONG - Use ListNode (10-50x slower)
workflow.add_node("UserListNode", "list", {
    "filter": {"active": True},
    "limit": 10000
})
count = len(results["list"])
```

### 2. Add Indexes for Frequently Counted Fields
```python
# ✅ CORRECT - Index frequently filtered fields
@db.model
class Order:
    id: str
    status: str
    user_id: str

    __dataflow__ = {
        'indexes': [
            ['status'],      # For status counts
            ['user_id']      # For per-user counts
        ]
    }
```

### 3. Use CountNode for Existence Checks
```python
# ✅ CORRECT - Fast existence check
workflow.add_node("OrderCountNode", "has_pending", {
    "filter": {
        "user_id": user_id,
        "status": "pending"
    }
})
has_pending = results["has_pending"]["count"] > 0

# ❌ WRONG - Fetches unnecessary data
workflow.add_node("OrderListNode", "pending_list", {
    "filter": {
        "user_id": user_id,
        "status": "pending"
    },
    "limit": 1
})
has_pending = len(results["pending_list"]) > 0
```

### 4. Combine with Pagination
```python
# ✅ CORRECT - Efficient pagination
workflow.add_node("UserCountNode", "total", {
    "filter": {"active": True}
})

workflow.add_node("UserListNode", "page", {
    "filter": {"active": True},
    "offset": page * limit,
    "limit": limit
})

# Calculate pagination:
# total_pages = ceil(results["total"]["count"] / limit)
```

## Troubleshooting

### ❌ Slow CountNode Queries
**Cause:** Missing index on filtered fields

**Solution:**
```python
# Add index to model
@db.model
class Order:
    status: str

    __dataflow__ = {
        'indexes': [['status']]  # ← Add index
    }
```

### ❌ Count Returns 0 Unexpectedly
**Cause:** Filter condition too restrictive or incorrect

**Solution:**
```python
# Debug with ListNode first
workflow.add_node("OrderListNode", "debug_list", {
    "filter": {"status": "pending"},
    "limit": 5
})
# Check if ListNode returns records

# Then use CountNode
workflow.add_node("OrderCountNode", "count", {
    "filter": {"status": "pending"}
})
```

## Related Resources

- **[count-node.md](../../../sdk-users/apps/dataflow/guides/count-node.md)** - Comprehensive CountNode guide
- **[dataflow-queries](dataflow-queries.md)** - Query patterns and filtering
- **[dataflow-performance](dataflow-performance.md)** - Performance optimization
- **[dataflow-crud-operations](dataflow-crud-operations.md)** - CRUD operation patterns

## When to Use This Skill

Use CountNode when you:
- Count records without fetching data (10-50x faster)
- Calculate pagination metadata (total pages, records)
- Perform existence checks (any matching records?)
- Generate dashboard metrics (user counts, order stats)
- Implement conditional logic based on counts
- Optimize performance-critical counting operations
