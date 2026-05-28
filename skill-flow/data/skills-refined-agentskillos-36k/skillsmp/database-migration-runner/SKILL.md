---
name: database-migration-runner
description: Safely manage database schema changes for Budget Buddy including listing pending migrations, backing up database, executing migrations sequentially, and providing rollback support. Use when migrating database, changing schema, adding tables/columns, or when the user asks to run migrations.
allowed-tools: [Bash(python*), Bash(sqlite3:*), Bash(cp:*), Bash(ls:*), Read, Grep, Glob]
---

# Database Migration Runner

## Overview

This skill helps you safely execute database migrations for Budget Buddy's SQLite database. It ensures backups are created, migrations run in correct order, and provides rollback capabilities if something goes wrong.

## Prerequisites

- SQLite database exists: `budget_buddy.db`
- Backend dependencies installed
- Working directory: `/Users/franklindickinson/Projects/budget-buddy-2`

## Quick Start

### Step 1: List Pending Migrations

```bash
ls -1 backend/database/migrations/*.py backend/database/migrations/*.sql 2>/dev/null | sort
```

Migrations are in `/backend/database/migrations/` as `.py` or `.sql` files.

### Step 2: Backup Database

**CRITICAL**: Always backup before running migrations!

```bash
cp budget_buddy.db budget_buddy.db.backup.$(date +%Y%m%d_%H%M%S)
```

Verify backup:
```bash
ls -lh budget_buddy.db.backup.*
```

### Step 3: Review Migration Content

Before executing, understand what the migration does:

**For Python migrations**:
```bash
cat backend/database/migrations/add_buddy_insights.py
```

**For SQL migrations**:
```bash
cat backend/database/migrations/create_buddy_insights_tables.sql
```

### Step 4: Execute Migration

**Python Migration**:
```bash
python backend/database/migrations/add_buddy_insights.py
```

**SQL Migration** (using SQLite):
```bash
sqlite3 budget_buddy.db < backend/database/migrations/create_buddy_insights_tables.sql
```

**SQL Migration** (using Python):
```bash
python -c "
import sqlite3
conn = sqlite3.connect('budget_buddy.db')
with open('backend/database/migrations/create_buddy_insights_tables.sql', 'r') as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
print('Migration executed successfully')
"
```

### Step 5: Verify Migration

```bash
sqlite3 budget_buddy.db ".schema" | grep -i "new_table_name"
```

Or check table exists:
```bash
sqlite3 budget_buddy.db ".tables"
```

### Step 6: Test Application

```bash
# Start backend
python -m uvicorn backend.api.main:app --reload --port 8000

# Test endpoint that uses new schema
curl http://127.0.0.1:8000/api/v2/diagnostics
```

## Key Validation Points

### Before Migration
- ✅ Database backup created
- ✅ Migration file reviewed and understood
- ✅ No active connections to database (stop backend)
- ✅ Sufficient disk space for backup

### During Migration
- ✅ No syntax errors in SQL/Python
- ✅ Foreign key constraints respected
- ✅ Data types compatible
- ✅ No data loss

### After Migration
- ✅ Tables/columns created successfully
- ✅ Existing data preserved
- ✅ Application starts without errors
- ✅ All API endpoints functional

## Common Issues & Solutions

### Issue: "database is locked"

**Cause**: Backend or another process has open connection

**Solution**:
```bash
# Stop backend
pkill -f "uvicorn.*8000"

# Wait a moment
sleep 2

# Retry migration
python backend/database/migrations/your_migration.py
```

### Issue: Migration fails mid-execution

**Cause**: Syntax error, constraint violation, or data issue

**Solution - Rollback**:
```bash
# Restore from backup
cp budget_buddy.db budget_buddy.db.failed
cp budget_buddy.db.backup.YYYYMMDD_HHMMSS budget_buddy.db

# Review error message
# Fix migration script
# Retry
```

### Issue: "table already exists"

**Cause**: Migration was partially executed or run twice

