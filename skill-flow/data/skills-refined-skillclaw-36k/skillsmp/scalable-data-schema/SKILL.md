---
name: scalable-data-schema
description: |
  Design database schemas that scale from prototype to production. Use when planning data models,
  designing tables, optimizing queries, or migrating schemas. Covers normalization, indexing,
  partitioning, and evolution strategies for SQL and NoSQL databases.
---

# Scalable Data Schema Design

Design database schemas that grow with your application—from prototype to millions of users.

## When to Use

Use this skill when:
- Starting a new project and designing initial data models
- Existing schema is causing performance issues
- Planning to scale from thousands to millions of records
- Migrating between database systems
- Data model needs to evolve without breaking changes

---

## Core Principles

### 1. Start Simple, Plan for Complex

**Prototype Phase** (< 10K records):
- Optimize for development speed
- Denormalize for convenience
- Use simple indexes
- Single database instance

**Growth Phase** (10K - 1M records):
- Normalize to reduce redundancy
- Add strategic indexes
- Introduce read replicas
- Monitor query performance

**Scale Phase** (> 1M records):
- Partition large tables
- Shard by logical boundaries
- Add caching layers
- Consider polyglot persistence

### 2. Query Patterns Drive Schema

**Anti-pattern**: Design schema, then write queries
**Best practice**: Identify queries, then design schema

```
Workflow:
1. List top 10 most frequent queries
2. List top 5 most expensive queries
3. Design indexes to support both
4. Benchmark with realistic data volumes
```

### 3. Plan for Evolution

**Schema versioning strategy**:
- Additive changes only (new columns, new tables)
- Deprecate old fields instead of deleting
- Use database migration tools (Flyway, Liquibase, Alembic)
- Version your schema in git

---

## Design Patterns

### Pattern 1: Event Sourcing for Audit Trails

**Use when**: You need complete history of changes

```sql
-- Anti-pattern: Update in place
UPDATE users SET email = 'new@example.com' WHERE id = 123;
-- Lost: Previous email, who changed it, when

-- Better: Event log
CREATE TABLE user_events (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  event_type VARCHAR(50) NOT NULL,  -- 'email_changed', 'profile_updated'
  event_data JSONB NOT NULL,         -- {old: 'old@...', new: 'new@...'}
  created_at TIMESTAMPTZ DEFAULT NOW(),
  created_by BIGINT                  -- Who made the change
);

CREATE INDEX idx_user_events_user_id ON user_events(user_id);
CREATE INDEX idx_user_events_created_at ON user_events(created_at DESC);

-- Current state is derived from events
CREATE VIEW current_users AS
SELECT DISTINCT ON (user_id)
  user_id,
  event_data->>'email' as email,
  created_at as last_updated
FROM user_events
WHERE event_type = 'email_changed'
ORDER BY user_id, created_at DESC;
```

**Trade-offs**:
- ✓ Complete audit trail
- ✓ Time travel queries
- ✗ More storage
- ✗ Queries more complex

### Pattern 2: Soft Deletes for Recovery

**Use when**: Data is valuable or deletion is rare

```sql
-- Basic soft delete
CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2),
  deleted_at TIMESTAMPTZ,           -- NULL = active, NOT NULL = deleted
  deleted_by BIGINT                 -- Who deleted it
);

-- Index for active records only (partial index)
CREATE INDEX idx_products_active ON products(id) WHERE deleted_at IS NULL;

-- Queries
SELECT * FROM products WHERE deleted_at IS NULL;  -- Active only
SELECT * FROM products WHERE deleted_at IS NOT NULL;  -- Deleted only
```

**Trade-offs**:
- ✓ Easy recovery
- ✓ Audit compliance
- ✗ Every query needs `WHERE deleted_at IS NULL`
- ✗ Unique constraints more complex

### Pattern 3: Polymorphic Associations

**Use when**: Multiple entity types share a relationship

