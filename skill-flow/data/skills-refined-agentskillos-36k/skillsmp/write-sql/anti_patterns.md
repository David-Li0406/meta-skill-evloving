# SQL Anti-Patterns to Avoid

This guide covers common SQL anti-patterns, why they're problematic, and the correct alternatives.

## Table of Contents

1. [Query Performance Anti-Patterns](#query-performance-anti-patterns)
2. [Schema Design Anti-Patterns](#schema-design-anti-patterns)
3. [Security Anti-Patterns](#security-anti-patterns)
4. [Data Integrity Anti-Patterns](#data-integrity-anti-patterns)
5. [Readability Anti-Patterns](#readability-anti-patterns)

---

## Query Performance Anti-Patterns

### 1. SELECT * (Selecting All Columns)

**Anti-Pattern:**
```sql
SELECT * FROM orders WHERE customer_id = 123;
```

**Problems:**
- Fetches unnecessary data, increasing I/O and memory usage
- Makes query fragile if table structure changes
- Prevents covering index optimization
- Makes it unclear what data is actually needed

**Correct:**
```sql
SELECT id, order_date, total, status
FROM orders
WHERE customer_id = 123;
```

---

### 2. Functions on Indexed Columns

**Anti-Pattern:**
```sql
-- Function on column prevents index usage
SELECT * FROM orders WHERE YEAR(order_date) = 2024;
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
SELECT * FROM products WHERE price + tax > 100;
```

**Problems:**
- Database cannot use indexes on the column
- Forces a full table scan
- Dramatically slower on large tables

**Correct:**
```sql
-- Use range queries instead
SELECT * FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';

-- Store normalized data or create functional index
SELECT * FROM users WHERE email_lower = 'john@example.com';

-- Rewrite arithmetic
SELECT * FROM products WHERE price > 100 - tax;
```

---

### 3. Leading Wildcards in LIKE

**Anti-Pattern:**
```sql
SELECT * FROM customers WHERE name LIKE '%smith';
SELECT * FROM products WHERE description LIKE '%widget%';
```

**Problems:**
- Cannot use indexes
- Forces full table scan
- Very slow on large tables

**Correct:**
```sql
-- Trailing wildcard can use index
SELECT * FROM customers WHERE name LIKE 'Smith%';

-- Use full-text search for middle wildcards
SELECT * FROM products
WHERE MATCH(description) AGAINST('widget');

-- Or consider a search index (Elasticsearch, etc.)
```

---

### 4. OR Conditions on Different Columns

**Anti-Pattern:**
```sql
SELECT * FROM products
WHERE name = 'Widget' OR category = 'Tools';
```

**Problems:**
- Often can't use indexes efficiently
- May cause full table scan

**Correct:**
```sql
-- UNION of separate indexed queries
SELECT * FROM products WHERE name = 'Widget'
UNION
SELECT * FROM products WHERE category = 'Tools';

-- Or use IN for same column
SELECT * FROM products WHERE category IN ('Tools', 'Hardware');
```

---

### 5. Using IN with Large Subqueries

**Anti-Pattern:**
```sql
SELECT * FROM customers
WHERE id IN (SELECT customer_id FROM orders WHERE total > 1000);
```

**Problems:**
- Subquery may return millions of rows
- All values loaded into memory
- Slow comparison

**Correct:**
```sql
-- EXISTS stops at first match
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = c.id AND o.total > 1000
);

-- Or use JOIN
SELECT DISTINCT c.*
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.total > 1000;
```

---

### 6. N+1 Query Problem

**Anti-Pattern:**
```python
# Pseudocode - runs N+1 queries
customers = query("SELECT * FROM customers")
for customer in customers:
    orders = query(f"SELECT * FROM orders WHERE customer_id = {customer.id}")
```

**Problems:**
- One query per row
- Network latency multiplied
- Database connection overhead

**Correct:**
```sql
-- Single query with JOIN
SELECT c.*, o.id AS order_id, o.total
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

-- Or batch fetch
SELECT * FROM orders WHERE customer_id IN (1, 2, 3, 4, 5);
```

---

### 7. Not Using LIMIT in Development

**Anti-Pattern:**
```sql
SELECT * FROM logs;  -- May return millions of rows
```

**Problems:**
- Overwhelming amount of data
- Memory exhaustion
- Long query times

**Correct:**
```sql
-- Always use LIMIT during development
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;
```

---

### 8. Implicit Type Conversion

**Anti-Pattern:**
```sql
-- user_id is INTEGER, but comparing to string
SELECT * FROM users WHERE user_id = '123';

-- date column compared to string
SELECT * FROM orders WHERE order_date = '2024-01-01';
```

**Problems:**
- May prevent index usage
- Can cause unexpected results
- Performance overhead for conversion

**Correct:**
```sql
-- Use correct types
SELECT * FROM users WHERE user_id = 123;

-- Explicit type conversion if needed
SELECT * FROM orders WHERE order_date = DATE('2024-01-01');
```

---

## Schema Design Anti-Patterns

### 9. Storing Comma-Separated Values

**Anti-Pattern:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    tags TEXT  -- 'admin,editor,viewer'
);

SELECT * FROM users WHERE tags LIKE '%admin%';
```

**Problems:**
- Cannot use indexes
- Cannot enforce referential integrity
- Difficult to update individual values
- Risk of matching partial values ('admin' matches 'superadmin')

**Correct:**
```sql
-- Use a junction table
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE tags (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE user_tags (
    user_id INTEGER REFERENCES users(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (user_id, tag_id)
);

SELECT u.* FROM users u
JOIN user_tags ut ON u.id = ut.user_id
JOIN tags t ON ut.tag_id = t.id
WHERE t.name = 'admin';
```

---

### 10. Entity-Attribute-Value (EAV) Pattern

**Anti-Pattern:**
```sql
CREATE TABLE entity_attributes (
    entity_id INTEGER,
    attribute_name TEXT,
    attribute_value TEXT
);

-- To get all attributes for one entity
SELECT * FROM entity_attributes WHERE entity_id = 1;
```

**Problems:**
- No type safety (everything is TEXT)
- Complex queries for simple operations
- Poor performance
- No constraints or validation

**Correct:**
```sql
-- Use proper columns
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2),
    weight DECIMAL(10,2),
    color TEXT
);

-- Or use JSON for truly dynamic attributes
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    attributes JSON
);
```

---

### 11. No Primary Key

**Anti-Pattern:**
```sql
CREATE TABLE logs (
    timestamp DATETIME,
    level TEXT,
    message TEXT
);
```

**Problems:**
- Cannot uniquely identify rows
- Cannot reference from other tables
- UPDATE/DELETE operations are risky
- No clustering for performance

**Correct:**
```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    level TEXT NOT NULL,
    message TEXT
);
```

---

## Security Anti-Patterns

### 12. SQL Injection Vulnerability

**Anti-Pattern:**
```python
# NEVER do this!
query = f"SELECT * FROM users WHERE name = '{user_input}'"
```

**Problems:**
- Attacker can inject: `'; DROP TABLE users; --`
- Data breach, data loss, unauthorized access

**Correct:**
```python
# Use parameterized queries
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (user_input,))

# Or use ORM
User.query.filter_by(name=user_input).all()
```

---

### 13. Exposing Sensitive Data

**Anti-Pattern:**
```sql
SELECT * FROM users;  -- Includes password_hash, ssn, etc.
```

**Problems:**
- Exposes sensitive information
- Compliance violations (GDPR, HIPAA)
- Security breach if logged

**Correct:**
```sql
-- Only select needed, non-sensitive columns
SELECT id, name, email, created_at FROM users;

-- Create a view for safe access
CREATE VIEW users_safe AS
SELECT id, name, email, created_at FROM users;
```

---

### 14. Dynamic Table/Column Names

**Anti-Pattern:**
```python
# User controls table name
table = user_input  # Could be "users; DROP TABLE users; --"
query = f"SELECT * FROM {table}"
```

**Problems:**
- SQL injection even with parameterized queries
- Parameters don't work for identifiers

**Correct:**
```python
# Whitelist allowed tables
allowed_tables = {'users', 'products', 'orders'}
if table not in allowed_tables:
    raise ValueError("Invalid table")

# Then use the validated name
query = f"SELECT * FROM {table}"
```

---

## Data Integrity Anti-Patterns

### 15. Missing Foreign Key Constraints

**Anti-Pattern:**
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,  -- No constraint!
    total DECIMAL(10,2)
);
```

**Problems:**
- Orphaned records (orders without customers)
- Data inconsistency
- Application must enforce integrity

**Correct:**
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    total DECIMAL(10,2)
);
```

---

### 16. Using FLOAT for Money

**Anti-Pattern:**
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    price FLOAT  -- Floating point!
);

