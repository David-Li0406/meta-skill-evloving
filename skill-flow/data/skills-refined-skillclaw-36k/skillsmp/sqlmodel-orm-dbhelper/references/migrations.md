# Database Migrations with Alembic

Production migration patterns for SQLModel projects.

---

## Why Migrations?

| Method | Development | Production |
|--------|-------------|------------|
| `create_all()` | OK | **NOT SAFE** |
| Alembic migrations | OK | **Recommended** |

`create_all()` issues:
- Won't modify existing tables
- No rollback capability
- No migration history
- Can't handle data migrations

---

## Setup Alembic

### Installation

```bash
pip install alembic
```

### Initialize

```bash
alembic init alembic
```

Creates:
```
alembic/
├── env.py           # Migration environment
├── script.py.mako   # Migration template
├── versions/        # Migration files
alembic.ini          # Configuration
```

### Configure env.py

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import SQLModel metadata
from sqlmodel import SQLModel

# Import all models to register them
from app.models import User, Order, Item  # noqa

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use SQLModel metadata
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Configure alembic.ini

```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[alembic:exclude]
# Tables to exclude from autogenerate
tables = alembic_version

sqlalchemy.url = postgresql://user:password@localhost/dbname
# Or use environment variable:
# sqlalchemy.url = driver://%(DB_USER)s:%(DB_PASS)s@localhost/dbname
```

### Environment Variable Support

```python
# alembic/env.py - add at top
import os
from dotenv import load_dotenv

load_dotenv()

# In run_migrations_online():
def get_url():
    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    # ... rest of function
```

---

## Creating Migrations

### Auto-generate Migration

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Add user table"

# Creates: alembic/versions/xxxx_add_user_table.py
```

### Manual Migration

```bash
# Create empty migration
alembic revision -m "Add custom index"
```

### Migration File Structure

```python
"""Add user table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2024-01-15 10:30:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_user_email', 'user', ['email'])

def downgrade() -> None:
    op.drop_index('ix_user_email', table_name='user')
    op.drop_table('user')
```

---

## Running Migrations

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade a1b2c3d4e5f6

# Upgrade +1 step
alembic upgrade +1
```

### Rollback Migrations

```bash
# Downgrade -1 step
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade a1b2c3d4e5f6

# Downgrade to base (empty database)
alembic downgrade base
```

### Check Status

```bash
# Current revision
alembic current

# Migration history
alembic history

# Show pending migrations
alembic history --indicate-current
```

---

## Common Migration Operations

### Add Column

```python
def upgrade() -> None:
    op.add_column('user', sa.Column('phone', sa.String(20), nullable=True))

def downgrade() -> None:
    op.drop_column('user', 'phone')
```

### Add Non-Nullable Column (with data)

```python
def upgrade() -> None:
    # Add as nullable first
    op.add_column('user', sa.Column('status', sa.String(20), nullable=True))

    # Populate existing rows
    op.execute("UPDATE user SET status = 'active' WHERE status IS NULL")

    # Make non-nullable
    op.alter_column('user', 'status', nullable=False)

def downgrade() -> None:
    op.drop_column('user', 'status')
```

### Rename Column

```python
def upgrade() -> None:
    op.alter_column('user', 'name', new_column_name='full_name')

def downgrade() -> None:
    op.alter_column('user', 'full_name', new_column_name='name')
```

### Add Index

```python
def upgrade() -> None:
    op.create_index('ix_order_user_id', 'order', ['user_id'])

def downgrade() -> None:
    op.drop_index('ix_order_user_id', table_name='order')
```

### Add Foreign Key

```python
def upgrade() -> None:
    op.add_column('order', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'fk_order_user_id',
        'order', 'user',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    op.drop_constraint('fk_order_user_id', 'order', type_='foreignkey')
    op.drop_column('order', 'user_id')
```

### Create Table with Relationships

```python
def upgrade() -> None:
    op.create_table(
        'order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('total', sa.Numeric(10, 2), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_order_user_id', 'order', ['user_id'])
    op.create_index('ix_order_status', 'order', ['status'])
```

---

## Data Migrations

### Migrate Data Between Tables

```python
from sqlalchemy import text

def upgrade() -> None:
    # Create new table
    op.create_table('user_profile', ...)

    # Migrate data
    connection = op.get_bind()
    connection.execute(text("""
        INSERT INTO user_profile (user_id, bio)
        SELECT id, bio FROM user WHERE bio IS NOT NULL
    """))

    # Remove old column
    op.drop_column('user', 'bio')

def downgrade() -> None:
    op.add_column('user', sa.Column('bio', sa.Text()))

    connection = op.get_bind()
    connection.execute(text("""
        UPDATE user SET bio = (
            SELECT bio FROM user_profile WHERE user_profile.user_id = user.id
        )
    """))

    op.drop_table('user_profile')
```

### Batch Data Updates

```python
def upgrade() -> None:
    connection = op.get_bind()

    # Process in batches for large tables
    batch_size = 1000
    offset = 0

    while True:
        result = connection.execute(text(f"""
            UPDATE user
            SET email = LOWER(email)
            WHERE id IN (
                SELECT id FROM user
                WHERE email != LOWER(email)
                LIMIT {batch_size}
            )
        """))

        if result.rowcount == 0:
            break
```

---

## Best Practices

### Migration Naming

```bash
# Good: Descriptive
alembic revision --autogenerate -m "Add user email verification fields"
alembic revision --autogenerate -m "Create order items table"

# Bad: Vague
alembic revision --autogenerate -m "Update"
alembic revision --autogenerate -m "Changes"
```

### Always Test Downgrade

```bash
# Test migration cycle
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

### Review Auto-generated Migrations

Auto-generate may miss:
- Data migrations
- Index names you want custom
- Enum type changes
- Check constraints

Always review before applying!

### Production Deployment

```bash
# 1. Backup database
pg_dump -h host -U user dbname > backup.sql

# 2. Test migration on staging

# 3. Apply in maintenance window
alembic upgrade head

# 4. Verify
alembic current
```

---

## Troubleshooting

### "Target database is not up to date"

```bash
alembic stamp head  # Mark current state as latest
```

### Multiple Heads

```bash
# Check for branch
alembic heads

# Merge branches
alembic merge -m "Merge branches" rev1 rev2
```

### Failed Migration Recovery

```bash
# If migration partially applied:
# 1. Manually fix database state
# 2. Stamp to correct revision
alembic stamp <last_successful_revision>
```
