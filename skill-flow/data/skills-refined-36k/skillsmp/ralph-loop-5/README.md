# Ralph Loop Skill

An autonomous development loop for Claude Code based on the Ralph Wiggum technique.

## Core Concept

Ralph is fundamentally simple: **a bash loop that repeatedly invokes Claude with fresh context**.

```
while not complete:
    claude -p "task.md"   # Fresh session each time
    check for completion
```

State persists in **files**, not conversation history. Each iteration re-reads the spec, checks git
state, and sees previous work in files - then works with fresh context.

## Installation

The skill is installed at `~/.claude/skills/ralph-loop/`.

Commands available:

- `/ralph-init` - Initialize a new Ralph loop
- `/ralph-status` - Check loop status
- `/ralph-cancel` - Cancel/cleanup a loop

## Quick Start

```bash
# 1. Initialize (in Claude Code)
/ralph-init "Build a REST API with CRUD operations. All tests must pass."

# 2. Run the loop (in terminal)
~/.claude/skills/ralph-loop/scripts/ralph.sh

# 3. Monitor (in another terminal)
tail -f .ralph/progress.log
```

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    External Bash Loop                        │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Iteration 1 │───▶│ Iteration 2 │───▶│ Iteration 3 │──▶  │
│  │ Fresh ctx   │    │ Fresh ctx   │    │ Fresh ctx   │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              .ralph/ (File I/O State)                │   │
│  │  spec.md | state.json | progress.log | evidence/    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

Each iteration:

1. Reads spec from `.ralph/spec.md` (re-anchoring)
2. Checks git state (re-anchoring)
3. Reads previous iteration output (re-anchoring)
4. Spawns fresh Claude session with prompt
5. Saves output to `.ralph/evidence/iter-NNN.log`
6. Checks for completion promise
7. Updates state in `.ralph/state.json`

## Configuration

Environment variables:

- `RALPH_MAX_ITERATIONS` - Max loop iterations (default: 25)
- `RALPH_MAX_ATTEMPTS` - Attempts before blocking (default: 5)
- `RALPH_TIMEOUT` - Seconds per iteration (default: 1800)
- `RALPH_PROMISE` - Completion promise text (default: DONE)
- `RALPH_MODEL` - Claude model to use (default: system default)

Command line:

```bash
ralph.sh --max-iterations 10 --promise "ALL_TESTS_PASS" --verbose
```

## Directory Structure

```
.ralph/
├── spec.md              # Task specification
├── state.json           # Loop state
├── progress.log         # Append-only log
├── evidence/            # Iteration outputs
│   ├── iter-001.log
│   ├── iter-002.log
│   └── ...
└── blocked.md           # Created if task blocks
```

## Completion

The loop stops when Claude outputs:

```
<promise>DONE</promise>
```

Or configure a custom promise:

```bash
/ralph-init "..." --promise "ALL_TESTS_PASS"
```

## Troubleshooting

**Loop never completes:**

- Check if tests are actually passing
- Review iteration logs: `cat .ralph/evidence/iter-*.log | less`
- Increase max iterations if making progress

**Task blocked:**

- Check `.ralph/blocked.md` for reason
- Reset attempts: `jq '.attempts = 0' .ralph/state.json > tmp && mv tmp .ralph/state.json`
- Remove block: `rm .ralph/blocked.md`

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
