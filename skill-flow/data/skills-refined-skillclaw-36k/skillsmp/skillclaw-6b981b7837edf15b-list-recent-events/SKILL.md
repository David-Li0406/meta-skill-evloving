---
name: list-recent-events
description: Use this skill when you need to collect recent Kubernetes events to identify issues such as warnings, errors, and state changes in your cluster.
---

# Skill body

## Preconditions

Before applying this skill, verify:

- You need to understand recent cluster activity.
- You are looking for warnings or errors.

## Actions

### 1. List Events from All Namespaces

Retrieve recent events from across the cluster.

```yaml
mcp_tool: kubernetes-mcp-server/events_list
params: {}
timeout: 60s
```

## Success Criteria

The skill succeeds when:

- [ ] Events retrieved successfully.
- [ ] Warnings/errors identified and categorized.

## Failure Handling

If events are unavailable, check API server connectivity.

## Examples

**Input Context:**
```json
{
  "reason": "routine health check",
  "time_range": "last 1 hour"
}
```

**Expected Outcome:**
List of recent events with warnings and errors highlighted, categorized by severity and resource type.