-- 0.1 + 0.2 might equal 0.30000000000000004
```

**Problems:**
- Floating point precision errors
- Rounding issues in financial calculations
- Legal/compliance issues

**Correct:**
```sql
-- Use DECIMAL with fixed precision
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    price DECIMAL(10, 2)  -- 10 digits, 2 after decimal
);

-- Or store cents as INTEGER
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    price_cents INTEGER  -- $19.99 = 1999
);
```

---

### 17. Soft Delete Without Indexes

**Anti-Pattern:**
```sql
-- Every query needs to filter deleted records
SELECT * FROM users WHERE email = 'x@y.com' AND deleted_at IS NULL;
SELECT * FROM orders WHERE customer_id = 1 AND deleted_at IS NULL;
```

**Problems:**
- Easy to forget the filter
- Performance issues without proper index
- Queries become verbose

**Correct:**
```sql
-- Create partial index for active records
CREATE INDEX idx_users_active ON users(email) WHERE deleted_at IS NULL;

-- Or use a view
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;

-- Then query the view
SELECT * FROM active_users WHERE email = 'x@y.com';
```

---

## Readability Anti-Patterns

### 18. Implicit Join Syntax

**Anti-Pattern:**
```sql
SELECT o.id, c.name
FROM orders o, customers c
WHERE o.customer_id = c.id;
```

**Problems:**
- Easy to accidentally create cartesian products
- Join conditions mixed with filters
- Harder to read and maintain

**Correct:**
```sql
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```

---

### 19. No Table Aliases with Joins

**Anti-Pattern:**
```sql
SELECT orders.id, customers.name, products.name
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN order_items ON orders.id = order_items.order_id
JOIN products ON order_items.product_id = products.id;
```

**Problems:**
- Verbose and hard to read
- Ambiguous column names
- Error-prone

**Correct:**
```sql
SELECT o.id, c.name AS customer_name, p.name AS product_name
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

---

### 20. Magic Numbers and Strings

**Anti-Pattern:**
```sql
SELECT * FROM orders WHERE status = 3;
SELECT * FROM users WHERE role = 'A';
```

**Problems:**
- Unclear meaning
- Hard to maintain
- Inconsistency risk

**Correct:**
```sql
-- Use descriptive values
SELECT * FROM orders WHERE status = 'shipped';
SELECT * FROM users WHERE role = 'admin';

-- Or create lookup tables
SELECT o.*
FROM orders o
JOIN order_statuses os ON o.status_id = os.id
WHERE os.name = 'shipped';
```

---

## Quick Reference Checklist

Before running any query, verify:

- [ ] No `SELECT *` - explicitly list columns
- [ ] No functions on indexed columns in WHERE
- [ ] No leading wildcards in LIKE
- [ ] Using EXISTS instead of IN for large subqueries
- [ ] Using parameterized queries (no string concatenation)
- [ ] Not exposing sensitive columns
- [ ] Using LIMIT during development
- [ ] Using explicit JOIN syntax
- [ ] Using meaningful table aliases
- [ ] Correct data types for comparisons
