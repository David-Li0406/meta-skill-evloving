---
name: dataflow-performance
description: "DataFlow performance optimization. Use when DataFlow performance, optimize, connection pool, query optimization, or slow queries."
---

# DataFlow Performance Optimization

Performance tuning for DataFlow applications with connection pooling, caching, and query optimization.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> Related Skills: [`dataflow-bulk-operations`](#), [`dataflow-queries`](#), [`dataflow-connection-config`](#)
> Related Subagents: `dataflow-specialist` (advanced optimization)

## Quick Reference

- **Connection Pooling**: 20-50 connections typical
- **Bulk Operations**: 10-100x faster for >100 records
- **Indexes**: Add to frequently queried fields
- **Caching**: Enable for read-heavy workloads
- **Benchmarks**: 31.8M ops/sec baseline, 99.9% cache hit rate

## Core Pattern

```python
from dataflow import DataFlow

# Production-optimized configuration
db = DataFlow(
    database_url="postgresql://...",

    # Connection pooling
    pool_size=20,              # Base connections
    pool_max_overflow=30,      # Extra connections
    pool_recycle=3600,         # Recycle after 1 hour
    pool_pre_ping=True,        # Validate connections

    # Performance
    monitoring=True,
    slow_query_threshold=100,  # Log queries >100ms

    # Caching (if Redis available)
    cache_enabled=True,
    cache_ttl=300  # 5 minutes
)

# Add indexes to models
@db.model
class Product:
    name: str
    category: str
    price: float
    active: bool

    __indexes__ = [
        {"fields": ["category", "active"]},
        {"fields": ["price"]},
        {"fields": ["created_at"]}
    ]
```

## Performance Optimization Strategies

### 1. Connection Pooling

```python
db = DataFlow(
    pool_size=20,           # 2x CPU cores typical
    pool_max_overflow=30,
    pool_recycle=3600
)
```

### 2. Use Bulk Operations

```python
# Slow - 1 op at a time
for product in products:
    workflow.add_node("ProductCreateNode", f"create_{product['id']}", product)

# Fast - 10-100x faster
workflow.add_node("ProductBulkCreateNode", "import", {
    "data": products,
    "batch_size": 1000
})
```

### 3. Add Indexes

```python
@db.model
class User:
    email: str
    active: bool

    __indexes__ = [
        {"fields": ["email"], "unique": True},
        {"fields": ["active"]}
    ]
```

### 4. Enable Caching

```python
workflow.add_node("ProductListNode", "cached_query", {
    "filter": {"active": True},
    "cache_key": "active_products",
    "cache_ttl": 300
})
```

### 5. Query Optimization

```python
# Good - selective filter first
workflow.add_node("ProductListNode", "query", {
    "filter": {
        "active": True,  # Most selective first
        "category": "electronics",
        "price": {"$lt": 1000}
    }
})

# Good - field selection
workflow.add_node("UserListNode", "names_only", {
    "fields": ["id", "name"],  # Only needed fields
    "filter": {"active": True}
})
```

### 6. Schema Cache

Thread-safe table existence cache eliminating redundant migration checks, providing 91-99% performance improvement for multi-operation workflows.

```python
from dataflow import DataFlow

# Default (cache enabled, no TTL)
db = DataFlow("postgresql://...")

# Custom configuration
db = DataFlow(
    "postgresql://...",
    schema_cache_enabled=True,      # Enable/disable cache
    schema_cache_ttl=300,            # TTL in seconds (None = no expiration)
    schema_cache_max_size=10000,    # Max cached tables
    schema_cache_validation=False,  # Schema checksum validation
)

# Performance Impact
# First operation: ~1500ms (cache miss with migration check)
# Subsequent operations: ~1ms (cache hit) - 99% faster!

# Cache Management
metrics = db._schema_cache.get_metrics()
print(f"Hit rate: {metrics['hit_rate']:.2%}")  # Should be >90%

# Clear cache
db._schema_cache.clear()

# Clear specific table
db._schema_cache.clear_table("User", database_url)
```

**When to Clear Cache:**
- After manual schema modifications
- After external migrations
- For debugging schema issues
- Cache auto-clears on DataFlow schema operations

**Performance Characteristics:**
- **First operation**: ~1500ms (cache miss)
- **Subsequent operations**: ~1ms (cache hit) - **99% faster**
- **Multi-operation workflows**: 91-99% overall improvement
- **Memory overhead**: <1KB per cached table
- **Thread safety**: RLock-protected concurrent access

## Performance Benchmarks

- **Single ops**: <1ms
- **Bulk create**: 10k+/sec
- **Bulk update**: 50k+/sec
- **Bulk delete**: 100k+/sec
- **Cache hit rate**: 99.9%

## Common Mistakes

### Mistake 1: Small Connection Pool

```python
# Wrong - pool exhaustion
db = DataFlow(pool_size=5)
```

**Fix: Adequate Pool**

```python
db = DataFlow(pool_size=20, pool_max_overflow=30)
```

### Mistake 2: Single Operations for Bulk

```python
# Wrong - very slow
for item in items:
    workflow.add_node("ItemCreateNode", f"create_{item['id']}", item)
```

**Fix: Use Bulk Operations**

```python
workflow.add_node("ItemBulkCreateNode", "import", {
    "data": items,
    "batch_size": 1000
})
```

## Documentation References

### Primary Sources
- **Performance Guide**: [`sdk-users/apps/dataflow/docs/production/performance.md`](../../../../sdk-users/apps/dataflow/docs/production/performance.md)
- **Database Optimization**: [`sdk-users/apps/dataflow/docs/advanced/database-optimization.md`](../../../../sdk-users/apps/dataflow/docs/advanced/database-optimization.md)
- **Pooling Guide**: [`sdk-users/apps/dataflow/docs/advanced/pooling.md`](../../../../sdk-users/apps/dataflow/docs/advanced/pooling.md)

### Related Documentation
- **README Performance**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L959-L984)

## Quick Tips

- pool_size = 2x CPU cores (typical)
- Use bulk operations for >100 records
- Add indexes to queried fields
- Enable caching for read-heavy
- Monitor slow queries (>100ms)

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow performance, optimize, connection pool, query optimization, slow queries, performance tuning, database optimization -->
