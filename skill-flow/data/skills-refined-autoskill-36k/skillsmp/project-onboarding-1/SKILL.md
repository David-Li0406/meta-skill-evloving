---
name: project-onboarding
description: Project-specific onboarding context (roles, key flows, data sensitivity, how to run tests, and where the canonical docs live).
---

## Canonical project context

- Project brief: `orga/domain/project-brief.md`
- Requirements: `orga/domain/requirements.md`
- Architecture: `orga/domain/architecture.md`
- Data model: `orga/domain/data-model.md`
- Plan: `orga/domain/project-plan.md`

## Users, roles, and permissions

- Define roles and what each role can see/do.
- If the project has sensitive data, document the threat hotspots and required mitigations.

## Privacy & security

- Data classification (public/internal/secret) and what counts as PII.
- Secrets handling: what must never be committed.
- High-risk surfaces (uploads, admin screens, exports, webhooks, auth flows).
- Minimal threat sketch and required tests/smoke checks.

## Repo hygiene

- `.gitignore` should exclude secrets and local artifacts (e.g. `.env`, `.venv/`, caches, uploads).
- Prefer `.env.example` for documenting required environment variables.

## Key flows

- List the top user journeys (the ones that drive most design/testing decisions).

## Development workflow

- Tasks index: `orga/tasks/TASKS.md`
- Start a task: GitHub Actions **Start Task**, then `/plan-task`.
- Finish a task: GitHub Actions **Finish Task**.

## Commands

- Tests: `python -m pytest -q`

## Notes

Update this skill whenever the project brief changes significantly.
