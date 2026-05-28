# Useful ThorDB Queries

## Performance Analysis

### Top Overall Time Sinks

```sql
SELECT category, element,
       count,
       duration/1e9 AS seconds_total,
       (duration*1.0/count)/1e9 AS seconds_avg
FROM times
ORDER BY duration DESC
LIMIT 30;
```

### Worst Average Time Per Invocation

Filter out one-off noise with count threshold:

```sql
SELECT category, element,
       count,
       (duration*1.0/count)/1e9 AS seconds_avg,
       duration/1e9 AS seconds_total
FROM times
WHERE count >= 5
ORDER BY (duration*1.0/count) DESC
LIMIT 30;
```

### Time by Category

```sql
SELECT category,
       SUM(count) AS total_invocations,
       SUM(duration)/1e9 AS total_seconds
FROM times
GROUP BY category
ORDER BY total_seconds DESC;
```

### Deep Scan Hotspots (YARA Rules)

```sql
SELECT element,
       count,
       duration/1e9 AS seconds,
       (duration*1.0/count)/1e9 AS avg_seconds
FROM times
WHERE category = 'deep_scan'
ORDER BY duration DESC
LIMIT 20;
```

### Bulk Scan Hotspots

```sql
SELECT element,
       count,
       duration/1e9 AS seconds
FROM times
WHERE category = 'bulk_scan'
ORDER BY duration DESC
LIMIT 20;
```

## Module Analysis

### Module Runtimes (Chronological)

```sql
SELECT module, element,
       datetime(started, 'unixepoch') AS start_time,
       duration AS seconds
FROM stats
ORDER BY started ASC;
```

### Slowest Modules

```sql
SELECT module,
       SUM(duration) AS total_seconds
FROM stats
GROUP BY module
ORDER BY total_seconds DESC;
```

### Recent Scans

```sql
SELECT DISTINCT
       datetime(started, 'unixepoch') AS scan_start,
       module
FROM stats
ORDER BY started DESC
LIMIT 50;
```

## Metadata Queries

### All Metadata Keys

```sql
SELECT key, value FROM tbl ORDER BY key;
```

### Schema Version

```sql
SELECT value FROM tbl WHERE key = 'schema_version';
```

### Resume State

```sql
SELECT key, value FROM tbl WHERE key LIKE 'resume%';
```

### Diff State

```sql
SELECT key, value FROM tbl WHERE key LIKE 'diff%';
```

## Export Queries

### Export Times to CSV

```sql
.mode csv
.headers on
.output times_export.csv
SELECT * FROM times ORDER BY duration DESC;
.output stdout
```

### Export Stats to CSV

```sql
.mode csv
.headers on
.output stats_export.csv
SELECT module, element, datetime(started, 'unixepoch') AS start_time, duration
FROM stats ORDER BY started DESC;
.output stdout
```

## Cleanup Queries

### Clear Timing Data (Reset Performance Stats)

```sql
DELETE FROM times;
VACUUM;
```

### Clear All Data (Full Reset)

```sql
DELETE FROM times;
DELETE FROM stats;
DELETE FROM tbl;
VACUUM;
```

**Note**: Clearing `tbl` removes resume markers and may affect `--resume` and `--diff` functionality.

## One-Liners

```bash
# Top 10 time sinks
sqlite3 thor10.db "SELECT element, duration/1e9 AS sec FROM times ORDER BY duration DESC LIMIT 10;"

# Total scan time by category
sqlite3 thor10.db "SELECT category, SUM(duration)/1e9 AS sec FROM times GROUP BY category;"

# Module durations from last scan
sqlite3 thor10.db "SELECT module, duration FROM stats ORDER BY started DESC LIMIT 10;"
```
