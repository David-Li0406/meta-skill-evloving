---
name: swe-wm-update
version: 2.0.0
description: Single-operation Working Memory update via background daemon
workflow:
  aware: true
  callable_from:
    - WF_START
    - WF_CLASSIFY
    - WF_EXECUTE
    - WF_CHECKPOINT
    - WF_VERIFY
    - WF_DONE
  default_return: null
  supports_standalone: false
  auto_transition: false
args:
  - name: session_id
    description: 8-char session ID (required)
    required: true
  - name: task
    description: Task description (required)
    required: true
  - name: feature
    description: Feature key(s) from INDEX_FEATURES (required)
    required: true
  - name: state
    description: Current workflow state WF_* (required)
    required: true
  - name: progress
    description: Progress items as markdown list (required)
    required: true
  - name: complexity
    description: simple|medium|large (optional, default medium)
    required: false
---

# /swe-wm-update

**CRITICAL: This skill uses the background daemon for non-blocking WM writes.**

The daemon is located at:
```
.claude/plugins/serena-workflow-engine/hooks/swe_hooks/core/wm_writer_daemon.py
```

## Why Use the Daemon?

- **Non-blocking**: Writes queued asynchronously, won't slow down workflow
- **Write coalescing**: Rapid updates to same file are batched
- **Format validation**: Validates against REF_WM specs before writing
- **Anti-pattern detection**: Rejects single-field edits (use full writes)

## Anti-Pattern (DO NOT DO THIS)

```python
# WRONG - Multiple blocking Serena calls!
edit_memory("WM_...", "Task: old", "Task: new", "literal")
edit_memory("WM_...", "Feature: old", "Feature: new", "literal")
edit_memory("WM_...", "State: old", "State: new", "literal")
```

## Correct Pattern - Using the Daemon

The daemon exposes these functions:

```python
from wm_writer_daemon import async_wm_write, async_wm_append, get_wm_writer

# Queue a full WM write (non-blocking)
async_wm_write(
    filepath=".serena/memories/WM_{session}_session.md",
    content=full_wm_content,
    operation_type='full_write',  # or 'state_update', 'edit_tracking', 'transition_log'
    validate=True,
    session_id="a7380848"
)

# Append to existing WM (reads current, appends, queues write)
async_wm_append(
    filepath=".serena/memories/WM_{session}_session.md",
    append_content="\n## New Section\n...",
    session_id="a7380848"
)
```

## Required Data

Before invoking, you MUST have ALL of:

| Field | Source | Example |
|-------|--------|---------|
| session_id | From hook output or WM filename | `a7380848` |
| task | User's request summary | `"Refactor auth module"` |
| feature | INDEX_FEATURES key | `BACKEND` or `BLOCKS,THEMES` |
| state | Current WF_* step | `WF_EXECUTE` |
| progress | Markdown checklist | `"- [x] Step 1\n- [ ] Step 2"` |

## Process

### Step 1: Validate Required Fields

If ANY field is missing, STOP and gather it first:
- No session_id? → Check hook output or `list_memories()`
- No task? → Ask user or infer from conversation
- No feature? → Check `INDEX_FEATURES` or ask user
- No state? → Determine from workflow position
- No progress? → Create initial checklist from task

### Step 2: Build Complete WM Content

```markdown
# Working Memory: Session {session_id}

## Session
- **ID**: {session_id}
- **Task**: {task}
- **Started**: {timestamp}

## Workflow Context
**Current State**: {state}
**Previous State**: {previous_state or 'None'}

## Task Context
- **Feature(s)**: {feature}
- **Complexity**: {complexity}

## Progress Tracking
### Pending
{progress}

## Requirements
{requirements or '(from user request)'}

## Implementation Notes
{notes or '(none yet)'}
```

### Step 3: Queue Write via Daemon

The hooks automatically use the daemon. When updating WM from workflow:

```python
# Hooks call this internally - writes are non-blocking
async_wm_write(
    filepath=f".serena/memories/WM_{session_id}_session.md",
    content=wm_content,
    operation_type='full_write',
    validate=True,
    session_id=session_id
)
```

**ONE queued operation. Non-blocking. Validated.**

### Step 4: Confirm

Output: `📋 Updated Working Memory: WM_{session_id}_session`

## Operation Types

| Type | Use Case | Validation |
|------|----------|------------|
| `full_write` | Complete WM replacement | Full format check |
| `state_update` | State transition only | Anti-pattern detection |
| `edit_tracking` | Increment edit counts | Minimal |
| `transition_log` | Log state changes | Minimal |
| `append` | Add section to existing | None |

## State Transitions

When updating state, also update progress:

| From → To | Progress Update |
|-----------|-----------------|
| WF_START → WF_CLASSIFY | Add classification checklist |
| WF_CLASSIFY → WF_EXECUTE | Add implementation checklist |
| WF_EXECUTE → WF_VERIFY | Mark implementation done, add verify checklist |
| WF_VERIFY → WF_DONE | Mark all complete |

## Validation Rules

The daemon will REJECT writes if:
1. session_id doesn't match `[a-f0-9]{8}` pattern
2. state doesn't match `WF_*` pattern
3. feature is empty or "(to be determined)"
4. task is empty or "(awaiting user task)"
5. Single-field edit detected (must do full writes)

## Daemon Stats

Check daemon health:
```python
writer = get_wm_writer()
stats = writer.get_stats()
# {'queued': N, 'written': N, 'failed': N, 'coalesced': N, 'validation_rejected': N}
```

## Exit

No explicit exit - this is a utility skill that returns to caller.
