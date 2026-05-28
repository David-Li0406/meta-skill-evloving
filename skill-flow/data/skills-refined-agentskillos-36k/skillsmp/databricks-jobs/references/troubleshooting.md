# Databricks Jobs Troubleshooting Guide

## Table of Contents

- [First Steps](#first-steps)
- [Failed Run Investigation](#failed-run-investigation)
- [Common Failure Patterns](#common-failure-patterns)
- [Cluster Issues](#cluster-issues)
- [Task Dependencies](#task-dependencies)
- [Permission Issues](#permission-issues)
- [Timeout Issues](#timeout-issues)

## First Steps

Always verify the run state before detailed investigation:

```bash
# 1. Get run overview
databricks jobs get-run <run_id> -o json | jq '{
  state: .state,
  job_id: .job_id,
  start_time: .start_time,
  end_time: .end_time,
  trigger: .trigger
}'

# 2. Check for failed tasks
databricks jobs get-run <run_id> -o json | jq '.tasks[] | select(.state.result_state != "SUCCESS") | {task_key, state}'

# 3. Get error output
databricks jobs get-run-output <run_id> -o json | jq '{error, error_trace}'
```

## Failed Run Investigation

### Step-by-Step Debug Flow

```bash
# Step 1: Identify failure type from run state
databricks jobs get-run <run_id> -o json | jq '.state'
# Check: result_state, life_cycle_state, state_message

# Step 2: For multi-task jobs, find the root cause task
databricks jobs get-run <run_id> -o json | jq '
  .tasks[]
  | select(.state.result_state == "FAILED")
  | {task_key, depends_on: .depends_on, state: .state}
'

# Step 3: Get detailed error for the failing task
# First, extract the task_run_id from Step 2 output
# (The run_id field in .tasks[] is the TASK run_id, not the job run_id)
databricks jobs get-run <task_run_id> -o json | jq '.state'

# Step 4: Check the cluster logs if cluster-related
databricks jobs get-run <run_id> -o json | jq '.cluster_instance'
```

### Extracting Task Run IDs

```bash
# Get all task run IDs
databricks jobs get-run <run_id> -o json | jq '.tasks[] | {task_key, run_id}'

# Get failed task run IDs only
databricks jobs get-run <run_id> -o json | jq '
  .tasks[]
  | select(.state.result_state == "FAILED")
  | {task_key, run_id}
'
```

## Common Failure Patterns

### Notebook Execution Failures

| Error Pattern | Cause | Solution |
|---------------|-------|----------|
| `ModuleNotFoundError` | Missing library | Add to cluster libraries or notebook scope |
| `AnalysisException` | Table not found | Check catalog/schema permissions |
| `Py4JJavaError` | Spark execution error | Check Spark UI for details |
| `AssertionError` | Assert failed in notebook | Review notebook logic |

**Get notebook output:**
```bash
databricks jobs get-run-output <run_id> -o json | jq '.notebook_output'
```

### Python Script Failures

```bash
# Check error and trace
databricks jobs get-run-output <run_id> -o json | jq '{
  error: .error,
  error_trace: .error_trace,
  metadata: .metadata
}'
```

### SQL Task Failures

```bash
# Check SQL query result
databricks jobs get-run-output <run_id> -o json | jq '.sql_output'
```

### JAR/Spark Submit Failures

```bash
# Check logs location
databricks jobs get-run <run_id> -o json | jq '.cluster_instance.spark_context_id'

# Driver logs available in:
# dbfs:/cluster-logs/<cluster_id>/driver/
```

## Cluster Issues

### Cluster Failed to Start

**Symptoms:**
- `life_cycle_state: INTERNAL_ERROR`
- `state_message` contains cluster error

**Diagnosis:**
```bash
# Get cluster details from run
databricks jobs get-run <run_id> -o json | jq '.cluster_instance'

# Check cluster events (if cluster_id available)
databricks clusters events --cluster-id <cluster_id> -o json | jq '.events[:5]'
```

**Common causes:**

| Cause | Solution |
|-------|----------|
| Instance unavailable | Use different node type or availability zone |
| Quota exceeded | Request quota increase or use smaller cluster |
| Image not found | Update Databricks Runtime version |
| Init script failed | Check init script logs |

### Cluster Terminated During Run

```bash
# Check termination reason
databricks clusters get --cluster-id <cluster_id> -o json | jq '.termination_reason'
```

## Task Dependencies

### Understanding Dependency Failures

When a task fails, all dependent tasks are automatically SKIPPED.

```bash
# Find skipped tasks and their dependencies
databricks jobs get-run <run_id> -o json | jq '
  .tasks[]
  | select(.state.result_state == "SKIPPED")
  | {task_key, depends_on}
'

# Trace the root cause (first failed task)
databricks jobs get-run <run_id> -o json | jq '
  .tasks
  | sort_by(.start_time)
  | map(select(.state.result_state == "FAILED"))
  | .[0]
'
```

### Circular Dependency Detection

```bash
# List all task dependencies
databricks jobs get <job_id> -o json | jq '.settings.tasks[] | {task_key, depends_on}'
```

## Permission Issues

### Common Permission Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `PERMISSION_DENIED` on notebook | User lacks access | Grant access or use service principal |
| `PERMISSION_DENIED` on cluster | Cluster ACL issue | Update cluster permissions |
| `PERMISSION_DENIED` on table | Unity Catalog issue | Grant table permissions |

**Check job permissions:**
```bash
databricks jobs get-permission-levels --job-id <job_id> -o json
databricks jobs get-permissions --job-id <job_id> -o json
```

### Service Principal Issues

```bash
# Verify the run-as identity
databricks jobs get <job_id> -o json | jq '.settings.run_as'

# Check service principal details
databricks service-principals get <sp_id> -o json
```

## Timeout Issues

### Job Timeout

```bash
# Check timeout settings
databricks jobs get <job_id> -o json | jq '{
  timeout_seconds: .settings.timeout_seconds,
  max_concurrent_runs: .settings.max_concurrent_runs
}'

# Check actual duration
databricks jobs get-run <run_id> -o json | jq '
  (.end_time - .start_time) / 1000 | floor | "\(.) seconds"
'
```

### Task Timeout

```bash
# Check task timeout settings
databricks jobs get <job_id> -o json | jq '.settings.tasks[] | {task_key, timeout_seconds}'
```

### Retry Configuration

```bash
# Check retry settings
databricks jobs get <job_id> -o json | jq '.settings.tasks[] | {
  task_key,
  max_retries: .max_retries,
  min_retry_interval_millis: .min_retry_interval_millis,
  retry_on_timeout: .retry_on_timeout
}'

# Check retry attempts in run
databricks jobs get-run <run_id> -o json | jq '.tasks[] | {task_key, attempt_number}'
```

## Repair Run

### Rerun Failed Tasks Only

```bash
# Rerun all failed tasks
databricks jobs repair-run <run_id> --rerun-all-failed-tasks -o json

# Rerun specific tasks
databricks jobs repair-run <run_id> --rerun-tasks '["task_key1", "task_key2"]' -o json

# Check repair history
databricks jobs get-run <run_id> -o json | jq '.repair_history'
```

### Repair Considerations

- Repair reruns only failed/skipped tasks
- Successful tasks retain their state
- New task run IDs are generated for repaired tasks
- Cluster may be reused or recreated depending on settings

## Quick Reference: State Codes

### result_state

| State | Description |
|-------|-------------|
| `SUCCESS` | Completed successfully |
| `FAILED` | Failed with error |
| `TIMED_OUT` | Exceeded timeout |
| `CANCELED` | Canceled by user/system |
| `MAXIMUM_CONCURRENT_RUNS_REACHED` | Max concurrent runs limit |
| `EXCLUDED` | Excluded from run (conditional task) |
| `SUCCESS_WITH_FAILURES` | Job succeeded but some tasks failed |

### life_cycle_state

| State | Description |
|-------|-------------|
| `PENDING` | Waiting for resources |
| `RUNNING` | Currently executing |
| `TERMINATING` | Shutting down |
| `TERMINATED` | Completed execution |
| `SKIPPED` | Skipped due to dependency |
| `INTERNAL_ERROR` | Internal error occurred |
