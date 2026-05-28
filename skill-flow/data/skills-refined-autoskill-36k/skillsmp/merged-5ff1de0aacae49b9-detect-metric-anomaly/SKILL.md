---
name: detect-metric-anomaly
description: Use this skill to analyze metrics for statistical anomalies using z-score analysis and threshold checking, enabling proactive monitoring and early warning.
---

# Detect Metric Anomaly

## Preconditions

Before applying this skill, verify:

- Metric name and current value are available.
- Historical baseline exists (or can be established).
- Threshold configuration is available.

## Actions

### 1. Retrieve Baseline Statistics

Get or calculate baseline from history:
```yaml
metric: <metric_name>
window_size: 1000  # Last N data points
statistics:
  - mean
  - std_dev
  - percentile_95
```

### 2. Calculate Z-Score

Determine how far the current value deviates from the baseline:
```python
z_score = (current_value - baseline.mean) / baseline.std_dev
```

Interpret z-score:
- |z| < 2: Normal variation
- 2 <= |z| < 3: Warning (unusual)
- |z| >= 3: Critical (anomaly)

### 3. Check Absolute Thresholds

Compare against configured thresholds:
```yaml
<metric_name>:
  warning: <warning_threshold>
  critical: <critical_threshold>
```

### 4. Detect Trends

Analyze recent window for sustained deviation:
```python
if 80% of last 10 values > baseline.mean:
    trend = "increasing"
elif 80% of last 10 values < baseline.mean:
    trend = "decreasing"
else:
    trend = "stable"
```

### 5. Generate Alert

If an anomaly is detected:
```yaml
alert:
  metric: <metric_name>
  severity: <calculated_severity>
  type: <anomaly_type>  # spike, drop, trend
  z_score: <z_score>
  current_value: <current_value>
  baseline_mean: <mean>
  recommendation: <suggested_action>
```

## Success Criteria

The skill succeeds when:

- [ ] Metric analyzed against baseline.
- [ ] Z-score calculated correctly.
- [ ] Alert generated if an anomaly is present.

## Failure Handling

If analysis fails:

1. Insufficient data: Wait for more samples.
2. No baseline: Initialize with current values.
3. Calculation error: Log and skip this check.

## Examples

**Input Context:**
```json
{
  "metric": "cpu_percent",
  "current_value": 92,
  "node": "worker-1"
}
```

**Expected Output:**
```json
{
  "anomaly_detected": true,
  "severity": "warning",
  "type": "threshold_breach",
  "z_score": 2.3,
  "baseline_mean": 45,
  "baseline_std_dev": 15,
  "percentile_rank": 97,
  "recommendation": "Investigate high CPU usage on worker-1"
}
```