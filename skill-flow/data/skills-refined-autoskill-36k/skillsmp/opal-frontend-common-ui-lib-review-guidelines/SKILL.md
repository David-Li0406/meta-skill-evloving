---
name: opal-frontend-common-ui-lib-review-guidelines
description: Automated review rules for opal-frontend-common-ui-lib PRs. Use when asked to review code, run @codex review, or provide PR feedback; apply severity levels and the required comment format.
---

# Opal Frontend Common UI Lib Review Guidelines

## Overview
Apply these rules when reviewing changes in opal-frontend-common-ui-lib; focus on P0/P1 blockers and use the required comment format.

## How to use
- Apply these rules to changes in this PR only.
- Prefer specific, line-anchored comments with a short rationale and a concrete fix.
- Treat P0 and P1 as blocking; P2 as advisory.

## Scope of review
Automated review should only analyze and comment on project-owned code within this repository.

In particular:
- Focus on TypeScript, templates, and styles under `projects/opal-frontend-common/**`, plus configuration that affects runtime behavior.
- Ignore generated files, build outputs (including `dist/` and `coverage/`), and `node_modules`.

## Severity definitions

- **P0 (blocker):** Security risk, data loss, broken UX/AX, build/test failure, or architectural violation that will be hard to undo.
- **P1 (high):** Regressions in quality, maintainability, or performance with simple fixes.
- **P2 (advice):** Stylistic or non-critical improvements.

---

## Repo scope

Angular v20+ standalone library using GOV.UK/HMCTS design system. Prefer modern Angular primitives (standalone components, template control flow, signals) and accessibility to WCAG 2.2 AA.

---

## P0 rules (must block)

1. **Security & safety**

- Unsanitised HTML or `bypassSecurityTrust*` without justification and tests.
- Interpolating user data into `[innerHTML]`/`[srcdoc]`/`style`, or unsafe URL handling.
- Credentials, tokens, secrets, or PII in code, logs, comments, or tests.

2. **Accessibility (AX)**

- Interactive elements not reachable by keyboard, `click` handlers on non-interactive elements without proper roles/tabindex.
- Missing visible label/`aria-label` for form controls or buttons; images without meaningful `alt`.

3. **Architecture & build integrity**

- New Angular modules where a **standalone** component/route/provider is appropriate.
- Mixing **signals** and imperative RxJS within the same component in a way that causes side-effects in template evaluation.
- Using **barrel exports** (`index.ts`, `export *`) or importing via barrels. Prefer **direct, specific imports** from the declaring file. Keep features self-contained by default.
- CI/test failures, TypeScript errors, or missing required checks.

---

## P1 rules (high priority)

1. **Angular correctness**

- Prefer `@if`, `@for`, `@switch` over legacy structural directives in new/changed templates.
- Use **computed signals** and **pure functions** for derived state; avoid calling methods with side effects in templates.
- Choose RxJS concurrency intentionally: `switchMap` for latest-only, `exhaustMap` for form submit, `concatMap` when order matters.

2. **Code quality fundamentals**

- Use clear, descriptive names for symbols, inputs/outputs, and tests; avoid abbreviations that obscure intent.
- Keep components and services small and cohesive; extract helpers to keep implementations readable.
- Prefer simple, readable code over cleverness; add comments that explain why decisions were made.
- Apply modern Angular features (standalone components, signals, control flow) in new/changed code.

3. **Performance**

- Avoid heavy work in templates (no `.map()`/`.filter()` or non-pure pipes inside bindings).
- Lazy-load routes and large feature areas; avoid broad shared providers when a **standalone provider** suffices.
- Guard against large third-party dependencies; if introduced, note size and reason.

4. **Testing**

- Add/maintain tests for new logic and error/empty states.
- Prefer Angular Testing Library/Harnesses; avoid brittle DOM selectors/data-testids when a Harness exists.

5. **Function design**

- Prefer **small, single-purpose, pure functions**.
- Keep cyclomatic complexity low.
- Pass explicit inputs and return data rather than performing side effects.

---

## P2 rules (advisory)

- Prefer container (smart) vs. presentational component separation when complexity grows.
- Keep features **self-contained** by default. **No barrels** (`index.ts`, `export *`) -- prefer direct file imports for tree-shaking.
- Provide brief inline docs when introducing patterns others should copy.

---

## What to ignore (unless requested)

- Typos in comments/docs (treat as P2 unless critical).
- Pure formatting churn without semantic change.

---

## Comment style for the reviewer (automated)

Use this shape to keep feedback crisp and useful:

### Examples

- **P0: Unsanitised HTML**
  _Problem:_ `[innerHTML]` used with dynamic user content in `case-summary.component.html`.
  _Why:_ XSS risk.
  _Fix:_ Remove `innerHTML`, render via bindings/DOM APIs, or use a trusted, sanitised subset with tests.

- **P1: Template work**
  _Problem:_ Method call `getItems()` used in template; performs filtering.
  _Why:_ Re-runs each change detection; performance risk.
  _Fix:_ Move to computed signal `itemsFiltered = computed(() => ...)` and bind to that.

- **P1: Concurrency**
  _Problem:_ Form submit uses `mergeMap`, causing double submits.
  _Why:_ Users can trigger parallel requests.
  _Fix:_ Use `exhaustMap` around submit stream and disable button while pending.

---

## Design system references
- https://design.homeoffice.gov.uk/design-system
- https://design-patterns.service.justice.gov.uk/
- https://design-system.service.gov.uk/
- https://alphagov.github.io/accessible-autocomplete/examples/
