---
name: duckdb
description: DuckDB SQL expertise for analytical queries, file-based data processing, and OLAP workloads. Use when writing DuckDB queries, optimizing analytical SQL, or working with Parquet/CSV/JSON files.
---

## DuckDB Overview

DuckDB is an embedded OLAP database optimized for analytical workloads. It runs in-process, requires no server, and excels at querying files directly.

## Key Syntax Differences

**Division behavior:**
```sql
SELECT 1 / 2;   -- Returns 0.5 (float division, not integer)
SELECT 1 // 2;  -- Returns 0 (integer division)
SELECT 1.0 / 0.0;  -- Returns Infinity (not an error)
```

**Case sensitivity:** DuckDB preserves case but matches case-insensitively.

## Friendly SQL Extensions

**FROM-first syntax:**
```sql
FROM my_table;  -- Equivalent to SELECT * FROM my_table
FROM my_table WHERE x > 5 LIMIT 10;
```

**GROUP BY ALL / ORDER BY ALL:**
```sql
SELECT city, count(*) FROM sales GROUP BY ALL;
SELECT * FROM sales ORDER BY ALL;
```

**SELECT * EXCLUDE / REPLACE:**
```sql
SELECT * EXCLUDE (sensitive_col) FROM users;
SELECT * REPLACE (upper(name) AS name) FROM users;
```

**COLUMNS() expression:**
```sql
SELECT COLUMNS('sales_.*') FROM data;
SELECT max(COLUMNS('numeric_.*')) FROM tbl;  -- Apply function to matching columns
SELECT COLUMNS(a.*) AS 'left_\0', COLUMNS(b.*) AS 'right_\0'  -- Rename in joins
FROM tbl_a a JOIN tbl_b b ON a.id = b.id;
```

**Reusable column aliases (lateral):**
```sql
SELECT i + 1 AS j, j + 2 AS k FROM range(0, 3) t(i);
```

**Prefix aliases:**
```sql
SELECT x: 42, y: 'hello';  -- Same as 42 AS x, 'hello' AS y
```

**LIMIT with percentage:**
```sql
SELECT * FROM tbl LIMIT 10%;
```

**List comprehensions and slicing:**
```sql
SELECT [x * 2 FOR x IN [1, 2, 3]];  -- [2, 4, 6]
SELECT 'DuckDB'[1:4];  -- 'Duck'
SELECT 'DuckDB'[-2:];  -- 'DB'
SELECT [1,2,3,4,5][-1];  -- 5 (last element)
```

**Function chaining with dot operator:**
```sql
SELECT 'hello'.upper().reverse();  -- 'OLLEH'
```

**SQL variables:**
```sql
SET VARIABLE my_date = '2024-01-01';
SELECT * FROM events WHERE date > getvariable('my_date');
```

**TRY expression (returns NULL on error):**
```sql
SELECT TRY(1/0);  -- NULL instead of error
SELECT TRY_CAST('abc' AS INTEGER);  -- NULL instead of error
```

**UNION BY NAME / INSERT BY NAME:**
```sql
SELECT * FROM t1 UNION ALL BY NAME SELECT * FROM t2;  -- Match by column names
INSERT INTO target BY NAME SELECT * FROM source;  -- Column order doesn't matter
```

**Generate series for date spines:**
```sql
SELECT * FROM generate_series(DATE '2024-01-01', DATE '2024-12-31', INTERVAL 1 DAY);
```

## File Querying

**Direct file access (no loading required):**
```sql
SELECT * FROM 'data.parquet';
SELECT * FROM 'data.csv';
SELECT * FROM 'data/*.parquet';  -- Glob patterns
SELECT * FROM read_parquet('s3://bucket/path/*.parquet');
```

**Track source files with filename:**
```sql
SELECT *, filename FROM read_parquet('data/*.parquet', filename=true);
```

**CSV with options:**
```sql
SELECT * FROM read_csv('file.csv', header=true, delim=',');
```

**Hive partitioning:**
```sql
SELECT * FROM read_parquet('data/*/*.parquet', hive_partitioning=true);
```

**Write files:**
```sql
COPY tbl TO 'output.parquet' (FORMAT parquet, COMPRESSION zstd);
COPY tbl TO 'output' (FORMAT parquet, PARTITION_BY (year, month));
```

**Dynamic file URLs:**
```sql
SELECT * FROM read_parquet(
    list_transform(generate_series(1, 12),
        m -> format('s3://bucket/data_{:02d}.parquet', m))
);
```

## CLI Usage

```bash
# Pipe data through DuckDB
cat data.json | duckdb -c "SELECT * FROM read_json_auto('/dev/stdin')"

# One-liner queries
duckdb -c "SUMMARIZE 'data.parquet'"
duckdb -c "DESCRIBE 'data.csv'"

# Output formats
duckdb -markdown -c "FROM data.parquet LIMIT 10"
duckdb -json -c "FROM data.parquet"
duckdb -csv -c "FROM data.parquet"

# Quick format conversion
duckdb -c "COPY (FROM 'input.csv') TO 'output.parquet'"
```

## OLAP Features

**QUALIFY clause (filter window results without subquery):**
```sql
SELECT * FROM sales
QUALIFY row_number() OVER (PARTITION BY region ORDER BY amount DESC) <= 3;
```

**Deduplication pattern:**
```sql
SELECT * FROM tbl
QUALIFY row_number() OVER (PARTITION BY key ORDER BY updated_at DESC) = 1;
```

**FILTER clause:**
```sql
SELECT 
    count(*) AS total,
    count(*) FILTER (WHERE status = 'active') AS active_count
FROM orders;
```

**GROUPING SETS / CUBE / ROLLUP:**
```sql
SELECT city, year, sum(sales)
FROM data GROUP BY CUBE (city, year);
```

