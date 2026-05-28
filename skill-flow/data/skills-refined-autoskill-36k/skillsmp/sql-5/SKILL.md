---
name: sql
description: Write SQL queries, optimize database performance, design schemas, and debug SQL issues. Use for database operations, query optimization, and schema design.
allowed-tools: Read, Bash
---

# SQL Skill

Comprehensive SQL assistance for database operations.

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
LIMIT 20 OFFSET 40;
```

**Upsert:**
```sql
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test')
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name;
```

**Window Functions:**
```sql
SELECT
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

## When to Use This Skill

Use `/sql` when working with databases, optimizing queries, or designing schemas.
