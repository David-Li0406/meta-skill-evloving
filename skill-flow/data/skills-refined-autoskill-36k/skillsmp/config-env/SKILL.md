---
name: config-env
description: Environment setup, configuration management, ports, and runtime settings for the pipeline. Use when adjusting configs, setting env vars, or diagnosing environment-specific behavior.
---

# Config + Environment

## Workflow

1) Identify the environment
- Clarify local vs staging vs production.
- Confirm which services and ports are involved.

2) Locate the configuration source of truth
- Prefer documented configuration maps and defaults.
- Avoid hardcoding when configuration is available.

3) Apply changes carefully
- Make minimal, reversible edits.
- Validate with a focused smoke test.

4) Record changes
- Document the config change and rationale.

## Repo Pointers

- `config/`
- `docs/reference/configuration.md`
- `docs/reference/config-architecture.md`
- `docs/reference/configuration-map.md`
- `docs/reference/environment-variables.md`
- `docs/reference/PORT_ASSIGNMENTS.md`
- `docs/reference/PORT_MIGRATION_8080_TO_7000.md`
- `setup-env.sh`

## Output Expectations

- Provide the exact config diffs and files touched.
- Provide a minimal validation step and outcome.

## Guardrails

- Avoid changing secrets in-repo.
- Keep environment-specific overrides isolated.
