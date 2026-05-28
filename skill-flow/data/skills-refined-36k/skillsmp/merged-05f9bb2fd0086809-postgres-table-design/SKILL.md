---
name: postgres-table-design
description: Use this skill when designing PostgreSQL tables, focusing on data types, indexing, constraints, performance patterns, and advanced features.
---

# PostgreSQL Table Design

## Core Rules

- Define a **PRIMARY KEY** for reference tables (e.g., users, orders). Prefer `BIGINT GENERATED ALWAYS AS IDENTITY`; use `UUID` only when global uniqueness is needed.
- **Normalize first (to 3NF)** to eliminate data redundancy; denormalize only for high-ROI reads where join performance is problematic.
- Add **NOT NULL** constraints where required; use **DEFAULT** values for common entries.
- Create **indexes for access paths you query**: PK/unique (auto), **FK columns (manual!)**, frequent filters/sorts, and join keys.
- Prefer **TIMESTAMPTZ** for event time; **NUMERIC** for money; **TEXT** for strings; **BIGINT** for integers; **DOUBLE PRECISION** for floats.

## PostgreSQL “Gotchas”

- **Identifiers**: unquoted → lowercased. Use `snake_case` for table/column names.
- **Unique + NULLs**: UNIQUE allows multiple NULLs. Use `UNIQUE (...) NULLS NOT DISTINCT` (PG15+) to restrict to one NULL.
- **FK indexes**: PostgreSQL does not auto-index FK columns; add them manually.
- **No silent coercions**: length/precision overflows error out.
- **Sequences/identity have gaps**; this is expected behavior.
- **Heap storage**: no clustered PK by default; `CLUSTER` is a one-off reorganization.
- **MVCC**: updates/deletes leave dead tuples; vacuum handles them.

## Data Types

- **IDs**: Prefer `BIGINT GENERATED ALWAYS AS IDENTITY`; use `UUID` for distributed systems.
- **Integers**: Prefer `BIGINT` unless space is critical; use `INTEGER` for smaller ranges.
- **Floats**: Prefer `DOUBLE PRECISION`; use `NUMERIC` for exact decimal arithmetic.
- **Strings**: Prefer `TEXT`; use `CHECK (LENGTH(col) <= n)` for length limits.
- **Money**: Use `NUMERIC(p,s)`; avoid float types.
- **Time**: Use `TIMESTAMPTZ` for timestamps; `DATE` for date-only; `INTERVAL` for durations.
- **Booleans**: Use `BOOLEAN` with `NOT NULL` unless tri-state values are required.
- **Enums**: Use `CREATE TYPE ... AS ENUM` for small, stable sets; use TEXT for evolving values.
- **Arrays**: Use `TEXT[]`, `INTEGER[]`, etc., for ordered lists; index with **GIN**.
- **Range types**: Use `daterange`, `numrange`, `tstzrange` for intervals.
- **Network types**: Use `INET` for IP addresses, `CIDR` for network ranges.
- **Geometric types**: Avoid built-in types; consider **PostGIS** for spatial features.
- **Text search**: Use `TSVECTOR` for full-text search; index with **GIN**.
- **Domain types**: Use `CREATE DOMAIN` for reusable custom types with validation.
- **Composite types**: Use `CREATE TYPE` for structured data within columns.
- **JSONB**: Prefer over JSON; index with **GIN**.
- **Vector types**: Use `vector` type by `pgvector` for similarity search.

### Do not use the following data types

- DO NOT use `timestamp` (without time zone); DO use `timestamptz`.
- DO NOT use `char(n)` or `varchar(n)`; DO use `text`.
- DO NOT use `money` type; DO use `numeric`.
- DO NOT use `timetz` type; DO use `timestamptz`.
- DO NOT use `serial` type; DO use `generated always as identity`.
- DO NOT use built-in geometric types; DO use `geometry` from PostGIS.

## Table Types

- **Regular**: default; fully durable, logged.
- **TEMPORARY**: session-scoped, auto-dropped, not logged.
- **UNLOGGED**: persistent but not crash-safe; faster writes.

## Row-Level Security

Enable with `ALTER TABLE tbl ENABLE ROW LEVEL SECURITY`. Create policies for user-based access control.

## Constraints

- **PK**: implicit UNIQUE + NOT NULL; creates a B-tree index.
- **FK**: specify `ON DELETE/UPDATE` actions; add explicit index on referencing column.
- **UNIQUE**: creates a B-tree index; allows multiple NULLs unless `NULLS NOT DISTINCT`.
- **CHECK**: row-local constraints; NULL values pass the check.
- **EXCLUDE**: prevents overlapping values using operators.

## Indexing

- **B-tree**: default for equality/range queries.
- **Composite**: order matters; index used if equality on leftmost prefix.
- **Covering**: includes non-key columns for index-only scans.
- **Partial**: for hot subsets.
- **Expression**: for computed search keys.
- **GIN**: for JSONB containment/existence, arrays, full-text search.
- **GiST**: for ranges, geometry, exclusion constraints.
- **BRIN**: for very large, naturally ordered data.

## Partitioning

- Use for very large tables where queries filter on partition key.
- **RANGE**: common for time-series.
- **LIST**: for discrete values.
- **HASH**: for even distribution.
- Prefer declarative partitioning or hypertables.

## Special Considerations

### Update-Heavy Tables

- **Separate hot/cold columns** to minimize bloat.
- **Use `fillfactor=90`** for HOT updates.
- **Avoid updating indexed columns**.

### Insert-Heavy Workloads

- **Minimize indexes**; use `COPY` or multi-row `INSERT`.
- **UNLOGGED tables** for staging data.
- **Defer index creation** for bulk loads.

### Upsert-Friendly Design

- **Requires UNIQUE index** on conflict target columns.
- **Use `EXCLUDED.column`** to reference would-be-inserted values.

### Safe Schema Evolution

- **Transactional DDL**: most DDL operations can run in transactions.
- **Concurrent index creation**: avoids blocking writes.
- **Volatile defaults cause rewrites**.

## Generated Columns

- Use `... GENERATED ALWAYS AS (<expr>) STORED` for computed fields.

## Extensions

- **`pgcrypto`**: for password hashing.
- **`uuid-ossp`**: alternative UUID functions.
- **`pg_trgm`**: fuzzy text search.
- **`citext`**: case-insensitive text type.
- **`timescaledb`**: for time-series automation.
- **`postgis`**: for geospatial support.
- **`pgvector`**: for vector similarity search.

## JSONB Guidance

- Prefer `JSONB` with **GIN** index.
- Use constraints to limit allowed JSONB values.

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