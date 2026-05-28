---
name: git-worktree-management
description: Use this skill to create, manage, scan, and clean up git worktrees for parallel development and isolated feature work.
---

# Managing Git Worktrees

This skill automates the management of git worktrees, allowing for parallel development and feature isolation. Use the `/worktree` command to invoke this skill.

## Agent Delegation

This skill delegates to specialized agents via the **Task tool**:

| Operation | Agent | Returns |
|-----------|-------|---------|
| Create | `sc-worktree-create` | JSON: success, path, branch, tracking_row |
| Scan | `sc-worktree-scan` | JSON: success, worktrees list, recommendations |
| Cleanup | `sc-worktree-cleanup` | JSON: success, branch_deleted, tracking_update |
| Abort | `sc-worktree-abort` | JSON: success, worktree_removed, tracking_update |

To invoke an agent, use the Task tool with:
- Prompt file: `.claude/agents/<agent-name>.md`
- Parameters as documented in each agent's Inputs section

## Standards and Paths
- Repo root: current directory.
- Default worktree base: `../<REPO_NAME>-worktrees`.
- Worktrees live in `<worktree_base>/<branch>`.
- Tracking document (if used): `<worktree_base>/worktree-tracking.md` must be updated on create/scan/cleanup/abandon. Allow a toggle to disable tracking for repos that don’t use it.
- Naming: worktree directory = branch name; branch naming follows repo policy (e.g., master release; develop/DevBranch integration; feature from integration; hotfix from master; release branches as needed).
- Branch protections/hooks: no direct commits to protected branches; ensure hooks/branch protections are respected across worktrees.
- Cleanliness: worktrees must be removed and tracking updated when work is complete or branch is merged.

## Workflows

### Scaffolding (if missing)
- Ensure base path exists: `<worktree_base>`. If missing, create it.
- If tracking is enabled, ensure tracking doc exists with headers.

### Create Worktree (and Branch)
1) Inputs: `--branch <name>`, `--base <master|develop|...>`, optional `--path`.
2) Ensure scaffolding/tracking doc exists (if enabled); fetch all: `git fetch --all --prune`.
3) Confirm base branch exists and is up to date.
4) Determine path: default `<worktree_base>/<branch>` (or override).
5) Create branch/worktree:
   - If branch does not yet exist: `git worktree add -b <branch> <path> <base>`.
   - If branch exists: `git worktree add <path> <branch>`.
6) In the new worktree, ensure hooks apply and verify status is clean.
7) If tracking enabled, add/refresh entry in tracking doc (branch, path, base, purpose, owner, created date, status).
8) Agent option: delegate to `sc-worktree-create` agent; it returns structured JSON (tracking row, status).

### Scan/Verify Worktrees
1) List worktrees: `git worktree list --porcelain`.
2) Cross-check tracking doc (if enabled); flag missing/stale entries or extra rows.
3) For each worktree, check status and merge state:
   - `git -C <path> status --short`
   - `git -C <path> fetch`
   - `git branch --remotes --contains <branch>` to see if merged.
4) Identify issues: untracked changes, diverged branches, merged-but-not-cleaned worktrees, missing tracking entries.
5) Update tracking doc with current state and issues (if enabled); propose cleanup where appropriate.
6) Agent option: delegate to `sc-worktree-scan` agent; it returns structured JSON.

### Clean-Up Worktree (Post-Merge or Finished Work)
1) If `git status` is not clean, stop and request explicit approval/coordination.
2) Ensure all work is committed/pushed or explicitly confirmed to discard.
3) Confirm target branch merged or otherwise approved for removal.
4) Remove worktree: `git worktree remove <path>` (use `--force` only with approval).
5) If merged and no unique commits, delete the branch locally (`git branch -d <branch>`) and remotely (`git push origin --delete <branch>`) by default; only skip if the user explicitly opts out. If the remote branch is already absent, continue without error. If not merged, only delete with explicit approval.
6) If tracking enabled, update tracking doc to remove/mark cleaned with merge SHA/date.
7) Agent option: delegate to `sc-worktree-cleanup` agent; it returns structured JSON.

