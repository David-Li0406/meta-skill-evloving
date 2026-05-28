---
name: completing-task
description: Use after completing and verifying a task. Checks git branch (feature → suggests finishing-a-development-branch), closes task, recursively checks parents with confirmation, runs bd sync. Handles task completion workflow for beads.
---

# Flow: Done

## Overview

**Core principle:** Ask before cascading.

This skill handles task completion: close task, check parents recursively, sync. Always asks before closing parent tasks - even when "obviously" all children are closed.

## Quick Reference

| Step | Action | Key Point |
|------|--------|-----------|
| 1. **Branch Check** | Validate git branch | Feature → stop, suggest workflow |
| 2. Find Task | Get in_progress leaf | Ask if multiple |
| 3. Close | `bd close {task-id}` | Use bd, not SQL |
| 4. **Check Parent** | Recursive parent check | With confirmation |
| 5. **Ask** | Before closing parent | Even if "obvious" |
| 6. **Sync** | `bd sync` | Always, at end |

**Key behavior:** Always ask before closing parents. Always run bd sync.

## Workflow

Follow these steps **in order**. Do not skip steps.

### 1. Check Git Branch (MANDATORY FIRST STEP)

```bash
git branch --show-current
```

**If feature branch detected** (`feature/*`, `fix/*`, or any non-generic):

**STOP** and inform user:

> "You're on feature branch `{branch-name}`.
>
> Use `superpowers:finishing-a-development-branch` to properly complete this work (handles merge/PR/cleanup and task closure together).
>
> Do NOT proceed with flow:done on feature branches."

Then exit. Do not continue workflow.

**If generic branch** (main, master, develop, trunk):
Continue to step 2.

### 2. Find In-Progress Leaf Task

```bash
bd list --status=in_progress
```

Filter for leaf tasks (no open children).

**If multiple found:** Ask which task is complete.
**If none found:** Inform "No in_progress leaf tasks. Check with `bd list --status=in_progress`"

### 3. Close Task

```bash
bd close {task-id}
```

**Use bd close.** Do NOT use direct SQL.

Confirm task closed.

### 4. Check Parent Recursively (with Confirmation)

After closing task, check if it has a parent:

```bash
bd show {task-id}
```

Look for parent relationship.

**If task has parent:**

```bash
bd show {parent-id}
```

Count open children.

**If parent has NO open children** (all closed):

**Ask user:**

> "Parent task `{parent-id}` now has all children closed.
>
> Close it too? (yes/no)"

**If user says yes:**
- Close parent with `bd close {parent-id}`
- Set current task to parent
- Repeat step 4 (recurse up)

**If user says no:**
- Stop recursion
- Proceed to step 6

**If parent has open children:**
- Stop recursion (parent cannot be closed yet)
- Proceed to step 6

**If task has no parent:**
- Proceed to step 6

### 5. Repeat Recursion

Continue checking grandparents, great-grandparents, etc. until:
- User says "no" to closing a parent, OR
- Parent has open children, OR
- No more parents exist

**Always ask at each level.** Do NOT auto-close parents.

### 6. Run bd sync (MANDATORY)

```bash
bd sync
```

Always run at end, regardless of how many tasks closed.

Confirm sync completed.

## Scope Boundaries

### This Skill DOES:
✅ Check git branch
✅ Find in_progress leaf task
✅ Close task with bd close
✅ Check parents recursively
✅ Ask before closing each parent
✅ Run bd sync at end

### This Skill Does NOT:
❌ Git operations (commit, push, merge, etc.)
❌ Create/switch branches
❌ Start next task (use flow:start)
❌ Update PRs or issues
❌ Run tests or builds
❌ Auto-close parents without asking
❌ Proceed on feature branches

**Scope note:** On feature branches, this skill STOPS and refers to finishing-a-development-branch.

## Red Flags - STOP

If you're thinking any of these, STOP and follow the workflow:

- "All children closed → close parent"
- "Branch check unnecessary"
- "bd sync is obvious (skip it)"
- "Use SQL for efficiency"
- "Parent obviously should close"
- "Being helpful by auto-closing cascade"
- "Feature branch doesn't matter"

