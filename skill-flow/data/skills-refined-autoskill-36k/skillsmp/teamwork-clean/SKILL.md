---
name: teamwork-clean
description: "This skill should be used when agents need to reset a teamwork project's execution state while preserving metadata. Use before starting a new project in the same session, after a failed project, or when task/verification state is corrupted. Cleans tasks/, verification/, workers/ directories while keeping project.json intact."
---

# Teamwork Clean

## Overview

Teamwork-clean resets a project's execution state to start fresh while preserving project metadata and history.

### Core Principles

1. **Surgical deletion** - Only removes execution artifacts (tasks, verification, workers)
2. **Metadata preservation** - Project identity, goal, and creation timestamp remain intact
3. **Idempotent operation** - Safe to run multiple times, won't clean already-cleaned projects
4. **Fresh start marker** - Adds `cleaned_at` timestamp to track cleanup history

### Use Case

When task state becomes inconsistent, workflow fails, or you need to restart execution with the same project configuration.

---

## When to Use

**USE teamwork-clean for:**
- Starting a new run in the same project (multiple attempts at same goal)
- Recovering from failed orchestration or stuck workers
- Cleaning up after testing or experimentation
- Resolving state corruption (duplicate tasks, conflicting claims, orphaned locks)

**DON'T use teamwork-clean for:**
- Normal project completion (state is valuable)
- Abandoning a project (use project deletion instead)
- Fixing a single task (use task-update --release instead)
- Active projects with workers running (stop workers first)

---

## What Gets Cleaned

The clean operation **deletes** these directories completely:

| Directory | Contents | Impact |
|-----------|----------|--------|
| `tasks/` | All task files (*.json) | Task definitions, status, evidence, claims |
| `verification/` | Verification results (wave-*.json, final.json) | Wave and final verification history |
| `workers/` | Worker state and logs | Worker session tracking, activity history |

**After cleanup**: These directories no longer exist. You start with a blank slate for execution.

---

## What's Preserved

The clean operation **preserves** project metadata:

| File | Preserved Data | Changes |
|------|---------------|---------|
| `project.json` | - Project name and team<br>- Goal description<br>- Creation timestamp<br>- Phase information | - Adds `cleaned_at` timestamp<br>- Resets stats to 0 (total, open, in_progress, resolved)<br>- Updates `updated_at` timestamp |
| `waves.json` | ❌ Deleted (if exists) | Wave definitions removed, will be regenerated on next run |

**Why preserve project.json?**
- Maintains project identity for status tracking
- Keeps goal definition for next attempt
- Tracks cleanup history via `cleaned_at` field
- Enables "retry with same goal" workflow

---

## Usage

### Command Invocation

```bash
/teamwork-clean --project <PROJECT> --team <TEAM>
```

### Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `--project` | Project name | Yes |
| `--team` | Sub-team name | Yes |

### Output

```
═══════════════════════════════════════════════════════════
 TEAMWORK PROJECT CLEANED
═══════════════════════════════════════════════════════════

 Project: my-app/auth-team
 Goal: Implement user authentication
 Created: 2026-01-15T10:00:00Z
 Cleaned: 2026-01-16T15:30:00Z

───────────────────────────────────────────────────────────

 Deleted directories:
 - tasks/
 - verification/
 - workers/

 Project metadata preserved in:
 ~/.claude/teamwork/my-app/auth-team/project.json

 Start fresh with:
 /teamwork --project "my-app" --team "auth-team"

═══════════════════════════════════════════════════════════
```

---

## Workflow Integration

### Before Starting New Project Run

```bash
# Check if project needs cleaning
/teamwork-status --project my-app --team auth-team

# If state is corrupted or you want fresh start
/teamwork-clean --project my-app --team auth-team

# Start new execution
/teamwork --project my-app --team auth-team
```

### After Failed Project

```bash
# Project failed, want to retry with different approach
/teamwork-clean --project my-app --team auth-team

# Orchestrator will plan from scratch
/teamwork --project my-app --team auth-team
```

### Handling Stuck Workers

```bash
# Workers are stuck on tasks, state is inconsistent
# First: Stop all workers (Ctrl+C in each terminal)

# Then: Clean the project
/teamwork-clean --project my-app --team auth-team

# Finally: Start fresh
/teamwork --project my-app --team auth-team
```

---

## Safety Guarantees

### Idempotency

```javascript
// First clean: Deletes tasks/, verification/, workers/
/teamwork-clean --project my-app --team auth-team
// Output: Project cleaned successfully

// Second clean: Detects already cleaned
/teamwork-clean --project my-app --team auth-team
// Output: Project my-app/auth-team already cleaned at 2026-01-16T15:30:00Z
```

**Guarantee**: Running clean multiple times is safe. Already-cleaned projects won't be cleaned again.

### No Data Loss Beyond Execution State

**Preserved**:
- Project name, goal, creation timestamp
- Project directory structure
- `cleaned_at` history for audit trail

