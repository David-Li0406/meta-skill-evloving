# AFK Mode - External Ralph-Style Loop

Away From Keyboard mode uses an external bash script to iterate, giving each
Claude invocation a fresh context window.

## How It Works

1. External bash `for` loop runs `claude -p "prompt"` repeatedly
2. Each iteration is a completely fresh Claude session
3. State persists in prd.json only (single source of truth)
4. Script checks prd.json for completion between iterations
5. Continues until all stories pass or max iterations reached

## Advantages

- **Fresh context every iteration** - No context rot
- **Truly unattended** - Can run overnight
- **Scalable** - Handle large PRDs without context limits
- **Resilient** - Session crashes don't lose progress

## Disadvantages

- **No accumulated context** - Each iteration starts fresh
- **File-based state only** - Can't remember conversation nuances
- **Less interactive** - Harder to intervene mid-run

## When to Use

- Bulk implementation work (many stories)
- Overnight/weekend runs
- Well-defined, low-risk tasks
- When you trust the PRD and want hands-off execution

## Usage Patterns

```bash
# Basic AFK mode
/go plans/feature/prd.json --afk

# With iteration limit
/go plans/feature/prd.json --afk --max 30

# With streaming output (recommended for monitoring)
/go plans/feature/prd.json --afk --stream
```

## Streaming Output

The `--stream` flag provides real-time visibility using jq filters:

```bash
/go plans/feature/prd.json --afk --stream
```

This shows Claude's output as it generates, useful for:
- Monitoring progress remotely
- Catching issues early
- Understanding what's happening without full attention

## Docker Sandbox (Requires Docker Desktop 4.50+)

For additional isolation:

```bash
/go plans/feature/prd.json --afk --sandbox
```

**Note:** `docker sandbox` is a Docker Desktop 4.50+ feature. Not available in
OrbStack, Colima, or standard Docker CLI. Skip `--sandbox` if unavailable.

## Completion Detection

The AFK script checks after each iteration:

1. **All stories pass?** - `jq '[.stories[] | select(.passes == false)] | length'`
2. **Completion promise?** - `<promise>ALL STORIES COMPLETE</promise>` in output
3. **Max iterations?** - Stop if limit reached

## File-Based State

AFK mode relies on prd.json as single source of truth:

| File | Purpose |
|------|---------|
| `prd.json` | Story status, completion times, commits, embedded log |
| Git history | Completed work |

## Prompt Structure

Each AFK iteration receives a prompt containing:
- Reference to prd.json and spec.md
- Current story details
- Instructions for autonomous work
- Completion markers to output

## Recommended Progression

```
Day 1: /go prd.json --once           # Learn the PRD
Day 1: /go prd.json --once           # Test a few more stories
Day 2: /go prd.json                  # HITL when confident
Day 3: /go prd.json --afk --stream   # AFK when proven
```

## Troubleshooting

**Iterations complete instantly without work:**
- Check if `docker sandbox` is available (Docker Desktop 4.50+ only)
- Remove `--sandbox` flag to run directly

**Stories not progressing:**
- Check prd.json for `passes: true` updates
- Check prd.json's `log` array for error entries
- Check git log for commits

**Context rot symptoms (shouldn't happen in AFK):**
- Verify actually using `--afk` flag
- Each iteration should show fresh session start
