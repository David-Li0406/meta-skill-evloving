---
name: dataflow-multi-instance
description: "Multiple isolated DataFlow instances. Use when multiple DataFlow, dev and prod, string IDs, context isolation, or separate DataFlow instances."
---

# DataFlow Multi-Instance Setup

Run multiple isolated DataFlow instances (dev/prod) with proper context separation.

> **Skill Metadata**
> Category: `dataflow`
> Priority: `MEDIUM`
> Related Skills: [`dataflow-models`](#), [`dataflow-connection-config`](#)
> Related Subagents: `dataflow-specialist`

## Quick Reference

- **Context Isolation**: Each instance maintains separate models
- **String IDs**: Preserved per instance
- **Pattern**: Dev + prod instances with different configs

## Core Pattern

```python
from dataflow import DataFlow

# Development instance
db_dev = DataFlow(
    database_url="sqlite:///dev.db",
    auto_migrate=True,
    existing_schema_mode=False
)

# Production instance
db_prod = DataFlow(
    database_url="postgresql://user:pass@localhost/prod",
    auto_migrate=False,
    existing_schema_mode=True
)

# Models isolated per instance
@db_dev.model
class DevModel:
    id: str
    name: str
    # Only in db_dev

@db_prod.model
class ProdModel:
    id: str
    name: str
    # Only in db_prod

# Verify isolation
print(f"Dev models: {list(db_dev.models.keys())}")    # ['DevModel']
print(f"Prod models: {list(db_prod.models.keys())}")  # ['ProdModel']
```

## Common Use Cases

- **Multi-Environment**: Dev/staging/prod isolation
- **Multi-Tenant**: Separate database per tenant
- **Read/Write Split**: Separate read replica
- **Migration Testing**: Test database + production
- **Multi-Database**: Different databases in same app

## Common Mistakes

### Mistake 1: Not Using Instance-Specific Decorators

```python
# Wrong - attempting to share models between instances
db1 = DataFlow("sqlite:///db1.db")
db2 = DataFlow("postgresql://db2")

# Attempting to use a generic @model decorator
# This would cause ambiguity about which instance owns the model
```

**Fix: Use Instance-Specific Decorators**

```python
# Correct - proper isolation with instance-specific decorators
db1 = DataFlow("sqlite:///db1.db")
db2 = DataFlow("postgresql://db2")

@db1.model
class Model1:
    name: str
# Model1 only in db1 - properly isolated
```

## Documentation References

### Primary Sources
- **README Multi-Instance**: [`sdk-users/apps/dataflow/README.md`](../../../../sdk-users/apps/dataflow/README.md#L87-L116)
- **DataFlow CLAUDE**: [`sdk-users/apps/dataflow/CLAUDE.md`](../../../../sdk-users/apps/dataflow/CLAUDE.md#L86-L116)

### Specialist Reference
- **DataFlow Specialist**: [`.claude/skills/dataflow-specialist.md`](../../dataflow-specialist.md#L86-L116)

## Quick Tips

- Each instance maintains separate models
- Proper context isolation enforced
- String IDs preserved per instance
- Use different configs per environment

## Keywords for Auto-Trigger

<!-- Trigger Keywords: multiple DataFlow, dev and prod, string IDs, context isolation, separate instances, multi-instance DataFlow, multiple databases -->
