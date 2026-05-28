---
name: ralph-eats-beads
description: Autonomous AI coding loop using bd for task management with parallel tmux subagents. Ships features while you sleep.
license: MIT
---

# Ralph BD - Parallel Autonomous Coding Loop

**Contract**: `skills-lib-lkv` (Ralph Contract v1)

Ralph runs Claude agents in a loop, picking tasks from `bd ready`, implementing them, and closing them on success. This version uses tmux for observability and supports parallel subagents.

## Architecture

```
ralph (tmux session)
├── parent (window 0) - orchestrator Claude
├── watchdog (window 1) - health monitor Claude (optional)
├── BD-001 (window 2) - subagent
├── BD-002 (window 3) - subagent
└── BD-003 (window 4) - subagent
```

## Prerequisites

- **bd** initialized with issues/epic
- **tmux** installed
- **Claude CLI** (`claude` command available)

## Quick Start

### Option A: Manual Plan (you create issues)

```bash
# 1. Create your epic and issues
bd create --type epic "Feature: User Authentication"
bd create "Add login form" --parent BD-001 --priority 1
bd create "Add email validation" --parent BD-001 --priority 2
bd create "Add auth server action" --parent BD-001 --priority 3

# 2. Start Ralph (25 max iterations)
scripts/ralph.sh 25

# 3. Attach to watch
tmux attach -t ralph
```

### Option B: AI-Generated Plan (planner creates issues)

```bash
# 1. Let Claude create the plan from requirements
scripts/planner.sh requirements.md

# Or inline:
scripts/planner.sh <<< "Add OAuth2 authentication with Google and GitHub providers"

# Or pipe from anywhere:
cat feature-spec.md | scripts/planner.sh

# 2. Watch the planner
tmux attach -t ralph-plan

# 3. Once plan is created, implement it
scripts/ralph.sh 25
```

## Planning vs Implementation

| Script | Session | Purpose |
|--------|---------|---------|
| `planner.sh` | ralph-plan | **Recursive loop** - creates/refines bd issues until plan is complete |
| `ralph.sh` | ralph | **Parallel loop** - implements issues from `bd ready` |

**Workflow:**
```
Requirements → planner.sh (iterates) → bd issues → ralph.sh (parallel) → Implemented code
```

Both loops support `MAX_ITERATIONS` - planner defaults to 3, implementation defaults to 10.

## How It Works

**Key principle**: Bash manages the iteration loop, each iteration gets fresh Claude context.

```
ralph.sh (bash loop)
├── Iteration 1
│   ├── Spawn fresh Claude parent
│   ├── Parent spawns subagents, then exits
│   ├── Bash waits for subagent windows to close
│   ├── bd sync
│   └── Check bd ready → continue or done
├── Iteration 2
│   └── (repeat with fresh context)
└── ...
```

1. Bash checks `bd ready` for available work
2. Bash spawns fresh Claude parent for this iteration
3. Parent runs `bd prime`, analyzes parallelizability
4. Parent spawns subagent tmux windows (3-5 concurrent), then exits
5. Bash waits for all subagent windows to close
6. Each subagent implements ONE issue, commits, closes issue
7. Bash syncs bd and loops until no work remains

## Observer Commands

```bash
# Attach to see everything
tmux attach -t ralph

# Tile all panes
tmux select-layout -t ralph tiled

# Watch specific agent
tmux select-window -t ralph:BD-123

# Capture agent output
tmux capture-pane -t ralph:BD-123 -p -S -1000 > agent.log

# Kill stuck agent
tmux kill-window -t ralph:BD-123

# Kill entire session
tmux kill-session -t ralph
```

## Planner Details

The planner (`scripts/planner.sh`) runs a **recursive loop** that iterates until the bd plan fully covers the input requirements:

```
while iteration < MAX_ITERATIONS:
    1. Read input plan file
    2. Check current bd state (existing issues)
    3. Compare: what's in the plan but missing from bd?
    4. If nothing missing → exit with summary
    5. Create missing issues with dependencies
    6. Repeat
```

Each iteration the planner:
1. **Re-reads the plan** - Keeps the source of truth in focus
2. **Audits bd state** - What stories exist? What's missing?
3. **Fills gaps** - Creates issues for uncovered sections
4. **Sets dependencies** - Ensures correct build order

