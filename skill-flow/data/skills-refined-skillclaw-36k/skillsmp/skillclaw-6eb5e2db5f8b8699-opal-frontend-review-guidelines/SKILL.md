---
name: opal-frontend-review-guidelines
description: Use this skill when reviewing code for opal-frontend or opal-frontend-common-ui-lib PRs, applying severity levels and the required comment format.
---

# Opal Frontend Review Guidelines

## Overview

Apply these rules when reviewing changes in opal-frontend or opal-frontend-common-ui-lib; focus on P0/P1 blockers and use the required comment format.

## Scope and Process

- Apply rules to changes in the PR only.
- Prefer specific, line-anchored feedback with rationale and concrete fixes.
- Treat P0 and P1 as blocking; treat P2 as advisory.

## Repo Scope

- Assume Angular v20+ standalone app/library using GOV.UK/HMCTS design system.
- Prefer modern Angular primitives (standalone components, template control flow, signals).
- Ensure accessibility aligns with WCAG 2.2 AA.

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