---
name: fastapi-alembic-setup
description: Use this skill when you need to configure Alembic for async SQLAlchemy migrations with PostgreSQL.
---

# FastAPI Alembic Setup

## Overview

This skill covers setting up Alembic for database migrations with async SQLAlchemy 2.0 and PostgreSQL.

## Initialize Alembic

```bash
# Initialize Alembic in the project root
uv run alembic init alembic
```

## Create alembic.ini

Create or update `alembic.ini` in the project root:

```ini
# Alembic Configuration

[alembic]
# Path to migration scripts
script_location = alembic

# Template used to generate migration files
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d%%(second).2d_%%(slug)s

# Set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# Truncate table name in version files
truncate_slug_length = 40

# Set to 'true' to allow .pyc and .pyo files without
# having their source .py files alongside them
# prepend_sys_path = .

# Timezone for file generation
timezone = UTC

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

## Create alembic/env.py

Replace `alembic/env.py` with the following code:

```python
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.config import settings
from app.core.models import Base

# Import all models here to ensure they're registered with Base.metadata
# This is crucial for autogenerate to detect all tables
# from app.items.models import Item
# from app.users.models import User

# Alembic Config object
config = context.config

# Set the database URL from settings
config.set_main_option("sqlalchemy.url", str(settings.database_url))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    # Implementation for running migrations offline
```