# Database Inspection Workflow

This guide provides structured workflows for inspecting and debugging your PostgreSQL database using raw SQL queries.

## When to Use Raw Queries

Use the raw query script during these workflow stages:

1. **Initial Investigation**: Understand data distribution and relationships
2. **Debugging Crawler Issues**: Diagnose crawler behavior and failures
3. **Performance Analysis**: Analyze query performance and index usage
4. **Data Validation**: Verify data consistency and integrity

## Workflow 1: Initial Investigation

**When**: Starting work on a feature or debugging issues

**Goal**: Understand the current state of your data

### Step 1: Get Table Overview

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = t.table_name) as column_count
  FROM information_schema.tables t
  WHERE table_schema = 'public'
  ORDER BY table_name;
"
```

**What to look for**:

- All expected tables exist
- Column counts match your schema expectations

### Step 2: Check Record Counts

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    schemaname,
    tablename,
    n_live_tup AS row_count
  FROM pg_stat_user_tables
  WHERE schemaname = 'public'
  ORDER BY n_live_tup DESC;
"
```

**What to look for**:

- Tables have expected data volume
- No unexpectedly empty or bloated tables

### Step 3: Verify Data Distribution

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    d.name as district,
    COUNT(DISTINCT f.id) as facility_count,
    COUNT(s) as session_count
  FROM \"District\" d
  LEFT JOIN \"Facility\" f ON f.\"districtId\" = d.id
  LEFT JOIN \"Session\" s ON s.\"venueId\" = f.id AND s.date >= CURRENT_DATE
  GROUP BY d.id, d.name
  ORDER BY facility_count DESC;
"
```

**What to look for**:

- Distribution across districts matches expectations
- No districts with missing data

## Workflow 2: Debugging Crawler Issues

**When**: Crawler behaves unexpectedly or fails

**Goal**: Diagnose crawler status and recent operations

### Step 1: Check Recent Crawl Jobs

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    id,
    status,
    \"playDate\",
    \"startedAt\",
    \"completedAt\",
    \"errorMessage\"
  FROM \"CrawlJob\"
  ORDER BY \"startedAt\" DESC
  LIMIT 5;
"
```

**What to look for**:

- Recent job status (PENDING, RUNNING, COMPLETED, FAILED)
- Error messages for failed jobs
- Completion times to identify performance issues

