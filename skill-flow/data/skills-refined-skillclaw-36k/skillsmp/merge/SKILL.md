---
name: merge
description: |
  Branch merging and conflict resolution patterns.
  Use when merging feature branches, handling conflicts, or cleaning up worktrees.
  Trigger with "merge branch", "resolve conflicts", "cleanup worktree".
model: haiku
allowed-tools: Bash, Read
---

# Merge - Branch Management

Patterns for merging worker branches and handling conflicts.

**CRITICAL**: Always kill the worker terminal BEFORE merging. See @references/terminal-cleanup.md

## Standard Merge Flow

```bash
ISSUE_ID="ISSUE-ID"
TABZ_API="http://localhost:8129"
TOKEN=$(cat /tmp/tabz-auth-token)

# 1. Kill worker terminal first
AGENT_ID=$(curl -s "$TABZ_API/api/agents" | jq -r --arg id "$ISSUE_ID" \
  '.data[] | select(.name == $id) | .id')
[ -n "$AGENT_ID" ] && curl -s -X DELETE "$TABZ_API/api/agents/$AGENT_ID" \
  -H "X-Auth-Token: $TOKEN"

# 2. Ensure on main
git checkout main
git pull

# 3. Merge feature branch
git merge "feature/$ISSUE_ID" --no-edit

# 4. Remove worktree and branch
git worktree remove ".worktrees/$ISSUE_ID" --force
git branch -d "feature/$ISSUE_ID"

# 5. Sync and push
bd sync
git push
```

## One-Command Alternative

For full cleanup with checkpoints, capture, and terminal kill:

```bash
./plugins/conductor/scripts/finalize-issue.sh "$ISSUE_ID"
```

## Conflict Detection

```bash
# Test merge without committing
git merge --no-commit --no-ff "feature/$ISSUE_ID"
git merge --abort
```

If conflicts exist, `git merge` will fail with conflict markers.

## Conflict Resolution

**Don't auto-resolve.** Report conflicts for manual resolution:

```bash
# Get conflict files
git diff --name-only --diff-filter=U

# Show conflict details
git diff --check
```

### Manual Resolution Steps

1. Navigate to worktree: `cd .worktrees/ISSUE-ID`
2. Open conflicting files
3. Resolve conflicts (remove markers, choose correct code)
4. Stage: `git add .`
5. Commit: `git commit`
6. Re-run cleanup

## Merge Strategies

### Fast-Forward (Clean history)
```bash
git merge --ff-only "feature/$ISSUE_ID"
```
Only works if main hasn't changed.

### No-FF (Always create merge commit)
```bash
git merge --no-ff "feature/$ISSUE_ID"
```
Creates merge commit even if fast-forward possible.

### Squash (Single commit)
```bash
git merge --squash "feature/$ISSUE_ID"
git commit -m "feat: description (ISSUE-ID)"
```
Combines all commits into one.

**Default**: Use `--no-edit` for automatic merge commit message.

## Worktree Cleanup

```bash
# Remove worktree (--force ignores uncommitted changes)
git worktree remove ".worktrees/ISSUE-ID" --force

# List remaining worktrees
git worktree list

# Prune stale worktree references
git worktree prune
```

## Branch Cleanup

```bash
# Delete local branch (fails if not merged)
git branch -d "feature/ISSUE-ID"

# Force delete (use carefully)
git branch -D "feature/ISSUE-ID"

# Delete remote branch
git push origin --delete "feature/ISSUE-ID"
```

## Batch Operations

```bash
# Find all merged feature branches
git branch --merged main | grep "feature/"

# Delete all merged feature branches
git branch --merged main | grep "feature/" | xargs git branch -d

# Find orphaned worktrees
git worktree list | grep -v "$(pwd)$"
```

## Error Handling

| Error | Action |
|-------|--------|
| Merge conflict | Stop, report files, require manual resolution |
| Branch not found | Skip branch deletion |
| Worktree not found | Skip worktree removal |
| Not on main | Checkout main first |
| Uncommitted changes | Stash or warn |
| TabzChrome not running | Skip terminal kill, continue with merge |
| No auth token | Skip terminal kill, continue with merge |

## Safety Checks

Before merging:
1. Verify issue is closed
2. **Kill worker terminal via TabzChrome API** (see @references/terminal-cleanup.md)
3. Verify branch exists
4. Check for conflicts first

After merging:
1. Verify merge succeeded
2. Run any CI checks
3. Sync beads
4. Push to remote
