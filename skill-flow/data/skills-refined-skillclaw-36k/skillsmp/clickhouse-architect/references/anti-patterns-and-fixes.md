**Skill**: [ClickHouse Architect](../SKILL.md)

# Anti-Patterns and Fixes

<!-- ADR: 2025-12-09-clickhouse-architect-skill -->

The "13 Deadly Sins" of ClickHouse with v24.4+ status and modern fixes.

## Overview

Some traditional anti-patterns have been significantly improved in v24.4+:

| Pattern             | Traditional Status | v24.4+ Status      |
| ------------------- | ------------------ | ------------------ |
| Large JOINs         | Avoid              | **180x improved**  |
| Mutations           | Avoid              | **1700x improved** |
| Other anti-patterns | Avoid              | Still avoid        |

## Still Critical Anti-Patterns

### 1. Too Many Parts

**Problem**: More than 300 active parts per partition causes degraded performance.

**Detection**:

```sql
SELECT database, table, partition, count() AS parts
FROM system.parts
WHERE active = 1
GROUP BY database, table, partition
HAVING parts > 300;
```

**Fix**:

- Reduce PARTITION BY granularity (monthly instead of daily)
- Increase batch sizes for inserts
- Run `OPTIMIZE TABLE ... FINAL` during maintenance windows

### 2. Small Batch Inserts

**Problem**: Inserting fewer than 1,000 rows per batch creates too many parts.

**Symptoms**:

- Growing part count
- Slow inserts
- High CPU from merges

**Fix**:

```python
# Buffer rows before inserting
BATCH_SIZE = 50000
buffer = []

for row in source:
    buffer.append(row)
    if len(buffer) >= BATCH_SIZE:
        client.insert('table', buffer)
        buffer = []
```

**Target**: 10,000-100,000 rows per batch.

### 3. High-Cardinality First ORDER BY

**Problem**: Placing high-cardinality columns first in ORDER BY makes queries 10x slower.

**Bad Example**:

```sql
-- Wrong: trade_id is unique (highest cardinality)
ORDER BY (trade_id, timestamp, symbol, exchange)
```

**Fix**:

```sql
-- Correct: lowest cardinality first
ORDER BY (exchange, symbol, timestamp, trade_id)
```

### 4. No Memory Limits

**Problem**: 78% of deployments don't configure memory limits, risking OOM kills.

**Fix**:

```sql
-- Set per-query limit
SET max_memory_usage = 10000000000;  -- 10GB

-- In users.xml or config
<max_memory_usage>10000000000</max_memory_usage>
<max_memory_usage_for_all_queries>50000000000</max_memory_usage_for_all_queries>
```

### 5. Denormalization Overuse

**Problem**: Pre-joining data into wide tables increases storage 10-100x and slows queries.

**Bad Pattern**:

```sql
-- Wide denormalized table
CREATE TABLE orders_denormalized (
    order_id UInt64,
    -- Order fields
    customer_name String,
    customer_email String,
    customer_address String,
    -- Product fields (repeated per order item!)
    product_name String,
    product_category String,
    ...
);
```

**Fix**: Use dictionaries for dimension lookups:

```sql
-- Fact table (normalized)
CREATE TABLE orders (
    order_id UInt64,
    customer_id UInt64,
    product_id UInt64,
    quantity UInt32,
    price Float64
);

-- Dictionary for customer lookup
CREATE DICTIONARY customers_dict (...)
SOURCE(CLICKHOUSE(TABLE 'customers'))
LAYOUT(FLAT());

-- Query with dictionary (6.6x faster than JOIN)
SELECT
    order_id,
    dictGet('customers_dict', 'name', customer_id) AS customer_name
FROM orders;
```

### 6. Over-Partitioning

**Problem**: Too many partitions (>1000 total) degrades performance.

**Bad Example**:

```sql
-- Creates 365+ partitions per year
PARTITION BY toYYYYMMDD(timestamp)
```

**Fix**:

```sql
-- 12 partitions per year
PARTITION BY toYYYYMM(timestamp)
```

### 7. Missing Codecs

**Problem**: Not using specialized codecs wastes 5-10x storage.

**Fix**: Apply appropriate codecs:

```sql
timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD)
price Float64 CODEC(Gorilla, ZSTD)
count UInt64 CODEC(T64, ZSTD)
```

## Improved in v24.4+ (Use with Caution)

### 8. Large JOINs (180x Improved)

**v24.4+ Improvement**: Predicate pushdown makes JOINs 180x faster in many cases.

**Still Avoid For**: Ultra-low-latency (<10ms) requirements.

**Better Alternative**: Dictionaries for dimension lookups.

```sql
-- Now acceptable for most use cases
SELECT o.*, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.timestamp > now() - INTERVAL 1 DAY;

-- Still better: Dictionary lookup
SELECT o.*, dictGet('customers', 'name', customer_id)
FROM orders o
WHERE timestamp > now() - INTERVAL 1 DAY;
```

### 9. Mutations (1700x Improved)

**v24.4+ Improvement**: Lightweight updates are 1700x faster.

**Traditional Mutations**: Still slow, avoid for frequent operations.

**Lightweight Updates**:

```sql
-- Fast in v24.4+ (lightweight)
ALTER TABLE trades UPDATE status = 'processed' WHERE trade_id = 123;

-- Still slow (traditional mutation)
ALTER TABLE trades DELETE WHERE timestamp < now() - INTERVAL 90 DAY;
```

**Better Pattern**: Use TTL for deletions:

```sql
TTL timestamp + INTERVAL 90 DAY DELETE
```

## Detection Query

Run to identify anti-patterns:

```sql
-- Check for all anti-patterns
SELECT
    database,
    table,
    -- Part count check
    (SELECT count() FROM system.parts WHERE active AND database = t.database AND table = t.name) AS part_count,
    -- Partition count
    (SELECT count(DISTINCT partition) FROM system.parts WHERE active AND database = t.database AND table = t.name) AS partition_count,
    -- Size analysis
    formatReadableSize(total_bytes) AS total_size
FROM system.tables t
WHERE database NOT IN ('system', 'INFORMATION_SCHEMA')
ORDER BY total_bytes DESC;
```

## Related References

- [Schema Design Workflow](./schema-design-workflow.md)
- [Audit and Diagnostics](./audit-and-diagnostics.md)
- [Idiomatic Architecture](./idiomatic-architecture.md)
