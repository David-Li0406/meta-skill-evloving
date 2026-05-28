---
name: task-discipline
description: TODO list discipline for task tracking. Activates for multi-step tasks (3+), complex work, or when systematic organization is needed. Use for tracking progress and ensuring completeness.
allowed-tools: ["update_plan"]
metadata:
  short-description: Rigorous task tracking discipline
---

# Task Discipline

**Read these references:**
- `references/task-management.md` - Complete TODO discipline (detailed)
- `~/.config/agent/core/methodology.md` - Problem-solving framework integration

## Instructions

Apply rigorous task tracking discipline per AGENT.md and references:

### When Required

Create TODO lists for:
- Tasks with 3+ steps
- Complex multi-file work
- Non-trivial implementation
- Any work benefiting from systematic tracking

### The Golden Rule

**Exactly ONE task `in_progress` at any given moment**
- ✗ Never ZERO in_progress (if work is happening)
- ✗ Never TWO OR MORE in_progress
- ✓ Always exactly ONE in_progress

This forces focus and prevents context-switching.

### Status Flow

```
pending → in_progress → completed
```

- **pending**: Not yet started
- **in_progress**: Currently working on (exactly ONE)
- **completed**: Finished successfully

### No Batching

Mark tasks as completed **immediately** after finishing.
- ✗ Bad: Complete multiple tasks, then update all at once
- ✓ Good: Finish task → mark completed → start next task

### When Blocked

If a task can't proceed:
1. Move it back to `pending`
2. Create new task describing the blocker
3. Mark blocker task as `in_progress`
4. Resolve blocker first

### Task Forms

Each task needs two forms:
- **content**: Imperative (e.g., "Run tests", "Fix bug in parser")
- **activeForm**: Present continuous (e.g., "Running tests", "Fixing bug in parser")

The activeForm shows what you're currently doing.

### Integration with Problem-Solving

Use TODO lists during Phase 2 (Plan) to break down work, then track progress during Phase 3 (Execute).
