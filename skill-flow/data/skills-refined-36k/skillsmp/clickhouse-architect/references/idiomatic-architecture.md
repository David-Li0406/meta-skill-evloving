**Skill**: [ClickHouse Architect](../SKILL.md)

# Idiomatic Architecture

<!-- ADR: 2025-12-09-clickhouse-architect-skill -->

ClickHouse-native patterns that replace traditional database approaches.

## Pattern Mapping

| Traditional Approach  | ClickHouse-Native Alternative    | Improvement                   |
| --------------------- | -------------------------------- | ----------------------------- |
| Repository pattern    | Direct SQL + parameterized views | Simpler                       |
| Regular views         | Parameterized views (23.1+)      | Flexible                      |
| JOINs for lookups     | Dictionaries                     | Up to 6.6x faster (see below) |
| App-level aggregation | Materialized views               | Pre-computed                  |
| DELETE for dedup      | ReplacingMergeTree               | Automatic                     |

**Note**: Dictionary performance gains are context-dependent. See [Dictionaries vs JOINs](#dictionaries-vs-joins-context-dependent) for decision framework.

## Parameterized Views (23.1+)

Replace static views with flexible table functions.

### Basic Example

```sql
-- Create parameterized view
CREATE VIEW trades_by_symbol AS
SELECT *
FROM trades
WHERE symbol = {symbol:String}
    AND timestamp >= {start_time:DateTime64}
    AND timestamp <= {end_time:DateTime64};

-- Query with parameters
SELECT * FROM trades_by_symbol(
    symbol = 'BTCUSDT',
    start_time = '2024-01-01 00:00:00',
    end_time = '2024-01-31 23:59:59'
);
```

### With Nullable Parameters

```sql
CREATE VIEW trades_filtered AS
SELECT *
FROM trades
WHERE symbol = coalesce({symbol:Nullable(String)}, symbol)
    AND exchange = coalesce({exchange:Nullable(String)}, exchange)
    AND timestamp >= {start_time:DateTime64};

-- Query with optional filters
SELECT * FROM trades_filtered(
    symbol = NULL,  -- No symbol filter
    exchange = 'binance',
    start_time = '2024-01-01'
);
```

### Array Parameters

```sql
CREATE VIEW trades_multi_symbol AS
SELECT *
FROM trades
WHERE symbol IN {symbols:Array(String)}
    AND timestamp >= {start_time:DateTime64};

-- Query with multiple symbols
SELECT * FROM trades_multi_symbol(
    symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT'],
    start_time = '2024-01-01'
);
```

## Dictionaries vs JOINs (Context-Dependent)

**Benchmark context**: The "6.6x faster" claim comes from Star Schema Benchmark with **1.4 billion rows** in the fact table.

### v24.4+ JOIN Improvements

ClickHouse 24.4 introduced significant JOIN optimizations:

- Predicate pushdown: **8-180x** faster (180x upper bound)
- Automatic OUTER→INNER conversion
- Enhanced equivalence class analysis

### When to Use Dictionaries (v24.4+)

| Scenario                            | Recommendation                        |
| ----------------------------------- | ------------------------------------- |
| Dimension table <500 rows           | Use JOINs (overhead negligible)       |
| Dimension table 500-10k rows        | Benchmark both approaches             |
| Dimension table >10k rows           | Consider dictionaries                 |
| Fact table >100M rows + star schema | Dictionaries recommended              |
| LEFT ANY JOIN semantics             | Dictionaries (direct join 25x faster) |

### When to Use JOINs (v24.4+)

| Scenario                         | Recommendation                           |
| -------------------------------- | ---------------------------------------- |
| Small dimension tables           | JOINs (v24.4+ optimizations handle well) |
| Complex JOIN types (FULL, RIGHT) | JOINs (dictionaries don't support)       |
| One-to-many relationships        | JOINs (dictionaries deduplicate keys)    |
| Pre-sorted data                  | Full sorting merge join                  |

### Create Dictionary

```sql
-- Source table
CREATE TABLE symbols (
    symbol String,
    name String,
    sector String,
    market_cap Float64
) ENGINE = MergeTree()
ORDER BY symbol;

-- Dictionary for fast lookups
CREATE DICTIONARY symbols_dict (
    symbol String,
    name String,
    sector String,
    market_cap Float64
)
PRIMARY KEY symbol
SOURCE(CLICKHOUSE(TABLE 'symbols'))
LAYOUT(FLAT())  -- Fastest for < 500k keys
LIFETIME(MIN 300 MAX 3600);
```

### Use in Queries

```sql
-- Instead of JOIN
SELECT
    t.symbol,
    t.price,
    dictGet('symbols_dict', 'name', t.symbol) AS symbol_name,
    dictGet('symbols_dict', 'sector', t.symbol) AS sector
FROM trades t
WHERE timestamp > now() - INTERVAL 1 DAY;
```

### Layout Selection

| Layout       | Best For                 | Key Limit | Memory    |
| ------------ | ------------------------ | --------- | --------- |
| FLAT         | Small dictionaries       | < 500k    | Keys x 8B |
| HASHED       | Medium, arbitrary keys   | < 10M     | Moderate  |
| RANGE_HASHED | Time-versioned lookups   | < 10M     | Higher    |
| CACHE        | Very large, infrequent   | Unlimited | LRU cache |
| DIRECT       | Always-fresh from source | N/A       | None      |

### Limitations

- **No duplicate keys**: Silently deduplicated (last value wins)
- **Memory-resident**: FLAT/HASHED load entirely into RAM
- **Update lag**: LIFETIME controls refresh frequency

## ReplacingMergeTree for Deduplication

Handle duplicates with eventual consistency at merge time.

### Basic Deduplication

```sql
CREATE TABLE trades (
    trade_id UInt64,
    symbol String,
    timestamp DateTime64(3),
    price Float64,
    quantity Float64
) ENGINE = ReplacingMergeTree()
ORDER BY (symbol, trade_id);

-- Duplicates with same (symbol, trade_id) merged at merge time
```

### Versioned Deduplication

```sql
CREATE TABLE trades (
    trade_id UInt64,
    symbol String,
    timestamp DateTime64(3),
    price Float64,
    quantity Float64,
    version UInt64  -- Higher version wins
) ENGINE = ReplacingMergeTree(version)
ORDER BY (symbol, trade_id);
```

### Query-Time Deduplication

```sql
-- FINAL forces deduplication at query time (slower)
SELECT * FROM trades FINAL
WHERE symbol = 'BTCUSDT';

-- Partition-aware FINAL (faster for partitioned tables)
SET do_not_merge_across_partitions_select_final = 1;
SELECT * FROM trades FINAL
WHERE symbol = 'BTCUSDT';
```

### Limitations

- **Eventual consistency**: Duplicates exist until merge
- **FINAL is slow**: 100x slower on large tables
- **ORDER BY is key**: Deduplication based on ORDER BY columns

## Materialized Views for Pre-Aggregation

Pre-compute expensive aggregations in real-time.

### Hourly Aggregation

```sql
-- Source table
CREATE TABLE trades (...) ENGINE = MergeTree() ...;

-- Materialized view for hourly stats
CREATE MATERIALIZED VIEW trades_hourly_mv
ENGINE = SummingMergeTree()
ORDER BY (exchange, symbol, hour)
AS SELECT
    exchange,
    symbol,
    toStartOfHour(timestamp) AS hour,
    sum(quantity) AS total_volume,
    sum(price * quantity) AS total_value,
    count() AS trade_count,
    min(price) AS low,
    max(price) AS high
FROM trades
GROUP BY exchange, symbol, hour;

-- Query pre-computed stats (instant)
SELECT * FROM trades_hourly_mv
WHERE symbol = 'BTCUSDT'
    AND hour >= now() - INTERVAL 7 DAY;
```

### AggregatingMergeTree for Complex Aggregates

```sql
CREATE MATERIALIZED VIEW trades_stats_mv
ENGINE = AggregatingMergeTree()
ORDER BY (exchange, symbol, day)
AS SELECT
    exchange,
    symbol,
    toDate(timestamp) AS day,
    sumState(quantity) AS total_volume,
    avgState(price) AS avg_price,
    quantileState(0.5)(price) AS median_price
FROM trades
GROUP BY exchange, symbol, day;

-- Query with merge functions
SELECT
    exchange,
    symbol,
    day,
    sumMerge(total_volume) AS volume,
    avgMerge(avg_price) AS avg,
    quantileMerge(0.5)(median_price) AS median
FROM trades_stats_mv
GROUP BY exchange, symbol, day;
```

### Warning: ReplacingMergeTree + Materialized View

**Avoid** putting AggregatingMergeTree on top of ReplacingMergeTree:

```sql
-- PROBLEMATIC: Duplicates may be aggregated before merge
CREATE MATERIALIZED VIEW stats_mv
ENGINE = SummingMergeTree()
AS SELECT ... FROM replacing_table GROUP BY ...;
```

The materialized view sees duplicates before ReplacingMergeTree merges them.

**Solution**: Use query-time aggregation with FINAL, or pre-deduplicate in a separate table.

## Related References

- [Schema Design Workflow](./schema-design-workflow.md)
- [Anti-Patterns and Fixes](./anti-patterns-and-fixes.md)
- [Audit and Diagnostics](./audit-and-diagnostics.md)
