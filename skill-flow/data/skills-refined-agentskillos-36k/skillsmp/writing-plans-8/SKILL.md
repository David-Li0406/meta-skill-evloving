---
name: writing-plans
description: Create comprehensive implementation plans with bite-sized tasks. Use after brainstorming produces a design, before touching code. Documents exact files, complete code, commands, expected output.
---

# Writing Plans

## Description
Create comprehensive implementation plans with bite-sized tasks. Assumes the executor has zero codebase context. Documents everything: exact files, complete code, commands, expected output.

## When to Use
- After `/brainstorming` produces a design
- Before touching code
- For any multi-step implementation

## Announcement
Say at start: **"I'm using the writing-plans skill to create the implementation plan."**

## Output Location
Save to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Core Principles

| Principle | Why |
|-----------|-----|
| DRY | Don't repeat yourself |
| YAGNI | Remove unnecessary features |
| TDD | Test-driven development |
| Frequent commits | Small, reversible changes |

## Bite-Sized Task Granularity

**Each step is ONE action (2-5 minutes):**

```
"Write the failing test"        ← step
"Run it to make sure it fails"  ← step
"Implement minimal code"        ← step
"Run tests, verify pass"        ← step
"Commit"                        ← step
```

## Plan Document Structure

### Required Header

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** Use `/executing-plans` to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

### Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

` ` `python
def test_specific_behavior():
    result = function(input)
    assert result == expected
` ` `

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

` ` `python
def function(input):
    return expected
` ` `

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

` ` `bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
` ` `
```

## What to Include

| Include | Example |
|---------|---------|
| Exact file paths | `src/services/notifications.ts:45-67` |
| Complete code | Full function, not "add validation" |
| Exact commands | `npm test -- --grep "notification"` |
| Expected output | "PASS" or "FAIL with 'undefined'" |
| Commit messages | `feat:`, `fix:`, `test:` |

## What NOT to Include

- Vague instructions ("add appropriate error handling")
- Placeholder code ("// implement logic here")
- Assumed knowledge ("use the standard pattern")

## Execution Handoff

After saving the plan, offer:

```
Plan complete and saved to `docs/plans/<filename>.md`.

Two execution options:

1. **This session** — Execute with `/executing-plans`, batch checkpoints

2. **Parallel session** — Open new Claude in worktree, run `/executing-plans`

Which approach?
```

## Example Plan Snippet

```markdown
# User Notifications Implementation Plan

> **For Claude:** Use `/executing-plans` to implement this plan task-by-task.

**Goal:** Add real-time in-app notifications for user events

**Architecture:** Event-driven with NotificationService, in-memory store, React context for UI

**Tech Stack:** TypeScript, React, Zustand

---

### Task 1: NotificationService Interface

**Files:**
- Create: `src/services/notifications/types.ts`
- Test: `src/services/notifications/__tests__/types.test.ts`

**Step 1: Write the type definitions**

` ` `typescript
export type NotificationType = 'info' | 'warning' | 'error' | 'success';

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
  createdAt: Date;
  read: boolean;
}

export interface NotificationService {
  add(notification: Omit<Notification, 'id' | 'createdAt' | 'read'>): Notification;
  markRead(id: string): void;
  getUnread(): Notification[];
}
` ` `

**Step 2: Commit**

` ` `bash
git add src/services/notifications/types.ts
git commit -m "feat(notifications): add type definitions"
` ` `

### Task 2: In-Memory Store Implementation
...
```
