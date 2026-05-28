---
name: pr-draft-summary
description: Use this skill when you need to create a PR title and draft description after completing substantial code changes, ensuring the summary is ready for submission.
---

# PR Draft Summary

## Purpose
Produce the PR-ready summary required in this repository after substantive code work is complete: a concise change summary plus a PR-ready title and draft description.

## When to Trigger
- The task for this repo is finished (or ready for review) and it touched runtime code, tests, examples, docs with behavior impact, or build/test configuration.
- You are about to send the "work complete" response and need the PR block included.
- Skip only for trivial or conversation-only tasks where no PR-style summary is expected.

## Inputs to Collect Automatically (do not ask the user)
- Current branch: `git rev-parse --abbrev-ref HEAD`.
- Working tree: `git status -sb`.
- Untracked files: `git ls-files --others --exclude-standard` (use with `git status -sb`).
- Changed files: `git diff --name-only` (unstaged) and `git diff --name-only --cached` (staged); sizes via `git diff --stat` and `git diff --stat --cached`.
- Base reference (use the branch's upstream, fallback to `origin/main`):
  - `BASE_REF=$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null || echo origin/main)`.
  - `BASE_COMMIT=$(git merge-base --fork-point "$BASE_REF" HEAD || git merge-base "$BASE_REF" HEAD || echo "$BASE_REF")`.
- Commits ahead of the base fork point: `git log --oneline --no-merges ${BASE_COMMIT}..HEAD`.
- Category signals for this repo: runtime (`packages/`, `src/agents/`, `examples/`), tests (`packages/**/test`, `tests/`, `integration-tests/`), docs (`docs/`, `README.md`, `mkdocs.yml`, `AGENTS.md`, `.github/`), build/test config (`package.json`, `pyproject.toml`, `pnpm-lock.yaml`, `Makefile`, `tsconfig*.json`, `eslint.config.*`, `vitest*.ts`).

## Workflow
1. Run the commands above without asking the user; compute `BASE_REF`/`BASE_COMMIT` first so later commands reuse them.
2. If there are no staged/unstaged/untracked changes and no commits ahead of `${BASE_COMMIT}`, reply briefly that no code changes were detected and skip emitting the PR block.
3. Infer change type from the touched paths listed under "Category signals"; classify as feature, fix, refactor, or docs-with-impact.