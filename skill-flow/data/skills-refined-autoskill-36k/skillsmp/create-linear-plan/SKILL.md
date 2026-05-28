---
name: create-linear-plan
description: "Create Linear Issues from requirements using the plan process. Same process as /plan but outputs to Linear Issues instead of file. Triggers - linear plan, plan to linear, create issues from plan."
---

# Create Linear Plan

**Iron Law:** Same process as `/plan`, different output target. Writing-Plans Process → Linear Issues.

## Overview

This skill runs the **plan** process and outputs the result to **Linear Issues** instead of a file.

```
/plan [feature]           → plan → docs/plans/*.md
/create-linear-plan       → plan → Linear Issues (phases + tasks)
```

**Both use the same process. Only the output differs.**

## No Code Policy

> **Plans must be plain prose.** No code blocks, no implementation snippets. Describe tasks in clear written English.

---

## The Workflow

### Step 1: Run Writing-Plans Process

**This is identical to `/plan`:**

```
1. CLARIFY   → Understand what we're building
2. RESEARCH  → Understand the existing codebase
3. DESIGN    → Structure the approach into phases
4. DOCUMENT  → Write tasks with verification
5. VALIDATE  → Review with user before creating
```

### Step 2: Clarify - Understand What We're Building

```markdown
## Goal Clarification

**What**: [One sentence - what we're building]
**Why**: [Business/user value]
**Success Criteria**:
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (observable)

**Scope**:
- IN: [What's included]
- OUT: [What's explicitly excluded]

**Constraints**:
- Technical: [Stack, performance]
- Dependencies: [What must exist first]
```

### Step 3: Research - Understand the Codebase

```markdown
## Codebase Research

**Relevant Files**:
- `src/path/to/related.ts` - Does X, we'll extend it
- `tests/path/to/tests.ts` - Existing test patterns

**Existing Patterns**:
- Authentication: Uses JWT middleware
- Error handling: Custom ApiError class

**Gotchas Found**:
- Must use specific error format
- Tests require mock database
```

### Step 4: Design - Structure into Phases

Break down into phases and tasks:

```markdown
## Design Overview

**Architecture**: [2-3 sentences on approach]

**Phases**:
1. Foundation - Setup and scaffolding
2. Core - Main implementation
3. Integration - Connect components
4. Testing - Verification

**Risk Areas**:
- [Area 1] - Mitigation: [strategy]
```

### Step 5: Document Tasks

Each task should be ONE action (2-5 minutes max):

**Good:**
- "Write failing test for X"
- "Implement minimal code to pass"
- "Run test to verify"

**Bad:**
- "Implement the feature" (too vague)
- "Add tests and implementation" (multiple actions)

### Step 6: Validate Before Creating

Show the user the complete plan for approval:

```markdown
## Proposed Linear Issues

**Project:** [Project Name]
**Phases:** 4
**Tasks:** 12

### Phase 1: Foundation
- Task 1.1: [Description]
- Task 1.2: [Description]
**Checkpoint:** [How to verify phase complete]

### Phase 2: Core
- Task 2.1: [Description]
...

Create these Linear Issues? I can adjust before creating.
```

### Step 7: Select Project & Create Issues

List available projects:
```typescript
mcp__linear-server__list_projects({ state: "started", limit: 50 })
```

**Create phase as parent issue:**
```typescript
const phaseIssue = await mcp__linear-server__create_issue({
  title: "[Phase 1] Foundation",
  description: "## Objective\n[Phase objective]\n\n## Checkpoint\n[Verification]",
  team: "Engineering",
  project: "project-uuid",
  labels: ["phase"]
});
// Returns: { id: "phase-uuid", identifier: "PEA-100" }
```

**Create tasks as sub-issues using `parentId`:**
```typescript
await mcp__linear-server__create_issue({
  title: "Write failing test for user model",
  description: "## Action\n[Task details]\n\n## Verify\n[How to verify]",
  team: "Engineering",
  parentId: "phase-uuid",  // ← THIS creates parent-child!
  labels: ["task"]
});
```

**DO NOT use `relatedTo`** - that creates "related" links, not parent-child.

### Step 8: Confirm Creation

```markdown
## Linear Plan Created

**Project:** [Project Name]
**Team:** [Team Name]

| Phase | ID | Tasks |
|-------|-----|-------|
| [Phase 1] Foundation | PEA-101 | 3 sub-issues |
| [Phase 2] Core | PEA-105 | 4 sub-issues |
| [Phase 3] Integration | PEA-110 | 3 sub-issues |
| [Phase 4] Testing | PEA-114 | 2 sub-issues |

**Total:** 4 phases, 12 tasks

**View in Linear:** https://linear.app/[workspace]/project/[slug]

**Next Steps:**
- Execute: `/execute`
- Or work issues directly in Linear
```

