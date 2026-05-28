# Example: Performance Investigation

Scenario: Tests are running slowly. Find the bottlenecks.

## Step 1: Overall Performance Analysis

```bash
log-analyzer perf test.log
```

This shows:
- Top 20 slowest operations (>1s by default)
- Orphan operations (potential hangs)
- Statistics per operation type

## Step 2: Adjust Threshold

```bash
# Find operations over 500ms
log-analyzer perf test.log --threshold-ms 500

# Find only very slow operations (>5s)
log-analyzer perf test.log --threshold-ms 5000 --top-n 50
```

## Step 3: Focus by Operation Type

```bash
# Analyze only HTTP requests
log-analyzer perf test.log --op-type Request

# Analyze only events
log-analyzer perf test.log --op-type Event

# Analyze only commands
log-analyzer perf test.log --op-type Command
```

## Step 4: Find Potential Hangs

```bash
# Show operations that started but never finished
log-analyzer perf test.log --orphans-only
```

Orphan operations indicate:
- Network timeouts
- Deadlocks
- Missing response handlers
- Test termination before completion

## Step 5: Component-Specific Analysis

```bash
# Analyze specific component
log-analyzer perf test.log -C core-universal

# Exclude noisy component
log-analyzer perf test.log --exclude-component socket
```

## Interpreting Statistics

| Metric | Meaning |
|--------|---------|
| P50 | Median duration (50% faster than this) |
| P95 | 95th percentile (only 5% slower) |
| P99 | 99th percentile (outliers) |
| Count | Number of occurrences |
| Total | Sum of all durations |

## Common Performance Issues

| Pattern | Investigation |
|---------|---------------|
| High P99 vs P50 | Occasional slow requests - check network/backend |
| Many orphans | Timeouts or missing handlers |
| Single slow op | Specific endpoint issue |
| All ops slow | System-wide issue (CPU, memory, network) |
