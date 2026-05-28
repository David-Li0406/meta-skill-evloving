---
name: list-pods-in-namespace
description: Use this skill to list all pods in a specific namespace along with their status, providing an overview of workload health.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- The namespace is specified.
- You need an overview of pods in the namespace.

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

- [ ] Pod list retrieved with status.
- [ ] Unhealthy pods identified.

## Failure Handling

If the list fails, check the existence of the namespace and permissions.

## Examples

**Input Context:**
```json
{
  "namespace": "production"
}
```

**Expected Outcome:**
Complete list of pods in the namespace with their current status, restart counts, and any pods not in Running state highlighted.