```sql
-- Anti-pattern: Nullable foreign keys
CREATE TABLE comments (
  id BIGSERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  post_id BIGINT,        -- Comment on post
  photo_id BIGINT,       -- OR comment on photo
  video_id BIGINT,       -- OR comment on video
  -- Only one should be set, but DB can't enforce this
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Better: Polymorphic with type
CREATE TABLE comments (
  id BIGSERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  commentable_type VARCHAR(50) NOT NULL,  -- 'Post', 'Photo', 'Video'
  commentable_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- Ensure only valid types
  CONSTRAINT valid_commentable_type
    CHECK (commentable_type IN ('Post', 'Photo', 'Video'))
);

CREATE INDEX idx_comments_commentable
  ON comments(commentable_type, commentable_id);

-- Query
SELECT * FROM comments
WHERE commentable_type = 'Post'
  AND commentable_id = 123;
```

**Trade-offs**:
- ✓ Flexible, extensible
- ✗ Can't use foreign key constraints
- ✗ Joins more complex

**When to avoid**: Use separate tables if types have very different fields.

### Pattern 4: Hierarchical Data (Adjacency List vs Nested Sets)

**Adjacency List** (simple, common):
```sql
CREATE TABLE categories (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  parent_id BIGINT REFERENCES categories(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_categories_parent ON categories(parent_id);

-- Get immediate children (fast)
SELECT * FROM categories WHERE parent_id = 5;

-- Get all descendants (requires recursive CTE - slower)
WITH RECURSIVE subcategories AS (
  SELECT * FROM categories WHERE id = 5
  UNION ALL
  SELECT c.* FROM categories c
  JOIN subcategories s ON c.parent_id = s.id
)
SELECT * FROM subcategories;
```

**Nested Sets** (fast reads, slow writes):
```sql
CREATE TABLE categories (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  lft INT NOT NULL,       -- Left boundary
  rgt INT NOT NULL,       -- Right boundary
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_categories_lft_rgt ON categories(lft, rgt);

-- Get all descendants (fast!)
SELECT * FROM categories
WHERE lft > 10 AND rgt < 20;

-- Get path to root (fast!)
SELECT * FROM categories c1
JOIN categories c2 ON c1.lft BETWEEN c2.lft AND c2.rgt
WHERE c1.id = 15
ORDER BY c2.lft;
```

**Choose**:
- Adjacency List: Frequent updates, shallow hierarchies
- Nested Sets: Mostly reads, deep hierarchies
- Materialized Path: Mix of both (store path as string: `/1/5/12/`)

### Pattern 5: Time-Series Data (Partitioning)

**Use when**: Data grows continuously over time

```sql
-- Basic time-series table
CREATE TABLE metrics (
  id BIGSERIAL,
  metric_name VARCHAR(100) NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL,
  tags JSONB,
  PRIMARY KEY (id, recorded_at)  -- Include partition key
) PARTITION BY RANGE (recorded_at);

-- Create partitions (monthly)
CREATE TABLE metrics_2026_01 PARTITION OF metrics
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE metrics_2026_02 PARTITION OF metrics
  FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

-- Index on each partition (automatically created on partition key)
CREATE INDEX idx_metrics_2026_01_name ON metrics_2026_01(metric_name);
CREATE INDEX idx_metrics_2026_02_name ON metrics_2026_02(metric_name);

-- Queries automatically use correct partition
SELECT AVG(value) FROM metrics
WHERE recorded_at BETWEEN '2026-01-15' AND '2026-01-20'
  AND metric_name = 'cpu_usage';
```

**Benefits**:
- ✓ Query only relevant partitions (partition pruning)
- ✓ Drop old partitions easily (instant delete)
- ✓ Parallel queries across partitions
- ✓ Manage storage per partition

---

## Indexing Strategy

### When to Index

