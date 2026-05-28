# SQL Query Examples

## Basic Queries

### 1. List All Customers from a City

```sql
SELECT name, email
FROM customers
WHERE city = 'New York'
```

### 2. Get Top Customers by Order Total

```sql
SELECT c.name, SUM(o.total) as total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
ORDER BY total_spent DESC
LIMIT 5
```

### 3. Find Products in a Category

```sql
SELECT name, price
FROM products
WHERE category = 'Electronics'
ORDER BY price DESC
```

### 4. Recent Orders with Customer Info

```sql
SELECT
    c.name AS customer,
    p.name AS product,
    o.quantity,
    o.total,
    o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
ORDER BY o.order_date DESC
LIMIT 10
```

## Aggregation Queries

### 5. Sales by Month

```sql
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS order_count,
    SUM(total) AS total_sales
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month DESC
```

### 6. Average Order Value by Customer

```sql
SELECT
    c.name,
    COUNT(o.id) AS order_count,
    ROUND(AVG(o.total), 2) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
HAVING COUNT(o.id) > 0
ORDER BY avg_order_value DESC
```

### 7. Product Sales Summary

```sql
SELECT
    p.name,
    p.category,
    SUM(o.quantity) AS total_sold,
    SUM(o.total) AS total_revenue
FROM products p
LEFT JOIN orders o ON p.id = o.product_id
GROUP BY p.id, p.name, p.category
ORDER BY total_revenue DESC
```

## Subqueries

### 8. Customers with Above-Average Spending

```sql
SELECT name, email
FROM customers
WHERE id IN (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total) > (
        SELECT AVG(customer_total)
        FROM (
            SELECT SUM(total) as customer_total
            FROM orders
            GROUP BY customer_id
        )
    )
)
```

### 9. Products Never Ordered

```sql
SELECT name, price
FROM products
WHERE id NOT IN (
    SELECT DISTINCT product_id
    FROM orders
)
```

## Window Functions (if supported)

### 10. Running Total of Sales

```sql
SELECT
    order_date,
    total,
    SUM(total) OVER (ORDER BY order_date) AS running_total
FROM orders
ORDER BY order_date
```

### 11. Rank Customers by Spending

```sql
SELECT
    c.name,
    SUM(o.total) AS total_spent,
    RANK() OVER (ORDER BY SUM(o.total) DESC) AS spending_rank
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
```

## Data Modification (if allowed)

### 12. Insert New Customer

```sql
INSERT INTO customers (name, email, city)
VALUES ('John Doe', 'john@example.com', 'Boston')
```

### 13. Update Product Price

```sql
UPDATE products
SET price = price * 1.10
WHERE category = 'Electronics'
```

### 14. Delete Old Orders

```sql
DELETE FROM orders
WHERE order_date < DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
```

## Complex Joins

### 15. Full Customer Order History

```sql
SELECT
    c.name AS customer,
    c.email,
    c.city,
    COUNT(o.id) AS total_orders,
    COALESCE(SUM(o.total), 0) AS lifetime_value,
    MIN(o.order_date) AS first_order,
    MAX(o.order_date) AS last_order
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email, c.city
ORDER BY lifetime_value DESC
```
