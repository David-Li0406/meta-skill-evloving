# Query Optimization

Detailed patterns for query optimization, N+1 prevention, and database performance.

## Query Analysis Tools

### PostgreSQL

```sql
-- Enable query statistics
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slowest queries
SELECT
  query,
  calls,
  round(mean_exec_time::numeric, 2) as avg_ms,
  round(total_exec_time::numeric, 2) as total_ms,
  rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Find most frequently called
SELECT query, calls, rows
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 20;

-- Reset statistics
SELECT pg_stat_statements_reset();
```

### MySQL

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- seconds
SET GLOBAL log_queries_not_using_indexes = 'ON';

-- Find slow queries (Performance Schema)
SELECT
  DIGEST_TEXT,
  COUNT_STAR as calls,
  AVG_TIMER_WAIT/1000000000 as avg_ms,
  SUM_TIMER_WAIT/1000000000 as total_ms
FROM performance_schema.events_statements_summary_by_digest
ORDER BY AVG_TIMER_WAIT DESC
LIMIT 20;
```

## EXPLAIN Analysis

### PostgreSQL EXPLAIN

```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- With execution stats (actually runs the query)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'test@example.com';

-- JSON format for programmatic analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE email = 'test@example.com';
```

### Reading EXPLAIN Output

```
Seq Scan on users  (cost=0.00..155.00 rows=5000 width=64)
                    └─ estimated cost  └─ rows  └─ row size

Index Scan using idx_users_email on users (cost=0.29..8.31 rows=1 width=64)
          └─ using index                   └─ much lower cost!
```

### Key Indicators

| Indicator | Problem | Solution |
|-----------|---------|----------|
| `Seq Scan` on large table | Missing index | Add index |
| `Sort` with high cost | No index for ORDER BY | Add sorted index |
| `Hash Join` with large dataset | Missing index on join column | Add index |
| `Nested Loop` with high rows | N+1 pattern | Use JOIN or subquery |
| `Bitmap Heap Scan` | Good! Using index efficiently | - |
| `Index Only Scan` | Excellent! All data from index | - |

### MySQL EXPLAIN

```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Analyze format (MySQL 8.0+)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

## N+1 Query Prevention

### Identifying N+1

```typescript
// BAD: N+1 queries
const users = await db.user.findMany();  // Query 1
for (const user of users) {
  const posts = await db.post.findMany({  // N queries
    where: { userId: user.id }
  });
  console.log(user.name, posts.length);
}
// Total: 1 + N queries
```

### Solution 1: Eager Loading

```typescript
// Prisma
const users = await db.user.findMany({
  include: { posts: true }
});

// Drizzle
const users = await db.query.users.findMany({
  with: { posts: true }
});

// TypeORM
const users = await userRepo.find({
  relations: ['posts']
});
```

### Solution 2: Explicit Joins

```typescript
// Drizzle
const result = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.userId));

// TypeORM QueryBuilder
const result = await userRepo
  .createQueryBuilder('user')
  .leftJoinAndSelect('user.posts', 'post')
  .getMany();
```

### Solution 3: Batch Loading

```typescript
// Collect all IDs first
const users = await db.user.findMany();
const userIds = users.map(u => u.id);

// Single query for all related data
const posts = await db.post.findMany({
  where: { userId: { in: userIds } }
});

// Map posts to users in memory
const postsByUser = new Map<number, Post[]>();
for (const post of posts) {
  const userPosts = postsByUser.get(post.userId) || [];
  userPosts.push(post);
  postsByUser.set(post.userId, userPosts);
}
```

### DataLoader Pattern

```typescript
import DataLoader from 'dataloader';

const postLoader = new DataLoader(async (userIds: number[]) => {
  const posts = await db.post.findMany({
    where: { userId: { in: userIds } }
  });

  const postsByUser = new Map<number, Post[]>();
  for (const post of posts) {
    const userPosts = postsByUser.get(post.userId) || [];
    userPosts.push(post);
    postsByUser.set(post.userId, userPosts);
  }

  return userIds.map(id => postsByUser.get(id) || []);
});

// Usage - automatically batches requests
for (const user of users) {
  const posts = await postLoader.load(user.id);  // Batched!
}
```

