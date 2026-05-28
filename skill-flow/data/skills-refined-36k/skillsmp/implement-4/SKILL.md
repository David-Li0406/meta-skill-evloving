---
name: implement
description: Use as default workflow when no specialized workflow (debug, iterate, pr-comment) applies. For general implementation tasks.
user_invocable: true
---

# Implement Workflow

Simple default workflow for general implementation. Use when specialized workflows don't apply.

## Initialize

```bash
python3 ~/.claude/plugins/agent-swarm/lib/implementer_workflow.py $ARGUMENTS
```

## Flow

```
WORK → VERIFY → DONE
     ↑    |
     +----+ (if tests/lint fail)
```

## Phases

| Phase | Purpose | Tools |
|-------|---------|-------|
| **work** | Do the task | All tools allowed |
| **verify** | Run tests and lint | All tools (can fix issues) |
| **done** | Complete | - |

## When to Use

- Subagent doing implementation work
- General task without specific workflow
- Default when no better workflow applies

## CLI

```bash
# Start
python3 lib/implementer_workflow.py start "Add feature X"

# With custom ID (for parallel agents)
python3 lib/implementer_workflow.py --id agent-123 start "Task"

# Check status
python3 lib/implementer_workflow.py status

# Record verification
python3 lib/implementer_workflow.py verify 1 1  # tests=pass, lint=pass

# Advance
python3 lib/implementer_workflow.py advance
```

## Exit Conditions

| Condition | Trigger |
|-----------|---------|
| `done` | Verification passed |
| `max_iterations` | 3 kickbacks |
| `user_stopped` | Manual stop |

## Permission Awareness

At task start, check workflow state for active permissions:

1. **Check active workflow**: `get_active_workflow_id()` returns current workflow
2. **Get permissions**: `get_permissions(workflow_id)` returns PermissionStore
3. **Verify tool access**: `is_tool_allowed(tool_name, **context)` before operations

**Programmatic check** (lib/permission_query.py):
```python
from permission_query import get_permissions, is_tool_allowed

# Check if Edit is allowed
allowed, reason = is_tool_allowed("Edit", file_path="src/main.py")
if not allowed:
    print(f"Blocked: {reason}")
```

**Self-enforcement**: Even in `work` phase with all tools allowed, respect any file path restrictions passed by the orchestrator.
