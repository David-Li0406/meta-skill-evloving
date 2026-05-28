**Skill**: [ClickHouse Architect](../SKILL.md)

# Schema Documentation for AI Understanding

<!-- ADR: 2025-12-09-clickhouse-schema-documentation -->

Schema comments and naming conventions help AI tools understand your ClickHouse schema. This reference provides evidence-based guidance on what works, ClickHouse-specific syntax, and when to graduate to more sophisticated approaches.

## Evidence-Based Positioning

### What the Research Shows

| Approach              | AI Accuracy Improvement | When to Use             |
| --------------------- | ----------------------- | ----------------------- |
| **Comments + Naming** | 20-27%                  | < 50 tables (baseline)  |
| **Data Catalogs**     | 30-40%                  | 50-500 tables           |
| **Semantic Layers**   | 3-4x (16%→54%)          | 500+ tables, enterprise |

**Key insight**: Schema comments are the _essential baseline_, not the complete solution. For small-to-medium schemas, they're sufficient. For enterprise scale, invest in semantic layers (dbt, Cube, AtScale).

**Sources**: AtScale 2025 study, SNAILS (SIGMOD 2025), TigerData research

## ClickHouse COMMENT Syntax

ClickHouse does **NOT** use standard SQL `COMMENT ON` syntax. Use the patterns below.

### Table-Level Comments

```sql
-- At creation
CREATE TABLE trades (
    trade_id UInt64,
    exchange LowCardinality(String),
    symbol LowCardinality(String),
    price Float64,
    quantity Float64,
    timestamp DateTime64(3)
) ENGINE = MergeTree()
ORDER BY (exchange, symbol, timestamp)
COMMENT 'Real-time trade events from crypto exchanges. Partitioned monthly.';

-- After creation
ALTER TABLE trades MODIFY COMMENT 'Updated: includes legacy data migration';
```

### Column-Level Comments

```sql
ALTER TABLE trades
    COMMENT COLUMN trade_id 'Unique identifier from exchange API',
    COMMENT COLUMN symbol 'Trading pair (e.g., BTCUSDT). LowCardinality for <10k unique values',
    COMMENT COLUMN price 'Execution price in quote currency. Use Gorilla codec for floats',
    COMMENT COLUMN timestamp 'Event time from exchange. DoubleDelta codec for monotonic';
```

### Query Comments from System Tables

```sql
-- Table comments
SELECT name, comment
FROM system.tables
WHERE database = 'default' AND name = 'trades';

-- Column comments
SELECT name, comment, type
FROM system.columns
WHERE database = 'default' AND table = 'trades'
ORDER BY position;
```

## Naming Conventions (SNAILS Research)

The SNAILS study (SIGMOD 2025) found that schema identifier "naturalness" has **statistically significant impact** on LLM accuracy. Naming may matter as much as comments.

### Naming Patterns

| Pattern                       | Example                      | Why It Works                     |
| ----------------------------- | ---------------------------- | -------------------------------- |
| **Descriptive nouns**         | `trade_events` not `te`      | LLMs understand natural language |
| **Verb prefixes for derived** | `calculated_vwap` not `vwap` | Signals computation              |
| **Unit suffixes**             | `price_usd`, `latency_ms`    | Eliminates ambiguity             |
| **Temporal qualifiers**       | `created_at`, `updated_at`   | Standard patterns recognized     |

### Anti-Patterns

| Anti-Pattern            | Problem                 | Fix                                            |
| ----------------------- | ----------------------- | ---------------------------------------------- |
| `t1`, `t2`, `temp`      | No semantic meaning     | Use descriptive names                          |
| `data`, `info`, `stuff` | Too generic             | Be specific: `order_data` → `order_line_items` |
| `flag`, `status`        | Unclear boolean meaning | `is_active`, `has_shipped`                     |
| Hungarian notation      | `strName`, `intCount`   | Let types speak: `name`, `count`               |

## Replication Considerations

Comment behavior varies by table engine:

| Operation                | ReplicatedMergeTree  | SharedMergeTree    |
| ------------------------ | -------------------- | ------------------ |
| `MODIFY COMMENT` (table) | Single replica only  | Propagates         |
| `COMMENT COLUMN`         | Propagates correctly | Propagates         |
| MV column comments       | Does NOT propagate   | Does NOT propagate |

**Best practice**: Apply column comments after table creation, before data ingestion. For Materialized Views, apply comments to the target table, not the view itself.

## Integration with Schema Design Workflow

Add comments as **Step 6** in the [Schema Design Workflow](./schema-design-workflow.md):

1. Define ORDER BY key
2. Select compression codecs
3. Configure PARTITION BY
4. Add performance accelerators
5. Validate with audit queries
6. **Document with COMMENT statements** ← NEW

### Complete Example

```sql
-- Step 1-5: Schema creation (see schema-design-workflow.md)
CREATE TABLE trades (
    trade_id UInt64,
    exchange LowCardinality(String),
    symbol LowCardinality(String),
    price Float64 CODEC(Gorilla, ZSTD),
    quantity Float64 CODEC(Gorilla, ZSTD),
    timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (exchange, symbol, timestamp, trade_id)
COMMENT 'Real-time trade events. Source: exchange websocket feeds.';

-- Step 6: Add column comments for AI understanding
ALTER TABLE trades
    COMMENT COLUMN trade_id 'Unique identifier from exchange API. Not globally unique.',
    COMMENT COLUMN exchange 'Exchange name (binance, coinbase, etc.). ~20 values.',
    COMMENT COLUMN symbol 'Trading pair in BASE/QUOTE format (e.g., BTC/USDT).',
    COMMENT COLUMN price 'Execution price in quote currency units.',
    COMMENT COLUMN quantity 'Trade size in base currency units.',
    COMMENT COLUMN timestamp 'Exchange-reported execution time (UTC).';
```

## When to Graduate Beyond Comments

| Project Scale | Recommendation                                  |
| ------------- | ----------------------------------------------- |
| < 50 tables   | COMMENT statements sufficient                   |
| 50-500 tables | Add data catalog (DataHub, Atlan)               |
| 500+ tables   | Semantic layer (dbt, Cube) for 3-4x improvement |

**Signs you need a semantic layer**:

- Multiple teams with different terminology for same concepts
- Business users asking "what does this column mean?" repeatedly
- AI tools generating incorrect queries despite comments
- Schema sprawl making comments hard to maintain

## Related References

- [Schema Design Workflow](./schema-design-workflow.md) - Step 1-5 of schema creation
- [Audit and Diagnostics](./audit-and-diagnostics.md) - Includes `system.columns` queries
