---
name: databricks-jobs
description: |
  Databricks Jobs management, monitoring, and debugging. Use for job status checks, run history, failure investigation, job execution, and historical analysis.
  Triggers: job status, run history, job failure, debug job, run job, cancel job, repair run, job metrics, failure analysis.
  Real-time operations use CLI (databricks jobs). Historical analysis uses System Tables (system.lakeflow.*).
metadata:
  version: 1.0.0
---

# Databricks Jobs

## Quick Reference

Extract `job_id` and `run_id` from URLs first (see [Extracting IDs from URLs](#extracting-ids-from-urls)).

| Operation | Tool | Command/Table |
|-----------|------|---------------|
| Real-time status | CLI | `databricks jobs get-run <run_id>` |
| List runs | CLI | `databricks jobs list-runs --job-id <job_id>` |
| Run job | CLI | `databricks jobs run-now <job_id>` |
| Cancel run | CLI | `databricks jobs cancel-run <run_id>` |
| Repair failed | CLI | `databricks jobs repair-run <run_id> --rerun-all-failed-tasks` |
| Historical analysis | SQL | `system.lakeflow.job_run_timeline` |

## Extracting IDs from URLs

```
https://<host>/jobs/<job_id>
https://<host>/jobs/<job_id>/runs/<run_id>
```

Example: `https://example.cloud.databricks.com/jobs/987402714328091/runs/304618225028273`
- `job_id`: 987402714328091
- `run_id`: 304618225028273

## CLI Command Syntax

**Critical**: Some commands use positional args, others require flags.

| Command | Syntax | Example |
|---------|--------|---------|
| `jobs get` | Positional | `databricks jobs get 123` |
| `jobs get-run` | Positional | `databricks jobs get-run 456` |
| `jobs get-run-output` | Positional | `databricks jobs get-run-output 456` |
| `jobs list-runs` | **Flag required** | `databricks jobs list-runs --job-id 123` |
| `jobs run-now` | Positional | `databricks jobs run-now 123` |
| `jobs cancel-run` | Positional | `databricks jobs cancel-run 456` |
| `jobs repair-run` | Positional | `databricks jobs repair-run 456 --rerun-all-failed-tasks` |

### Common Mistakes

| Wrong | Correct |
|-------|---------|
| `databricks jobs get --job-id 123` | `databricks jobs get 123` |
| `databricks jobs get-run --run-id 456` | `databricks jobs get-run 456` |
| `databricks jobs list-runs 123` | `databricks jobs list-runs --job-id 123` |

## Core Workflows

### Check Run Status

```bash
databricks jobs get-run <run_id>```

Key fields:
- `state.result_state` - Result (SUCCESS, FAILED, TIMED_OUT, CANCELED)
- `state.state_message` - Error message
- `tasks[]` - Status of each task

### Investigate Failed Run

```bash
# Step 1: Get run overview
databricks jobs get-run <run_id> -o json | jq '.state'

# Step 2: Find failed tasks
databricks jobs get-run <run_id> -o json | jq '.tasks[] | select(.state.result_state == "FAILED") | {task_key, state}'

# Step 3: Get error details
databricks jobs get-run-output <run_id> -o json | jq '{error, error_trace}'

# Step 4: Repair (rerun failed tasks)
databricks jobs repair-run <run_id> --rerun-all-failed-tasks```

For detailed troubleshooting: See [Troubleshooting Guide](references/troubleshooting.md)

### List and Search Jobs

```bash
# List all jobs
databricks jobs list
# Search by name
databricks jobs list -o json | jq '.jobs[] | select(.settings.name | contains("keyword"))'

# Get job definition
databricks jobs get <job_id>```

### List Runs

```bash
# All runs for a job
databricks jobs list-runs --job-id <job_id>
# Active runs only
databricks jobs list-runs --job-id <job_id> --active-only```

### Execute Jobs

```bash
# Run immediately
databricks jobs run-now <job_id>
# Run with parameters
databricks jobs run-now <job_id> --notebook-params '{"param1": "value1"}'databricks jobs run-now <job_id> --python-params '["arg1", "arg2"]'databricks jobs run-now <job_id> --jar-params '["arg1", "arg2"]'```

### Cancel and Repair

```bash
# Cancel a run
databricks jobs cancel-run <run_id>

# Rerun all failed tasks
databricks jobs repair-run <run_id> --rerun-all-failed-tasks
# Rerun specific tasks
databricks jobs repair-run <run_id> --rerun-tasks '["task_key1", "task_key2"]'```

### Multi-task Job Investigation

```bash
# List task definitions
databricks jobs get <job_id> -o json | jq '.settings.tasks[] | {task_key, description}'

# Check task states in a run
databricks jobs get-run <run_id> -o json | jq '.tasks[] | {task_key, state, start_time, end_time}'

# Get task dependencies
databricks jobs get <job_id> -o json | jq '.settings.tasks[] | {task_key, depends_on}'
```

### Check Schedule and Triggers

```bash
# Schedule settings
databricks jobs get <job_id> -o json | jq '.settings.schedule'

# Trigger settings (file arrival, etc.)
databricks jobs get <job_id> -o json | jq '.settings.trigger'
```

## System Tables (Historical Analysis)

Use for trend analysis and metrics. Data may be delayed by several hours.

| Table | Purpose |
|-------|---------|
| `system.lakeflow.jobs` | Job definitions |
| `system.lakeflow.job_run_timeline` | Run history |
| `system.lakeflow.job_task_run_timeline` | Task run details |

### Quick Queries

```sql
-- Failed runs in the last 24 hours
SELECT j.name, r.run_id, r.result_state, r.period_start_time
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.result_state = 'FAILED'
  AND r.period_start_time >= CURRENT_DATE - INTERVAL 1 DAY
ORDER BY r.period_start_time DESC;

-- Run history for a specific job
SELECT run_id, result_state, period_start_time,
  TIMESTAMPDIFF(MINUTE, period_start_time, period_end_time) AS duration_min
FROM system.lakeflow.job_run_timeline
WHERE job_id = <job_id>  -- Use job_id extracted from URL
ORDER BY period_start_time DESC
LIMIT 20;
```

For comprehensive historical analysis queries: See [System Tables Reference](references/system-tables.md)

## result_state Reference

| State | Description |
|-------|-------------|
| `SUCCESS` | Completed successfully |
| `FAILED` | Failed with error |
| `TIMED_OUT` | Exceeded timeout |
| `CANCELED` | Canceled by user/system |
| `RUNNING` | Currently executing |
| `PENDING` | Waiting to run |
| `SKIPPED` | Skipped (dependency failed) |

## References

- [Troubleshooting Guide](references/troubleshooting.md): Detailed failure investigation and debugging
- [System Tables Reference](references/system-tables.md): Historical analysis queries and schema
