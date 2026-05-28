# Database Schema Design - Sharp Edges

## Postgres Enum Transaction Trap

### **Id**
postgres-enum-transaction-trap
### **Summary**
ALTER TYPE ADD VALUE cannot be used in transaction until committed
### **Severity**
critical
### **Situation**
Adding new enum value in a migration that also uses that value
### **Why**
  PostgreSQL restricts enum modifications inside transactions. You add 'PENDING' to
  OrderStatus enum, then try to use it in the same migration. The new value doesn't
  exist yet from the transaction's perspective. Migration fails. Worse in older
  PostgreSQL versions where ADD VALUE couldn't be in transactions at all.
  
### **Solution**
  -- WRONG: Same transaction
  BEGIN;
  ALTER TYPE order_status ADD VALUE 'PENDING';
  INSERT INTO orders (status) VALUES ('PENDING'); -- FAILS!
  COMMIT;
  
  -- RIGHT: Separate migrations
  -- Migration 1: Add enum value
  ALTER TYPE order_status ADD VALUE 'PENDING';
  
  -- Migration 2: Use the new value (runs after commit)
  INSERT INTO orders (status) VALUES ('PENDING');
  
  -- For Prisma: Split into two separate migration files
  -- For Drizzle: Use two separate migration SQL files
  
### **Symptoms**
  - "invalid input value for enum" during migration
  - Migration works locally but fails in CI
  - Enum value not recognized in same transaction
### **Detection Pattern**
ALTER TYPE.*ADD VALUE[^;]*;[^;]*INSERT|UPDATE.*VALUES.*\(

## Uuid V4 Mysql Clustered Disaster

### **Id**
uuid-v4-mysql-clustered-disaster
### **Summary**
Random UUID v4 destroys MySQL/InnoDB insert performance
### **Severity**
critical
### **Situation**
Using UUID v4 as primary key in MySQL with clustered index
### **Why**
  MySQL InnoDB uses clustered primary key - rows are physically ordered by PK.
  UUID v4 is random. Every insert goes to a random position in the B-tree.
  Pages split constantly. Insert performance degrades 10-50x. With millions of
  rows, inserts take seconds instead of milliseconds.
  
### **Solution**
  -- WRONG: Random UUID in MySQL
  CREATE TABLE orders (
    id CHAR(36) PRIMARY KEY, -- UUID v4, random
    created_at TIMESTAMP
  );
  
  -- RIGHT: Auto-increment or UUID v7 in MySQL
  CREATE TABLE orders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    public_id CHAR(36) UNIQUE, -- UUID for external use
    created_at TIMESTAMP
  );
  
  -- Or use UUID v7 (time-ordered)
  -- Node.js: import { v7 as uuidv7 } from 'uuid';
  
  -- PostgreSQL note: Less severe because PG uses heap, not clustered PK
  -- But UUID v7 still better for index locality
  
### **Symptoms**
  - Insert latency increases with table size
  - Buffer pool hit rate drops
  - SHOW ENGINE INNODB STATUS shows high page splits
### **Detection Pattern**
@id @default\\(uuid\\(\\)\\)|PRIMARY KEY.*uuid|CHAR\\(36\\).*PRIMARY

## Migration No Rollback

### **Id**
migration-no-rollback
### **Summary**
Destructive migration without tested rollback path
### **Severity**
critical
### **Situation**
Running ALTER TABLE DROP COLUMN or data transformation in production
### **Why**
  Column dropped. Data gone. Something breaks. No rollback script. "We have backups"
  but restore takes 4 hours and means 4 hours of data loss. Team scrambles to
  recreate column and data. Some data is permanently lost.
  
### **Solution**
  -- WRONG: Drop column directly
  ALTER TABLE users DROP COLUMN legacy_field;
  
  -- RIGHT: Expand-Contract Migration Pattern
  -- Phase 1: Stop writing to column (deploy code first)
  -- Phase 2: Add migration that drops column
  -- Phase 3: Keep backup for rollback window (7 days)
  
  -- For any destructive migration, have:
  -- 1. Tested rollback script
  -- 2. Data backup of affected tables
  -- 3. Runbook for recovery
  
  -- Example rollback script:
  -- up.sql
  ALTER TABLE users DROP COLUMN legacy_field;
  
  -- down.sql
  ALTER TABLE users ADD COLUMN legacy_field VARCHAR(255);
  -- Note: Data is gone, but schema is restored
  
### **Symptoms**
  - Migrations without corresponding down/rollback
  - "We'll handle rollback if needed" (famous last words)
  - DROP COLUMN in production migration
