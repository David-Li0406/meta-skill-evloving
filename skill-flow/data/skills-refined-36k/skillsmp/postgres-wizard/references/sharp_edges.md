# Postgres Wizard - Sharp Edges

## Index Not Used

### **Id**
index-not-used
### **Summary**
Index exists but query planner ignores it
### **Severity**
high
### **Situation**
Created an index but EXPLAIN shows sequential scan
### **Why**
  PostgreSQL's planner estimates cost. Sometimes seq scan IS faster:
  - Small table (< few thousand rows)
  - Selecting > 5-10% of rows
  - Column statistics are stale (need ANALYZE)
  - Index column order doesn't match query
  - Expression in WHERE doesn't match index expression
  - Collation mismatch (especially with text_pattern_ops)
  
### **Solution**
  1. Run ANALYZE to update statistics:
     ANALYZE table_name;
  
  2. Check index column order matches query:
     -- Query: WHERE a = 1 AND b > 10 ORDER BY c
     -- Index: CREATE INDEX ON t (a, b, c) -- correct
     -- Index: CREATE INDEX ON t (c, a, b) -- wrong order
  
  3. For expression queries, create expression index:
     -- Query: WHERE lower(name) = 'john'
     CREATE INDEX ON users (lower(name));
  
  4. Check if you're selecting too many rows:
     SELECT n_live_tup FROM pg_stat_user_tables WHERE relname = 'table';
     -- If WHERE matches > 10% of rows, seq scan may be optimal
  
  5. Force index for testing (don't do in production):
     SET enable_seqscan = off;
     EXPLAIN ANALYZE SELECT ...;
  
### **Symptoms**
  - EXPLAIN shows "Seq Scan" despite index
  - Query slow on large table with obvious filter
  - Index exists in \di but never used
### **Detection Pattern**
Seq Scan|sequential scan|seqscan

## Transaction Id Wraparound

### **Id**
transaction-id-wraparound
### **Summary**
Database approaching transaction ID wraparound, requires vacuum
### **Severity**
critical
### **Situation**
Long-running transactions or inadequate vacuuming
### **Why**
  PostgreSQL uses 32-bit transaction IDs (4 billion). When you run out,
  the database shuts down to prevent data corruption. Anti-wraparound
  vacuum MUST run before this happens. Long-running transactions block
  vacuum from cleaning old XIDs.
  
### **Solution**
  1. Monitor age:
     SELECT datname, age(datfrozenxid) FROM pg_database;
     -- Warning at 200M, panic at 1B
  
  2. Check for long transactions:
     SELECT pid, now() - xact_start as duration, query
     FROM pg_stat_activity
     WHERE state = 'active'
     ORDER BY duration DESC;
  
  3. Tune autovacuum for high-churn tables:
     ALTER TABLE memories SET (
       autovacuum_vacuum_scale_factor = 0.01,
       autovacuum_analyze_scale_factor = 0.005
     );
  
  4. Emergency: manual vacuum freeze
     VACUUM FREEZE memories;
  
### **Symptoms**
  - WARNING logs about "oldest xmin" or "approaching wraparound"
  - Autovacuum constantly running on same table
  - Database suddenly read-only
### **Detection Pattern**
datfrozenxid|autovacuum_freeze|VACUUM FREEZE

## Bloated Tables

### **Id**
bloated-tables
### **Summary**
Table/index size much larger than actual data
### **Severity**
medium
### **Situation**
High UPDATE/DELETE workloads without proper vacuuming
### **Why**
  PostgreSQL uses MVCC - updates create new row versions, deletes mark
  rows as dead. Dead tuples aren't removed until VACUUM. If vacuum can't
  keep up, tables bloat. A 1GB table can become 10GB of mostly dead tuples.
  Queries scan all that dead space.
  
### **Solution**
  1. Check bloat:
     SELECT schemaname, tablename,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total,
            n_dead_tup
     FROM pg_stat_user_tables
     ORDER BY n_dead_tup DESC;
  
  2. Tune autovacuum for the table:
     ALTER TABLE memories SET (
       autovacuum_vacuum_threshold = 1000,
       autovacuum_vacuum_scale_factor = 0.05
     );
  
  3. For severe bloat, use pg_repack (online):
     CREATE EXTENSION pg_repack;
     pg_repack -d database -t bloated_table
  
  4. Or VACUUM FULL (locks table!):
     VACUUM FULL memories;  -- Blocks all access
  
### **Symptoms**
  - pg_total_relation_size much larger than data
  - n_dead_tup in millions
  - Slow queries on tables with lots of updates
### **Detection Pattern**
n_dead_tup|pg_repack|VACUUM FULL

## Lock Contention

### **Id**
lock-contention
### **Summary**
Queries waiting on locks, causing cascading slowdowns
### **Severity**
high
### **Situation**
Multiple transactions accessing same rows
### **Why**
  PostgreSQL has row-level locking, but some operations take table locks.
  DDL (ALTER TABLE, CREATE INDEX) blocks everything. Long transactions
  hold locks, causing other transactions to queue. The queue can grow
  faster than it drains, causing system-wide slowdown.
  
### **Solution**
  1. Check waiting queries:
     SELECT blocked_locks.pid AS blocked_pid,
            blocked_activity.query AS blocked_query,
            blocking_locks.pid AS blocking_pid,
            blocking_activity.query AS blocking_query
     FROM pg_locks blocked_locks
     JOIN pg_stat_activity blocked_activity ON blocked_locks.pid = blocked_activity.pid
     JOIN pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
       AND blocking_locks.relation = blocked_locks.relation
       AND blocking_locks.pid != blocked_locks.pid
     JOIN pg_stat_activity blocking_activity ON blocking_locks.pid = blocking_activity.pid
     WHERE NOT blocked_locks.granted;
  
  2. Use lock_timeout to fail fast:
     SET lock_timeout = '10s';
  
  3. Use CONCURRENTLY for indexes:
     CREATE INDEX CONCURRENTLY idx ON table (col);  -- Doesn't lock writes
  
  4. Keep transactions short:
     -- Bad: open transaction, process in app, commit
     -- Good: prepare in app, single transaction for DB ops
  
### **Symptoms**
  - Queries stuck in "waiting" state
  - pg_stat_activity shows "Lock" wait_event_type
  - Application timeouts during DDL
### **Detection Pattern**
pg_locks|lock_timeout|CONCURRENTLY

## Connection Exhaustion

### **Id**
connection-exhaustion
### **Summary**
"FATAL: too many connections" during traffic spikes
### **Severity**
high
### **Situation**
Production traffic without connection pooling
### **Why**
  Default max_connections is 100. Each connection consumes ~10MB.
  Apps without pooling open connection per request. Traffic spike =
  connection storm = database crashes or rejects connections.
  
### **Solution**
  1. Use connection pooler (PgBouncer):
     # Pool handles 1000 app connections with 20 DB connections
     default_pool_size = 20
     max_client_conn = 1000
  
  2. Tune max_connections with pooler:
     -- With pooler: lower is better
     max_connections = 50  -- Reserved for pooler + admin
  
  3. Monitor connections:
     SELECT count(*) FROM pg_stat_activity;
     SELECT usename, count(*) FROM pg_stat_activity GROUP BY usename;
  
  4. Set app-side pool limits:
     # asyncpg pool
     pool = await asyncpg.create_pool(
         min_size=5,
         max_size=20,
         command_timeout=30
     )
  
### **Symptoms**
  - FATAL: too many connections for role
  - Application connection timeouts
  - Database memory exhaustion
### **Detection Pattern**
max_connections|connection pool|PgBouncer

## Implicit Cast Prevents Index

### **Id**
implicit-cast-prevents-index
### **Summary**
Type mismatch causes implicit cast, bypassing index
### **Severity**
medium
### **Situation**
Query uses wrong type for indexed column
### **Why**
  If column is INTEGER but query uses '123' (string), PostgreSQL may
  cast every row to compare. Index on integer column can't be used
  for string comparison. Similar issues with timestamp vs date,
  UUID vs string.
  
### **Solution**
  1. Check column types:
     \d+ table_name
  
  2. Use explicit casts in queries:
     -- Column is UUID, parameter is string
     WHERE id = '123e4567-e89b-12d3-a456-426614174000'::uuid
  
  3. Check ORM parameter types match:
     # Python - use proper types
     cursor.execute("SELECT * FROM t WHERE id = %s", (uuid_obj,))  # Not str
  
  4. Create expression index if needed:
     CREATE INDEX ON table (id::text);  -- If queries always use text
  
### **Symptoms**
  - Index exists but EXPLAIN shows filter, not index cond
  - "::type" casts appearing in EXPLAIN output
  - Same query fast with literal, slow with parameter
### **Detection Pattern**
implicit cast|::text|::uuid|::integer

## Missing Statistics

### **Id**
missing-statistics
### **Summary**
Query planner makes wrong decisions due to stale stats
### **Severity**
medium
### **Situation**
After bulk loads or significant data changes
### **Why**
  PostgreSQL estimates row counts using statistics. After bulk inserts,
  deletes, or schema changes, stats are outdated. Planner chooses wrong
  join order, wrong index, or wrong scan type based on old numbers.
  
### **Solution**
  1. Run ANALYZE after bulk operations:
     ANALYZE table_name;
     ANALYZE;  -- All tables
  
  2. Check last analyze time:
     SELECT schemaname, relname, last_analyze, last_autoanalyze
     FROM pg_stat_user_tables;
  
  3. Increase statistics target for problematic columns:
     ALTER TABLE memories ALTER COLUMN agent_id SET STATISTICS 1000;
     ANALYZE memories;
  
  4. Tune autovacuum analyze threshold:
     ALTER TABLE memories SET (
       autovacuum_analyze_scale_factor = 0.01
     );
  
### **Symptoms**
  - EXPLAIN estimates wildly different from actual
  - rows=1000 (actual rows=1000000)
  - Slow queries after data migration
### **Detection Pattern**
ANALYZE|SET STATISTICS|analyze_scale_factor

## Pgvector Distance Gotchas

### **Id**
pgvector-distance-gotchas
### **Summary**
Vector search returns wrong results or is slow
### **Severity**
medium
### **Situation**
Using pgvector for similarity search
### **Why**
  pgvector has multiple distance functions with different semantics.
  L2 (Euclidean) and cosine similarity are NOT the same. Many embedding
  models produce normalized vectors (cosine = L2 for normalized).
  Wrong index type or distance function = wrong results.
  
### **Solution**
  1. Match distance function to your embeddings:
     -- OpenAI embeddings: use cosine or inner product
     -- Normalized vectors: L2 = cosine (use L2, it's faster)
  
  2. Create appropriate index:
     -- For cosine similarity (most common)
     CREATE INDEX ON embeddings USING ivfflat (vector vector_cosine_ops);
  
     -- For L2 distance
     CREATE INDEX ON embeddings USING ivfflat (vector vector_l2_ops);
  
     -- For inner product
     CREATE INDEX ON embeddings USING ivfflat (vector vector_ip_ops);
  
  3. Set appropriate lists for IVFFlat:
     -- Rule: lists = sqrt(rows)
     CREATE INDEX ON embeddings USING ivfflat (vector vector_cosine_ops)
       WITH (lists = 1000);  -- For ~1M vectors
  
  4. Tune probes for accuracy/speed tradeoff:
     SET ivfflat.probes = 10;  -- Higher = more accurate, slower
  
### **Symptoms**
  - Similar items not in top results
  - Vector search slower than expected
  - Results change after re-indexing
### **Detection Pattern**
vector_cosine_ops|vector_l2_ops|ivfflat|pgvector