This ensures complex plans with many sections get fully decomposed into implementable stories.

### Input Formats

```bash
# From file
scripts/planner.sh requirements.md
scripts/planner.sh feature-spec.txt

# Inline (heredoc)
scripts/planner.sh << 'EOF'
Add user authentication:
- OAuth2 with Google and GitHub
- Session management with JWT
- Protected routes middleware
EOF

# One-liner
scripts/planner.sh <<< "Add dark mode with system preference detection"

# Pipe from anywhere
curl -s https://example.com/spec.md | scripts/planner.sh
gh issue view 123 --json body -q .body | scripts/planner.sh
```

### What the Planner Creates

```
Epic: AUTH-001 "Feature: OAuth2 Authentication"
├── AUTH-002 "Add OAuth2 configuration" [ready]
├── AUTH-003 "Create Google provider" [depends: AUTH-002]
├── AUTH-004 "Create GitHub provider" [depends: AUTH-002]
├── AUTH-005 "Add callback handlers" [depends: AUTH-003, AUTH-004]
└── AUTH-006 "Add protected route middleware" [depends: AUTH-005]
```

Stories include:
- Clear acceptance criteria
- File paths to modify
- References to existing patterns
- Testing requirements

## Watchdog (Active Health Monitor)

The watchdog is a separate Claude agent that monitors Ralph sessions and unsticks them automatically. Unlike the passive monitor, it takes action:

```bash
# Start watchdog for a ralph session (30 second check interval)
scripts/watchdog.sh ralph-myproject 30

# It runs in its own tmux window within the session
tmux select-window -t ralph-myproject:watchdog
```

The watchdog:
- **Detects idle agents** - Looks for Claude CLI prompts indicating waiting state
- **Checks issue status** - Queries bd to see if work is complete
- **Nudges stuck agents** - Sends tmux keystrokes to prompt them to continue
- **Kills completed windows** - Cleans up windows where the issue is closed
- **Kicks the parent** - Sends Enter if parent is idle with work remaining

This keeps Ralph flowing autonomously without human intervention.

## Passive Monitor (Logging Only)

For unattended runs where you just want logging without intervention:

```bash
# Start monitor (checks every 20 min, logs to /tmp/ralph-monitor.log)
nohup scripts/monitor.sh 20 &

# Check status
tail -f /tmp/ralph-monitor.log
```

The passive monitor detects:
- **STOPPED**: Ralph session died unexpectedly
- **STUCK**: Only parent window but work remains (2 consecutive checks)
- **COMPLETE**: No ready work and only parent window
- **RUNNING**: Normal operation with active subagents

## bd Workflow

### Setup Work

```bash
# Create epic
bd create --type epic "Feature: Dark Mode"  # → BD-001

# Create stories
bd create "Add theme toggle" --parent BD-001 --priority 1
bd create "Add theme context" --parent BD-001 --priority 2
bd create "Update components" --parent BD-001 --priority 3

# Add dependencies (bd ready respects these)
bd dep add BD-004 BD-003  # BD-004 depends on BD-003
```

### Monitor Progress

```bash
bd ready              # What's workable?
bd epic status BD-001 # Epic completion
bd blocked            # What's stuck?
bd activity           # Recent changes
```

### After Completion

```bash
bd list --state closed --parent BD-001  # All closed?
bd show BD-002 --comments               # Review learnings
bd epic close-eligible                  # Close the epic
```

## Best Practices

### Right-Sized Stories

```
BAD:  "Build authentication system"
GOOD: "Add login form with email/password fields"
      "Add client-side email validation"
      "Create auth server action"
```

### Clear Acceptance Criteria

In issue body:
```
Acceptance Criteria:
- [ ] Email field with validation
- [ ] Password field with show/hide
- [ ] typecheck passes
- [ ] tests pass
```

### Learnings Accumulate

Agents add learnings via `bd comments`. Future iterations benefit:
```bash
bd show BD-005 --comments
bd search "migration pattern"
```

## Not Suitable For

- Exploratory work without clear criteria
- Major refactors spanning entire codebase
- Security-critical code
- Anything needing human review before commit
