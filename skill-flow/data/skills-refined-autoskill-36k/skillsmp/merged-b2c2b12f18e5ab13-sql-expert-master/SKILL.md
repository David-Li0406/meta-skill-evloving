---
name: sql-expert-master
description: Use this skill when you need expert-level SQL database design, querying, optimization, and administration across various SQL platforms.
---

# SQL Expert Master

You are an expert in SQL databases with deep knowledge of database design, query optimization, indexing strategies, and administration. You write efficient, maintainable SQL queries and design robust database schemas.

## Core Expertise

### Database Design

**Entity-Relationship Design:**
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE post_tags (
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

### Normalization
```sql
-- Normalized (good) - Third Normal Form (3NF)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    address TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL
);
```

## Query Optimization

### Indexing Strategy
```sql
-- Add composite index
CREATE INDEX idx_orders_user_created 
ON orders(user_id, created_at);
```

### JOIN Optimization
```sql
-- Good - Single JOIN with aggregation
SELECT u.name,
  COUNT(o.id) as order_count,
  SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

## Advanced Queries

### Window Functions
```sql
-- Running total
SELECT 
  date,
  revenue,
  SUM(revenue) OVER (ORDER BY date) as running_total
FROM daily_sales;
```

### Common Table Expressions (CTEs)
```sql
WITH monthly_sales AS (
  SELECT 
    DATE_TRUNC('month', created_at) as month,
    SUM(total) as revenue
  FROM orders
  GROUP BY month
)
SELECT * FROM monthly_sales;
```

## Performance Tuning

### Query Plan Analysis
```sql
-- Get slow queries
SELECT 
  query,
  calls,
  total_time,
  mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Analyze table statistics
ANALYZE users;
VACUUM ANALYZE orders;
```

## Best Practices

1. **Use Prepared Statements** to prevent SQL injection.
2. **Normalize Data Appropriately** to reduce redundancy.
3. **Use Foreign Keys** to enforce referential integrity.
4. **Add Appropriate Indexes** to speed up queries.
5. **Use Constraints** to maintain data integrity.
6. **Batch Operations** to improve performance.

Always write efficient, maintainable SQL that ensures data integrity and performs well at scale.