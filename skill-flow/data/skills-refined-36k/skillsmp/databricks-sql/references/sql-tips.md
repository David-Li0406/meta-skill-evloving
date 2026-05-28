# SQL Tips

Best practices for writing queries in Databricks SQL.

## Basics

### 3-Level Namespace

Unity Catalog uses `catalog.schema.table` structure.

```sql
SELECT * FROM main.default.users
```

### Use LIMIT

Always use `LIMIT` during development and debugging.

```sql
-- Development
SELECT * FROM large_table LIMIT 100

-- Production: use proper filtering
SELECT * FROM large_table WHERE date = current_date()
```

## Performance

### Leverage Partitions

Filtering on partition columns limits scan range.

```sql
-- Filter on partition column (e.g., date)
SELECT * FROM events WHERE date >= '2024-01-01'
```

### Avoid SELECT *

Specify only needed columns.

```sql
-- Bad
SELECT * FROM users WHERE id = 1

-- Good
SELECT id, name, email FROM users WHERE id = 1
```

### EXISTS vs IN

Use `EXISTS` when subquery result is large.

```sql
-- IN (when subquery result is small)
SELECT * FROM orders WHERE user_id IN (SELECT id FROM vip_users)

-- EXISTS (when subquery result is large)
SELECT * FROM orders o WHERE EXISTS (
    SELECT 1 FROM users u WHERE u.id = o.user_id AND u.status = 'active'
)
```

## Useful Functions

### Date Operations

```sql
-- Today
SELECT current_date()

-- N days ago
SELECT date_sub(current_date(), 7)

-- Truncate date
SELECT date_trunc('month', order_date)

-- Format date
SELECT date_format(created_at, 'yyyy-MM-dd HH:mm:ss')
```

### String Operations

```sql
-- Concatenate
SELECT concat(first_name, ' ', last_name) AS full_name

-- Split
SELECT split(tags, ',') AS tag_array

-- Regex
SELECT regexp_extract(email, '@(.+)$', 1) AS domain
```

### JSON Operations

```sql
-- Extract field from JSON
SELECT json_data:name AS name
SELECT json_data:address.city AS city

-- JSON array
SELECT json_data:items[0] AS first_item

-- Parse JSON
SELECT from_json(json_string, 'struct<name:string,age:int>') AS parsed
```

### NULL Handling

```sql
-- Replace NULL
SELECT coalesce(nickname, name, 'Unknown') AS display_name

-- NULL check
SELECT * FROM users WHERE email IS NOT NULL

-- NULL-safe comparison
SELECT * FROM t1, t2 WHERE t1.value <=> t2.value
```

## Aggregation

### GROUP BY

```sql
SELECT
    category,
    count(*) AS count,
    sum(amount) AS total,
    avg(amount) AS average
FROM orders
GROUP BY category
```

### HAVING

```sql
SELECT category, count(*) AS count
FROM orders
GROUP BY category
HAVING count(*) > 100
```

### Window Functions

```sql
-- Ranking
SELECT
    name,
    score,
    rank() OVER (ORDER BY score DESC) AS rank
FROM players

-- Cumulative sum
SELECT
    date,
    amount,
    sum(amount) OVER (ORDER BY date) AS cumulative
FROM daily_sales

-- Moving average
SELECT
    date,
    amount,
    avg(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS weekly_avg
FROM daily_sales
```

## CTE (Common Table Expression)

Break complex queries into CTEs.

```sql
WITH active_users AS (
    SELECT * FROM users WHERE status = 'active'
),
recent_orders AS (
    SELECT * FROM orders WHERE date >= date_sub(current_date(), 30)
)
SELECT
    u.name,
    count(o.id) AS order_count
FROM active_users u
JOIN recent_orders o ON u.id = o.user_id
GROUP BY u.name
```

## EXPLAIN

Check query plan to identify bottlenecks.

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 123
EXPLAIN EXTENDED SELECT * FROM orders WHERE user_id = 123
```
