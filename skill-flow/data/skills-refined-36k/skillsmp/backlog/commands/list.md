---
description: List all unarchived tasks with status, dependencies, and worktrees
argument-hint: [--worktrees-only] [--json] [--compact]
allowed-tools: Read, Bash, Glob, Grep
---

# List Tasks

Show all unarchived tasks with their status, dependencies, and associated worktrees.

**Arguments:** $ARGUMENTS

## Quick Start

Run the task list scripts to generate formatted output:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/index-to-json.sh" | "${CLAUDE_PLUGIN_ROOT}/scripts/format-task-list.sh"
```

This generates a beautifully formatted task list with status emojis, summaries, and next actions.

## Arguments

| Argument | Description |
|----------|-------------|
| `--json` | Output raw JSON (for programmatic use) |
| `--compact` | Minimal output (just the task table) |
| `--worktrees-only` | Show only active worktrees |

## Instructions

### Standard List (Default)

For the default view, run the formatting pipeline:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/index-to-json.sh" | "${CLAUDE_PLUGIN_ROOT}/scripts/format-task-list.sh"
```

This outputs:
- Task table with ID, Title, Status, Dependencies, Worktree
- Summary with counts by status
- Active worktrees section
- Next actions (ready to start, currently blocked)

### JSON Output (--json)

For programmatic access or integration with other tools:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/index-to-json.sh" --pretty
```

JSON structure:
```json
{
  "project": "ProjectName",
  "generated": "2025-01-21T12:00:00Z",
  "tasks": [
    {
      "id": "PROJ-001",
      "title": "Task title",
      "status": "Ready",
      "computedStatus": "Ready",
      "dependencies": [],
      "blockers": [],
      "worktree": {
        "branch": null,
        "path": null,
        "mode": null
      }
    }
  ],
  "worktrees": [...],
  "summary": {
    "total": 5,
    "byStatus": {
      "complete": {"count": 1, "tasks": "PROJ-001"},
      "inProgress": {"count": 1, "tasks": "PROJ-002"},
      ...
    }
  }
}
```

### Compact Output (--compact)

For minimal output showing just the task table:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/index-to-json.sh" | "${CLAUDE_PLUGIN_ROOT}/scripts/format-task-list.sh" --compact
```

### Worktrees-Only View (--worktrees-only)

Show only active worktree information:

```bash
git worktree list
```

Then for each worktree (except main), check for PROMPT.md to get task info:

```
═══════════════════════════════════════════════════════════════════
 ACTIVE WORKTREES
═══════════════════════════════════════════════════════════════════

| Task | Branch | Path | Mode | Status |
|------|--------|------|------|--------|
| {PREFIX}-002 | feature/registry | /path/to/wt/feature/registry | Implementation | In Progress |
| {PREFIX}-005 | feature/protocol | /path/to/wt/feature/protocol | Review | In Review |

Total: 2 active worktrees

## Orphan Worktrees

(Worktrees without PROMPT.md - may be stale)

| Branch | Path |
|--------|------|
| feature/old-branch | /path/to/wt/feature/old-branch |

## Cleanup Commands

Remove orphan worktrees:
"${CLAUDE_PLUGIN_ROOT}/scripts/wt-remove.sh" feature/old-branch
```

## Output Format

### Sample Output

```
═══════════════════════════════════════════════════════════════════════════════
  TASK LIST: ManaMesh
═══════════════════════════════════════════════════════════════════════════════
┌────────┬───────────────────────────────────────┬────────────────┬────────────────────────┬────────────────────────────┐
│   ID   │                 Title                 │     Status     │      Dependencies      │          Worktree          │
├────────┼───────────────────────────────────────┼────────────────┼────────────────────────┼────────────────────────────┤
│ MM-001 │ Frontend Skeleton + boardgame.io Core │ ✅ Complete    │ -                      │ -                          │
├────────┼───────────────────────────────────────┼────────────────┼────────────────────────┼────────────────────────────┤
│ MM-002 │ WebRTC + Two-Way Join Codes           │ ✅ Complete    │ MM-001                 │ -                          │
├────────┼───────────────────────────────────────┼────────────────┼────────────────────────┼────────────────────────────┤
│ MM-003 │ libp2p DHT Discovery                  │ 📋 In Review   │ MM-002                 │ feature/libp2p-dht         │
└────────┴───────────────────────────────────────┴────────────────┴────────────────────────┴────────────────────────────┘

Summary

Total: 3 tasks
┌────────────────┬───────┬────────────────────────┐
│     Status     │ Count │         Tasks          │
├────────────────┼───────┼────────────────────────┤
│ ✅ Complete    │ 2     │ MM-001, MM-002         │
├────────────────┼───────┼────────────────────────┤
│ 📋 In Review   │ 1     │ MM-003                 │
└────────────────┴───────┴────────────────────────┘

Next Actions

Ready to start:
- /backlog:launch MM-004 - mDNS Local Discovery
```

## Status Icons

| Status | Icon | Description |
|--------|------|-------------|
| Complete | ✅ | Task finished and merged |
| In Progress | 🚀 | Agent actively working |
| In Review | 📋 | Work complete, code review |
| Changes Requested | 🔄 | Review feedback to address |
| Ready | 🆕 | All dependencies met, can start |
| Blocked | ❌ | Waiting on dependencies |

## Error Handling

- **No tasks/ directory:** "Run /design:init to set up task management"
- **No design.yaml:** "Run /design:init to configure the repository"
- **Empty INDEX.md:** "No tasks defined. Use /design to create your first task"
- **jq not installed:** JSON formatting requires jq (`brew install jq`)

## Integration

The JSON output can be consumed by:
- CI/CD pipelines for status reporting
- Dashboard tools
- Custom scripts and integrations
- Other Claude Code plugins

Save JSON for external tools:
```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/index-to-json.sh" -o tasks.json
```

## Related Commands

- `/backlog` - Detailed status with dependency graph and analysis
- `/backlog:read <ID>` - Read full task details
- `/backlog:launch <ID>` - Launch a new agent worktree
- `/backlog:complete <ID>` - Complete and cleanup worktree
- `/backlog:prune` - Archive completed tasks
