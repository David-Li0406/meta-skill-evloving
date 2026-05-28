---
name: api-data-migration
description: Generate Drizzle migrations with composite indexes, multi-tenancy support (organization_id), and timestamp triggers. Use when creating tables, adding columns, or implementing tenant isolation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Data Migration

## Purpose

Generate Drizzle ORM migrations with proper schema definition, composite indexes for tenant queries, multi-tenancy support (organization_id), and timestamp triggers.

## When to Use

- Creating new database tables
- Adding columns to existing tables
- Creating indexes for performance
- Implementing tenant isolation at database level

## What It Generates

### Directory Structure

```
packages/db-main/drizzle/0001_{timestamp}_{name}.sql
packages/db-main/src/schemas/{entity}.ts
```

## Patterns Enforced

### organization_id Column

All tables MUST have `organization_id` as first column:

- Type: `uuid`
- Nullable: `false` (required)
- Indexed: Yes
- Used for tenant scoping

### Composite Indexes

For queries like `WHERE organization_id = ? AND status = ?`:

- Create index on `(organization_id, status)`
- Improves query performance for tenant-scoped queries
- Avoids N+1 queries

### Timestamps

All tables have:

- `created_at TIMESTAMP NOT NULL DEFAULT NOW()`
- `updated_at TIMESTAMP NOT NULL DEFAULT NOW()`
- Trigger to update `updated_at` on UPDATE

### Foreign Keys

- Foreign keys use `ON DELETE CASCADE` for cleanup
- References use `organization_id` in FK for tenant isolation

## Usage Example

```bash
/skill data-migration --name=add_products_table --schema='id:uuid,name:text,price:int,active:boolean' --domain=main
```

## Related Files

- [Data Repository](../data-repository/SKILL.md) - Repository for the table
- [Feature CQRS](../feature-cqrs/SKILL.md) - CQRS handlers using the table
