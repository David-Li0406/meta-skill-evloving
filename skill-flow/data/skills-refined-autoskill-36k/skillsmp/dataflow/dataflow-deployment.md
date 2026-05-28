---
name: dataflow-deployment
description: "DataFlow production deployment patterns. Use when asking 'deploy dataflow', 'dataflow production', 'dataflow docker', or 'dataflow fastapi'."
---

# DataFlow Production Deployment

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> SDK Version: `0.10.15+`

## Docker/FastAPI Deployment (v0.10.15+ FIX)

✅ **`auto_migrate=True` NOW WORKS in Docker/FastAPI!**

DataFlow v0.10.15+ uses `SyncDDLExecutor` with synchronous database drivers (psycopg2, sqlite3) for table creation, completely bypassing event loop boundary issues.

### Zero-Config Pattern (Recommended)

```python
from dataflow import DataFlow
from fastapi import FastAPI

# Zero-config: auto_migrate=True (default) now works!
db = DataFlow("postgresql://user:pass@localhost:5432/mydb")

@db.model  # Tables created immediately via sync DDL
class User:
    id: str
    name: str
    email: str

app = FastAPI()

@app.post("/users")
async def create_user(data: dict):
    return await db.express.create("User", data)

@app.get("/users/{id}")
async def get_user(id: str):
    return await db.express.read("User", id)

@app.get("/users")
async def list_users(limit: int = 100):
    return await db.express.list("User", limit=limit)
```

### How It Works

- `SyncDDLExecutor` uses psycopg2 (PostgreSQL) or sqlite3 (SQLite) - no asyncio
- Tables are created synchronously at model registration time
- CRUD operations use async drivers (asyncpg, aiosqlite) as before
- No event loop conflicts because DDL and CRUD use separate connection types

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install DataFlow with PostgreSQL support
RUN pip install kailash-dataflow[postgresql]

COPY . /app

# No special setup needed - auto_migrate=True works!
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Alternative: Manual Table Creation

For explicit control over table creation timing:

```python
from dataflow import DataFlow
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Use auto_migrate=False for manual control
db = DataFlow("postgresql://...", auto_migrate=False)

@db.model
class User:
    id: str
    name: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Option 1: Sync table creation
    db.create_tables_sync()

    # Option 2: Async table creation
    # await db.create_tables_async()

    yield
    await db.close_async()

app = FastAPI(lifespan=lifespan)
```

## ⚠️ In-Memory SQLite Limitation

In-memory databases (`:memory:`) **cannot** use sync DDL because each connection gets a separate database. They automatically fall back to lazy table creation:

```python
# In-memory SQLite: Uses lazy creation (still works, just deferred)
db = DataFlow(":memory:", auto_migrate=True)  # Tables created on first access
```

## Environment Configuration

```python
import os
from dataflow import DataFlow, LoggingConfig

# Use environment variables for production
db = DataFlow(
    os.getenv("DATABASE_URL"),
    log_config=LoggingConfig.production()  # Clean logs
)
```

## Production Settings

| Setting | Development | Production |
|---------|-------------|------------|
| `auto_migrate` | `True` (default) | `True` or `False` |
| `log_config` | `LoggingConfig.development()` | `LoggingConfig.production()` |
| `pool_size` | Default | Configure via database URL |

## Documentation

- **Quickstart**: [`sdk-users/apps/dataflow/docs/getting-started/quickstart.md`](../../../../sdk-users/apps/dataflow/docs/getting-started/quickstart.md)
- **Docker Guide**: [`sdk-users/apps/dataflow/docs/production/deployment.md`](../../../../sdk-users/apps/dataflow/docs/production/deployment.md)

<!-- Trigger Keywords: deploy dataflow, dataflow production, dataflow docker, dataflow kubernetes, dataflow fastapi -->
