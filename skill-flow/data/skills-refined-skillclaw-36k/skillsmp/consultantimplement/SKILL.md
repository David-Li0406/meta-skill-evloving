---
name: consultant:implement
description: "Implement a story following subtasks exactly. Alex writes clean code, tests first, small commits. The story file is the contract."
invocation: user
---

# Implement Story

Implement a developer-ready story following the subtasks exactly as specified.

## Prerequisites

- Story file exists in `_consultant/stories/STORY-XXX.md`
- Story status is "ready-for-dev"
- Technical context is available in project-context.md

## Process

### 1. Load Story
```bash
Read _consultant/stories/STORY-{XXX}.md
```
Understand ALL requirements before coding.

### 2. Update Status
```yaml
# sprint-status.yaml
stories:
  - id: STORY-XXX
    status: in_progress  # Changed from ready-for-dev
```

### 3. Implement Each Subtask

For each TASK in the story:

```
a. Check existing patterns in codebase
b. Write failing test (if TDD)
c. Implement the change
d. Make test pass
e. Commit:
   feat(scope): description [STORY-XXX]

   Co-Authored-By: Claude <noreply@anthropic.com>
f. Check off subtask in story file
```

### 4. Update Dev Notes

Add implementation details to story:
```markdown
## Dev Notes
- Implemented using {pattern}
- Created files: {list}
- Modified files: {list}
- Notes: {anything_important}
```

### 5. Run All Tests
```bash
npm test  # All must pass
```

### 6. Complete Story
```yaml
# sprint-status.yaml
stories:
  - id: STORY-XXX
    status: done
```

## Commit Convention

```
type(scope): description [STORY-XXX]

- Detail 1
- Detail 2

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: feat, fix, refactor, test, docs, chore

## Checkpoints

STOP and request approval for:
- Security-related code
- Database schema changes
- External API integrations
- Payment processing

## Agent

This skill uses the `consultant-developer` subagent.
