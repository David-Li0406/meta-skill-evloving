---
name: task-review
description: Verify task completion across multi-agent projects through structured reflection. Use when (1) reviewing another agent's work before merging or handoff, (2) validating your own task completion before reporting done, (3) performing quality assurance on completed deliverables, (4) generating completion reports for stakeholders, or (5) checking if all success criteria have been met.
---

# Task Review

Structured reflection to verify task completion, maintain focus, and prevent context rot.

## Purpose

As context grows, agents tend to drift from original intent. This skill provides checkpoints to:
- **Reflect** on what was asked vs what's being done
- **Realign** attention to the core objective
- **Verify** completion against success criteria

## Quick Reflection

Ask these questions at any point:

1. **What was I asked to do?** (Original intent)
2. **What have I done so far?** (Current state)
3. **Am I still on track?** (Alignment check)
4. **What's left?** (Remaining work)

## Reflection Workflow

### Step 1: Recall Original Intent

Before proceeding, explicitly state:

- **The ask**: What did the user/requester actually want?
- **Success looks like**: How will we know it's done?
- **Scope boundaries**: What's included? What's explicitly NOT included?

> [!TIP]
> If you can't clearly state the original intent, context rot may have occurred. Go back to the original request.

### Step 2: Audit Current State

List what has been accomplished:

| Action Taken | Relates to Original Ask? | Still Relevant? |
|--------------|--------------------------|-----------------|
| [action 1]   | ✅ / ⚠️ / ❌             | Yes / No        |
| [action 2]   | ✅ / ⚠️ / ❌             | Yes / No        |

**Signs of drift:**
- Actions that don't map to the original ask
- Rabbit holes pursued without clear purpose
- Scope creep beyond initial boundaries

### Step 3: Refocus Attention

If drift detected, course-correct:

1. **Stop** - Pause current activity
2. **Summarize** - What's the core objective in one sentence?
3. **Prioritize** - What's the single most important next step?
4. **Resume** - Continue with renewed focus

### Step 4: Verify Completion

Before marking done:

```
□ Original intent addressed
□ All stated success criteria met
□ No critical gaps remain
□ Result is usable/actionable
```

## Completion Status

**COMPLETE** - Original intent fully addressed, success criteria met

**NEEDS WORK** - Partial progress, clear gaps remain

**BLOCKED** - Cannot proceed without external input

**OFF TRACK** - Significant drift, needs re-planning

## Reflection Report Template

```markdown
# Task Reflection

## Original Intent
[What was asked, in one sentence]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Current State
[Brief summary of what's been done]

## Alignment Check
- On track: [Yes/No/Partially]
- Drift detected: [None/Minor/Significant]

## Status: [COMPLETE | NEEDS WORK | BLOCKED | OFF TRACK]

## Next Actions
- [If not complete, what's next]
```

## When to Reflect

Use this skill:

- **Before starting** - Clarify intent upfront
- **Mid-task checkpoint** - Every 5-10 actions, pause and reflect
- **Before reporting done** - Final verification
- **When confused** - Lost track of what you're doing
- **After errors** - Something went wrong, reassess

## Cross-Agent Handoff

When reviewing another agent's work:

1. **Read their stated intent** - What did they think they were doing?
2. **Compare to original ask** - Did they understand correctly?
3. **Verify their claims** - Did they actually do what they said?
4. **Check for gaps** - What might they have missed?

For domain-specific verification patterns (code, docs, config), see [verification-checklist.md](references/verification-checklist.md).
