---
name: beads-issue-tracking
description: Use this when working on tasks in this repo that require bd (beads) issue tracking, status updates, and the mandatory end-of-session push workflow.
---

# Beads (bd) issue tracking workflow

Use this skill whenever the user asks to start work on an issue, check work queue/status, add notes, mark blocked, close work, or “land the plane”.

## Commands (preferred)

- Find work: `bd ready`
- Current status: `bd status`
- View issue details: `bd show <id>` (or `bd show <id> --json`)
- Start work: `bd update <id> --status in_progress`
- Add a note: `bd update <id> --notes "..."`
- Blocked (with notes): `bd update <id> --status blocked --notes "..."`
- Close issue: `bd close <id> --reason "..."`
- Sync bd metadata: `bd sync`

## Hard rules (this repo)

- If code changes were made, do not end the session until **push succeeds**.
- Prefer the repository’s documented workflows in `_AGENTS.md`.

## “Landing the plane” checklist (must follow)

1. Run appropriate quality gates for the changed area (tests/build/lint if available).
2. Update bd issue status (close finished work, or set blocked with notes).
3. Follow the mandatory session close protocol (do not skip steps):
   - `git status` (confirm what changed)
   - `git add <files>` (stage code changes)
   - `bd sync` (commit beads changes)
   - `git commit -m "..."` (commit code)
   - `bd sync` (commit any new beads changes)
   - `git push` (must succeed)

## Guidance for agents

- If an issue id is not provided, ask for the bd issue id (one question max), or run `bd status` / `bd ready` to locate candidates.
- Prefer using editor tasks when available (e.g., VS Code tasks for bd commands).
