---
name: sync-batdigest
description: Sync and deploy BatDigest by generating `batdigest-flask/dist`, inlining CSS, syncing into `batdigest-static`, committing/pushing, verifying live parity, and submitting IndexNow. Use when asked to "sync batdigest", "deploy batdigest", "generate dist", "inline css", "verify live deploy", or "submit IndexNow" for BatDigest.
---

# Sync BatDigest

## Overview

Run the canonical BatDigest sync/deploy runlists (git sync, generate `dist/`, inline CSS, copy into `batdigest-static`, verify live deploy, submit IndexNow) using `references/SYNC_DEPLOY_Agent.md` as the source of truth.

## Assumptions

- Repos live at `~/Coding_Projects/batdigest-flask` and `~/Coding_Projects/batdigest-static`.
- A Python virtualenv exists at `batdigest-flask/venv` (Mac/Linux) or `batdigest-flask\\venv` (Windows).
- You have `git` and either `rsync` (Mac/Linux) or `robocopy` (Windows).

## Workflow Decision Tree

1. Prompt for the runlist number (unless the user already specified one):
   - Ask: `Which sync would you like to run?`
   - `0` - Standard deploy (`#4 → #6 → #7 → #8`)
   - `1` - Standard deploy + verify (`#4 → #6 → #7 → #8 → #9`)
   - `2` - Standard deploy + verify + IndexNow (auto) (`#4 → #6 → #7 → #8 → #9 → #10`)
   - `3` - Full deploy + verify + IndexNow (auto + manual) (`#4 → #6 → #7 → #8 → #9 → #10 → #11`)
2. If `batdigest-static` is behind locally, run `#5` before `#8`.
3. If the user picks `3`, ask for the specific URLs for `#11` (or skip `#11` if they say none).
4. For each numbered step, use the platform-specific command block from `references/SYNC_DEPLOY_Agent.md`.

## Safety Notes

- Step `#8` mirrors directories (`rsync --delete` / `robocopy /MIR`): keep the excludes exactly as written to avoid deleting repo-only files.
- If `git pull --rebase` hits conflicts, stop and resolve before continuing.
- If verification (`#9`) fails, rerun after a few minutes (cache) before investigating deeper.

## Quick Mapping (Common Requests)

- “Standard deploy” → `#4 #6 #7 #8`
- “Deploy and verify” → `#4 #6 #7 #8 #9`
- “Deploy, verify, submit IndexNow” → `#4 #6 #7 #8 #9 #10` (plus `#11` if the user provides explicit URLs)

## Resources

- `references/SYNC_DEPLOY_Agent.md`: canonical runlists and command blocks (#0–#14)
