---
name: databases
description: PostgreSQL and MongoDB patterns - queries, indexing, performance optimization, migrations.
---

# Databases

> **Load this skill** when working with PostgreSQL or MongoDB.

## Database Selection

| Use PostgreSQL When | Use MongoDB When |
|---------------------|------------------|
| Complex relationships | Document-oriented data |
| ACID transactions needed | Flexible schema |
| Complex queries/joins | Horizontal scaling |
| Data integrity critical | Rapid prototyping |
| Reporting/analytics | Nested/hierarchical data |

---

## PostgreSQL

### Essential Queries

```sql
-- Create with returning
INSERT INTO users (email, name) 
VALUES ('test@example.com', 'Test')
RETURNING id, created_at;

-- Upsert (insert or update)
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Updated')
ON CONFLICT (email) 
DO UPDATE SET name = EXCLUDED.name, updated_at = NOW();

-- Pagination with cursor
SELECT * FROM posts
WHERE created_at < $1
ORDER BY created_at DESC
LIMIT 20;

-- Full-text search
SELECT * FROM articles
WHERE to_tsvector('english', title || ' ' || body) 
  @@ plainto_tsquery('english', $1);
```

### Indexing Strategy

```sql
-- B-tree (default) - equality and range
CREATE INDEX idx_users_email ON users(email);

-- Partial index - subset of rows
CREATE INDEX idx_active_users ON users(email) 
WHERE deleted_at IS NULL;

-- Composite index - multiple columns (order matters!)
CREATE INDEX idx_posts_user_date ON posts(user_id, created_at DESC);

-- GIN index - full-text search, JSONB
CREATE INDEX idx_posts_search ON posts 
USING GIN(to_tsvector('english', title || ' ' || body));

-- Covering index - include columns for index-only scans
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);
```

### Performance Analysis

```sql
-- Explain query plan
EXPLAIN ANALYZE 
SELECT * FROM users WHERE email = 'test@example.com';

-- Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Table statistics
SELECT schemaname, tablename, n_live_tup, n_dead_tup,
       last_vacuum, last_autovacuum
FROM pg_stat_user_tables;

-- Index usage
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public';
```

### Transactions

```sql
-- Explicit transaction
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- With savepoint for partial rollback
BEGIN;
  INSERT INTO orders (user_id, total) VALUES (1, 100);
  SAVEPOINT before_items;
  INSERT INTO order_items (order_id, product_id) VALUES (1, 999);
  -- If item insert fails, rollback just that part
  ROLLBACK TO before_items;
COMMIT;
```

---

## MongoDB

### Essential Operations

```javascript
// Insert with auto-generated ID
db.users.insertOne({
  email: "test@example.com",
  name: "Test",
  createdAt: new Date()
})

// Upsert
db.users.updateOne(
  { email: "test@example.com" },
  { $set: { name: "Updated" }, $setOnInsert: { createdAt: new Date() }},
  { upsert: true }
)

// Aggregation pipeline
db.orders.aggregate([
  { $match: { status: "completed" }},
  { $group: { _id: "$userId", total: { $sum: "$amount" }}},
  { $sort: { total: -1 }},
  { $limit: 10 }
])

// Pagination with cursor
db.posts.find({ createdAt: { $lt: lastSeenDate }})
  .sort({ createdAt: -1 })
  .limit(20)
```

### Indexing

```javascript
// Single field index
db.users.createIndex({ email: 1 }, { unique: true })

// Compound index (order matters!)
db.posts.createIndex({ userId: 1, createdAt: -1 })

// Text index for search
db.articles.createIndex({ title: "text", body: "text" })

// TTL index for auto-expiry
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 })

// Partial index
db.users.createIndex(
  { email: 1 },
  { partialFilterExpression: { deletedAt: null }}
)
```

### Performance Analysis

```javascript
// Explain query
db.users.find({ email: "test@example.com" }).explain("executionStats")

// Current operations
db.currentOp({ "active": true, "secs_running": { $gt: 5 }})

// Collection stats
db.users.stats()

// Index usage
db.users.aggregate([{ $indexStats: {} }])
```

---

## Common Patterns

### Soft Delete

```sql
-- PostgreSQL
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = $1;
```

```javascript
// MongoDB
db.users.updateOne({ _id: id }, { $set: { deletedAt: new Date() }})

// Query active users
db.users.find({ deletedAt: null })
```

### Pagination Comparison

| Method | Pros | Cons |
|--------|------|------|
| Offset/Limit | Simple, random access | Slow on large offsets |
| Cursor-based | Consistent, fast | No random access |
| Keyset | Very fast | Requires unique, sequential key |

```sql
-- Keyset pagination (recommended for large datasets)
SELECT * FROM posts
WHERE (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

### Optimistic Locking

```sql
-- PostgreSQL with version column
UPDATE products 
SET stock = stock - 1, version = version + 1
WHERE id = $1 AND version = $2;
-- Check rows affected; if 0, someone else updated
```

```javascript
// MongoDB with version field
db.products.updateOne(
  { _id: id, version: currentVersion },
  { $inc: { stock: -1, version: 1 }}
)
// Check modifiedCount; if 0, retry
```

---

## Migration Best Practices

1. **Always reversible** - Write down AND up migrations
2. **Small changes** - One logical change per migration
3. **Test on copy** - Never migrate production without testing
4. **Avoid locks** - Use concurrent index creation
5. **Backfill separately** - Don't hold transactions for data migration

```sql
-- Safe index creation (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Safe column addition
ALTER TABLE users ADD COLUMN phone TEXT; -- No default, nullable
-- Then backfill in batches
-- Then add NOT NULL if needed
```

---

## Quick Reference

### PostgreSQL

| Need | Command |
|------|---------|
| Connect | `psql -h host -U user -d database` |
| List tables | `\dt` |
| Describe table | `\d tablename` |
| List indexes | `\di` |
| Query plan | `EXPLAIN ANALYZE query` |

### MongoDB

| Need | Command |
|------|---------|
| Connect | `mongosh "mongodb://host/db"` |
| List collections | `show collections` |
| Collection stats | `db.collection.stats()` |
| Indexes | `db.collection.getIndexes()` |
| Query plan | `.explain("executionStats")` |
