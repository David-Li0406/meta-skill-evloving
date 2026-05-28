---
name: documentation-updater
description: >-
  Keep oltre-content-ingestor documentation accurate when
  code/config/infrastructure changes. Use when implementing features, refactors,
  or fixes that affect main code, scripts, env vars, integrations
  (Strapi/Slack/scraping providers). Updates README.md, AGENTS.md docs/, and
  operational guides, and verifies links/commands stay correct.
metadata:
  sync:
    version: 2
    files: {}
    hash: sha256-f9d608f205299e3b42dcd9925f28e15cbf015ce8bf0461358452f4b3d375e155
---
# Documentation Updater

Maintain `README.md`, `AGENTS.md`, `docs/`, and operational reference docs (e.g. `lambda-creation-rules.md`) as a first-class part of shipping changes in this repository (AWS CDK + Lambdas + Step Functions + MongoDB/LocalStack).

## When to use

Activate this Skill when:

- A change alters **how to run/test locally** (LocalStack, Docker, env bootstrap).
- You add/remove/change **environment variables**, secrets, or `.env*` usage.
- You change **AWS profile/region assumptions** used by scripts.
- You add/modify **operational scripts** under `scripts/` (seed, redeploy, read logs, quick update).

## Principles (project fit)

1. **Prefer updating existing docs over adding new ones.** Add a new doc only when it clearly reduces confusion.
2. **Keep docs executable.** Commands must match `package.json` scripts; paths must match the repo tree.
3. **Respect environment sourcing rules.** When docs tell users to run commands/tests, include the correct env sourcing:
   - Local/non-online: `source ./scripts/setup-env.sh local`
   - Production/online: `source ./scripts/setup-env.sh production`
4. **Document “what & why”, not internal trivia.** Focus on user outcomes and maintenance workflows.
5. **Cross-link instead of duplicating.** Point `README.md` to `docs/…` and keep a single source of truth.

## Workflow

### 1) Determine doc impact from the change

Identify what category the change falls into and what docs it likely affects.

### 2) Update the smallest set of docs that restores accuracy

- Update only the relevant sections; avoid broad rewrites.
- Keep headings and tone consistent with the existing file.
- Prefer adding links from `README.md` into `docs/*` for deep dives, instead of duplicating instructions.

### 3) Add “quick verification” steps

When documenting new or changed workflows, include:

- The exact command(s) to run (prefer `npm run …` scripts).
- The expected output/behavior at a high level (1–2 bullets).
- Any common failure mode and how to fix it (1 short subsection max).

### 4) Check for drift and broken references

- Confirm referenced scripts exist in `package.json`.
- Confirm file paths exist (`docs/…`, `scripts/…`, `lambdas/…`).