**Solution**:
```bash
# Check if table exists
sqlite3 budget_buddy.db "SELECT name FROM sqlite_master WHERE type='table' AND name='your_table';"

# If exists, either:
# 1. Skip this migration (already applied)
# 2. Add IF NOT EXISTS to CREATE TABLE statement
# 3. Drop and recreate (DANGEROUS - loses data)
```

### Issue: Foreign key constraint fails

**Cause**: Referenced table doesn't exist or data inconsistency

**Solution**:
```bash
# Check foreign keys
sqlite3 budget_buddy.db "PRAGMA foreign_keys;"

# If OFF, enable:
sqlite3 budget_buddy.db "PRAGMA foreign_keys = ON;"

# Verify referenced tables exist
sqlite3 budget_buddy.db ".tables"
```

## Migration Examples

### Example 1: Add Column to Existing Table

**SQL Migration** (`add_trip_tag_column.sql`):
```sql
-- Add trip_tag column to transactions table
ALTER TABLE transactions ADD COLUMN trip_tag TEXT;

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_transactions_trip_tag ON transactions(trip_tag);
```

Execute:
```bash
sqlite3 budget_buddy.db < backend/database/migrations/add_trip_tag_column.sql
```

### Example 2: Create New Table with Foreign Key

**SQL Migration** (`create_buddy_insights_tables.sql`):
```sql
-- Create weekly_reflections table
CREATE TABLE IF NOT EXISTS weekly_reflections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start_date DATE NOT NULL,
    spending_summary TEXT,
    category_insights TEXT,
    goal_progress TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index
CREATE INDEX IF NOT EXISTS idx_weekly_reflections_week ON weekly_reflections(week_start_date);
```

Execute:
```bash
sqlite3 budget_buddy.db < backend/database/migrations/create_buddy_insights_tables.sql
```

### Example 3: Python Migration with Data Transform

**Python Migration** (`migrate_dining_out_to_going_out.py`):
```python
import sqlite3

def migrate():
    conn = sqlite3.connect('budget_buddy.db')
    cursor = conn.cursor()

    # Update category name
    cursor.execute("""
        UPDATE budget_allocations
        SET category = 'Going Out'
        WHERE category = 'Dining Out'
    """)

    # Update transactions
    cursor.execute("""
        UPDATE transactions
        SET bb_category = 'Going Out'
        WHERE bb_category = 'Dining Out'
    """)

    conn.commit()

    # Verify
    count = cursor.execute("""
        SELECT COUNT(*) FROM transactions WHERE bb_category = 'Going Out'
    """).fetchone()[0]

    print(f"Migrated {count} transactions to 'Going Out' category")

    conn.close()

if __name__ == '__main__':
    migrate()
```

Execute:
```bash
python backend/database/migrations/migrate_dining_out_to_going_out.py
```

## Migration Best Practices

1. **Always Backup First**
   ```bash
   cp budget_buddy.db budget_buddy.db.backup.$(date +%Y%m%d_%H%M%S)
   ```

2. **Use Transactions** (in Python migrations):
   ```python
   try:
       cursor.execute("...")
       conn.commit()
   except Exception as e:
       conn.rollback()
       print(f"Error: {e}")
   ```

3. **Use IF NOT EXISTS** (for idempotency):
   ```sql
   CREATE TABLE IF NOT EXISTS new_table (...);
   ALTER TABLE ... ADD COLUMN IF NOT EXISTS ... ;  -- SQLite 3.35+
   ```

4. **Test on Copy First**:
   ```bash
   cp budget_buddy.db test_migration.db
   sqlite3 test_migration.db < migration.sql
   ```

5. **Document Changes** in migration file:
   ```sql
   -- Migration: Add trip tagging feature
   -- Date: 2026-01-01
   -- Author: Team
   -- Purpose: Enable tagging transactions for trips/events
   ```

6. **Version Migration Files**:
   ```
   001_initial_schema.sql
   002_add_buddy_insights.py
   003_add_trip_tags.sql
   ```

## Rollback Procedures

### Immediate Rollback (Just Ran Migration)

