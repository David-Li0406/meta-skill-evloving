# ABOUTME: Templates for spec-driven development
# ABOUTME: Spec files, task files, and README configuration

# Spec-Driven Development Templates

Copy and adapt these templates when creating spec artifacts.

---

## Spec File Template

**Filename**: `specs/{feature-slug}.md`

```markdown
# Spec: {Feature Name}

**Status**: DRAFT | APPROVED | IN_PROGRESS | COMPLETED
**Created**: {YYYY-MM-DD}
**Last Updated**: {YYYY-MM-DD}

---

## 1. Objective

{One paragraph: What are we building and WHY?}

---

## 2. Requirements

### Functional Requirements

- [ ] FR1: {System must do X when Y happens}
- [ ] FR2: {User can perform Z action}

### Non-Functional Requirements

- [ ] NFR1: Performance - {e.g., Response time < 200ms}
- [ ] NFR2: Security - {e.g., Auth required}

### Out of Scope

- {What we are NOT building}

---

## 3. Technical Strategy

### Stack

- **Frontend**: Next.js component in `src/app/...`
- **Backend**: Fastify route in `src/modules/...`
- **Database**: Prisma schema changes

### Key Components

1. {Component A} - {Purpose}
2. {Component B} - {Purpose}

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {Decision 1} | {Choice} | {Why} |

---

## 4. Acceptance Criteria

- [ ] AC1: {Specific, testable criterion}
- [ ] AC2: {Specific, testable criterion}

---

## 5. Open Questions

1. {Question about scope/behavior?}
2. {Question about edge cases?}

---

## 6. References

- {Link to related docs}
- {Link to existing code}
```

---

## Task File Template

**Filename**: `specs/{feature-slug}.tasks.md`

```markdown
# Tasks: {Feature Name}

**Spec**: ./{feature-slug}.md
**Created**: {YYYY-MM-DD}
**Status**: PENDING | IN_PROGRESS | COMPLETED

---

## Context

{2-3 sentence summary from spec}

---

## Prerequisites

- [ ] {Setup needed}
- [ ] {Dependencies}

---

## Tasks

### Phase 1: Foundation

- [ ] **Task 1**: {Description}
  - Acceptance: {How to verify}
  - Files: {Expected files}

- [ ] **Task 2**: {Description}
  - Acceptance: {How to verify}
  - Files: {Expected files}

### Phase 2: Core Implementation

- [ ] **Task 3**: {Description}
  - Acceptance: {How to verify}

### Phase 3: Integration

- [ ] **Task 4**: {Integration task}
  - Acceptance: {How to verify}

---

## Completion Checklist

- [ ] All tasks marked complete
- [ ] All tests passing
- [ ] Pre-commit hooks passing
- [ ] Spec acceptance criteria met

---

## Notes

{Execution notes, blockers, decisions}
```

---

## Minimal Spec Template (Quick Start)

For simple features:

```markdown
# Spec: {Feature Name}

**Status**: DRAFT

## Objective
{What and why in 2-3 sentences}

## Requirements
- [ ] {Requirement 1}
- [ ] {Requirement 2}

## Approach
{Brief technical strategy}

## Open Questions
1. {Question?}
```

---

## specs/README.md Template

```markdown
# Specs Configuration

Project-specific overrides for spec-driven development.

## Language Configuration

Primary: TypeScript (Next.js + Fastify)

## Project Conventions

### Required Spec Sections

- [ ] Security considerations (for auth-related specs)
- [ ] Performance implications (for data-heavy features)

### Naming Conventions

- Spec files: `{feature-name}.md` (kebab-case)
- Task files: `{feature-name}.tasks.md`
- Branch naming: `feature/spec-{name}`

## Workflow Overrides

### Before /spec.tasks

- Ensure related Prisma schema is designed

### During /spec.run

- Run `npm run test` after each task
- Invoke `/typescript` for .ts files

### After Completion

- Update CLAUDE.md if new module added
```
