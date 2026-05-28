# Module: Testing & Quality Planning (Required for Project Plans)

## Objective

Ensure that every planned feature, refactor, or backend revamp includes explicit testing and CI/CD quality requirements.

## When this module is required

You MUST invoke this module when:
- Adding new features
- Modifying existing behavior
- Refactoring backend logic
- Changing data models, APIs, or workflows

## Testing Surfaces You Must Consider

### 1) Unit Tests

- Required for all new logic
- Required when existing logic behavior changes
- Specify:
  - What modules/functions require tests
  - Whether new tests must be written or existing tests updated

### 2) Coverage Expectations

- Define minimum coverage expectations if applicable
- Specify:
  - New code must not reduce coverage
  - Coverage gaps introduced by refactors must be addressed
- If coverage is not enforced, explicitly state why

### 3) Integration / Feature Tests

- Required when:
  - Multiple components interact
  - APIs, workflows, or state transitions change
- Specify test boundaries and assumptions

### 4) CI / CD Checks (Mandatory)

For each phase or task, specify which checks must pass:
- [ ] Unit tests
- [ ] Integration tests
- [ ] Coverage checks
- [ ] Type checking
- [ ] Linting / formatting
- [ ] Build checks

### 5) Regression Protection

If this is a backend revamp:
- Identify critical paths that must not regress
- Require tests that lock in existing behavior
- Explicitly call out "behavior preserved vs behavior changed"

## Output Requirement

You must produce a **Testing & Quality Plan section** in every project plan.

Use `templates/testing-quality-plan.template.md` for the format.

## Quality Gates

PRs without tests when required **WILL BE REJECTED**.

Engineers cannot merge without:
- All specified tests passing
- Coverage requirements met (if defined)
- All CI checks green

## Red flags

- "Add tests" without specifying what tests
- Backend changes without regression tests
- New features without unit tests
- Refactors without coverage impact analysis