**Deleted**:
- Task files (can be regenerated by orchestrator)
- Verification results (will be regenerated on execution)
- Worker logs (not needed after cleanup)

**Guarantee**: Project identity and goal remain intact. Only execution artifacts are removed.

### Error Handling

| Scenario | Behavior | Exit Code |
|----------|----------|-----------|
| Project doesn't exist | Error message, no changes | 1 |
| Directory deletion fails | Error message, partial cleanup possible | 1 |
| project.json update fails | Error message, directories may be deleted | 1 |

**Guarantee**: Script exits with error code 1 on any failure. Check output for details.

---

## Examples

### Example 1: Fresh Start After Testing

```bash
# Scenario: Tested orchestration, want clean state for actual work

# Current state has test tasks
/teamwork-status --project my-app --team auth-team
# Output: 5 tasks (3 resolved, 2 open)

# Clean the project
/teamwork-clean --project my-app --team auth-team
# Output: Deleted tasks/, verification/, workers/

# Verify clean state
/teamwork-status --project my-app --team auth-team
# Output: 0 tasks, ready for fresh start
```

### Example 2: Recovering from Corrupted State

```bash
# Scenario: Workers claimed tasks but never completed, locks are stale

# Check status (shows stuck tasks)
/teamwork-status --project my-app --team auth-team
# Output: Task 3 claimed by session-abc (30 minutes ago), still in_progress

# Stop all workers
# (Ctrl+C in each worker terminal)

# Clean the project
/teamwork-clean --project my-app --team auth-team
# Output: Deleted corrupted task state

# Start fresh
/teamwork --project my-app --team auth-team
# Output: Orchestrator creates new task plan
```

### Example 3: Multiple Cleanup Attempts

```bash
# Scenario: Want to try different planning approaches

# First attempt
/teamwork --project my-app --team auth-team
# (Orchestrator creates plan, workers execute, fails)

# Clean and retry
/teamwork-clean --project my-app --team auth-team
/teamwork --project my-app --team auth-team
# (New plan, still fails)

# Clean and retry again
/teamwork-clean --project my-app --team auth-team
/teamwork --project my-app --team auth-team
# (Third attempt succeeds)

# Check cleanup history
cat ~/.claude/teamwork/my-app/auth-team/project.json
# Shows: cleaned_at timestamp from last cleanup
```

---

## Agent Guidance

### Decision-Making Checklist

Before recommending `/teamwork-clean`, verify:

1. **Is the project stuck?**
   - Check `/teamwork-status` for task progress
   - Look for tasks claimed > 1 hour ago with no progress
   - Check for verification failures that block progress

2. **Are workers stopped?**
   - Cleaning while workers are active causes race conditions
   - Instruct user to stop workers first (Ctrl+C)

3. **Is cleanup the right solution?**
   - Single stuck task → Use `task-update --release` instead
   - Want to abandon project → Delete project directory instead
   - Just checking status → Use `/teamwork-status` only

4. **Has user confirmed data loss?**
   - Cleaning deletes all task definitions and evidence
   - If valuable work exists, suggest backing up first
   - Explain cleanup is irreversible for execution state

### When to Recommend Clean

| Situation | Recommend Clean? | Alternative |
|-----------|------------------|-------------|
| First project attempt failed | Yes | Explain what went wrong, clean, retry |
| Multiple stale task claims | Yes | Stop workers, clean, restart |
| Corrupted verification state | Yes | Clean verification/, restart |
| Single task needs retry | No | Use `task-update --release` |
| Want to change goal | No | Create new project instead |
| Checking progress | No | Use `/teamwork-status` only |

### Communication Pattern

```markdown
**Detected Issue**: [Describe what's wrong - e.g., "3 tasks stuck in progress for >1 hour"]

**Recommended Action**: Clean project state and start fresh

**Steps**:
1. Stop all active workers (Ctrl+C in worker terminals)
2. Run: `/teamwork-clean --project my-app --team auth-team`
3. Verify clean state: `/teamwork-status --project my-app --team auth-team`
4. Start fresh: `/teamwork --project my-app --team auth-team`

**What gets deleted**: tasks/, verification/, workers/ directories
**What's preserved**: project.json with goal and metadata
```

---

## Related Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/teamwork` | Start or resume project | After cleaning, to begin fresh execution |
| `/teamwork-status` | Check project progress | Before cleaning, to diagnose issues |
| `/teamwork-worker` | Start worker | After cleaning, for task execution |
| `task-update --release` | Release single task | Alternative to cleaning for stuck task |

---

## Additional Resources

### Script Reference

- **Location**: `plugins/teamwork/src/scripts/project-clean.js`
- **Called by**: `/teamwork-clean` command
- **Dependencies**: `project-utils.js`, `args.js`

### State Schema

See teamwork CLAUDE.md for:
- Project state format (project.json)
- Task state format (tasks/*.json)
- Verification state format (verification/*.json)
