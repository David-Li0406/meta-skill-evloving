---
name: postgres-schema-design
description: Use this skill when designing or modifying PostgreSQL schemas, including data types, constraints, indexing, and advanced features.
---

# PostgreSQL Schema Design

## When to use this skill
- Creating or modifying PostgreSQL tables (DDL).
- Working with JSONB, Arrays, or specialized Postgres types.
- Creating triggers or functions (PL/pgSQL).

## Core Rules

- Define a **PRIMARY KEY** for reference tables (users, orders, etc.). Prefer `BIGINT GENERATED ALWAYS AS IDENTITY`; use `UUID` only when global uniqueness is needed.
- **Normalize first (to 3NF)** to eliminate data redundancy; denormalize only for high-ROI reads where join performance is proven problematic.
- Add **NOT NULL** constraints where semantically required; use **DEFAULT**s for common values.
- Create **indexes for access paths you actually query**: PK/unique (auto), **FK columns (manual!)**, frequent filters/sorts, and join keys.

## Data Types

- **Timestamps**: Use `timestamptz` (Timestamp with Time Zone); avoid `timestamp` (without TZ).
- **Text**: Use `text` instead of `varchar(n)` unless a strict limit is architecturally required.
- **JSON**: Use `jsonb` for storage and indexing; avoid `json`.
- **Primary Keys**: Prefer `bigint GENERATED ALWAYS AS IDENTITY` or `uuid` (v4/v7).
- **Money**: Use `NUMERIC(p,s)`; avoid `money` type.
- **Booleans**: Use `BOOLEAN` with `NOT NULL` constraint unless tri-state values are required.
- **Arrays**: Use `TEXT[]`, `INTEGER[]`, etc. for ordered lists; index with **GIN** for containment queries.

## Constraints & Integrity

- **Check Constraints**: Use `CHECK` constraints generously (e.g., `CHECK (price > 0)`).
- **Foreign Keys**: Index all FK columns manually; PostgreSQL does not auto-index them.
- **Exclusion Constraints**: Use where `UNIQUE` is not enough (e.g., non-overlapping time ranges).

## Advanced Features

- **Triggers**: Use for audit logs or complex data consistency that cannot be enforced by constraints.
- **Partitions**: Consider declarative partitioning for massive time-series tables.
- **Enumerations**: Use Native Enums for strict, infrequently changing sets; otherwise, use a reference table.

## Indexing

- **B-tree**: Default for equality/range queries.
- **Partial**: For hot subsets (e.g., `WHERE status = 'active'`).
- **GIN**: For JSONB containment/existence, arrays, and full-text search.
- **GiST**: For ranges, geometry, and exclusion constraints.

## Partitioning

- Use for very large tables (>100M rows) where queries consistently filter on partition key.
- Prefer declarative partitioning or hypertables; do NOT use table inheritance.

## Special Considerations

### Update-Heavy Tables

- **Separate hot/cold columns** to minimize bloat.
- **Use `fillfactor=90`** to leave space for HOT updates.

### Insert-Heavy Workloads

- **Minimize indexes**; only create what you query.
- **Use `COPY` or multi-row `INSERT`** instead of single-row inserts.

### Safe Schema Evolution

- **Transactional DDL**: Most DDL operations can run in transactions and be rolled back.
- **Concurrent index creation**: `CREATE INDEX CONCURRENTLY` avoids blocking writes.

## Examples

### Users

```sql
CREATE TABLE users (
  user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX ON users (LOWER(email));
CREATE INDEX ON users (created_at);
```

### Orders

```sql
CREATE TABLE orders (
  order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(user_id),
  status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','PAID','CANCELED')),
  total NUMERIC(10,2) NOT NULL CHECK (total > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON orders (user_id);
CREATE INDEX ON orders (created_at);
```

### JSONB

```sql
CREATE TABLE profiles (
  user_id BIGINT PRIMARY KEY REFERENCES users(user_id),
  attrs JSONB NOT NULL DEFAULT '{}',
  theme TEXT GENERATED ALWAYS AS (attrs->>'theme') STORED
);
CREATE INDEX profiles_attrs_gin ON profiles USING GIN (attrs);
```