### **Detection Pattern**
DROP COLUMN|DROP TABLE(?! IF EXISTS)|TRUNCATE

## Missing Fk Index

### **Id**
missing-fk-index
### **Summary**
Foreign key without index causes table-wide locks on parent delete
### **Severity**
high
### **Situation**
Creating foreign key relationship without adding index on child table
### **Why**
  User has 100,000 orders. Delete user. PostgreSQL checks all orders for that user_id.
  Without index, it's a full table scan. Table locked. Other queries wait. For large
  tables, this can lock for minutes. MySQL at least requires indexes on FKs;
  PostgreSQL does not.
  
### **Solution**
  -- WRONG: FK without index (PostgreSQL allows this!)
  model Order {
    id     String @id
    userId String
    user   User   @relation(fields: [userId], references: [id])
    // No index on userId!
  }
  
  -- RIGHT: Always index foreign keys
  model Order {
    id     String @id
    userId String
    user   User   @relation(fields: [userId], references: [id])
  
    @@index([userId]) // CRITICAL!
  }
  
  -- Check for missing indexes on FKs:
  SELECT
    tc.table_name,
    kcu.column_name,
    CASE WHEN i.indexname IS NULL THEN 'MISSING INDEX' ELSE 'OK' END
  FROM information_schema.table_constraints tc
  JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
  LEFT JOIN pg_indexes i
    ON i.tablename = tc.table_name AND i.indexdef LIKE '%' || kcu.column_name || '%'
  WHERE tc.constraint_type = 'FOREIGN KEY';
  
### **Symptoms**
  - DELETE on parent table takes unexpectedly long
  - Lock wait timeouts during cascade operations
  - Why is deleting one user taking 30 seconds?
### **Detection Pattern**
@relation\\(fields.*references(?![^}]*@@index)

## Alter Table Lock Production

### **Id**
alter-table-lock-production
### **Summary**
ALTER TABLE on large table locks it for minutes/hours
### **Severity**
high
### **Situation**
Adding column with default, changing column type, or adding constraint to production table
### **Why**
  Table has 50 million rows. ALTER TABLE ADD COLUMN name VARCHAR(255) DEFAULT 'unknown'.
  PostgreSQL rewrites entire table to add default values. Table locked for writes.
  Users see 500 errors. In MySQL, even simple ALTERs can lock the table completely.
  
### **Solution**
  -- WRONG: Add column with default on huge table
  ALTER TABLE users ADD COLUMN status VARCHAR(50) DEFAULT 'active';
  -- Locks table while writing default to 50M rows
  
  -- RIGHT: Three-phase migration
  -- Phase 1: Add nullable column (instant, no rewrite)
  ALTER TABLE users ADD COLUMN status VARCHAR(50);
  
  -- Phase 2: Backfill in batches (no locks)
  DO $$
  DECLARE
    batch_size INT := 10000;
  BEGIN
    LOOP
      UPDATE users SET status = 'active'
      WHERE id IN (
        SELECT id FROM users
        WHERE status IS NULL
        LIMIT batch_size
      );
      IF NOT FOUND THEN EXIT; END IF;
      COMMIT;
      PERFORM pg_sleep(0.1); -- Don't hammer DB
    END LOOP;
  END $$;
  
  -- Phase 3: Add NOT NULL constraint (after all rows filled)
  ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';
  ALTER TABLE users ALTER COLUMN status SET NOT NULL;
  
  -- Tools: pg_repack, pt-online-schema-change, gh-ost
  
### **Symptoms**
  - "Simple" migration takes hours
  - Application timeouts during migration
  - "We need a maintenance window" for column addition
### **Detection Pattern**
ALTER TABLE.*ADD COLUMN.*DEFAULT|ALTER TABLE.*ALTER COLUMN.*TYPE

## Soft Delete Query Leak

### **Id**
soft-delete-query-leak
### **Summary**
Soft delete records leak into queries missing the deletedAt filter
### **Severity**
high
### **Situation**
Using soft deletes but forgetting WHERE deletedAt IS NULL in some queries
### **Why**
  Developer writes new feature. Uses findMany without deletedAt filter.
  Deleted users appear in search results. Deleted orders show in reports.
  Bug discovered weeks later when customer complains about "deleted" data appearing.
  Every query in the entire codebase is now suspect.
  
