# Comprehensive Alembic Migrations Guide

## Table of Contents
1. Alembic Setup and Configuration
2. Creating Migrations
3. Schema Changes Patterns
4. Data Migrations
5. Migration Best Practices
6. Running Migrations
7. Production Workflow
8. Troubleshooting

---

## 1. Alembic Setup and Configuration

### Initial Setup

```bash
# Install Alembic
pip install alembic

# Initialize Alembic in your project
alembic init alembic

# This creates:
# alembic/
# ├── env.py          # Migration environment
# ├── script.py.mako  # Migration template
# └── versions/       # Migration files
# alembic.ini         # Alembic configuration
```

### Configure alembic.ini

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .

# Database URL (use environment variable in production)
sqlalchemy.url = postgresql://user:password@localhost/dbname

file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
```

### Configure env.py for SQLModel

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# Import your SQLModel models
from app.models import SQLModel
from app.database import get_database_url

config = context.config
config.set_main_option("sqlalchemy.url", get_database_url())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate'
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

---

## 2. Creating Migrations

### Autogenerate Migration (Recommended)

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Add user table"
```

### Manual Migration

```bash
# Create empty migration file
alembic revision -m "custom migration"
```

---

## 3. Schema Changes Patterns

### Adding a Column

```python
def upgrade() -> None:
    op.add_column('user', sa.Column('phone', sa.String(20), nullable=True))

def downgrade() -> None:
    op.drop_column('user', 'phone')
```

### Adding Non-Nullable Column with Default

```python
def upgrade() -> None:
    # Step 1: Add as nullable
    op.add_column('user', sa.Column('role', sa.String(50), nullable=True))
    # Step 2: Set default for existing rows
    op.execute("UPDATE user SET role = 'user' WHERE role IS NULL")
    # Step 3: Make non-nullable
    op.alter_column('user', 'role', nullable=False)

def downgrade() -> None:
    op.drop_column('user', 'role')
```

### Renaming a Column

```python
def upgrade() -> None:
    op.alter_column('user', 'name', new_column_name='full_name')

def downgrade() -> None:
    op.alter_column('user', 'full_name', new_column_name='name')
```

### Changing Column Type

```python
def upgrade() -> None:
    # PostgreSQL
    op.alter_column('user', 'age', type_=sa.String(3), postgresql_using='age::text')

def downgrade() -> None:
    op.alter_column('user', 'age', type_=sa.Integer())
```

### Adding Foreign Key

```python
def upgrade() -> None:
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_post_user_id', 'post', 'user',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    op.drop_constraint('fk_post_user_id', 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
```

### Adding Index

```python
def upgrade() -> None:
    op.create_index('idx_user_email_username', 'user', ['email', 'username'])

def downgrade() -> None:
    op.drop_index('idx_user_email_username', table_name='user')
```

### Creating a New Table

```python
def upgrade() -> None:
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_user_id', 'task', ['user_id'])

def downgrade() -> None:
    op.drop_index('idx_task_user_id', table_name='task')
    op.drop_table('task')
```

---

## 4. Data Migrations

### Simple Data Update

```python
from sqlalchemy import text

def upgrade() -> None:
    op.execute(text("UPDATE user SET is_active = true WHERE is_active IS NULL"))

def downgrade() -> None:
    op.execute(text("UPDATE user SET is_active = NULL WHERE is_active = true"))
```

### Complex Data Migration

```python
from sqlalchemy.orm import Session

def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    # Perform complex data manipulation
    users = session.execute(text("SELECT id, username FROM user")).fetchall()
    for user in users:
        session.execute(
            text("INSERT INTO welcome_task (user_id, title) VALUES (:uid, :title)"),
            {"uid": user.id, "title": f"Welcome {user.username}!"}
        )
    session.commit()
```

### Batch Operations for Large Tables

```python
def upgrade() -> None:
    batch_size = 1000
    offset = 0

    while True:
        result = op.execute(text(f"""
            UPDATE user SET email_verified = false
            WHERE email_verified IS NULL
            AND id IN (
                SELECT id FROM user WHERE email_verified IS NULL
                ORDER BY id LIMIT {batch_size} OFFSET {offset}
            )
        """))
        if result.rowcount == 0:
            break
        offset += batch_size
```

---

## 5. Migration Best Practices

### 1. Always Review Autogenerated Migrations

Autogenerate is helpful but not perfect. Always review before applying.

### 2. Use Descriptive Migration Names

```bash
# Good
alembic revision --autogenerate -m "add_user_email_verification_fields"

# Bad
alembic revision --autogenerate -m "update"
```

### 3. One Logical Change Per Migration

Keep migrations focused and atomic.

### 4. Test Migrations Both Ways

```bash
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

### 5. Never Edit Applied Migrations

Create a new migration to fix issues instead.

---

## 6. Running Migrations

### Basic Commands

```bash
# Show current revision
alembic current

# Show migration history
alembic history --verbose

# Upgrade to latest
alembic upgrade head

# Upgrade one step
alembic upgrade +1

# Downgrade one step
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade abc123

# Show SQL without executing
alembic upgrade head --sql

# Stamp database at revision (mark as applied without running)
alembic stamp head
```

---

## 7. Production Workflow

### Pre-Deployment Checklist

```bash
# 1. Test locally
alembic upgrade head
alembic downgrade base
alembic upgrade head

# 2. Review migration files
# 3. Backup production database
pg_dump mydb > backup_$(date +%Y%m%d_%H%M%S).sql

# 4. Test on staging
# 5. Monitor for issues
```

### Zero-Downtime Migration Strategy

```python
# Phase 1: Add new column (nullable)
def upgrade():
    op.add_column('user', sa.Column('new_email', sa.String(), nullable=True))

# Deploy app that writes to both columns

# Phase 2: Backfill data
def upgrade():
    op.execute("UPDATE user SET new_email = email WHERE new_email IS NULL")

# Phase 3: Make non-nullable
def upgrade():
    op.alter_column('user', 'new_email', nullable=False)

# Deploy app that reads from new column

# Phase 4: Drop old column
def upgrade():
    op.drop_column('user', 'email')
```

---

## 8. Troubleshooting

### Alembic Can't Detect Changes

```python
# Ensure all models are imported in env.py
from app.models import User, Task, Team
target_metadata = SQLModel.metadata
```

### Migration Conflicts

```bash
# Multiple heads
alembic heads

# Merge branches
alembic merge -m "merge branches" head1 head2
```

### Failed Migration

```bash
# Check current state
alembic current

# Option 1: Fix and stamp
alembic stamp head

# Option 2: Downgrade and retry
alembic downgrade -1
alembic upgrade head
```

### SQLite Limitations

```python
# Use batch operations for SQLite
def upgrade() -> None:
    with op.batch_alter_table('user') as batch_op:
        batch_op.add_column(sa.Column('new_field', sa.String()))
```
