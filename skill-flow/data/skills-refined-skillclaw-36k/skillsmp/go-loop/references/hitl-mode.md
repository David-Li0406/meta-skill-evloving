# HITL Mode - Hook-Based Iteration

Human-In-The-Loop mode uses Claude Code's stop hook to create a continuous iteration
loop within a single session.

## How It Works

1. Claude attempts to exit after completing work
2. Stop hook intercepts the exit
3. Hook validates completion (prd.json updated, commit exists, reviews run)
4. If not complete, hook blocks exit and injects next prompt
5. Claude continues with accumulated context

## Advantages

- **Full context** - Claude sees all previous work in conversation
- **Interactive** - Can intervene, redirect, or clarify at any point
- **Debugging-friendly** - Watch each step, understand failures

## Disadvantages

- **Context rot** - Output quality can degrade as context fills
- **Session limits** - May hit context limits on long PRDs
- **Requires attention** - Not truly "away from keyboard"

## When to Use

- Learning a new workflow
- Debugging problematic stories
- Tasks requiring judgment calls
- When you want to observe and potentially intervene

## Single Iteration Mode (`--once`)

Use `--once` to run exactly one iteration, then stop:

```bash
/go plans/feature/prd.json --once
```

This is valuable for:
- Testing PRD quality before committing to full loop
- Debugging specific story failures
- Understanding what Claude will do before letting it loose

## Workflow Example

```
1. /go plans/auth/prd.json --once    # Test story #1
2. Review output, adjust PRD if needed
3. /go plans/auth/prd.json --once    # Test story #2
4. Confident in pattern? Remove --once
5. /go plans/auth/prd.json           # Let it run
```

## Pre-Commit Review Requirement

HITL mode enforces mandatory reviews before commits:

```xml
<!-- Must appear BEFORE commit -->
<reviews_complete/>

<!-- After commit with story reference -->
<story_complete story_id="1"/>
```

The stop hook blocks advancement until reviews are run and findings addressed.

## Marker Reference

| Marker | Purpose |
|--------|---------|
| `<reviews_complete/>` | Signal that reviewers ran and findings addressed |
| `<story_complete story_id="N"/>` | Signal story N committed |
| `<promise>TEXT</promise>` | Exit loop with completion (generic mode) |

## Fallback Detection

If markers are forgotten, the hook can auto-detect:
- prd.json has `passes: true` for story
- Git commit exists with story reference

But `<reviews_complete/>` is **always required** - no fallback for quality gate.
