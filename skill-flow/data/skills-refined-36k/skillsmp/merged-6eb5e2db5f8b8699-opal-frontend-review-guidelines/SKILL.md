---
name: opal-frontend-review-guidelines
description: Use this skill when reviewing code in opal-frontend or opal-frontend-common-ui-lib PRs, applying severity levels and the required comment format.
---

# Opal Frontend Review Guidelines

## Overview

Apply these rules when reviewing changes in opal-frontend and opal-frontend-common-ui-lib; focus on P0/P1 blockers and use the required comment format.

## Scope and Process

- Apply rules to changes in the PR only.
- Prefer specific, line-anchored feedback with rationale and concrete fixes.
- Treat P0 and P1 as blocking; P2 as advisory.

## Repo Scope

- Assume Angular v20+ standalone app/library using GOV.UK/HMCTS design system.
- Focus on TypeScript, templates, and styles under `projects/opal-frontend-common/**`, plus configuration affecting runtime behavior.
- Ignore generated files, build outputs (including `dist/` and `coverage/`), and `node_modules`.

## Severity Definitions

- **P0 (blocker):** Security risk, data loss, broken UX/AX, build/test failure, or architectural violation that will be hard to undo.
- **P1 (high):** Regressions in quality, maintainability, or performance with simple fixes.
- **P2 (advice):** Stylistic or non-critical improvements.

## P0 Rules (Blockers)

### Security and Safety

- Avoid unsanitised HTML or `bypassSecurityTrust*` without justification and tests.
- Avoid interpolating user data into `[innerHTML]`, `[srcdoc]`, or `style`, and avoid unsafe URL handling.
- Avoid credentials, tokens, secrets, or PII in code, logs, comments, or tests.

### Accessibility

- Keep interactive elements keyboard reachable; do not put `click` handlers on non-interactive elements without proper roles/tabindex.
- Provide visible labels or `aria-label` for form controls and buttons; ensure images have meaningful `alt`.

### Architecture and Build Integrity

- Use standalone components/routes/providers; avoid adding Angular modules when standalone is appropriate.
- Avoid mixing signals and imperative RxJS in ways that cause side effects in template evaluation.
- Avoid barrel exports (`index.ts`, `export *`) and barrel imports; use direct imports.
- Avoid CI/test failures, TypeScript errors, or missing required checks.

## P1 Rules (High Priority)

### Angular Correctness

- Prefer `@if`, `@for`, `@switch` over legacy structural directives in new/changed templates.
- Use computed signals and pure functions for derived state; avoid methods with side effects in templates.
- Choose RxJS concurrency intentionally: `switchMap` for latest-only, `exhaustMap` for form submit, `concatMap` when order matters.

### Code Quality Fundamentals

- Use clear, descriptive names; avoid abbreviations that obscure intent.
- Keep components and services small and cohesive; extract helpers for readability.
- Prefer simple, readable code; add comments that explain why decisions were made.
- Apply modern Angular features in new/changed code.

### Performance

- Avoid heavy work in templates (no `.map()`/`.filter()` or non-pure pipes in bindings).
- Lazy-load routes and large features; avoid broad shared providers when a standalone provider suffices.
- Guard against large third-party dependencies; note size and reason if introduced.

### Testing

- Add or maintain tests for new logic and error/empty states.
- Prefer Angular Testing Library/Harnesses; avoid brittle DOM selectors/data-testids when a Harness exists.

### Function Design

- Prefer small, single-purpose, pure functions.
- Keep cyclomatic complexity low.
- Pass explicit inputs and return data rather than performing side effects.

## P2 Rules (Advisory)

- Prefer container vs presentational component separation when complexity grows.
- Keep features self-contained by default; avoid barrels and prefer direct imports.
- Provide brief inline docs when introducing patterns others should copy.

## Ignore Unless Requested

- Ignore typos in comments/docs unless critical.
- Ignore pure formatting churn without semantic change.

## Comment Format

Use this exact shape:

```
[Severity]: <Rule name>
Problem: <what is wrong in one sentence>
Why: <risk/impact>
Fix: <specific change>
Example: <code snippet or link to guideline>
```

## Design System References

- https://design.homeoffice.gov.uk/design-system
- https://design-patterns.service.justice.gov.uk/
- https://design-system.service.gov.uk/
- https://alphagov.github.io/accessible-autocomplete/examples/