### Step 2: Check Crawl Job Status Summary

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    status,
    COUNT(*) as count,
    MAX(\"startedAt\") as last_run
  FROM \"CrawlJob\"
  WHERE \"startedAt\" > NOW() - INTERVAL '1 hour'
  GROUP BY status;
"
```

**What to look for**:

- Jobs stuck in PENDING or RUNNING status
- Failed job patterns
- Recent activity levels

### Step 3: Inspect Dead Letter Queue

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    \"faCode\",
    date,
    error,
    attempts,
    status,
    \"lastFailedAt\"
  FROM \"DeadLetterEntry\"
  WHERE status = 'PENDING'
  ORDER BY \"lastFailedAt\" DESC
  LIMIT 10;
"
```

**What to look for**:

- Failed crawl attempts
- Error patterns (timeouts, API errors, etc.)
- Retry attempts

### Step 4: Check Session Availability Patterns

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    date::date,
    COUNT(*) as total_sessions,
    COUNT(*) FILTER (WHERE available = true) as available_sessions
  FROM \"Session\"
  WHERE date >= CURRENT_DATE
  GROUP BY date::date
  ORDER BY date;
"
```

**What to look for**:

- Consistent data availability across dates
- Missing dates or gaps in data
- Unexpected availability patterns

## Workflow 3: Performance Analysis

**When**: Investigating slow queries or performance issues

**Goal**: Identify bottlenecks and optimization opportunities

### Step 1: Check Index Usage

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
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
"
```

**What to look for**:

- Frequently used indexes (high scan count)
- Unused indexes (zero scan count - consider removing)
- Index efficiency (tuples_read vs tuples_fetched)

### Step 2: Find Unused Indexes

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    schemaname,
    tablename,
    indexname
  FROM pg_stat_user_indexes
  WHERE schemaname = 'public'
    AND idx_scan = 0
  ORDER BY tablename, indexname;
"
```

**What to look for**:

- Indexes that are never used (candidates for removal)

### Step 3: Check Table Scan Patterns

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    schemaname,
    tablename,
    seq_scan,
    idx_scan,
    seq_scan / NULLIF((seq_scan + idx_scan), 0) * 100 AS seq_scan_pct
  FROM pg_stat_user_tables
  WHERE schemaname = 'public'
  ORDER BY seq_scan DESC;
"
```

**What to look for**:

- High sequential scan percentage (indicates missing indexes)
- Tables with poor index usage

### Step 4: Analyze Table Sizes

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS index_size
  FROM pg_tables
  WHERE schemaname = 'public'
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

**What to look for**:

- Largest tables (potential optimization targets)
- Index-to-table size ratios (large indexes may need review)

## Workflow 4: Data Validation

**When**: Verifying data integrity before deploying features

**Goal**: Ensure data consistency and referential integrity

### Step 1: Check Orphaned Records

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT COUNT(*) as orphaned_sessions
  FROM \"Session\" s
  LEFT JOIN \"Facility\" f ON s.\"venueId\" = f.id
  WHERE f.id IS NULL;
"
```

**What to look for**:

- Sessions without matching facilities (should be 0)

### Step 2: Find Duplicate Records

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    \"venueId\",
    \"facilityCode\",
    date,
    \"startTime\",
    COUNT(*) as count
  FROM \"Session\"
  GROUP BY \"venueId\", \"facilityCode\", date, \"startTime\"
  HAVING COUNT(*) > 1;
"
```

**What to look for**:

- Duplicate sessions (should be 0 due to unique constraints)

### Step 3: Verify Foreign Key Relationships

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confrelid::regclass AS referenced_table
  FROM pg_constraint
  WHERE contype = 'f'
    AND connamespace = 'public'::regnamespace;
"
```

**What to look for**:

- All expected foreign key constraints exist
- Constraint names are clear and descriptive

### Step 4: Check Constraint Enforcement

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    pg_get_constraintdef(oid) AS constraint_definition
  FROM pg_constraint
  WHERE connamespace = 'public'::regnamespace
  ORDER BY conrelid::regclass::text, conname;
"
```

**What to look for**:

- All expected constraints are defined
- Constraint definitions match business rules

## Standard Investigation Sequence

Follow this sequence for comprehensive database inspection:

1. **Database Health** → Understand data volume and distribution
2. **Recent Activity** → Identify current state and issues
3. **Specific Records** → Deep dive into problem areas
4. **Relationships** → Ensure data integrity
5. **Performance** → Identify optimization opportunities

## Example: Complete Investigation

### 1. Check Database Health

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    COUNT(DISTINCT \"venueId\") as facilities,
    COUNT(*) as total_sessions,
    COUNT(*) FILTER (WHERE available = true) as available
  FROM \"Session\"
  WHERE date >= CURRENT_DATE;
"
```

### 2. Check Recent Crawl Jobs

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT status, COUNT(*)
  FROM \"CrawlJob\"
  WHERE \"startedAt\" > NOW() - INTERVAL '1 hour'
  GROUP BY status;
"
```

### 3. Inspect Failed Operations

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT * FROM \"DeadLetterEntry\"
  WHERE status = 'PENDING'
  ORDER BY \"lastFailedAt\" DESC
  LIMIT 5;
"
```

### 4. Verify Data Integrity

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT COUNT(*) as orphaned
  FROM \"Session\" s
  LEFT JOIN \"Facility\" f ON s.\"venueId\" = f.id
  WHERE f.id IS NULL;
"
```

### 5. Check Index Usage

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    tablename,
    indexname,
    idx_scan
  FROM pg_stat_user_indexes
  WHERE schemaname = 'public'
  ORDER BY idx_scan ASC
  LIMIT 10;
"
```

## Interactive Mode

For exploratory investigations, use interactive mode:

```bash
tsx .agent/skills/prisma-db/scripts/raw-query.ts --interactive
```

Then run queries sequentially:

```bash
sql> SELECT COUNT(*) FROM "Session";
sql> SELECT * FROM "CrawlJob" ORDER BY "startedAt" DESC LIMIT 1;
sql> \q (to quit)
```

## Integration with Development Workflows

### Before Schema Changes

```bash
# Check current data distribution
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT
    \"facilityCode\",
    COUNT(*) as session_count
  FROM \"Session\"
  GROUP BY \"facilityCode\"
  ORDER BY session_count DESC;
"
```

### After Schema Changes

```bash
# Verify migration success
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT table_name, column_name, data_type
  FROM information_schema.columns
  WHERE table_schema = 'public'
  ORDER BY table_name, ordinal_position;
"
```

### During Feature Development

```bash
# Interactive mode for exploration
tsx .agent/skills/prisma-db/scripts/raw-query.ts --interactive
```

## Tips for Effective Inspection

1. **Start Simple**: Begin with counts and aggregations before fetching detailed records
2. **Use Filters**: Always filter by date or status to reduce dataset size
3. **Iterate**: Refine queries based on initial findings
4. **Document**: Note unexpected patterns or issues for follow-up
5. **Compare**: Compare current state with previous snapshots when possible

## Related Resources

- [Common Inspection Queries](./common-inspection-queries.md)
- [Query Optimization Guide](./query-optimization-guide.md)
- [Best Practices](./best-practices.md)
