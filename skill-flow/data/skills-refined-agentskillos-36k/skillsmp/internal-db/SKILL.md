---
name: internal-db
description: "Persist data across ticket executions using MotherDuck/DuckDB. Use when tasks require: (1) Storing workflow state that persists between tickets, (2) Caching expensive computations or API results, (3) Maintaining lookup tables for business logic, (4) Tracking execution history and audit logs. Check `resources/INTERNAL_DB.md` for current schema. Environment variable FULCRUM_INTERNAL_DB_RW must be set."
license: "© 2025 Daisyloop Technologies Inc. See LICENSE.txt"
---

# Internal Database (MotherDuck/DuckDB)

## Before You Start

> **Check `resources/INTERNAL_DB.md` first** to understand existing tables, columns, and relationships before writing queries or creating new tables.

## Prerequisites

Before using the internal DB, verify credentials are available:

```python
import os

if not os.environ.get('FULCRUM_INTERNAL_DB_RW'):
    print("Internal DB not available - skipping DB operations")
    # Continue with non-DB logic or exit gracefully
```

If credentials are not set, the internal DB is still being provisioned. Skip DB operations for now - the next sandbox run will automatically retry provisioning.

## Overview

The internal database is a per-project MotherDuck (cloud DuckDB) database for persisting data across agent runs. Use it for workflow state, caching, lookup tables, and audit logs.

**Key characteristics:**
- Persists across ticket executions within the same project
- Schema introspected after unfurl and documented in `resources/INTERNAL_DB.md`
- Uses standard SQL with DuckDB extensions

## Quick Start

```python
import os
import duckdb

token = os.environ["FULCRUM_INTERNAL_DB_RW"]
db_name = os.environ["FULCRUM_INTERNAL_DB_NAME"]

# Connect to MotherDuck
conn = duckdb.connect(f"md:{db_name}?motherduck_token={token}")

# Query existing data
result = conn.execute("SELECT * FROM my_table LIMIT 10").fetchall()

# Always close when done
conn.close()
```

## Connection Patterns

### Pattern 1: Token in Connection String (Recommended)

```python
import os
import duckdb

token = os.environ["FULCRUM_INTERNAL_DB_RW"]
db_name = os.environ["FULCRUM_INTERNAL_DB_NAME"]

conn = duckdb.connect(f"md:{db_name}?motherduck_token={token}")
```

### Pattern 2: Token in Config

```python
conn = duckdb.connect(
    f"md:{db_name}",
    config={"motherduck_token": token}
)
```

### Pattern 3: Using motherduck_token Env Var

The `motherduck_token` environment variable is automatically set as an alias. DuckDB will use it automatically:

```python
# motherduck_token env var is already set
conn = duckdb.connect(f"md:{db_name}")
```

### Single Database Mode

To restrict access to only the project's database:

```python
conn = duckdb.connect(
    f"md:{db_name}?motherduck_token={token}",
    config={"motherduck_attach_mode": "single"}
)
```

## Creating Tables

Always use `IF NOT EXISTS` for idempotent table creation:

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS workflow_state (
        id INTEGER PRIMARY KEY,
        key VARCHAR NOT NULL UNIQUE,
        value VARCHAR,
        updated_at TIMESTAMP DEFAULT now()
    )
""")
```

## Read Operations

### Basic Query

```python
# Fetch all results
rows = conn.execute("SELECT * FROM workflow_state").fetchall()

# Fetch as DataFrame
import pandas as pd
df = conn.execute("SELECT * FROM workflow_state").df()
```

### Parameterized Queries

```python
# Positional parameters
row = conn.execute(
    "SELECT * FROM workflow_state WHERE key = ?",
    ["my_key"]
).fetchone()

# Named parameters
row = conn.execute(
    "SELECT * FROM workflow_state WHERE key = $key",
    {"key": "my_key"}
).fetchone()
```

## Write Operations

> **Warning:** Write operations cannot be undone. Verify data before committing.

### Insert

```python
conn.execute(
    "INSERT INTO workflow_state (id, key, value) VALUES (?, ?, ?)",
    [1, "status", "completed"]
)
```

### Upsert (Insert or Update)

```python
conn.execute("""
    INSERT INTO workflow_state (id, key, value, updated_at)
    VALUES (?, ?, ?, now())
    ON CONFLICT (key) DO UPDATE SET
        value = excluded.value,
        updated_at = excluded.updated_at
""", [1, "status", "in_progress"])
```

### Bulk Insert

```python
import pandas as pd

df = pd.DataFrame({
    "key": ["a", "b", "c"],
    "value": ["1", "2", "3"]
})

conn.execute("INSERT INTO workflow_state (key, value) SELECT * FROM df")
```

### Update

```python
conn.execute(
    "UPDATE workflow_state SET value = ? WHERE key = ?",
    ["new_value", "my_key"]
)
```

### Delete

```python
conn.execute("DELETE FROM workflow_state WHERE key = ?", ["old_key"])
```

## Context Manager Pattern

For automatic connection cleanup:

```python
import os
import duckdb
from contextlib import contextmanager

@contextmanager
def get_internal_db():
    token = os.environ.get("FULCRUM_INTERNAL_DB_RW")
    db_name = os.environ.get("FULCRUM_INTERNAL_DB_NAME")

    if not token or not db_name:
        raise ValueError("Internal DB not configured")

    conn = duckdb.connect(f"md:{db_name}?motherduck_token={token}")
    try:
        yield conn
    finally:
        conn.close()

# Usage
with get_internal_db() as conn:
    result = conn.execute("SELECT * FROM my_table").fetchall()
```

## Best Practices

1. **Check credentials first** - Always verify `FULCRUM_INTERNAL_DB_RW` is set before attempting operations
2. **Use parameterized queries** - Never use f-strings or string concatenation for user inputs
3. **Close connections** - Use context managers or explicit `conn.close()` to release resources
4. **Create tables idempotently** - Always use `IF NOT EXISTS` for table creation
5. **Check schema documentation** - Read `resources/INTERNAL_DB.md` before writing queries
6. **Document new tables** - When creating tables during unfurl, add docstrings describing the schema

## Scripts

Ready-to-use scripts for common database operations:

- `scripts/inspect_internal_db.py` - Discover tables, columns, and schema
- `scripts/query_internal_db.py` - Execute queries and export as CSV/JSON

```bash
# List all tables
uv run skills/internal-db/scripts/inspect_internal_db.py

# Inspect specific table
uv run skills/internal-db/scripts/inspect_internal_db.py --table workflow_state

# Query to CSV
uv run skills/internal-db/scripts/query_internal_db.py "SELECT * FROM cache LIMIT 10"

# Query to JSON file
uv run skills/internal-db/scripts/query_internal_db.py "SELECT * FROM audit_log" --format json --output audit.json
```

## References

- `references/patterns.md` - Common usage patterns:
  - Workflow state management (key-value storage, checkpoints)
  - Caching with TTL (memoization, invalidation)
  - Lookup tables (configuration, business rules)
  - Audit logging (change tracking, execution history)
  - Session context (ticket-scoped data)
  - Schema versioning and migrations (dry-run testing, data preservation)

## Differences from sql Skill

| Aspect | `internal-db` | `sql` |
|--------|---------------|-------|
| Purpose | Persist project data across tickets | Query external user databases |
| Database | MotherDuck (cloud DuckDB) | PostgreSQL, MySQL, SQLite, SQL Server |
| Credentials | System-injected | User-provided connection strings |
| Library | `duckdb` Python client | SQLAlchemy 2.0+ |
| Schema docs | `resources/INTERNAL_DB.md` | `resources/RESOURCES.md` |
