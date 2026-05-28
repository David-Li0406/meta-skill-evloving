---
name: bv-integration
description: |
  Beads Viewer (BV) integration for visual task management and smart task selection.
  Use for Kanban views, dependency graphs, and the robot-plan API for auto-selecting next tasks.
  Keywords: beads, viewer, kanban, dependency graph, robot-plan, task selection, bottleneck
tags: [workflow, beads, visualization, task-selection]
compatibility: Requires BV binary installed via curl script. Works with all agents.
allowed-tools:
  - Bash(bv:*)
  - Bash(which:*)
  - Read
---

# Beads Viewer Integration

BV is a TUI for visualizing Beads issues with graph analysis and a robot protocol for agents.

## Quick Reference

| Command | Human Use | Agent Use |
|---------|-----------|-----------|
| `bv` | Interactive TUI | N/A (requires TTY) |
| `bv --robot-plan` | N/A | Get next highest-impact task |
| `bv --robot-insights` | N/A | Get graph metrics JSON |
| `bv --export-graph` | Export HTML graph | N/A |

## Auto-Select Next Task (Robot Mode)

Instead of `bd list --status open`, use BV for smarter task selection:

```bash
bv --robot-plan
```

Returns JSON with the highest-impact unblocked task:
```json
{
  "next": "bd-xyz",
  "unblocks": 5,
  "impact_score": 0.87,
  "reason": "Critical path task, unblocks 5 downstream dependencies",
  "alternatives": ["bd-abc", "bd-def"]
}
```

### Using in Agent Workflow

```bash
# Get next task ID
NEXT_TASK=$(bv --robot-plan | jq -r .next)

# If valid, show details
if [ -n "$NEXT_TASK" ] && [ "$NEXT_TASK" != "null" ]; then
    bd show "$NEXT_TASK"
fi
```

## Graph Insights (Robot Mode)

Get graph analysis metrics:

```bash
bv --robot-insights
```

Returns:
```json
{
  "bottlenecks": ["bd-xyz"],
  "critical_path": ["bd-a", "bd-b", "bd-c"],
  "cycles": [],
  "density": 0.42,
  "pagerank": {"bd-xyz": 0.15, "bd-abc": 0.12}
}
```

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/beads_viewer/main/install.sh | bash
```

## Verification

```bash
# Check installed
which bv && bv --version

# Robot protocol works (run in repo with .beads/)
cd ~/affordabot && bv --robot-plan | jq .

# Optional: Interactive TUI (human only)
bv
```

## Interactive TUI Keys (Human Reference)

| Key | Action |
|-----|--------|
| `b` | Kanban board view |
| `g` | Dependency graph |
| `i` | Insights dashboard |
| `h` | History view |
| `t` | Time-travel (compare git revisions) |
| `/` | Fuzzy search |
| `j/k` | Navigate up/down |
| `Enter` | View details |
| `q` | Quit |

## Integration with lib/fleet

FleetDispatcher can use BV for smart task selection:

```python
from lib.fleet import FleetDispatcher

dispatcher = FleetDispatcher()

# Auto-select highest-impact task
next_task = dispatcher.auto_select_task(repo="affordabot")
if next_task:
    dispatcher.dispatch(beads_id=next_task, ...)
```

## When to Use BV vs bd CLI

| Scenario | Use |
|----------|-----|
| Create/update issues | `bd create`, `bd update` |
| Find next task (smart) | `bv --robot-plan` |
| Find any ready task | `bd ready` |
| Visualize dependencies | `bv` (interactive) or `bv --robot-insights` |
| Graph bottleneck analysis | `bv --robot-insights` |

## Fallback

If BV is not installed or fails, fall back to bd:

```bash
NEXT=$(bv --robot-plan 2>/dev/null | jq -r .next)
if [ -z "$NEXT" ] || [ "$NEXT" = "null" ]; then
    NEXT=$(bd ready --limit 1 --json | jq -r '.[0].id')
fi
```

---

**Last Updated:** 2026-01-14
**Repository:** https://github.com/Dicklesworthstone/beads_viewer
**Related Skills:** beads-workflow
