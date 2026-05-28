---
name: get-capacity-recommendations
description: Use this skill to analyze cluster capacity and provide scaling recommendations for proactive resource management.
---

# Get Capacity Recommendations

## Preconditions

Before applying this skill, verify:

- Resource usage data is available for nodes
- Historical data exists for forecasting
- Cluster metrics are accessible

## Actions

### 1. Collect Current Resource Usage

Gather usage data for all resources:
```yaml
resources:
  - type: cpu
    unit: cores
    nodes: [<node_list>]
  - type: memory
    unit: GB
    nodes: [<node_list>]
  - type: storage
    unit: GB
    nodes: [<node_list>]
  - type: pods
    unit: count
    nodes: [<node_list>]
```

### 2. Calculate Cluster Totals

Aggregate across nodes:
```python
total_capacity = sum(node.capacity for node in nodes)
total_used = sum(node.used for node in nodes)
utilization = total_used / total_capacity
```

### 3. Forecast Future Usage

Project usage based on growth rate:
```python
days_of_data = (now - earliest_data).days
growth_rate = (latest_usage - earliest_usage) / days_of_data

forecast_30d = current_usage + (growth_rate * 30)
forecast_90d = current_usage + (growth_rate * 90)
```

### 4. Calculate Days Until Threshold

Project when thresholds will be reached:
```python
warning_threshold = 0.80 * total_capacity
critical_threshold = 0.90 * total_capacity

days_to_warning = (warning_threshold - current_usage) / growth_rate
days_to_critical = (critical_threshold - current_usage) / growth_rate
```

### 5. Check Node Balance

Identify imbalanced nodes:
```python
avg_utilization = mean(node.utilization for node in nodes)
imbalanced = [n for n in nodes if abs(n.utilization - avg_utilization) > 0.2]
```

### 6. Generate Recommendations

Create actionable recommendations:
```yaml
recommendations:
  - type: scale_up
    urgency: high
    resource: <resource_type>
    reason: "Days to critical: <days>"
  - type: rebalance
    urgency: medium
    nodes: [<node_list>]
    reason: "Utilization imbalance > 20%"
```

## Success Criteria

The skill succeeds when:

- [ ] All resource types analyzed
- [ ] Forecast calculated with confidence
- [ ] Recommendations prioritized by urgency

## Failure Handling

If analysis fails:

1. Insufficient data: Return only current state
2. Missing metrics: Use available data, note gaps
3. Calculation error: Return partial recommendations

## Examples

**Input Context:**
```json
{
  "cluster": "<cluster_name>",
  "forecast_days": 30
}
```

**Expected Output:**
```json
{
  "current_state": {
    "cpu_utilization": <cpu_utilization>,
    "memory_utilization": <memory_utilization>,
    "storage_utilization": <storage_utilization>,
    "pod_count": <pod_count>
  },
  "forecast_30d": {
    "memory_utilization": <predicted_memory_utilization>,
    "days_to_warning": <days_to_warning>,
    "days_to_critical": <days_to_critical>
  },
  "recommendations": [
    {
      "type": "scale_up",
      "resource": "memory",
      "urgency": "high",
      "confidence": <confidence_level>,
      "action": "<action_description>",
      "reason": "Memory will reach 80% in <days> days at current growth"
    }
  ],
  "node_balance": {
    "balanced": false,
    "imbalanced_nodes": ["<node_list>"],
    "suggestion": "Rebalance workloads from <node_list>"
  }
}
```