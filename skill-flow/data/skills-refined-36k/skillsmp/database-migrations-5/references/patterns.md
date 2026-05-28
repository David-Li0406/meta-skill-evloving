# Database Migrations

## Patterns

### **Drizzle Migrations**
  #### **Description**
Drizzle Kit migration workflow
  #### **Example**
    // drizzle.config.ts
    import type { Config } from 'drizzle-kit';
    
    export default {
      schema: './src/db/schema.ts',
      out: './drizzle',
      driver: 'pg',
      dbCredentials: {
        connectionString: process.env.DATABASE_URL!,
      },
    } satisfies Config;
    
    
    // Generate migration
    npx drizzle-kit generate:pg
    
    // Creates: drizzle/0001_add_users_table.sql
    
    
    // Apply migrations
    import { drizzle } from 'drizzle-orm/postgres-js';
    import { migrate } from 'drizzle-orm/postgres-js/migrator';
    import postgres from 'postgres';
    
    async function runMigrations() {
      const connection = postgres(process.env.DATABASE_URL!, { max: 1 });
      const db = drizzle(connection);
    
      console.log('Running migrations...');
      await migrate(db, { migrationsFolder: './drizzle' });
      console.log('Migrations complete');
    
      await connection.end();
    }
    
    runMigrations();
    
    
    // In CI/CD
    // 1. Run migrations before deploying new code
    // 2. New code is backwards compatible with old schema
    // 3. After deploy, run cleanup migration if needed
    
### **Prisma Migrations**
  #### **Description**
Prisma Migrate workflow
  #### **Example**
    // schema.prisma
    model User {
      id        String   @id @default(uuid())
      email     String   @unique
      name      String?
      createdAt DateTime @default(now())
    }
    
    
    // Development: Create and apply
    npx prisma migrate dev --name add_users
    
    
    // Production: Apply only
    npx prisma migrate deploy
    
    
    // Reset (development only!)
    npx prisma migrate reset
    
    
    // Check migration status
    npx prisma migrate status
    
    
    // Resolve failed migration
    npx prisma migrate resolve --applied "20240101120000_add_users"
    
    
    // In package.json
    {
      "scripts": {
        "db:migrate:dev": "prisma migrate dev",
        "db:migrate:deploy": "prisma migrate deploy",
        "db:migrate:status": "prisma migrate status"
      }
    }
    
### **Expand Contract**
  #### **Description**
Safe schema evolution pattern
  #### **Example**
    # EXPAND-CONTRACT PATTERN
    # Rename column: old_name -> new_name
    
    ## Step 1: EXPAND (add new column)
    
    -- Migration: 001_add_new_column.sql
    ALTER TABLE users ADD COLUMN new_name VARCHAR(255);
    
    -- Backfill data
    UPDATE users SET new_name = old_name WHERE new_name IS NULL;
    
    -- Add trigger for sync during transition
    CREATE OR REPLACE FUNCTION sync_user_name()
    RETURNS TRIGGER AS $$
    BEGIN
      IF NEW.old_name IS DISTINCT FROM OLD.old_name THEN
        NEW.new_name = NEW.old_name;
      END IF;
      IF NEW.new_name IS DISTINCT FROM OLD.new_name THEN
        NEW.old_name = NEW.new_name;
      END IF;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER user_name_sync
      BEFORE UPDATE ON users
      FOR EACH ROW
      EXECUTE FUNCTION sync_user_name();
    
    
    ## Step 2: Deploy code reading from new_name
    ## Step 3: Deploy code writing to new_name
    
    
    ## Step 4: CONTRACT (remove old column)
    
    -- Migration: 002_remove_old_column.sql
    DROP TRIGGER user_name_sync ON users;
    DROP FUNCTION sync_user_name();
    ALTER TABLE users DROP COLUMN old_name;
    
### **Zero Downtime Add Column**
  #### **Description**
Add column without locking
  #### **Example**
    # ZERO-DOWNTIME: ADD COLUMN
    
    ## PostgreSQL
    
    -- Safe: ADD COLUMN with NULL (no table rewrite)
    ALTER TABLE users ADD COLUMN phone VARCHAR(50);
    
    -- Safe: ADD COLUMN with DEFAULT (Postgres 11+, no table rewrite)
    ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
    
    -- DANGEROUS: ADD COLUMN NOT NULL without DEFAULT (locks table)
    -- Don't do this on large tables!
    ALTER TABLE users ADD COLUMN status VARCHAR(20) NOT NULL;
    
    
    ## Safe way to add NOT NULL:
    
    -- Step 1: Add nullable column
    ALTER TABLE users ADD COLUMN status VARCHAR(20);
    
    -- Step 2: Backfill in batches
    UPDATE users SET status = 'active'
    WHERE status IS NULL
    AND id IN (SELECT id FROM users WHERE status IS NULL LIMIT 10000);
    
    -- Step 3: Add NOT NULL constraint
    ALTER TABLE users ALTER COLUMN status SET NOT NULL;
    
    
    ## Drizzle approach
    
    // Schema change
    export const users = pgTable('users', {
      // ... existing columns
      status: varchar('status', { length: 20 }).default('active'),
    });
    
    // Generate migration, review SQL, apply
    
