# MySQL-Specific Migration Gotchas

Common MySQL pitfalls and surprises during schema migrations.

**Principle:** MySQL's migration behavior is not always intuitive. Understanding these gotchas prevents silent failures and data loss.

---

## Gotcha 1: CREATE TABLE IF NOT EXISTS Skips Schema Differences

### The Problem

```sql
-- Desired schema:
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    name VARCHAR(200),  -- Want 200 characters
    email VARCHAR(255)
);
```

**What happens:**
- Table doesn't exist → Creates table with schema above ✅
- Table exists with **exact schema above** → No-op (skip) ✅
- Table exists with **different schema** → **No-op (skip)** ❌

**Example Failure:**

```sql
-- Current state: users table exists
-- | id | name VARCHAR(100) | created_at |

-- Run migration:
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(255)
);

-- Expected: Alter table to match schema
-- Actual: SKIPS entirely (table exists, different or not)

-- Result:
-- | id | name VARCHAR(100) | created_at |
-- name still VARCHAR(100), email missing, created_at still there!
```

### The Fix

```sql
-- Create table only if missing
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY
);

-- Then add/modify columns conditionally
SET @col_email = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'email'
);
SET @sql = IF(@col_email = 0,
    'ALTER TABLE users ADD COLUMN email VARCHAR(255)',
    'SELECT "email exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Verify type
SET @col_type = (
    SELECT COLUMN_TYPE FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'name'
);
SET @sql = IF(@col_type != 'varchar(200)',
    'ALTER TABLE users MODIFY COLUMN name VARCHAR(200)',
    'SELECT "name already VARCHAR(200)"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
```

**Key Takeaway:** `CREATE TABLE IF NOT EXISTS` is useful only for creating NEW tables. For existing tables, use `ALTER TABLE`.

---

## Gotcha 2: ALTER TABLE MODIFY COLUMN Changes Type, Not Data

### The Problem

```sql
-- Current state:
-- users.status: VARCHAR(20) with values: 'active', 'inactive', 'pending', 'suspended'

-- Migration:
ALTER TABLE users MODIFY COLUMN status ENUM('active', 'inactive');

-- Expected: All rows converted to ENUM, invalid values rejected
-- Actual: Type changes BUT existing invalid data remains!

-- Result:
SELECT status FROM users WHERE id = 123;
-- Returns: 'pending' (still there, even though not in ENUM!)
```

### Why This Happens

MySQL's `MODIFY COLUMN` changes the **column definition** but doesn't revalidate existing rows. Old data persists in original format.

### The Fix

```sql
-- Step 1: Check existing data BEFORE changing type
SELECT DISTINCT status FROM users;

-- If incompatible values exist, migrate them first:
UPDATE users SET status = 'inactive' WHERE status NOT IN ('active', 'inactive');

-- Step 2: Verify all data is compatible
SELECT COUNT(*) FROM users WHERE status NOT IN ('active', 'inactive');
-- Must be 0!

-- Step 3: Now safe to change type
ALTER TABLE users MODIFY COLUMN status ENUM('active', 'inactive');

-- Step 4: Verify final state
DESCRIBE users;
SELECT DISTINCT status FROM users;
```

**Key Takeaway:** Always migrate DATA before changing column TYPE.

---

## Gotcha 3: ENUM Value Mismatch Fails Silently

### The Problem

```sql
-- Schema: status ENUM('pending', 'completed', 'failed')
INSERT INTO jobs (ticker, status) VALUES ('NVDA19', 'running');

-- Expected: Error (invalid ENUM value)
-- Actual: INSERT succeeds but affects 0 rows (silent failure!)

SELECT * FROM jobs WHERE ticker = 'NVDA19';
-- Returns: Empty set (data never inserted)
```

### Why This Happens

MySQL's `INSERT` with invalid ENUM value doesn't raise error in default mode. Row is silently rejected.

### The Fix