**PIVOT / UNPIVOT:**
```sql
PIVOT sales ON year USING sum(amount);
UNPIVOT monthly ON jan, feb, mar INTO NAME month VALUE amount;
```

**Top-N per group (efficient):**
```sql
SELECT arg_max(name, score, 3) FROM students GROUP BY class;
```

**ASOF JOIN (time-series lookups):**
```sql
FROM trades ASOF JOIN quotes USING (symbol, timestamp);
```

## Nested Types

```sql
-- LIST (variable length)
SELECT [1, 2, 3] AS my_list;
SELECT list_aggregate(my_list, 'sum') FROM tbl;

-- STRUCT (named fields)
SELECT {'name': 'Alice', 'age': 30} AS person;
SELECT person.name FROM tbl;

-- MAP
SELECT map([1, 2], ['a', 'b']) AS my_map;
```

## Query Analysis

**DESCRIBE (schema inspection):**
```sql
DESCRIBE my_table;
DESCRIBE SELECT * FROM my_table WHERE x > 5;
```

**EXPLAIN (query plan without execution):**
```sql
EXPLAIN SELECT * FROM tbl WHERE x > 5;
EXPLAIN (FORMAT json) SELECT * FROM tbl;  -- JSON output
EXPLAIN (FORMAT graphviz) SELECT * FROM tbl;  -- DOT format
```

**EXPLAIN ANALYZE (execute and show actual metrics):**
```sql
EXPLAIN ANALYZE SELECT * FROM tbl WHERE x > 5;
```

**Profiling to file:**
```sql
PRAGMA enable_profiling = 'json';
PRAGMA profiling_output = '/tmp/profile.json';
PRAGMA profiling_mode = 'detailed';  -- Include optimizer metrics
SELECT * FROM tbl;
-- Visualize: python -m duckdb.query_graph /tmp/profile.json
```

**SUMMARIZE (quick data profiling):**
```sql
SUMMARIZE my_table;
SUMMARIZE FROM 'data.parquet';
```

## Performance Notes

**No manual indexes needed:** DuckDB auto-creates min-max indexes (zonemaps) for predicate pushdown. Only consider ART indexes for highly selective point queries (<0.1% of data).

**Prefer Parquet:** Supports predicate pushdown, projection pushdown, and compression. Much faster than CSV for repeated queries.

**Memory configuration:**
```sql
SET memory_limit = '8GB';
SET threads = 4;
```

## Useful Aggregates

```sql
-- Statistical
median(x), mode(x), quantile_cont(x, 0.5)
quantile_cont(x, [0.25, 0.5, 0.75])  -- Multiple quantiles at once
stddev_samp(x), corr(y, x), regr_slope(y, x)

-- Collection
list(x), string_agg(x, ', ')
list(item ORDER BY pos ASC)  -- Ordered aggregation

-- Advanced
arg_max(arg, val)  -- Value of arg at max val
arg_min(arg, val)  -- Value of arg at min val
approx_count_distinct(x)  -- HyperLogLog (faster than COUNT DISTINCT)
histogram(x)  -- Frequency distribution
```

## Remote Files (httpfs)

```sql
INSTALL httpfs; LOAD httpfs;

-- Query remote files
SELECT * FROM 'https://example.com/data.parquet';

-- S3 access
CREATE SECRET my_s3 (TYPE S3, KEY_ID 'xxx', SECRET 'yyy', REGION 'us-east-1');
SELECT * FROM 's3://bucket/path/*.parquet';

-- Authenticated HTTP APIs
CREATE SECRET http_auth (
    TYPE HTTP,
    EXTRA_HTTP_HEADERS MAP {'Authorization': 'Bearer TOKEN'}
);
SELECT * FROM read_json('https://api.example.com/data');
```

## Key Extensions

| Extension | Purpose |
|-----------|---------|
| `httpfs` | HTTP/S3 remote file access |
| `spatial` | GIS/geospatial + Excel read/write |
| `fts` | Full-text search |
| `vss` | Vector similarity search (embeddings) |
| `excel` | Native Excel support |
| `delta` | Delta Lake tables |
| `iceberg` | Apache Iceberg tables |
| `postgres` | Query PostgreSQL directly |

**Excel via spatial extension:**
```sql
INSTALL spatial; LOAD spatial;
FROM st_read('file.xlsx', layer='Sheet1');  -- Read
COPY (FROM tbl) TO 'out.xlsx' WITH (FORMAT GDAL, DRIVER 'XLSX');  -- Write
```

## Table Macros (Parameterized Views)

```sql
CREATE MACRO filtered_data(start_date, end_date) AS TABLE
SELECT * FROM events WHERE event_date BETWEEN start_date AND end_date;

SELECT * FROM filtered_data('2024-01-01', '2024-12-31');
```

## Introspection

```sql
DESCRIBE my_table;
SUMMARIZE my_table;
SHOW TABLES;
SELECT * FROM duckdb_tables();
SELECT * FROM duckdb_columns();
SELECT * FROM duckdb_settings();
```

## Common Gotchas

1. **Division returns float** - Use `//` for integer division
2. **Division by zero returns Infinity/NaN** - Not an error like PostgreSQL
3. **No VACUUM for space reclaim** - Only rebuilds statistics
4. **list() includes NULLs** - Use `list(x) FILTER (WHERE x IS NOT NULL)`
5. **Results not deterministic without ORDER BY** - Use `ORDER BY ALL` when needed
6. **Timestamps are timezone-naive by default** - Use `TIMESTAMPTZ` or `SET TimeZone`
7. **EXPLAIN shows estimated cardinality (EC)** - Use `EXPLAIN ANALYZE` for actual metrics