## Query Optimization Patterns

### Select Only Needed Columns

```typescript
// BAD: Select all columns
const users = await db.user.findMany();

// GOOD: Select specific columns
const users = await db.user.findMany({
  select: { id: true, email: true, name: true }
});

// Raw SQL
SELECT id, email, name FROM users;  -- NOT SELECT *
```

### Pagination

```typescript
// Offset pagination (simple but slow for large offsets)
const users = await db.user.findMany({
  skip: 100,
  take: 10,
  orderBy: { id: 'asc' }
});

// Cursor pagination (better for large datasets)
const users = await db.user.findMany({
  take: 10,
  cursor: { id: lastSeenId },
  orderBy: { id: 'asc' }
});

// Keyset pagination SQL
SELECT * FROM users
WHERE id > 100  -- last seen ID
ORDER BY id ASC
LIMIT 10;
```

### Efficient Counting

```sql
-- Avoid COUNT(*) on large tables
-- Use approximate counts when exact not needed

-- PostgreSQL: Table statistics (approximate)
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'users';

-- With conditions, use EXPLAIN
EXPLAIN SELECT COUNT(*) FROM users WHERE status = 'active';
-- Read "rows" estimate from output
```

### Bulk Operations

```typescript
// BAD: Individual inserts
for (const user of users) {
  await db.user.create({ data: user });
}

// GOOD: Bulk insert
await db.user.createMany({
  data: users,
  skipDuplicates: true
});

// Prisma: Bulk update with transaction
await db.$transaction(
  users.map(user =>
    db.user.update({
      where: { id: user.id },
      data: { status: user.status }
    })
  )
);

// Raw SQL bulk upsert
INSERT INTO users (id, email, name)
VALUES
  (1, 'a@test.com', 'A'),
  (2, 'b@test.com', 'B'),
  (3, 'c@test.com', 'C')
ON CONFLICT (id) DO UPDATE SET
  email = EXCLUDED.email,
  name = EXCLUDED.name;
```

### Subqueries vs Joins

```sql
-- Subquery (often slower)
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);

-- JOIN (usually faster)
SELECT DISTINCT u.* FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.amount > 100;

-- EXISTS (good for checking existence)
SELECT * FROM users u
WHERE EXISTS (
  SELECT 1 FROM orders o
  WHERE o.user_id = u.id AND o.amount > 100
);
```

## Index Optimization

### Index Selection Strategy

```sql
-- Query pattern analysis
-- For: SELECT * FROM orders WHERE user_id = ? AND status = ? ORDER BY created_at

-- Option 1: Separate indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
-- Problem: Bitmap scan, then sort

-- Option 2: Composite index (optimal)
CREATE INDEX idx_orders_user_status_created
ON orders(user_id, status, created_at DESC);
-- Result: Single index scan, no sort
```

### Covering Indexes

```sql
-- Query only needs id, email, name
SELECT id, email, name FROM users WHERE email LIKE 'a%';

-- Covering index includes all needed columns
CREATE INDEX idx_users_email_covering
ON users(email) INCLUDE (name);
-- Result: Index-only scan, no table access
```

### Partial Indexes

```sql
-- Only index active users
CREATE INDEX idx_users_email_active
ON users(email) WHERE deleted_at IS NULL;

-- Only index recent orders
CREATE INDEX idx_orders_recent
ON orders(created_at) WHERE created_at > NOW() - INTERVAL '30 days';
```

### Index Usage Analysis

```sql
-- PostgreSQL: Check if indexes are being used
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT
  schemaname || '.' || tablename as table,
  indexname,
  pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelid NOT IN (
  SELECT indexrelid FROM pg_constraint WHERE contype = 'p'
);
```

## Common Query Anti-Patterns

### Leading Wildcard Search

```sql
-- BAD: Cannot use index
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- GOOD: Trailing wildcard uses index
SELECT * FROM users WHERE email LIKE 'john%';

-- Solution: Full-text search or reverse index
CREATE INDEX idx_users_email_reverse ON users(reverse(email));
SELECT * FROM users WHERE reverse(email) LIKE reverse('%@gmail.com');
-- Or use pg_trgm extension
```

