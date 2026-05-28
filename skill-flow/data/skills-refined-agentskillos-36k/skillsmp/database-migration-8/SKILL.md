---
name: database-migration
description: Safe database migration workflow with zero-downtime strategies
license: MIT
---

# Database Migration Skill

Use this skill when creating, running, or troubleshooting database migrations.

## When to Use

- Adding or modifying database tables
- Changing column types or constraints
- Creating indexes
- Data migrations or backfills
- Schema versioning

## Migration Principles

1. **Backwards Compatible**: Migrations should work with current AND previous code versions
2. **Reversible**: Always include a rollback strategy
3. **Atomic**: Each migration does one logical change
4. **Tested**: Test migrations on a copy of production data
5. **Documented**: Explain why, not just what

## Safe Migration Patterns

### Adding a Column

```typescript
// ✅ Safe: Add nullable column (no lock on reads)
export async function up(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.string('phone').nullable();
  });
}

export async function down(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('phone');
  });
}
```

### Adding a NOT NULL Column

```typescript
// Migration 1: Add nullable column
export async function up(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.string('status').nullable();
  });
}

// Migration 2: Backfill data (after deployment)
export async function up(db: Knex) {
  await db('users')
    .whereNull('status')
    .update({ status: 'active' });
}

// Migration 3: Add NOT NULL constraint (after verification)
export async function up(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.string('status').notNullable().alter();
  });
}
```

### Renaming a Column (Zero Downtime)

```typescript
// Migration 1: Add new column
export async function up(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.string('full_name');
  });
}

// Migration 2: Copy data
export async function up(db: Knex) {
  await db.raw('UPDATE users SET full_name = name');
}

// Migration 3: Deploy code using full_name
// ... code changes ...

// Migration 4: Drop old column (after all code deployed)
export async function up(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('name');
  });
}
```

### Adding an Index (Safely)

```sql
-- PostgreSQL: Create index without blocking writes
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Note: CONCURRENTLY cannot be used in a transaction
-- Run outside of migration transaction or use separate step
```

```typescript
export async function up(db: Knex) {
  // For PostgreSQL with CONCURRENTLY
  await db.raw(`
    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email 
    ON users(email)
  `);
}
```

### Dropping a Column (Zero Downtime)

```typescript
// Step 1: Stop writing to column (code change)
// Step 2: Deploy code that doesn't read column
// Step 3: Drop column in migration

export async function up(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('deprecated_field');
  });
}

export async function down(db: Knex) {
  // Can't restore data, just recreate structure
  await db.schema.alterTable('users', (table) => {
    table.string('deprecated_field').nullable();
  });
}
```

## Data Migrations

### Batch Processing

```typescript
const BATCH_SIZE = 1000;

export async function up(db: Knex) {
  let processed = 0;
  let hasMore = true;

  while (hasMore) {
    const result = await db.raw(`
      WITH batch AS (
        SELECT id FROM users
        WHERE new_field IS NULL
        LIMIT ${BATCH_SIZE}
      )
      UPDATE users
      SET new_field = compute_value(old_field)
      WHERE id IN (SELECT id FROM batch)
      RETURNING id
    `);

    processed += result.rowCount;
    hasMore = result.rowCount === BATCH_SIZE;

    // Log progress
    console.log(`Processed ${processed} rows`);

    // Prevent overwhelming the database
    await new Promise(resolve => setTimeout(resolve, 100));
  }
}
```

### Validation Migration

```typescript
export async function up(db: Knex) {
  // Check data consistency before adding constraint
  const invalid = await db('users')
    .whereNull('email')
    .orWhere('email', '')
    .count('* as count')
    .first();

  if (invalid.count > 0) {
    throw new Error(`Found ${invalid.count} users with invalid email`);
  }

  // Safe to add constraint
  await db.schema.alterTable('users', (table) => {
    table.string('email').notNullable().alter();
  });
}
```

## Migration File Structure

```
migrations/
├── 20240101000000_create_users_table.ts
├── 20240102000000_add_email_index.ts
├── 20240103000000_add_user_status.ts
└── 20240104000000_backfill_user_status.ts
```

### Naming Convention

```
YYYYMMDDHHMMSS_description.ts

Examples:
20240115143000_create_orders_table.ts
20240115143100_add_orders_user_foreign_key.ts
20240115143200_add_orders_status_index.ts
```

## Rollback Strategies

### Code-Level Rollback

```typescript
export async function down(db: Knex) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('new_column');
  });
}
```

### Point-in-Time Recovery

```bash
# PostgreSQL
pg_restore -d dbname --target-time="2024-01-15 14:30:00" backup.dump

# MySQL
mysqlbinlog --stop-datetime="2024-01-15 14:30:00" binlog.000001 | mysql
```

## Testing Migrations

```typescript
describe('Migration: add_user_status', () => {
  beforeAll(async () => {
    // Use test database
    await db.migrate.rollback();
    await db.migrate.latest();
  });

  it('should add status column', async () => {
    const hasColumn = await db.schema.hasColumn('users', 'status');
    expect(hasColumn).toBe(true);
  });

  it('should backfill existing users', async () => {
    const nullStatus = await db('users').whereNull('status').count();
    expect(nullStatus[0].count).toBe('0');
  });

  it('should rollback cleanly', async () => {
    await db.migrate.rollback();
    const hasColumn = await db.schema.hasColumn('users', 'status');
    expect(hasColumn).toBe(false);
  });
});
```

## PostgreSQL Specific

### Check Constraints

```sql
-- Add constraint without validating existing rows (fast)
ALTER TABLE users ADD CONSTRAINT users_age_positive
  CHECK (age >= 0) NOT VALID;

-- Validate separately (acquires lighter lock)
ALTER TABLE users VALIDATE CONSTRAINT users_age_positive;
```

### Lock Monitoring

```sql
-- Check for blocking locks
SELECT 
  blocked.pid AS blocked_pid,
  blocked.query AS blocked_query,
  blocking.pid AS blocking_pid,
  blocking.query AS blocking_query
FROM pg_locks blocked_locks
JOIN pg_stat_activity blocked ON blocked.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
  AND blocking_locks.relation = blocked_locks.relation
  AND blocking_locks.pid != blocked_locks.pid
JOIN pg_stat_activity blocking ON blocking.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

## Migration Checklist

### Before Migration
- [ ] Migration tested on staging
- [ ] Rollback plan documented
- [ ] Team notified of migration
- [ ] Backup verified
- [ ] Off-peak time selected

### During Migration
- [ ] Monitor query performance
- [ ] Watch for lock contention
- [ ] Track progress for long migrations

### After Migration
- [ ] Verify schema changes
- [ ] Check application health
- [ ] Validate data integrity
- [ ] Update documentation

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Large table ALTER | Locks table | Use CONCURRENTLY, batch |
| Missing down() | Can't rollback | Always write rollback |
| NOT NULL without default | Breaks existing rows | Add default or backfill |
| Dropping column early | Code still reads it | Remove from code first |
| No testing | Surprises in prod | Test on prod data copy |
