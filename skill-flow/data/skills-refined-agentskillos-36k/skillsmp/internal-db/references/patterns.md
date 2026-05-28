# Internal Database Patterns

Common usage patterns for the internal MotherDuck database. These patterns address typical needs for persisting data across ticket executions.

## Table of Contents

1. [Workflow State Management](#workflow-state-management)
2. [Caching Expensive Operations](#caching-expensive-operations)
3. [Lookup Tables](#lookup-tables)
4. [Audit Logging](#audit-logging)
5. [Session Context](#session-context)
6. [Schema Versioning & Migrations](#schema-versioning--migrations)

---

## Workflow State Management

Store state that persists between ticket executions.

### Key-Value State Table

```python
# Create table (idempotent)
conn.execute("""
    CREATE TABLE IF NOT EXISTS workflow_state (
        key VARCHAR PRIMARY KEY,
        value VARCHAR,
        updated_at TIMESTAMP DEFAULT now()
    )
""")

# Get state
def get_state(conn, key: str) -> str | None:
    result = conn.execute(
        "SELECT value FROM workflow_state WHERE key = ?", [key]
    ).fetchone()
    return result[0] if result else None

# Set state (upsert)
def set_state(conn, key: str, value: str):
    conn.execute("""
        INSERT INTO workflow_state (key, value, updated_at)
        VALUES (?, ?, now())
        ON CONFLICT (key) DO UPDATE SET
            value = excluded.value,
            updated_at = now()
    """, [key, value])
```

### Status Tracking Across Tickets

```python
# Track multi-step workflow progress
conn.execute("""
    CREATE TABLE IF NOT EXISTS workflow_progress (
        workflow_id VARCHAR PRIMARY KEY,
        current_step INTEGER DEFAULT 0,
        total_steps INTEGER,
        status VARCHAR DEFAULT 'pending',
        started_at TIMESTAMP DEFAULT now(),
        completed_at TIMESTAMP
    )
""")

# Update progress
def update_progress(conn, workflow_id: str, step: int, status: str = "in_progress"):
    completed = "now()" if status == "completed" else "NULL"
    conn.execute(f"""
        UPDATE workflow_progress
        SET current_step = ?, status = ?, completed_at = {completed}
        WHERE workflow_id = ?
    """, [step, status, workflow_id])
```

### Checkpoint/Resume Pattern

```python
# Save checkpoint before expensive operation
def save_checkpoint(conn, task_id: str, checkpoint_data: dict):
    import json
    conn.execute("""
        INSERT INTO workflow_state (key, value)
        VALUES (?, ?)
        ON CONFLICT (key) DO UPDATE SET value = excluded.value, updated_at = now()
    """, [f"checkpoint:{task_id}", json.dumps(checkpoint_data)])

# Resume from checkpoint
def load_checkpoint(conn, task_id: str) -> dict | None:
    import json
    result = conn.execute(
        "SELECT value FROM workflow_state WHERE key = ?",
        [f"checkpoint:{task_id}"]
    ).fetchone()
    return json.loads(result[0]) if result else None
```

---

## Caching Expensive Operations

Cache API results or expensive computations with TTL.

### Cache Table with TTL

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS cache (
        key VARCHAR PRIMARY KEY,
        value VARCHAR,
        created_at TIMESTAMP DEFAULT now(),
        expires_at TIMESTAMP
    )
""")

# Get cached value (respecting TTL)
def get_cached(conn, key: str) -> str | None:
    result = conn.execute("""
        SELECT value FROM cache
        WHERE key = ?
        AND (expires_at IS NULL OR expires_at > now())
    """, [key]).fetchone()
    return result[0] if result else None

# Set cached value with TTL (hours)
def set_cached(conn, key: str, value: str, ttl_hours: int = 24):
    conn.execute("""
        INSERT INTO cache (key, value, expires_at)
        VALUES (?, ?, now() + INTERVAL ? HOUR)
        ON CONFLICT (key) DO UPDATE SET
            value = excluded.value,
            created_at = now(),
            expires_at = excluded.expires_at
    """, [key, value, ttl_hours])
```

### Memoization Pattern

```python
import json
import hashlib

def memoize_to_db(conn, func_name: str, args: tuple, compute_fn):
    """Memoize function results to internal DB."""
    # Create cache key from function name and args
    key = f"{func_name}:{hashlib.md5(json.dumps(args).encode()).hexdigest()}"

    # Check cache
    cached = get_cached(conn, key)
    if cached:
        return json.loads(cached)

    # Compute and cache
    result = compute_fn(*args)
    set_cached(conn, key, json.dumps(result))
    return result
```

### Cache Invalidation

```python
# Invalidate specific key
def invalidate_cache(conn, key: str):
    conn.execute("DELETE FROM cache WHERE key = ?", [key])

# Invalidate by prefix (e.g., all "api:" keys)
def invalidate_cache_prefix(conn, prefix: str):
    conn.execute("DELETE FROM cache WHERE key LIKE ?", [f"{prefix}%"])

# Clean expired entries
def clean_expired_cache(conn):
    conn.execute("DELETE FROM cache WHERE expires_at < now()")
```

---

## Lookup Tables

Store reference data and configuration.

### Configuration Table

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS config (
        key VARCHAR PRIMARY KEY,
        value VARCHAR,
        description VARCHAR
    )
""")

# Get config with default
def get_config(conn, key: str, default: str = None) -> str:
    result = conn.execute(
        "SELECT value FROM config WHERE key = ?", [key]
    ).fetchone()
    return result[0] if result else default
```

### Business Rules Table

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS business_rules (
        rule_name VARCHAR PRIMARY KEY,
        rule_type VARCHAR,
        rule_value VARCHAR,
        active BOOLEAN DEFAULT TRUE,
        effective_from TIMESTAMP DEFAULT now(),
        effective_until TIMESTAMP
    )
""")

# Get active rules
def get_active_rules(conn, rule_type: str) -> list[dict]:
    result = conn.execute("""
        SELECT rule_name, rule_value FROM business_rules
        WHERE rule_type = ?
        AND active = TRUE
        AND effective_from <= now()
        AND (effective_until IS NULL OR effective_until > now())
    """, [rule_type]).fetchall()
    return [{"name": r[0], "value": r[1]} for r in result]
```

---

## Audit Logging

Track execution history and changes.

### Audit Log Table

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT now(),
        action VARCHAR NOT NULL,
        entity_type VARCHAR,
        entity_id VARCHAR,
        details VARCHAR,
        ticket_id VARCHAR
    )
""")

# Log an action
def log_action(conn, action: str, entity_type: str = None,
               entity_id: str = None, details: dict = None):
    import json
    import os
    ticket_id = os.environ.get("FULCRUM_TICKET_UUID")
    conn.execute("""
        INSERT INTO audit_log (action, entity_type, entity_id, details, ticket_id)
        VALUES (?, ?, ?, ?, ?)
    """, [action, entity_type, entity_id,
          json.dumps(details) if details else None, ticket_id])
```

### Change Tracking Pattern

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS change_log (
        id INTEGER PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT now(),
        table_name VARCHAR NOT NULL,
        record_id VARCHAR NOT NULL,
        field_name VARCHAR NOT NULL,
        old_value VARCHAR,
        new_value VARCHAR,
        changed_by VARCHAR
    )
""")

# Log a field change
def log_change(conn, table: str, record_id: str,
               field: str, old_val, new_val):
    conn.execute("""
        INSERT INTO change_log (table_name, record_id, field_name, old_value, new_value)
        VALUES (?, ?, ?, ?, ?)
    """, [table, str(record_id), field, str(old_val), str(new_val)])
```

---

## Session Context

Store ticket-scoped temporary data.

### Ticket Context Table

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS ticket_context (
        ticket_id VARCHAR NOT NULL,
        key VARCHAR NOT NULL,
        value VARCHAR,
        created_at TIMESTAMP DEFAULT now(),
        PRIMARY KEY (ticket_id, key)
    )
""")

# Store context for current ticket
def set_ticket_context(conn, key: str, value: str):
    import os
    ticket_id = os.environ.get("FULCRUM_TICKET_UUID", "unknown")
    conn.execute("""
        INSERT INTO ticket_context (ticket_id, key, value)
        VALUES (?, ?, ?)
        ON CONFLICT (ticket_id, key) DO UPDATE SET
            value = excluded.value
    """, [ticket_id, key, value])

# Get context for current ticket
def get_ticket_context(conn, key: str) -> str | None:
    import os
    ticket_id = os.environ.get("FULCRUM_TICKET_UUID", "unknown")
    result = conn.execute("""
        SELECT value FROM ticket_context
        WHERE ticket_id = ? AND key = ?
    """, [ticket_id, key]).fetchone()
    return result[0] if result else None
```

### Cleanup Old Context

```python
# Clean up context older than N days
def cleanup_old_context(conn, days: int = 7):
    conn.execute("""
        DELETE FROM ticket_context
        WHERE created_at < now() - INTERVAL ? DAY
    """, [days])
```

---

## Schema Versioning & Migrations

Track and manage schema changes safely.

### Migration Tracking Table

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        applied_at TIMESTAMP DEFAULT now()
    )
""")

# Check if migration was applied
def migration_applied(conn, version: int) -> bool:
    result = conn.execute(
        "SELECT 1 FROM schema_migrations WHERE version = ?", [version]
    ).fetchone()
    return result is not None

# Record migration
def record_migration(conn, version: int, name: str):
    conn.execute("""
        INSERT INTO schema_migrations (version, name)
        VALUES (?, ?)
    """, [version, name])
```

### Dry-Run Migration Pattern

**Always test migrations before applying:**

```python
def migrate_with_dry_run(conn, migration_sql: str, dry_run: bool = True) -> dict:
    """
    Test migration before applying.

    Args:
        conn: DuckDB connection
        migration_sql: SQL to execute
        dry_run: If True, rollback changes after testing

    Returns:
        Dict with status and any errors
    """
    try:
        conn.execute("BEGIN TRANSACTION")
        conn.execute(migration_sql)

        if dry_run:
            conn.execute("ROLLBACK")
            return {"status": "dry_run_success", "applied": False}
        else:
            conn.execute("COMMIT")
            return {"status": "success", "applied": True}

    except Exception as e:
        conn.execute("ROLLBACK")
        return {"status": "error", "error": str(e), "applied": False}
```

### Safe Migration Workflow

**For any schema change during unfurl:**

```python
def safe_migrate(conn, version: int, name: str, migration_sql: str):
    """
    Safe migration workflow:
    1. Check if already applied
    2. Dry-run to test
    3. Apply if dry-run succeeds
    4. Record migration
    """
    # Step 1: Check if already applied
    if migration_applied(conn, version):
        print(f"Migration {version} already applied, skipping")
        return

    # Step 2: Dry-run test
    print(f"Testing migration {version}: {name}")
    result = migrate_with_dry_run(conn, migration_sql, dry_run=True)

    if result["status"] != "dry_run_success":
        raise Exception(f"Migration dry-run failed: {result.get('error')}")

    # Step 3: Apply migration
    print(f"Applying migration {version}: {name}")
    result = migrate_with_dry_run(conn, migration_sql, dry_run=False)

    if result["status"] != "success":
        raise Exception(f"Migration failed: {result.get('error')}")

    # Step 4: Record migration
    record_migration(conn, version, name)
    print(f"Migration {version} applied successfully")
```

### Data Preservation During Schema Changes

**Never DROP TABLE without backup:**

```python
def backup_table(conn, table_name: str) -> str:
    """Backup table before destructive operation."""
    backup_name = f"{table_name}_backup_{int(time.time())}"
    conn.execute(f"CREATE TABLE {backup_name} AS SELECT * FROM {table_name}")
    return backup_name
```

**Safe column type change (preserves data):**

```python
def safe_column_type_change(conn, table: str, column: str,
                            new_type: str, transform: str = None):
    """
    Safely change column type while preserving data.

    Args:
        table: Table name
        column: Column to change
        new_type: New column type
        transform: SQL expression to transform data (default: CAST)
    """
    temp_col = f"{column}_new"
    transform = transform or f"CAST({column} AS {new_type})"

    # Step 1: Add new column
    conn.execute(f"ALTER TABLE {table} ADD COLUMN {temp_col} {new_type}")

    # Step 2: Copy data with transformation
    conn.execute(f"UPDATE {table} SET {temp_col} = {transform}")

    # Step 3: Verify data
    null_count = conn.execute(f"""
        SELECT COUNT(*) FROM {table}
        WHERE {temp_col} IS NULL AND {column} IS NOT NULL
    """).fetchone()[0]

    if null_count > 0:
        conn.execute(f"ALTER TABLE {table} DROP COLUMN {temp_col}")
        raise Exception(f"Data loss detected: {null_count} rows would lose data")

    # Step 4: Drop old, rename new
    conn.execute(f"ALTER TABLE {table} DROP COLUMN {column}")
    conn.execute(f"ALTER TABLE {table} RENAME COLUMN {temp_col} TO {column}")
```

**Add column with backfill:**

```python
def add_column_with_backfill(conn, table: str, column: str,
                             col_type: str, backfill_sql: str):
    """Add column and populate with data from existing columns."""
    # Add nullable column first
    conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

    # Backfill data
    conn.execute(f"UPDATE {table} SET {column} = {backfill_sql}")

    # Verify backfill
    null_count = conn.execute(f"""
        SELECT COUNT(*) FROM {table} WHERE {column} IS NULL
    """).fetchone()[0]

    print(f"Added column {column}, backfilled {null_count} NULL values remain")
```
