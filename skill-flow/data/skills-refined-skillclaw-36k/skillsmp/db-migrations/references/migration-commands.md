# Migration Commands Reference

Quick reference for Alembic migration commands in the Vibe4Vets backend.

## Setup

```bash
cd backend

# Ensure environment is ready
source .venv/bin/activate

# For PostgreSQL (recommended)
export DATABASE_URL="postgresql://user:pass@localhost:5432/vibe4vets"
```

## Primary Commands

### View Status

```bash
# Show current migration revision
alembic current

# Show migration history
alembic history --verbose

# Show pending migrations
alembic heads
```

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one step
alembic upgrade +1

# Upgrade to specific revision
alembic upgrade abc123
```

### Rollback Migrations

```bash
# Downgrade one step
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade abc123

# Downgrade all (dangerous!)
alembic downgrade base
```

### Create Migrations

```bash
# Auto-generate from model changes (recommended)
alembic revision --autogenerate -m "add phone column to resource"

# Create empty migration for manual changes
alembic revision -m "custom data migration"
```

### Utility Commands

```bash
# Show SQL without executing
alembic upgrade head --sql

# Mark database at revision without running migration
alembic stamp head

# Merge multiple heads
alembic merge -m "merge branches" head1 head2
```

## Common Workflows

### Adding/Modifying Columns

```bash
# 1. Modify SQLModel models in app/models/

# 2. Generate migration
alembic revision --autogenerate -m "add field to resource"

# 3. Review generated migration in alembic/versions/

# 4. Apply migration
alembic upgrade head
```

### Testing Migrations Locally

```bash
# Full cycle test
alembic upgrade head
alembic downgrade -1
alembic upgrade head
```

### Iterating on Recent Migration

```bash
# Downgrade
alembic downgrade -1

# Edit the migration file

# Re-apply
alembic upgrade head
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `ALEMBIC_CONFIG` | Path to alembic.ini (optional) |
