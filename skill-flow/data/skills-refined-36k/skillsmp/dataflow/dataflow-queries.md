---
name: dataflow-queries
description: "MongoDB-style query syntax for DataFlow filters. Use when DataFlow query, MongoDB syntax, $gt $lt $in operators, query filters, filter conditions, or advanced queries."
---

# DataFlow Query Patterns

Use MongoDB-style query operators for filtering, searching, and aggregating DataFlow data.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> Related Skills: [`dataflow-crud-operations`](#), [`dataflow-models`](#), [`dataflow-bulk-operations`](#)
> Related Subagents: `dataflow-specialist` (complex queries, optimization)

## ⚠️ Important: Filter Operators

All MongoDB-style filter operators are fully supported. Ensure you're using the latest DataFlow version for complete operator support.

**To ensure all operators work correctly:**
```bash
pip install --upgrade kailash-dataflow
```

**Supported Operators:**
- ✅ $ne (not equal)
- ✅ $nin (not in)
- ✅ $in (in)
- ✅ $not (logical NOT)
- ✅ All comparison operators ($gt, $lt, $gte, $lte)

## Quick Reference

- **Operators**: `$gt`, `$gte`, `$lt`, `$lte`, `$ne`, `$in`, `$nin`, `$regex`, `$or`, `$and`, `$not`
- **Performance**: <10ms for most queries, <100ms for aggregations
- **SQL Database Agnostic**: Works across PostgreSQL, MySQL, SQLite (MongoDB has native query language)
- **Pattern**: Use in `filter` parameter of ListNode

```python
# Basic comparison
{"age": {"$gt": 18}}

# Multiple conditions (implicit AND)
{"active": True, "age": {"$gte": 18}}

# OR conditions
{"$or": [{"role": "admin"}, {"role": "manager"}]}

# IN operator
{"category": {"$in": ["electronics", "computers"]}}

# Text search
{"name": {"$regex": "laptop"}}
```

## Core Pattern

```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

db = DataFlow()

@db.model
class Product:
    name: str
    category: str
    price: float
    stock: int
    active: bool = True

workflow = WorkflowBuilder()

# Simple filter
workflow.add_node("ProductListNode", "active_products", {
    "filter": {"active": True}
})

# Comparison operators
workflow.add_node("ProductListNode", "affordable_products", {
    "filter": {
        "price": {"$lt": 100.00},
        "stock": {"$gt": 0}
    }
})

# Range query
workflow.add_node("ProductListNode", "mid_range_products", {
    "filter": {
        "price": {"$gte": 50.00, "$lte": 150.00}
    }
})

# IN operator
workflow.add_node("ProductListNode", "electronics", {
    "filter": {
        "category": {"$in": ["phones", "laptops", "tablets"]}
    }
})

# OR conditions
workflow.add_node("ProductListNode", "featured_or_popular", {
    "filter": {
        "$or": [
            {"featured": True},
            {"views": {"$gt": 1000}}
        ]
    }
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Common Use Cases

- **Search**: Text search with regex
- **Filtering**: Age restrictions, status filters
- **Price Ranges**: E-commerce price filtering
- **Multi-Select**: Category or tag filtering
- **Exclusions**: NOT IN patterns

## Query Operators Reference

### Comparison Operators

| Operator | SQL Equivalent | Example |
|----------|---------------|---------|
| `$gt` | `>` | `{"age": {"$gt": 18}}` |
| `$gte` | `>=` | `{"age": {"$gte": 18}}` |
| `$lt` | `<` | `{"price": {"$lt": 100}}` |
| `$lte` | `<=` | `{"price": {"$lte": 100}}` |
| `$ne` | `!=` | `{"status": {"$ne": "inactive"}}` |
| `$eq` | `=` | `{"active": {"$eq": true}}` (or just `{"active": true}`) |
| `$null` | `IS NULL` | `{"deleted_at": {"$null": True}}` |
| `$exists` | `IS NOT NULL` | `{"email": {"$exists": True}}` |

### Null Checking Operators (v0.10.6+)

**For soft-delete filtering and nullable field queries:**

```python
# Query for NULL values (e.g., non-deleted records)
workflow.add_node("PatientListNode", "active_patients", {
    "filter": {"deleted_at": {"$null": True}}  # WHERE deleted_at IS NULL
})

# Query for NOT NULL values
workflow.add_node("PatientListNode", "deleted_patients", {
    "filter": {"deleted_at": {"$exists": True}}  # WHERE deleted_at IS NOT NULL
})

# Alternative: $eq with None also works (v0.10.6+)
workflow.add_node("PatientListNode", "active", {
    "filter": {"deleted_at": {"$eq": None}}  # Also generates IS NULL
})
```

**Common Pattern - Soft Delete Filtering:**
```python
# soft_delete: True only affects DELETE operations, NOT queries!
# You MUST manually filter in queries:
workflow.add_node("ModelListNode", "active_records", {
    "filter": {"deleted_at": {"$null": True}}  # Exclude soft-deleted records
})
```

### Logical Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `$and` | All conditions | `{"$and": [{"active": true}, {"verified": true}]}` |
| `$or` | Any condition | `{"$or": [{"role": "admin"}, {"super_user": true}]}` |
| `$not` | Negation | `{"$not": {"status": "suspended"}}` |

### Array Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `$in` | Value in list | `{"category": {"$in": ["a", "b", "c"]}}` |
| `$nin` | Value not in list | `{"role": {"$nin": ["guest", "banned"]}}` |
| `$contains` | Array contains value | `{"tags": {"$contains": "featured"}}` |
| `$overlap` | Arrays overlap | `{"tags": {"$overlap": ["sale", "new"]}}` |

### Text Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `$regex` | Pattern match | `{"name": {"$regex": "laptop"}}` |
| `$regex` + `$options` | Case-insensitive | `{"email": {"$regex": "john", "$options": "i"}}` |
| `$text` | Full-text search | `{"$text": {"$search": "gaming laptop"}}` |

## Key Parameters / Options

### Sorting

```python
workflow.add_node("ProductListNode", "sorted_products", {
    "filter": {"active": True},
    "order_by": ["-price", "name"]  # - prefix for descending
})
```

### Pagination

```python
# Offset-based
workflow.add_node("ProductListNode", "page_2", {
    "filter": {"active": True},
    "order_by": ["created_at"],
    "limit": 20,
    "offset": 20  # Skip first 20 (page 2)
})

# Cursor-based (more efficient)
workflow.add_node("ProductListNode", "next_page", {
    "filter": {
        "active": True,
        "id": {"$gt": last_id}  # After last seen ID
    },
    "order_by": ["id"],
    "limit": 20
})
```

### Field Selection

```python
# Select specific fields only
workflow.add_node("UserListNode", "names_only", {
    "filter": {"active": True},
    "fields": ["id", "name", "email"]  # Only these fields
})

# Exclude fields
workflow.add_node("ProductListNode", "no_description", {
    "filter": {"active": True},
    "exclude_fields": ["description", "long_text"]
})
```

### Aggregation

```python
# Group by and aggregate
workflow.add_node("OrderListNode", "revenue_by_status", {
    "group_by": "status",
    "aggregations": {
        "total_revenue": {"$sum": "total"},
        "order_count": {"$count": "*"},
        "avg_order": {"$avg": "total"}
    }
})
```

## Common Mistakes

### Mistake 1: Using SQL Operators

```python
# Wrong - SQL operators don't work
workflow.add_node("ProductListNode", "query", {
    "filter": {"price > 100"}  # FAILS
})
```

**Fix: Use MongoDB-Style Operators**

```python
# Correct
workflow.add_node("ProductListNode", "query", {
    "filter": {"price": {"$gt": 100.00}}
})
```

### Mistake 2: Implicit AND with OR

```python
# Wrong - will fail
workflow.add_node("UserListNode", "query", {
    "filter": {
        "active": True,
        "$or": [{"role": "admin"}, {"role": "manager"}]
        # Mixing levels incorrectly
    }
})
```

**Fix: Use $and for Mixed Conditions**

```python
# Correct
workflow.add_node("UserListNode", "query", {
    "filter": {
        "$and": [
            {"active": True},
            {"$or": [{"role": "admin"}, {"role": "manager"}]}
        ]
    }
})
```

### Mistake 3: Forgetting $ Prefix

```python
# Wrong - missing $ prefix
workflow.add_node("ProductListNode", "query", {
    "filter": {"price": {"gt": 100}}  # FAILS
})
```

**Fix: Always Use $ Prefix**

```python
# Correct
workflow.add_node("ProductListNode", "query", {
    "filter": {"price": {"$gt": 100}}
})
```

## Related Patterns

- **For CRUD operations**: See [`dataflow-crud-operations`](#)
- **For bulk operations**: See [`dataflow-bulk-operations`](#)
- **For performance**: See [`dataflow-performance`](#)
- **For result access**: See [`dataflow-result-access`](#)

## When to Escalate to Subagent

Use `dataflow-specialist` subagent when:
- Designing complex aggregation queries
- Optimizing slow query performance
- Working with full-text search
- Implementing faceted search
- Creating dashboard analytics
- Troubleshooting query errors

## Documentation References

### Primary Sources
- **Query Patterns**: [`sdk-users/apps/dataflow/docs/development/query-patterns.md`](../../../../sdk-users/apps/dataflow/docs/development/query-patterns.md)
- **README Examples**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L335-L348)
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md)

### Related Documentation
- **Query Builder**: [`sdk-users/apps/dataflow/docs/features/query-builder.md`](../../../../sdk-users/apps/dataflow/docs/features/query-builder.md)
- **Database Optimization**: [`sdk-users/apps/dataflow/docs/advanced/database-optimization.md`](../../../../sdk-users/apps/dataflow/docs/advanced/database-optimization.md)
- **Performance Guide**: [`sdk-users/apps/dataflow/docs/production/performance.md`](../../../../sdk-users/apps/dataflow/docs/production/performance.md)

## Examples

### Example 1: E-commerce Search

```python
workflow = WorkflowBuilder()

# Complex product search
workflow.add_node("ProductListNode", "search_results", {
    "filter": {
        "$and": [
            {"active": True},
            {"name": {"$regex": "laptop", "$options": "i"}},
            {"price": {"$gte": 500.00, "$lte": 2000.00}},
            {"category": {"$in": ["computers", "electronics"]}},
            {"stock": {"$gt": 0}}
        ]
    },
    "order_by": ["-views", "-rating"],
    "limit": 20
})
```

### Example 2: Dashboard Analytics

```python
# Revenue by category
workflow.add_node("OrderListNode", "category_revenue", {
    "filter": {
        "status": {"$in": ["completed", "shipped"]},
        "created_at": {"$gte": "2024-01-01"}
    },
    "group_by": "category",
    "aggregations": {
        "revenue": {"$sum": "total"},
        "orders": {"$count": "*"},
        "avg_order": {"$avg": "total"}
    },
    "order_by": ["-revenue"]
})
```

### Example 3: User Search with Multiple Filters

```python
# Advanced user search
workflow.add_node("UserListNode", "power_users", {
    "filter": {
        "$and": [
            {"active": True},
            {"verified": True},
            {
                "$or": [
                    {"subscription": "premium"},
                    {"purchases": {"$gte": 10}}
                ]
            },
            {"last_login": {"$gte": "30 days ago"}},
            {"role": {"$nin": ["guest", "banned"]}}
        ]
    },
    "order_by": ["-total_spent", "-created_at"],
    "limit": 100
})
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Invalid operator: gt` | Missing $ prefix | Use `$gt` not `gt` |
| `TypeError: unsupported operand` | SQL syntax in filter | Use MongoDB-style operators |
| `No results returned` | Filter too restrictive | Check individual conditions |
| `Query timeout` | Inefficient query | Add indexes, simplify filter |

## Quick Tips

- Always use $ prefix for operators
- Multiple conditions at same level = implicit AND
- Use $and explicitly when mixing with $or
- Regex is case-sensitive unless `$options: "i"`
- Add indexes for frequently queried fields
- Use cursor pagination for better performance
- Limit + offset for simple pagination

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow query, MongoDB syntax, $gt, $lt, $in, $or, $and, query filters, filter conditions, query operators, advanced queries, database filters, search filters, query patterns, filter syntax -->
