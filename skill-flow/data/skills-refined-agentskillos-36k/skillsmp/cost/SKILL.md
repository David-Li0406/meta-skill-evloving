---
name: cost
version: 1.0.0
changelog: Initial quick metrics check
description: Quick context health check. See /checkpoint for full state management.
---

# Cost

Quick context health check.

## Task
$ARGUMENTS

## Instructions

Output: `## Cost`

### Read Metrics

```bash
.claude/skills/shared/scripts/read-metrics.sh
```

Key fields: `used_percentage`, `total_cost_usd`, `stale` (true if >5min old).

### Interpretation

See `agent_docs/context.md` for utilization thresholds and recommended actions.

For full state management, use `/checkpoint`.

## Exit Criteria

User understands current context health.
