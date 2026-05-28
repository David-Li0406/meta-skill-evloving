---
name: database-migration
description: Use this skill for safe database migration workflows with zero-downtime strategies.
---

# Database Migration Skill

This skill guides you through creating, running, and troubleshooting database migrations while ensuring zero-downtime.

## When to Use

- Adding or modifying database tables
- Changing column types or constraints
- Creating indexes
- Data migrations or backfills
- Schema versioning

## Migration Principles

1. **Backwards Compatible**: Migrations should work with current AND previous code versions.
2. **Reversible**: Always include a rollback strategy.
3. **Atomic**: Each migration should perform one logical change.
4. **Tested**: Test migrations on a copy of production data.
5. **Documented**: Explain why changes are made, not just what changes are made.

## Migration Safety Rules

1. Always backup before migration.
2. Test migration on staging first.
3. Make migrations reversible.
4. Deploy in small batches.
5. Monitor during migration.

## Safe Migration Patterns

### Adding a Column

```typescript
// Safe: Add nullable column (no lock on reads)
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

## Data Migration Strategies

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

## Rollback Strategies

| Strategy | When to Use |
|----------|-------------|
| Script rollback | Data changes, can undo |
| Backup restore | Major failure, data loss |
| Feature flag off | Code changes |
| Traffic reroute | Service migration |

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

## Best Practices

1. **One change per migration** - Easier to rollback.
2. **Always write DOWN migrations** - You will need them.
3. **Test on production data copy** - Size matters.
4. **Use transactions** - Atomic changes.
5. **Monitor during migration** - Watch for locks.

## Common Migration Scenarios

### Adding Required Column
```sql
-- Wrong: Locks table, fails on existing rows
ALTER TABLE users ADD COLUMN email VARCHAR NOT NULL;

-- Right: Three-phase approach
ALTER TABLE users ADD COLUMN email VARCHAR;
UPDATE users SET email = 'unknown@example.com' WHERE email IS NULL;
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
```

### Large Table Index
```sql
-- Wrong: Blocks writes
CREATE INDEX idx_orders_user ON orders(user_id);

-- Right: Non-blocking
CREATE INDEX CONCURRENTLY idx_orders_user ON orders(user_id);
```

### Type Conversion
```sql
-- Add new column
ALTER TABLE products ADD COLUMN price_cents INTEGER;

-- Migrate data
UPDATE products SET price_cents = (price * 100)::INTEGER;

-- Switch application to use new column
-- Drop old column
ALTER TABLE products DROP COLUMN price;
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