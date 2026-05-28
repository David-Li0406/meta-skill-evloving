---
name: codex-review
description: Run OpenAI Codex CLI reviews from Claude Code. Use when the user asks for a Codex review or mentions triggers like "codex-review", "/codex-review", or "codex review".
---

# Codex Review

## Overview

Run `codex review` and iterate on fixes until the review is clean. Claude Code applies fixes locally and re-runs the review.

## Workflow

1. Confirm the review target.
   - If the user specifies a target, follow it.
   - Otherwise, prefer `--uncommitted` when there are local changes.
   - If there are no local changes, use `--base origin/main` (or the repo default).
2. Prepare the temp environment under `~/.claude/tmp` (see "Temp directory setup"). Ensure these env vars are set before running `codex review`.
   - Claude Code runs each shell command in a fresh process, so `export` does not persist across commands.
   - Always run the temp setup and `codex review` in the same shell invocation (see "Command templates").
3. If the user wants to override the review model, append `-c review_model="MODEL"` to the command (default stays as-is when omitted).
4. If the user wants to override reasoning effort, append `-c model_reasoning_effort="EFFORT"` to the command (default stays as-is when omitted). Use a value supported by the review model.
5. Run `codex review` with the chosen target and any custom prompt (plus the optional `-c review_model="MODEL"` from step 3 and `-c model_reasoning_effort="EFFORT"` from step 4).
6. Read the review output and extract actionable findings.
7. If findings exist, fix them in the codebase and re-run the same review target.
8. Repeat until no findings remain or after 10 loops, then report status.

## Temp directory setup

Use a per-run temp directory to avoid `/tmp` failures in sandboxed environments. Set these env vars before running `codex review`.
Important: run the temp setup and `codex review` in the same shell invocation, or the exports will be lost.

```sh
mkdir -p ~/.claude/tmp
TMPDIR="$(mktemp -d ~/.claude/tmp/codex-review.XXXXXXXX)"
ZDOTDIR="$TMPDIR/zsh"
mkdir -p "$ZDOTDIR"
XCRUN_CACHE_PATH="$TMPDIR/xcrun_db"
DARWIN_USER_TEMP_DIR="$TMPDIR"
export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR
```

Only `~/.claude/tmp` is allowed for temp usage. Do not create temp directories inside the repo or under `/tmp`.

## Timeout

**Important**: `codex review` can take a long time (several minutes). Always set a **30-minute timeout** (1800000 ms) when running the command to ensure it completes.

## Command templates

Always include the temp directory setup before running `codex review` and do not split these into multiple shell commands:

```sh
mkdir -p ~/.claude/tmp && \
TMPDIR="$(mktemp -d ~/.claude/tmp/codex-review.XXXXXXXX)" && \
ZDOTDIR="$TMPDIR/zsh" && \
mkdir -p "$ZDOTDIR" && \
XCRUN_CACHE_PATH="$TMPDIR/xcrun_db" && \
DARWIN_USER_TEMP_DIR="$TMPDIR" && \
export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR && \
codex review --uncommitted [-c review_model="MODEL"] [-c model_reasoning_effort="EFFORT"]
```

```sh
mkdir -p ~/.claude/tmp && \
TMPDIR="$(mktemp -d ~/.claude/tmp/codex-review.XXXXXXXX)" && \
ZDOTDIR="$TMPDIR/zsh" && \
mkdir -p "$ZDOTDIR" && \
XCRUN_CACHE_PATH="$TMPDIR/xcrun_db" && \
DARWIN_USER_TEMP_DIR="$TMPDIR" && \
export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR && \
codex review --base <branch> [-c review_model="MODEL"] [-c model_reasoning_effort="EFFORT"]
```

```sh
mkdir -p ~/.claude/tmp && \
TMPDIR="$(mktemp -d ~/.claude/tmp/codex-review.XXXXXXXX)" && \
ZDOTDIR="$TMPDIR/zsh" && \
mkdir -p "$ZDOTDIR" && \
XCRUN_CACHE_PATH="$TMPDIR/xcrun_db" && \
DARWIN_USER_TEMP_DIR="$TMPDIR" && \
export TMPDIR ZDOTDIR XCRUN_CACHE_PATH DARWIN_USER_TEMP_DIR && \
codex review --commit <sha> [-c review_model="MODEL"] [-c model_reasoning_effort="EFFORT"]
```

## Output handling

- Summarize the review results in a short list.
- If fixes were applied, list the changed files and confirm the re-review is clean.
- If issues remain after the max loops, call out the remaining findings.
