---
name: detect-recurrence-pattern
description: Use this skill when you need to identify recurring patterns in issues and events to inform prevention strategies.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- Issue records are available for analysis.
- A minimum of 3 occurrences in the analysis window.
- Timestamp data is available for temporal analysis.

## Actions

### 1. Collect Issue Records

Gather issue data for analysis:
```yaml
issue_record:
  issue_type: string       # e.g., "CrashLoopBackOff", "OOMKilled"
  resource: string         # e.g., "pod/app-123"
  namespace: string        # e.g., "production"
  timestamp: datetime
  metadata: object
  resolved: boolean
```

### 2. Detect Resource Patterns

Group issues by base resource name:
```python
# Group by namespace/kind/base-name
by_base_name = group_issues_by_resource_base()

for key, group in by_base_name.items():
    if len(group) >= min_occurrences:
        # Pattern detected: same resource having recurring issues
        pattern = RecurrencePattern(
            pattern_type="resource",
            description=f"Recurring issues on {key}",
            confidence=min(1.0, len(group) / 10),
            severity=calculate_severity(group)
        )
```

### 3. Detect Temporal Patterns

Analyze time intervals between issues:
```python
# Calculate intervals between consecutive issues
intervals = [issues[i].timestamp - issues[i-1].timestamp for i in range(1, len(issues))]

# Check for periodic patterns (low variance = regular occurrence)
avg_interval = mean(intervals)
std_dev = standard_deviation(intervals)

if std_dev / avg_interval < 0.3:
    # Periodic pattern detected
    pattern_type = "periodic"
    period_desc = format_period(avg_interval)  # e.g., "every 2 hours"
```

### 4. Detect Cluster Patterns

Find issues occurring together:
```python
# Group issues by 5-minute windows
windows = group_by_time_window(issues, window_seconds=300)

for window, group in windows.items():
    if len(group) >= 3:
        # Cluster pattern: multiple issues at the same time
        pattern = RecurrencePattern(
            pattern_type="cluster",
            description=f"Cluster of {len(group)} issues occurring together",
            confidence=min(1.0, len(group) / 10)
        )
```

### 5. Suggest Prevention Strategies

Based on detected patterns, suggest strategies to prevent future occurrences:
- For resource patterns, consider resource allocation adjustments.
- For temporal patterns, analyze workload during peak times.
- For cluster patterns, investigate common causes among clustered issues.