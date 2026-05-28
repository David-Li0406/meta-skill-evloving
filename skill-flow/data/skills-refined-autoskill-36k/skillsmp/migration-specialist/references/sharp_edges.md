# Migration Specialist - Sharp Edges

## Alter Table Lock

### **Id**
alter-table-lock
### **Summary**
ALTER TABLE locks entire table, blocks all writes
### **Severity**
critical
### **Situation**
Adding column or constraint to large table
### **Why**
  ALTER TABLE memories ADD COLUMN new_col TEXT;
  On 100M row table, this can take hours. During that time, table is locked.
  All writes blocked. Application times out. Users see errors.
  
### **Solution**
  1. For PostgreSQL, use CONCURRENTLY where possible:
     CREATE INDEX CONCURRENTLY idx ON table (col);
  
  2. For adding nullable column (fast in PostgreSQL 11+):
     ALTER TABLE memories ADD COLUMN new_col TEXT;  -- Instant if nullable
  
  3. For adding column with default (PostgreSQL 11+):
     ALTER TABLE memories ADD COLUMN new_col TEXT DEFAULT 'value';  -- Also instant
  
  4. For older PostgreSQL or other DBs:
     # 1. Add nullable column (fast)
     ALTER TABLE memories ADD COLUMN new_col TEXT;
     # 2. Backfill in batches
     UPDATE memories SET new_col = 'value'
     WHERE id BETWEEN 1 AND 10000;
     # 3. Add NOT NULL constraint
     ALTER TABLE memories ALTER COLUMN new_col SET NOT NULL;
  
  5. Use pg_repack for table rewrites:
     pg_repack -d mydb -t memories
  
### **Symptoms**
  - Application timeouts during migration
  - lock wait timeout exceeded
  - Writes queuing behind ALTER TABLE
### **Detection Pattern**
ALTER TABLE|ADD COLUMN|DROP COLUMN|ADD CONSTRAINT

## Foreign Key Add Scan

### **Id**
foreign-key-add-scan
### **Summary**
Adding foreign key scans entire table for validation
### **Severity**
high
### **Situation**
Adding foreign key constraint to existing table
### **Why**
  ALTER TABLE memories ADD CONSTRAINT fk_agent
    FOREIGN KEY (agent_id) REFERENCES agents(id);
  
  PostgreSQL must verify every row satisfies constraint.
  10M rows = full table scan = minutes to hours.
  Lock held during validation.
  
### **Solution**
  1. Add constraint as NOT VALID first (instant):
     ALTER TABLE memories
       ADD CONSTRAINT fk_agent
       FOREIGN KEY (agent_id) REFERENCES agents(id)
       NOT VALID;
  
  2. Validate separately (no lock on writes):
     ALTER TABLE memories VALIDATE CONSTRAINT fk_agent;
  
  3. Clean up invalid data first:
     DELETE FROM memories
     WHERE agent_id NOT IN (SELECT id FROM agents);
  
### **Symptoms**
  - Migration takes much longer than expected
  - Application blocked during constraint addition
  - "pending trigger events" errors
### **Detection Pattern**
FOREIGN KEY|REFERENCES|ADD CONSTRAINT

## Deploy Order Failure

### **Id**
deploy-order-failure
### **Summary**
Code and schema deployed in wrong order, breaks production
### **Severity**
critical
### **Situation**
Deploying code that depends on new schema before schema exists
### **Why**
  New code does: SELECT new_column FROM memories;
  Deploy code first. Schema not updated yet.
  Boom: "column new_column does not exist".
  All requests fail.
  
### **Solution**
  1. Schema changes MUST be backward compatible:
     # Phase 1: Add column (old code ignores it)
     # Phase 2: Deploy code that uses column (both work)
     # Phase 3: Remove old column support
  
  2. Use version checks in code:
     async def get_memory(id):
         if await schema_has_column('memories', 'new_col'):
             return await db.fetch("SELECT new_col...")
         return await db.fetch("SELECT old_col...")
  
  3. Deploy order checklist:
     - [ ] Can old code run with new schema? (expand)
     - [ ] Can new code run with old schema? (optional but safer)
     - [ ] Rollback tested?
  
  4. Use database migrations with dependency tracking:
     # Alembic/Django migrations run before app starts
  
### **Symptoms**
  - Immediate errors after deployment
  - "column does not exist" or "table does not exist"
  - Works in staging, fails in production
### **Detection Pattern**
deploy|release|migration.*order

## Backfill Timeout

### **Id**
backfill-timeout
### **Summary**
Backfill query times out or blocks production traffic
### **Severity**
high
### **Situation**
Updating existing rows with new column values
### **Why**
  UPDATE memories SET embedding = compute_embedding(content);
  10M rows × 100ms each = 11.5 days. But transaction times out.
  Even without timeout, locks resources the whole time.
  
