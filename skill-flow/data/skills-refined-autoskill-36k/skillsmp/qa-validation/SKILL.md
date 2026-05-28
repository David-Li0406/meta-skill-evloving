---
name: qa-validation
description: Quality assurance, validation checks, metrics, and regression verification for pipeline outputs. Use when running validation suites, checking image quality, or defining acceptance criteria.
---

# QA + Validation

## Workflow

1) Define acceptance criteria
- Clarify which metrics or artifacts define success.
- Align on thresholds and expected ranges.

2) Select the right validation tools
- Prefer existing diagnostics/validation scripts.
- Run the smallest useful scope first.

3) Execute validation
- Capture outputs and logs for reproducibility.

4) Summarize results
- Highlight failures, deltas, and likely root causes.

## Repo Pointers

- `docs/pipeline-validation.md`
- `docs/verification/`
- `docs/testing/`
- `scripts/diagnostics/`
- `scripts/quality/`
- `scripts/validation/`
- `tests/`

## Output Expectations

- Provide pass/fail summary with key metrics.
- Provide artifact locations and commands used.

## Guardrails

- Avoid changing thresholds without clear approval.
- Record the exact dataset and config used for validation.
