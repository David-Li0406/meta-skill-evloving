# Autonomous Behavior (`--auto`)

Skip prompts between tasks for continuous execution. Combinable with `--delegate` and/or `--parallel`.

## Contents

- [Overview](#overview)
- [Flag Combinations](#flag-combinations)
- [Enabling Autonomous Mode](#enabling-autonomous-mode)
- [Pause Triggers](#pause-triggers)
- [Recovery Patterns](#recovery-patterns)
- [Gate Comparison](#gate-comparison)
- [Best Practices](#best-practices)

## Overview

The `--auto` flag enables continuous task execution without requiring user approval between each task. The system automatically:

1. Completes the current task
2. Selects the next recommended task
3. Executes it immediately
4. Repeats until a pause trigger fires

### When to Use

| Scenario | Recommended Mode |
|----------|------------------|
| Implementing a well-defined spec | Autonomous |
| Exploratory work or unclear requirements | Interactive |
| Large batch of similar tasks | Autonomous |
| Tasks requiring frequent decisions | Interactive |
| Overnight/unattended execution | Autonomous |

### Session Tracking

Autonomous mode uses session-config to track state:
- Session starts when `--auto` is invoked
- Progress persists across `/clear` boundaries
- Session ends when spec completes or user abandons

> See [session-management.md](./session-management.md) for session-config MCP action details.

## Flag Combinations

`--auto` is orthogonal and combinable with `--delegate` and `--parallel`:

| Flags | Behavior |
|-------|----------|
| `--auto` | Autonomous, inline (same context) |
| `--auto --delegate` | Autonomous, sequential subagent per task |
| `--auto --delegate --parallel` | Autonomous, concurrent subagents |

**Defaults:** Loaded from `[implement]` section in `foundry-mcp.toml`. CLI flags override.

## Enabling Autonomous Mode

### Via Command Flag

```bash
foundry-implement --auto                         # Inline execution
foundry-implement --auto --delegate              # Delegate to subagent
foundry-implement --auto --delegate --parallel   # Concurrent subagents
```

### Via TOML Defaults

Set in `foundry-mcp.toml`:
```toml
[implement]
auto = true       # Always skip prompts
delegate = true   # Always use subagent
parallel = false  # Sequential by default
```

### Via Interactive Selection

When running `foundry-implement` without flags and no TOML defaults:
```
"Select execution mode:"
- "Interactive, inline (default)"
- "Autonomous, inline (--auto)"
- "Interactive, delegated (--delegate)"
- "Autonomous, delegated (--auto --delegate)"
- "Autonomous, parallel (--auto --delegate --parallel)"
```

### Resuming a Paused Session

```bash
foundry-implement --auto
# If session exists and is paused, you'll be prompted:
# "Resume session?" / "Start fresh?"
```

## Pause Triggers

Autonomous execution pauses when specific thresholds are reached.

### Trigger Table

| Trigger | Threshold | Detection | Auto-Resume |
|---------|-----------|-----------|-------------|
| Context limit | >= 85% | Context monitor hook | No |
| Error threshold | >= 3 consecutive | Task completion failures | No |
| Blocked task | Any unresolved blocker | `can_start: false` | No |
| Task limit | N tasks (configurable) | Session counter | No |
| User interrupt | Ctrl+C or interrupt | Signal handler | No |
| Spec complete | All tasks done | Progress check | N/A |

### Context Limit (>= 85%)

**Detection:** The `context-monitor` hook reports `[CONTEXT X%]` warnings.

**Behavior:**
1. Complete current task if possible
2. Pause session with `reason="context_limit"`
3. Output recovery guidance

**Output:**
```
Context at 87%. Session paused at task-3-2.
Completed 5 tasks this session.
Run `/clear` then `foundry-implement --auto` to resume.
```

### Error Threshold (>= 3 Consecutive)

**Detection:** Task completion returns error or task marked blocked 3+ times in a row.

**Behavior:**
1. Pause session with `reason="error_threshold"`
2. List failed tasks with error summaries
3. Wait for user investigation

**Output:**
```
3 consecutive task failures. Session paused.
Failed tasks:
- task-2-1: ImportError in module X
- task-2-2: Test assertion failed
- task-2-3: Blocked by missing dependency
Fix issues manually, then `foundry-implement --auto` to resume.
```

### Blocked Task

**Detection:** `task action="prepare"` returns `can_start: false`.

**Behavior:**
1. Check if alternative tasks exist
2. If yes, skip to next available task (no pause)
3. If no, pause session with `reason="blocked_task"`

**Output:**
```
Next task (task-4-1) is blocked by: task-3-2 (incomplete)
No alternative tasks available. Session paused.
Resolve blocker or mark task as skipped, then resume.
```

### Task Limit

**Detection:** Session `completed_tasks` count reaches threshold.

**Purpose:** Periodic checkpoint for user review.

**Default:** 10 tasks (configurable via session-config).

**Output:**
```
Completed 10 tasks this session. Checkpoint pause.
Progress: 10/25 tasks (40%)
Review changes, then `foundry-implement --auto` to continue.
```

### User Interrupt

**Detection:** Ctrl+C or SIGINT signal.

**Behavior:**
1. Complete current atomic operation if safe
2. Pause session with `reason="user_requested"`
3. Save state for resume

## Recovery Patterns

### After /clear

Session state persists in MCP storage. Recovery flow:

```
User runs: foundry-implement --auto
    │
    ├─ Check session-config status
    │
    ├─ Session exists and paused?
    │       │
    │       ├─ Yes → "Resume session? (paused at task-X)"
    │       │           ├─ Resume → Continue from current_task
    │       │           └─ Fresh → End session, start new
    │       │
    │       └─ No → Start new session
    │
    └─ Begin autonomous execution
```

### After Context Limit

1. Run `/clear` to reset context
2. Run `foundry-implement --auto`
3. Accept "Resume session" prompt
4. Execution continues from paused task

### After Error Threshold

1. Review error output from pause message
2. Fix underlying issues (imports, tests, dependencies)
3. Run `foundry-implement --auto`
4. Accept "Resume session" prompt
5. Error counter resets on successful task completion

### After Blocked Task

**Option A: Resolve the blocker**
1. Complete the blocking task manually
2. Run `foundry-implement --auto` to resume

**Option B: Skip the blocked task**
1. Mark task as blocked/skipped via MCP
2. Run `foundry-implement --auto` to continue with next available

### Abandoning a Session

To start completely fresh:
```bash
foundry-implement --auto
# When prompted "Resume session?", select "Start fresh"
```

Or explicitly end:
```bash
mcp__plugin_foundry_foundry-mcp__task action="session-config" spec_id={spec-id} command="end"
```

## Gate Comparison

How decision points differ between modes:

| Gate | Interactive Mode | Autonomous Mode |
|------|------------------|-----------------|
| **Task selection** | AskUserQuestion with options | Auto-select recommended task |
| **Plan approval** | AskUserQuestion required | Skip (use recommended plan) |
| **Implementation start** | Explicit "Approve & Start" | Auto-start after prepare |
| **Task completion** | Mark complete, surface next | Mark complete, auto-continue |
| **Continue prompt** | "Continue to next task?" | Skip (auto-continue) |
| **Blocked task** | Present alternatives | Auto-skip or pause |
| **Context warning** | Suggest /clear | Auto-pause session |
| **Spec complete** | Report completion | Report completion (same) |

### Gates That Always Apply

Even in autonomous mode, these gates require interaction:

| Gate | Reason |
|------|--------|
| Pause recovery | User must confirm resume vs fresh start |
| Error investigation | User must fix issues before continuing |
| Spec activation | Initial spec selection is always interactive |

### Gates That Are Skipped

| Gate | Autonomous Behavior |
|------|---------------------|
| Task selection | Use `task action="prepare"` recommendation |
| Plan details | Accept generated plan |
| Continue prompt | Proceed immediately |

## Auto-Commit Behavior

After marking a task complete, check the response for `suggest_commit`:

### When `suggest_commit: true` and `commit_scope: "task"`

The git cadence is set to "task" - commit after each task:

1. Stage all changes: `git add -A`
2. Commit with message from `commit_message_hint` (e.g., "task: Implement user validation")
3. Do NOT prompt - this is silent auto-commit per user config
4. Continue to next task

### When `suggest_commit: true` and `commit_scope: "phase"`

The git cadence is set to "phase" and a phase just completed:

1. Stage all changes: `git add -A`
2. Commit with message from `commit_message_hint` (e.g., "phase: Core API Implementation")
3. Do NOT prompt - this is silent auto-commit per user config
4. Continue to next task

### When `suggest_commit: false`

No commit action needed. The git cadence is either "manual" or no phase boundary was crossed. Continue to next task.

### Example Task Completion Response

```json
{
  "status": "success",
  "data": {
    "task_id": "task-1-2",
    "completed_at": "2025-01-03T10:00:00Z",
    "progress": {"completed_tasks": 5, "total_tasks": 12, "percentage": 42},
    "suggest_commit": true,
    "commit_scope": "task",
    "commit_message_hint": "task: Add input validation"
  }
}
```

## Best Practices

### Before Starting Autonomous Mode

1. **Review the spec** - Ensure tasks are well-defined
2. **Check dependencies** - Verify external deps are available
3. **Commit current work** - Clean git state recommended
4. **Set reasonable task limit** - Prevent runaway execution

### During Autonomous Execution

1. **Monitor output** - Watch for warnings
2. **Don't interrupt mid-task** - Wait for task boundaries
3. **Check git status** - Periodically verify changes

### After Pause

1. **Review completed work** - Check git diff
2. **Address pause reason** - Don't just resume blindly
3. **Run tests** - Verify accumulated changes work together

### Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Ignoring context warnings | OOM or truncation | Pause and /clear promptly |
| Resuming without fixing errors | Immediate re-pause | Investigate root cause first |
| Running on unclear specs | Poor quality output | Use interactive for exploration |
| Never reviewing progress | Drift from intent | Use task limits for checkpoints |
