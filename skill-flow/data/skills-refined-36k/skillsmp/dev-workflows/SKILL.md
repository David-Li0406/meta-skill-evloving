---
name: dev-workflows
description: Development workflows for the pipeline including tests, linting, local dev servers, CI checks, and code organization. Use when implementing features, running tests, or preparing changes for review.
---

# Dev Workflows

## Workflow

1) Identify the change scope
- Determine backend, frontend, scripts, or docs impact.

2) Select the minimal verification
- Prefer the smallest test or check that validates the change.
- Use existing scripts and Make targets where available.

3) Run checks and fix regressions
- Capture outputs and keep changes focused.

4) Summarize changes and testing
- Provide a concise test summary and any gaps.

## Repo Pointers

- `Makefile`
- `pyproject.toml`
- `package.json`
- `scripts/dev/`
- `scripts/verify-stack.sh`
- `docs/testing/`
- `docs/reference/testing-infrastructure.md`
- `docs/reference/code-organization.md`
- `docs/reference/git-conventions.md`

## Output Expectations

- Provide commands run and key results.
- Note any skipped tests and why.

## Guardrails

- Avoid broad test sweeps unless requested.
- Keep changes scoped and documented.
