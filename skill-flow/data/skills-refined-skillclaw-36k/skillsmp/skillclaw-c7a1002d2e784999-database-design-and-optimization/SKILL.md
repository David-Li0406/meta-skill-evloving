---
name: database-design-and-optimization
description: Use this skill when designing and optimizing database schemas, writing queries, managing migrations, and improving performance across SQL and NoSQL databases.
---

# Database Design and Optimization

## When to Use

- Designing new database schemas for applications.
- Refactoring existing schemas for performance or scalability.
- Defining relationships between tables (1:1, 1:N, N:M).
- Managing database migrations safely.
- Optimizing query performance and indexing strategies.

## Schema Design Principles

### Normalization Guidelines
```sql
-- 1NF: Atomic values, no repeating groups
-- 2NF: No partial dependencies on composite keys
-- 3NF: No transitive dependencies

-- Users table (normalized)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Addresses table (separate entity)
CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  street VARCHAR(255),
  city VARCHAR(100),
  country VARCHAR(100),
  is_primary BOOLEAN DEFAULT false
);
```

### Denormalization for Performance
```sql
-- When read performance matters more than write consistency
CREATE TABLE order_summaries (
  id SERIAL PRIMARY KEY,
  order_id INTEGER REFERENCES orders(id),
  customer_name VARCHAR(255),  -- Denormalized from customers
  total_amount DECIMAL(10,2),
  item_count INTEGER,
  last_updated TIMESTAMPTZ DEFAULT NOW()
);
```

## Index Design

### Common Index Patterns
```sql
-- B-tree (default) for equality and range queries
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- Partial index for specific conditions
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;

-- GIN index for array/JSONB columns
CREATE INDEX idx_posts_tags ON posts USING GIN(tags);

-- Covering index (includes additional columns)
CREATE INDEX idx_orders_covering ON orders(user_id) INCLUDE (total, status);
```

### Index Analysis
```sql
-- Check index usage
SELECT
  schemaname, tablename, indexname,
  idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find missing indexes
SELECT
  relname, seq_scan, seq_tup_read,
  idx_scan, idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_tup_read DESC;
```

## Migration Patterns

### Safe Migration Template
```sql
-- Always use transactions
BEGIN;

-- Add column with default (non-blocking in PG 11+)
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';

-- Create index concurrently (doesn't lock table)
CREATE INDEX CONCURRENTLY idx_users_status ON users(status);
COMMIT;
```

## Query Optimization

### Analyze Queries
```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123;

-- MySQL
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;
```

### Common Optimizations
```sql
-- Add missing index
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);

-- Composite index for common queries
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
```

## Maintenance and Health Checks
```sql
-- Active connections (PostgreSQL)
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state;

-- Long running queries
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > '5 minutes'::interval;
```