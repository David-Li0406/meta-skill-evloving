---
name: context-management
description: Context window auto-reset procedures for Ralph agents
category: orchestration
depends-on: [ralph-core]
---

# Context Window Management

> "Your context will fill up after many iterations. Use automation to manage it."

## The Problem

After implementing many features or running many iterations, your context window will fill up. This causes:
- Slower responses
- Forgetting earlier instructions
- Inconsistent behavior

## The Solution: Automatic Context Reset

Use automation scripts to automatically restart your session when context is full.

### Start Auto-Monitor (Background Terminal)

Run in a separate terminal before starting your agent session:

```bash
# Option 1: Python (recommended)
python scripts/restart-agent.py --agent {AGENT} --monitor --threshold 70

# Option 2: PowerShell
powershell -File scripts/monitor-context.ps1 -AgentName {AGENT} -ContextThreshold 70
```

### What These Scripts Do

1. Monitor your context usage every 30 seconds
2. Automatically launch a new terminal at 70% capacity
3. Signal you to save your state and exit
4. The new session will automatically resume from state files

This enables **indefinite autonomous operation** without manual intervention.

## Manual Restart (If Automation Fails)

If you need to manually restart:

```bash
# PowerShell
.\scripts\restart-agent.ps1 -AgentName {AGENT}

# Python
python scripts/restart-agent.py --agent {AGENT}
```

## Before Restarting

Ensure your work is saved:

### PM Coordinator
- All tasks have updated status in `prd.json`
- `coordinator-progress.txt` has current summary
- `coordinator-state.json` is current
- No task is mid-assignment (complete or defer)

### Developer
- All changes committed to git
- Task status updated to "ready_for_qa" or "idle"
- No implementation mid-progress

### QA
- Validation results committed to PRD (`passes` field updated)
- Task status updated in `coordinator-state.json`
- All bugs logged in `current-task.json` if any
- No validation mid-progress

## After Restart

The new session will automatically reload essential state:

```bash
READ .claude/session/coordinator-state.json
READ .claude/session/current-task.json
READ prd.json
```

Continue from where you left off.

## What You Need to Resume

You only need these files to resume:

- `prd.json` - Task list and status
- `coordinator-state.json` - Session state
- `current-task.json` - Current task (if any)
- Agent-specific progress file

## What You Can Forget

After restart, you can safely forget:

- Past task implementation details
- Past retrospective discussions
- Old file contents you've read
- Completed task specifications
- Historical discussion transcripts

## Minimal Context Footprint

**Keep**:
- Current task specifications
- Currently edited files
- Quality mindset and coding standards
- Feedback loop commands
- Session state (iteration, stats)

**Don't keep**:
- Completed task file contents
- Past task specifications
- Historical discussion transcripts
- Past retrospective details (logged in files)

## Context Reset Detection in Polling Loop

Your polling loop should check for restart signals:

```
FOREVER:
  WAIT 30 seconds

  # CHECK FOR RESTART SIGNAL
  RUN: python scripts/restart-agent.py --agent {AGENT} --check
  IF exit code == 0 (signal detected):
    COMPLETE current work
    UPDATE coordinator-state.json
    SAVE pending work
    DELETE restart-flag-{AGENT}.json
    EXIT  # New terminal already launched

  # Continue normal polling...
```

## State File Persistence

These files survive across context resets:

| File | Purpose | Survives Reset |
|------|---------|----------------|
| `prd.json` | Task list | ✅ Yes |
| `coordinator-state.json` | Session state | ✅ Yes |
| `current-task.json` | Active task | ✅ Yes |
| `coordinator-progress.txt` | PM log | ✅ Yes |
| `developer-progress.txt` | Developer log | ✅ Yes |
| `qa-progress.txt` | QA log | ✅ Yes |
| `retrospective.txt` | Active retrospective | ✅ Yes |
| `persistent-state/consolidation-mode.json` | **Consolidation mode state** | ✅ Yes |

### ⚠️ IMPORTANT: Consolidation Mode State Preservation

**Consolidation mode state is now automatically preserved across context resets.**

When PM agent context is reset:
1. Consolidation mode state is saved to `persistent-state/consolidation-mode.json`
2. After reset, PM automatically restores consolidation mode
3. This prevents workers from being blocked after context resets

**Manual Recovery (if needed):**

```powershell
# Save consolidation state
. .\.claude\scripts\message-queue.ps1
Save-ConsolidationState -SessionDir ".claude\session"

# Restore consolidation state (after context reset)
Restore-ConsolidationState -SessionDir ".claude\session"
```

## Verification

To verify context reset is working:

1. Check `.claude/session/context-reset-count.txt` - should increment on each reset
2. Check that `iteration` counter in `coordinator-state.json` continues across resets
3. Verify agent continues working from where it left off

## Reference

- [ralph-core.md](ralph-core.md) — Session structure
- [ralph-event-protocol.md](ralph-event-protocol.md) — Event-driven messaging protocol
