-- Performance Auditor: Quick Query Analysis Script
-- Run this to get an overview of query performance issues

-- === QUICK HEALTH CHECK ===
-- Tables with high sequential scan rates (N+1 indicator)
SELECT
  tablename,
  seq_scan,
  idx_scan,
  CASE
    WHEN seq_scan > idx_scan * 10 THEN '🔴 CRITICAL: Likely N+1 or missing index'
    WHEN seq_scan > idx_scan THEN '🟡 WARNING: Consider index'
    ELSE '✅ OK'
  END as assessment,
  pg_size_pretty(pg_total_relation_size('public.' || tablename)) as table_size
FROM pg_stat_user_tables
WHERE schemaname = 'public'
  AND (seq_scan + idx_scan) > 100
ORDER BY seq_scan DESC
LIMIT 15;

-- === SLOWEST QUERIES ===
-- Queries taking the most total time
SELECT
  query,
  calls,
  ROUND(total_exec_time::numeric, 2) as total_ms,
  ROUND(mean_exec_time::numeric, 2) as mean_ms,
  ROUND(max_exec_time::numeric, 2) as max_ms,
  CASE
    WHEN mean_exec_time > 500 THEN '🔴 VERY SLOW'
    WHEN mean_exec_time > 100 THEN '🟡 SLOW'
    ELSE '✅ OK'
  END as speed
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat%'
  AND query NOT LIKE '%information_schema%'
ORDER BY total_exec_time DESC
LIMIT 10;

-- === FREQUENTLY CALLED QUERIES ===
-- Most called queries (good targets for optimization)
SELECT
  query,
  calls,
  ROUND(mean_exec_time::numeric, 2) as mean_ms,
  calls * ROUND(mean_exec_time::numeric, 2) as cumulative_impact,
  CASE
    WHEN calls * ROUND(mean_exec_time::numeric, 2) > 10000 THEN '🔴 HIGH IMPACT'
    WHEN calls * ROUND(mean_exec_time::numeric, 2) > 1000 THEN '🟡 MEDIUM IMPACT'
    ELSE '✅ LOW IMPACT'
  END as impact
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat%'
ORDER BY calls DESC
LIMIT 10;

-- === UNUSED INDEXES ===
-- Indexes not being used (candidates for removal)
SELECT
  indexname,
  tablename,
  idx_scan,
  pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
  CASE
    WHEN pg_relation_size(indexrelid) > 10 * 1024 * 1024 THEN '🔴 Large unused index'
    ELSE '🟡 Unused'
  END as concern
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
  AND indexname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 10;

-- === CACHE HIT RATIO ===
-- How effectively PostgreSQL is using indexes (should be > 99%)
SELECT
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit) as heap_hit,
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio,
  CASE
    WHEN sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) > 0.99 THEN '✅ Excellent'
    WHEN sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) > 0.95 THEN '🟡 Good'
    ELSE '🔴 Poor - consider indexes or more RAM'
  END as health
FROM pg_statio_user_tables
WHERE schemaname = 'public';

-- === NEXT STEPS ===
-- If you see issues:
-- 1. Red flags: Run EXPLAIN ANALYZE on the slow query
-- 2. Missing indexes: CREATE INDEX idx_name ON table(column);
-- 3. N+1 patterns: Check if query in loop or map()
-- 4. Large unused index: DROP INDEX IF EXISTS index_name;
