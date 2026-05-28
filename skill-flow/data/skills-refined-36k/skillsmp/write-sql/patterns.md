# SQL Patterns Reference

A comprehensive guide to common SQL patterns for query construction and optimization.

## Table of Contents

1. [Join Patterns](#join-patterns)
2. [Subquery Patterns](#subquery-patterns)
3. [Common Table Expressions (CTEs)](#common-table-expressions-ctes)
4. [Window Functions](#window-functions)
5. [Aggregation Patterns](#aggregation-patterns)
6. [Data Transformation](#data-transformation)
7. [Recursive Queries](#recursive-queries)
8. [Performance Patterns](#performance-patterns)

---

## Join Patterns

### Inner Join - Match Both Tables
```sql
SELECT o.id, o.total, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
```

### Left Join - All from Left, Match from Right
```sql
-- Find customers with their orders (including those with no orders)
SELECT c.name, COALESCE(COUNT(o.id), 0) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;
```

### Self Join - Compare Rows in Same Table
```sql
-- Find employees and their managers
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### Cross Join - Cartesian Product
```sql
-- Generate all date-product combinations
SELECT d.date, p.product_id
FROM dates d
CROSS JOIN products p;
```

### Multiple Joins
```sql
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    p.name AS product_name,
    oi.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.order_date >= '2024-01-01';
```

---

## Subquery Patterns

### Scalar Subquery - Returns Single Value
```sql
SELECT
    name,
    salary,
    salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```

### Correlated Subquery - References Outer Query
```sql
-- Find latest order for each customer
SELECT c.name, o.order_date, o.total
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.order_date = (
    SELECT MAX(o2.order_date)
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
);
```

### EXISTS - Check for Existence
```sql
-- Customers who have placed orders
SELECT c.name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### NOT EXISTS - Check for Non-Existence
```sql
-- Customers with no orders
SELECT c.name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### IN with Subquery
```sql
-- Products that have been ordered
SELECT name
FROM products
WHERE id IN (SELECT DISTINCT product_id FROM order_items);
```

---

## Common Table Expressions (CTEs)

### Basic CTE
```sql
WITH high_value_orders AS (
    SELECT customer_id, SUM(total) AS total_spent
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total) > 1000
)
SELECT c.name, hvo.total_spent
FROM customers c
JOIN high_value_orders hvo ON c.id = hvo.customer_id
ORDER BY hvo.total_spent DESC;
```

### Multiple CTEs
```sql
WITH
monthly_sales AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(total) AS revenue
    FROM orders
    GROUP BY 1
),
monthly_growth AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly_sales
)
SELECT
    month,
    revenue,
    ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 2) AS growth_pct
FROM monthly_growth
WHERE prev_revenue IS NOT NULL;
```

### CTE for Readability
```sql
WITH
active_customers AS (
    SELECT * FROM customers WHERE status = 'active'
),
recent_orders AS (
    SELECT * FROM orders WHERE order_date >= DATE('now', '-30 days')
),
customer_order_summary AS (
    SELECT
        ac.id,
        ac.name,
        COUNT(ro.id) AS recent_order_count,
        COALESCE(SUM(ro.total), 0) AS recent_total
    FROM active_customers ac
    LEFT JOIN recent_orders ro ON ac.id = ro.customer_id
    GROUP BY ac.id, ac.name
)
SELECT * FROM customer_order_summary
WHERE recent_order_count > 0
ORDER BY recent_total DESC;
```

---

## Window Functions

### ROW_NUMBER - Sequential Numbering
```sql
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees;
```

### RANK and DENSE_RANK
```sql
SELECT
    name,
    department,
    salary,
    RANK() OVER (ORDER BY salary DESC) AS rank,           -- Gaps after ties
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank -- No gaps
FROM employees;
```

### Partition By - Group Within Groups
```sql
SELECT
    name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank,
    salary - AVG(salary) OVER (PARTITION BY department) AS diff_from_dept_avg
FROM employees;
```

### LAG and LEAD - Access Adjacent Rows
```sql
SELECT
    order_date,
    total,
    LAG(total) OVER (ORDER BY order_date) AS prev_total,
    LEAD(total) OVER (ORDER BY order_date) AS next_total,
    total - LAG(total) OVER (ORDER BY order_date) AS change
FROM orders;
```

### Running Totals
```sql
SELECT
    order_date,
    total,
    SUM(total) OVER (ORDER BY order_date) AS running_total,
    AVG(total) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7day_avg
FROM orders;
```

### FIRST_VALUE and LAST_VALUE
```sql
SELECT
    name,
    department,
    salary,
    FIRST_VALUE(name) OVER (PARTITION BY department ORDER BY salary DESC) AS highest_paid,
    LAST_VALUE(name) OVER (
        PARTITION BY department
        ORDER BY salary DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS lowest_paid
FROM employees;
```

---

## Aggregation Patterns

### Conditional Aggregation
```sql
SELECT
    category,
    COUNT(*) AS total_products,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_count,
    SUM(CASE WHEN stock = 0 THEN 1 ELSE 0 END) AS out_of_stock,
    AVG(CASE WHEN status = 'active' THEN price END) AS avg_active_price
FROM products
GROUP BY category;
```

### GROUP BY with ROLLUP (PostgreSQL/MySQL)
```sql
-- Note: SQLite doesn't support ROLLUP
SELECT
    COALESCE(category, 'TOTAL') AS category,
    COALESCE(subcategory, 'Subtotal') AS subcategory,
    SUM(revenue) AS revenue
FROM sales
GROUP BY ROLLUP(category, subcategory);
```

### HAVING - Filter Aggregated Results
```sql
SELECT
    customer_id,
    COUNT(*) AS order_count,
    SUM(total) AS total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 5 AND SUM(total) > 1000;
```

### Distinct Count
```sql
SELECT
    category,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) AS total_orders
FROM orders o
JOIN products p ON o.product_id = p.id
GROUP BY category;
```

---

## Data Transformation

### Pivot - Rows to Columns
```sql
SELECT
    product_id,
    SUM(CASE WHEN quarter = 1 THEN revenue ELSE 0 END) AS Q1,
    SUM(CASE WHEN quarter = 2 THEN revenue ELSE 0 END) AS Q2,
    SUM(CASE WHEN quarter = 3 THEN revenue ELSE 0 END) AS Q3,
    SUM(CASE WHEN quarter = 4 THEN revenue ELSE 0 END) AS Q4
FROM sales
GROUP BY product_id;
```

### Unpivot - Columns to Rows
```sql
SELECT product_id, 'Q1' AS quarter, Q1 AS revenue FROM quarterly_sales
UNION ALL
SELECT product_id, 'Q2', Q2 FROM quarterly_sales
UNION ALL
SELECT product_id, 'Q3', Q3 FROM quarterly_sales
UNION ALL
SELECT product_id, 'Q4', Q4 FROM quarterly_sales;
```

### String Aggregation
```sql
-- SQLite
SELECT customer_id, GROUP_CONCAT(product_name, ', ') AS products
FROM order_items
GROUP BY customer_id;

-- PostgreSQL
SELECT customer_id, STRING_AGG(product_name, ', ') AS products
FROM order_items
GROUP BY customer_id;
```

### COALESCE - Handle NULLs
```sql
SELECT
    name,
    COALESCE(phone, email, 'No contact') AS primary_contact
FROM customers;
```

### NULLIF - Prevent Division by Zero
```sql
SELECT
    name,
    revenue / NULLIF(cost, 0) AS profit_ratio
FROM products;
```

---

## Recursive Queries

### Hierarchical Data (Org Chart)
```sql
WITH RECURSIVE org_tree AS (
    -- Base case: CEO (no manager)
    SELECT id, name, manager_id, 1 AS level, name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case
    SELECT e.id, e.name, e.manager_id, ot.level + 1, ot.path || ' > ' || e.name
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY path;
```

### Category Tree
```sql
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, name AS full_path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ct.full_path || ' > ' || c.name
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree;
```

### Generate Number Series
```sql
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 100
)
SELECT n FROM numbers;
```

### Generate Date Series
```sql
WITH RECURSIVE dates AS (
    SELECT DATE('2024-01-01') AS date
    UNION ALL
    SELECT DATE(date, '+1 day') FROM dates WHERE date < DATE('2024-12-31')
)
SELECT date FROM dates;
```

---

## Performance Patterns

### Index-Friendly Queries
```sql
-- GOOD: Equality on indexed column
SELECT * FROM orders WHERE customer_id = 123;

-- GOOD: Range on indexed column
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- BAD: Function on indexed column (can't use index)
SELECT * FROM orders WHERE YEAR(order_date) = 2024;
```

### EXISTS vs IN for Large Sets
```sql
-- Prefer EXISTS for large subqueries
SELECT c.name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.total > 1000
);

-- IN is OK for small sets
SELECT name FROM products WHERE category_id IN (1, 2, 3);
```

### Batch Processing
```sql
-- Process in chunks to avoid locking
UPDATE products
SET last_checked = CURRENT_TIMESTAMP
WHERE id IN (
    SELECT id FROM products WHERE last_checked IS NULL LIMIT 1000
);
```

### Avoid SELECT *
```sql
-- BAD: Fetches all columns
SELECT * FROM orders WHERE customer_id = 123;

-- GOOD: Only fetch needed columns
SELECT id, order_date, total FROM orders WHERE customer_id = 123;
```