### Abandon Worktree (Discard Work)
1) If `git status` is not clean, stop and request explicit approval/coordination.
2) Confirm user approval to discard local changes and optionally delete the branch.
3) Remove worktree: `git worktree remove <path>` (force only with approval).
4) If instructed, delete the branch locally (`git branch -D <branch>`) and remotely (`git push origin --delete <branch>`).
5) If tracking enabled, update tracking doc to remove the entry and note abandonment.
6) Agent option: delegate to `sc-worktree-abort` agent; it returns structured JSON.

### Update Protected Branch (Pull Latest Changes)
1) **Verify branch is protected**: Only operates on branches in protected_branches list. If no branch is specified, update all protected branches that have worktrees.
2) Check if worktree exists at expected path; error if missing.
3) If `git status` is not clean, stop and report dirty state.
4) Fetch and pull: `git fetch origin <branch>` then `git pull origin <branch>`.
5) **If merge conflicts occur**:
   - Collect conflicted files: `git diff --name-only --diff-filter=U`
   - Return control to main agent with conflict details
   - Main agent coordinates with user to resolve conflicts
   - After resolution, user commits and continues
6) **If clean pull**: Update tracking with last_checked timestamp and commits pulled count.
7) Agent option: delegate to `sc-worktree-update` agent; it returns structured JSON with success or conflict details.

## Safety and Reminders
- **NEVER delete protected branches** (main, develop, master) under any circumstances.
- Protected branches can only be removed from worktrees; the branch itself must always be preserved.
- Never delete branches or force-remove worktrees without explicit approval.
- Never clean/abandon a worktree with uncommitted changes unless explicitly approved.
- Keep tracking doc in sync on every operation when enabled.
- Respect branch protections and hooks; no direct commits to protected branches.
- Use background agents for long scans/cleanups; keep the main context focused on decisions and summaries.

## Commands
### Create Worktree
```
/worktree create <feature-name>
```

### List Worktrees
```
/worktree list
```

### Remove Worktree
```
/worktree remove <name>
```

### Status
```
/worktree status
```

## Directory Structure
```
project/
├── .worktrees/           # All worktrees live here
│   ├── auth-feature/     # Isolated worktree
│   └── api-refactor/     # Another worktree
├── .gitignore           # Should include .worktrees/
└── ...
```

## Environment Files
These files are copied to new worktrees if they exist:
| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `.env.local` | Local overrides |
| `.env.development` | Development config |
| `.nvmrc` | Node version |
| `.node-version` | Node version (alternative) |
| `.npmrc` | npm configuration |
| `.tool-versions` | asdf version manager |

## Behavior Rules
### MUST DO
- Create worktrees under `.worktrees/` directory
- Add `.worktrees/` to `.gitignore` automatically
- Copy environment files to new worktrees
- Run package install in new worktrees
- Confirm before removing worktrees

### MUST NOT
- Create worktrees outside `.worktrees/`
- Force delete branches without confirmation
- Leave orphaned worktrees

## Error Handling
### Error: Branch Already Exists
### Error: Worktree Directory Already Exists
### Error: Package Install Fails
### Error: Disk Space Insufficient
### Error: Invalid Worktree Name
### Error: Worktree Locked

## Cleanup Instructions for Partial Failures
If worktree creation fails partway through, clean up in reverse order:
```bash
# 1. Remove node_modules if install started
# 2. Remove the worktree directory
# 3. Prune worktree references
# 4. Delete the branch if it was created
# 5. Verify clean state
```

**Automated cleanup function:**
```bash
cleanup_failed_worktree() {
    local name="$1"
    rm -rf ".worktrees/${name}/node_modules" 2>/dev/null
    git worktree remove ".worktrees/${name}" --force 2>/dev/null || rm -rf ".worktrees/${name}"
    git worktree prune
    git branch -D "feat/${name}" 2>/dev/null
    echo "Cleaned up failed worktree: ${name}"
}
```