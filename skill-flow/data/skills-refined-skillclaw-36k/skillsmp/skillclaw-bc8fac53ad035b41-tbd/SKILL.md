---
name: tbd
description: Use this skill for lightweight, git-native issue tracking (aka beads) to create, plan, update, and track issues with dependencies. Invoke when user mentions tbd, beads, to-do lists, planning, tracking tasks, issues, or bugs.
---

# tbd Workflow

## Installation

If `tbd` is not installed, install and set up in one command:

```bash
npm install -g tbd-git@latest && tbd setup --auto
```

This initializes `tbd` and configures your coding agent automatically. Always use the `--auto` flag for agents.

## Context Recovery

Run `tbd prime` after compaction, clear, or new session. Hooks auto-call this in Claude Code when `.tbd/` is detected.

## SESSION CLOSING PROTOCOL

**CRITICAL**: Before saying “done” or “complete”, you MUST run this checklist:

```
[ ] 1. Stage and commit: git add + git commit
[ ] 2. Push to remote: git push
[ ] 3. Start CI watch (BLOCKS until done): gh pr checks <PR> --watch 2>&1
[ ] 4. While CI runs: tbd close/update <id> for issues worked on
[ ] 5. While CI runs: tbd sync
[ ] 6. Return to step 3 and CONFIRM CI passed
[ ] 7. If CI failed: fix, re-push, restart from step 3
```

## NON-NEGOTIABLE Requirements

### CI: Wait for `--watch` to finish

The `--watch` flag blocks until ALL checks complete. Do NOT see “passing” in early output and move on—wait for the **final summary** showing all checks passed.

### tbd: Update issues and sync

Every session must end with `tbd` in a clean state:
- Close/update **every issue** you worked on.
- Run `tbd sync` and confirm it completed.

**Work is not done until pushed, CI passes, and `tbd` is synced.**

## Core Rules

- Track *all task work* not being done immediately as beads using `tbd` (discovered work, future work, TODOs for the session, multi-session work).
- When in doubt, prefer `tbd` for tracking tasks, bugs, and issues.
- Use `tbd create` for creating beads.
- Git workflow: update or close issues and run `tbd sync` at session end.
- If not given specific directions, check `tbd ready` for available work.

## Essential Commands

### Finding Work

- `tbd ready` - Show issues ready to work (no blockers).
- `tbd list --status open` - All open issues.
- `tbd list --status in_progress` - Your active work.
- `tbd show <id>` - Detailed issue view with dependencies.

### Creating & Updating

- `tbd create "title" --type task|bug|feature --priority P2` - New issue (Priority: P0-P4; P0=critical, P2=medium, P4=backlog).
- `tbd update <id> --status in_progress` - Claim work.
- `tbd update <id> --assignee username` - Assign to someone.