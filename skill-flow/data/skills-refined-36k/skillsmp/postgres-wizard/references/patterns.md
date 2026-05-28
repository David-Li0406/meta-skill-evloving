# PostgreSQL Wizard

## Patterns


---
  #### **Name**
EXPLAIN ANALYZE Deep Dive
  #### **Description**
Systematic query plan analysis for optimization
  #### **When**
Any slow query or performance investigation
  #### **Example**
    -- Enable timing and buffers for full picture
    EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
    SELECT m.*, e.name as entity_name
    FROM memories m
    JOIN memory_entities me ON m.memory_id = me.memory_id
    JOIN entities e ON me.entity_id = e.entity_id
    WHERE m.agent_id = 'agent-123'
      AND m.created_at > NOW() - INTERVAL '7 days'
    ORDER BY m.salience DESC
    LIMIT 100;
    
    -- Reading the plan (bottom-up):
    /*
    Limit  (cost=1234.56..1234.78 rows=100 width=256)
           (actual time=45.123..45.456 rows=100 loops=1)
      Buffers: shared hit=1234 read=56
      ->  Sort  (cost=1234.56..1245.67 rows=4500 width=256)
                (actual time=45.100..45.200 rows=100 loops=1)
            Sort Key: m.salience DESC
            Sort Method: top-N heapsort  Memory: 128kB
            Buffers: shared hit=1234 read=56
            ->  Nested Loop  (cost=0.87..1100.00 rows=4500 width=256)
                            (actual time=0.050..40.000 rows=4500 loops=1)
                  Buffers: shared hit=1234 read=56
                  ->  Index Scan using memories_agent_created_idx on memories m
                                (cost=0.43..500.00 rows=4500 width=200)
                                (actual time=0.030..10.000 rows=4500 loops=1)
                        Index Cond: ((agent_id = 'agent-123')
                                 AND (created_at > (now() - '7 days')))
                        Buffers: shared hit=500 read=20
                  ->  Index Scan using memory_entities_pkey on memory_entities me
                                (...)
    */
    
    -- Key metrics to check:
    -- 1. actual time vs estimated (bad estimates = stale stats)
    -- 2. rows vs expected (bad estimates = wrong plan)
    -- 3. shared hit vs read (low hit ratio = needs more memory)
    -- 4. Sort Method (external = needs work_mem tuning)
    
    -- Create covering index to eliminate table access
    CREATE INDEX CONCURRENTLY memories_agent_salience_covering
      ON memories (agent_id, created_at DESC)
      INCLUDE (salience, content_summary)
      WHERE created_at > NOW() - INTERVAL '30 days';
    

---
  #### **Name**
Partial and Expression Indexes
  #### **Description**
Targeted indexes for specific query patterns
  #### **When**
Hot query paths with predictable WHERE clauses
  #### **Example**
    -- Partial index: only index what you query
    -- 95% of queries are for recent, active memories
    CREATE INDEX CONCURRENTLY memories_recent_active
      ON memories (agent_id, created_at DESC)
      WHERE status = 'active'
        AND created_at > NOW() - INTERVAL '30 days';
    
    -- Expression index: index computed values
    -- Queries filter by lower(content)
    CREATE INDEX CONCURRENTLY memories_content_lower
      ON memories (agent_id, lower(content) text_pattern_ops);
    
    -- JSONB path index: index specific JSON paths
    CREATE INDEX CONCURRENTLY memories_metadata_type
      ON memories ((metadata->>'type'))
      WHERE metadata->>'type' IS NOT NULL;
    
    -- GIN index for JSONB containment queries
    CREATE INDEX CONCURRENTLY memories_metadata_gin
      ON memories USING gin (metadata jsonb_path_ops);
    
    -- Composite index with INCLUDE for covering queries
    CREATE INDEX CONCURRENTLY memories_lookup_covering
      ON memories (agent_id, memory_type, created_at DESC)
      INCLUDE (content_summary, salience, embedding_id)
      WHERE status = 'active';
    
    -- Verify index is used
    EXPLAIN (ANALYZE)
    SELECT * FROM memories
    WHERE agent_id = 'agent-123'
      AND status = 'active'
      AND created_at > NOW() - INTERVAL '7 days';
    

---
  #### **Name**
Table Partitioning Strategy
  #### **Description**
Time-based and hash partitioning for large tables
  #### **When**
