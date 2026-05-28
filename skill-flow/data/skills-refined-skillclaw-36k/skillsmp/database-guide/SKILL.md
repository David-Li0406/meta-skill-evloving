---
name: database-guide
description: Set up and manage PostgreSQL databases in FastAPI applications using Docker for local development (single-command, no docker-compose) and environment variables for production. Follows no-migrations philosophy - drop and recreate on schema changes. Covers setup_postgres.sh scripts, environment files (must source manually, NOT auto-loaded), pydantic-settings config, SQLModel connections, lifespan handlers, session management, and pytest with in-memory SQLite. Use when configuring database connections, creating setup scripts, handling schema changes, or troubleshooting database issues.
---

# Database Management Guide

Guide for PostgreSQL database setup in FastAPI applications using Docker and environment-based configuration.

## Core Philosophy

1. **Simple local Docker** - Single command, no docker-compose
2. **Remote PostgreSQL for production** - Environment variable based
3. **No migrations** - Delete and re-index when schema changes
4. **Environment files NOT auto-loaded** - Must source before running

## Quick Start Checklist

When setting up a new project with PostgreSQL:

- [ ] Create `setup_postgres.sh` script
- [ ] Add `deployment/*.env` to `.gitignore`
- [ ] Create `deployment/demo.env` with local credentials
- [ ] Create `backend/app/config.py` with Settings class
- [ ] Create `backend/app/database.py` with engine and session
- [ ] Add lifespan handler to `main.py` for table creation
- [ ] Create `backend/tests/conftest.py` with SQLite fixture
- [ ] Add PostgreSQL dependencies to `requirements.txt`

## Step-by-Step Setup

### 1. Create Docker Setup Script

Create `setup_postgres.sh` in project root:

```bash
#!/bin/bash
# Stop and remove existing container if it exists
docker stop <app>-db 2>/dev/null
docker rm <app>-db 2>/dev/null

# Start PostgreSQL container
docker run -d \
    --name <app>-db \
    -e POSTGRES_USER=<app> \
    -e POSTGRES_PASSWORD=<app> \
    -e POSTGRES_DB=<app> \
    -p 5432:5432 \
    -v <app>_postgres_data:/var/lib/postgresql/data \
    postgres:16-alpine

echo "PostgreSQL container started"
echo "Waiting for database to be ready..."
sleep 5
```

**Replace `<app>` with your application name.**

Make executable and run:
```bash
chmod +x setup_postgres.sh
./setup_postgres.sh
```

### 2. Create Environment Files

**Development** (`deployment/demo.env`):
```bash
# Database configuration
export POSTGRES_USER="<app>"
export POSTGRES_PASSWORD="<dev-password>"
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DB="<app>"
```

**Production** (`deployment/production.env`):
```bash
# Remote PostgreSQL credentials
export POSTGRES_USER="<production-user>"
export POSTGRES_PASSWORD="<secure-password>"
export POSTGRES_HOST="<remote-host>"
export POSTGRES_PORT="5432"
export POSTGRES_DB="<production-db>"
```

**CRITICAL:** Add to `.gitignore`:
```
deployment/*.env
```

### 3. Backend Configuration

**Config file** (`backend/app/config.py`):

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "<app-name>"

    # PostgreSQL connection components - read from environment
    postgres_user: str = "<app>"
    postgres_password: str = "<app>"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "<app>"

    @property
    def database_url(self) -> str:
        """Construct database URL from components"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        # Settings come from environment only - no .env file auto-loading
        # User must source deployment/*.env before running backend
        pass

settings = Settings()
```

**Database connection** (`backend/app/database.py`):

```python
from sqlmodel import create_engine, SQLModel, Session
from .config import settings
import os

# Check for explicit SQL echo setting from environment
sql_echo = os.environ.get("SQL_ECHO", "false").lower() == "true"

# Create engine using database URL from settings
engine = create_engine(settings.database_url, echo=sql_echo)

def create_db_and_tables():
    """Create all database tables based on SQLModel definitions"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI dependency that provides a database session"""
    with Session(engine) as session:
        yield session
```

### 4. Application Startup

Add lifespan handler in `backend/app/main.py`:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database initialized")

    yield

    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
```

### 5. Use Database in Endpoints

```python
from fastapi import Depends
from sqlmodel import Session
from .database import get_session

@app.get("/items")
def get_items(session: Session = Depends(get_session)):
    items = session.query(Item).all()
    return items

@app.post("/items")
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
```

## Testing Setup

Tests use **in-memory SQLite** for speed and isolation.

**Test configuration** (`backend/tests/conftest.py`):

```python
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh in-memory SQLite database for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
```

**Using in tests:**

```python
def test_create_item(session: Session):
    item = Item(name="Test Item")
    session.add(item)
    session.commit()

    assert item.id is not None
```

## Daily Workflow

### Starting Development

```bash
# 1. Start PostgreSQL container (if not running)
./setup_postgres.sh

# 2. Load environment variables
source deployment/demo.env

# 3. Start backend
source .venv/bin/activate
uvicorn backend.main:app --reload
```

**IMPORTANT:** Always source the environment file before running the backend!

### Managing the Container

```bash
# Check if running
docker ps

# Stop container
docker stop <app>-db

# Start existing container
docker start <app>-db

# Remove container (keeps volume data)
docker rm <app>-db

# View logs
docker logs <app>-db
```

## Handling Schema Changes

**No migrations!** When schema changes:

```bash
# 1. Stop backend (Ctrl+C)

# 2. Delete database
docker stop <app>-db
docker rm <app>-db
docker volume rm <app>_postgres_data

# 3. Recreate database
./setup_postgres.sh

# 4. Restart backend (tables auto-created)
source deployment/demo.env
uvicorn backend.main:app --reload

# 5. Re-seed data as needed
```

## Dependencies

**requirements.txt:**
```txt
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
sqlmodel>=0.0.22
psycopg2-binary>=2.9.10
pydantic-settings>=2.0.0
```

**Dev dependencies:**
```txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

## Troubleshooting

### Connection Refused
- Check container running: `docker ps`
- Verify environment variables: `echo $POSTGRES_HOST`
- Check port binding: `docker port <app>-db`

### Password Authentication Failed
- Ensure environment variables match Docker container
- Test with psql: `psql -h localhost -U <app> -d <app>`

### Tables Not Created
- Verify `create_db_and_tables()` called in lifespan
- Check SQLModel imports `SQLModel` as base
- Look for errors in startup logs

### Port Already in Use
- Stop existing PostgreSQL: `docker stop <app>-db`
- Or use different port in Docker command

## SQL Query Logging

Enable detailed logging:
```bash
export SQL_ECHO=true
source deployment/demo.env
uvicorn backend.main:app --reload
```

## Common Patterns

### Multiple Database Models

```python
# backend/app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
```

### Transaction Management

```python
@app.post("/transfer")
def transfer(
    from_id: int,
    to_id: int,
    amount: float,
    session: Session = Depends(get_session)
):
    try:
        # All operations in single transaction
        from_account = session.get(Account, from_id)
        to_account = session.get(Account, to_id)

        from_account.balance -= amount
        to_account.balance += amount

        session.add(from_account)
        session.add(to_account)
        session.commit()

        return {"status": "success"}
    except Exception as e:
        session.rollback()
        raise
```

## Reference

Complete documentation: `/home/nsheff/workspaces/claude-web/DATABASE_GUIDE.md`
