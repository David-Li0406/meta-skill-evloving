---
name: unstuck
description: Structured problem-solving workflow for debugging. Use after 3 failed attempts at solving an issue, when stuck on a problem, or when encountering repeated errors.
---

# Structured Problem-Solving Workflow

Use this workflow after 3 failed attempts at solving an issue.

## Step 1: Document What Failed

Before trying anything else, document:

- **What you tried** (list each approach)
- **Specific error messages** (exact text)
- **Why you think it failed** (hypothesis)

```markdown
## Failed Attempts Log

### Attempt 1: [approach]
- Error: [message]
- Hypothesis: [why it failed]

### Attempt 2: [approach]
- Error: [message]
- Hypothesis: [why it failed]

### Attempt 3: [approach]
- Error: [message]
- Hypothesis: [why it failed]
```

## Step 2: Research Alternatives

Find 2-3 similar implementations in:
- The same codebase (how do similar features work?)
- Open source projects (how do others solve this?)
- Official documentation (what's the intended approach?)

Note the different approaches used and why they might work.

## Step 3: Question Fundamentals

Ask yourself:

1. **Is this the right abstraction level?**
   - Am I solving too high-level or too low-level?
   - Should I be working at a different layer?

2. **Can this be split into smaller problems?**
   - What's the smallest piece I can verify works?
   - Can I isolate the failing component?

3. **Is there a simpler approach entirely?**
   - Am I over-engineering?
   - What would the boring solution look like?

## Step 4: Try a Different Angle

Consider:

- **Different library/framework feature** - Is there a built-in solution?
- **Different architectural pattern** - Would a different pattern simplify this?
- **Remove abstraction** - Would removing a layer make it clearer?
- **Invert the approach** - Push vs pull? Sync vs async? Client vs server?

## Output

After completing these steps, you should have either:
1. A new approach to try
2. A clear question to ask for help
3. Understanding that the problem is blocked on external factors

If still stuck after this workflow, escalate with your documented attempts.