### **Solution**
  -- WRONG: Manual deletedAt filter (easy to forget)
  const users = await prisma.user.findMany({
    where: { role: 'ADMIN' } // Forgot deletedAt!
  });
  
  -- RIGHT: Prisma middleware for automatic filtering
  prisma.$use(async (params, next) => {
    if (params.model === 'User') {
      if (params.action === 'findMany' || params.action === 'findFirst') {
        params.args.where = {
          ...params.args.where,
          deletedAt: null
        };
      }
    }
    return next(params);
  });
  
  -- RIGHT: Database views for soft delete
  CREATE VIEW active_users AS
    SELECT * FROM users WHERE deleted_at IS NULL;
  
  -- RIGHT: Drizzle with explicit filter helper
  const activeUsers = (table) => isNull(table.deletedAt);
  db.select().from(users).where(activeUsers(users));
  
### **Symptoms**
  - Deleted records appearing in UI
  - Count mismatches between "all" and "active"
  - Customer complaints about seeing deleted data
### **Detection Pattern**
findMany\\(|findFirst\\(|SELECT.*FROM.*(?!WHERE.*deleted)

## Cascade Delete Spiral

### **Id**
cascade-delete-spiral
### **Summary**
CASCADE DELETE triggers chain reaction across related tables
### **Severity**
high
### **Situation**
Deleting parent record with CASCADE relationships to large child tables
### **Why**
  User has 50,000 posts, each with comments, each with reactions. DELETE user triggers
  cascade. PostgreSQL deletes posts, which cascades to comments, which cascades to
  reactions. Transaction holds locks on all tables. Minutes pass. Other users can't
  create posts or comments. Application appears frozen.
  
### **Solution**
  -- WRONG: Deep cascade chains
  model User {
    posts Post[] @relation(onDelete: Cascade)
  }
  model Post {
    comments Comment[] @relation(onDelete: Cascade)
  }
  model Comment {
    reactions Reaction[] @relation(onDelete: Cascade)
  }
  -- DELETE FROM users WHERE id = 1 --> cascade nightmare
  
  -- RIGHT: Soft delete for users, background cleanup
  async function deleteUser(userId: string) {
    // Mark as deleted (instant)
    await prisma.user.update({
      where: { id: userId },
      data: { deletedAt: new Date() }
    });
  
    // Queue background job for cleanup
    await jobQueue.add('cleanup-user-data', { userId });
  }
  
  // Background worker - batched deletion
  async function cleanupUserData(userId: string) {
    let deleted = 1;
    while (deleted > 0) {
      const result = await prisma.post.deleteMany({
        where: { authorId: userId },
        take: 1000
      });
      deleted = result.count;
      await sleep(100); // Don't hammer DB
    }
  }
  
### **Symptoms**
  - DELETE statement runs for minutes
  - Transaction timeouts on simple-looking deletes
  - Lock waits spike when deleting "small" records
### **Detection Pattern**
onDelete:\\s*Cascade.*onDelete:\\s*Cascade|CASCADE.*CASCADE

## Decimal Precision Loss

### **Id**
decimal-precision-loss
### **Summary**
Using FLOAT/DOUBLE for money causes rounding errors
### **Severity**
high
### **Situation**
Storing prices, account balances, or financial calculations
### **Why**
  $19.99 stored as FLOAT becomes 19.989999771118164. Multiply by quantity, round
  for display, small errors accumulate. End of month, books don't balance by $47.23.
  Finance team asks questions. Nobody knows which transactions are wrong.
  
### **Solution**
  -- WRONG: Float for money
  model Product {
    price Float  // 19.99 becomes 19.989999...
  }
  
  -- RIGHT: Decimal with explicit precision
  model Product {
    price Decimal @db.Decimal(10, 2)  // Up to 99,999,999.99
  }
  
  model Account {
    balance Decimal @db.Decimal(15, 2)  // Larger for balances
  }
  
  -- RIGHT: Integer cents (avoid decimals entirely)
  model Product {
    priceInCents Int  // 1999 = $19.99
  }
  
  // Application layer converts
  const displayPrice = (cents: number) => (cents / 100).toFixed(2);
  const toCents = (dollars: number) => Math.round(dollars * 100);
  
### **Symptoms**
  - Financial reports off by small amounts
  - 0.1 + 0.2 !== 0.3 in calculations
  - Price displays as $19.989999999
### **Detection Pattern**
Float.*price|Float.*amount|Float.*balance|DOUBLE.*price

## Orm Enum Mismatch

### **Id**
orm-enum-mismatch
### **Summary**
ORM enum and database enum get out of sync
### **Severity**
medium
### **Situation**
Adding enum value in code but forgetting migration, or vice versa
### **Why**
  Developer adds 'ARCHIVED' to TypeScript enum. Forgets migration. Deploys. First
  request with status='ARCHIVED' crashes with "invalid input value for enum".
  Or worse: migration adds value, code doesn't know about it, validation fails.
  
### **Solution**
  -- WRONG: Enum in code only
  enum OrderStatus {
    PENDING = 'PENDING',
    SHIPPED = 'SHIPPED',
    ARCHIVED = 'ARCHIVED', // Added here but not in DB!
  }
  
  -- RIGHT: Single source of truth + sync check
  // Option 1: Generate TypeScript from database
  // prisma generate creates matching enum
  
  // Option 2: Startup validation
  async function validateEnums() {
    const dbValues = await prisma.$queryRaw`
      SELECT enumlabel FROM pg_enum
      WHERE enumtypid = 'order_status'::regtype
    `;
    const codeValues = Object.values(OrderStatus);
  
    const missing = codeValues.filter(v => !dbValues.includes(v));
    if (missing.length) {
      throw new Error(`DB missing enum values: ${missing.join(', ')}`);
    }
  }
  
  // Option 3: Use string with CHECK constraint instead of enum
  model Order {
    status String @default("PENDING")
    // CHECK (status IN ('PENDING', 'SHIPPED', 'ARCHIVED'))
  }
  
### **Symptoms**
  - "invalid input value for enum" errors after deploy
  - Works locally, fails in production
  - Enum drift between environments
### **Detection Pattern**
enum.*\\{[^}]*\\}

## N1 Migration Disaster

### **Id**
n1-migration-disaster
### **Summary**
Migration runs N queries instead of 1 for data transformation
### **Severity**
medium
### **Situation**
Data migration that loops and updates records one at a time
### **Why**
  Migration script updates 1 million rows. Uses ORM loop with await in each iteration.
  Each update is separate query + commit. Migration takes 6 hours. If it fails at
  row 500,000, you have half-migrated data and no easy way to resume.
  
### **Solution**
  -- WRONG: Loop with individual updates
  const users = await prisma.user.findMany();
  for (const user of users) {
    await prisma.user.update({
      where: { id: user.id },
      data: { fullName: `${user.firstName} ${user.lastName}` }
    }); // 1M users = 1M queries = hours
  }
  
  -- RIGHT: Single UPDATE statement
  await prisma.$executeRaw`
    UPDATE users
    SET full_name = first_name || ' ' || last_name
    WHERE full_name IS NULL
  `; // 1 query = seconds
  
  -- RIGHT: Batched for huge tables
  DO $$
  DECLARE
    affected INT;
  BEGIN
    LOOP
      UPDATE users
      SET full_name = first_name || ' ' || last_name
      WHERE id IN (
        SELECT id FROM users
        WHERE full_name IS NULL
        LIMIT 10000
      );
      GET DIAGNOSTICS affected = ROW_COUNT;
      IF affected = 0 THEN EXIT; END IF;
      COMMIT; -- Release locks between batches
    END LOOP;
  END $$;
  
### **Symptoms**
  - Migration "runs forever"
  - Database CPU pegged during migration
  - Migration files contain for loops with await
### **Detection Pattern**
for.*await.*update|forEach.*await.*update|map.*await.*update

## Timestamp Timezone Chaos

### **Id**
timestamp-timezone-chaos
### **Summary**
Storing timestamps without timezone causes confusion across regions
### **Severity**
medium
### **Situation**
Using TIMESTAMP instead of TIMESTAMPTZ, or not normalizing to UTC
### **Why**
  Order placed at 11 PM PST stored as 2024-01-15 23:00:00. Server in EST reads it
  as 11 PM EST. Order appears 3 hours late. Reports run at "midnight" show different
  data depending on which server runs them. DST changes cause ghost hours.
  
### **Solution**
  -- WRONG: Timestamp without timezone
  model Order {
    createdAt DateTime  // TIMESTAMP WITHOUT TIME ZONE
  }
  
  -- RIGHT: Always use TIMESTAMPTZ and store UTC
  model Order {
    createdAt DateTime @db.Timestamptz  // TIMESTAMP WITH TIME ZONE
  }
  
  -- PostgreSQL: Server should be in UTC
  ALTER DATABASE mydb SET timezone TO 'UTC';
  
  -- Application: Always store/compare in UTC
  const order = await prisma.order.create({
    data: {
      createdAt: new Date().toISOString() // UTC
    }
  });
  
  // Convert to user timezone only for display
  const userTime = new Date(order.createdAt).toLocaleString('en-US', {
    timeZone: user.timezone
  });
  
### **Symptoms**
  - Reports show different data at different times
  - Order placed yesterday shows as today
  - DST transitions cause data anomalies
### **Detection Pattern**
DateTime(?!.*Timestamptz)|TIMESTAMP(?!TZ| WITH TIME)