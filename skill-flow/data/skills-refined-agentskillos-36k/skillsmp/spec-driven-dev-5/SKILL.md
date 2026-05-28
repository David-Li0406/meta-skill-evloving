---
name: spec-driven-dev
description: >-
  Spec-driven development framework for ecommerce features. Orchestrates from
  intent to implementation via structured specs and task breakdown.
  Triggers on "/spec.plan", "/spec.refine", "/spec.clarify", "/spec.tasks",
  "/spec.run", "I want to build", "I want to add", "create spec", "feature spec",
  "new feature", "implement feature".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, TodoWrite, Task
---

# ABOUTME: Spec-driven development framework for ecommerce project
# ABOUTME: Manages lifecycle: /spec.plan -> /spec.refine -> /spec.tasks -> /spec.run

# Spec-Driven Development

Iterative feature development ensuring zero ambiguity before execution.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/spec.plan <intent>` | Create spec from feature description |
| `/spec.refine [section]` | Improve spec with research |
| `/spec.clarify <response>` | Answer clarification questions |
| `/spec.tasks` | Break spec into executable tasks |
| `/spec.run [task#]` | Execute tasks with TDD |

---

## Core Principle

**Iterate until clarity**: No task execution begins until ALL questions are resolved. Claude must be able to execute without interruptions.

---

## Phase 1: `/spec.plan` - Create Specification

**Trigger**: `/spec.plan <description>` or "I want to build/add X"

### Workflow

1. **Check `specs/` folder** - create if missing
2. **Generate spec file**: `specs/{feature-slug}.md`
3. **Fill initial sections** from user intent
4. **Generate clarifying questions**
5. **STOP and present questions**

### Output

```
Created: specs/feature-name.md (DRAFT)

Questions requiring clarification:
1. [Question about scope]
2. [Question about behavior]

Use /spec.clarify to answer.
```

---

## Phase 2: `/spec.refine` - Research & Improve

**Trigger**: `/spec.refine [section]`

### Workflow

1. Load active DRAFT spec
2. Search codebase for similar patterns
3. Update Technical Strategy
4. Re-evaluate clarity
5. **If questions remain: STOP and present**

---

## Phase 3: `/spec.clarify` - Answer Questions

**Trigger**: `/spec.clarify <response>`

### Example

```
User: /spec.clarify Q1: OAuth2 with Google only. Q2: Admin can also delete.

Updated specs/auth-system.md:
- Added OAuth2/Google to Technical Strategy
- Updated permissions

Remaining questions: None
Spec ready. Use /spec.tasks
```

---

## Phase 4: `/spec.tasks` - Task Breakdown

**Trigger**: `/spec.tasks`

### Prerequisites

- Active spec must be DRAFT or APPROVED
- "Open Questions" section must be empty
- If questions exist: **STOP → /spec.clarify**

### Task Granularity

Tasks should be **high-level logical units**:
- "Implement authentication middleware"
- "Create user model and repository"
- "Add API endpoints for user CRUD"

TDD cycle happens WITHIN each task during `/spec.run`.

---

## Phase 5: `/spec.run` - Execute Tasks

**Trigger**: `/spec.run [task#]`

### Prerequisites

- Task file must exist: `specs/{feature}.tasks.md`
- If no task file: **STOP → /spec.tasks**

### Execution Rules

- **TDD for each task**: Red → Green → Refactor → Commit
- **Invoke language skills**: `/typescript` for .ts files
- **Respect hooks**: Pre-commit must pass
- **Mark completed** in task file

---

## File Structure

```
specs/
├── README.md                   # Project config
├── user-wishlist.md            # Spec (APPROVED)
├── user-wishlist.tasks.md      # Task breakdown
├── payment-stripe.md           # Spec (DRAFT)
└── ...
```

---

## Spec Status Flow

```
DRAFT -> APPROVED -> IN_PROGRESS -> COMPLETED
          |              |
          v              v
      (questions?)   (blocked?)
          |              |
          v              v
        DRAFT      IN_PROGRESS
```

---

## Ecommerce-Specific Scopes

When creating specs, consider these modules:

| Module | Files | Considerations |
|--------|-------|----------------|
| Auth | `apps/backend/src/modules/auth/` | JWT, sessions, rate limits |
| Catalog | `apps/backend/src/modules/catalog/` | Redis caching |
| Cart | Frontend hooks + Backend | Session persistence |
| Orders | `apps/backend/src/modules/orders/` | Transactions |
| Checkout | `apps/frontend/src/app/checkout/` | Payment flow |

---

## Templates

See `references/templates.md` for:
- Spec file template
- Task file template
- specs/README.md template

---

## Session Resume

On context compaction:

1. Check `specs/` for files with status `IN_PROGRESS`
2. Check `.tasks.md` files for unchecked items
3. Report: "Found in-progress spec: X with Y tasks remaining"
4. Ask: "Continue with /spec.run?"
