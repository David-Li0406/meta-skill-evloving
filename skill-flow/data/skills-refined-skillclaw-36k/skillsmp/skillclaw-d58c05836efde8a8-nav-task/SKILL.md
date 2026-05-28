---
name: nav-task
description: Use this skill when you need to manage Navigator task documentation, including creating implementation plans, archiving completed tasks, and updating the task index.
---

# Navigator Task Manager Skill

Create and manage task documentation - implementation plans that capture what was built, how, and why.

## When to Invoke

Invoke this skill when the user:
- Says "document this feature", "archive this task"
- Says "create task doc for...", "document what I built"
- Completes a feature and mentions "done", "finished", "complete"
- Starts a new feature and says "create implementation plan"

**DO NOT invoke** if:
- User is asking about existing tasks (use Read, not creation)
- Creating SOPs (that's a different skill)
- Updating system docs (different skill)

## Execution Steps

### Step 1: Determine Task ID

**If user provided task ID** (e.g., "TASK-01", "GH-123"):
- Use their ID directly

**If no ID provided**:
- Read `.agent/.nav-config.json` for `task_prefix`
- Check existing tasks: `ls .agent/tasks/*.md`
- Generate next number: `{prefix}-{next-number}`
- Example: Last task is TASK-05, create TASK-06

### Step 2: Determine Action (Create vs Archive)

**Creating new task** (starting feature):
```
User: "Create task doc for OAuth implementation"
→ Action: CREATE
→ Generate empty implementation plan template
```

**Archiving completed task** (feature done):
```
User: "Document this OAuth feature I just built"
→ Action: ARCHIVE
→ Generate implementation plan from conversation
```

### Step 3: Create New Task (If Starting Feature)

Generate task document from template:

```markdown
# TASK-{XX}: {Feature Name}

**Status**: 🚧 In Progress
**Created**: {YYYY-MM-DD}
**Assignee**: {from PM tool or "Manual"}

---

## Context

**Problem**:
[What problem does this solve?]

**Goal**:
[What are we building?]

**Success Criteria**:
- [ ] [Specific measurable outcome]
- [ ] [Another outcome]

---

## Implementation Plan

### Phase 1: {Name}
**Goal**: [What this phase accomplishes]

**Tasks**:
- [ ] [Specific task]
- [ ] [Another task]

**Files**:
- `path/to/file.ts` - [Purpose]

### Phase 2: {Name}
...

---

## Technical Decisions

| Decision | Options Considered | Chosen | Reasoning |
|----------|-------------------|--------|-----------|
| [What] | [Option A, B, C] | [Chosen] | [Why] |

---

## Dependencies

**Requires**:
- [ ] {prerequisite task or setup}

**Blocks**:
- [ ] {task that is blocked}
```