### **Solution**
  1. Batch updates:
     DO $$
     DECLARE
         batch_size INT := 1000;
     BEGIN
         LOOP
             UPDATE memories
             SET embedding = compute_embedding(content)
             WHERE embedding IS NULL
               AND id IN (
                 SELECT id FROM memories
                 WHERE embedding IS NULL
                 LIMIT batch_size
                 FOR UPDATE SKIP LOCKED
             );
             IF NOT FOUND THEN EXIT; END IF;
             COMMIT;
             PERFORM pg_sleep(0.05);  -- Rate limit
         END LOOP;
     END $$;
  
  2. Use background job with progress tracking:
     class BackfillJob:
         async def run(self):
             last_id = await self.get_checkpoint()
             while True:
                 rows = await self.process_batch(after=last_id)
                 if not rows:
                     break
                 last_id = rows[-1].id
                 await self.save_checkpoint(last_id)
  
  3. Accept eventual consistency:
     # New rows get value immediately
     # Old rows backfilled asynchronously
     # Handle NULL in code during transition
  
### **Symptoms**
  - Migration times out
  - Production slowed during backfill
  - "statement timeout" errors
### **Detection Pattern**
UPDATE.*SET.*WHERE|backfill|batch

## Rollback Data Loss

### **Id**
rollback-data-loss
### **Summary**
Rollback loses data written after migration
### **Severity**
critical
### **Situation**
Rolling back migration that changed column type or structure
### **Why**
  Migrate: Change status from string to enum.
  New code writes enum values.
  Rollback: Old code can't read enum values.
  Either crash or data corruption.
  
### **Solution**
  1. Make migrations reversible:
     # Forward: Add new column, backfill, switch
     # Reverse: Switch back, drop new column
     # No data loss either direction
  
  2. Don't delete data during expand phase:
     # Keep old column until contract phase
     # Can always roll back to reading old column
  
  3. Version your data:
     UPDATE memories
     SET data = jsonb_set(data, '{version}', '2')
     WHERE ...
  
  4. Plan for rollback data handling:
     # Document: "Rows created after migration will need X on rollback"
  
### **Symptoms**
  - "Cannot deserialize" after rollback
  - Data corruption after rollback
  - New records missing after rollback
### **Detection Pattern**
rollback|revert|undo|backward

## Index Creation Lock

### **Id**
index-creation-lock
### **Summary**
CREATE INDEX blocks writes on table
### **Severity**
high
### **Situation**
Adding index to large table
### **Why**
  CREATE INDEX idx_agent ON memories (agent_id);
  Holds write lock for entire index build duration.
  On 100M rows, could be 30+ minutes.
  All inserts/updates blocked.
  
### **Solution**
  1. Use CONCURRENTLY (PostgreSQL):
     CREATE INDEX CONCURRENTLY idx_agent ON memories (agent_id);
     -- Takes longer but doesn't lock
  
  2. Handle concurrent index failure:
     # CONCURRENTLY can fail, leaving invalid index
     DROP INDEX CONCURRENTLY IF EXISTS idx_agent;
     CREATE INDEX CONCURRENTLY idx_agent ON memories (agent_id);
  
  3. Schedule during low traffic:
     # Even CONCURRENTLY adds load
     # Run during maintenance window if possible
  
  4. Monitor replication lag:
     # Large index builds cause replica lag
  
### **Symptoms**
  - Writes blocked during index creation
  - canceling statement due to lock timeout
  - Index marked as INVALID after failure
### **Detection Pattern**
CREATE INDEX|DROP INDEX|CONCURRENTLY

## Trigger Cascade Explosion

### **Id**
trigger-cascade-explosion
### **Summary**
Trigger causes cascade of updates during migration
### **Severity**
high
### **Situation**
Migration with triggers or cascading foreign keys
### **Why**
  UPDATE parent SET status = 'archived';
  Trigger on parent updates all children.
  Cascade to grandchildren.
  1 row becomes 10,000 updates.
  Transaction log explodes. Migration takes hours.
  
### **Solution**
  1. Disable triggers during bulk operations:
     ALTER TABLE memories DISABLE TRIGGER ALL;
     -- Do migration --
     ALTER TABLE memories ENABLE TRIGGER ALL;
  
  2. Use session_replication_role:
     SET session_replication_role = replica;
     -- Triggers don't fire --
     SET session_replication_role = DEFAULT;
  
  3. Be aware of cascade effects:
     # Check for ON UPDATE CASCADE, ON DELETE CASCADE
     # Estimate affected row counts
  
  4. Consider disabling foreign keys temporarily:
     ALTER TABLE child DROP CONSTRAINT fk_parent;
     -- Migrate --
     ALTER TABLE child ADD CONSTRAINT fk_parent ...;
  
### **Symptoms**
  - Migration much slower than expected
  - Transaction log growing rapidly
  - Unexpected rows being modified
### **Detection Pattern**
trigger|cascade|ON UPDATE|ON DELETE