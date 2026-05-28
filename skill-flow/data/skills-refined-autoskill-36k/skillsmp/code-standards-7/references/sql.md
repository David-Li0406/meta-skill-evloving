# SQL Standards

Guidelines for writing clear, maintainable SQL.

## Formatting

### Keywords

- **UPPERCASE** for SQL keywords: `SELECT`, `FROM`, `WHERE`, `JOIN`
- **lowercase** for identifiers: `user_id`, `created_at`

```sql
-- Yes
SELECT 
    user_id,
    email,
    created_at
FROM users
WHERE is_active = TRUE;

-- No
select USER_ID, EMAIL from USERS where IS_ACTIVE = true;
```

### Alignment

Major clauses on new lines, indented consistently:

```sql
SELECT 
    u.id,
    u.name,
    u.email,
    o.total AS order_total
FROM users u
INNER JOIN orders o 
    ON u.id = o.user_id
WHERE u.is_active = TRUE
    AND o.created_at > '2024-01-01'
ORDER BY o.created_at DESC
LIMIT 100;
```

### Commas

Leading commas (preferred for easier commenting/diffing):

```sql
SELECT 
    id
    , name
    , email
    , created_at
FROM users;
```

Or trailing (more common):

```sql
SELECT 
    id,
    name,
    email,
    created_at
FROM users;
```

Pick one and be consistent.

---

## Naming

### Tables

- **Plural nouns:** `users`, `orders`, `order_items`
- **snake_case:** `user_preferences`, `payment_methods`
- **No prefixes:** `users` not `tbl_users`

### Columns

- **snake_case:** `first_name`, `created_at`
- **Descriptive:** `user_id` not `uid`
- **Boolean prefix:** `is_`, `has_`, `can_` → `is_active`, `has_shipped`
- **Timestamps:** `_at` suffix → `created_at`, `updated_at`, `deleted_at`

### Primary Keys

- Use `id` for single-column primary keys
- Use `[table]_id` for foreign keys: `user_id`, `order_id`

### Indexes

```
idx_[table]_[columns]
```

Examples:
- `idx_users_email`
- `idx_orders_user_id_created_at`

---

## Query Patterns

### Explicit Column Lists

Never `SELECT *` in application code:

```sql
-- Yes
SELECT id, name, email FROM users;

-- No (in production code)
SELECT * FROM users;
```

### Table Aliases

Use meaningful short aliases:

```sql
SELECT 
    u.name AS user_name,
    o.total AS order_total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### JOIN Syntax

Always use explicit `JOIN`:

```sql
-- Yes
SELECT *
FROM orders o
INNER JOIN users u ON o.user_id = u.id;

-- No (implicit join)
SELECT *
FROM orders o, users u
WHERE o.user_id = u.id;
```

### Subqueries vs CTEs

Use CTEs for readability:

```sql
-- Yes - CTE
WITH active_users AS (
    SELECT id, name
    FROM users
    WHERE is_active = TRUE
),
recent_orders AS (
    SELECT user_id, SUM(total) AS total_spent
    FROM orders
    WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT 
    u.name,
    COALESCE(o.total_spent, 0) AS total_spent
FROM active_users u
LEFT JOIN recent_orders o ON u.id = o.user_id;

-- Avoid - nested subqueries
SELECT 
    u.name,
    COALESCE(o.total_spent, 0)
FROM (SELECT id, name FROM users WHERE is_active = TRUE) u
LEFT JOIN (
    SELECT user_id, SUM(total) AS total_spent
    FROM orders
    WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
) o ON u.id = o.user_id;
```

---

## Performance

### Index-Friendly Conditions

```sql
-- Yes - can use index on email
WHERE email = 'test@example.com'

-- No - function prevents index use
WHERE LOWER(email) = 'test@example.com'

-- Fix - use expression index or store lowercase
```

### Avoid SELECT DISTINCT as a Fix

If you need `DISTINCT`, you probably have a join problem:

```sql
-- Suspicious - why are there duplicates?
SELECT DISTINCT u.id, u.name
FROM users u
JOIN orders o ON u.id = o.user_id;

-- Better - understand and fix the join
SELECT u.id, u.name
FROM users u
WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = u.id);
```

### LIMIT for Safety

Always use `LIMIT` in development/debugging:

```sql
-- Safe exploration
SELECT * FROM large_table LIMIT 100;
```

### Batch Operations

For large updates/deletes, batch to avoid lock contention:

```sql
-- Batch delete
DELETE FROM logs
WHERE created_at < '2024-01-01'
LIMIT 10000;
-- Run repeatedly until 0 rows affected
```

---

## Transactions

### Explicit Transactions

For multi-statement operations:

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT;
-- Or ROLLBACK on error
```

### Keep Transactions Short

- Don't hold transactions across user interactions
- Acquire locks in consistent order to prevent deadlocks

---

## Safety

### Parameterized Queries

Never interpolate user input:

```python
# NEVER
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ALWAYS
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### WHERE Clause on UPDATE/DELETE

Always require a `WHERE` clause:

```sql
-- Dangerous - affects all rows
UPDATE users SET is_active = FALSE;

-- Safe
UPDATE users SET is_active = FALSE WHERE last_login < '2023-01-01';
```

### Soft Deletes

Consider soft deletes for important data:

```sql
-- Instead of DELETE
UPDATE users 
SET deleted_at = NOW()
WHERE id = 123;

-- Query active records
SELECT * FROM users WHERE deleted_at IS NULL;
```

---

## Comments

### Explain Why, Not What

```sql
-- Bad: Select users
SELECT * FROM users;

-- Good: Exclude soft-deleted users for GDPR compliance
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Complex Query Documentation

```sql
/*
 * Monthly revenue report
 * 
 * Calculates total revenue per product category for the previous month.
 * Excludes refunded orders and test accounts.
 *
 * Used by: dashboard, finance export
 * Last updated: 2024-03-15
 */
WITH valid_orders AS (
    -- Exclude test accounts (email domain) and refunds
    SELECT o.*
    FROM orders o
    JOIN users u ON o.user_id = u.id
    WHERE u.email NOT LIKE '%@test.com'
        AND o.status != 'refunded'
        AND o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
        AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
)
SELECT ...
```

---

## Anti-Patterns

### OR in WHERE (Performance)

```sql
-- Slow - can't use single index
WHERE status = 'active' OR status = 'pending'

-- Better
WHERE status IN ('active', 'pending')
```

### NOT IN with NULL

```sql
-- Bug: returns no rows if subquery contains NULL
WHERE id NOT IN (SELECT user_id FROM blocked_users)

-- Safe
WHERE id NOT IN (SELECT user_id FROM blocked_users WHERE user_id IS NOT NULL)

-- Better
WHERE NOT EXISTS (SELECT 1 FROM blocked_users WHERE user_id = users.id)
```

### Implicit Type Conversion

```sql
-- Bad - string comparison on integer column
WHERE user_id = '123'

-- Good - correct type
WHERE user_id = 123
```
