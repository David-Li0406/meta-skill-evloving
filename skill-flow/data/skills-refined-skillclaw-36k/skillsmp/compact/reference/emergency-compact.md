# Emergency Compact Procedure

Use this when context is critical and standard compact isn't fast enough.

## When to Use Emergency Compact

- Context at 95%+ and still receiving errors
- Memory warnings appearing
- Tool calls failing due to context limits
- Must preserve work immediately

## Emergency Procedure

### Step 1: Immediate State Capture (30 seconds)

Write to `.context/emergency-state.md`:

```markdown
# Emergency State - [timestamp]

## Current Task
[One sentence: what you're doing]

## Files Modified
[List files, one per line]

## Critical Context
[3-5 bullet points of must-know facts]

## Next Action
[Exactly what to do next]
```

### Step 2: Notify User

```
EMERGENCY COMPACT REQUIRED

Context is at critical levels. I've saved emergency state to:
.context/emergency-state.md

To continue:
1. Start a new conversation
2. Run /session-start
3. Reference emergency-state.md

Work preserved:
- [list key items]
```

### Step 3: Stop Work

Do not attempt further tool calls. Context is exhausted.

## Recovery

1. New session starts
2. `/session-start` runs
3. Loads emergency-state.md
4. Continues from "Next Action"

## Prevention

- Run `/context-status` every 30-45 minutes
- `/checkpoint` after milestones
- Delegate aggressively to subagents
- Don't load unnecessary files

## Signs You're Approaching Emergency

| Warning | Level | Action |
|---------|-------|--------|
| Responses shorter | Medium | `/checkpoint` |
| Forgetting recent context | High | Standard `/compact` |
| Tool calls failing | Critical | Emergency compact |
