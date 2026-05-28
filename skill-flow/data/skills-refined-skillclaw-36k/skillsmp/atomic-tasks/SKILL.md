---
name: atomic-tasks
description: Task structure and atomic commit patterns for granular, verifiable work units
triggers:
  - atomic task
  - task structure
  - task planning
  - commit strategy
  - work breakdown
---

# Atomic Tasks Skill

This skill provides patterns for creating well-structured, atomic tasks that follow the principle: **One task = One commit = One thing**.

## Core Principles

### Atomicity
Each task should be:
- **Self-contained**: Completes a single logical unit of work
- **Independently verifiable**: Can be tested/verified in isolation
- **Safely committable**: Results in a working codebase if committed alone
- **Rollback-friendly**: Can be reverted without breaking other tasks

### Task Properties

| Property | Purpose | Required |
|----------|---------|----------|
| `id` | Unique identifier (TASK-XXX) | Yes |
| `status` | Current state (pending/in_progress/completed/blocked) | Yes |
| `name` | Short descriptive name | Yes |
| `description` | What this task accomplishes | Yes |
| `depends` | Task IDs this depends on | No |
| `files` | Files to create/modify | Yes |
| `actions` | Specific steps to take | Yes |
| `verify` | How to verify completion | Yes |
| `done` | Completion criteria | Yes |
| `commit` | Conventional commit message | Yes |

## Task Sizing Guidelines

### Too Large (Split It)
- Touches more than 5 files
- Has more than 5 actions
- Takes more than 30 minutes
- Multiple logical concerns mixed together
- Commit message needs "and" multiple times

### Too Small (Combine It)
- Only renames a variable
- Single-line change with no logic
- Cannot be meaningfully verified
- Would create noise in git history

### Just Right
- 1-3 files modified typically
- 2-5 clear actions
- Single responsibility
- Clear verification steps
- Concise commit message

## Task Status Flow

```
pending ─── in_progress ─── completed
    │            │
    │            └── blocked (external dependency)
    │
    └── skipped (no longer needed)
```

## Dependency Management

### Dependency Types
1. **Code Dependency**: Task B needs code from Task A
2. **Schema Dependency**: Task B needs database changes from Task A
3. **Config Dependency**: Task B needs configuration from Task A
4. **Knowledge Dependency**: Task B needs information gathered in Task A

### Dependency Rules
- No circular dependencies allowed
- Minimize dependency chains (prefer parallelizable tasks)
- Document why dependency exists
- Re-evaluate if blocked task is taking too long

## Verification Patterns

### Automated Verification
```xml
<verify>
  <step>npm test -- [test-pattern]</step>
  <step>npm run build</step>
  <step>npm run lint -- [file]</step>
</verify>
```

### Manual Verification
```xml
<verify>
  <step>Visually confirm [UI element] appears</step>
  <step>Manual test: [test scenario]</step>
</verify>
```

### Combined Verification
```xml
<verify>
  <step>npm test -- auth</step>
  <step>Manual: Login with test credentials</step>
  <step>Check logs for errors</step>
</verify>
```

## Done Criteria Patterns

### Feature Tasks
```xml
<done>
  <criterion>Feature is accessible via [entry point]</criterion>
  <criterion>Tests cover happy path and error cases</criterion>
  <criterion>No new lint warnings introduced</criterion>
</done>
```

### Bug Fix Tasks
```xml
<done>
  <criterion>Original issue no longer reproduces</criterion>
  <criterion>Regression test added</criterion>
  <criterion>Related functionality still works</criterion>
</done>
```

### Refactor Tasks
```xml
<done>
  <criterion>All existing tests still pass</criterion>
  <criterion>No functional changes detected</criterion>
  <criterion>[Quality metric] improved</criterion>
</done>
```

## Commit Message Convention

Follow Conventional Commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring |
| `test` | Adding/updating tests |
| `docs` | Documentation only |
| `chore` | Maintenance tasks |
| `style` | Formatting changes |
| `perf` | Performance improvements |

### Examples
```
feat(auth): add login endpoint
fix(cart): prevent negative quantities
refactor(api): extract validation middleware
test(user): add registration edge cases
```

## Task Decomposition Process

1. **Start with the goal**: What is the end result?
2. **Identify major components**: What distinct pieces are needed?
3. **Check for dependencies**: What order must they happen in?
4. **Size each component**: Is each one atomic?
5. **Split if needed**: Break large components down
6. **Define verification**: How will we know each is done?
7. **Write commit messages**: Force clarity of purpose

## Anti-Patterns to Avoid

### The Kitchen Sink
```xml
<!-- BAD: Too many unrelated changes -->
<task id="TASK-001">
  <name>Add auth and update styling and fix bugs</name>
  ...
</task>
```

### The Invisible Task
```xml
<!-- BAD: No way to verify -->
<task id="TASK-001">
  <name>Improve code quality</name>
  <verify></verify>
</task>
```

### The Dependency Chain
```
<!-- BAD: Long sequential chain -->
TASK-001 → TASK-002 → TASK-003 → TASK-004 → TASK-005
```

### The Vague Action
```xml
<!-- BAD: Not actionable -->
<actions>
  <action>Make it better</action>
  <action>Fix the thing</action>
</actions>
```

## Integration with Workflow

### PLAN Phase
- Create all tasks using XML format
- Verify cross-plan consistency
- Establish execution order

### EXECUTE Phase
- Process one task at a time
- Mark status transitions
- Run verification after each
- Commit on success

### VERIFY Phase
- Review all completed tasks
- Run integration verification
- Confirm done criteria met

See `xml-format.md` for complete XML schema reference.
