---
name: git-commit
description: Generate Conventional Commits messages and run git add/git commit from current repo changes. Use when the user says "git commit" or asks to auto-stage changes and craft a commit message from the diff.
---

# Git Commit Agent

## Overview

Create a Conventional Commits message based on the current staged diff, then perform `git commit` after auto-staging relevant changes (excluding obvious temp files).

## Workflow

1. Check for already-staged changes.
   - Run `git diff --cached --name-status`.
   - If staged files exist, skip staging and proceed to inspection/commit using the staged set.
2. Stage changes when nothing is staged.
   - Run the staging script from this skill: `python3 <skill-root>/scripts/stage_changes.py`
   - The script stages tracked changes (`git add -u`) and selectively stages untracked files that are not ignored and not temporary.
   - If nothing is staged after running, stop and report that there are no relevant changes to commit.

3. Inspect staged changes.
   - Use `git diff --cached --name-status` to understand file-level changes.
   - Use `git diff --cached` to spot functional changes and key behaviors.

4. Compose a Conventional Commits message.
   - Format:
     - Title line: `type(scope): short summary`
     - Body: 2-6 bullet points, each starting with `- `, describing the most important changes.
   - Choose `type` by best fit:
     - `feat`: new user-facing functionality
     - `fix`: bug fixes or behavior corrections
     - `refactor`: internal change without behavior change
     - `docs`: documentation-only change
     - `test`: tests-only change
     - `build`, `ci`, `chore`, `perf`, `style`, `revert` as appropriate
   - Choose `scope` from the most relevant top-level area (examples: `core`, `raftor`, `wal`, `rpc`, `tests`, `docs`, `build`). Omit scope if unclear.
   - Keep the summary under ~72 chars; avoid trailing period.

5. Commit without prompting for confirmation.
   - Use multi-line message via repeated `-m` flags, for example:
     - `git commit -m "type(scope): summary" -m "- bullet one" -m "- bullet two"`

## Notes

- Do not include obvious temporary or generated files (e.g., editor swap files, build outputs, caches).
- Prefer clarity over cleverness in the summary and bullets; mention key files if it helps understanding.

## Resources

### scripts/

- `stage_changes.py`: stage tracked changes and select untracked files while skipping temp-like paths.
