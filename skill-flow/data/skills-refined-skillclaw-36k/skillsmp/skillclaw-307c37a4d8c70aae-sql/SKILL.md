---
name: sql
description: Use this skill when you need to write SQL queries, optimize database performance, design schemas, and debug SQL issues.
---

# Skill body

## 1. Query Writing

**Basic Queries:**
```sql
-- SELECT with WHERE
SELECT name, email FROM users WHERE active = true;

-- JOIN operations
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Aggregate functions
SELECT category, COUNT(*), AVG(price)
FROM products
GROUP BY category
HAVING COUNT(*) > 5;

-- Subqueries
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);
```

## 2. Query Optimization

**Use EXPLAIN:**
```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';

-- Look for:
-- - Sequential scans (add indexes)
-- - High cost values
-- - Nested loops on large tables
```

**Add Indexes:**
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Multi-column index
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Unique index
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE active = true;
```

## 3. Schema Design

**Tables:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. Migrations

**Add Column:**
```sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Add with default
ALTER TABLE users ADD COLUMN verified BOOLEAN DEFAULT false;
```

**Modify Column:**
```sql
ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(320);
ALTER TABLE users ALTER COLUMN name SET NOT NULL;
```

## 5. Transactions

```sql
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- With error handling
BEGIN;
    -- operations
    SAVEPOINT sp1;
    -- more operations
    ROLLBACK TO sp1;
COMMIT;
```

## 6. Common Patterns

**Pagination:**
```sql
SELECT * FROM products
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;
```

## 7. Advanced Query Patterns

### Window Functions
```sql
-- Running totals
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM transactions;

-- Ranking
SELECT
    name,
    score,
    RANK() OVER (ORDER BY score DESC) as rank,
    DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
    ROW_NUMBER() OVER (ORDER BY score DESC) as row_num
FROM players;

-- Partition by category
SELECT
    category,
    product,
    sales,
    sales * 100.0 / SUM(sales) OVER (PARTITION BY category) as pct_of_category
FROM products;
```

### CTEs (Common Table Expressions)
```sql
WITH
monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total
    FROM orders
    GROUP BY 1
),
growth AS (
    SELECT
        month,
        total,
        LAG(total) OVER (ORDER BY month) as prev_month,
        (total - LAG(total) OVER (ORDER BY month)) / NULLIF(LAG(total) OVER (ORDER BY month), 0) * 100 as growth_pct
    FROM monthly_sales
)
SELECT * FROM growth WHERE growth_pct < 0;
```

### Recursive CTEs
```sql
-- Hierarchical data (org chart, categories)
WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates ORDER BY level, name;
```