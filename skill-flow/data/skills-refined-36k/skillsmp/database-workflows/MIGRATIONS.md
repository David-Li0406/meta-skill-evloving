# Migration Strategies

Detailed patterns for database migrations, rollback strategies, and version control.

## Migration Principles

### Golden Rules

1. **Always reversible** - Every migration must have a rollback
2. **Atomic changes** - One logical change per migration
3. **No data loss** - Rollback must preserve data when possible
4. **Backward compatible** - Support running both old and new code
5. **Test on production copy** - Run migrations on cloned production data

### Migration Naming

```
# Format: {timestamp}_{action}_{target}
20240115120000_create_users_table
20240115120100_add_email_index_to_users
20240115120200_rename_username_to_name_in_users
20240115120300_drop_legacy_tokens_table
```

## ORM Migration Commands

### Prisma

```bash
# Generate migration
bunx prisma migrate dev --create-only --name add_email_to_users

# Apply migrations (development)
bunx prisma migrate dev

# Apply migrations (production)
bunx prisma migrate deploy

# Reset database (development only!)
bunx prisma migrate reset

# Check migration status
bunx prisma migrate status
```

### Drizzle

```bash
# Generate migration
bunx drizzle-kit generate:pg --name add_email_to_users

# Apply migrations
bunx drizzle-kit push:pg

# Drop all and recreate (development)
bunx drizzle-kit drop

# View pending migrations
bunx drizzle-kit check:pg
```

### TypeORM

```bash
# Generate migration from entities
bunx typeorm migration:generate -n AddEmailToUsers

# Create empty migration
bunx typeorm migration:create -n AddEmailToUsers

# Run migrations
bunx typeorm migration:run

# Revert last migration
bunx typeorm migration:revert

# Show pending migrations
bunx typeorm migration:show
```

## Common Migration Patterns

### Add Column (Backward Compatible)

```sql
-- Up
ALTER TABLE users ADD COLUMN middle_name TEXT;

-- Down
ALTER TABLE users DROP COLUMN middle_name;
```

**ORM Examples:**

```typescript
// Prisma schema change
model User {
  id         Int     @id @default(autoincrement())
  email      String
  middleName String? @map("middle_name")  // nullable for existing rows
}

// Drizzle
export const addMiddleName = pgTable('users', {
  middleName: text('middle_name'),
});

// TypeORM migration
export class AddMiddleName1234567890 implements MigrationInterface {
  async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.addColumn('users', new TableColumn({
      name: 'middle_name',
      type: 'text',
      isNullable: true,
    }));
  }

  async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropColumn('users', 'middle_name');
  }
}
```

### Add NOT NULL Column

**Three-phase approach for zero downtime:**

```sql
-- Phase 1: Add nullable column with default
ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active';

-- Phase 2: Backfill existing rows (run in application)
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Phase 3: Add NOT NULL constraint (separate migration)
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
```

### Rename Column (Zero Downtime)

**Three-phase approach:**

```sql
-- Phase 1: Add new column
ALTER TABLE users ADD COLUMN full_name TEXT;
UPDATE users SET full_name = name;

-- Phase 2: Application writes to both columns
-- (deploy application change)

-- Phase 3: Drop old column (after all instances updated)
ALTER TABLE users DROP COLUMN name;
```

### Add Index Without Locking

```sql
-- PostgreSQL: Non-blocking index creation
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Note: CONCURRENTLY cannot run in a transaction
-- Use separate migration or raw SQL
```

```typescript
// TypeORM: Raw SQL for concurrent index
export class AddEmailIndex1234567890 implements MigrationInterface {
  async up(queryRunner: QueryRunner): Promise<void> {
    // Must run outside transaction
    await queryRunner.query(
      'CREATE INDEX CONCURRENTLY idx_users_email ON users(email)'
    );
  }

  async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query('DROP INDEX idx_users_email');
  }
}
```

### Change Column Type

```sql
-- Safe: Widening types
ALTER TABLE products ALTER COLUMN description TYPE TEXT;  -- VARCHAR to TEXT

-- Unsafe: Narrowing types (requires data check)
-- First verify no data exceeds new limit
SELECT * FROM products WHERE LENGTH(description) > 100;

-- Then alter with explicit cast
ALTER TABLE products
ALTER COLUMN description TYPE VARCHAR(100)
USING LEFT(description, 100);
```

### Add Foreign Key

```sql
-- Up
ALTER TABLE posts
ADD CONSTRAINT fk_posts_user
FOREIGN KEY (user_id) REFERENCES users(id);

CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Down
ALTER TABLE posts DROP CONSTRAINT fk_posts_user;
DROP INDEX idx_posts_user_id;
```

### Add Unique Constraint

```sql
-- Check for duplicates first
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Add constraint
ALTER TABLE users ADD CONSTRAINT uq_users_email UNIQUE (email);
```

## Large Table Migrations

### Batched Updates

```sql
-- Instead of one massive UPDATE
-- Bad: UPDATE users SET status = 'active';

-- Good: Batch in chunks
DO $$
DECLARE
  batch_size INT := 10000;
  affected INT;
BEGIN
  LOOP
    UPDATE users
    SET status = 'active'
    WHERE id IN (
      SELECT id FROM users
      WHERE status IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );
    GET DIAGNOSTICS affected = ROW_COUNT;
    EXIT WHEN affected = 0;
    COMMIT;
    PERFORM pg_sleep(0.1);  -- Brief pause to reduce load
  END LOOP;
END $$;
```

