# Testing & Quality Plan: <Sprint/Project Name>

> **Template scope**: Use this template in **sprint plans** for overall testing strategy.
> For individual task testing requirements, use `testing-expectations.template.md`.

## Overview

This document defines testing requirements and quality gates for the sprint/project.

**A plan without testing requirements is INCOMPLETE.**

---

## Unit Testing

### New tests required for:

| Module/Feature | Test File | Owner | Priority |
|----------------|-----------|-------|----------|
| <module> | `<test-file.test.ts>` | TASK-XXX | Required |
| <feature> | `<test-file.test.ts>` | TASK-YYY | Required |

### Existing tests to update:

| Module/Behavior | Test File | Reason | Owner |
|-----------------|-----------|--------|-------|
| <module> | `<test-file.test.ts>` | <behavior change> | TASK-XXX |

---

## Coverage Expectations

### Rules:

- [ ] New code must not reduce overall coverage
- [ ] Target coverage: <X%> (or "no specific target, justify")
- [ ] Coverage gaps introduced by refactors must be addressed

### Coverage exceptions (if any):

| File/Module | Reason for exception |
|-------------|---------------------|
| <file> | <reason> |

---

## Integration / Feature Testing

### Required scenarios:

| Scenario | Description | Tasks Involved | Owner |
|----------|-------------|----------------|-------|
| <scenario 1> | <description> | TASK-XXX, TASK-YYY | <owner> |
| <scenario 2> | <description> | TASK-ZZZ | <owner> |

### Test boundaries and assumptions:

- <boundary 1>
- <assumption 1>

---

## CI / CD Quality Gates

The following MUST pass before merge:

| Check | Required | Notes |
|-------|----------|-------|
| Unit tests | Yes | `npm test` |
| Integration tests | <Yes/No/If applicable> | <notes> |
| Coverage checks | <Yes/No> | <threshold or "no regression"> |
| Type checking | Yes | `npm run type-check` |
| Linting / formatting | Yes | `npm run lint` |
| Build step | Yes | `npm run build` |
| Security audit | <Yes/No> | <notes> |

---

## Backend Revamp Safeguards

*Required if this sprint includes backend changes.*

### Existing behaviors that MUST be preserved:

| Behavior | Test protecting it | Verified by |
|----------|-------------------|-------------|
| <behavior 1> | `<test>` | TASK-XXX |
| <behavior 2> | `<test>` | TASK-YYY |

### Behaviors intentionally changed:

| Old Behavior | New Behavior | Reason | Test |
|--------------|--------------|--------|------|
| <old> | <new> | <reason> | `<test>` |

### Critical paths requiring regression tests:

| Critical Path | Tests | Owner |
|---------------|-------|-------|
| <path 1> | `<tests>` | TASK-XXX |

---

## Per-Task Testing Requirements

| Task ID | Unit Tests | Integration Tests | Coverage | Notes |
|---------|------------|-------------------|----------|-------|
| TASK-XXX | Required | Not required | No regression | <notes> |
| TASK-YYY | Required | Required | +5% target | <notes> |

---

## Quality Enforcement

- [ ] All tasks have explicit testing requirements
- [ ] No "add tests" without specifying what
- [ ] CI gates are explicit
- [ ] PRs without required tests will be REJECTED

---

## Review Checklist (Before Sprint Starts)

- [ ] Every feature has a testing plan
- [ ] Backend changes have regression tests
- [ ] CI gates are defined for each phase
- [ ] Test ownership is assigned
- [ ] Coverage expectations are documented
