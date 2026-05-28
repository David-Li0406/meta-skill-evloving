# Database Performance

Query optimization and indexing strategies.

## N+1 Query Problem

The most common database performance issue.

```python
# ❌ N+1 Problem: 1 query for posts + N queries for authors
posts = Post.objects.all()  # 1 query
for post in posts:
    print(post.author.name)  # N queries (one per post)

# ✅ Fixed with JOIN/prefetch
posts = Post.objects.select_related('author').all()  # 1 query
for post in posts:
    print(post.author.name)  # No additional queries
```

## Indexing Strategies

### When to Add Indexes

- Columns in WHERE clauses
- Columns in JOIN conditions
- Columns in ORDER BY
- Foreign keys

### When NOT to Index

- Small tables (< 1000 rows)
- Columns with low cardinality (boolean, status)
- Frequently updated columns
- Tables with heavy write loads

### Index Types

```sql
-- B-tree (default, most common)
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Works for: WHERE user_id = ? AND status = ?
-- Works for: WHERE user_id = ?
-- Does NOT work for: WHERE status = ?

-- Partial index (filter subset)
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';

-- Covering index (includes all needed columns)
CREATE INDEX idx_users_lookup ON users(email) INCLUDE (name, created_at);
```

## Query Optimization

### Use EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Look for:
-- - Seq Scan (full table scan - usually bad)
-- - Index Scan (good)
-- - Rows estimate vs actual (big difference = stale statistics)
-- - Sort (expensive for large sets)
```

### Common Fixes

```sql
-- ❌ Function on indexed column prevents index use
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- ✅ Use expression index or normalize data
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- ❌ LIKE with leading wildcard
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- ✅ Use full-text search or reverse index
CREATE INDEX idx_users_email_reverse ON users(REVERSE(email));

-- ❌ OR can prevent index use
SELECT * FROM orders WHERE user_id = 1 OR status = 'pending';

-- ✅ Use UNION
SELECT * FROM orders WHERE user_id = 1
UNION
SELECT * FROM orders WHERE status = 'pending';
```

## Connection Pooling

```python
# ❌ New connection per request
def get_user(id):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    return cursor.fetchone()

# ✅ Connection pool
from psycopg2 import pool

connection_pool = pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    dsn=DATABASE_URL
)

def get_user(id):
    conn = connection_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        return cursor.fetchone()
    finally:
        connection_pool.putconn(conn)
```

## Pagination

```sql
-- ❌ OFFSET is slow for large offsets
SELECT * FROM posts ORDER BY created_at DESC OFFSET 10000 LIMIT 20;
-- Must scan and discard 10000 rows

-- ✅ Cursor-based pagination
SELECT * FROM posts
WHERE created_at < '2024-01-15T10:30:00'
ORDER BY created_at DESC
LIMIT 20;
-- Uses index directly
```

## Monitoring Queries

```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Find missing indexes
SELECT schemaname, tablename, seq_scan, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_scan DESC;
```
