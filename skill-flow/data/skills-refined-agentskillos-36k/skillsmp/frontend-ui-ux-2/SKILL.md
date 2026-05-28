---
name: frontend-ui-ux
description: Frontend UI/UX changes, dashboards, visualizations, and UI testing. Use when modifying the web UI, improving UX, adjusting visualizations, or running frontend tests.
---

# Frontend UI + UX

## Workflow

1) Clarify the UX goal
- Identify the screen, user role, and expected behavior.
- Define success criteria (usability, performance, visual clarity).

2) Locate the implementation
- Find the relevant UI module and data source.
- Prefer existing components and patterns unless a new pattern is justified.

3) Implement with intentional design
- Make visual choices explicit (type, color, spacing, motion).
- Avoid generic layouts; tailor to the pipeline’s domain and data.

4) Verify behavior
- Run the smallest relevant UI test or manual flow.
- Capture screenshots or notes for review.

## Repo Pointers

- `frontend/`
- `e2e/`
- `verify_ui.spec.ts`
- `debug_ui.spec.ts`
- `docs/how-to/dashboard.md`
- `docs/how-to/interactive-visualizations.md`
- `docs/how-to/visualization.md`
- `docs/how-to/visualization-expansion.md`
- `scripts/playwright/`

## Output Expectations

- Provide file paths changed and rationale for design choices.
- Provide a minimal test or manual verification summary.

## Guardrails

- Preserve existing visual language unless explicitly changing it.
- Avoid UI regressions by checking critical flows.
