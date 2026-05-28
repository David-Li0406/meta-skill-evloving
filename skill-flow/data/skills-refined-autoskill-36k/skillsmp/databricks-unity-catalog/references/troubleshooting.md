# Unity Catalog Troubleshooting

Debugging procedures for common Unity Catalog errors.

## Table of Contents

- [Table Not Found](#table-not-found)
- [Access Denied / Permission Errors](#access-denied--permission-errors)
- [Data Quality Investigation](#data-quality-investigation)
- [Recent Changes Investigation](#recent-changes-investigation)

## Table Not Found

Step-by-step verification when a table cannot be found:

```sql
-- Step 1: Check if catalog exists
SHOW CATALOGS LIKE '<catalog>';

-- Step 2: Check if schema exists
SHOW SCHEMAS IN <catalog> LIKE '<schema>';

-- Step 3: Check if table exists
SHOW TABLES IN <catalog>.<schema> LIKE '<table>';

-- Step 4: Search with pattern (for typos)
SHOW TABLES IN <catalog>.<schema> LIKE '%<partial_name>%';

-- Step 5: Check current context
SELECT current_catalog(), current_schema();

-- Step 6: Search across schemas
SELECT table_catalog, table_schema, table_name
FROM <catalog>.information_schema.tables
WHERE table_name LIKE '%<partial_name>%';
```

### Common Causes

| Issue | Solution |
|-------|----------|
| Wrong catalog | Verify catalog with `SHOW CATALOGS` |
| Wrong schema | Verify schema with `SHOW SCHEMAS IN <catalog>` |
| Typo in name | Use `LIKE '%partial%'` pattern search |
| Table deleted | Check `DESCRIBE HISTORY` if table exists |
| No permission | See [Access Denied](#access-denied--permission-errors) |

## Access Denied / Permission Errors

Full permission verification procedure:

```sql
-- Step 1: Identify current user
SELECT current_user();

-- Step 2: Check catalog access
SHOW GRANTS ON CATALOG <catalog>;

-- Step 3: Check schema access
SHOW GRANTS ON SCHEMA <catalog>.<schema>;

-- Step 4: Check table access
SHOW GRANTS ON TABLE <catalog>.<schema>.<table>;

-- Step 5: Check grants to specific user
SHOW GRANTS TO `user@example.com`;
```

### Required Permissions for SELECT

All three levels must be granted:

```sql
-- 1. Catalog access
GRANT USE CATALOG ON CATALOG <catalog> TO `user@example.com`;

-- 2. Schema access
GRANT USE SCHEMA ON SCHEMA <catalog>.<schema> TO `user@example.com`;

-- 3. Table access
GRANT SELECT ON TABLE <catalog>.<schema>.<table> TO `user@example.com`;
```

### Permission Error Messages

| Error | Missing Permission |
|-------|-------------------|
| `CATALOG_NOT_FOUND` | `USE CATALOG` on catalog |
| `SCHEMA_NOT_FOUND` | `USE SCHEMA` on schema |
| `TABLE_OR_VIEW_NOT_FOUND` | `SELECT` on table (or table doesn't exist) |
| `PERMISSION_DENIED` | Specific privilege on object |

### Grant via Groups

For team access, grant to groups instead of individuals:

```sql
-- Grant to group (recommended)
GRANT USE CATALOG ON CATALOG <catalog> TO `data_analysts`;
GRANT USE SCHEMA ON SCHEMA <catalog>.<schema> TO `data_analysts`;
GRANT SELECT ON TABLE <catalog>.<schema>.<table> TO `data_analysts`;
```

## Data Quality Investigation

### NULL Value Analysis

```sql
SELECT
  COUNT(*) AS total_rows,
  COUNT(<column>) AS non_null_count,
  COUNT(*) - COUNT(<column>) AS null_count,
  ROUND(100.0 * (COUNT(*) - COUNT(<column>)) / COUNT(*), 2) AS null_pct
FROM <catalog>.<schema>.<table>;
```

### Duplicate Detection

```sql
-- Find duplicates in key column
SELECT <key_column>, COUNT(*) AS cnt
FROM <catalog>.<schema>.<table>
GROUP BY <key_column>
HAVING COUNT(*) > 1
ORDER BY cnt DESC
LIMIT 20;

-- Duplicate row details
WITH dups AS (
  SELECT <key_column>
  FROM <catalog>.<schema>.<table>
  GROUP BY <key_column>
  HAVING COUNT(*) > 1
)
SELECT t.*
FROM <catalog>.<schema>.<table> t
JOIN dups d ON t.<key_column> = d.<key_column>
ORDER BY t.<key_column>
LIMIT 100;
```

### Value Distribution

```sql
-- Distinct value count
SELECT COUNT(DISTINCT <column>) AS distinct_count
FROM <catalog>.<schema>.<table>;

-- Top values by frequency
SELECT <column>, COUNT(*) AS cnt
FROM <catalog>.<schema>.<table>
GROUP BY <column>
ORDER BY cnt DESC
LIMIT 20;

-- Numeric column statistics
SELECT
  MIN(<numeric_col>) AS min_val,
  MAX(<numeric_col>) AS max_val,
  AVG(<numeric_col>) AS avg_val,
  STDDEV(<numeric_col>) AS std_val,
  PERCENTILE(<numeric_col>, 0.5) AS median_val
FROM <catalog>.<schema>.<table>;
```

### Data Freshness

```sql
-- Latest record timestamp
SELECT MAX(<timestamp_col>) AS latest_record
FROM <catalog>.<schema>.<table>;

-- Records by date
SELECT DATE(<timestamp_col>) AS date, COUNT(*) AS row_count
FROM <catalog>.<schema>.<table>
GROUP BY DATE(<timestamp_col>)
ORDER BY date DESC
LIMIT 30;
```

## Recent Changes Investigation

### Table History Analysis

```sql
-- Recent operations
SELECT
  version,
  timestamp,
  userId,
  userName,
  operation,
  operationParameters,
  operationMetrics
FROM (DESCRIBE HISTORY <catalog>.<schema>.<table>)
ORDER BY version DESC
LIMIT 20;

-- Filter by operation type
SELECT *
FROM (DESCRIBE HISTORY <catalog>.<schema>.<table>)
WHERE operation IN ('WRITE', 'DELETE', 'UPDATE', 'MERGE')
ORDER BY version DESC
LIMIT 10;

-- Changes in last 24 hours
SELECT *
FROM (DESCRIBE HISTORY <catalog>.<schema>.<table>)
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS
ORDER BY version DESC;
```

### Compare Versions

```sql
-- Row count difference
SELECT
  (SELECT COUNT(*) FROM <catalog>.<schema>.<table> VERSION AS OF <new_version>) AS new_count,
  (SELECT COUNT(*) FROM <catalog>.<schema>.<table> VERSION AS OF <old_version>) AS old_count;

-- Added rows
SELECT * FROM <catalog>.<schema>.<table> VERSION AS OF <new_version>
EXCEPT
SELECT * FROM <catalog>.<schema>.<table> VERSION AS OF <old_version>;

-- Deleted rows
SELECT * FROM <catalog>.<schema>.<table> VERSION AS OF <old_version>
EXCEPT
SELECT * FROM <catalog>.<schema>.<table> VERSION AS OF <new_version>;
```

### Restore Previous Version

```sql
-- Restore to specific version
RESTORE TABLE <catalog>.<schema>.<table> TO VERSION AS OF <version>;

-- Restore to specific timestamp
RESTORE TABLE <catalog>.<schema>.<table> TO TIMESTAMP AS OF '<timestamp>';
```
