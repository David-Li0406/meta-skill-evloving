---
name: git-merge-linear
description: Use this skill to merge a task branch into its base branch with a linear history while remaining in the task worktree.
---

# Git Linear Merge Skill

Merge a task branch to its base branch while staying in the task worktree. This skill uses `git push . HEAD:<base>` to fast-forward the base branch without checking out.

## When to Use

- After the task branch has passed review and user approval.
- When merging a completed task to the base branch (e.g., main, v1.10).
- To maintain a clean, linear git history.

## Prerequisites

- [ ] User approval obtained.
- [ ] Working directory is clean (commit or stash changes).
- [ ] You are in the task worktree (not the main repo).

## Workflow

### Step 0: Read Git Workflow Preferences

Check the `PROJECT.md` for configured merge preferences before proceeding.

```bash
# Check if Git Workflow section exists in PROJECT.md
WORKFLOW_SECTION=$(grep -A30 "^## Git Workflow" .claude/cat/PROJECT.md 2>/dev/null)

if [[ -n "$WORKFLOW_SECTION" ]]; then
  # Check if linear merge is allowed by workflow config
  MERGE_METHOD=$(echo "$WORKFLOW_SECTION" | grep "MUST use" | head -1)

  if echo "$MERGE_METHOD" | grep -qi "merge commit"; then
    echo "⚠️ WARNING: PROJECT.md specifies merge commits, but this skill uses fast-forward."
    echo "Consider using standard 'git merge --no-ff' instead."
    echo ""
    echo "To proceed anyway, continue with this skill."
    echo "To honor PROJECT.md preference, abort and use: git merge --no-ff {branch}"
  fi

  if echo "$MERGE_METHOD" | grep -qi "squash"; then
    echo "⚠️ WARNING: PROJECT.md specifies squash merge, but this skill uses fast-forward."
    echo "Consider using 'git merge --squash' instead."
    echo ""
  fi
fi
```

### Step 1: Verify Location and Detect Base Branch

```bash
# Verify we're in a worktree (not main repo)
WORKTREE_PATH=$(pwd)
MAIN_REPO=$(git worktree list | head -1 | awk '{print $1}')

if [[ "$WORKTREE_PATH" == "$MAIN_REPO" ]]; then
  echo "ERROR: Must run from task worktree, not main repo"
  echo "Navigate to: /workspace/.worktrees/<task-name>"
  exit 1
fi

# Get current branch
TASK_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Detect base branch from worktree metadata (fail-fast if missing)
CAT_BASE_FILE="$(git rev-parse --git-dir)/cat-base"
if [[ ! -f "$CAT_BASE_FILE" ]]; then
  echo "ERROR: cat-base file not found: $CAT_BASE_FILE"
  echo "This worktree was not created properly. Recreate with /cat:work."
  echo "Or set manually: echo '<base-branch>' > \"$CAT_BASE_FILE\""
  exit 1
fi
BASE_BRANCH=$(cat "$CAT_BASE_FILE")

echo "Task branch: $TASK_BRANCH"
echo "Base branch: $BASE_BRANCH"
echo "Worktree: $WORKTREE_PATH"

# Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "ERROR: Uncommitted changes detected"
  echo "Commit or stash changes before merging"
  exit 1
fi
```

### Step 2: Squash Commits (if needed)

```bash
# Count commits ahead of base branch
COMMIT_COUNT=$(git rev-list --count "${BASE_BRANCH}..HEAD")
echo "Commits to merge: $COMMIT_COUNT"

if [[ "$COMMIT_COUNT" -eq 0 ]]; then
  echo "ERROR: No commits to merge"
  exit 1
fi

if [[ "$COMMIT_COUNT" -gt 1 ]]; then
  echo "Squashing $COMMIT_COUNT commits into 1..."

  # Get combined commit message from all commits
  COMBINED_MSG=$(git log --reverse --format="- %s" "${BASE_BRANCH}..HEAD")
  FIRST_MSG=$(git log -1 --format="%s" "${BASE_BRANCH}..HEAD" | head -1)

  # Soft reset to base and create single commit
  git reset --soft "$BASE_BRANCH"
  git commit -m "$FIRST_MSG

Changes:
```