```bash
# Stop backend
pkill -f "uvicorn.*8000"

# Restore from most recent backup
LATEST_BACKUP=$(ls -t budget_buddy.db.backup.* | head -1)
cp budget_buddy.db budget_buddy.db.failed
cp $LATEST_BACKUP budget_buddy.db

# Verify restoration
sqlite3 budget_buddy.db ".tables"

# Restart backend
python -m uvicorn backend.api.main:app --reload --port 8000
```

### Rollback Specific Change (Table/Column)

```sql
-- Drop table (DANGER: Loses data)
DROP TABLE IF EXISTS new_table;

-- Remove column (SQLite limitation: must recreate table)
-- 1. Create new table without column
-- 2. Copy data from old table
-- 3. Drop old table
-- 4. Rename new table
```

### Rollback Data Changes

```bash
# If you have backup with good data
sqlite3 backup.db "SELECT * FROM transactions WHERE id = 123;"

# Copy that data to current database
# Use UPDATE or INSERT statements
```

## Technical Details

### SQLite Limitations

- **Can't drop columns** (< SQLite 3.35): Must recreate table
- **Can't modify columns**: Must recreate table
- **Limited ALTER TABLE**: Only ADD COLUMN, RENAME TABLE, RENAME COLUMN

Workaround:
```sql
-- 1. Create new table with desired schema
CREATE TABLE transactions_new (...);

-- 2. Copy data
INSERT INTO transactions_new SELECT * FROM transactions;

-- 3. Drop old table
DROP TABLE transactions;

-- 4. Rename new table
ALTER TABLE transactions_new RENAME TO transactions;
```

### Migration Files in Project

Current migrations in `/backend/database/migrations/`:
- `add_buddy_insights.py`
- `consolidate_goal_dimensions.py`
- `create_buddy_insights_tables.sql`
- `create_transaction_aggregations.py`
- `add_income_savings_to_reflections.sql`
- Plus 14+ more migration scripts

### Database Schema

14 core tables:
1. `transactions` - All bank transactions
2. `budget_allocations` - Monthly budget categories
3. `monthly_income` - Income tracking
4. `monthly_reflections` - Month-end reviews
5. `sinking_funds` - Savings goals
6. `sinking_fund_transactions` - Fund deposits/withdrawals
7. `institutions` - Banks (from Plaid)
8. `accounts` - Bank accounts
9. `account_connection_log` - Sync history
10. `weekly_summaries` - Weekly aggregations
11. `subscription_patterns` - Recurring transactions
12. `weekly_reflections` - Buddy AI weekly insights
13. `weekly_plans` - Weekly spending plans
14. `chat_goals` - User goals from chat

## Testing the Skill

1. **Create test migration**:
   ```bash
   cat > backend/database/migrations/test_add_column.sql << 'EOF'
   -- Test migration
   ALTER TABLE transactions ADD COLUMN test_column TEXT;
   EOF
   ```

2. **Backup database**:
   ```bash
   cp budget_buddy.db budget_buddy.db.test_backup
   ```

3. **Run migration**:
   ```bash
   sqlite3 budget_buddy.db < backend/database/migrations/test_add_column.sql
   ```

4. **Verify**:
   ```bash
   sqlite3 budget_buddy.db "PRAGMA table_info(transactions);" | grep test_column
   ```

5. **Rollback**:
   ```bash
   cp budget_buddy.db.test_backup budget_buddy.db
   ```

6. **Clean up**:
   ```bash
   rm backend/database/migrations/test_add_column.sql
   rm budget_buddy.db.test_backup
   ```

## Integration with Other Skills

- **Full-Stack Setup** - Creates initial database
- **Development Diagnostics** - Validates schema integrity
- **Backend Server Startup** - Database must be migrated before server starts

## References

- `/backend/database/migrations/` - All migration files
- `/backend/database/models.py` - SQLAlchemy models (target schema)
- `/backend/database/session.py` - Database connection
- `budget_buddy.db` - SQLite database file

## Last Updated

January 1, 2026
