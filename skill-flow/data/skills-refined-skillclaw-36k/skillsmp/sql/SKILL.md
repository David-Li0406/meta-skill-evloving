---
name: sql
description: "Database querying and analysis using SQLAlchemy 2.0+ with support for PostgreSQL, MySQL, SQLite, and SQL Server. Use when tasks require: (1) Querying databases via SQL, (2) Reading data into DataFrames for analysis, (3) Performing database operations with proper transaction handling. Environment variable with connection string must be set (check resources/RESOURCES.md for available databases and schemas)."
license: "© 2025 Daisyloop Technologies Inc. See LICENSE.txt"
---

# SQL Database Integration

## Before You Start

> **Read `resources/RESOURCES.md` first** to understand available databases, table structures, column types, and relationships before writing any queries. Alternatively, run `scripts/inspect_schema.py` to discover schema programmatically.

## Overview

Query databases using SQLAlchemy 2.0+ with pandas integration for analysis. Supports PostgreSQL, MySQL, SQLite, and SQL Server.

## Quick Start

```python
import os
import pandas as pd
from sqlalchemy import create_engine, text

# Connection string from environment (set via resources)
engine = create_engine(os.environ["DATABASE_URL"])

# Read query results into DataFrame
df = pd.read_sql("SELECT * FROM users LIMIT 10", engine)
print(df.head())
```

## Connection Patterns

### Using Environment Variables

Connection strings are stored as secret resources and injected as environment variables. Check `resources/RESOURCES.md` for the variable name.

```python
import os
from sqlalchemy import create_engine

# Get connection string from environment
conn_str = os.environ["DATABASE_URL"]  # or your specific env var name
engine = create_engine(conn_str)
```

### Engine-Specific Patterns

See `references/engines.md` for connection string formats and driver-specific details for:
- PostgreSQL (psycopg)
- MySQL (pymysql)
- SQLite (built-in)
- SQL Server (pyodbc)

## Read Operations

### Basic Queries with pandas

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(os.environ["DATABASE_URL"])

# Simple query
df = pd.read_sql("SELECT * FROM orders WHERE status = 'pending'", engine)

# With parameters (safe from SQL injection)
df = pd.read_sql(
    "SELECT * FROM orders WHERE customer_id = :cid",
    engine,
    params={"cid": 123}
)
```

### Using SQLAlchemy Core

```python
from sqlalchemy import create_engine, text

engine = create_engine(os.environ["DATABASE_URL"])

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM products WHERE price > :min_price"), {"min_price": 100})
    for row in result:
        print(row)
```

## Write Operations

> **⚠️ EXTREME CAUTION REQUIRED**
>
> Write operations (INSERT, UPDATE, DELETE) **cannot be undone**. Always:
> 1. **Use `--dry-run` first** to preview changes without committing
> 2. **Verify the WHERE clause** - a missing or wrong WHERE affects all rows
> 3. **Start with SELECT** - run the equivalent SELECT to see affected rows
> 4. **Back up data** before bulk updates on production
>
> ```bash
> # ALWAYS dry-run first
> uv run scripts/execute_sql.py "UPDATE users SET active = false WHERE id = 123" --dry-run
> ```

### Transactions

```python
from sqlalchemy import create_engine, text

engine = create_engine(os.environ["DATABASE_URL"])

# Transaction with automatic commit/rollback
with engine.begin() as conn:
    conn.execute(text("UPDATE orders SET status = :status WHERE id = :id"), {"status": "shipped", "id": 123})
    conn.execute(text("INSERT INTO order_history (order_id, event) VALUES (:oid, :event)"), {"oid": 123, "event": "shipped"})
# Commits automatically if no exception, rolls back on error
```

### Insert with Returning

```python
with engine.begin() as conn:
    result = conn.execute(
        text("INSERT INTO users (name, email) VALUES (:name, :email) RETURNING id"),
        {"name": "Alice", "email": "alice@example.com"}
    )
    new_id = result.scalar()
    print(f"Created user with ID: {new_id}")
```

## Further Analysis with Pandas

After loading data, use pandas for analysis:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(os.environ["DATABASE_URL"])

# Load data
df = pd.read_sql("SELECT * FROM sales", engine)

# Analysis
summary = df.groupby("region").agg({
    "revenue": ["sum", "mean"],
    "quantity": "sum"
})

# Filter and transform
recent = df[df["date"] >= "2024-01-01"]
recent["margin"] = recent["revenue"] - recent["cost"]

# Export results
summary.to_excel("output/sales_summary.xlsx")
```

### Large Datasets with Chunking

```python
# Process large tables in chunks
chunks = pd.read_sql("SELECT * FROM large_table", engine, chunksize=10000)

for chunk in chunks:
    # Process each chunk
    processed = chunk[chunk["status"] == "active"]
    # ... further processing
```

## Best Practices

1. **Always parameterize queries** - Never use f-strings or string concatenation for user inputs
2. **Use transactions for writes** - Ensures atomicity and enables rollback
3. **Check schema first** - Read `resources/RESOURCES.md` before writing queries
4. **Close connections** - Use context managers (`with`) to ensure proper cleanup
5. **Limit result sets** - Use `LIMIT` during development to avoid pulling large datasets

## Scripts

Ready-to-use scripts for common database operations:

- `scripts/inspect_schema.py` - Discover tables, columns, keys, and indexes
- `scripts/query_to_dataframe.py` - Execute queries and export as CSV/JSON
- `scripts/execute_sql.py` - Run write operations with transaction safety and dry-run

```bash
# Examples
uv run scripts/inspect_schema.py --table users
uv run scripts/query_to_dataframe.py "SELECT * FROM orders" --format csv
uv run scripts/execute_sql.py "UPDATE users SET active = true" --dry-run
```

## References

- `references/engines.md` - Connection strings, SQL dialect differences, and gotchas
- `references/patterns.md` - Advanced SQL patterns:
  - Window functions (ROW_NUMBER, LAG/LEAD, running totals)
  - CTEs (recursive and non-recursive)
  - Pivoting data
  - Date/time operations by engine
  - JSON operations by engine