**Index when**:
- Column used in WHERE clause frequently
- Column used in JOIN conditions
- Column used in ORDER BY
- Foreign keys (even if DB doesn't auto-create)

**Don't index when**:
- Table is small (< 1000 rows)
- Column has low cardinality (few distinct values)
- Column is updated frequently
- Index would be larger than table

### Index Types

**B-Tree** (default, most common):
```sql
CREATE INDEX idx_users_email ON users(email);
-- Use for: =, <, >, <=, >=, BETWEEN, IN, LIKE 'prefix%'
```

**Hash** (exact matches only):
```sql
CREATE INDEX idx_users_email ON users USING HASH(email);
-- Use for: = only (faster than B-Tree for equality)
```

**GIN** (Generalized Inverted Index - for arrays/JSONB):
```sql
CREATE INDEX idx_products_tags ON products USING GIN(tags);
-- Use for: JSONB @>, arrays && or @> operators
```

**Partial Index** (index subset of rows):
```sql
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;
-- Smaller, faster for common queries
```

**Composite Index** (multiple columns):
```sql
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
-- Order matters! Works for:
--   WHERE user_id = X
--   WHERE user_id = X ORDER BY created_at DESC
-- Doesn't help:
--   WHERE created_at = Y (user_id not in query)
```

### Index Maintenance

```sql
-- Find unused indexes (PostgreSQL)
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey';

-- Find duplicate indexes
SELECT tablename, array_agg(indexname)
FROM pg_indexes
GROUP BY tablename, indexdef
HAVING COUNT(*) > 1;

-- Rebuild bloated indexes
REINDEX INDEX CONCURRENTLY idx_users_email;
```

---

## Schema Evolution

### Additive-Only Migrations

**Safe (zero downtime)**:
```sql
-- Add new column with default
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Add new table
CREATE TABLE user_preferences (...);

-- Add new index concurrently (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_created ON users(created_at);
```

**Risky (requires downtime or careful planning)**:
```sql
-- Drop column (breaks old code)
ALTER TABLE users DROP COLUMN old_field;

-- Rename column (breaks old code)
ALTER TABLE users RENAME COLUMN old_name TO new_name;

-- Change column type (may lock table)
ALTER TABLE users ALTER COLUMN age TYPE BIGINT;
```

### Safe Migration Pattern

**3-Step Deploy**:

```sql
-- Step 1: Add new column (deploy, code ignores it)
ALTER TABLE users ADD COLUMN email_new VARCHAR(255);

-- Step 2: Backfill + dual write (deploy, code writes both)
UPDATE users SET email_new = email WHERE email_new IS NULL;
-- App code now writes to both email and email_new

-- Step 3: Switch over (deploy, code uses only email_new)
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_new TO email;
```

### Versioned Schema

```sql
-- Track migrations
CREATE TABLE schema_migrations (
  version VARCHAR(50) PRIMARY KEY,
  applied_at TIMESTAMPTZ DEFAULT NOW()
);

-- Example migration file: 20260121_add_user_phone.sql
BEGIN;

ALTER TABLE users ADD COLUMN phone VARCHAR(20);

INSERT INTO schema_migrations (version)
VALUES ('20260121_add_user_phone');

COMMIT;
```

---

## Database Selection Guide

### SQL (Relational)

**PostgreSQL**:
- ✓ Best for: Complex queries, ACID transactions, JSONB
- ✓ Advanced features: Full-text search, geospatial (PostGIS)
- Use when: You need strong consistency and rich query capabilities

**MySQL/MariaDB**:
- ✓ Best for: Read-heavy workloads, replication
- ✓ Widely supported, mature ecosystem
- Use when: You need simple replication or hosting constraints

**SQLite**:
- ✓ Best for: Embedded databases, single-user apps
- Use when: No separate DB server needed

### NoSQL

**MongoDB** (Document):
- ✓ Best for: Flexible schema, rapid iteration
- ✓ Schema-less (actually schema-on-read)
- Use when: Schema changes frequently, hierarchical data

**Redis** (Key-Value):
- ✓ Best for: Caching, sessions, pub/sub
- Use when: Ultra-fast reads, temporary data

**DynamoDB** (Key-Value):
- ✓ Best for: Serverless, predictable performance
- Use when: AWS ecosystem, pay-per-request pricing

**Cassandra** (Wide-Column):
- ✓ Best for: Time-series, write-heavy workloads
- Use when: Multi-datacenter, massive scale

### Decision Matrix

| Use Case | Database | Why |
|----------|----------|-----|
| User accounts, transactions | PostgreSQL | ACID, relations |
| Product catalog (e-commerce) | PostgreSQL | Complex queries, inventory |
| Session storage | Redis | Fast, ephemeral |
| Activity feed | Cassandra | Write-heavy, time-series |
| Analytics events | ClickHouse | Columnar, OLAP |
| Document storage | MongoDB | Flexible schema |
| Geospatial queries | PostgreSQL + PostGIS | Best geo support |

---

## Performance Optimization

### Query Analysis

```sql
-- Analyze query plan (PostgreSQL)
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2026-01-01'
GROUP BY u.id, u.name;

-- Look for:
-- "Seq Scan" on large tables → Add index
-- "Hash Join" instead of "Nested Loop" → May need different index
-- High "actual time" → Slow query
```

### Common Fixes

**Problem**: Slow JOIN on large tables
```sql
-- Before
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending';

-- Fix: Index foreign key
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
```

**Problem**: Slow COUNT(*) on large table
```sql
-- Before (scans entire table)
SELECT COUNT(*) FROM orders;

-- Fix: Use estimate for large tables
SELECT reltuples::BIGINT AS estimate
FROM pg_class
WHERE relname = 'orders';

-- Or: Maintain counter
CREATE TABLE table_stats (
  table_name VARCHAR(50) PRIMARY KEY,
  row_count BIGINT,
  updated_at TIMESTAMPTZ
);
```

**Problem**: N+1 queries
```sql
-- Before (1 query + N queries for each user)
users = query("SELECT * FROM users LIMIT 10")
for user in users:
    orders = query("SELECT * FROM orders WHERE user_id = ?", user.id)

-- Fix: Eager load with JOIN or IN
SELECT u.*, o.* FROM users u
LEFT JOIN orders o ON u.id = o.user_id
LIMIT 10;

-- Or use IN for large sets
user_ids = [1, 2, 3, ...]
SELECT * FROM orders WHERE user_id IN (?, ?, ?)
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| **ENUM in column type** | Hard to change | Lookup table with foreign key |
| **Storing arrays as strings** | Can't query efficiently | Array column or join table |
| **GUID/UUID as primary key** | Fragmented indexes, 16 bytes | BIGSERIAL (8 bytes, sequential) |
| **Premature optimization** | Complexity without benefit | Start simple, optimize when needed |
| **Missing foreign keys** | Data integrity issues | Always use FK constraints |
| **No created_at/updated_at** | Can't audit or debug | Add to all tables |
| **Over-normalization** | Too many JOINs | Denormalize for read patterns |
| **Under-normalization** | Data duplication, update anomalies | Normalize until 3NF, then denormalize strategically |

---

## Output Format

When helping with schema design:

```
## Schema Analysis

### Current Pain Points
- [Specific issue 1]
- [Specific issue 2]

### Recommended Schema

[SQL DDL for new tables/changes]

### Indexes

[Recommended indexes with rationale]

### Migration Strategy

[Step-by-step migration plan]

### Trade-offs
- ✓ Advantages
- ✗ Disadvantages

### Expected Performance Impact
- Reads: [faster/slower, by how much]
- Writes: [faster/slower, by how much]
- Storage: [increase/decrease]
```

---

## Integration

Works with:
- **database-schema** - Initial schema design
- **api-design** - Align schema with API needs
- **systems-decompose** - Feature-driven schema design
- **data-infrastructure-at-scale** - Infrastructure for scaled schemas