```typescript
// TypeScript batched update
async function batchUpdate(db: Database, batchSize = 10000) {
  let affected = 0;
  do {
    const result = await db.execute(sql`
      UPDATE users
      SET status = 'active'
      WHERE id IN (
        SELECT id FROM users
        WHERE status IS NULL
        LIMIT ${batchSize}
      )
    `);
    affected = result.rowCount;
    await new Promise(r => setTimeout(r, 100));
  } while (affected > 0);
}
```

### Online Schema Changes

For MySQL (using gh-ost or pt-online-schema-change):

```bash
# gh-ost example
gh-ost \
  --database=mydb \
  --table=users \
  --alter="ADD COLUMN middle_name VARCHAR(255)" \
  --execute

# pt-online-schema-change
pt-online-schema-change \
  --alter="ADD COLUMN middle_name VARCHAR(255)" \
  D=mydb,t=users \
  --execute
```

## Rollback Strategies

### Simple Rollback

```typescript
// TypeORM
export class AddStatusColumn1234567890 implements MigrationInterface {
  async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.addColumn('users', new TableColumn({
      name: 'status',
      type: 'text',
      default: "'active'",
    }));
  }

  async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropColumn('users', 'status');
  }
}
```

### Rollback with Data Preservation

```sql
-- Up: Split name into first_name and last_name
ALTER TABLE users ADD COLUMN first_name TEXT;
ALTER TABLE users ADD COLUMN last_name TEXT;
UPDATE users SET
  first_name = split_part(name, ' ', 1),
  last_name = split_part(name, ' ', 2);

-- Down: Merge back (preserve original data if column still exists)
UPDATE users SET name = first_name || ' ' || COALESCE(last_name, '');
ALTER TABLE users DROP COLUMN first_name;
ALTER TABLE users DROP COLUMN last_name;
```

### Irreversible Migrations

```typescript
// TypeORM: Mark as irreversible
export class DropLegacyTable1234567890 implements MigrationInterface {
  async up(queryRunner: QueryRunner): Promise<void> {
    // Backup before dropping
    await queryRunner.query(`
      CREATE TABLE legacy_users_backup AS
      SELECT * FROM legacy_users
    `);
    await queryRunner.dropTable('legacy_users');
  }

  async down(queryRunner: QueryRunner): Promise<void> {
    throw new Error('This migration is irreversible. Restore from backup.');
  }
}
```

## Zero-Downtime Deployment Pattern

### Expand-Contract Pattern

```
Phase 1: EXPAND (add new structure)
├── Add new columns/tables
├── Deploy code that writes to both old and new
└── Backfill existing data

Phase 2: MIGRATE (switch reads)
├── Deploy code that reads from new structure
└── Continue writing to both

Phase 3: CONTRACT (remove old structure)
├── Deploy code that only uses new structure
└── Remove old columns/tables
```

### Example: Rename Column

```
# Phase 1: Add new column
Migration: ALTER TABLE users ADD COLUMN full_name TEXT;
Deploy: Application writes to both `name` and `full_name`
Script: UPDATE users SET full_name = name WHERE full_name IS NULL;

# Phase 2: Switch reads
Deploy: Application reads from `full_name`, writes to both

# Phase 3: Drop old column
Deploy: Application only uses `full_name`
Migration: ALTER TABLE users DROP COLUMN name;
```

## Version Control Best Practices

### Migration Files Structure

```
migrations/
├── 20240101000000_create_users_table.sql
├── 20240101000100_create_posts_table.sql
├── 20240102000000_add_email_index.sql
└── 20240102000100_add_status_to_users.sql
```

### Never Edit Applied Migrations

Once a migration is applied to any environment:
- Never modify its content
- Create a new migration for fixes
- Document why in commit message

### Squashing Migrations

```bash
# Create a baseline migration for new environments
# Keep full history for existing deployments

# Prisma
bunx prisma migrate reset --skip-seed
bunx prisma db push
bunx prisma migrate dev --name baseline

# Manual approach
pg_dump --schema-only mydb > migrations/0000_baseline.sql
```

## Testing Migrations

### Local Testing

```bash
# Test migration on fresh database
docker compose up -d postgres_test
bunx prisma migrate deploy --preview-feature
bunx prisma migrate reset

# Test rollback
bunx prisma migrate reset --skip-seed
```

### Production Clone Testing

```bash
# Clone production database
pg_dump production_db | psql test_migration_db

# Run migrations
bunx prisma migrate deploy

# Run application tests
bun test

# Verify rollback works
bunx typeorm migration:revert
```

## Migration Checklist

### Before Creating

- [ ] Understand current schema and data
- [ ] Plan for zero-downtime deployment
- [ ] Consider rollback strategy
- [ ] Check for large table implications

### During Development

- [ ] Migration is idempotent (can run twice safely)
- [ ] Down migration is implemented
- [ ] No hardcoded environment-specific values
- [ ] Large tables use batched operations
- [ ] Indexes created CONCURRENTLY if needed

### Before Deployment

- [ ] Tested on production data copy
- [ ] Execution time is acceptable
- [ ] Rollback tested
- [ ] Application compatible with old AND new schema
- [ ] Monitoring in place for migration impact

### After Deployment

- [ ] Verify migration completed successfully
- [ ] Check application logs for errors
- [ ] Monitor database performance
- [ ] Update documentation if schema changed