```python
# Pattern 1: Validate ENUM values in application code
VALID_STATUSES = {'pending', 'completed', 'failed'}

def create_job(ticker: str, status: str):
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}. Must be one of {VALID_STATUSES}")

    rowcount = db.execute(
        "INSERT INTO jobs (ticker, status) VALUES (%s, %s)",
        (ticker, status)
    )

    # Check operation outcome
    if rowcount == 0:
        logger.error(f"INSERT failed for {ticker} with status {status}")
        return False

    return True
```

```sql
-- Pattern 2: Enable strict SQL mode (rejects invalid ENUMs)
SET sql_mode = 'STRICT_ALL_TABLES';

INSERT INTO jobs (ticker, status) VALUES ('NVDA19', 'running');
-- Now raises: Data truncated for column 'status'
```

**Key Takeaway:** Always check `rowcount` after INSERT/UPDATE. Zero rows affected = silent failure.

---

## Gotcha 4: Foreign Key Type Mismatch Fails Silently

### The Problem

```sql
-- ticker_data.symbol: VARCHAR(20)
-- reports.ticker_symbol: VARCHAR(50)

ALTER TABLE reports ADD CONSTRAINT fk_reports_ticker
FOREIGN KEY (ticker_symbol) REFERENCES ticker_data(symbol);

-- Expected: Error (type mismatch)
-- Actual: Constraint created, but INSERT fails silently!

INSERT INTO reports (ticker_symbol, report_text) VALUES ('NVDA19', 'Analysis');
-- INSERT succeeds, but rowcount = 0 (silent failure)
```

### Why This Happens

MySQL allows FK with type mismatch (as long as base type is compatible). But lookups fail because comparison uses different lengths.

### The Fix

```sql
-- Step 1: Verify types BEFORE creating FK
SELECT
    c1.COLUMN_TYPE AS reports_type,
    c2.COLUMN_TYPE AS ticker_data_type
FROM information_schema.COLUMNS c1
JOIN information_schema.COLUMNS c2
WHERE c1.TABLE_NAME = 'reports' AND c1.COLUMN_NAME = 'ticker_symbol'
  AND c2.TABLE_NAME = 'ticker_data' AND c2.COLUMN_NAME = 'symbol';

-- Step 2: Fix type mismatch
ALTER TABLE reports MODIFY COLUMN ticker_symbol VARCHAR(20);

-- Step 3: Verify referential integrity
SELECT r.ticker_symbol
FROM reports r
LEFT JOIN ticker_data t ON r.ticker_symbol = t.symbol
WHERE t.symbol IS NULL;
-- Must return empty set!

-- Step 4: Now safe to create FK
ALTER TABLE reports ADD CONSTRAINT fk_reports_ticker
FOREIGN KEY (ticker_symbol) REFERENCES ticker_data(symbol);
```

**Key Takeaway:** FK columns must have **exact same type** (not just compatible base type).

---

## Gotcha 5: INDEX Name Collisions Across Tables

### The Problem

```sql
-- Table 1:
CREATE INDEX idx_created_at ON users(created_at);

-- Table 2:
CREATE INDEX idx_created_at ON reports(created_at);

-- Expected: Two indexes (different tables)
-- Actual: Error: "Duplicate key name 'idx_created_at'" (MySQL 5.x)
```

### Why This Happens

In older MySQL versions, index names are global across database (not scoped to table).

### The Fix

```sql
-- Use table prefix in index names
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_reports_created_at ON reports(created_at);

-- Or use table_column pattern
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_reports_created ON reports(created_at);
```

**Key Takeaway:** Always prefix index names with table name to avoid collisions.

---

## Gotcha 6: ALTER TABLE Locks Table (Blocking Writes)

### The Problem

```sql
-- Production database with 10M rows
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- Expected: Quick operation
-- Actual: Table locked for 30+ seconds, all writes blocked!
```

### Why This Happens

By default, `ALTER TABLE` uses `ALGORITHM=COPY` which:
1. Creates new table with new schema
2. Copies all rows from old table
3. Swaps tables

During this time, table is **write-locked**.

### The Fix

```sql
-- Use ALGORITHM=INPLACE (no table copy)
ALTER TABLE users ADD COLUMN email VARCHAR(255), ALGORITHM=INPLACE;

-- Check if operation supports INPLACE
-- Supported: ADD COLUMN, ADD INDEX (most cases)
-- Not supported: MODIFY COLUMN (type change), some charset changes

-- For unsupported operations, use online schema change tool
-- (e.g., gh-ost, pt-online-schema-change)
```

