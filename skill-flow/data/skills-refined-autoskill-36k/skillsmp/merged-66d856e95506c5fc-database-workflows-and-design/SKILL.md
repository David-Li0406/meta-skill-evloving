---
name: database-workflows-and-design
description: Use this skill when designing database schemas, planning migrations, optimizing queries, and managing data models across various database systems.
---

# Database Workflows and Design

This skill provides a comprehensive guide for designing efficient database schemas, planning migrations, optimizing queries, and managing data models across relational and document databases.

## Design Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE DESIGN PROCESS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. REQUIREMENTS      2. MODELING         3. SCHEMA             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │ Entities    │  →  │ ER diagram  │  →  │ Tables &    │       │
│  │ Attributes  │     │ Relations   │     │ Columns     │       │
│  │ Constraints │     │ Cardinality │     │ Constraints │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                                 │
│  4. INDEXES          5. MIGRATION        6. REVIEW              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │ Query       │  →  │ Safe changes│  →  │ Performance │       │
│  │ patterns    │     │ Rollback    │     │ Consistency │       │
│  │ Performance │     │ Zero-down   │     │ Integrity   │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Core Principles

### 1. Data Integrity First
Enforce constraints at the database level, not just application.

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
  status VARCHAR(20) NOT NULL DEFAULT 'pending'
);
```

### 2. Normalize by Default, Denormalize with Purpose
Start with 3NF. Denormalize only when performance needs are measured.

### 3. Explicit Over Implicit
Use clear naming and explicit constraints.

### 4. Plan for Evolution
Design schemas for safe migrations and future changes.

## Quick Reference for Database Workflows

| Task | Key Action |
|------|------------|
| Schema design | Normalize to 3NF, add indexes for queries |
| Migration review | Check reversibility, data preservation |
| Query optimization | Explain analyze, check indexes |
| N+1 prevention | Eager load relations, use joins |
| Index selection | Composite for multi-column WHERE |

## When to Use This Skill

- Designing new database schemas
- Reviewing migration files before running
- Optimizing slow queries
- Debugging N+1 query problems
- Adding or reviewing indexes
- Working with ORMs like Prisma, Drizzle, or TypeORM

## Schema Design Checklist

Before creating or modifying schemas:

- [ ] Tables have singular names (`user` not `users`)
- [ ] Primary keys are `id` (auto-increment or UUID)
- [ ] Foreign keys follow `{table}_id` pattern
- [ ] Timestamps include `created_at`, `updated_at`
- [ ] Nullable columns are intentional
- [ ] Indexes cover common query patterns
- [ ] No redundant data (normalized to 3NF minimum)

## Migration Workflow

### Before Creating Migrations

```bash
# Prisma
bunx prisma migrate dev --create-only --name descriptive_name

# Drizzle
bunx drizzle-kit generate:pg --name descriptive_name

# TypeORM
bunx typeorm migration:generate -n DescriptiveName
```

### Migration Review Checklist

- [ ] Migration is reversible (has down/rollback)
- [ ] No data loss on rollback
- [ ] Large tables use batched operations
- [ ] Indexes created CONCURRENTLY (if supported)
- [ ] Foreign key constraints don't lock tables
- [ ] Default values for new NOT NULL columns

## Query Optimization Quick Guide

### Identify Slow Queries

```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
```

### Analyze Queries

```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- MySQL
EXPLAIN ANALYZE SELECT ...;
```

### Common Optimizations

| Problem | Solution |
|---------|----------|
| Full table scan | Add index on WHERE columns |
| Filesort | Add index matching ORDER BY |
| Using temporary | Optimize GROUP BY, add composite index |
| Seq Scan on large table | Add covering index |

## N+1 Query Prevention

### Problem Pattern

```typescript
// BAD: N+1 queries
const users = await db.user.findMany();
for (const user of users) {
  const posts = await db.post.findMany({ where: { userId: user.id } });
}
```

### Solution Pattern

```typescript
// GOOD: Single query with relation
const users = await db.user.findMany({
  include: { posts: true }
});
```

## Index Design Checklist

```
□ Primary key (automatic)
□ Foreign keys (add manually in most DBs)
□ Unique constraints
□ Columns in WHERE clauses (high selectivity)
□ Columns in ORDER BY
□ Columns in JOIN conditions
□ Composite indexes for multi-column queries

⚠️ Avoid:
□ Indexing low-cardinality columns alone (status, boolean)
□ Over-indexing (slows writes)
□ Indexes that duplicate existing coverage
```

## ORM Integration

### Prisma

```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  orders    Order[]
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
}
```

### Drizzle

```typescript
export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
});
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No index on foreign key | Add index on FK columns |
| SELECT * in production | Select only needed columns |
| N+1 in loops | Use eager loading or joins |
| Missing timestamps | Add created_at, updated_at |
| Nullable by default | Explicitly define NOT NULL |
| No migration rollback | Always write down migration |

## References

- [Schema patterns](references/schema-patterns.md) — Common schema patterns (users, multi-tenant, polymorphic, etc.)
- [Migration strategies](references/migration-strategies.md) — Safe migration techniques, rollback procedures, zero-downtime patterns
- [Index design](references/index-design.md) — When and how to add indexes, query analysis
- [PostgreSQL features](references/postgresql.md) — PostgreSQL-specific features, extensions, optimization
- [Prisma patterns](references/prisma-patterns.md) — Prisma schema design, migrations, best practices
- [Query optimization](references/query-optimization.md) — Identifying and fixing slow queries, EXPLAIN analysis