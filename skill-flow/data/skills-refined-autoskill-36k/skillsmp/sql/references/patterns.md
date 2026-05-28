# Advanced SQL Patterns

Reference for advanced SQL patterns across database engines.

## Table of Contents
- [Window Functions](#window-functions)
- [CTEs (Common Table Expressions)](#ctes-common-table-expressions)
- [Pivoting Data](#pivoting-data)
- [Date/Time Operations](#datetime-operations)
- [JSON Operations](#json-operations)

---

## Window Functions

Window functions perform calculations across rows related to the current row.

### ROW_NUMBER, RANK, DENSE_RANK

```sql
-- Number rows within each group
SELECT
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) as order_num,
    RANK() OVER (ORDER BY amount DESC) as amount_rank
FROM orders;
```

### LAG and LEAD

```sql
-- Compare with previous/next row
SELECT
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) as prev_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) as daily_change
FROM daily_sales;
```

### Running Totals and Moving Averages

```sql
-- Running total
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Moving average (last 7 rows)
SELECT
    date,
    value,
    AVG(value) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7
FROM metrics;
```

### FIRST_VALUE and LAST_VALUE

```sql
-- Get first/last values in partition
SELECT
    department,
    employee,
    salary,
    FIRST_VALUE(employee) OVER (PARTITION BY department ORDER BY salary DESC) as top_earner
FROM employees;
```

---

## CTEs (Common Table Expressions)

CTEs create named temporary result sets for cleaner queries.

### Basic CTE

```sql
WITH high_value_orders AS (
    SELECT * FROM orders WHERE amount > 1000
)
SELECT customer_id, COUNT(*) as order_count
FROM high_value_orders
GROUP BY customer_id;
```

### Multiple CTEs

```sql
WITH
monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) as month,
        SUM(amount) as total
    FROM orders
    GROUP BY 1
),
monthly_avg AS (
    SELECT AVG(total) as avg_total FROM monthly_sales
)
SELECT
    ms.month,
    ms.total,
    ma.avg_total,
    ms.total - ma.avg_total as diff_from_avg
FROM monthly_sales ms
CROSS JOIN monthly_avg ma;
```

### Recursive CTE

```sql
-- Hierarchical data (org chart, categories)
WITH RECURSIVE org_tree AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees under managers
    SELECT e.id, e.name, e.manager_id, t.level + 1
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree ORDER BY level, name;
```

---

## Pivoting Data

Transform rows to columns.

### CASE WHEN Aggregation (All Engines)

```sql
-- Pivot sales by quarter
SELECT
    product,
    SUM(CASE WHEN quarter = 'Q1' THEN amount ELSE 0 END) as Q1,
    SUM(CASE WHEN quarter = 'Q2' THEN amount ELSE 0 END) as Q2,
    SUM(CASE WHEN quarter = 'Q3' THEN amount ELSE 0 END) as Q3,
    SUM(CASE WHEN quarter = 'Q4' THEN amount ELSE 0 END) as Q4
FROM sales
GROUP BY product;
```

### Conditional Counts

```sql
-- Count by status
SELECT
    department,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active,
    COUNT(CASE WHEN status = 'inactive' THEN 1 END) as inactive
FROM employees
GROUP BY department;
```

### SQL Server PIVOT

```sql
-- SQL Server specific
SELECT *
FROM (
    SELECT product, quarter, amount FROM sales
) src
PIVOT (
    SUM(amount) FOR quarter IN ([Q1], [Q2], [Q3], [Q4])
) pvt;
```

---

## Date/Time Operations

Date handling varies significantly by engine.

### Date Truncation

| Engine | Truncate to Month |
|--------|------------------|
| PostgreSQL | `DATE_TRUNC('month', date_col)` |
| MySQL | `DATE_FORMAT(date_col, '%Y-%m-01')` |
| SQLite | `DATE(date_col, 'start of month')` |
| SQL Server | `DATETRUNC(month, date_col)` (2022+) or `DATEADD(month, DATEDIFF(month, 0, date_col), 0)` |

### Date Arithmetic

| Operation | PostgreSQL | MySQL | SQLite | SQL Server |
|-----------|------------|-------|--------|------------|
| Add days | `date + INTERVAL '7 days'` | `DATE_ADD(date, INTERVAL 7 DAY)` | `DATE(date, '+7 days')` | `DATEADD(day, 7, date)` |
| Difference | `date1 - date2` | `DATEDIFF(date1, date2)` | `JULIANDAY(date1) - JULIANDAY(date2)` | `DATEDIFF(day, date2, date1)` |

### Extract Components

| Component | PostgreSQL | MySQL | SQLite | SQL Server |
|-----------|------------|-------|--------|------------|
| Year | `EXTRACT(YEAR FROM date)` | `YEAR(date)` | `strftime('%Y', date)` | `YEAR(date)` |
| Month | `EXTRACT(MONTH FROM date)` | `MONTH(date)` | `strftime('%m', date)` | `MONTH(date)` |
| Day of week | `EXTRACT(DOW FROM date)` | `DAYOFWEEK(date)` | `strftime('%w', date)` | `DATEPART(dw, date)` |

### Group by Time Period

```sql
-- PostgreSQL
SELECT DATE_TRUNC('week', created_at) as week, COUNT(*)
FROM events GROUP BY 1;

-- MySQL
SELECT DATE(created_at - INTERVAL WEEKDAY(created_at) DAY) as week, COUNT(*)
FROM events GROUP BY 1;

-- SQLite
SELECT DATE(created_at, 'weekday 0', '-7 days') as week, COUNT(*)
FROM events GROUP BY 1;
```

---

## JSON Operations

Working with JSON columns varies by engine.

### PostgreSQL JSON

```sql
-- Access JSON field
SELECT data->>'name' as name FROM users;                    -- text
SELECT data->'address'->>'city' as city FROM users;         -- nested

-- Filter by JSON value
SELECT * FROM users WHERE data->>'status' = 'active';

-- JSON aggregation
SELECT JSON_AGG(name) FROM users WHERE active = true;

-- JSON array contains
SELECT * FROM products WHERE tags ? 'sale';                 -- contains key
SELECT * FROM products WHERE tags @> '["featured"]';        -- contains value
```

### MySQL JSON

```sql
-- Access JSON field
SELECT JSON_EXTRACT(data, '$.name') as name FROM users;     -- with quotes
SELECT JSON_UNQUOTE(JSON_EXTRACT(data, '$.name')) FROM users; -- without quotes
SELECT data->>'$.name' as name FROM users;                  -- shorthand (8.0+)

-- Filter by JSON value
SELECT * FROM users WHERE JSON_EXTRACT(data, '$.status') = 'active';

-- JSON array contains
SELECT * FROM products WHERE JSON_CONTAINS(tags, '"sale"');
```

### SQLite JSON

```sql
-- Access JSON field (3.38+)
SELECT json_extract(data, '$.name') as name FROM users;
SELECT data->>'$.name' as name FROM users;                  -- shorthand

-- Filter by JSON value
SELECT * FROM users WHERE json_extract(data, '$.status') = 'active';
```

### SQL Server JSON

```sql
-- Access JSON field
SELECT JSON_VALUE(data, '$.name') as name FROM users;       -- scalar
SELECT JSON_QUERY(data, '$.address') as address FROM users; -- object/array

-- Filter by JSON value
SELECT * FROM users WHERE JSON_VALUE(data, '$.status') = 'active';

-- Parse JSON array
SELECT value FROM OPENJSON(@json_array);
```
