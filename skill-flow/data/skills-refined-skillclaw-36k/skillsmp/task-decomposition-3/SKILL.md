---
name: task-decomposition
description: Hybrid task decomposition strategy for teamwork projects. Covers plan-based and semantic decomposition, granularity rules, role assignment, and complexity assessment.
---

# Task Decomposition Strategy

This skill provides comprehensive guidelines for breaking down project goals into actionable tasks. Use this when planning teamwork projects to ensure optimal task granularity, proper role assignment, and appropriate complexity assessment.

---

## Hybrid Decomposition Strategy

Use a combination of plan-based (Strategy A) and semantic (Strategy B) decomposition:

### Strategy A: Plan Document Based

Use when `plans` option is provided with detailed implementation documents.

1. **Extract Steps**: Parse plan documents for Markdown headers (## Step N, ### Phase N)
2. **Map to Tasks**: Each header section becomes a task candidate
3. **Sub-decompose**: If a step mentions multiple files (>3), split into sub-tasks
4. **Verify Atomicity**: Each task should be completable in one worker session

Example transformation:
```
Plan: "03.impl-workspace-setup.md"
├─ Step 1: Root workspace → Task: "Initialize pnpm monorepo workspace"
├─ Step 2.1: Database package → Task: "Create database package structure"
├─ Step 2.2: items schema → Task: "Implement items.schema.ts"
├─ Step 2.3: item-features schema → Task: "Implement item-features.schema.ts with pgvector"
└─ Step 3: Docker → Task: "Configure Docker Compose for dev environment"
```

### Strategy B: Semantic Decomposition

Use when no plan documents provided, or as sub-decomposition within Strategy A.

1. **File-based**: New file creation = separate task
2. **Complexity-based**: Complex file with multiple classes → split by class
3. **Dependency-based**: Interface and implementation = separate tasks
4. **Test-based**: Each independently testable unit = candidate task

---

## Granularity Rules

- 1 task = 1-3 files changed (recommended)
- 1 task = 10-30 minutes work (recommended)
- 1 task = independently testable/verifiable

### Anti-patterns (Avoid)

- ❌ "Setup entire workspace" (too broad)
- ❌ "Implement backend" (too vague)
- ❌ "Create all schemas" (bundles multiple files)

### Good patterns (Recommended)

- ✅ "Create items.schema.ts with Item table"
- ✅ "Add SearchUseCase with keyword search"
- ✅ "Configure Docker Compose for PostgreSQL"

---

## Role Assignment

Assign each task to the appropriate role based on its primary focus:

| Role       | When to Use                                |
| ---------- | ------------------------------------------ |
| `frontend` | UI, components, styling, user interactions |
| `backend`  | API, services, database, business logic    |
| `test`     | Tests, fixtures, mocks                     |
| `devops`   | CI/CD, deployment, infrastructure          |
| `docs`     | Documentation, README, examples            |
| `security` | Auth, permissions, input validation        |
| `review`   | Code review, refactoring                   |
| `general`  | Miscellaneous, cross-cutting               |

---

## Complexity Assessment

Workers use different models based on task complexity. Assign complexity to optimize resource usage:

| Complexity | Model | Criteria | Examples |
| ---------- | ----- | -------- | -------- |
| `simple`   | haiku | Single file, <10 lines, minor changes | Config updates, typo fixes, simple docs |
| `standard` | sonnet | 1-3 files, typical CRUD, straightforward | API endpoints, UI components, tests |
| `complex`  | opus | 5+ files, architecture, security-critical | Auth systems, DB migrations, major refactors |

### Guidelines for Complexity Assessment

- **simple**: Task is obvious, minimal thinking required, low risk
- **standard**: Task requires moderate planning, some decision-making
- **complex**: Task requires deep analysis, multiple considerations, high impact

### Decision Rules

**Default to `standard`** when uncertain. Upgrade to `complex` if:
- Task involves authentication/authorization
- Task touches database schema
- Task spans 5+ files
- Task has architectural implications
- Task is security-sensitive

---

## Best Practices

1. **Be specific** - Vague tasks get vague results
2. **Include context** - Description should be self-contained
3. **Maximize parallelism** - Minimize unnecessary dependencies
4. **Granular tasks** - Prefer more smaller tasks over fewer large ones
5. **Clear acceptance criteria** - Workers need to know when task is complete
