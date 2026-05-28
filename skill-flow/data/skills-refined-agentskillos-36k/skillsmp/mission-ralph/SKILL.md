---
name: mission-ralph
description: "Launch ralph.sh in background. Best for large features (10+ tasks). Automatic execution until completion."
---

# /mission-ralph - Automatic Background Execution

Launch the Ralph loop in background. Runs automatically until all tasks complete or a critical blocker halts execution.

## The Process

1. **Validate feature** - Check feature exists and has tasks
2. **Activate feature** - Run `bd update FEATURE_ID --status in_progress`
3. **Launch Ralph** - Run script in background
4. **Inform user** - Tell them how to monitor progress
5. **Exit** - HOUSTON's job is done, Ralph takes over

## Launch Command

```bash
bash skills/mission/scripts/ralph.sh FEATURE_ID &
```

Or with visible mode (mprocs TUI):
```bash
bash skills/mission/scripts/ralph.sh FEATURE_ID --visible
```

## What Ralph Does

Ralph spawns fresh Pods for each task in a loop:
1. Get next ready task via `bd ready`
2. Spawn Pod (Scout -> Worker -> Inspector -> Analyst -> Airlock)
3. Handle result (complete, retry, or create blocking bug)
4. Continue until no tasks remain or critical halt

Each Pod includes a Scout phase that gathers codebase context before Worker executes.

## User Communication

After launching:

```
HOUSTON: Ralph loop launched for feature FEATURE_ID.

         Ralph runs automatically in background.
         Check progress: /capcom

         You'll be notified on:
         - Feature completion
         - Critical blocker (requires intervention)

         Safe to close this session.
```

## Monitoring

- `/capcom` - Check feature status and task progress
- `bd list --parent FEATURE_ID` - See all tasks
- `bd ready` - See what's next in queue
- `bd dep tree FEATURE_ID` - See task hierarchy and status

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Feature complete |
| 1 | Critical blocker - check `/capcom` |
| 2 | Configuration error |
