# Migration Specialist

## Patterns


---
  #### **Name**
Expand-Contract Migration
  #### **Description**
Add new, migrate, remove old - never break compatibility
  #### **When**
Any schema change in production
  #### **Example**
    # Phase 1: EXPAND - Add new column (backward compatible)
    # Old code ignores new column, new code uses it
    
    -- Migration 001_add_embedding_v2.sql
    ALTER TABLE memories ADD COLUMN embedding_v2 vector(1536);
    
    -- Backfill in batches (doesn't lock table)
    UPDATE memories
    SET embedding_v2 = embedding_v1
    WHERE embedding_v2 IS NULL
      AND id IN (
        SELECT id FROM memories
        WHERE embedding_v2 IS NULL
        LIMIT 1000
      );
    
    # Phase 2: MIGRATE - Deploy code that writes to both
    class MemoryRepository:
        async def create(self, memory: Memory):
            # Write to both columns during transition
            await db.execute("""
                INSERT INTO memories (content, embedding_v1, embedding_v2)
                VALUES ($1, $2, $2)
            """, memory.content, memory.embedding)
    
        async def get(self, id: str):
            # Read from new column, fall back to old
            row = await db.fetchone("""
                SELECT *, COALESCE(embedding_v2, embedding_v1) as embedding
                FROM memories WHERE id = $1
            """, id)
            return Memory.from_row(row)
    
    # Phase 3: VERIFY - Confirm all rows migrated
    SELECT COUNT(*) FROM memories WHERE embedding_v2 IS NULL;
    -- Should be 0
    
    # Phase 4: SWITCH - Deploy code that only uses new column
    class MemoryRepository:
        async def create(self, memory: Memory):
            await db.execute("""
                INSERT INTO memories (content, embedding_v2)
                VALUES ($1, $2)
            """, memory.content, memory.embedding)
    
    # Phase 5: CONTRACT - Remove old column
    -- Migration 002_drop_embedding_v1.sql
    ALTER TABLE memories DROP COLUMN embedding_v1;
    

---
  #### **Name**
Zero-Downtime Column Rename
  #### **Description**
Rename column without breaking running code
  #### **When**
Renaming database columns
  #### **Example**
    # Problem: ALTER TABLE RENAME COLUMN breaks old code immediately
    # Solution: Use expand-contract pattern
    
    # Step 1: Add new column
    ALTER TABLE memories ADD COLUMN content_text TEXT;
    
    # Step 2: Backfill (online, batched)
    -- Run as background job
    DO $$
    DECLARE
        batch_size INT := 1000;
        affected INT;
    BEGIN
        LOOP
            UPDATE memories
            SET content_text = content
            WHERE content_text IS NULL
              AND id IN (
                SELECT id FROM memories
                WHERE content_text IS NULL
                LIMIT batch_size
                FOR UPDATE SKIP LOCKED
              );
            GET DIAGNOSTICS affected = ROW_COUNT;
            EXIT WHEN affected = 0;
            PERFORM pg_sleep(0.1);  -- Throttle
        END LOOP;
    END $$;
    
    # Step 3: Add trigger to keep in sync
    CREATE OR REPLACE FUNCTION sync_content()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.content_text := COALESCE(NEW.content_text, NEW.content);
        NEW.content := COALESCE(NEW.content, NEW.content_text);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER sync_content_trigger
    BEFORE INSERT OR UPDATE ON memories
    FOR EACH ROW EXECUTE FUNCTION sync_content();
    
    # Step 4: Deploy code using new column name
    # Step 5: Drop old column and trigger
    DROP TRIGGER sync_content_trigger ON memories;
    ALTER TABLE memories DROP COLUMN content;
    ALTER TABLE memories RENAME COLUMN content_text TO content;
    

---
  #### **Name**
Feature Flag Migration
  #### **Description**
Use feature flags to gradually roll out changes
  #### **When**
Risky changes that need gradual rollout
  #### **Example**
    from typing import Protocol
    import random
    
    class FeatureFlagService(Protocol):
        async def is_enabled(self, flag: str, user_id: str) -> bool: ...
    
    class MemoryService:
        def __init__(self, flags: FeatureFlagService):
            self.flags = flags
            self.old_repo = OldMemoryRepository()
            self.new_repo = NewMemoryRepository()
    
        async def store(self, memory: Memory, user_id: str):
            # Check if user should use new system
            use_new = await self.flags.is_enabled("new_memory_store", user_id)
    
            if use_new:
                return await self.new_repo.store(memory)
            else:
                return await self.old_repo.store(memory)
    
        async def retrieve(self, query: str, user_id: str):
            # Read from both during migration
            use_new = await self.flags.is_enabled("new_memory_store", user_id)
    
            if use_new:
                # Try new first, fall back to old
                results = await self.new_repo.search(query)
                if not results:
                    results = await self.old_repo.search(query)
                return results
            else:
                return await self.old_repo.search(query)
    
    # Feature flag rollout strategy:
    # 1. Enable for internal users (1%)
    # 2. Enable for beta users (5%)
    # 3. Enable for 10%, 25%, 50% random users
    # 4. Enable for all (100%)
    # 5. Remove flag and old code
    
    # LaunchDarkly / Unleash config:
    {
        "name": "new_memory_store",
        "strategies": [
            {"name": "userWithId", "parameters": {"userIds": "internal@company.com"}},
            {"name": "gradualRollout", "parameters": {"percentage": "10"}}
        ]
    }
    

---
  #### **Name**
Blue-Green Database Migration
  #### **Description**
Switch between database versions without downtime
  #### **When**
Major database changes or platform migrations
  #### **Example**
    # Blue-Green with read replica promotion
    
    # Phase 1: Set up Green (new) as replica of Blue (current)
    # - Create new database cluster
    # - Configure as streaming replica of Blue
    # - Apply schema changes to Green (won't affect replication)
    
    # Phase 2: Prepare application for switchover
    class DatabaseRouter:
        def __init__(self):
            self.blue_pool = create_pool(BLUE_DATABASE_URL)
            self.green_pool = create_pool(GREEN_DATABASE_URL)
            self.write_to = "blue"
            self.read_from = "blue"
    
        async def get_read_connection(self):
            if self.read_from == "green":
                return await self.green_pool.acquire()
            return await self.blue_pool.acquire()
    
        async def get_write_connection(self):
            if self.write_to == "green":
                return await self.green_pool.acquire()
            return await self.blue_pool.acquire()
    
    # Phase 3: Switch reads to Green
    router.read_from = "green"
    # Monitor for errors, performance
    
    # Phase 4: Stop writes, wait for replication, switch writes
    router.write_to = "green"
    # Green is now primary
    
    # Phase 5: Deprecate Blue
    # - Keep Blue running for quick rollback (24h)
    # - Then shut down Blue cluster
    

## Anti-Patterns


---
  #### **Name**
Big Bang Migration
  #### **Description**
Changing everything at once
  #### **Why**
No rollback path. Single failure takes down everything.
  #### **Instead**
Small steps with backward compatibility at each stage

---
  #### **Name**
Locking Migrations
  #### **Description**
ALTER TABLE that locks table for long time
  #### **Why**
Production traffic blocked. Users see errors.
  #### **Instead**
Use pg_repack, online DDL, or expand-contract

---
  #### **Name**
No Rollback Plan
  #### **Description**
We'll figure it out if something goes wrong
  #### **Why**
Something WILL go wrong. Panic leads to more mistakes.
  #### **Instead**
Write rollback migration. Test rollback. Document steps.

---
  #### **Name**
Schema-Code Coupling
  #### **Description**
Deploying schema and code changes together
  #### **Why**
If one fails, both must roll back. Complex coordination.
  #### **Instead**
Make schema changes backward compatible. Deploy separately.

---
  #### **Name**
Testing Only on Empty Database
  #### **Description**
Migrations tested without production-scale data
  #### **Why**
Works on 100 rows. Times out on 100 million rows.
  #### **Instead**
Test on production data clone. Measure migration time.