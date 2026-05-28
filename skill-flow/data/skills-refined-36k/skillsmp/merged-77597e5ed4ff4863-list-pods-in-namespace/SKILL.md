---
name: list-pods-in-namespace
description: Use this skill to list all pods in a specific namespace with their status, providing an overview of workload health.
---

# List Pods in Namespace

## Preconditions

Before applying this skill, verify:

- Namespace is specified
- Need overview of pods in namespace

## Actions

### 1. List Pods in the Namespace

Retrieve all pods in the specified namespace with their status.

```yaml
mcp_tool: kubernetes-mcp-server/pods_list_in_namespace
params:
  namespace: $namespace
timeout: 30s
```

## Success Criteria

The skill succeeds when:

- [ ] Pod list retrieved with status
- [ ] Unhealthy pods identified

## Failure Handling

If the list fails, check namespace existence and permissions.

## Examples

**Input Context:**
```json
{
  "namespace": "<namespace>"
}
```

**Expected Outcome:**
Complete list of pods in the namespace with their current status, restart counts, and any pods not in Running state highlighted.