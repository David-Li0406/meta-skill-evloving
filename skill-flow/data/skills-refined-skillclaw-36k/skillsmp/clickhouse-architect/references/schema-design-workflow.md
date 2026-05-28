**Skill**: [ClickHouse Architect](../SKILL.md)

# Schema Design Workflow

<!-- ADR: 2025-12-09-clickhouse-architect-skill -->

Complete workflow for designing ClickHouse schemas from requirements to production.

## Workflow Overview

```
Requirements → ORDER BY → Codecs → PARTITION BY → Accelerators → Validate
```

## Step 1: Gather Requirements

Before designing the schema, understand:

| Question                     | Impact on Design           |
| ---------------------------- | -------------------------- |
| What queries will run most?  | ORDER BY column selection  |
| What's the data volume?      | PARTITION BY granularity   |
| What's the retention period? | TTL configuration          |
| Cloud or self-hosted?        | Engine selection           |
| Query latency requirements?  | Index and projection needs |

## Step 2: Define ORDER BY Key

The ORDER BY clause determines query performance more than any other factor.

### Decision Process

1. List all columns used in WHERE clauses
2. Order by cardinality (lowest first)
3. Limit to 3-5 columns
4. Ensure range query columns are included

### Example Walkthrough

**Scenario**: Trading data with queries filtering by exchange, symbol, and time ranges.

```sql
-- Query patterns:
-- 1. WHERE exchange = 'binance' AND symbol = 'BTCUSDT' AND timestamp > ...
-- 2. WHERE symbol = 'ETHUSDT' ORDER BY timestamp
-- 3. WHERE timestamp BETWEEN ... AND ... (rare)

-- Cardinality analysis:
-- exchange: ~10 values (LOW)
-- symbol: ~1000 values (MEDIUM)
-- timestamp: millions (HIGH)
-- trade_id: unique (HIGHEST)

-- Optimal ORDER BY:
ORDER BY (exchange, symbol, timestamp, trade_id)
```

## Step 3: Select Data Types and Codecs

Match column types to their optimal codecs:

```sql
CREATE TABLE trades (
    -- Identifiers
    trade_id UInt64,

    -- Low-cardinality strings
    exchange LowCardinality(String),
    symbol LowCardinality(String),
    side LowCardinality(String),

    -- Timestamps with specialized codec
    timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD),

    -- Float values with Gorilla compression
    price Float64 CODEC(Gorilla, ZSTD),
    quantity Float64 CODEC(Gorilla, ZSTD),

    -- Integer counters
    sequence_num UInt64 CODEC(T64, ZSTD)
) ENGINE = MergeTree()
ORDER BY (exchange, symbol, timestamp, trade_id);
```

## Step 4: Configure PARTITION BY

Use PARTITION BY for **data lifecycle management**, not query optimization.

### Guidelines

| Data Volume      | Recommended Partition | Example                 |
| ---------------- | --------------------- | ----------------------- |
| < 1B rows/month  | Monthly               | `toYYYYMM(timestamp)`   |
| 1-10B rows/month | Weekly                | `toMonday(timestamp)`   |
| > 10B rows/month | Daily (with caution)  | `toYYYYMMDD(timestamp)` |

### TTL Integration

```sql
CREATE TABLE trades (
    ...
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (exchange, symbol, timestamp, trade_id)
TTL timestamp + INTERVAL 90 DAY DELETE;
```

## Step 5: Add Performance Accelerators

### When to Use Each

| Accelerator       | Use Case                                 |
| ----------------- | ---------------------------------------- |
| Projection        | Alternative sort order needed frequently |
| Materialized View | Pre-computed aggregations for dashboards |
| Dictionary        | Dimension lookups replacing JOINs        |
| Skip Index        | High-cardinality column filtering        |

### Projection Example

```sql
-- Add projection for queries sorted by symbol first
ALTER TABLE trades ADD PROJECTION trades_by_symbol (
    SELECT * ORDER BY symbol, exchange, timestamp
);
ALTER TABLE trades MATERIALIZE PROJECTION trades_by_symbol;
```

### Skip Index Example

```sql
-- Bloom filter for rare text searches
ALTER TABLE trades ADD INDEX idx_trade_id trade_id TYPE bloom_filter GRANULARITY 4;
```

## Step 6: Validate Schema

Run the audit script to verify:

```bash
clickhouse-client --multiquery < scripts/schema-audit.sql
```

### Validation Checklist

- [ ] Part count < 300 per partition
- [ ] Compression ratio > 3x for numeric columns
- [ ] Query execution time meets SLA
- [ ] Memory usage within limits
- [ ] Replication lag (if applicable) < 10 seconds

## Complete Example

```sql
-- Production-ready trading table
CREATE TABLE trades (
    -- Identifiers
    trade_id UInt64,

    -- Categorical (low cardinality)
    exchange LowCardinality(String),
    symbol LowCardinality(String),
    side Enum8('buy' = 1, 'sell' = 2),

    -- Time series
    timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD),

    -- Numeric measurements
    price Float64 CODEC(Gorilla, ZSTD),
    quantity Float64 CODEC(Gorilla, ZSTD),
    quote_quantity Float64 CODEC(Gorilla, ZSTD),

    -- Metadata
    is_maker Bool,
    sequence_num UInt64 CODEC(T64, ZSTD)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (exchange, symbol, timestamp, trade_id)
TTL timestamp + INTERVAL 90 DAY DELETE
SETTINGS index_granularity = 8192;

-- Add projection for symbol-first queries
ALTER TABLE trades ADD PROJECTION trades_by_symbol (
    SELECT * ORDER BY symbol, exchange, timestamp
);
ALTER TABLE trades MATERIALIZE PROJECTION trades_by_symbol;
```

## Related References

- [Compression Codec Selection](./compression-codec-selection.md)
- [Anti-Patterns and Fixes](./anti-patterns-and-fixes.md)
- [Audit and Diagnostics](./audit-and-diagnostics.md)
