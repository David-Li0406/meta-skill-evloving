# Databricks Jobs System Tables Reference

Historical analysis using `system.lakeflow.*` tables. Data may be delayed by several hours.

## Table of Contents

- [Table Overview](#table-overview)
- [Basic Queries](#basic-queries)
- [Failure Analysis](#failure-analysis)
- [Performance Analysis](#performance-analysis)
- [Cost Analysis](#cost-analysis)
- [Alerting Queries](#alerting-queries)
- [Schema Reference](#schema-reference)

## Table Overview

| Table | Purpose | Retention |
|-------|---------|-----------|
| `system.lakeflow.jobs` | Job definitions | Active + 30 days deleted |
| `system.lakeflow.job_run_timeline` | Run history | 365 days |
| `system.lakeflow.job_task_run_timeline` | Task run details | 365 days |

## Basic Queries

### List Jobs

```sql
-- All active jobs
SELECT
  job_id,
  name,
  creator_user_name,
  run_as_user_name,
  create_time
FROM system.lakeflow.jobs
WHERE delete_time IS NULL
ORDER BY create_time DESC;

-- Search by name pattern
SELECT job_id, name, creator_user_name
FROM system.lakeflow.jobs
WHERE name LIKE '%etl%'
  AND delete_time IS NULL;
```

### Recent Runs for a Job

```sql
SELECT
  run_id,
  result_state,
  period_start_time,
  period_end_time,
  TIMESTAMPDIFF(MINUTE, period_start_time, period_end_time) AS duration_minutes
FROM system.lakeflow.job_run_timeline
WHERE job_id = <job_id>  -- Use job_id extracted from URL (e.g., 987402714328091)
ORDER BY period_start_time DESC
LIMIT 20;
```

### Today's Runs Overview

```sql
SELECT
  j.name AS job_name,
  r.result_state,
  COUNT(DISTINCT r.run_id) AS run_count
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.period_start_time >= CURRENT_DATE
GROUP BY j.name, r.result_state
ORDER BY j.name, r.result_state;
```

## Failure Analysis

### Failed Runs (Last 24 Hours)

```sql
SELECT
  j.name AS job_name,
  r.job_id,
  r.run_id,
  r.result_state,
  r.termination_code,
  r.period_start_time
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.result_state IN ('FAILED', 'TIMED_OUT', 'CANCELED')
  AND r.period_start_time >= CURRENT_DATE - INTERVAL 1 DAY
ORDER BY r.period_start_time DESC;
```

### Failure Rate by Job (Last 7 Days)

```sql
SELECT
  j.name AS job_name,
  r.job_id,
  COUNT(DISTINCT CASE WHEN r.result_state = 'SUCCESS' THEN r.run_id END) AS success_count,
  COUNT(DISTINCT CASE WHEN r.result_state = 'FAILED' THEN r.run_id END) AS failure_count,
  ROUND(
    COUNT(DISTINCT CASE WHEN r.result_state = 'FAILED' THEN r.run_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT r.run_id), 0), 2
  ) AS failure_rate_pct
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.period_start_time >= CURRENT_DATE - INTERVAL 7 DAY
GROUP BY j.name, r.job_id
HAVING COUNT(DISTINCT CASE WHEN r.result_state = 'FAILED' THEN r.run_id END) > 0
ORDER BY failure_rate_pct DESC;
```

### Frequently Failing Tasks

```sql
SELECT
  j.name AS job_name,
  t.task_key,
  COUNT(*) AS failure_count
FROM system.lakeflow.job_task_run_timeline t
JOIN system.lakeflow.jobs j ON t.job_id = j.job_id
WHERE t.result_state = 'FAILED'
  AND t.period_start_time >= CURRENT_DATE - INTERVAL 30 DAY
GROUP BY j.name, t.task_key
ORDER BY failure_count DESC
LIMIT 20;
```

### Failure Trend by Day

```sql
SELECT
  DATE(r.period_start_time) AS run_date,
  COUNT(DISTINCT CASE WHEN r.result_state = 'SUCCESS' THEN r.run_id END) AS success,
  COUNT(DISTINCT CASE WHEN r.result_state = 'FAILED' THEN r.run_id END) AS failed,
  COUNT(DISTINCT CASE WHEN r.result_state = 'TIMED_OUT' THEN r.run_id END) AS timed_out,
  COUNT(DISTINCT CASE WHEN r.result_state = 'CANCELED' THEN r.run_id END) AS canceled
FROM system.lakeflow.job_run_timeline r
WHERE r.period_start_time >= CURRENT_DATE - INTERVAL 30 DAY
GROUP BY DATE(r.period_start_time)
ORDER BY run_date DESC;
```

## Performance Analysis

### Average Duration by Job (Last 7 Days)

```sql
SELECT
  j.name AS job_name,
  COUNT(DISTINCT r.run_id) AS run_count,
  ROUND(AVG(TIMESTAMPDIFF(MINUTE, r.period_start_time, r.period_end_time)), 1) AS avg_minutes,
  MAX(TIMESTAMPDIFF(MINUTE, r.period_start_time, r.period_end_time)) AS max_minutes,
  MIN(TIMESTAMPDIFF(MINUTE, r.period_start_time, r.period_end_time)) AS min_minutes
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.result_state = 'SUCCESS'
  AND r.period_start_time >= CURRENT_DATE - INTERVAL 7 DAY
GROUP BY j.name
ORDER BY avg_minutes DESC;
```

### Slowest Tasks

```sql
SELECT
  j.name AS job_name,
  t.task_key,
  COUNT(*) AS run_count,
  ROUND(AVG(TIMESTAMPDIFF(MINUTE, t.period_start_time, t.period_end_time)), 1) AS avg_minutes,
  MAX(TIMESTAMPDIFF(MINUTE, t.period_start_time, t.period_end_time)) AS max_minutes
FROM system.lakeflow.job_task_run_timeline t
JOIN system.lakeflow.jobs j ON t.job_id = j.job_id
WHERE t.result_state = 'SUCCESS'
  AND t.period_start_time >= CURRENT_DATE - INTERVAL 7 DAY
GROUP BY j.name, t.task_key
ORDER BY avg_minutes DESC
LIMIT 20;
```

### Duration Trend for a Specific Job

```sql
SELECT
  DATE(r.period_start_time) AS run_date,
  COUNT(DISTINCT r.run_id) AS run_count,
  ROUND(AVG(TIMESTAMPDIFF(MINUTE, r.period_start_time, r.period_end_time)), 1) AS avg_minutes,
  MAX(TIMESTAMPDIFF(MINUTE, r.period_start_time, r.period_end_time)) AS max_minutes
FROM system.lakeflow.job_run_timeline r
WHERE r.job_id = <job_id>  -- Use job_id extracted from URL
  AND r.result_state = 'SUCCESS'
  AND r.period_start_time >= CURRENT_DATE - INTERVAL 30 DAY
GROUP BY DATE(r.period_start_time)
ORDER BY run_date DESC;
```

### Queue Time Analysis

```sql
-- Jobs with longest queue wait times
SELECT
  j.name AS job_name,
  ROUND(AVG(TIMESTAMPDIFF(SECOND, r.queue_start_time, r.period_start_time)), 0) AS avg_queue_seconds
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.queue_start_time IS NOT NULL
  AND r.period_start_time >= CURRENT_DATE - INTERVAL 7 DAY
GROUP BY j.name
HAVING avg_queue_seconds > 60
ORDER BY avg_queue_seconds DESC;
```

## Cost Analysis

### Compute Usage by Job (DBU Hours)

```sql
-- Note: compute_ids contains cluster/warehouse info
SELECT
  j.name AS job_name,
  r.job_id,
  COUNT(DISTINCT r.run_id) AS run_count,
  SUM(TIMESTAMPDIFF(MINUTE, r.period_start_time, r.period_end_time)) / 60.0 AS total_hours
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.period_start_time >= CURRENT_DATE - INTERVAL 30 DAY
GROUP BY j.name, r.job_id
ORDER BY total_hours DESC
LIMIT 20;
```

### Daily Compute Hours

```sql
SELECT
  DATE(r.period_start_time) AS run_date,
  COUNT(DISTINCT r.run_id) AS total_runs,
  ROUND(SUM(TIMESTAMPDIFF(MINUTE, r.period_start_time, r.period_end_time)) / 60.0, 2) AS total_hours
FROM system.lakeflow.job_run_timeline r
WHERE r.period_start_time >= CURRENT_DATE - INTERVAL 30 DAY
GROUP BY DATE(r.period_start_time)
ORDER BY run_date DESC;
```

## Alerting Queries

### Jobs Not Run Today

```sql
-- Scheduled jobs that haven't run today
SELECT
  j.job_id,
  j.name,
  MAX(r.period_start_time) AS last_run
FROM system.lakeflow.jobs j
LEFT JOIN system.lakeflow.job_run_timeline r ON j.job_id = r.job_id
WHERE j.delete_time IS NULL
GROUP BY j.job_id, j.name
HAVING MAX(r.period_start_time) < CURRENT_DATE
   OR MAX(r.period_start_time) IS NULL
ORDER BY last_run;
```

### Long Running Jobs

```sql
-- Jobs running longer than 2 hours
SELECT
  j.name AS job_name,
  r.run_id,
  r.period_start_time,
  TIMESTAMPDIFF(MINUTE, r.period_start_time, CURRENT_TIMESTAMP) AS running_minutes
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.result_state = 'RUNNING'
  AND TIMESTAMPDIFF(MINUTE, r.period_start_time, CURRENT_TIMESTAMP) > 120;
```

### Consecutive Failures

```sql
-- Jobs with 3+ consecutive failures
-- Note: This query scans only the last 7 days of data
-- Adjust the INTERVAL value to analyze a longer period
WITH ranked_runs AS (
  SELECT
    job_id,
    run_id,
    result_state,
    period_start_time,
    ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY period_start_time DESC) AS rn
  FROM system.lakeflow.job_run_timeline
  WHERE period_start_time >= CURRENT_DATE - INTERVAL 7 DAY
)
SELECT
  j.name AS job_name,
  r.job_id,
  COUNT(*) AS consecutive_failures
FROM ranked_runs r
JOIN system.lakeflow.jobs j ON r.job_id = j.job_id
WHERE r.rn <= 5
  AND r.result_state = 'FAILED'
GROUP BY j.name, r.job_id
HAVING COUNT(*) >= 3
ORDER BY consecutive_failures DESC;
```

## Schema Reference

### system.lakeflow.jobs

| Column | Type | Description |
|--------|------|-------------|
| `job_id` | LONG | Unique job identifier |
| `name` | STRING | Job name |
| `creator_user_name` | STRING | Job creator |
| `run_as_user_name` | STRING | Run-as identity |
| `create_time` | TIMESTAMP | Job creation time |
| `delete_time` | TIMESTAMP | Job deletion time (NULL if active) |

### system.lakeflow.job_run_timeline

| Column | Type | Description |
|--------|------|-------------|
| `job_id` | LONG | Job identifier |
| `run_id` | LONG | Run identifier |
| `run_name` | STRING | Run name |
| `result_state` | STRING | Result state (SUCCESS, FAILED, etc.) |
| `termination_code` | STRING | Termination reason code |
| `period_start_time` | TIMESTAMP | Run start time |
| `period_end_time` | TIMESTAMP | Run end time |
| `queue_start_time` | TIMESTAMP | Queue entry time |
| `compute_ids` | ARRAY | Compute resource IDs used |

### system.lakeflow.job_task_run_timeline

| Column | Type | Description |
|--------|------|-------------|
| `job_id` | LONG | Job identifier |
| `run_id` | LONG | Job run identifier |
| `task_run_id` | LONG | Task run identifier |
| `task_key` | STRING | Task key |
| `result_state` | STRING | Task result state |
| `termination_code` | STRING | Termination reason code |
| `period_start_time` | TIMESTAMP | Task start time |
| `period_end_time` | TIMESTAMP | Task end time |
| `compute_ids` | ARRAY | Compute resource IDs used |

## Notes

- **Data Latency**: System tables data may be delayed by several hours
- **Row Granularity**: Long-running jobs are split into hourly rows in timeline tables
- **Retention**: 365 days for run data, active + 30 days for job definitions
- **Cross-workspace**: System tables only contain current workspace data
