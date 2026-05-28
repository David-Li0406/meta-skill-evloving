---
title: Never SELECT *, List Columns Explicitly
impact: CRITICAL
impactDescription: Reduces network transfer and enables covering indexes
tags: query, select, performance, columns
---

## Never SELECT *, List Columns Explicitly

SELECT * fetches all columns, wasting bandwidth and preventing index-only scans. List only the columns you need.

**Incorrect (SELECT *):**

```sql
-- ❌ Fetches all 50 columns when you only need 3
SELECT * FROM users WHERE status = 'active';

-- ❌ In joins, fetches duplicate columns
SELECT * FROM orders
JOIN users ON orders.user_id = users.id
JOIN products ON orders.product_id = products.id;

-- ❌ Breaks when schema changes
SELECT * FROM products; -- New column added = app breaks
```

**Correct (explicit columns):**

```sql
-- ✓ Only fetches needed columns
SELECT id, name, email FROM users WHERE status = 'active';

-- ✓ Clear column ownership in joins
SELECT
    o.id AS order_id,
    o.total,
    o.created_at,
    u.name AS customer_name,
    p.name AS product_name
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id;

-- ✓ Enables covering index (index-only scan)
-- Index: (status, name, email)
SELECT name, email FROM users WHERE status = 'active';
-- Query can be satisfied entirely from index!
```

**Benefits of explicit columns:**

```sql
-- 1. Smaller result set = faster transfer
-- 2. Covering indexes possible
-- 3. Self-documenting queries
-- 4. Schema changes don't break app
-- 5. Prevents accidental sensitive data exposure

-- For COUNT, you don't need any columns
SELECT COUNT(*) FROM users WHERE status = 'active';

-- EXISTS doesn't need columns either
SELECT EXISTS(SELECT 1 FROM users WHERE email = 'test@example.com');
```

**Exception - when SELECT * is acceptable:**

```sql
-- Temporary exploration in development
SELECT * FROM new_table LIMIT 10;

-- When you genuinely need all columns AND they're stable
-- (rare - usually better to be explicit)
```

Reference: [SELECT Optimization](https://dev.mysql.com/doc/refman/8.0/en/select-optimization.html)