### Functions on Indexed Columns

```sql
-- BAD: Function prevents index use
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- GOOD: Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Or: Store normalized data
ALTER TABLE users ADD COLUMN email_normalized TEXT
  GENERATED ALWAYS AS (LOWER(email)) STORED;
CREATE INDEX idx_users_email_normalized ON users(email_normalized);
```

### Implicit Type Conversion

```sql
-- BAD: String column compared to integer
SELECT * FROM users WHERE phone = 1234567890;  -- type mismatch

-- GOOD: Match types
SELECT * FROM users WHERE phone = '1234567890';
```

### OR Conditions

```sql
-- Often slow: OR prevents single index use
SELECT * FROM users WHERE email = 'a@test.com' OR name = 'John';

-- Better: UNION (if needed)
SELECT * FROM users WHERE email = 'a@test.com'
UNION
SELECT * FROM users WHERE name = 'John';
```

### SELECT DISTINCT Overuse

```sql
-- BAD: DISTINCT to hide join duplicates
SELECT DISTINCT u.* FROM users u
JOIN orders o ON u.id = o.user_id;

-- GOOD: EXISTS for checking relationships
SELECT u.* FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- Or aggregate properly
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

## Database-Specific Optimizations

### PostgreSQL

```sql
-- Use LATERAL for row-by-row subqueries
SELECT u.*, latest_order.*
FROM users u
LEFT JOIN LATERAL (
  SELECT * FROM orders
  WHERE user_id = u.id
  ORDER BY created_at DESC
  LIMIT 1
) latest_order ON true;

-- Parallel query (PostgreSQL 10+)
SET max_parallel_workers_per_gather = 4;

-- Analyze table statistics
ANALYZE users;

-- Vacuum to reclaim space
VACUUM ANALYZE users;
```

### MySQL

```sql
-- Force index usage
SELECT * FROM users FORCE INDEX (idx_users_email)
WHERE email = 'test@example.com';

-- Optimize table
OPTIMIZE TABLE users;

-- Check query cache (deprecated in MySQL 8.0)
SHOW STATUS LIKE 'Qcache%';
```

### SQLite

```sql
-- Analyze for query planner
ANALYZE;

-- Check query plan
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com';

-- Enable WAL for better concurrency
PRAGMA journal_mode = WAL;

-- Optimize for reads
PRAGMA cache_size = -64000;  -- 64MB cache
```

## Monitoring and Alerting

### Key Metrics to Monitor

| Metric | Warning Threshold | Action |
|--------|------------------|--------|
| Query time > 1s | Alert | Optimize query |
| Sequential scans on large tables | Monitor | Add index |
| Lock wait time > 5s | Alert | Check for deadlocks |
| Connection count > 80% | Alert | Add connection pool |
| Cache hit ratio < 95% | Alert | Increase memory |

### Query Logging

```typescript
// Prisma: Enable query logging
const prisma = new PrismaClient({
  log: [
    { emit: 'event', level: 'query' },
    { emit: 'stdout', level: 'error' },
  ],
});

prisma.$on('query', (e) => {
  if (e.duration > 1000) {  // > 1 second
    console.warn('Slow query:', e.query, e.duration + 'ms');
  }
});

// Drizzle: Query logging
import { drizzle } from 'drizzle-orm/postgres-js';

const db = drizzle(client, {
  logger: {
    logQuery(query, params) {
      console.log('Query:', query, params);
    }
  }
});
```

## Query Optimization Checklist

### Before Optimization

- [ ] Identify slow query with monitoring
- [ ] Get execution plan with EXPLAIN ANALYZE
- [ ] Understand data distribution

### During Optimization

- [ ] Check for missing indexes
- [ ] Look for N+1 patterns
- [ ] Verify efficient join strategy
- [ ] Consider query rewrite
- [ ] Test with production-like data volume

### After Optimization

- [ ] Verify improvement with EXPLAIN ANALYZE
- [ ] Test under concurrent load
- [ ] Monitor for regressions
- [ ] Document optimization for team
