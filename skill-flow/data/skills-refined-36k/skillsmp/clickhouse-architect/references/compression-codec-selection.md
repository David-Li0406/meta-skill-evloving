**Skill**: [ClickHouse Architect](../SKILL.md)

# Compression Codec Selection

<!-- ADR: 2025-12-09-clickhouse-architect-skill -->

Decision guide and benchmarks for selecting optimal ClickHouse compression codecs.

## Quick Selection Guide

| Column Type               | Default Codec          | Read-Heavy Alternative | When to Use Alternative         |
| ------------------------- | ---------------------- | ---------------------- | ------------------------------- |
| DateTime/DateTime64       | DoubleDelta + ZSTD     | DoubleDelta + LZ4      | Monotonic, read-heavy workloads |
| Float (prices, gauges)    | Gorilla + ZSTD         | Gorilla + LZ4          | Decompression speed critical    |
| Integer (counters, IDs)   | T64 + ZSTD             | —                      | T64 works best with ZSTD        |
| Integer (slowly changing) | Delta + ZSTD           | Delta + LZ4            | Read-heavy workloads            |
| String (< 10k unique)     | LowCardinality(String) | —                      | Always use LowCardinality       |
| String (high cardinality) | ZSTD(3)                | LZ4                    | Decompression speed critical    |
| General/Mixed             | ZSTD(3)                | LZ4                    | When unsure, ZSTD is safer      |

## Note on Codec Combinations

Delta/DoubleDelta + Gorilla combinations are **blocked by default** via `allow_suspicious_codecs`.

**Why blocked**: Gorilla already performs implicit delta compression internally. Combining Delta/DoubleDelta with Gorilla is **redundant**—it adds overhead without compression benefit.

**Historical context**: A corruption bug existed in this combination (fixed in PR #45615, Jan 2023). The blocking (PR #45652) remains as a best practice guardrail, not because of danger.

**Best practice**: Use each codec family independently for its intended data type:

- DoubleDelta/Delta: Timestamps, monotonic sequences
- Gorilla: Float values (prices, gauges)

```sql
-- Correct usage
price Float64 CODEC(Gorilla, ZSTD)              -- Floats: use Gorilla
timestamp DateTime64 CODEC(DoubleDelta, ZSTD)   -- Timestamps: use DoubleDelta
```

## Codec Reference

### DoubleDelta

**Best for**: Monotonically increasing timestamps, sequence numbers

**How it works**: Stores difference of differences (second derivative)

**Typical ratio**: 10-50x for timestamps

```sql
timestamp DateTime64(3) CODEC(DoubleDelta, ZSTD)
event_time DateTime CODEC(DoubleDelta, ZSTD)
sequence_id UInt64 CODEC(DoubleDelta, ZSTD)  -- If monotonic
```

### Gorilla

**Best for**: Float values (prices, measurements, gauges)

**How it works**: XOR-based encoding for IEEE 754 floats

**Typical ratio**: 5-15x for financial data

**Restriction**: Float32/Float64 only

```sql
price Float64 CODEC(Gorilla, ZSTD)
temperature Float32 CODEC(Gorilla, ZSTD)
percentage Float64 CODEC(Gorilla, ZSTD)
```

### T64

**Best for**: General integers, especially with ZSTD

**How it works**: Transform to 64-bit chunks, compress value distribution

**Typical ratio**: 3-8x

**Note**: Works best with ZSTD, not LZ4

```sql
count UInt64 CODEC(T64, ZSTD)
user_id UInt32 CODEC(T64, ZSTD)
quantity Int64 CODEC(T64, ZSTD)
```

### Delta

**Best for**: Slowly changing integer values

**How it works**: Stores differences between consecutive values

**Typical ratio**: 5-20x for small deltas

```sql
version UInt32 CODEC(Delta, ZSTD)
revision Int32 CODEC(Delta, ZSTD)
```

### LowCardinality

**Best for**: String columns with < 10,000 unique values

**How it works**: Dictionary encoding with integer references

**Typical improvement**: 4x query speed, 3-5x compression

```sql
status LowCardinality(String)
country LowCardinality(String)
exchange LowCardinality(String)
```

### ZSTD

**Best for**: General-purpose compression, always as final codec

**Levels**: 1-22 (default 1, recommended 3 for balance)

```sql
-- Level 3 is good balance of speed/ratio
description String CODEC(ZSTD(3))
json_payload String CODEC(ZSTD(3))
```

### LZ4

**Best for**: Speed-critical scenarios (slightly faster than ZSTD)

**Trade-off**: 10-20% worse compression than ZSTD

```sql
-- Only if decompression speed is critical
log_line String CODEC(LZ4)
```

## Upcoming Codecs

### ALP (Adaptive Lossless floating-Point)

**Status**: 🔄 In Development (PR #91362, Dec 2025)

**Best for**: Float columns with better compression than Gorilla

**How it works**: Adaptive encoding that exploits patterns in floating-point data

**Current status**: Not yet available in any ClickHouse release. PR #91362 is under active review (opened Dec 2, 2025). Issue #60533 tracks the feature request.

**When available**: ALP will provide an alternative to Gorilla for float compression, potentially with better ratios for certain data patterns.

```sql
-- Future syntax (not yet available)
price Float64 CODEC(ALP, ZSTD)  -- Once released
```

## Codec Chaining

Chain specialized codecs with general-purpose compression:

| Specialized Codec | Default Chain | Read-Heavy Alternative        | Notes                        |
| ----------------- | ------------- | ----------------------------- | ---------------------------- |
| DoubleDelta       | ZSTD          | LZ4 (1.76x faster decompress) | LZ4 for monotonic sequences  |
| Gorilla           | ZSTD          | LZ4                           | ZSTD provides better ratio   |
| T64               | ZSTD          | —                             | T64 works best with ZSTD     |
| Delta             | ZSTD          | LZ4                           | LZ4 for read-heavy workloads |

**Decision guide**:

- **ZSTD** (default): Better compression ratio, safer when data patterns unknown
- **LZ4**: 1.76x faster decompression, use when read latency is critical

## Benchmark Results

Typical compression ratios (higher is better):

| Column Type      | No Codec | ZSTD Only | Specialized + ZSTD |
| ---------------- | -------- | --------- | ------------------ |
| DateTime64       | 1x       | 3-4x      | 15-50x             |
| Float prices     | 1x       | 2-3x      | 8-15x              |
| Integer counters | 1x       | 2-4x      | 5-10x              |
| Low-card strings | 1x       | 3-5x      | 10-20x (LowCard)   |

## Validation Query

Check compression effectiveness:

```sql
SELECT
    column,
    type,
    compression_codec,
    formatReadableSize(data_compressed_bytes) AS compressed,
    formatReadableSize(data_uncompressed_bytes) AS uncompressed,
    round(data_uncompressed_bytes / data_compressed_bytes, 2) AS ratio
FROM system.columns
WHERE database = 'your_database'
    AND table = 'your_table'
ORDER BY data_uncompressed_bytes DESC;
```

## Migration

To change codec on existing column:

```sql
-- Add new column with desired codec
ALTER TABLE trades ADD COLUMN price_new Float64 CODEC(Gorilla, ZSTD);

-- Copy data
ALTER TABLE trades UPDATE price_new = price WHERE 1;

-- Swap columns
ALTER TABLE trades DROP COLUMN price;
ALTER TABLE trades RENAME COLUMN price_new TO price;
```

## Related References

- [Schema Design Workflow](./schema-design-workflow.md)
- [Anti-Patterns and Fixes](./anti-patterns-and-fixes.md)
