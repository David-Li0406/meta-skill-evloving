---
name: dataflow-dialects
description: "SQL database support in DataFlow - PostgreSQL, MySQL, and SQLite with 100% feature parity. Use when asking 'dataflow postgres', 'dataflow mysql', 'dataflow sqlite', or 'database dialects'. For MongoDB or pgvector, see Multi-Database Support Matrix in SKILL.md."
---

# DataFlow SQL Database Dialects

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> DataFlow Version: `0.6.0+`
> **Note**: This guide covers SQL databases. For MongoDB (document database) or pgvector (vector search), see SKILL.md Multi-Database Support Matrix.

## 100% SQL Feature Parity

**All three SQL databases support identical operations:**
- ✅ Same 9 nodes per model (Create, Read, Update, Delete, List, BulkCreate, BulkUpdate, BulkDelete, Count)
- ✅ Identical workflows work across all databases
- ✅ Same query syntax and filtering
- ✅ Full async operations with connection pooling
- ✅ Enterprise features (multi-tenancy, soft deletes, transactions)

## PostgreSQL (Production Enterprise)

```python
from dataflow import DataFlow

db = DataFlow("postgresql://user:pass@localhost:5432/mydb")

# Pros:
# - Advanced features (PostGIS, JSONB, arrays)
# - Multi-writer, full ACID
# - Proven at scale
# - Best for production enterprise apps

# Cons:
# - Requires PostgreSQL server
# - Slightly higher resource usage
```

**Best For:** Production enterprise, PostGIS spatial data, complex analytics, large-scale deployments

## MySQL (Web Hosting)

```python
db = DataFlow("mysql://user:pass@localhost:3306/mydb")

# With charset configuration
db = DataFlow("mysql://user:pass@localhost:3306/mydb?charset=utf8mb4&collation=utf8mb4_unicode_ci")

# Pros:
# - Widely available on web hosting
# - Existing MySQL infrastructure
# - Excellent read performance
# - InnoDB for ACID compliance

# Cons:
# - Requires MySQL server
# - Some advanced features require MySQL 8.0+
```

**Best For:** Web hosting environments, existing MySQL infrastructure, read-heavy workloads, cost optimization

## SQLite (Development/Mobile)

```python
# In-memory (fast testing)
db = DataFlow(":memory:")

# File-based
db = DataFlow("sqlite:///app.db")

# With WAL mode for better concurrency
db = DataFlow("sqlite:///app.db", enable_wal=True)

# Pros:
# - Zero config, no server needed
# - Perfect for development/testing
# - Excellent for mobile apps
# - Single-file database

# Cons:
# - Single-writer (WAL mode improves this)
# - Not recommended for high-concurrency web apps
```

**Best For:** Development/testing, mobile apps, edge computing, serverless functions, desktop applications

## Feature Comparison

| Feature | PostgreSQL | MySQL | SQLite |
|---------|------------|-------|--------|
| **Driver** | asyncpg | aiomysql | aiosqlite + custom pooling |
| **Concurrency** | Multi-writer | Multi-writer (InnoDB) | Single-writer (WAL improves) |
| **Multi-Instance** | ✅ Safe | ✅ Safe | ⚠️ Not for concurrent writes |
| **Setup** | Requires server | Requires server | Zero config |
| **DataFlow Nodes** | ✅ All 9 | ✅ All 9 | ✅ All 9 |
| **Connection Pooling** | ✅ Native | ✅ Native | ✅ Custom |
| **Transactions** | ✅ ACID | ✅ ACID (InnoDB) | ✅ ACID |
| **JSON Support** | ✅ JSONB | ✅ 5.7+ | ✅ JSON1 |
| **Full-Text Search** | ✅ | ✅ | ✅ FTS5 |
| **Best Performance** | Complex queries | Read-heavy | Small datasets |

## Switching Between Databases

```python
import os
from dataflow import DataFlow

# Environment-based selection
env = os.getenv("ENV", "development")

if env == "development":
    # Fast local development
    db = DataFlow(":memory:")

elif env == "staging":
    # MySQL for web hosting compatibility
    db = DataFlow(os.getenv("MYSQL_URL"))

else:
    # PostgreSQL for production
    db = DataFlow(os.getenv("DATABASE_URL"))

# Same model works everywhere
@db.model
class User:
    id: str
    name: str
    email: str

# Same 9 nodes generated regardless of database
```

## Multi-Database Workflows

```python
# Use different databases for different purposes
dev_db = DataFlow(":memory:")  # SQLite for testing
web_db = DataFlow("mysql://...")  # MySQL for web app
prod_db = DataFlow("postgresql://...")  # PostgreSQL for analytics

# Same models work across all
@dev_db.model
@web_db.model
@prod_db.model
class Order:
    customer_id: int
    total: float
```

## Connection Examples

### PostgreSQL
```python
# Basic
db = DataFlow("postgresql://user:pass@localhost:5432/mydb")

# With SSL
db = DataFlow("postgresql://user:pass@localhost:5432/mydb?sslmode=require")

# With pool config
db = DataFlow(
    "postgresql://user:pass@localhost:5432/mydb",
    pool_size=20,
    max_overflow=30
)
```

### MySQL
```python
# Basic
db = DataFlow("mysql://user:pass@localhost:3306/mydb")

# With charset
db = DataFlow("mysql://user:pass@localhost:3306/mydb?charset=utf8mb4")

# With SSL
db = DataFlow(
    "mysql://user:pass@localhost:3306/mydb",
    ssl_ca="/path/to/ca.pem",
    charset="utf8mb4"
)
```

### SQLite
```python
# In-memory
db = DataFlow(":memory:")

# File-based
db = DataFlow("sqlite:///path/to/database.db")

# With WAL mode
db = DataFlow("sqlite:///db.db", enable_wal=True, pool_size=5)
```

## Database Selection Guide

### Choose PostgreSQL When:
- Enterprise production applications
- PostGIS spatial data needed
- Complex analytics and reporting
- High-concurrency write operations
- Advanced features (arrays, JSONB)

### Choose MySQL When:
- Web hosting environments (cPanel, shared hosting)
- Existing MySQL infrastructure
- Read-heavy workloads
- Cost optimization (lower resources than PostgreSQL)
- Integration with MySQL-specific tools

### Choose SQLite When:
- Development and testing
- Mobile applications (iOS/Android)
- Edge computing and IoT
- Serverless functions
- Desktop applications
- Prototyping and demos

## Migration Between Databases

DataFlow makes it easy to migrate between databases:

1. **Export data** from old database using workflows
2. **Change connection string** to new database
3. **Run auto-migration** - DataFlow creates schema automatically
4. **Import data** using bulk operations

The same workflow code works on all databases!

## Documentation

- **Database Support**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#database-connection)
- **Connection Config**: [dataflow-connection-config.md](dataflow-connection-config.md)

<!-- Trigger Keywords: dataflow postgres, dataflow mysql, dataflow sqlite, database dialects, dataflow databases, database selection -->
