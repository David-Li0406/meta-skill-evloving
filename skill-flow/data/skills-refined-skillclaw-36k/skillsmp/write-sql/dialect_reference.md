# SQL Dialect Reference

This guide covers syntax differences between major SQL databases: SQLite, PostgreSQL, MySQL, and SQL Server.

## Table of Contents

1. [Data Types](#data-types)
2. [String Operations](#string-operations)
3. [Date and Time](#date-and-time)
4. [Limiting Results](#limiting-results)
5. [Auto-Increment](#auto-increment)
6. [Boolean Values](#boolean-values)
7. [NULL Handling](#null-handling)
8. [Conditional Logic](#conditional-logic)
9. [String Functions](#string-functions)
10. [Aggregate Functions](#aggregate-functions)
11. [Window Functions](#window-functions)
12. [JSON Support](#json-support)
13. [Table Operations](#table-operations)
14. [Upsert (Insert or Update)](#upsert-insert-or-update)

---

## Data Types

| Type | SQLite | PostgreSQL | MySQL | SQL Server |
|------|--------|------------|-------|------------|
| Integer | `INTEGER` | `INTEGER`, `BIGINT` | `INT`, `BIGINT` | `INT`, `BIGINT` |
| Decimal | `REAL` | `DECIMAL(p,s)`, `NUMERIC` | `DECIMAL(p,s)` | `DECIMAL(p,s)` |
| Float | `REAL` | `REAL`, `DOUBLE PRECISION` | `FLOAT`, `DOUBLE` | `FLOAT`, `REAL` |
| String | `TEXT` | `VARCHAR(n)`, `TEXT` | `VARCHAR(n)`, `TEXT` | `VARCHAR(n)`, `NVARCHAR(n)` |
| Boolean | `INTEGER` (0/1) | `BOOLEAN` | `TINYINT(1)`, `BOOLEAN` | `BIT` |
| Date | `TEXT` | `DATE` | `DATE` | `DATE` |
| Datetime | `TEXT` | `TIMESTAMP` | `DATETIME` | `DATETIME2` |
| Binary | `BLOB` | `BYTEA` | `BLOB` | `VARBINARY(MAX)` |
| UUID | `TEXT` | `UUID` | `CHAR(36)` | `UNIQUEIDENTIFIER` |
| JSON | `TEXT` | `JSON`, `JSONB` | `JSON` | `NVARCHAR(MAX)` |

---

## String Operations

### Concatenation

```sql
-- SQLite
SELECT first_name || ' ' || last_name AS full_name FROM users;

-- PostgreSQL
SELECT first_name || ' ' || last_name AS full_name FROM users;
-- Or
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;

-- MySQL
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;

-- SQL Server
SELECT first_name + ' ' + last_name AS full_name FROM users;
-- Or
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users;
```

### String Length

```sql
-- SQLite
SELECT LENGTH(name) FROM users;

-- PostgreSQL
SELECT LENGTH(name) FROM users;
SELECT CHAR_LENGTH(name) FROM users;

-- MySQL
SELECT LENGTH(name) FROM users;      -- Bytes
SELECT CHAR_LENGTH(name) FROM users; -- Characters

-- SQL Server
SELECT LEN(name) FROM users;         -- Excludes trailing spaces
SELECT DATALENGTH(name) FROM users;  -- Bytes
```

### Substring

```sql
-- SQLite
SELECT SUBSTR(name, 1, 3) FROM users;

-- PostgreSQL
SELECT SUBSTRING(name FROM 1 FOR 3) FROM users;
SELECT SUBSTR(name, 1, 3) FROM users;

-- MySQL
SELECT SUBSTRING(name, 1, 3) FROM users;
SELECT SUBSTR(name, 1, 3) FROM users;

-- SQL Server
SELECT SUBSTRING(name, 1, 3) FROM users;
```

---

## Date and Time

### Current Date/Time

```sql
-- SQLite
SELECT DATE('now');                    -- Current date
SELECT TIME('now');                    -- Current time
SELECT DATETIME('now');                -- Current datetime
SELECT DATETIME('now', 'localtime');   -- Local time

-- PostgreSQL
SELECT CURRENT_DATE;                   -- Current date
SELECT CURRENT_TIME;                   -- Current time
SELECT CURRENT_TIMESTAMP;              -- Current datetime
SELECT NOW();                          -- Current datetime with timezone

-- MySQL
SELECT CURDATE();                      -- Current date
SELECT CURTIME();                      -- Current time
SELECT NOW();                          -- Current datetime
SELECT CURRENT_TIMESTAMP;              -- Current datetime

-- SQL Server
SELECT GETDATE();                      -- Current datetime
SELECT GETUTCDATE();                   -- UTC datetime
SELECT SYSDATETIME();                  -- High precision datetime
SELECT CAST(GETDATE() AS DATE);        -- Current date only
```

### Date Extraction

```sql
-- SQLite
SELECT strftime('%Y', order_date) AS year FROM orders;
SELECT strftime('%m', order_date) AS month FROM orders;
SELECT strftime('%d', order_date) AS day FROM orders;
SELECT strftime('%W', order_date) AS week FROM orders;

-- PostgreSQL
SELECT EXTRACT(YEAR FROM order_date) AS year FROM orders;
SELECT EXTRACT(MONTH FROM order_date) AS month FROM orders;
SELECT EXTRACT(DAY FROM order_date) AS day FROM orders;
SELECT DATE_PART('week', order_date) AS week FROM orders;

-- MySQL
SELECT YEAR(order_date) AS year FROM orders;
SELECT MONTH(order_date) AS month FROM orders;
SELECT DAY(order_date) AS day FROM orders;
SELECT WEEK(order_date) AS week FROM orders;

-- SQL Server
SELECT YEAR(order_date) AS year FROM orders;
SELECT MONTH(order_date) AS month FROM orders;
SELECT DAY(order_date) AS day FROM orders;
SELECT DATEPART(WEEK, order_date) AS week FROM orders;
```

### Date Arithmetic

```sql
-- SQLite
SELECT DATE('now', '+7 days');         -- Add 7 days
SELECT DATE('now', '-1 month');        -- Subtract 1 month
SELECT DATE('now', 'start of month');  -- First of month

-- PostgreSQL
SELECT CURRENT_DATE + INTERVAL '7 days';
SELECT CURRENT_DATE - INTERVAL '1 month';
SELECT DATE_TRUNC('month', CURRENT_DATE);

-- MySQL
SELECT DATE_ADD(CURDATE(), INTERVAL 7 DAY);
SELECT DATE_SUB(CURDATE(), INTERVAL 1 MONTH);
SELECT DATE_FORMAT(CURDATE(), '%Y-%m-01');

-- SQL Server
SELECT DATEADD(DAY, 7, GETDATE());
SELECT DATEADD(MONTH, -1, GETDATE());
SELECT DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1);
```

### Date Difference

```sql
-- SQLite
SELECT JULIANDAY('2024-12-31') - JULIANDAY('2024-01-01') AS days;

-- PostgreSQL
SELECT '2024-12-31'::DATE - '2024-01-01'::DATE AS days;
SELECT AGE('2024-12-31', '2024-01-01');

-- MySQL
SELECT DATEDIFF('2024-12-31', '2024-01-01') AS days;
SELECT TIMESTAMPDIFF(DAY, '2024-01-01', '2024-12-31') AS days;

-- SQL Server
SELECT DATEDIFF(DAY, '2024-01-01', '2024-12-31') AS days;
```

---

## Limiting Results

```sql
-- SQLite
SELECT * FROM users LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;

-- PostgreSQL
SELECT * FROM users LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;
SELECT * FROM users FETCH FIRST 10 ROWS ONLY;  -- SQL standard

-- MySQL
SELECT * FROM users LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;
SELECT * FROM users LIMIT 20, 10;  -- offset, count (reversed!)

-- SQL Server
SELECT TOP 10 * FROM users;
SELECT * FROM users ORDER BY id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```

---

## Auto-Increment

```sql
-- SQLite
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,          -- 4-byte integer
    name VARCHAR(100)
);
-- Or with GENERATED:
CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);

-- MySQL
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

-- SQL Server
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100)
);
```

### Getting Last Inserted ID

```sql
-- SQLite
SELECT last_insert_rowid();

-- PostgreSQL
INSERT INTO users (name) VALUES ('John') RETURNING id;
-- Or
SELECT currval('users_id_seq');

-- MySQL
SELECT LAST_INSERT_ID();

-- SQL Server
SELECT SCOPE_IDENTITY();
SELECT @@IDENTITY;  -- Less safe, includes triggers
```

---

## Boolean Values

```sql
-- SQLite (uses 0 and 1)
SELECT * FROM users WHERE active = 1;
SELECT * FROM users WHERE active = 0;

-- PostgreSQL
SELECT * FROM users WHERE active = TRUE;
SELECT * FROM users WHERE active = FALSE;
SELECT * FROM users WHERE active;  -- Implicit TRUE

-- MySQL
SELECT * FROM users WHERE active = TRUE;
SELECT * FROM users WHERE active = 1;

-- SQL Server (uses BIT)
SELECT * FROM users WHERE active = 1;
SELECT * FROM users WHERE active = 0;
```

---

## NULL Handling

### COALESCE (All Dialects)

```sql
-- Works in all dialects
SELECT COALESCE(phone, email, 'No contact') FROM users;
```

### IFNULL / NVL / ISNULL

```sql
-- SQLite
SELECT IFNULL(phone, 'N/A') FROM users;

-- PostgreSQL
SELECT COALESCE(phone, 'N/A') FROM users;

-- MySQL
SELECT IFNULL(phone, 'N/A') FROM users;
SELECT COALESCE(phone, 'N/A') FROM users;

-- SQL Server
SELECT ISNULL(phone, 'N/A') FROM users;
SELECT COALESCE(phone, 'N/A') FROM users;
```

### NULLIF (All Dialects)

```sql
-- Works in all dialects - returns NULL if values are equal
SELECT value / NULLIF(divisor, 0) FROM numbers;  -- Prevents division by zero
```

---

## Conditional Logic

### CASE Expression (All Dialects)

```sql
-- Standard CASE works in all dialects
SELECT
    name,
    CASE
        WHEN score >= 90 THEN 'A'
        WHEN score >= 80 THEN 'B'
        WHEN score >= 70 THEN 'C'
        ELSE 'F'
    END AS grade
FROM students;
```

### IIF (SQL Server, SQLite 3.32+)

```sql
-- SQLite (3.32+) and SQL Server
SELECT IIF(score >= 60, 'Pass', 'Fail') FROM students;

-- Equivalent in all dialects
SELECT CASE WHEN score >= 60 THEN 'Pass' ELSE 'Fail' END FROM students;
```

### IF Function (MySQL Only)

```sql
-- MySQL only
SELECT IF(score >= 60, 'Pass', 'Fail') FROM students;
```

---

## String Functions

| Function | SQLite | PostgreSQL | MySQL | SQL Server |
|----------|--------|------------|-------|------------|
| Upper | `UPPER(s)` | `UPPER(s)` | `UPPER(s)` | `UPPER(s)` |
| Lower | `LOWER(s)` | `LOWER(s)` | `LOWER(s)` | `LOWER(s)` |
| Trim | `TRIM(s)` | `TRIM(s)` | `TRIM(s)` | `TRIM(s)` or `LTRIM(RTRIM(s))` |
| Left | `SUBSTR(s,1,n)` | `LEFT(s,n)` | `LEFT(s,n)` | `LEFT(s,n)` |
| Right | `SUBSTR(s,-n)` | `RIGHT(s,n)` | `RIGHT(s,n)` | `RIGHT(s,n)` |
| Replace | `REPLACE(s,a,b)` | `REPLACE(s,a,b)` | `REPLACE(s,a,b)` | `REPLACE(s,a,b)` |
| Position | `INSTR(s,sub)` | `POSITION(sub IN s)` | `LOCATE(sub,s)` | `CHARINDEX(sub,s)` |
| Reverse | N/A | `REVERSE(s)` | `REVERSE(s)` | `REVERSE(s)` |
| Repeat | N/A | `REPEAT(s,n)` | `REPEAT(s,n)` | `REPLICATE(s,n)` |

---

## Aggregate Functions

### String Aggregation

```sql
-- SQLite
SELECT GROUP_CONCAT(name, ', ') FROM users GROUP BY department;

-- PostgreSQL
SELECT STRING_AGG(name, ', ') FROM users GROUP BY department;
SELECT STRING_AGG(name, ', ' ORDER BY name) FROM users GROUP BY department;

-- MySQL
SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM users GROUP BY department;
SELECT GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') FROM users GROUP BY department;

-- SQL Server
SELECT STRING_AGG(name, ', ') FROM users GROUP BY department;
SELECT STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name) FROM users GROUP BY department;
```

### Distinct Count

```sql
-- Works in all dialects
SELECT COUNT(DISTINCT category) FROM products;
```

---

## Window Functions

### Basic Window Functions (All Dialects)

```sql
-- ROW_NUMBER, RANK, DENSE_RANK work in all modern dialects
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank
FROM employees;
```

### LAG and LEAD

```sql
-- Works in all modern dialects
SELECT
    order_date,
    total,
    LAG(total, 1) OVER (ORDER BY order_date) AS prev_total,
    LEAD(total, 1) OVER (ORDER BY order_date) AS next_total
FROM orders;
```

### Frame Specification

```sql
-- Running total (all dialects)
SELECT
    order_date,
    total,
    SUM(total) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS running_total
FROM orders;

-- Moving average
SELECT
    order_date,
    total,
    AVG(total) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg
FROM orders;
```

---

## JSON Support

### Extracting JSON Values

```sql
-- SQLite (3.38+)
SELECT json_extract(data, '$.name') FROM users;
SELECT data->>'$.name' FROM users;  -- As text

-- PostgreSQL
SELECT data->'name' FROM users;      -- As JSON
SELECT data->>'name' FROM users;     -- As text
SELECT data #> '{nested,key}' FROM users;  -- Nested path

-- MySQL
SELECT JSON_EXTRACT(data, '$.name') FROM users;
SELECT data->'$.name' FROM users;
SELECT JSON_UNQUOTE(data->'$.name') FROM users;  -- As text

-- SQL Server
SELECT JSON_VALUE(data, '$.name') FROM users;    -- Scalar value
SELECT JSON_QUERY(data, '$.address') FROM users; -- Object/array
```

### JSON Array Operations

```sql
-- SQLite
SELECT json_array_length(data, '$.items') FROM orders;

-- PostgreSQL
SELECT jsonb_array_length(data->'items') FROM orders;
SELECT jsonb_array_elements(data->'items') FROM orders;  -- Unnest

-- MySQL
SELECT JSON_LENGTH(data, '$.items') FROM orders;
SELECT JSON_TABLE(...) -- Complex extraction

-- SQL Server
SELECT JSON_VALUE(data, '$.items') FROM orders;
CROSS APPLY OPENJSON(data, '$.items')  -- Unnest
```

---

## Table Operations

### Check If Table Exists

```sql
-- SQLite
SELECT name FROM sqlite_master WHERE type='table' AND name='users';

-- PostgreSQL
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'users'
);

-- MySQL
SELECT EXISTS (
    SELECT * FROM information_schema.tables
    WHERE table_name = 'users'
);

-- SQL Server
SELECT OBJECT_ID('users', 'U') IS NOT NULL;
```

### Rename Table

```sql
-- SQLite
ALTER TABLE old_name RENAME TO new_name;

-- PostgreSQL
ALTER TABLE old_name RENAME TO new_name;

-- MySQL
RENAME TABLE old_name TO new_name;
-- Or
ALTER TABLE old_name RENAME new_name;

-- SQL Server
EXEC sp_rename 'old_name', 'new_name';
```

### Add Column

```sql
-- SQLite (limited - no DEFAULT with expressions)
ALTER TABLE users ADD COLUMN email TEXT;

-- PostgreSQL
ALTER TABLE users ADD COLUMN email VARCHAR(255) DEFAULT 'unknown';

-- MySQL
ALTER TABLE users ADD COLUMN email VARCHAR(255) DEFAULT 'unknown';

-- SQL Server
ALTER TABLE users ADD email VARCHAR(255) DEFAULT 'unknown';
```

---

## Upsert (Insert or Update)

```sql
-- SQLite
INSERT INTO users (id, name, email) VALUES (1, 'John', 'john@example.com')
ON CONFLICT(id) DO UPDATE SET name = excluded.name, email = excluded.email;

-- PostgreSQL
INSERT INTO users (id, name, email) VALUES (1, 'John', 'john@example.com')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, email = EXCLUDED.email;

-- MySQL
INSERT INTO users (id, name, email) VALUES (1, 'John', 'john@example.com')
ON DUPLICATE KEY UPDATE name = VALUES(name), email = VALUES(email);

-- SQL Server
MERGE INTO users AS target
USING (VALUES (1, 'John', 'john@example.com')) AS source (id, name, email)
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET name = source.name, email = source.email
WHEN NOT MATCHED THEN INSERT (id, name, email) VALUES (source.id, source.name, source.email);
```

---

## Quick Dialect Detection

To identify which database you're connected to:

```sql
-- SQLite
SELECT sqlite_version();

-- PostgreSQL
SELECT version();

-- MySQL
SELECT VERSION();

-- SQL Server
SELECT @@VERSION;
```
