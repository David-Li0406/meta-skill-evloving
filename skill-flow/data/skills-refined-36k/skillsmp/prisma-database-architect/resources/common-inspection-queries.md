# Common Inspection Queries

This resource provides a collection of SQL queries useful for inspecting and debugging your PostgreSQL database.

## Usage

Execute these queries using the raw query script:

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "YOUR_QUERY_HERE"
```

## Database Overview

### Check Database Size

```sql
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### List All Tables

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### List All Columns in a Table

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'Session'
ORDER BY ordinal_position;
```

## Table Statistics

### Count Records in All Tables

```sql
SELECT
  schemaname,
  tablename,
  n_live_tup AS row_count
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;
```

### Check Table Bloat

```sql
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
  n_live_tup AS rows,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename) / NULLIF(n_live_tup, 0)) AS bytes_per_row
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY pg_relation_size(schemaname||'.'||tablename) DESC;
```

## Index Analysis

### List All Indexes

```sql
SELECT
  schemaname,
  tablename,
  indexname,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

### Check Index Usage

```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

### Find Unused Indexes

```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
ORDER BY tablename, indexname;
```

## Crawler-Specific Queries

### Check Recent Crawl Jobs

```sql
SELECT
  id,
  status,
  "playDate",
  "startedAt",
  "completedAt",
  "errorMessage"
FROM "CrawlJob"
ORDER BY "startedAt" DESC
LIMIT 5;
```

### Crawl Job Status Summary

```sql
SELECT
  status,
  COUNT(*) as count,
  MAX("startedAt") as last_run
FROM "CrawlJob"
WHERE "startedAt" > NOW() - INTERVAL '7 days'
GROUP BY status
ORDER BY count DESC;
```

### Inspect Session Availability by Date

```sql
SELECT
  date::date,
  COUNT(*) as total_sessions,
  COUNT(*) FILTER (WHERE available = true) as available_sessions
FROM "Session"
WHERE date >= CURRENT_DATE
GROUP BY date::date
ORDER BY date;
```

### Find Sessions by Facility Type

```sql
SELECT
  f.name as facility_name,
  ft.name as facility_type,
  COUNT(s) as session_count,
  COUNT(s) FILTER (WHERE s.available = true) as available_count
FROM "Facility" f
LEFT JOIN "FacilityType" ft ON f."facilityTypeId" = ft.id
LEFT JOIN "Session" s ON s."venueId" = f.id AND s.date >= CURRENT_DATE
GROUP BY f.id, f.name, ft.id, ft.name
ORDER BY session_count DESC;
```

### Check Dead Letter Queue

```sql
SELECT
  "faCode",
  date,
  error,
  attempts,
  status,
  "lastFailedAt"
FROM "DeadLetterEntry"
WHERE status != 'RESOLVED'
ORDER BY "lastFailedAt" DESC
LIMIT 10;
```

### Dead Letter Queue Summary

```sql
SELECT
  status,
  COUNT(*) as count,
  AVG(attempts) as avg_attempts,
  MAX("lastFailedAt") as last_failure
FROM "DeadLetterEntry"
GROUP BY status
ORDER BY count DESC;
```

## Data Integrity

### Check Orphaned Records

```sql
-- Find sessions without matching facilities
SELECT COUNT(*) as orphaned_sessions
FROM "Session" s
LEFT JOIN "Facility" f ON s."venueId" = f.id
WHERE f.id IS NULL;
```

### Find Duplicate Records

```sql
-- Find potential duplicate sessions
SELECT
  "venueId",
  "facilityCode",
  date,
  "startTime",
  COUNT(*) as count
FROM "Session"
GROUP BY "venueId", "facilityCode", date, "startTime"
HAVING COUNT(*) > 1;
```

### Check Foreign Key Constraints

```sql
SELECT
  conname AS constraint_name,
  conrelid::regclass AS table_name,
  confrelid::regclass AS referenced_table
FROM pg_constraint
WHERE contype = 'f'
  AND connamespace = 'public'::regnamespace;
```

## Performance Analysis

### Slow Queries (Requires pg_stat_statements extension)

```sql
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Table Scan Statistics

```sql
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  idx_tup_fetch,
  seq_scan / NULLIF((seq_scan + idx_scan), 0) * 100 AS seq_scan_pct
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY seq_scan DESC;
```

### Connection Statistics

```sql
SELECT
  state,
  COUNT(*) as connections
FROM pg_stat_activity
WHERE datname = current_database()
GROUP BY state;
```

## Data Distribution

### Session Distribution by District

```sql
SELECT
  d.name as district,
  COUNT(s) as total_sessions,
  COUNT(s) FILTER (WHERE s.available = true) as available_sessions
FROM "District" d
LEFT JOIN "Facility" f ON f."districtId" = d.id
LEFT JOIN "Session" s ON s."venueId" = f.id AND s.date >= CURRENT_DATE
GROUP BY d.id, d.name
ORDER BY total_sessions DESC;
```

### Facility Type Distribution

```sql
SELECT
  ft.name as facility_type,
  COUNT(DISTINCT f.id) as facility_count,
  COUNT(s) as session_count
FROM "FacilityType" ft
LEFT JOIN "Facility" f ON f."facilityTypeId" = ft.id
LEFT JOIN "Session" s ON s."venueId" = f.id AND s.date >= CURRENT_DATE
GROUP BY ft.id, ft.name
ORDER BY facility_count DESC;
```

## Maintenance

### Vacuum Analysis

```sql
SELECT
  schemaname,
  tablename,
  last_vacuum,
  last_autovacuum,
  vacuum_count,
  autovacuum_count
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY last_vacuum DESC NULLS LAST;
```

### Table Bloat Detailed

```sql
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Tips

1. **Use LIMIT**: Always add `LIMIT` to queries that might return many rows
2. **Filter by Date**: When querying sessions, always filter by date to reduce dataset size
3. **Aggregate First**: Use COUNT, SUM, AVG before fetching detailed records
4. **Explain Analyze**: Prefix queries with `EXPLAIN ANALYZE` to see execution plans:

   ```sql
   EXPLAIN ANALYZE SELECT * FROM "Session" WHERE date >= CURRENT_DATE;
   ```

## Related Resources

- [Database Inspection Workflow](./database-inspection-workflow.md)
- [Query Optimization Guide](./query-optimization-guide.md)
- [Best Practices](./best-practices.md)
