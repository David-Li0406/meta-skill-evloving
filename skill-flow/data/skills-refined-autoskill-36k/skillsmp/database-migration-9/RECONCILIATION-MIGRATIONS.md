# Reconciliation Migration Patterns

Idempotent migration patterns for unknown database states.

**Principle:** Reconciliation migrations use conditional logic to transition from **any intermediate state** to the desired schema without destructive operations.

---

## Why Reconciliation Migrations?

**Traditional Sequential Migrations:**
```sql
-- Assumes clean state
ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

**Problems:**
- If column already exists → Error: "Duplicate column name"
- If migration runs twice → Failure
- If someone manually added column → Conflict

**Reconciliation Solution:**
```sql
-- Works regardless of current state
SET @col_exists = (SELECT COUNT(*) FROM information_schema.COLUMNS
                   WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'email');
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN email VARCHAR(255)',
    'SELECT "Already exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
```

**Benefits:**
- ✅ Idempotent (can run multiple times)
- ✅ Handles partial migrations
- ✅ Recovers from failures
- ✅ Reconciles schema drift

---

## Pattern 1: Conditional Column Creation

### Basic Pattern

```sql
-- Check if column exists
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'email'
);

-- Add column only if missing
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN email VARCHAR(255)',
    'SELECT "Column email already exists" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

### With Default Value

```sql
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'created_at'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'SELECT "Column created_at already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

### With NOT NULL Constraint

```sql
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'status'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN status ENUM("active", "inactive") NOT NULL DEFAULT "active"',
    'SELECT "Column status already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

---

## Pattern 2: Conditional Index Creation

### Single Column Index

```sql
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND INDEX_NAME = 'idx_email'
);

SET @sql = IF(@idx_exists = 0,
    'CREATE INDEX idx_email ON users(email)',
    'SELECT "Index idx_email already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

### Composite Index

```sql
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND INDEX_NAME = 'idx_user_lookup'
);

