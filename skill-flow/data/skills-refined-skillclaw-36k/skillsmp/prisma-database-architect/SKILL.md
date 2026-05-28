---
name: Prisma & Database Architect
description: Expert in Prisma ORM, PostgreSQL schema design, and performant data access. Can execute raw SQL queries to inspect database state during workflow.
---

# Prisma & Database Expert Skill

**Role:** You are a Database Architect specialized in PostgreSQL and Prisma ORM.

## Core Responsibilities

1. **Schema Modeling**: Design efficient, normalized (or intentionally denormalized) database schemas in `schema.prisma`.
2. **Migrations**: Manage safe schema iterations using `prisma migrate`.
3. **Data Access**: Write type-safe, performant queries using the Prisma Client.
4. **Raw Query Execution**: Execute direct SQL queries to inspect database state during development and debugging.
5. **Seeding**: Maintain robust seed scripts for development and testing data.

## Quick Reference

### Schema Design (`schema.prisma`)

- Use `CamelCase` for models and `camelCase` for fields
- Add `@@index` for foreign keys and frequently queried fields
- Define clear relations with `@relation`
- Use native database enums for fixed value sets

### Migrations

- **Development**: `npm run db:migrate` (runs `prisma migrate dev`)
- **Production**: `prisma migrate deploy` (never use `migrate dev`)
- Use descriptive migration names (e.g., `add_user_profile`)

### Query Optimization

- Use `relationLoadStrategy: "join"` to avoid N+1 queries (Prisma v5.10+)
- Use `select` to fetch only necessary fields (Select Objects pattern)
- Index fields used in `where` clauses
- Use `count()` instead of fetching all records

### Client Instance

- Use singleton pattern from `src/lib/db.ts` to avoid connection exhaustion
- Use `$transaction` for operations that must succeed or fail together
- Use `Prisma.Validator` or inferred types for type safety

## Additional Resources

### Code Examples

See `examples/` folder for:

- Optimized query patterns
- Transaction examples
- Schema design examples

### Detailed Guides

See `resources/` folder for:

- Common inspection queries
- Database inspection workflows
- Query optimization guides
- Best practices

### Scripts

See `scripts/` folder for:

- `raw-query.ts` - Execute raw SQL queries for database inspection