**All of these mean: Follow workflow. Check branch. Ask before closing parents. Run bd sync.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "All children closed → close parent" | Ask first. User might add more children or want to review. |
| "Branch check unnecessary" | Feature branch needs different workflow. Always check. |
| "bd sync is obvious" | Obvious steps get skipped. Make it explicit. |
| "Use SQL for efficiency" | bd close has logging, events, validation. Use it. |
| "Parent obviously should close" | Obvious to you ≠ user wants it. Ask. |
| "Being helpful by auto-closing" | Asking IS being helpful. Assuming isn't. |
| "Feature branch doesn't matter" | Feature branches need PR workflow. Always check. |

## Examples

### ❌ BAD: Auto-close parent

```
User: "Task done, flow:done"
Agent: [Closes task]
       [Checks parent, sees all children closed]
       [Automatically closes parent without asking]
       Done!
```

**Problems:**
- Didn't check branch
- Auto-closed parent without asking
- Didn't run bd sync

### ✅ GOOD: Ask before closing parent

```
User: "Task done, flow:done"
Agent: [Checks branch: master, OK to proceed]
       [Closes task claude-tools-abc.3]

       Parent task claude-tools-abc now has all children closed.

       Close it too? (yes/no)

User: yes
Agent: [Closes parent]
       [Runs bd sync]

       ✓ Closed claude-tools-abc.3
       ✓ Closed claude-tools-abc (parent)
       ✓ Synced with remote

       Done.
```

**Correct because:**
- Checked branch first
- Asked before closing parent
- Ran bd sync
- Clear confirmation

### ❌ BAD: Feature branch proceed

```
User: "Done with this feature, flow:done"
Agent: [On feature/add-auth branch]
       [Closes task anyway]
```

**Problem:** Proceeded on feature branch without checking.

### ✅ GOOD: Feature branch handling

```
User: "Done with this feature, flow:done"
Agent: [Checks branch: feature/add-auth]

       You're on feature branch `feature/add-auth`.

       Use `superpowers:finishing-a-development-branch` to properly
       complete this work (handles merge/PR/cleanup and task closure together).

       Do NOT proceed with flow:done on feature branches.
```

**Correct because:**
- Checked branch
- Stopped when detected feature branch
- Suggested correct workflow
- Did not close task

### ❌ BAD: Skip bd sync

```
User: "flow:done"
Agent: [Closes task]
       [Asks about parent, closes]
       Done!
```

**Problem:** Skipped bd sync at end.

### ✅ GOOD: Always bd sync

```
User: "flow:done"
Agent: [Checks branch]
       [Closes task]
       [Asks about parent, closes if yes]
       [Runs bd sync]

       ✓ Synced with remote

       Done.
```

**Correct because:**
- bd sync always run at end
- Explicit confirmation

## Edge Cases

### Multiple In-Progress Tasks

```
Found 2 in_progress leaf tasks:
1. claude-tools-abc: Feature X
2. claude-tools-def: Feature Y

Which task is complete? (enter 1 or 2, or task ID)
```

### No In-Progress Tasks

```
No in_progress leaf tasks found.

Check task status with:
  bd list --status=in_progress
```

### Deep Hierarchy (3 levels)

```
Closed claude-tools-abc.2.1

Parent claude-tools-abc.2 now has all children closed.
Close it too? (yes/no)

[User: yes]

Closed claude-tools-abc.2

Parent claude-tools-abc now has all children closed.
Close it too? (yes/no)

[User: yes]

Closed claude-tools-abc

No more parents. Running bd sync...
```

### Parent Has Open Sibling

```
Closed claude-tools-abc.1

Parent claude-tools-abc still has open children:
- claude-tools-abc.2 (open)

Not asking to close parent (has open children).

Running bd sync...
```

## The Bottom Line

Always follow the workflow.

**Check branch FIRST.** Feature branch → stop, suggest finishing-a-development-branch.

**Ask before closing parents.** Even when "obviously" all children closed.

**Run bd sync ALWAYS.** At end, no exceptions.

Obvious logic requires MORE structure, not less.
