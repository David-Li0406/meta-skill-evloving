# Unity Catalog Lineage Analysis

Comprehensive guide for data lineage tracking, impact analysis, and data flow investigation.

## Table of Contents

- [Lineage System Tables](#lineage-system-tables)
- [Table Lineage Analysis](#table-lineage-analysis)
- [Column Lineage Analysis](#column-lineage-analysis)
- [Dependency Mapping](#dependency-mapping)
- [Impact Analysis](#impact-analysis)
- [Entity Types and Relationships](#entity-types-and-relationships)
- [Workflow and Job Lineage](#workflow-and-job-lineage)
- [Lineage Quality and Coverage](#lineage-quality-and-coverage)
- [Lineage API Reference](#lineage-api-reference)
- [Change Data Feed](#change-data-feed)

## Lineage System Tables

Unity Catalog tracks lineage automatically in system tables:

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `system.access.table_lineage` | Table-level lineage | `source_table_full_name`, `target_table_full_name`, `event_time` |
| `system.access.column_lineage` | Column-level lineage | `source_column_name`, `target_column_name`, `source_table_full_name` |

### Table Lineage Schema

```sql
DESCRIBE TABLE system.access.table_lineage;
-- Key columns:
-- source_table_full_name: STRING - Fully qualified source table name
-- source_table_catalog: STRING - Source catalog name
-- source_table_schema: STRING - Source schema name
-- source_table_name: STRING - Source table name
-- source_type: STRING - Entity type (TABLE, VIEW, NOTEBOOK, etc.)
-- target_table_full_name: STRING - Fully qualified target table name
-- target_table_catalog: STRING - Target catalog name
-- target_table_schema: STRING - Target schema name
-- target_table_name: STRING - Target table name
-- target_type: STRING - Entity type
-- event_time: TIMESTAMP - When lineage was captured
-- event_type: STRING - Type of operation (WRITE, READ, etc.)
-- entity_type: STRING - Source entity type (TABLE, PATH, NOTEBOOK)
-- entity_id: STRING - Unique entity identifier
```

### Column Lineage Schema

```sql
DESCRIBE TABLE system.access.column_lineage;
-- Key columns:
-- source_table_full_name: STRING
-- source_column_name: STRING
-- target_table_full_name: STRING
-- target_column_name: STRING
-- event_time: TIMESTAMP
```

## Table Lineage Analysis

### Upstream Analysis (Data Sources)

Find all tables that feed data into a target table:

```sql
-- Direct upstream tables
SELECT DISTINCT
  source_table_full_name,
  source_type,
  COUNT(*) AS connection_count,
  MAX(event_time) AS last_event
FROM system.access.table_lineage
WHERE target_table_full_name = '<catalog>.<schema>.<table>'
GROUP BY source_table_full_name, source_type
ORDER BY last_event DESC;

-- Upstream with event details
SELECT
  source_table_full_name,
  source_type,
  event_type,
  event_time,
  entity_type,
  entity_id
FROM system.access.table_lineage
WHERE target_table_full_name = '<catalog>.<schema>.<table>'
ORDER BY event_time DESC
LIMIT 100;
```

### Downstream Analysis (Data Consumers)

Find all tables that consume data from a source table:

```sql
-- Direct downstream tables
SELECT DISTINCT
  target_table_full_name,
  target_type,
  COUNT(*) AS connection_count,
  MAX(event_time) AS last_event
FROM system.access.table_lineage
WHERE source_table_full_name = '<catalog>.<schema>.<table>'
GROUP BY target_table_full_name, target_type
ORDER BY last_event DESC;

-- Downstream with entity details
SELECT
  target_table_full_name,
  target_type,
  entity_type,
  entity_id,
  event_time
FROM system.access.table_lineage
WHERE source_table_full_name = '<catalog>.<schema>.<table>'
ORDER BY event_time DESC;
```

### Lineage Timeline

Track how lineage evolved over time:

```sql
-- Lineage events over time
SELECT
  DATE(event_time) AS event_date,
  source_table_full_name,
  target_table_full_name,
  event_type,
  COUNT(*) AS event_count
FROM system.access.table_lineage
WHERE target_table_full_name = '<catalog>.<schema>.<table>'
  AND event_time >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
ORDER BY event_date DESC, event_count DESC;

-- First and last seen connections
SELECT
  source_table_full_name,
  target_table_full_name,
  MIN(event_time) AS first_seen,
  MAX(event_time) AS last_seen,
  COUNT(*) AS total_events
FROM system.access.table_lineage
WHERE target_table_full_name = '<catalog>.<schema>.<table>'
GROUP BY source_table_full_name, target_table_full_name
ORDER BY last_seen DESC;
```

## Column Lineage Analysis

### Column-Level Data Flow

```sql
-- All source columns for a target table
SELECT DISTINCT
  source_table_full_name,
  source_column_name,
  target_column_name,
  MAX(event_time) AS last_event
FROM system.access.column_lineage
WHERE target_table_full_name = '<catalog>.<schema>.<table>'
GROUP BY source_table_full_name, source_column_name, target_column_name
ORDER BY target_column_name, source_table_full_name;

-- Source columns for specific target column
SELECT
  source_table_full_name,
  source_column_name,
  event_time
FROM system.access.column_lineage
WHERE target_table_full_name = '<catalog>.<schema>.<table>'
  AND target_column_name = '<column_name>'
ORDER BY event_time DESC;

-- Columns affected by a source column change
SELECT DISTINCT
  target_table_full_name,
  target_column_name,
  MAX(event_time) AS last_event
FROM system.access.column_lineage
WHERE source_table_full_name = '<catalog>.<schema>.<table>'
  AND source_column_name = '<column_name>'
GROUP BY target_table_full_name, target_column_name
ORDER BY last_event DESC;
```

### Column Transformation Mapping

```sql
-- Full column mapping for a table
SELECT
  target_column_name,
  COLLECT_LIST(STRUCT(source_table_full_name, source_column_name)) AS source_columns
FROM system.access.column_lineage
WHERE target_table_full_name = '<catalog>.<schema>.<table>'
GROUP BY target_column_name
ORDER BY target_column_name;

-- Columns with multiple sources (potential joins or unions)
SELECT
  target_table_full_name,
  target_column_name,
  COUNT(DISTINCT source_table_full_name) AS source_table_count,
  COUNT(DISTINCT source_column_name) AS source_column_count
FROM system.access.column_lineage
GROUP BY target_table_full_name, target_column_name
HAVING COUNT(DISTINCT source_table_full_name) > 1
ORDER BY source_table_count DESC;
```

## Dependency Mapping

### Recursive Upstream Dependencies

Find all tables in the dependency chain (full data provenance):

```sql
-- All upstream dependencies (recursive)
WITH RECURSIVE deps AS (
  -- Direct dependencies
  SELECT DISTINCT
    source_table_full_name AS table_name,
    target_table_full_name AS dependent_table,
    1 AS depth
  FROM system.access.table_lineage
  WHERE target_table_full_name = '<catalog>.<schema>.<table>'

  UNION ALL

  -- Indirect dependencies
  SELECT DISTINCT
    l.source_table_full_name,
    d.table_name,
    d.depth + 1
  FROM system.access.table_lineage l
  JOIN deps d ON l.target_table_full_name = d.table_name
  WHERE d.depth < 10  -- Prevent infinite loops
)
SELECT
  table_name,
  MIN(depth) AS min_depth,
  COUNT(*) AS path_count
FROM deps
GROUP BY table_name
ORDER BY min_depth, table_name;
```

### Recursive Downstream Dependencies

Find all tables affected downstream:

```sql
-- All downstream dependents (recursive)
WITH RECURSIVE impact AS (
  -- Direct dependents
  SELECT DISTINCT
    target_table_full_name AS table_name,
    source_table_full_name AS source_table,
    1 AS depth
  FROM system.access.table_lineage
  WHERE source_table_full_name = '<catalog>.<schema>.<table>'

  UNION ALL

  -- Indirect dependents
  SELECT DISTINCT
    l.target_table_full_name,
    i.table_name,
    i.depth + 1
  FROM system.access.table_lineage l
  JOIN impact i ON l.source_table_full_name = i.table_name
  WHERE i.depth < 10
)
SELECT
  table_name,
  MIN(depth) AS min_depth,
  COUNT(*) AS path_count
FROM impact
GROUP BY table_name
ORDER BY min_depth, table_name;
```

### Dependency Graph Metrics

```sql
-- Tables with most dependencies (upstream)
SELECT
  target_table_full_name AS table_name,
  COUNT(DISTINCT source_table_full_name) AS upstream_count
FROM system.access.table_lineage
GROUP BY target_table_full_name
ORDER BY upstream_count DESC
LIMIT 20;

-- Most referenced tables (downstream)
SELECT
  source_table_full_name AS table_name,
  COUNT(DISTINCT target_table_full_name) AS downstream_count
FROM system.access.table_lineage
GROUP BY source_table_full_name
ORDER BY downstream_count DESC
LIMIT 20;

-- Hub tables (high upstream AND downstream)
WITH upstream AS (
  SELECT target_table_full_name AS table_name, COUNT(DISTINCT source_table_full_name) AS up_count
  FROM system.access.table_lineage GROUP BY 1
),
downstream AS (
  SELECT source_table_full_name AS table_name, COUNT(DISTINCT target_table_full_name) AS down_count
  FROM system.access.table_lineage GROUP BY 1
)
SELECT
  COALESCE(u.table_name, d.table_name) AS table_name,
  COALESCE(u.up_count, 0) AS upstream_count,
  COALESCE(d.down_count, 0) AS downstream_count,
  COALESCE(u.up_count, 0) + COALESCE(d.down_count, 0) AS total_connections
FROM upstream u
FULL OUTER JOIN downstream d ON u.table_name = d.table_name
ORDER BY total_connections DESC
LIMIT 20;
```

## Impact Analysis

### Schema Change Impact

Before modifying a table schema, assess downstream impact:

```sql
-- Tables affected by schema change
SELECT
  l.target_table_full_name,
  COUNT(DISTINCT l.target_column_name) AS affected_columns,
  MAX(l.event_time) AS last_usage
FROM system.access.column_lineage l
WHERE l.source_table_full_name = '<catalog>.<schema>.<table>'
GROUP BY l.target_table_full_name
ORDER BY affected_columns DESC;

-- Column-level impact details
SELECT
  target_table_full_name,
  target_column_name,
  source_column_name
FROM system.access.column_lineage
WHERE source_table_full_name = '<catalog>.<schema>.<table>'
  AND source_column_name IN ('<col1>', '<col2>')  -- Columns being modified
ORDER BY target_table_full_name, target_column_name;
```

### Breaking Change Detection

```sql
-- Find potential breaking changes (tables reading dropped columns)
WITH dropped_columns AS (
  SELECT '<catalog>.<schema>.<table>' AS table_name, '<column_name>' AS column_name
  -- Add more dropped columns as needed
)
SELECT
  cl.target_table_full_name,
  cl.target_column_name,
  dc.column_name AS dropped_source_column
FROM system.access.column_lineage cl
JOIN dropped_columns dc
  ON cl.source_table_full_name = dc.table_name
  AND cl.source_column_name = dc.column_name
ORDER BY cl.target_table_full_name;
```

### Critical Path Analysis

```sql
-- Tables with single source (high impact if source fails)
WITH source_counts AS (
  SELECT
    target_table_full_name,
    COUNT(DISTINCT source_table_full_name) AS source_count
  FROM system.access.table_lineage
  GROUP BY target_table_full_name
)
SELECT
  l.target_table_full_name,
  l.source_table_full_name AS single_source
FROM system.access.table_lineage l
JOIN source_counts sc ON l.target_table_full_name = sc.target_table_full_name
WHERE sc.source_count = 1
ORDER BY l.target_table_full_name;
```

## Entity Types and Relationships

### Entity Type Analysis

```sql
-- Lineage by entity type
SELECT
  entity_type,
  source_type,
  target_type,
  COUNT(*) AS lineage_count
FROM system.access.table_lineage
GROUP BY entity_type, source_type, target_type
ORDER BY lineage_count DESC;

-- Non-table sources (notebooks, paths, etc.)
SELECT DISTINCT
  entity_type,
  entity_id,
  target_table_full_name,
  MAX(event_time) AS last_event
FROM system.access.table_lineage
WHERE entity_type != 'TABLE'
GROUP BY entity_type, entity_id, target_table_full_name
ORDER BY last_event DESC;
```

### External Source Tracking

```sql
-- Tables sourced from external paths
SELECT
  source_table_full_name,
  target_table_full_name,
  entity_type,
  COUNT(*) AS event_count
FROM system.access.table_lineage
WHERE source_type = 'PATH' OR entity_type = 'PATH'
GROUP BY ALL
ORDER BY event_count DESC;

-- Notebook-originated lineage
SELECT
  entity_id AS notebook_path,
  target_table_full_name,
  COUNT(*) AS write_count,
  MAX(event_time) AS last_write
FROM system.access.table_lineage
WHERE entity_type = 'NOTEBOOK'
GROUP BY entity_id, target_table_full_name
ORDER BY last_write DESC;
```

## Workflow and Job Lineage

### Job-Table Relationships

```sql
-- Tables modified by jobs (via entity tracking)
SELECT
  entity_id AS job_or_notebook,
  entity_type,
  target_table_full_name,
  COUNT(*) AS modification_count,
  MAX(event_time) AS last_modification
FROM system.access.table_lineage
WHERE entity_type IN ('JOB', 'NOTEBOOK', 'WORKFLOW')
GROUP BY entity_id, entity_type, target_table_full_name
ORDER BY last_modification DESC;
```

### Cross-Schema Lineage

```sql
-- Lineage crossing schema boundaries
SELECT
  source_table_schema,
  target_table_schema,
  COUNT(DISTINCT source_table_full_name) AS source_table_count,
  COUNT(DISTINCT target_table_full_name) AS target_table_count,
  COUNT(*) AS connection_count
FROM system.access.table_lineage
WHERE source_table_schema != target_table_schema
GROUP BY source_table_schema, target_table_schema
ORDER BY connection_count DESC;

-- Cross-catalog lineage
SELECT
  source_table_catalog,
  target_table_catalog,
  COUNT(DISTINCT source_table_full_name) AS source_table_count,
  COUNT(DISTINCT target_table_full_name) AS target_table_count
FROM system.access.table_lineage
WHERE source_table_catalog != target_table_catalog
GROUP BY source_table_catalog, target_table_catalog
ORDER BY source_table_count DESC;
```

## Lineage Quality and Coverage

### Lineage Coverage Assessment

```sql
-- Tables with lineage vs without
WITH all_tables AS (
  SELECT table_catalog || '.' || table_schema || '.' || table_name AS full_name
  FROM system.information_schema.tables
  WHERE table_schema NOT IN ('information_schema')
),
tables_with_lineage AS (
  SELECT DISTINCT target_table_full_name AS full_name
  FROM system.access.table_lineage
  UNION
  SELECT DISTINCT source_table_full_name
  FROM system.access.table_lineage
)
SELECT
  (SELECT COUNT(*) FROM all_tables) AS total_tables,
  (SELECT COUNT(*) FROM tables_with_lineage) AS tables_with_lineage,
  ROUND(100.0 * (SELECT COUNT(*) FROM tables_with_lineage) /
    NULLIF((SELECT COUNT(*) FROM all_tables), 0), 2) AS coverage_pct;

-- Tables without any lineage
SELECT t.full_name
FROM (
  SELECT table_catalog || '.' || table_schema || '.' || table_name AS full_name
  FROM system.information_schema.tables
  WHERE table_schema NOT IN ('information_schema')
) t
LEFT JOIN (
  SELECT DISTINCT target_table_full_name AS full_name FROM system.access.table_lineage
  UNION
  SELECT DISTINCT source_table_full_name FROM system.access.table_lineage
) l ON t.full_name = l.full_name
WHERE l.full_name IS NULL;
```

### Stale Lineage Detection

```sql
-- Lineage not updated recently (potential stale data)
SELECT
  source_table_full_name,
  target_table_full_name,
  MAX(event_time) AS last_event,
  DATEDIFF(CURRENT_DATE, MAX(event_time)) AS days_since_last_event
FROM system.access.table_lineage
GROUP BY source_table_full_name, target_table_full_name
HAVING DATEDIFF(CURRENT_DATE, MAX(event_time)) > 30
ORDER BY days_since_last_event DESC;
```

## Lineage API Reference

### Table Lineage API

```bash
# Get table lineage (includes upstream and downstream)
databricks api get /api/2.1/unity-catalog/lineage/table-lineage \
  --json '{
    "table_name": "<catalog>.<schema>.<table>",
    "include_entity_lineage": true
  }'

# Response structure:
# {
#   "upstreams": [{"tableInfo": {...}, "notebookInfos": [...]}],
#   "downstreams": [{"tableInfo": {...}}]
# }
```

### Column Lineage API

```bash
# Get column lineage
databricks api get /api/2.1/unity-catalog/lineage/column-lineage \
  --json '{
    "table_name": "<catalog>.<schema>.<table>",
    "column_name": "<column_name>"
  }'

# Response structure:
# {
#   "upstream_cols": [{"name": "col", "catalog_name": "...", ...}],
#   "downstream_cols": [...]
# }
```

### Batch Lineage Queries

```bash
# Query lineage for multiple tables
for table in catalog.schema.table1 catalog.schema.table2; do
  databricks api get /api/2.1/unity-catalog/lineage/table-lineage \
    --json "{\"table_name\": \"$table\"}"
done
```

## Change Data Feed

Track row-level changes for fine-grained lineage:

### Enable Change Data Feed

```sql
-- Enable on existing table
ALTER TABLE <catalog>.<schema>.<table>
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- Create table with CDF enabled
CREATE TABLE <catalog>.<schema>.<new_table> (
  id INT,
  value STRING
) TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

### Query Changes

```sql
-- Changes between versions
SELECT
  _change_type,
  _commit_version,
  _commit_timestamp,
  *
FROM table_changes('<catalog>.<schema>.<table>', <start_version>, <end_version>);

-- Changes since timestamp
SELECT *
FROM table_changes('<catalog>.<schema>.<table>', '<start_timestamp>', '<end_timestamp>');

-- Change summary by type
SELECT
  _change_type,
  COUNT(*) AS row_count
FROM table_changes('<catalog>.<schema>.<table>', <start_version>)
GROUP BY _change_type;

-- Change types:
-- 'insert' - New row added
-- 'update_preimage' - Row value before update
-- 'update_postimage' - Row value after update
-- 'delete' - Row was deleted
```

### Track Data Modifications

```sql
-- Daily change volume
SELECT
  DATE(_commit_timestamp) AS change_date,
  _change_type,
  COUNT(*) AS row_count
FROM table_changes('<catalog>.<schema>.<table>', CURRENT_DATE - INTERVAL 7 DAYS)
GROUP BY ALL
ORDER BY change_date DESC, _change_type;

-- Identify high-churn records
SELECT
  <key_column>,
  COUNT(*) AS change_count
FROM table_changes('<catalog>.<schema>.<table>', <start_version>)
GROUP BY <key_column>
HAVING COUNT(*) > 5
ORDER BY change_count DESC;
```

## Data Freshness and History

### Table Modification History

```sql
-- Recent operations
SELECT
  version,
  timestamp,
  userId,
  userName,
  operation,
  operationMetrics
FROM (DESCRIBE HISTORY <catalog>.<schema>.<table>)
ORDER BY version DESC
LIMIT 20;

-- Last update time
SELECT MAX(timestamp) AS last_modified
FROM (DESCRIBE HISTORY <catalog>.<schema>.<table>)
WHERE operation IN ('WRITE', 'MERGE', 'UPDATE', 'DELETE');

-- Operations by user
SELECT
  userName,
  operation,
  COUNT(*) AS op_count,
  MAX(timestamp) AS last_operation
FROM (DESCRIBE HISTORY <catalog>.<schema>.<table>)
GROUP BY userName, operation
ORDER BY op_count DESC;
```
