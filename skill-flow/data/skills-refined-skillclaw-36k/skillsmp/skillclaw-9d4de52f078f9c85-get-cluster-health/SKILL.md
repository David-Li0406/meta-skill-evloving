---
name: get-cluster-health
description: Use this skill to assess the overall health status of a Kubernetes cluster, including node readiness and system pod health, for periodic checks or incident investigations.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- Kubernetes cluster is accessible
- `kubectl` or MCP has cluster-admin or read permissions

## Actions

### 1. Get Node Status

List all nodes and their readiness status.

```yaml
mcp_tool: kubernetes-mcp-server/resources_list
params:
  apiVersion: v1
  kind: Node
timeout: 30s
```

### 2. Get System Pod Health

Check pods in the `kube-system` namespace for any issues.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: kube-system
timeout: 30s
```

### 3. Get Recent Events

Check for warning events across the cluster.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params: {}
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] All nodes are in Ready state
- [ ] All kube-system pods are Running
- [ ] No critical warning events in the last hour

## Failure Handling

If nodes are NotReady or pods are failing:

1. Capture the current state for analysis
2. Trigger diagnostic skills for specific issues
3. Escalate if multiple nodes or critical pods are affected

## Examples

**Output:**
```json
{
  "nodes": {
    "total": 3,
    "ready": 3,
    "not_ready": 0
  },
  "system_pods": {
    "total": 12,
    "running": 12,
    "failed": 0
  },
  "warnings": 0,
  "healthy": true
}
```