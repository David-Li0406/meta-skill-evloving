---
name: skill-discovery
description: Use this at the start of non-trivial work to quickly load the right runbooks (skills + path-scoped instructions) before making changes.
---

## Goal

Avoid “missing context” by making skill discovery a deliberate first step.

## When to use

Use this whenever the task is:
- Multi-step or multi-file
- Touching an unfamiliar area (API/server, storage, scanner, UI, smoke)
- Debugging CI/smoke failures
- Changing REST contracts

## Procedure (fast, repeatable)

1) Identify the domain(s)
- Rust backend: CLI, server, storage, scanner
- Frontend: Vue UI under `view/`
- Smoke: end-to-end harness under `smoke/`
- Docs/contracts: `docs/openapi.json`, `docs/help/*`

2) Load path-scoped rules
- If you will touch Rust: `.github/instructions/backend.instructions.md`
- If you will touch UI: `.github/instructions/frontend.instructions.md`
- If you will touch smoke tests: `.github/instructions/smoke.instructions.md`

3) Load the 1–3 most relevant skills

Keyword → skill mapping (pick the best match):
- “agent scripts”, “low noise”, “dot reporter”, “no ANSI” → `.github/skills/agent-friendly-commands/SKILL.md`
- “endpoint”, “REST”, “DTO”, “OpenAPI”, “schema” → `.github/skills/api-contract-change-end-to-end/SKILL.md`
- “nextest”, “Rust tests”, “integration test failing” → `.github/skills/nextest-targeted-testing/SKILL.md`
- “Vitest”, “UI tests”, “typecheck”, “frontend test” → `.github/skills/vitest-targeted-testing/SKILL.md`
- “smoke”, “Playwright”, “E2E”, “serve” → `.github/skills/smoke-suite-debugging/SKILL.md`
- “local dev”, “Vite”, “lotar serve”, “ports”, “SSE” → `.github/skills/local-dev-serve-troubleshooting/SKILL.md`
- “task tracking”, “.tasks”, “LoTaR tasks” → `.github/skills/lotar-task-tracking/SKILL.md`

4) Verify before you assume
- Confirm current behavior (tests/repro) before changing semantics.
- Search for existing helpers before introducing new ones.

Safety note:
- `AGENTS.md` is the canonical policy (tests required, no secrets/PII, no git operations for recovery). Skills only add extra context.

## Continuous improvement

If you find yourself looking up the same thing twice (commands, env vars, gotchas), add it to the most relevant skill or create a new narrowly-scoped one. Keep changes minimal and link out to docs instead of duplicating them.