Tables exceeding millions of rows with clear partition keys
  #### **Example**
    -- Time-based partitioning for memories
    CREATE TABLE memories (
        memory_id UUID PRIMARY KEY,
        agent_id UUID NOT NULL,
        content TEXT NOT NULL,
        embedding_id UUID,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        salience FLOAT DEFAULT 0.5
    ) PARTITION BY RANGE (created_at);
    
    -- Create partitions for each month
    CREATE TABLE memories_2024_01 PARTITION OF memories
        FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
    CREATE TABLE memories_2024_02 PARTITION OF memories
        FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
    -- ... more partitions
    
    -- Automate partition creation with pg_partman
    CREATE EXTENSION pg_partman;
    
    SELECT partman.create_parent(
        p_parent_table := 'public.memories',
        p_control := 'created_at',
        p_type := 'native',
        p_interval := 'monthly',
        p_premake := 3  -- Create 3 future partitions
    );
    
    -- Hash partitioning for even distribution
    CREATE TABLE embeddings (
        embedding_id UUID PRIMARY KEY,
        vector vector(1536) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    ) PARTITION BY HASH (embedding_id);
    
    CREATE TABLE embeddings_0 PARTITION OF embeddings
        FOR VALUES WITH (MODULUS 4, REMAINDER 0);
    CREATE TABLE embeddings_1 PARTITION OF embeddings
        FOR VALUES WITH (MODULUS 4, REMAINDER 1);
    CREATE TABLE embeddings_2 PARTITION OF embeddings
        FOR VALUES WITH (MODULUS 4, REMAINDER 2);
    CREATE TABLE embeddings_3 PARTITION OF embeddings
        FOR VALUES WITH (MODULUS 4, REMAINDER 3);
    
    -- Partition-wise operations
    -- PostgreSQL prunes partitions automatically
    EXPLAIN SELECT * FROM memories
    WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01';
    -- Shows: Seq Scan on memories_2024_01 (other partitions pruned)
    

---
  #### **Name**
Connection Pooling with PgBouncer
  #### **Description**
Proper connection pooling configuration
  #### **When**
Any production PostgreSQL deployment
  #### **Example**
    # pgbouncer.ini
    [databases]
    memory_service = host=127.0.0.1 port=5432 dbname=memory_service
    
    [pgbouncer]
    listen_addr = 0.0.0.0
    listen_port = 6432
    auth_type = scram-sha-256
    auth_file = /etc/pgbouncer/userlist.txt
    
    # Pool sizing
    # Rule: (pool_size * num_pools) <= max_connections - reserved
    default_pool_size = 20
    min_pool_size = 5
    reserve_pool_size = 5
    reserve_pool_timeout = 3
    
    # Pool mode
    # transaction: best for web apps (connection per transaction)
    # session: required for prepared statements, SET commands
    # statement: only for simple queries (rare)
    pool_mode = transaction
    
    # Timeouts
    server_idle_timeout = 300
    server_lifetime = 3600
    client_idle_timeout = 0
    query_timeout = 30
    query_wait_timeout = 120
    
    # Limits
    max_client_conn = 1000
    max_db_connections = 100
    
    # Logging
    log_connections = 1
    log_disconnections = 1
    log_pooler_errors = 1
    
    # Stats
    stats_period = 60
    admin_users = pgbouncer_admin
    
    ---
    -- Application connection string
    -- Connect to PgBouncer, not PostgreSQL directly
    DATABASE_URL=postgresql://user:pass@localhost:6432/memory_service
    
    -- Monitor pool usage
    -- Connect to pgbouncer admin database
    psql -h localhost -p 6432 -U pgbouncer_admin pgbouncer
    
    SHOW POOLS;
    SHOW STATS;
    SHOW CLIENTS;
    SHOW SERVERS;
    

## Anti-Patterns


---
  #### **Name**
SELECT * in Production
  #### **Description**
Fetching all columns when only a few are needed
  #### **Why**
Wastes I/O, prevents covering indexes, breaks when schema changes.
  #### **Instead**
Explicitly list needed columns, use INCLUDE indexes

---
  #### **Name**
Missing Connection Pooler
  #### **Description**
Apps connecting directly to PostgreSQL
  #### **Why**
PostgreSQL forks per connection (~10MB each). 100 connections = 1GB. Connection storms kill DB.
  #### **Instead**
Always use PgBouncer or built-in pooler (Supabase, RDS Proxy)

---
  #### **Name**
N+1 Query Pattern
  #### **Description**
Querying in app loop instead of JOINs or IN clauses
  #### **Why**
100 items = 101 round trips. Network latency dominates.
  #### **Instead**
JOIN at database level, use LATERAL for complex cases

---
  #### **Name**
Ignoring VACUUM
  #### **Description**
Not monitoring or tuning autovacuum
  #### **Why**
Dead tuples accumulate, table bloats, indexes bloat, queries slow down.
  #### **Instead**
Monitor pg_stat_user_tables.n_dead_tup, tune autovacuum per table

---
  #### **Name**
Indexes on Every Column
  #### **Description**
Creating indexes without query analysis
  #### **Why**
Indexes slow writes, consume storage, may never be used.
  #### **Instead**
Create indexes based on EXPLAIN analysis of actual queries