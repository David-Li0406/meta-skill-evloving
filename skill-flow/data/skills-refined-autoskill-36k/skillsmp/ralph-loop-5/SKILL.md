---
name: ralph-loop
description:
  Autonomous development loop with fresh context per iteration. Uses an external bash loop that
  spawns fresh Claude sessions, storing state in files to prevent context drift. Based on the
  original Ralph Wiggum technique by Geoffrey Huntley.
---

# Ralph Loop

An autonomous development loop for Claude Code. The key insight: **fresh context per iteration**
with **file I/O as state**.

## Core Principles

### 1. Fresh Context Per Iteration

Each iteration spawns a **new Claude session**. No transcript accumulation.

```
Iteration 1: claude -p "task.md" → works → exits
Iteration 2: claude -p "task.md" → sees files from iter 1 → works → exits
Iteration 3: claude -p "task.md" → sees files from iter 1+2 → works → exits
```

### 2. File I/O as State

All state lives in `.ralph/`:

- `spec.md` - The task specification (re-read each iteration)
- `state.json` - Iteration count, attempts, status
- `progress.log` - Append-only progress tracking
- `evidence/` - Proof of work (iteration outputs, test results)

### 3. Re-Anchoring Every Iteration

Before each iteration, Claude re-reads:

- The original task specification
- Current git state
- Test results from previous iteration
- Evidence of completed work

This prevents drift and ensures the model stays grounded in reality.

### 4. Failure Handling

- Track attempts per task
- Auto-block after N failures with a reason file
- Failed iterations don't pollute future context

## Directory Structure

```
.ralph/
├── spec.md              # Task specification (user-provided)
├── state.json           # Loop state (iteration, attempts, status)
├── progress.log         # Append-only execution log
├── evidence/            # Proof of work
│   ├── iter-001.log     # Raw output from iteration 1
│   ├── iter-002.log     # Raw output from iteration 2
│   └── ...
└── blocked.md           # If task gets stuck (reason + suggestions)
```

## Usage

### Initialize a Ralph Loop

```bash
# Create spec file and initialize state
/ralph-init "Build a REST API with CRUD operations. Tests must pass."
```

### Run the Loop

```bash
# External bash loop - run from terminal
~/.claude/skills/ralph-loop/scripts/ralph.sh
```

### Monitor Progress

```bash
# Check current state
cat .ralph/state.json | jq .

# View progress log
tail -f .ralph/progress.log

# See latest iteration output
cat .ralph/evidence/iter-*.log | tail -100
```

### Stop the Loop

The loop stops when:

1. Claude outputs `<promise>DONE</promise>` (completion)
2. Max iterations reached (default: 25)
3. Max attempts per task exceeded (default: 5)
4. You press Ctrl+C

## Configuration

Environment variables:

- `RALPH_MAX_ITERATIONS` - Max loop iterations (default: 25)
- `RALPH_MAX_ATTEMPTS` - Attempts before blocking (default: 5)
- `RALPH_TIMEOUT` - Seconds per iteration (default: 1800)
- `RALPH_PROMISE` - Completion promise text (default: DONE)
- `RALPH_MODEL` - Claude model to use

## When to Use

**Good for:**

- Well-defined tasks with testable success criteria
- Tasks requiring iteration (get tests to pass)
- Overnight/unattended runs
- Tasks with automatic verification

**Not good for:**

- Tasks requiring human judgment
- Unclear success criteria
- Interactive exploration

## Credits

Based on the Ralph Wiggum technique by Geoffrey Huntley (ghuntley.com/ralph).