### **Safe Index Creation**
  #### **Description**
Create indexes without blocking
  #### **Example**
    # CONCURRENT INDEX CREATION
    
    ## PostgreSQL
    
    -- WRONG: Blocks all writes
    CREATE INDEX idx_users_email ON users(email);
    
    -- RIGHT: Non-blocking (takes longer but no lock)
    CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
    
    
    ## Gotchas with CONCURRENTLY:
    
    1. Cannot run in a transaction
    2. If it fails, leaves invalid index (must drop and retry)
    3. Takes 2-3x longer than regular index
    
    -- Check for invalid indexes
    SELECT indexrelname, pg_size_pretty(pg_relation_size(indexrelid))
    FROM pg_stat_user_indexes
    WHERE idx_scan = 0
    AND schemaname = 'public';
    
    
    ## In migration file
    
    -- drizzle/0005_add_email_index.sql
    -- This migration must run outside transaction
    
    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email
    ON users(email);
    
    
    ## Migration runner config
    
    // For Drizzle, run separately
    const indexMigration = postgres(process.env.DATABASE_URL!, {
      max: 1,
      // No transaction for CONCURRENTLY
    });
    
    await indexMigration.unsafe(`
      CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email)
    `);
    
### **Backfill Pattern**
  #### **Description**
Safely backfill large tables
  #### **Example**
    # BATCH BACKFILL PATTERN
    
    // Backfill in batches to avoid locking
    async function backfillStatus(db: Database) {
      const BATCH_SIZE = 10000;
      let updated = 0;
    
      while (true) {
        const result = await db.execute(sql`
          UPDATE users
          SET status = 'active'
          WHERE id IN (
            SELECT id FROM users
            WHERE status IS NULL
            LIMIT ${BATCH_SIZE}
          )
        `);
    
        if (result.rowCount === 0) break;
    
        updated += result.rowCount;
        console.log(`Backfilled ${updated} rows`);
    
        // Pause between batches to reduce load
        await new Promise(r => setTimeout(r, 100));
      }
    
      console.log(`Backfill complete: ${updated} total rows`);
    }
    
    
    // With progress tracking
    async function backfillWithProgress(db: Database) {
      // Get total count first
      const [{ count }] = await db.execute(sql`
        SELECT COUNT(*) as count FROM users WHERE status IS NULL
      `);
    
      console.log(`Need to backfill ${count} rows`);
    
      let processed = 0;
      const startTime = Date.now();
    
      while (processed < count) {
        await db.execute(sql`
          UPDATE users
          SET status = 'active'
          WHERE id IN (
            SELECT id FROM users
            WHERE status IS NULL
            ORDER BY id
            LIMIT 10000
          )
        `);
    
        processed += 10000;
        const elapsed = (Date.now() - startTime) / 1000;
        const rate = processed / elapsed;
        const remaining = (count - processed) / rate;
    
        console.log(`Progress: ${processed}/${count} (${remaining.toFixed(0)}s remaining)`);
      }
    }
    

## Anti-Patterns

### **Auto Migrate Production**
  #### **Description**
Letting ORMs auto-migrate in production
  #### **Wrong**
prisma db push in production, auto-sync schema
  #### **Right**
Generate migrations, review, test, then apply
### **No Rollback Plan**
  #### **Description**
Migrating without rollback strategy
  #### **Wrong**
Just apply the migration, it'll be fine
  #### **Right**
Write down migration for every migration
### **Big Bang Migration**
  #### **Description**
Massive schema change in single migration
  #### **Wrong**
Rename 10 columns, add 5 tables, change types
  #### **Right**
Break into small, reversible migrations
### **Lock Entire Table**
  #### **Description**
Long-running operations holding locks
  #### **Wrong**
UPDATE users SET x = y; (10M rows, 30 min lock)
  #### **Right**
Batch updates, concurrent index creation
### **No Testing**
  #### **Description**
Not testing migrations on production data
  #### **Wrong**
Works on 100 rows in dev, should be fine
  #### **Right**
Test on anonymized production data dump