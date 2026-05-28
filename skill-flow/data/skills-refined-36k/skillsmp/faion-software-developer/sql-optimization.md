---
id: sql-optimization
name: "SQL Optimization"
domain: DEV
skill: faion-software-developer
category: "development"
---

# SQL Optimization

## Overview

SQL optimization involves analyzing and improving database queries to reduce execution time, minimize resource consumption, and improve application responsiveness. It covers query analysis, index optimization, query rewriting, and understanding execution plans.

## When to Use

- Slow query complaints from users or monitoring alerts
- Database CPU/IO consistently high
- Application response times degrading under load
- Before deploying new features with complex queries
- Regular performance audits and maintenance

## Key Principles

- **Measure before optimizing**: Use EXPLAIN ANALYZE to understand actual performance
- **Optimize the right queries**: Focus on frequent queries, not just slow ones
- **Indexes are not free**: They speed reads but slow writes
- **Reduce data movement**: Filter early, join smart, fetch only needed columns
- **Consider the full picture**: Query optimization, connection pooling, caching

## Best Practices

### Query Analysis with EXPLAIN

```sql
-- Always use EXPLAIN ANALYZE for real execution stats
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.id, o.total_amount, u.email
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE o.status = 'pending'
  AND o.created_at > NOW() - INTERVAL '7 days'
ORDER BY o.created_at DESC
LIMIT 100;

-- Reading the output:
-- Seq Scan = full table scan (usually bad for large tables)
-- Index Scan = using index (good)
-- Bitmap Index Scan = combining multiple indexes
-- Nested Loop = for each row in outer, scan inner (watch for large outer sets)
-- Hash Join = build hash table, probe (good for larger datasets)
-- Sort = in-memory or disk sort (watch for high cost)
```

### Index Optimization

```sql
-- Before: Slow query with sequential scan
SELECT * FROM orders
WHERE user_id = '123' AND status = 'pending';

-- After: Add composite index matching query pattern
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- For range queries, put equality columns first
-- Query: WHERE user_id = ? AND created_at > ?
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);

-- Covering index to avoid table lookup
CREATE INDEX idx_orders_covering ON orders(user_id, status)
    INCLUDE (total_amount, created_at);

-- Partial index for common filter
CREATE INDEX idx_orders_pending ON orders(created_at)
    WHERE status = 'pending';
```

### Query Rewriting

```sql
-- Bad: Subquery in SELECT (N+1 problem)
SELECT
    o.id,
    (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
FROM orders o;

-- Good: Use JOIN with aggregation
SELECT o.id, COUNT(oi.id) as item_count
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id;

-- Bad: OR conditions preventing index use
SELECT * FROM products
WHERE category_id = 1 OR category_id = 2 OR category_id = 3;

-- Good: Use IN clause
SELECT * FROM products
WHERE category_id IN (1, 2, 3);

-- Bad: Function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- Good: Use expression index or fix at application level
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
-- Or store email lowercase and compare directly
```

### Pagination Optimization

```sql
-- Bad: OFFSET for deep pagination (scans all skipped rows)
SELECT * FROM products ORDER BY created_at DESC LIMIT 20 OFFSET 10000;

-- Good: Keyset/cursor pagination
SELECT * FROM products
WHERE created_at < '2024-01-15 10:30:00'
ORDER BY created_at DESC
LIMIT 20;

-- For complex sorting, use composite cursor
SELECT * FROM products
WHERE (created_at, id) < ('2024-01-15 10:30:00', 'uuid-here')
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

### Batch Operations

```sql
-- Bad: Individual inserts in a loop
INSERT INTO logs (message) VALUES ('log1');
INSERT INTO logs (message) VALUES ('log2');
-- ... repeated 1000 times

-- Good: Batch insert
INSERT INTO logs (message) VALUES
    ('log1'), ('log2'), ('log3'), ... ('log1000');

-- Good: COPY for bulk loading
COPY logs(message) FROM '/path/to/data.csv' WITH CSV;

-- Batch updates with CTE
WITH to_update AS (
    SELECT id FROM orders
    WHERE status = 'pending'
      AND created_at < NOW() - INTERVAL '30 days'
    LIMIT 1000
)
UPDATE orders SET status = 'expired'
WHERE id IN (SELECT id FROM to_update);
```

### Connection and Query Tuning

```python
# Use connection pooling (SQLAlchemy example)
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=20,           # Maintain 20 connections
    max_overflow=10,        # Allow 10 additional when busy
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=3600,      # Recycle connections after 1 hour
)

# Use server-side cursors for large result sets
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execution_options(stream_results=True).execute(
        text("SELECT * FROM large_table")
    )
    for batch in result.partitions(1000):
        process_batch(batch)
```

### Materialized Views for Complex Aggregations

```sql
-- Create materialized view for dashboard stats
CREATE MATERIALIZED VIEW daily_sales_stats AS
SELECT
    DATE(created_at) as sale_date,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE status = 'delivered'
GROUP BY DATE(created_at);

-- Create index on materialized view
CREATE INDEX idx_sales_stats_date ON daily_sales_stats(sale_date);

-- Refresh periodically (can be done concurrently)
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_stats;
```

## Anti-patterns

- **SELECT ***: Always specify needed columns
- **N+1 queries**: Use JOINs or batch loading instead
- **Missing WHERE clause**: On UPDATE/DELETE operations
- **Implicit type conversion**: Causes index bypass
- **LIKE '%pattern%'**: Full text search needed instead
- **DISTINCT as a fix**: Usually indicates a JOIN problem
- **ORDER BY RAND()**: Extremely slow for large tables
- **Not using prepared statements**: Security and performance issue

## References

- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [Use The Index, Luke](https://use-the-index-luke.com/)
- [pgMustard - EXPLAIN Analyzer](https://www.pgmustard.com/)
- [Percona Blog - Query Optimization](https://www.percona.com/blog/)
