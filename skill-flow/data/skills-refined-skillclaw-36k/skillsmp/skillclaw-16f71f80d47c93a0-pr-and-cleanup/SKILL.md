---
name: pr-and-cleanup
description: Use this skill when you want to automate the process of creating a Pull Request and cleaning up your worktree after completing development in a worktree environment.
---

# Skill body

This skill automates the following steps after completing work in a worktree:

1. Verify the current worktree directory and branch.
2. Check for uncommitted changes and warn the user if any are detected.
3. Create a Pull Request (PR) on GitHub.
4. If the PR is created successfully, delete the worktree.
5. Switch back to the main branch (or specified branch).

## Instructions

### 1. Verify Environment

Ensure you are in the correct worktree:

```bash
# Check if in the correct worktree
git worktree list | grep "$(pwd)"
```

### 2. Check for Uncommitted Changes

Verify if there are any uncommitted changes:

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️ Uncommitted changes detected"
  git status
  # Prompt user for action
fi
```

### 3. Create Pull Request

Create a Pull Request using the GitHub CLI:

```bash
# Basic PR creation
gh pr create

# Or specify title and body
gh pr create --title "feat: Add new feature" --body "Detailed description..."

# Create as a draft
gh pr create --draft
```

### 4. Clean Up Worktree

After a successful PR creation, clean up the worktree:

```bash
# Get the current worktree path
WORKTREE_PATH=$(git worktree list | grep "$(git branch --show-current)" | awk '{print $1}')

# Switch to the main branch
git checkout main  # or another specified branch

# Remove the worktree
git worktree remove "$WORKTREE_PATH"
```

### 5. Report Status

After completion, provide the user with the following information:

```markdown
✅ PR creation and cleanup completed

**PR URL:** <pr-url>
**Deleted worktree:** <worktree-path>
**Current branch:** main
```

### 6. Handle Options

#### PR Creation Only

To create a PR without deleting the worktree:

```bash
./pr_and_cleanup.sh --pr-only
```

#### Cleanup Only

To clean up the worktree after a PR has been created:

```bash
./pr_and_cleanup.sh --cleanup-only
```

## Prerequisites

- Ensure you are executing this in the worktree directory.
- All changes must be committed.
- The `gh` CLI must be installed and authenticated.