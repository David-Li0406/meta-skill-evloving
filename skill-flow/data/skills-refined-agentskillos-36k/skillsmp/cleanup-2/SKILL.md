---
name: cleanup
description: "Clean up completed work: inspect branches, update main, remove merged branches (local and optionally remote), reconcile beads, and produce a concise report. Trigger on queries like: 'clean up', 'tidy up', 'prune branches', 'housekeeping'."
---

# Cleanup Skill

Triggers
- "clean up"
- "tidy up"
- "cleanup"
- "housekeeping"

## Purpose
- Inspect repository branches and beads, identify merged or stale work, remove safely deletable branches, propose bead closures, and produce a concise report of actions and next steps.

## Required tools
- `git` (required)
- `bd` (beads CLI) — optional but recommended for bead metadata
- `gh` (GitHub CLI) — optional for PR summaries

## Runtime flags (recommended)
- `dry-run` (default): list actions without performing deletes or closes
- `confirm_all`: allow single confirmation to apply a group of safe actions
- `delete-remote` (opt-in): permit remote branch deletion when explicitly confirmed

## Preconditions & safety
- Never delete a remote branch or close a bead without explicit confirmation.
- Never rewrite history or force-push without explicit permission.
- Default protected branches: `main`, `master`, `develop` (do not delete or target for deletion).
- Detect default branch dynamically when possible (check `git remote show origin` or fallback to `main`).
- Use conservative merge checks (`git merge-base --is-ancestor`) to determine whether a branch's HEAD is contained in the default branch.

## High-level Steps

1) Inspect current branch
- Show current branch: `git rev-parse --abbrev-ref HEAD`.
- Detect default branch (recommended): `git remote show origin` and parse "HEAD branch". Fallback to `main`.
- If current branch is not the default branch:
  - Fetch remote: `git fetch origin --prune`.
  - Check whether current branch is merged into `origin/<default>`:
    - `git merge-base --is-ancestor HEAD origin/<default>` (exit code 0 => merged)
  - If not merged: present summary (branch name, last commit, unpushed commits, associated bead) and ask user: keep working / open PR / merge / skip deletion.
  - If merged and user permits (or in `confirm_all`), allow continuing to default branch.

2) Switch to default branch and update
- `git fetch origin --prune`.
- `git checkout <default>`.
- `git pull --ff-only origin <default>` (if fast-forward fails, report and ask).

3) Summarize open PRs targeting default
- If `gh` available: `gh pr list --state open --base <default> --json number,title,headRefName,url,author`.
- Present any open PRs and their head branches; skip deleting branches that have open PRs unless user explicitly authorizes.

4) Identify merged local branches
- List local branches merged into `origin/<default>` using conservative check per branch:
  - For each branch `b` (excluding protected names and current):
    - `git merge-base --is-ancestor b origin/<default>` (exit code 0 => merged)
- Present candidate list with metadata: last commit date, upstream (if any), bead id (if parseable), and open PR presence.
- Ask user to confirm deletion. If confirmed and not `dry-run`: `git branch -d <branch>` (safe delete). If `-d` fails, report and offer `-D` only with explicit permission.

5) Offer remote deletion (opt-in)
- For each deleted or candidate local branch with a remote `origin/<branch>`:
  - Verify no open PR references it and that it is merged (use `git merge-base --is-ancestor origin/<branch> origin/<default>`).
  - Present remote deletion candidates; ask per-branch or grouped confirmation based on `confirm_all`.
  - If confirmed and not `dry-run` and `delete-remote` enabled: `git push origin --delete <branch>`.

6) Summarize remaining branches
- Produce a table of remaining local and remote branches with: name, upstream, last commit, merged? (yes/no), bead id (if any), and open PR links (if available).
- For each remaining branch, offer actions: keep / delete / create PR / assign bead / rebase / merge.

7) Beads (bd) review
- Run `bd sync` to ensure bead data is current.
- If `bd` available: `bd list --status in_progress --json`.
- Cross-reference beads with branches found in the repo. For each in-progress bead, show last updated, linked branches, and recommend close if: bead's branch is merged and PRs/commits indicate completion or inactivity (configurable age threshold).
- For each bead use the status skill to evaluate their suitability for closure.
- Present candidate bead closures and ask for confirmation. If confirmed and not `dry-run`: `bd close <id> --reason "Completed" --json` then `bd sync`.
  - If there are no candidates, report none found.

8) Final report
- Produce concise report including:
  - Branches deleted (local + remote)
  - Branches kept and reasons
  - Beads closed
  - Any operations skipped or requiring manual intervention
- Offer to save report: `history/cleanup-report-<timestamp>.md` (write only with confirmation).

Branch ↔ Bead mapping
- Parse branch names for bead tokens using the project's convention: `<prefix>-<id>/...` (example: `bd-123/feature`).
- If found: `bd show <id> --json` to include title, status, priority, and comments.
- If not found: flag branch for manual review and present guidance for associating to a bead.

Commands (examples)
- Detect default: `git remote show origin` or `git symbolic-ref refs/remotes/origin/HEAD`.
- Conservative merge check: `git merge-base --is-ancestor <branch> origin/<default>`.
- List branches for manual checking: `git for-each-ref --format='%(refname:short) %(committerdate:iso8601)' refs/heads/`.
- PR summary: `gh pr list --state open --base <default> --json number,title,headRefName,url,author`.
- Beads: `bd list --status in_progress --json`, `bd show <id> --json`, `bd close <id> --reason "Completed" --json`, `bd sync`.

Safety prompts (always asked)
- Confirm local branch deletions with full list and dry-run preview.
- Confirm remote deletions per-branch or as a single group (if `confirm_all`).
- Confirm bead closures and show bead details (description, last comments, linked branches).
- If default branch cannot be fast-forwarded, ask how to proceed (pause or abort).

Suggested bundled resources (optional)
- `scripts/list-merged-branches.sh` — helper to produce a conservative list of merged branches using `git merge-base` (recommended to include in the skill if operations will be repeated).
- `references/branch-naming.md` — guide describing repo-specific branch naming and bead conventions.

Outputs
- Human-readable summary printed to terminal.
- Optional `history/cleanup-report-<timestamp>.md` written on confirmation.

Example short dialogue
- Agent: "I can inspect merged branches and propose deletions in dry-run mode. Shall I proceed? (yes/no)"
- User: "Yes — run dry-run and show candidates, do not delete remotes."
- Agent: "Dry-run complete. Candidate local deletions: A, B. Remote candidates: C. Would you like to delete local A, B? (yes/no)"

Notes for operators
- Skill assumes `bd` and `gh` may be available; proceed gracefully if not.
- Follow AGENTS.md bead/branch naming conventions. If conventions differ, flag branches for manual mapping.
- Do not create or modify commits, force-push, or change remote configuration without explicit permission.

End.
