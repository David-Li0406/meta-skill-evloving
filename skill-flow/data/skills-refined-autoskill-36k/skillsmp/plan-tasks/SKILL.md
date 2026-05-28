---
name: plan-tasks
description: Creates granular implementation tasks from PRD documents. Use when user wants to plan work, create tasks from a PRD, implement a feature spec, or break down requirements into actionable steps. Triggers on phrases like "plan tasks", "create tasks from PRD", "implement PRD", "break down the spec", or when user wants to start working on a PRD document.
---

# Plan Tasks from PRD

Create implementation tasks from PRD documents.

## Workflow

### 1. List available PRDs

```bash
~/.claude/skills/plan-tasks/scripts/list-prds.sh
```

Or manually:
```bash
ls -1 .local/prds/wip/ 2>/dev/null || ls -1 .local/prds/backlog/ 2>/dev/null
```

If no PRDs found, inform user and stop.

### 2. Select PRD

Use `AskUserQuestion` with available PRD files as options.

### 3. Analyze PRD

Read the full PRD. Extract:
- Capabilities and features
- Module structure
- Dependency graph
- Implementation phases

### 4. Create tasks

Use `TaskCreate` for each task. Follow these rules:

**Task qualities**:
- **Atomic**: Single focused change
- **Self-contained**: All context in description
- **Sequenced**: Dependencies explicit
- **Unambiguous**: No decisions left to implementer

**Task description format**:
```
{What to do}

Location: {file paths or how to find them}

Details:
- {specific requirement 1}
- {specific requirement 2}

Verify: {how to confirm it's done}
```

### 5. Set dependencies

Use `TaskUpdate` with `addBlockedBy` to link dependent tasks.

Follow PRD's dependency graph:
- Phase 0 tasks: no blockers
- Phase 1 tasks: blocked by Phase 0
- etc.

### 6. Report summary

Output:
- Total tasks created
- Execution order (phases)
- Any PRD ambiguities needing clarification

## Granularity Guide

| Too coarse | Properly granular |
|------------|-------------------|
| "Add user authentication" | "Create User model with email, passwordHash in src/models/" |
| "Build the API" | "Add POST /users endpoint accepting {email, password}, return 201" |
| "Handle errors" | "Add try/catch in UserService.create(), throw ServiceError on failure" |

See `references/task-examples.md` for more examples.

## Reference Files

- `references/task-examples.md` - Good vs bad task examples
