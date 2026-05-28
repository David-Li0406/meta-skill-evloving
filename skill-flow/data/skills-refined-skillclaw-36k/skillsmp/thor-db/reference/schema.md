# ThorDB Schema Reference

ThorDB is an SQLite database. Open with any SQLite client:

```bash
sqlite3 /var/lib/thor/thor10.db
```

## Tables Overview

| Table | Purpose |
|-------|---------|
| `times` | Fine-grained timing for hooks, deep_scan, bulk_scan elements |
| `stats` | Coarse module-level runtime stats per scan |
| `tbl` | Key-value metadata store (schema version, resume markers, etc.) |

## `times` Table

Accumulated timing data for performance analysis.

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `category` | TEXT | Category: `hooks`, `deep_scan`, `bulk_scan`, etc. |
| `element` | TEXT | Specific element (rule name, file type, etc.) |
| `count` | INTEGER | Number of invocations |
| `duration` | INTEGER | Total duration in nanoseconds |

### Notes

- `duration` is in nanoseconds (divide by 1e9 for seconds)
- Values accumulate across scans (not per-scan)
- High `count` with high `duration` = consistent slow element
- High `duration` with low `count` = occasional slow element

### Example Data

```
category   | element              | count  | duration
-----------+----------------------+--------+---------------
deep_scan  | HKTL_CobaltStrike    | 45230  | 89234000000
bulk_scan  | PE_Header_Check      | 128456 | 23456000000
hooks      | yara_callback        | 892341 | 156789000000
```

## `stats` Table

Module-level runtime statistics per scan run.

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `module` | TEXT | Module name (Filescan, ProcessCheck, etc.) |
| `element` | TEXT | Sub-element or empty |
| `started` | INTEGER | Unix timestamp when module started |
| `duration` | INTEGER | Duration in seconds |

### Notes

- `duration` is in seconds (not nanoseconds)
- One row per module per scan
- `started` allows chronological ordering

### Example Data

```
module         | element | started    | duration
---------------+---------+------------+---------
Filescan       |         | 1705234567 | 3421
ProcessCheck   |         | 1705238000 | 45
RegistryChecks |         | 1705238050 | 234
Eventlog       |         | 1705238300 | 567
```

## `tbl` Table

Generic key-value store for metadata.

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `key` | TEXT | Metadata key |
| `value` | TEXT/BLOB | Metadata value |

### Common Keys

| Key | Description |
|-----|-------------|
| `schema_version` | Database schema version |
| `last_run_id` | Identifier of last scan |
| `resume_*` | Resume markers for interrupted scans |
| `diff_*` | Delta comparison data |

### Example Data

```
key             | value
----------------+------------------
schema_version  | 3
last_run_id     | S-a1b2c3d4
resume_position | /path/to/last/file
```

## Schema Discovery

Dump full schema:
```sql
.schema
```

List all tables:
```sql
.tables
```

Describe a table:
```sql
PRAGMA table_info(times);
```
