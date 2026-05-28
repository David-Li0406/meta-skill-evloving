---
name: dataflow-connection-config
description: "DataFlow database connection configuration for SQL (PostgreSQL, MySQL, SQLite), MongoDB, and pgvector. Use when DataFlow connection, database URL, connection string, special characters in password, or connection setup."
---

# DataFlow Connection Configuration

Configure database connections with full support for special characters in passwords and connection pooling.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> Related Skills: [`dataflow-quickstart`](#), [`dataflow-models`](#), [`dataflow-existing-database`](#)
> Related Subagents: `dataflow-specialist` (connection troubleshooting, pooling optimization)

## Quick Reference

- **Format**: `scheme://[user[:pass]@]host[:port]/database`
- **Special Chars**: Fully supported in passwords
- **SQL Databases**: PostgreSQL, MySQL, SQLite (9 nodes per @db.model)
- **Document Database**: MongoDB (8 specialized nodes, flexible schema)
- **Vector Search**: PostgreSQL pgvector (3 vector nodes for RAG/semantic search)
- **Pooling**: Automatic, configurable

## Core Pattern

```python
from dataflow import DataFlow

# PostgreSQL with special characters
db = DataFlow(
    database_url="postgresql://admin:MySecret#123$@localhost:5432/mydb",
    pool_size=20,
    pool_max_overflow=30
)

# SQLite (development)
db_dev = DataFlow(
    database_url="sqlite:///dev.db"
)

# Environment variable (recommended)
import os
db_prod = DataFlow(
    database_url=os.getenv("DATABASE_URL")
)
```

## Common Use Cases

- **Production**: PostgreSQL with connection pooling
- **Development**: SQLite for fast iteration
- **Testing**: In-memory SQLite
- **Multi-Environment**: Different configs per environment
- **Special Passwords**: Passwords with #, $, @, ? characters

## Connection String Format

### PostgreSQL

```python
# Full format
"postgresql://username:password@host:port/database?param=value"

# Examples
"postgresql://user:pass@localhost:5432/mydb"
"postgresql://readonly:secret@replica.host:5432/analytics"
"postgresql://admin:Complex$Pass!@10.0.1.5:5432/production"
```

### SQLite

```python
# File-based
"sqlite:///path/to/database.db"
"sqlite:////absolute/path/database.db"

# In-memory (testing)
"sqlite:///:memory:"
":memory:"  # Shorthand
```

## Key Parameters

```python
db = DataFlow(
    # Connection
    database_url="postgresql://...",

    # Connection pooling
    pool_size=20,              # Base connections
    pool_max_overflow=30,      # Extra connections
    pool_recycle=3600,         # Recycle after 1 hour
    pool_pre_ping=True,        # Validate connections

    # Timeouts
    connect_timeout=10,        # Connection timeout (seconds)
    command_timeout=30,        # Query timeout

    # Behavior
    echo=False,                # SQL logging (debug only)
    auto_migrate=True,         # Auto schema updates
    existing_schema_mode=False # Use existing schema only
)
```

## Common Mistakes

### Mistake 1: URL Encoding Passwords

```python
# Wrong (old workaround, no longer needed)
password = "MySecret%23123%24"  # Manual encoding
db = DataFlow(f"postgresql://user:{password}@host/db")
```

**Fix: Use Password Directly**

```python
# Correct - automatic handling
db = DataFlow("postgresql://user:MySecret#123$@host/db")
```

### Mistake 2: Small Connection Pool

```python
# Wrong - pool exhaustion under load
db = DataFlow(
    database_url="postgresql://...",
    pool_size=5  # Too small for production
)
```

**Fix: Adequate Pool Size**

```python
# Correct
db = DataFlow(
    database_url="postgresql://...",
    pool_size=20,
    pool_max_overflow=30
)
```

## Related Patterns

- **For existing databases**: See [`dataflow-existing-database`](#)
- **For multi-instance**: See [`dataflow-multi-instance`](#)
- **For performance**: See [`dataflow-performance`](#)

## When to Escalate to Subagent

Use `dataflow-specialist` when:
- Connection pool exhaustion
- Timeout issues
- SSL/TLS configuration
- Read/write splitting
- Multi-database setup

## Documentation References

### Primary Sources
- **README Connection Section**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L1033-L1086)
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md#L1033-L1085)

### Related Documentation
- **Pooling Guide**: [`sdk-users/apps/dataflow/docs/advanced/pooling.md`](../../../../sdk-users/apps/dataflow/docs/advanced/pooling.md)
- **Deployment**: [`sdk-users/apps/dataflow/docs/production/deployment.md`](../../../../sdk-users/apps/dataflow/docs/production/deployment.md)

## Examples

### Example 1: Multi-Environment Setup

```python
import os

# Development
if os.getenv("ENV") == "development":
    db = DataFlow("sqlite:///dev.db", auto_migrate=True)

# Staging
elif os.getenv("ENV") == "staging":
    db = DataFlow(
        database_url=os.getenv("DATABASE_URL"),
        pool_size=10,
        auto_migrate=True
    )

# Production
else:
    db = DataFlow(
        database_url=os.getenv("DATABASE_URL"),
        pool_size=20,
        pool_max_overflow=30,
        auto_migrate=False,
        existing_schema_mode=True
    )
```

### Example 2: Connection with Complex Password

```python
# Password with special characters
db = DataFlow(
    database_url="postgresql://admin:P@ssw0rd!#$@db.example.com:5432/prod",
    pool_size=20,
    pool_pre_ping=True,
    connect_timeout=10
)
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Wrong host/port | Verify connection string |
| Password authentication failed | Special chars in password | Use latest DataFlow |
| Pool exhausted | pool_size too small | Increase pool_size |
| Connection timeout | Network/firewall | Check connect_timeout |

## Quick Tips

- Use environment variables for credentials
- Special characters work with no encoding required
- SQLite for development, PostgreSQL for production
- pool_size = 2x CPU cores (typical)
- Enable pool_pre_ping for reliability
- Test connection before deployment

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow connection, database URL, connection string, PostgreSQL connection, SQLite connection, special characters password, connection pool, database setup, connection configuration -->