**Key Takeaway:** For large tables, always specify `ALGORITHM=INPLACE` to avoid table locks.

---

## Gotcha 7: DEFAULT CURRENT_TIMESTAMP on Non-TIMESTAMP Columns

### The Problem

```sql
-- Want: created_at with current timestamp
ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;

-- Expected: Works
-- Actual: Error in MySQL < 5.6.5
```

### Why This Happens

`CURRENT_TIMESTAMP` as default was only supported for DATETIME in MySQL 5.6.5+. Before that, only TIMESTAMP columns could use it.

### The Fix

```sql
-- MySQL 5.6.5+
ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;

-- MySQL < 5.6.5
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Or use trigger (works in all versions)
ALTER TABLE users ADD COLUMN created_at DATETIME;

DELIMITER $$
CREATE TRIGGER users_created_at_default
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF NEW.created_at IS NULL THEN
        SET NEW.created_at = NOW();
    END IF;
END$$
DELIMITER ;
```

**Key Takeaway:** Check MySQL version compatibility for DEFAULT expressions.

---

## Gotcha 8: Charset/Collation Mismatches

### The Problem

```sql
-- Table: utf8mb4_unicode_ci
-- Column: utf8_general_ci

SELECT * FROM users WHERE name = 'José';

-- Expected: Returns row
-- Actual: May not match due to collation difference
```

### Why This Happens

Different collations compare strings differently:
- `utf8_general_ci`: Fast, less accurate (ß = ss)
- `utf8mb4_unicode_ci`: Slower, more accurate
- `utf8mb4_bin`: Binary (case-sensitive)

### The Fix

```sql
-- Check current charsets/collations
SELECT
    TABLE_NAME,
    TABLE_COLLATION
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE();

SELECT
    COLUMN_NAME,
    CHARACTER_SET_NAME,
    COLLATION_NAME
FROM information_schema.COLUMNS
WHERE TABLE_NAME = 'users' AND CHARACTER_SET_NAME IS NOT NULL;

-- Standardize to utf8mb4_unicode_ci
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Or per-column
ALTER TABLE users MODIFY COLUMN name VARCHAR(100)
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Key Takeaway:** Use consistent charset/collation across all tables and columns (prefer `utf8mb4_unicode_ci`).

---

## Gotcha 9: AUTO_INCREMENT Reset on Truncate

### The Problem

```sql
-- Before:
SELECT MAX(id) FROM users;  -- Returns 1000

TRUNCATE TABLE users;

-- After:
INSERT INTO users (name) VALUES ('Alice');
SELECT id FROM users WHERE name = 'Alice';  -- Returns 1 (not 1001!)
```

### Why This Happens

`TRUNCATE` resets `AUTO_INCREMENT` counter. `DELETE` does not.

### The Fix

```sql
-- If you need to preserve AUTO_INCREMENT:
DELETE FROM users;  -- Slow for large tables
ALTER TABLE users AUTO_INCREMENT = 1001;  -- Reset manually

-- Or check current value before truncate:
SELECT AUTO_INCREMENT FROM information_schema.TABLES
WHERE TABLE_NAME = 'users';
-- Save value, then TRUNCATE, then restore:
ALTER TABLE users AUTO_INCREMENT = 1001;
```

**Key Takeaway:** Use `DELETE` if you need to preserve AUTO_INCREMENT sequence.

---

## Gotcha 10: JSON Column Type Differences (MySQL 5.7 vs 8.0)

### The Problem

```python
# MySQL 5.7: JSON stored as TEXT
# MySQL 8.0: JSON is native type

# Code that worked in 5.7:
db.execute("INSERT INTO reports (data) VALUES (%s)", (json.dumps(data),))

# MySQL 8.0: Might need:
db.execute("INSERT INTO reports (data) VALUES (%s)", (json.dumps(data),))
# Or:
db.execute("INSERT INTO reports (data) VALUES (CAST(%s AS JSON))", (json.dumps(data),))
```

### The Fix

```python
# Universal pattern (works in both versions)
import json