---

## Linear Hierarchy

```
Project (from /create-linear-spec)
├── Issue [Phase 1] ← Parent issue
│   ├── Sub-Issue [Task 1.1] ← Uses parentId
│   └── Sub-Issue [Task 1.2]
├── Issue [Phase 2]
│   └── Sub-Issue [Task 2.1]
└── Issue [Phase 3: Verification]
    └── Sub-Issue [Test coverage]
```

---

## Phase Issue Template

```markdown
**Title:** [Phase N] {Phase Name}
**Labels:** phase
**Project:** {Project ID}

## Objective
{What this phase accomplishes}

## Tasks
{List of tasks - created as sub-issues}

## Dependencies
{What must be complete before this phase}

## Checkpoint
{Verification step - how to know phase is complete}
```

## Task Issue Template

```markdown
**Title:** {Task description - action verb + object}
**Labels:** task
**Parent:** {Phase Issue UUID}

## Action
{Specific task to complete - one action only}

## Files
{Exact file paths to create/modify}

## Verify
{Command and expected output}
```

---

## Example

**User says:** `/create-linear-plan user authentication`

**Steps 1-5 - Writing-Plans Process:**

```
Clarify:
- What: User authentication with email/password
- Why: Enable personalized experience
- Success: Users can register, login, logout

Research:
- Found: JWT middleware exists
- Pattern: bcrypt for passwords
- Gotcha: Must use ApiError class

Design:
- Phase 1: Database schema (User model)
- Phase 2: Auth endpoints (register, login, logout)
- Phase 3: Middleware (JWT verification)
- Phase 4: Testing (unit + integration)
```

**Step 6 - Validate:**

```markdown
## Proposed Linear Issues

**Project:** User Authentication
**Phases:** 4
**Tasks:** 10

### Phase 1: Database Schema
- Write failing test for User model
- Create User model in Prisma
- Run migration
**Checkpoint:** `npm test` passes for User model

Create these Linear Issues?
```

**Step 7 - Create:**

```typescript
// Phase 1
const phase1 = await create_issue({
  title: "[Phase 1] Database Schema",
  team: "Engineering",
  project: "auth-uuid",
  labels: ["phase"],
  description: "## Objective\nCreate User model..."
});

// Task 1.1
await create_issue({
  title: "Write failing test for User model",
  team: "Engineering",
  parentId: phase1.id,
  labels: ["task"],
  description: "## Action\nCreate test file..."
});
```

**Step 8 - Confirm:**

```
## Linear Plan Created

**Project:** User Authentication

| Phase | ID | Tasks |
|-------|-----|-------|
| [Phase 1] Database Schema | PEA-101 | 3 |
| [Phase 2] Auth Endpoints | PEA-105 | 4 |
| [Phase 3] Middleware | PEA-110 | 2 |
| [Phase 4] Testing | PEA-113 | 1 |

**Total:** 4 phases, 10 tasks

Next: `/execute` or work in Linear
```

---

## Quick Reference

```
PROCESS: Same as /plan (plan)
OUTPUT:  Linear Issues (phases as parents, tasks as sub-issues)
TOOLS:   mcp__linear-server__create_issue (with parentId)

1. CLARIFY   → Goal and scope
2. RESEARCH  → Codebase patterns
3. DESIGN    → Phases and tasks
4. DOCUMENT  → Task details
5. VALIDATE  → User approval
6. SELECT    → Choose project
7. CREATE    → Issues with hierarchy
8. CONFIRM   → Return summary

HIERARCHY:
- Phase → Parent Issue (labels: ["phase"])
- Task → Sub-Issue (parentId: phase-uuid, labels: ["task"])
```

## Red Flags - STOP

- Skipping plan process and just converting a file
- Tasks that take more than 10 minutes
- Using `relatedTo` instead of `parentId`
- Missing checkpoints for phases
- Vague tasks like "Implement X"
- Creating without user validation

---

## Milestones Note

Linear milestones cannot be created via API/MCP. To use milestones:

1. Create milestones in Linear UI (Project → Overview → Add milestone)
2. Assign phases using: `update_issue({ id, milestone: "name" })`

---

## Integration

**Uses:**
- **plan** skill - Same process
- **Linear MCP** - Output target

**Mirrors:**
- `/plan` - Same process, different output (file vs Linear)

**Pairs with:**
- `/create-linear-spec` - Creates project first
- `/execute` - Execute the plan
