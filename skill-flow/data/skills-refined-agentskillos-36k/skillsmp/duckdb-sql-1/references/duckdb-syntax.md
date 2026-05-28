# DuckDB Syntax Reference

## Table of Contents

- [Data Types](#data-types)
- [String Operations](#string-operations)
- [Date/Time Functions](#datetime-functions)
- [Aggregations](#aggregations)
- [Type Casting](#type-casting)
- [Useful DuckDB Features](#useful-duckdb-features)
- [CLI Commands](#cli-commands)

---

## Data Types

- `INTEGER`, `BIGINT`, `DOUBLE`, `DECIMAL(p,s)`
- `VARCHAR`, `TEXT`
- `DATE`, `TIMESTAMP`, `INTERVAL`
- `BOOLEAN`
- `LIST`, `STRUCT`, `MAP` (nested types)

---

## String Operations

- Concatenation: `||` operator
- Functions: `length()`, `lower()`, `upper()`, `trim()`, `substring()`
- Pattern matching: `LIKE`, `ILIKE` (case-insensitive), `regexp_matches()`

---

## Date/Time Functions

- Current: `current_date`, `current_timestamp`
- Extract: `date_part('year', date_col)`, `extract(month FROM date_col)`
- Truncate: `date_trunc('month', date_col)`
- Format: `strftime(date_col, '%Y-%m-%d')`
- Arithmetic: `date_col + INTERVAL '7 days'`

---

## Aggregations

- Standard: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`
- Advanced: `LIST()`, `STRING_AGG()`, `PERCENTILE_CONT()`
- Window: `ROW_NUMBER()`, `LAG()`, `LEAD()`, `SUM() OVER()`

---

## Type Casting

- `CAST(col AS TYPE)`
- `col::TYPE` (shorthand)
- `TRY_CAST(col AS TYPE)` (returns NULL on failure)

---

## Useful DuckDB Features

- `EXCLUDE` in SELECT: `SELECT * EXCLUDE (col1, col2) FROM table`
- `COLUMNS()` for pattern matching: `SELECT COLUMNS('.*_id') FROM table`
- `UNPIVOT` and `PIVOT` for reshaping
- `SAMPLE` for random sampling: `SELECT * FROM table USING SAMPLE 10%`

---

## CLI Commands

### For .ddb files

```bash
# Get tables from a database
duckdb sales.ddb -c "SELECT table_name FROM information_schema.tables WHERE table_schema='main';"

# Get columns for a table
duckdb sales.ddb -c "DESCRIBE customers;"

# Generate schema file
duckdb sales.ddb -c ".schema" > duckdb_sql_assets/schema_sales.sql

# Sample distinct values for enum detection
duckdb sales.ddb -c "SELECT DISTINCT status FROM orders LIMIT 25;"
```

### For .csv files

```bash
# Get inferred schema
duckdb -c "DESCRIBE SELECT * FROM 'data/transactions.csv';"

# Sample data
duckdb -c "SELECT * FROM 'data/transactions.csv' LIMIT 10;"

# Sample distinct values for enum detection
duckdb -c "SELECT DISTINCT status FROM 'data/transactions.csv' LIMIT 25;"

# Query with explicit options (if auto-detect fails)
duckdb -c "SELECT * FROM read_csv('data/transactions.csv', header=true, delim=',');"
```

### For .parquet files

```bash
# Get embedded schema
duckdb -c "DESCRIBE SELECT * FROM 'data/events.parquet';"

# Sample data
duckdb -c "SELECT * FROM 'data/events.parquet' LIMIT 10;"

# Sample distinct values for enum detection
duckdb -c "SELECT DISTINCT category FROM 'data/events.parquet' LIMIT 25;"
```

### General

```bash
# Check DuckDB version
duckdb -version

# Expand glob pattern to see matched files
ls logs/*.csv
```