def store_json_column(data: dict):
    # Always serialize to string
    json_string = json.dumps(data)

    # Let MySQL handle type conversion
    db.execute(
        "INSERT INTO reports (data) VALUES (%s)",
        (json_string,)
    )
```

**Key Takeaway:** Always pass JSON as string to database. Let MySQL convert to native JSON type.

---

## Quick Reference

### Silent Failure Checklist

After running migration, always verify:

```sql
-- 1. Check table exists
SHOW TABLES LIKE 'users';

-- 2. Check all columns exist
DESCRIBE users;

-- 3. Check column types match
SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT
FROM information_schema.COLUMNS
WHERE TABLE_NAME = 'users'
ORDER BY ORDINAL_POSITION;

-- 4. Check indexes exist
SHOW INDEX FROM users;

-- 5. Check foreign keys exist
SELECT
    CONSTRAINT_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'users'
  AND REFERENCED_TABLE_NAME IS NOT NULL;

-- 6. Check charset/collation
SELECT TABLE_COLLATION FROM information_schema.TABLES WHERE TABLE_NAME = 'users';
```

### Common Migration Failures

| Operation | Failure Mode | Detection |
|-----------|--------------|-----------|
| **CREATE TABLE IF NOT EXISTS** | Skips on schema mismatch | Check DESCRIBE output |
| **MODIFY COLUMN** | Type changes, data doesn't | Query distinct values |
| **INSERT with invalid ENUM** | Rowcount = 0 | Check rowcount after INSERT |
| **FK type mismatch** | Constraint exists, INSERT fails | Verify FK column types match |
| **ADD COLUMN (large table)** | Table locked | Use ALGORITHM=INPLACE |
| **Charset mismatch** | Query doesn't match | Check collations match |

### Safe Migration Pattern

```sql
-- 1. Start transaction (rollback on failure)
START TRANSACTION;

-- 2. Run migration with verification
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- 3. Verify result
SELECT COUNT(*) INTO @col_count
FROM information_schema.COLUMNS
WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'email';

-- 4. Rollback if verification fails
IF @col_count = 0 THEN
    ROLLBACK;
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Migration failed';
ELSE
    COMMIT;
END IF;
```

---

## Troubleshooting Guide

### "Duplicate key name" Error

**Cause:** Index name already exists (possibly on different table in MySQL < 5.7).

**Fix:** Prefix index names with table name: `idx_users_email` instead of `idx_email`.

---

### "Data truncated for column" Error

**Cause:** Existing data doesn't fit new type/ENUM values.

**Fix:**
```sql
-- Check existing data
SELECT DISTINCT column_name FROM table_name;

-- Migrate incompatible values
UPDATE table_name SET column_name = 'new_value'
WHERE column_name NOT IN ('valid1', 'valid2');

-- Then change type
ALTER TABLE table_name MODIFY COLUMN column_name ENUM('valid1', 'valid2');
```

---

### "Cannot add foreign key constraint" Error

**Cause:** Referential integrity violation or type mismatch.

**Fix:**
```sql
-- Check orphaned rows
SELECT t1.id
FROM child_table t1
LEFT JOIN parent_table t2 ON t1.parent_id = t2.id
WHERE t2.id IS NULL;

-- Delete orphans
DELETE FROM child_table WHERE parent_id NOT IN (SELECT id FROM parent_table);

-- Verify types match
SELECT
    c1.COLUMN_TYPE AS child_type,
    c2.COLUMN_TYPE AS parent_type
FROM information_schema.COLUMNS c1, information_schema.COLUMNS c2
WHERE c1.TABLE_NAME = 'child_table' AND c1.COLUMN_NAME = 'parent_id'
  AND c2.TABLE_NAME = 'parent_table' AND c2.COLUMN_NAME = 'id';
```

---

## References

- [MySQL ALTER TABLE Documentation](https://dev.mysql.com/doc/refman/8.0/en/alter-table.html)
- [MySQL Online DDL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl.html)
- [Common MySQL Gotchas](https://stackoverflow.com/questions/tagged/mysql+migration)
