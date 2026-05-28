---
name: check-node-resources
description: Use this skill to check resource usage (CPU, memory) on cluster nodes, helping to identify nodes under pressure and assess overall cluster health.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- Metrics server is available.
- You need to understand the cluster resource status.

## Actions

### 1. Get Resource Usage for All Nodes

Retrieve CPU and memory usage metrics for all nodes.

```yaml
mcp_tool: kubernetes-mcp-server/nodes_top
params: {}
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Node resource metrics are retrieved successfully.
- [ ] Resource pressure is identified if present.

## Failure Handling

If metrics are unavailable:

1. Check if the metrics server is deployed.
2. Request the Prometheus MCP server deployment.

## Examples

**Input Context:**
```json
{
  "reason": "investigating scheduling issues",
  "suspected_node": "worker-01"
}
```

**Expected Outcome:**
Node metrics retrieved showing CPU and memory usage for each node, with any nodes under pressure clearly identified.