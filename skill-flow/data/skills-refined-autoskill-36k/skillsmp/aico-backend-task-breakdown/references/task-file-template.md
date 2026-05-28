# Task File Template

This template defines the structure for backend task breakdown files.

## Story-based Task File

**Filename**: `story-{story-name}.md`

**Location**: `docs/reference/backend/tasks/`

```markdown
# Story Tasks: [Story Name]

> **Story**: docs/reference/pm/stories/{story-id}.md
> **Design**: docs/reference/backend/designs/{design-name}.md (if applicable)
> **Role**: backend
> **Created**: YYYY-MM-DD
> **Updated**: YYYY-MM-DD

---

## Task 1: [Task Name]

> **Status**: pending | in_progress | completed
> **Type**: setup | feature | improvement
> **Depends on**: -
> **Estimated**: 1-2h (optional)

### Description

[Clear description of what this task achieves]

### Context

- Part of [Story Name] story
- First task - sets up foundation
- Should follow design system tokens

### Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Scope

**Files to create/modify:**

- Create: `src/components/...`
- Modify: `src/pages/...`

**Key components:**

- Component A
- Component B

### Implementation Steps

> Note: Detailed steps can be added using `/backend.plan` command

1. [Brief step description]
2. [Brief step description]
3. [Brief step description]

### Notes

[Any additional notes, considerations, or technical decisions]

---

## Task 2: [Task Name]

> **Status**: pending
> **Type**: feature
> **Depends on**: Task 1

### Description

[Clear description of what this task achieves]

### Context

- Part of [Story Name] story
- Depends on: Task 1 (setup must be complete)
- Implements [specific feature/component]

### Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

### Scope

**Files to create/modify:**

- Create: `src/components/...`

### Implementation Steps

> Note: Add detailed steps using `/backend.plan story-{name}` and specify task number

1. [Brief step description]

### Notes

[Any notes]

---

## Task 3: Add Tests

> **Status**: pending
> **Type**: testing
> **Depends on**: Task 2

### Description

Add comprehensive unit and integration tests for all implemented features.

### Acceptance Criteria

- [ ] Unit tests for all components
- [ ] Integration tests for user flows
- [ ] All tests passing

### Scope

**Files to create:**

- `src/components/__tests__/...`

### Implementation Steps

1. Write unit tests
2. Write integration tests
3. Verify all tests pass

---

## Progress

- Total tasks: 3
- Completed: 0
- In progress: 0
- Pending: 3

**Next task**: Task 1: [Task Name]
```

## Standalone Task File

**Filename**: `standalone-{requirement-name}.md`

**Location**: `docs/reference/backend/tasks/`

**Structure**: Same as story-based task file, just replace:

- Header: `# Standalone Tasks: [Requirement Name]`
- Remove `> **Story**: ...` line (no story reference)
- Otherwise identical structure

## Task Types

| Type        | Examples                                |
| ----------- | --------------------------------------- |
| Setup       | Create component structure, setup state |
| UI          | Implement section/component layout      |
| Logic       | Add form validation, API integration    |
| Interaction | Implement hover, click, animations      |
| Testing     | Unit tests, integration tests           |

## Ordering Rules

1. **Setup tasks first** - Component structure, routing
2. **Static UI before dynamic** - Layout before logic
3. **Core functionality before edge cases** - Happy path first
4. **Tests after implementation** - Each feature gets tests
