---
name: check-pod-resources
description: Use this skill to check resource usage (CPU, memory) for pods in a Kubernetes cluster, helping to identify pods that are consuming excessive resources.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- Metrics server is available.
- You need to understand pod resource consumption.

## Actions

### 1. Get Resource Usage for Pods

Retrieve CPU and memory usage metrics for pods in the specified namespace.

```yaml
mcp_tool: kubernetes-mcp-server/pods_top
params:
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Pod resource metrics are retrieved successfully.
- [ ] High resource consumers are identified if present.

## Failure Handling

If metrics are unavailable:

1. Check if the metrics-server is deployed.
2. Fall back to resource requests/limits from the pod specification.

## Examples

**Input Context:**
```json
{
  "namespace": "production",
  "reason": "investigating high memory usage"
}
```

**Expected Outcome:**
Pod metrics retrieved showing CPU and memory usage for each pod, with any pods consuming excessive resources clearly identified.