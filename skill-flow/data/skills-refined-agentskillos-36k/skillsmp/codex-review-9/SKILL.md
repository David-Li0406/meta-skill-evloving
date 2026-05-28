---
name: codex-review
description: Self-review loop for code changes. Use when Codex edits files or prepares a PR and should run `codex exec --sandbox workspace-write review --base BASE`, fix findings, and re-run until clean (max 10). Also run tests when a test command is configured or detectable.
---

# Codex Review

## Overview
Run tests first when possible, then run a local self-review loop with `codex exec --sandbox workspace-write review` after code changes, using a 30-minute timeout for the review command, select the most appropriate base, and re-run tests if review fixes changed code.

## Workflow
1. Confirm the repo is a git checkout and changes exist. If `git status --porcelain` is empty, skip the loop.
2. Confirm the working directory is the repo root for the changes under review. If changes live in a nested repo (e.g., `dependencies/<Repo>`), run all commands from that repo root or set `workdir`/`-C` so paths like `Sources/` resolve correctly.
3. Resolve the test command (see "Test selection") and run tests now. If tests fail, fix and repeat step 3. If no test command is found, continue.
4. Prepare the temp environment under `~/.codex/tmp` (see "Temp directory setup"). Ensure these env vars are set in the `codex exec --sandbox workspace-write review` process environment (do not rely on a shell wrapper).
5. Resolve the review base (see "Base selection").
6. If the user wants to override the review model, append `-c review_model="MODEL"` to the review command (default stays as-is when omitted).
7. If the user wants to override reasoning effort, append `-c model_reasoning_effort="EFFORT"` to the review command (default stays as-is when omitted). Use a value supported by the review model.
8. Run `codex exec --sandbox workspace-write review --base <base>` (plus the optional `-c review_model="MODEL"` from step 6 and `-c model_reasoning_effort="EFFORT"` from step 7) with the temp env from step 4, using a 30-minute (1800s) timeout.
9. If findings exist, fix them.
10. If this is a base-branch review and fixes were made, commit the fixes before re-running the review (see "Commit-before-rereview").
11. Repeat steps 8-10 until clean or 10 iterations.
12. If any fixes were made after the initial test run, re-run tests (see "Test selection"). If tests fail, fix and return to step 8.
13. Stop after 10 iterations and report remaining issues with context.

## Temp directory setup
Use a per-run temp directory to avoid `/tmp` failures and allow parallel runs. Set these env vars in the process that launches `codex review`.
Only `~/.codex/tmp` is allowed for temp usage. Do not create temp directories inside the repo (e.g., `.tmp`) or under `/tmp`.
When running with `--sandbox workspace-write`, ensure `ZDOTDIR` is inside `TMPDIR` so the shell does not access paths outside the sandbox.
Avoid `~/.codex/tmp/zsh.*` or other `TMPDIR`-external `ZDOTDIR` paths.

```
mkdir -p ~/.codex/tmp
TMPDIR="$(mktemp -d ~/.codex/tmp/codex-review.XXXXXXXX)"
ZDOTDIR="$TMPDIR/zsh"
mkdir -p "$ZDOTDIR"
XCRUN_CACHE_PATH="$TMPDIR/xcrun_db"
DARWIN_USER_TEMP_DIR="$TMPDIR"
export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR
```

Recommended launch example:

```
mkdir -p ~/.codex/tmp
TMPDIR="$(mktemp -d ~/.codex/tmp/codex-review.XXXXXXXX)"
ZDOTDIR="$TMPDIR/zsh"
mkdir -p "$ZDOTDIR"
XCRUN_CACHE_PATH="$TMPDIR/xcrun_db"
DARWIN_USER_TEMP_DIR="$TMPDIR"
export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR
codex exec --sandbox workspace-write review --base <base> [-c review_model="MODEL"] [-c model_reasoning_effort="EFFORT"]
```

If you cannot set these env vars directly on the `codex review` process, stop and ask the user.

Keep the temp dir for debugging if needed; otherwise it can be removed after the loop.

## Base selection
Use the first match in this priority order, then keep it fixed for the loop:
1. Use `CODEX_REVIEW_BASE` if set.
2. If `.codex-review.json` exists at repo root, read `base` or `baseCandidates`.
3. If the current branch has an upstream (`git rev-parse --abbrev-ref --symbolic-full-name @{u}`), use it.
4. If `origin/HEAD` exists, use it.
5. Else collect candidates from: `origin/develop/*`, `origin/develop`, `origin/main`, `origin/master`, `develop`, `main`, `master`. Prefer candidates that are ancestors of `HEAD`.
6. If a single candidate remains, use it. If none or multiple remain, ask the user to choose and explain the options.

## Test selection
Use the first match in this priority order:
1. Use `CODEX_TEST_COMMAND` if set.
2. If `.codex-review.json` defines `test`, run it.
3. If `scripts/test.sh` exists, run `./scripts/test.sh`.
4. If `Makefile` has a `test` target, run `make test`.
5. If `package.json` has a `test` script: use `pnpm test` when `pnpm-lock.yaml` exists, otherwise `npm test`.
6. If no test command is found, report "Not run (no test command configured)".

## Commit-before-rereview
Require a commit before re-running the review only for base-branch reviews. Skip this for worktree-only reviews.

Determine review mode:
- Treat the review as worktree-only if the user explicitly asked for "作業ベース" or `.codex-review.json` sets `"reviewMode": "worktree"`.
- Otherwise, treat it as a base-branch review (e.g., current branch vs `main`, `develop`, or an upstream).
- If unsure, ask the user.

Commit rules for base-branch reviews:
- If fixes were made after review findings, stage only those fixes and commit before re-running review.
- Do not commit unrelated changes; if unrelated changes exist, ask the user what to include.
- Write a concise, diff-based commit message tailored to the fixes.
- Follow repository policy (only commit when allowed); if unsure, ask the user.

## Notes
- Honor explicit user requests to skip review or tests.
- Ask the user to choose the base when ambiguous; do not guess silently.
