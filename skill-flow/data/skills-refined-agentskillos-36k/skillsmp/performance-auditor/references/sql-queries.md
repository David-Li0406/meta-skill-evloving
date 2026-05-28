# Database Performance SQL Queries

Comprehensive SQL queries for analyzing and optimizing database performance.

## Table of Contents
1. [Query Performance Analysis](#query-performance-analysis)
2. [Index Optimization](#index-optimization)
3. [Sequential Scan Detection](#sequential-scan-detection)
4. [Slow Query Detection](#slow-query-detection)

## Query Performance Analysis

Test query performance with EXPLAIN ANALYZE:

```sql
-- Test single verse lookup performance
EXPLAIN ANALYZE
SELECT * FROM public.get_verse_by_ref(
  'John', 3, 16, 'finstlk201', 'fi'
);

-- Test chapter lookup performance
EXPLAIN ANALYZE
SELECT * FROM public.get_chapter_by_ref(
  'Genesis', 1, 'finstlk201', 'fi'
);

-- Test search performance
EXPLAIN ANALYZE
SELECT * FROM public.search_text('rakkaus', 'finstlk201', 50);

-- Check execution time statistics
SELECT
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
WHERE query LIKE '%get_verse_by_ref%'
  OR query LIKE '%get_chapter_by_ref%'
  OR query LIKE '%search_text%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## Index Optimization

Find queries that need indexes:

```sql
-- Check for sequential scans (potential missing indexes)
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  seq_tup_read / NULLIF(seq_scan, 0) as avg_seq_tup_read,
  CASE
    WHEN seq_scan > idx_scan THEN 'Consider index'
    ELSE 'OK'
  END as recommendation
FROM pg_stat_user_tables
WHERE schemaname IN ('public', 'bible_schema')
ORDER BY seq_scan DESC
LIMIT 20;

-- Check index usage (find unused or underutilized indexes)
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname IN ('public', 'bible_schema')
ORDER BY idx_scan ASC
LIMIT 20;

-- Suggest indexes for frequently queried columns
SELECT
  'CREATE INDEX idx_' || table_name || '_' || column_name ||
  ' ON ' || table_schema || '.' || table_name || '(' || column_name || ');' as suggested_index
FROM information_schema.columns
WHERE table_schema IN ('public', 'bible_schema')
  AND table_name IN (
    SELECT tablename
    FROM pg_stat_user_tables
    WHERE seq_scan > 1000 AND seq_scan > idx_scan
  )
  AND column_name IN ('user_id', 'verse_id', 'created_at', 'osis', 'status');
```

## Sequential Scan Detection

Identify tables with high sequential scan ratios:

```sql
-- Sequential scans vs index scans ratio
SELECT
  schemaname,
  tablename,
  seq_scan,
  idx_scan,
  ROUND(100.0 * seq_scan / (seq_scan + idx_scan), 2) as seq_scan_ratio,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as table_size
FROM pg_stat_user_tables
WHERE schemaname IN ('public', 'bible_schema')
  AND (seq_scan + idx_scan) > 0
ORDER BY seq_scan DESC
LIMIT 20;
```

## Slow Query Detection

Find queries taking longest time:

```sql
-- Slowest queries by total time
SELECT
  query,
  calls,
  ROUND(total_exec_time::numeric, 2) as total_time_ms,
  ROUND(mean_exec_time::numeric, 2) as mean_time_ms,
  ROUND(max_exec_time::numeric, 2) as max_time_ms,
  ROUND(stddev_exec_time::numeric, 2) as stddev_time_ms
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat%'
ORDER BY total_exec_time DESC
LIMIT 20;

-- Most frequently called slow queries
SELECT
  query,
  calls,
  ROUND(mean_exec_time::numeric, 2) as mean_time_ms,
  ROUND(max_exec_time::numeric, 2) as max_time_ms,
  calls * ROUND(mean_exec_time::numeric, 2) as cumulative_impact
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat%'
  AND mean_exec_time > 50  -- Queries slower than 50ms
ORDER BY calls DESC
LIMIT 20;
```

## Interpretation Tips

- **seq_scan > idx_scan**: Likely missing index, but check if table is small (<10k rows)
- **avg_seq_tup_read > 1000**: Sequential scan is reading many rows, consider index
- **idx_tup_fetch low**: Index exists but not being used effectively
- **EXPLAIN ANALYZE planning time > 5ms**: Query planner overhead, consider simplifying query
