---
name: using-jj
description: Use when operating in a repository that contains `.jj/`, when a repository is colocated with `.jj/` and `.git/`, or when the user mentions jj/Jujutsu. Prefer jj workflows over git in jj-managed repositories unless the user explicitly requests git.
---

# Jujutsu (jj) workflow

## Goal
Execute VCS tasks in jj-managed repositories using jj's model, with commands verified by `jj help` and no guessing.

## Terminology
Term definitions live in `references/jj-vocabulary.json`. Do not inline glossaries here; update the vocabulary package instead.

## Workflow (scripted, fail-closed)
1. Run `python3 skills/using-jj/scripts/detect_vcs.py --path <path> --format json`. Proceed only when `vcs` is `jj` or `colocated`; otherwise stop and follow the repository's VCS.
2. Run `python3 skills/using-jj/scripts/catalog_commands.py --format json` (source `markdown-help`, fallback `completion:bash`).
3. If exactly one candidate: run `jj help <command>`, then execute using the documented syntax and flags.
4. If multiple candidates: compare summaries to the stated intent; if still ambiguous, ask one focused question listing options and wait for an explicit choice.
5. If no candidates: run `jj help` and `jj help -k <keyword>` to refine, re-run `catalog_commands`, and if still none, fail closed with the error template below.
6. Solve with catalog + help before asking for clarification; do not punt when the tools can resolve the intent.

## Script interfaces (examples)
- detect_vcs: `python3 skills/using-jj/scripts/detect_vcs.py --path . --format json` -> keys: `vcs`, `path`, `root`, `jj_root`, `git_root`, `jj_root_source`, `git_root_source`, `warnings`.
- catalog_commands: `python3 skills/using-jj/scripts/catalog_commands.py --format json` -> keys: `source`, `generated_at`, `command_count`, `commands` (each: `name`, `summary`, `usage`). Uses `jj util markdown-help`, falls back to `jj util completion bash` (command names only).

## Operational defaults (jj model)
- The working copy is a commit; there is no staging area. Finish work by updating the description and moving to a new empty change (use `jj help` to find exact commands).
- Use change IDs as stable identifiers; commit/revision IDs are snapshots that can change.
- Bookmarks are named pointers that follow rewrites; assume there is no current bookmark.
- Conflicts can remain in the tree after rewrites; resolve them explicitly with jj's conflict tooling.
- The operation log is the recovery mechanism; prefer reversible steps.
- Canonical terminology lives in `skills/using-jj/references/jj-vocabulary.json`. Validate changes with `python3 skills/terminology-work/scripts/validate_vocab.py`.

## Git interop
- Treat jj as Git-backed, but prefer jj's git integration (`jj help git`) instead of calling git directly.
- In colocated repositories, use git only when the user explicitly asks or a tool cannot operate via jj.

## Script behavior (Unix style)
- Compose small, explicit steps. Treat script output as data and avoid hidden state or inference.
- Accept critical identifiers as flags; only infer when there is exactly one unambiguous candidate.
- Capture stdout/stderr, check exit codes, and fail closed on mismatches.
- Report what was discovered and why decisions were made; no silent fallbacks.

## Fail-closed errors
If `detect_vcs` shows no jj repository:
- what failed: jj workflow not applicable
- why it failed: `.jj/` not detected in the current path
- required input: confirm the repository location or the intended VCS
- discovered: `detect_vcs` output and current working directory

If `jj` is missing:
- what failed: `jj` executable not found
- why it failed: `jj` not on PATH
- required input: a PATH where `jj` exists or install jj
- discovered: `detect_vcs` output and current working directory

If intent cannot be mapped after `catalog_commands` and keyword help:
- what failed: no jj command matches the stated intent
- why it failed: no candidate summaries matched the intent
- required input: a jj-specific description of the goal or an explicit command choice
- discovered: `catalog_commands` output, `jj help` summaries, and keywords attempted
