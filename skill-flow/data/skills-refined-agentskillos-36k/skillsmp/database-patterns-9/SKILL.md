---
name: database-patterns
description: "Schema design, migrations, queries, and indexing strategies. Use when designing database schemas, writing migrations, or optimizing queries."
---

# Database Patterns

## Overview

Decision guide for database design focusing on schema patterns, migrations, and query optimization.

## Schema Design Principles

### Naming Conventions

```sql
-- Tables: plural, snake_case
users, order_items, user_preferences

-- Columns: snake_case
created_at, user_id, is_active

-- Indexes: table_column(s)_idx
users_email_idx, orders_user_id_status_idx

-- Foreign keys: table_column_fkey
orders_user_id_fkey
```

### Essential Columns

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- business fields...
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at TIMESTAMPTZ  -- soft delete
);

-- Auto-update updated_at
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

## Relationship Patterns

### One-to-Many

```sql
-- Parent
CREATE TABLE users (
  id UUID PRIMARY KEY
);

-- Child (many side has FK)
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  -- Always index foreign keys
  CONSTRAINT posts_user_id_idx INDEX (user_id)
);
```

### Many-to-Many

```sql
-- Junction table
CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  assigned_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (user_id, role_id)
);
```

### Self-Referential

```sql
-- Hierarchical (e.g., categories, comments)
CREATE TABLE categories (
  id UUID PRIMARY KEY,
  parent_id UUID REFERENCES categories(id),
  name TEXT NOT NULL
);
```

## Indexing Strategy

### Index Decision Matrix

| Query Pattern | Index Type |
|--------------|------------|
| Exact match (`=`) | B-tree (default) |
| Range (`<`, `>`, `BETWEEN`) | B-tree |
| Text search (`LIKE 'prefix%'`) | B-tree |
| Full-text search | GIN with tsvector |
| JSON queries | GIN |
| Geospatial | GiST |

### Composite Index Order

```sql
-- Columns in WHERE/ORDER BY order, most selective first
CREATE INDEX orders_user_status_date_idx
  ON orders (user_id, status, created_at DESC);

-- Query this index supports:
SELECT * FROM orders
WHERE user_id = ? AND status = ?
ORDER BY created_at DESC;
```

### Partial Indexes

```sql
-- Only index active users (smaller, faster)
CREATE INDEX users_active_email_idx
  ON users (email)
  WHERE deleted_at IS NULL;
```

## Migration Patterns

### Safe Migration Sequence

```sql
-- 1. Add nullable column
ALTER TABLE users ADD COLUMN phone TEXT;

-- 2. Backfill data
UPDATE users SET phone = '' WHERE phone IS NULL;

-- 3. Add constraint
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

### Rename Column (Zero Downtime)

```sql
-- 1. Add new column
ALTER TABLE users ADD COLUMN full_name TEXT;

-- 2. Dual-write in application code

-- 3. Backfill
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- 4. Switch reads to new column

-- 5. Stop writing to old column

-- 6. Drop old column
ALTER TABLE users DROP COLUMN name;
```

## Query Optimization

### N+1 Prevention

```typescript
// BAD: N+1 queries
const users = await db.user.findMany();
for (const user of users) {
  user.posts = await db.post.findMany({ where: { userId: user.id } });
}

// GOOD: Eager loading
const users = await db.user.findMany({
  include: { posts: true },
});

// GOOD: Explicit join
const users = await db.user.findMany({
  include: { posts: { select: { id: true, title: true } } },
});
```

### Batch Operations

```typescript
// BAD: Individual inserts
for (const item of items) {
  await db.item.create({ data: item });
}

// GOOD: Batch insert
await db.item.createMany({ data: items });

// GOOD: Transaction for related operations
await db.$transaction([
  db.order.create({ data: order }),
  db.inventory.update({ where: { id }, data: { quantity: { decrement: 1 } } }),
]);
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No FK indexes | Slow joins | Index all foreign keys |
| SELECT * | Over-fetching | Select specific columns |
| Missing NOT NULL | Data integrity | Default to NOT NULL |
| String IDs | Slow comparisons | Use UUID or BIGINT |
| No soft delete | Data loss | Add deleted_at |
| Over-normalization | Complex queries | Denormalize when needed |

## Red Flags

- Foreign keys without indexes
- Tables without primary key
- Missing created_at/updated_at
- No cascading rules on FKs
- Queries without LIMIT on large tables
- LIKE '%search%' on unindexed columns

## Quick Reference

```sql
-- Check index usage
SELECT indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Find missing indexes (slow queries)
SELECT query, calls, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Table size
SELECT pg_size_pretty(pg_total_relation_size('table_name'));
```

```typescript
// Prisma transaction
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  await tx.profile.create({ data: { userId: user.id } });
  return user;
});

// Drizzle batch
await db.batch([
  db.insert(users).values(userData),
  db.insert(profiles).values(profileData),
]);
```
