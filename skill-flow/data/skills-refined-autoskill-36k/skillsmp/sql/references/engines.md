# Database Engine Reference

Engine-specific connection patterns and quirks for SQLAlchemy 2.0+.

## PostgreSQL

**Driver**: `psycopg` (psycopg3)

**Connection String**:
```
postgresql+psycopg://user:password@host:5432/database
```

**With Schema**:
```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://user:password@host:5432/database",
    connect_args={"options": "-csearch_path=my_schema"}
)
```

**SSL Connection**:
```python
engine = create_engine(
    "postgresql+psycopg://user:password@host:5432/database?sslmode=require"
)
```

**Notes**:
- Default port: 5432
- Supports `RETURNING` clause for INSERT/UPDATE/DELETE
- Use `::type` for explicit type casting

---

## MySQL

**Driver**: `pymysql`

**Connection String**:
```
mysql+pymysql://user:password@host:3306/database
```

**With Charset**:
```python
engine = create_engine(
    "mysql+pymysql://user:password@host:3306/database?charset=utf8mb4"
)
```

**Notes**:
- Default port: 3306
- Use `charset=utf8mb4` for full Unicode support
- `RETURNING` not supported; use `SELECT LAST_INSERT_ID()` after INSERT
- Case sensitivity depends on server configuration

---

## SQLite

**Driver**: Built-in Python `sqlite3`

**Connection String**:
```
sqlite:///path/to/database.db
```

**In-Memory**:
```
sqlite:///:memory:
```

**Relative Path**:
```python
from pathlib import Path

db_path = Path(__file__).parent / "data.db"
engine = create_engine(f"sqlite:///{db_path}")
```

**Notes**:
- No port or host (file-based or in-memory)
- Limited concurrent write support
- Use `check_same_thread=False` for multi-threaded access:
  ```python
  engine = create_engine("sqlite:///db.sqlite", connect_args={"check_same_thread": False})
  ```

---

## SQL Server (MSSQL)

**Driver**: `pyodbc`

**Connection String**:
```
mssql+pyodbc://user:password@host:1433/database?driver=ODBC+Driver+18+for+SQL+Server
```

**Trusted Connection (Windows)**:
```
mssql+pyodbc://@host/database?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes
```

**With Encryption**:
```python
engine = create_engine(
    "mssql+pyodbc://user:password@host:1433/database"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&encrypt=yes"
    "&TrustServerCertificate=yes"
)
```

**Notes**:
- Default port: 1433
- Requires ODBC driver installed on system
- Use `TOP n` instead of `LIMIT n` for limiting rows
- Schema qualification: `schema.table_name`

---

## Common Patterns

### Connection Pooling

```python
engine = create_engine(
    os.environ["DATABASE_URL"],
    pool_size=5,           # Number of connections to keep
    max_overflow=10,       # Extra connections when pool is full
    pool_timeout=30,       # Seconds to wait for connection
    pool_recycle=1800      # Recycle connections after 30 minutes
)
```

### Echo SQL (Debugging)

```python
engine = create_engine(os.environ["DATABASE_URL"], echo=True)
```

### Dispose Connections

```python
# Clean up all connections (useful at end of script)
engine.dispose()
```

---

## SQL Dialect Differences

Quick reference for syntax differences across engines.

### Row Limiting

| Engine | Syntax |
|--------|--------|
| PostgreSQL | `LIMIT n` or `LIMIT n OFFSET m` |
| MySQL | `LIMIT n` or `LIMIT m, n` |
| SQLite | `LIMIT n` or `LIMIT n OFFSET m` |
| SQL Server | `TOP n` or `OFFSET m ROWS FETCH NEXT n ROWS ONLY` |

### String Functions

| Operation | PostgreSQL | MySQL | SQLite | SQL Server |
|-----------|------------|-------|--------|------------|
| Concatenate | `'a' \|\| 'b'` | `CONCAT('a', 'b')` | `'a' \|\| 'b'` | `'a' + 'b'` or `CONCAT` |
| Length | `LENGTH(s)` | `LENGTH(s)` | `LENGTH(s)` | `LEN(s)` |
| Substring | `SUBSTRING(s, 1, 3)` | `SUBSTRING(s, 1, 3)` | `SUBSTR(s, 1, 3)` | `SUBSTRING(s, 1, 3)` |
| Lowercase | `LOWER(s)` | `LOWER(s)` | `LOWER(s)` | `LOWER(s)` |
| Trim | `TRIM(s)` | `TRIM(s)` | `TRIM(s)` | `LTRIM(RTRIM(s))` |

### NULL Handling

| Operation | PostgreSQL | MySQL | SQLite | SQL Server |
|-----------|------------|-------|--------|------------|
| Coalesce | `COALESCE(a, b)` | `COALESCE(a, b)` | `COALESCE(a, b)` | `COALESCE(a, b)` |
| If null | `COALESCE(a, b)` | `IFNULL(a, b)` | `IFNULL(a, b)` | `ISNULL(a, b)` |
| Null-safe = | `a IS NOT DISTINCT FROM b` | `a <=> b` | `a IS b` | N/A |

### Auto-Increment

| Engine | Definition | Get Last ID |
|--------|------------|-------------|
| PostgreSQL | `SERIAL` or `GENERATED AS IDENTITY` | `RETURNING id` |
| MySQL | `AUTO_INCREMENT` | `SELECT LAST_INSERT_ID()` |
| SQLite | `INTEGER PRIMARY KEY` | `SELECT last_insert_rowid()` |
| SQL Server | `IDENTITY(1,1)` | `SELECT SCOPE_IDENTITY()` |

### Boolean Type

| Engine | Type | True | False |
|--------|------|------|-------|
| PostgreSQL | `BOOLEAN` | `TRUE` | `FALSE` |
| MySQL | `BOOLEAN` (alias for TINYINT) | `1` | `0` |
| SQLite | INTEGER | `1` | `0` |
| SQL Server | `BIT` | `1` | `0` |

---

## Common Gotchas

### PostgreSQL
- **Case-sensitive identifiers**: Quoted identifiers (`"TableName"`) preserve case; unquoted are lowercased
- **Single quotes only**: Use `'string'` for strings, `"identifier"` for identifiers
- **Array indexing**: Arrays are 1-based, not 0-based

### MySQL
- **Case sensitivity**: Table names case-sensitive on Linux, insensitive on Windows/macOS
- **Backticks for identifiers**: Use `` `column` `` not `"column"`
- **ONLY_FULL_GROUP_BY**: Non-aggregated columns in SELECT must be in GROUP BY (default since 5.7)
- **Zero dates**: `0000-00-00` is valid unless `NO_ZERO_DATE` mode enabled

### SQLite
- **Type affinity**: No strict types; `INTEGER`, `TEXT`, etc. are affinities, not constraints
- **Single writer**: Only one write transaction at a time; reads can occur concurrently
- **No ALTER COLUMN**: Use table rebuild to change column types
- **Boolean**: No native boolean; use `0` and `1`

### SQL Server
- **Square brackets**: Use `[column]` for identifiers (or `"column"` with QUOTED_IDENTIFIER ON)
- **GO is not SQL**: `GO` is a batch separator for SSMS, not part of T-SQL
- **TOP requires ORDER BY**: `TOP` without `ORDER BY` returns arbitrary rows
- **Datetime precision**: `DATETIME` has ~3.33ms precision; use `DATETIME2` for higher
