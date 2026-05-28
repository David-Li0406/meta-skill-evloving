-- ClickHouse Schema Audit Script
-- ADR: 2025-12-09-clickhouse-architect-skill
-- Usage: clickhouse-client --multiquery < schema-audit.sql

-- ============================================================================
-- SECTION 1: Part Count Analysis (Critical: >300 parts = problem)
-- ============================================================================

SELECT '=== PART COUNT BY TABLE ===' AS section;

SELECT
    database,
    table,
    partition,
    count() AS parts,
    sum(rows) AS total_rows,
    formatReadableSize(sum(bytes_on_disk)) AS disk_size,
    CASE
        WHEN count() > 300 THEN 'CRITICAL'
        WHEN count() > 100 THEN 'WARNING'
        ELSE 'OK'
    END AS status
FROM system.parts
WHERE active = 1
GROUP BY database, table, partition
HAVING parts > 10
ORDER BY parts DESC
LIMIT 50;

-- ============================================================================
-- SECTION 2: Compression Analysis
-- ============================================================================

SELECT '=== COMPRESSION RATIO BY COLUMN ===' AS section;

SELECT
    database,
    table,
    column,
    type,
    compression_codec,
    formatReadableSize(data_compressed_bytes) AS compressed,
    formatReadableSize(data_uncompressed_bytes) AS uncompressed,
    round(data_uncompressed_bytes / data_compressed_bytes, 2) AS ratio
FROM system.columns
WHERE database NOT IN ('system', 'INFORMATION_SCHEMA', 'information_schema')
    AND data_compressed_bytes > 0
ORDER BY data_uncompressed_bytes DESC
LIMIT 100;

-- ============================================================================
-- SECTION 3: Table Engine and Settings
-- ============================================================================

SELECT '=== TABLE ENGINES AND SETTINGS ===' AS section;

SELECT
    database,
    name AS table,
    engine,
    partition_key,
    sorting_key,
    primary_key,
    formatReadableSize(total_bytes) AS total_size,
    total_rows
FROM system.tables
WHERE database NOT IN ('system', 'INFORMATION_SCHEMA', 'information_schema')
ORDER BY total_bytes DESC
LIMIT 50;

-- ============================================================================
-- SECTION 4: Query Performance Analysis (Last 24 hours)
-- ============================================================================

SELECT '=== SLOW QUERIES (Last 24h) ===' AS section;

SELECT
    type,
    query_kind,
    round(query_duration_ms / 1000, 2) AS duration_sec,
    formatReadableSize(memory_usage) AS memory,
    formatReadableSize(read_bytes) AS read_bytes,
    read_rows,
    substring(query, 1, 100) AS query_preview
FROM system.query_log
WHERE event_time > now() - INTERVAL 24 HOUR
    AND type = 'QueryFinish'
    AND query_duration_ms > 1000
ORDER BY query_duration_ms DESC
LIMIT 20;

-- ============================================================================
-- SECTION 5: Active Queries
-- ============================================================================

SELECT '=== ACTIVE QUERIES ===' AS section;

SELECT
    query_id,
    user,
    round(elapsed, 2) AS elapsed_sec,
    formatReadableSize(memory_usage) AS memory,
    formatReadableSize(read_bytes) AS read_bytes,
    substring(query, 1, 100) AS query_preview
FROM system.processes
ORDER BY elapsed DESC;

-- ============================================================================
-- SECTION 6: Replication Status (if applicable)
-- ============================================================================

SELECT '=== REPLICATION STATUS ===' AS section;

SELECT
    database,
    table,
    is_readonly,
    is_session_expired,
    future_parts,
    parts_to_check,
    queue_size,
    inserts_in_queue,
    merges_in_queue,
    log_pointer,
    CASE
        WHEN is_readonly = 1 THEN 'CRITICAL: READONLY'
        WHEN queue_size > 100 THEN 'WARNING: LARGE QUEUE'
        ELSE 'OK'
    END AS status
FROM system.replicas
ORDER BY queue_size DESC;

-- ============================================================================
-- SECTION 7: Disk Usage
-- ============================================================================

SELECT '=== DISK USAGE ===' AS section;

SELECT
    name,
    path,
    formatReadableSize(free_space) AS free_space,
    formatReadableSize(total_space) AS total_space,
    round(100 * (1 - free_space / total_space), 2) AS used_percent,
    CASE
        WHEN (1 - free_space / total_space) > 0.9 THEN 'CRITICAL'
        WHEN (1 - free_space / total_space) > 0.8 THEN 'WARNING'
        ELSE 'OK'
    END AS status
FROM system.disks;

-- ============================================================================
-- SECTION 8: Ongoing Merges
-- ============================================================================

SELECT '=== ONGOING MERGES ===' AS section;

SELECT
    database,
    table,
    elapsed,
    progress,
    num_parts,
    formatReadableSize(total_size_bytes_compressed) AS size,
    formatReadableSize(memory_usage) AS memory
FROM system.merges
ORDER BY elapsed DESC;

-- ============================================================================
-- SECTION 9: Memory Usage Metrics
-- ============================================================================

SELECT '=== MEMORY METRICS ===' AS section;

SELECT
    metric,
    formatReadableSize(value) AS value
FROM system.metrics
WHERE metric LIKE '%Memory%'
ORDER BY value DESC;

-- ============================================================================
-- SECTION 10: Index Effectiveness (Sample Query)
-- ============================================================================

SELECT '=== INDEX EFFECTIVENESS SAMPLE ===' AS section;

-- Run EXPLAIN on your critical queries to check index usage:
-- EXPLAIN indexes = 1
-- SELECT ...
-- FROM your_table
-- WHERE ...

SELECT
    'Run EXPLAIN indexes=1 on critical queries to check:' AS tip,
    '- SelectedParts vs TotalParts' AS metric_1,
    '- SelectedRanges and SelectedMarks' AS metric_2,
    '- Lower is better for all metrics' AS note;