SET @sql = IF(@idx_exists = 0,
    'CREATE INDEX idx_user_lookup ON users(email, status)',
    'SELECT "Index idx_user_lookup already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

### Unique Index

```sql
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND INDEX_NAME = 'idx_email_unique'
);

SET @sql = IF(@idx_exists = 0,
    'CREATE UNIQUE INDEX idx_email_unique ON users(email)',
    'SELECT "Unique index idx_email_unique already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

---

## Pattern 3: Conditional Column Modification

### Change Column Type

```sql
-- Get current column type
SET @current_type = (
    SELECT COLUMN_TYPE
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'name'
);

-- Modify only if type is different
SET @sql = IF(@current_type != 'varchar(200)',
    'ALTER TABLE users MODIFY COLUMN name VARCHAR(200)',
    'SELECT "Column name already VARCHAR(200)"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- CRITICAL: Verify existing data fits new type
SELECT name FROM users WHERE LENGTH(name) > 200;
-- If any rows returned, migration will truncate data!
```

### Change NULL Constraint

```sql
-- Get current NULL constraint
SET @is_nullable = (
    SELECT IS_NULLABLE
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'email'
);

-- Modify only if currently NULL
SET @sql = IF(@is_nullable = 'YES',
    'ALTER TABLE users MODIFY COLUMN email VARCHAR(255) NOT NULL',
    'SELECT "Column email already NOT NULL"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- CRITICAL: Verify no NULL values exist
SELECT COUNT(*) FROM users WHERE email IS NULL;
-- If count > 0, migration will fail!
```

### Change Default Value

```sql
-- Get current default
SET @current_default = (
    SELECT COLUMN_DEFAULT
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
      AND COLUMN_NAME = 'status'
);

-- Modify only if default is different
SET @sql = IF(@current_default != 'active',
    'ALTER TABLE users ALTER COLUMN status SET DEFAULT "active"',
    'SELECT "Column status default already active"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

---

## Pattern 4: Conditional Foreign Key Creation

```sql
-- Check if FK exists
SET @fk_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'reports'
      AND CONSTRAINT_NAME = 'fk_reports_ticker'
      AND CONSTRAINT_TYPE = 'FOREIGN KEY'
);

-- Add FK only if missing
SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE reports ADD CONSTRAINT fk_reports_ticker FOREIGN KEY (ticker_symbol) REFERENCES ticker_data(symbol)',
    'SELECT "FK fk_reports_ticker already exists"'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- CRITICAL: Verify referential integrity BEFORE adding FK
SELECT r.ticker_symbol
FROM reports r
LEFT JOIN ticker_data t ON r.ticker_symbol = t.symbol
WHERE t.symbol IS NULL;
-- If any rows returned, FK creation will fail!
```

---

## Pattern 5: Conditional Table Creation

```sql
-- Create table only if doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ⚠️ GOTCHA: If table exists with different schema, this does NOTHING
-- To add missing columns to existing table:

-- Check table exists
SET @table_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'users'
);

-- Create if missing
SET @create_table = IF(@table_exists = 0,
    'CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100))',
    'SELECT "Table users already exists"'
);

PREPARE stmt FROM @create_table;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Then add columns conditionally (see Pattern 1)
```

---

## Pattern 6: Complete Table Reconciliation

**Scenario:** Ensure table has correct schema regardless of current state.

```sql
-- migrations/RECONCILE_users_table.sql

-- Step 1: Ensure table exists
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY
);

-- Step 2: Add name column if missing
SET @col_name = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'name'
);
SET @sql = IF(@col_name = 0,
    'ALTER TABLE users ADD COLUMN name VARCHAR(100)',
    'SELECT "name exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 3: Add email column if missing
SET @col_email = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'email'
);
SET @sql = IF(@col_email = 0,
    'ALTER TABLE users ADD COLUMN email VARCHAR(255)',
    'SELECT "email exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 4: Add status column if missing
SET @col_status = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'status'
);
SET @sql = IF(@col_status = 0,
    'ALTER TABLE users ADD COLUMN status ENUM("active", "inactive") DEFAULT "active"',
    'SELECT "status exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 5: Add email index if missing
SET @idx_email = (
    SELECT COUNT(*) FROM information_schema.STATISTICS
    WHERE TABLE_NAME = 'users' AND INDEX_NAME = 'idx_email'
);
SET @sql = IF(@idx_email = 0,
    'CREATE INDEX idx_email ON users(email)',
    'SELECT "idx_email exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 6: Verify final schema
SELECT
    COLUMN_NAME,
    COLUMN_TYPE,
    IS_NULLABLE,
    COLUMN_DEFAULT
FROM information_schema.COLUMNS
WHERE TABLE_NAME = 'users'
ORDER BY ORDINAL_POSITION;
```

---

## Pattern 7: Data Migration Within Reconciliation

**Scenario:** Add column with values derived from existing data.

```sql
-- Add full_name column combining first_name + last_name

-- Step 1: Add column if missing
SET @col_exists = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'full_name'
);
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN full_name VARCHAR(200)',
    'SELECT "full_name exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 2: Populate data (only if column was just added)
-- Check if column is empty
SET @rows_populated = (SELECT COUNT(*) FROM users WHERE full_name IS NOT NULL);

-- Populate if empty
UPDATE users
SET full_name = CONCAT(first_name, ' ', last_name)
WHERE full_name IS NULL AND @rows_populated = 0;

-- Step 3: Verify
SELECT first_name, last_name, full_name FROM users LIMIT 5;
```

---

## Pattern 8: Rollback-Safe Migrations

**Scenario:** Migration that can be rolled back if it fails.

```sql
START TRANSACTION;

-- Step 1: Add column
SET @col_exists = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'email'
);
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE users ADD COLUMN email VARCHAR(255)',
    'SELECT "email exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 2: Verify schema
SELECT COUNT(*) INTO @col_count
FROM information_schema.COLUMNS
WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'email';

-- Step 3: Rollback if verification fails
IF @col_count = 0 THEN
    ROLLBACK;
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Migration failed: email column not added';
ELSE
    COMMIT;
END IF;
```

---

## Real-World Example: Fixing Broken Migration

**Scenario:** Migration 005 failed halfway through. Database in unknown state.

```sql
-- migrations/RECONCILE_005_fix_broken_migration.sql
-- Fixes: 005_add_user_preferences.sql (failed mid-execution)

-- Original migration attempted to:
-- 1. Add preferences table
-- 2. Add user_id FK to preferences
-- 3. Add index on preferences.user_id

-- Check current state and fix

-- Step 1: Ensure preferences table exists
CREATE TABLE IF NOT EXISTS preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT
);

-- Step 2: Add user_id column if missing (might exist from partial run)
SET @col_exists = (
    SELECT COUNT(*) FROM information_schema.COLUMNS
    WHERE TABLE_NAME = 'preferences' AND COLUMN_NAME = 'user_id'
);
SET @sql = IF(@col_exists = 0,
    'ALTER TABLE preferences ADD COLUMN user_id INT',
    'SELECT "user_id exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 3: Add FK if missing
SET @fk_exists = (
    SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS
    WHERE TABLE_NAME = 'preferences'
      AND CONSTRAINT_NAME = 'fk_preferences_user'
);
SET @sql = IF(@fk_exists = 0,
    'ALTER TABLE preferences ADD CONSTRAINT fk_preferences_user FOREIGN KEY (user_id) REFERENCES users(id)',
    'SELECT "FK exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 4: Add index if missing
SET @idx_exists = (
    SELECT COUNT(*) FROM information_schema.STATISTICS
    WHERE TABLE_NAME = 'preferences' AND INDEX_NAME = 'idx_user_id'
);
SET @sql = IF(@idx_exists = 0,
    'CREATE INDEX idx_user_id ON preferences(user_id)',
    'SELECT "idx_user_id exists"');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Step 5: Verify final state
DESCRIBE preferences;
SHOW INDEX FROM preferences;
```

---

## Testing Reconciliation Migrations

```python
def test_reconciliation_migration_handles_all_states():
    """Test migration works from any intermediate state"""

    # State 1: Clean database (no table)
    run_migration('RECONCILE_users_table.sql')
    assert table_exists('users')
    assert column_exists('users', 'email')

    # State 2: Table exists, missing column
    drop_column('users', 'email')
    run_migration('RECONCILE_users_table.sql')  # Should add column
    assert column_exists('users', 'email')

    # State 3: Everything exists
    run_migration('RECONCILE_users_table.sql')  # Should not error
    assert column_exists('users', 'email')

    # State 4: Table exists with different schema
    modify_column('users', 'email', 'VARCHAR(100)')
    run_migration('RECONCILE_users_table.sql')  # Should fix type
    assert get_column_type('users', 'email') == 'VARCHAR(255)'
```

---

## Quick Reference

### When to Use Reconciliation

| Scenario | Use Reconciliation? | Why |
|----------|---------------------|-----|
| **Production deployment** | ✅ Always | Unknown state |
| **Clean dev environment** | ❌ Sequential OK | Known clean state |
| **Fixing failed migration** | ✅ Always | Partial state |
| **Schema drift detected** | ✅ Always | Out of sync |
| **Multi-environment sync** | ✅ Always | Different states |

### Reconciliation Checklist

Before deploying reconciliation migration:
- [ ] Tests all possible states (no table, partial schema, full schema)
- [ ] Checks existing data compatibility (not just schema)
- [ ] Verifies final state (DESCRIBE, SHOW INDEX)
- [ ] Can run multiple times without errors (true idempotency)
- [ ] Logs what actions it takes (for debugging)

---

## References

- [Evolutionary Database Design (Martin Fowler)](https://www.martinfowler.com/articles/evodb.html)
- [Blue-Green Database Deployments](https://www.braintreepayments.com/blog/safe-database-migrations/)
- [Online Schema Changes (GitHub gh-ost)](https://github.com/github/gh-ost)
