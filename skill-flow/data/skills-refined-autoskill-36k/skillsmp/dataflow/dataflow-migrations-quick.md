---
name: dataflow-migrations-quick
description: "DataFlow automatic migrations and schema changes. Use when DataFlow migration, auto_migrate, schema changes, add column, or migration basics."
---

# DataFlow Migrations Quick Start

Automatic schema migrations with safety controls for development and production.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `HIGH`
> Related Skills: [`dataflow-models`](#), [`dataflow-existing-database`](#)
> Related Subagents: `dataflow-specialist` (complex migrations, production safety)

## Quick Reference

- **Development (CLI/scripts)**: `auto_migrate=True` (default) - safe, preserves data
- **Docker/FastAPI**: `auto_migrate=False` + `create_tables_async()` in lifespan - **REQUIRED**
- **Production**: `auto_migrate=False` + manual migrations
- **Enterprise**: Full migration system with risk assessment
- **Safety**: auto_migrate ALWAYS preserves existing data (but fails in Docker/FastAPI async contexts)

## Core Pattern

```python
from dataflow import DataFlow

# Development - automatic migrations
db_dev = DataFlow(
    database_url="sqlite:///dev.db",
    auto_migrate=True  # Default - safe for development
)

@db_dev.model
class User:
    name: str
    email: str

# Add field later - auto-migrates safely
@db_dev.model
class User:
    name: str
    email: str
    age: int = 0  # New field with default - safe migration
```

## Migration Modes

### Development Mode (auto_migrate=True)

```python
db = DataFlow(auto_migrate=True)

@db.model
class Product:
    name: str
    price: float

# Later: Add field - auto-migrates
@db.model
class Product:
    name: str
    price: float
    category: str = "general"  # New field added automatically
```

**Safety**: Verified - no data loss on repeat runs

### Production Mode (auto_migrate=False)

```python
db = DataFlow(
    auto_migrate=False,          # Manual control
    existing_schema_mode=True    # Maximum safety
)

# Schema changes require manual migration
```

### Enterprise Mode

```python
from dataflow.migrations.risk_assessment_engine import RiskAssessmentEngine
from dataflow.migrations.not_null_handler import NotNullColumnHandler

# Assess risk before changes
risk_engine = RiskAssessmentEngine(connection_manager)
assessment = await risk_engine.assess_operation_risk(
    operation_type="add_not_null_column",
    table_name="users",
    column_name="status"
)

# Execute with safety checks
handler = NotNullColumnHandler(connection_manager)
plan = await handler.plan_not_null_addition("users", column_def)
result = await handler.execute_not_null_addition(plan)
```

## Common Migrations

### Add Nullable Column

```python
@db.model
class User:
    name: str
    email: str
    phone: str = None  # Nullable - safe to add
```

### Add NOT NULL Column

```python
@db.model
class User:
    name: str
    email: str
    status: str = "active"  # Default required for NOT NULL
```

### Remove Column

```python
# Use Column Removal Manager
from dataflow.migrations.column_removal_manager import ColumnRemovalManager

remover = ColumnRemovalManager(connection_manager)
removal_plan = await remover.plan_column_removal("users", "old_field")
result = await remover.execute_column_removal(removal_plan)
```

## Common Mistakes

### Mistake 1: No Default for NOT NULL

```python
# WRONG - No default for required field
@db.model
class User:
    name: str
    email: str
    status: str  # No default - migration fails!
```

**Fix: Provide Default**

```python
@db.model
class User:
    name: str
    email: str
    status: str = "active"  # Default for existing rows
```

### Mistake 2: Production with auto_migrate=True

```python
# RISKY - Auto-migrations in production
db_prod = DataFlow(
    database_url="postgresql://prod/db",
    auto_migrate=True  # Don't use in production!
)
```

**Fix: Disable for Production**

```python
db_prod = DataFlow(
    database_url="postgresql://prod/db",
    auto_migrate=False,
    existing_schema_mode=True
)
```

## Related Patterns

- **For models**: See [`dataflow-models`](#)
- **For existing databases**: See [`dataflow-existing-database`](#)

## Documentation References

### Primary Sources
- **NOT NULL Handler**: [`sdk-users/apps/dataflow/docs/development/not-null-column-addition.md`](../../../../sdk-users/apps/dataflow/docs/development/not-null-column-addition.md)
- **Column Removal**: [`sdk-users/apps/dataflow/docs/development/column-removal-system.md`](../../../../sdk-users/apps/dataflow/docs/development/column-removal-system.md)
- **Auto Migration**: [`sdk-users/apps/dataflow/docs/workflows/auto-migration.md`](../../../../sdk-users/apps/dataflow/docs/workflows/auto-migration.md)

### Related Documentation
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md#L316-L360)
- **Migration Orchestration**: [`sdk-users/apps/dataflow/docs/workflows/migration-orchestration-engine.md`](../../../../sdk-users/apps/dataflow/docs/workflows/migration-orchestration-engine.md)

## Quick Tips

- auto_migrate=True safe for development CLI/scripts (preserves data)
- **⚠️ Docker/FastAPI**: Use `auto_migrate=False` + `create_tables_async()` in lifespan
- Always provide defaults for NOT NULL columns
- Use existing_schema_mode=True for production
- Enterprise system available for complex migrations
- Test migrations on staging before production

## Keywords for Auto-Trigger

<!-- Trigger Keywords: DataFlow migration, auto_migrate, schema changes, add column, migration basics, schema migration, database migration, alter table, migration safety -->
