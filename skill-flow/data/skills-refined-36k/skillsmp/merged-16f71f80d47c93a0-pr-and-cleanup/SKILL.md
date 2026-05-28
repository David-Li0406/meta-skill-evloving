---
name: pr-and-cleanup
description: Use this skill to automate the creation of a Pull Request (PR) and cleanup of the worktree environment after completing development.
---

# PR and Cleanup Skill

This skill automates the process of creating a Pull Request (PR) and cleaning up the worktree environment after development is complete.

## Overview

The skill performs the following actions automatically:

1. Detects the current worktree directory and branch.
2. Checks for uncommitted changes.
3. Creates a PR on GitHub.
4. Deletes the worktree after a successful PR creation.
5. Switches back to the main branch (repository root).

**Important**: Local and remote branches will remain intact.

## Usage

### Basic Usage

```bash
# Execute within the worktree directory
cd .worktrees/<feature-name>
bash ../../.claude/skills/pr-and-cleanup/scripts/pr_and_cleanup.sh
```

### Options

```bash
# Create PR only (do not delete worktree)
bash pr_and_cleanup.sh --pr-only

# Cleanup only (if PR has already been created)
bash pr_and_cleanup.sh --cleanup-only

# Specify title and body in advance
bash pr_and_cleanup.sh --title "<title>" --body "<description>"

# Create as a draft PR
bash pr_and_cleanup.sh --draft
```

## Prerequisites

- Must be executed within the worktree directory.
- All changes must be committed.
- `gh` CLI must be installed and authenticated.

## Steps

### 1. Verify Environment

Check the current state:

```bash
# Ensure execution within the worktree
git worktree list | grep "$(pwd)"

# Check current branch
git branch --show-current

# Check for uncommitted changes
git status --short
```

### 2. Check for Uncommitted Changes

Detect if there are any changes:

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️ Uncommitted changes detected"
  git status
  # Prompt user for action
fi
```

**Options:**
- Commit changes before proceeding.
- Discard changes and continue (using `--force` option).
- Cancel the operation.

### 3. Ensure Changes are Pushed

Check for unpushed commits:

```bash
if [ -n "$(git log @{u}.. 2>/dev/null)" ]; then
  echo "⚠️ Unpushed commits detected"
  # Confirm whether to push automatically
fi
```

### 4. Create Pull Request

Create a PR using the GitHub CLI:

```bash
# Basic PR creation (interactive)
gh pr create

# Or specify title and description
gh pr create --title "<title>" --body "<description>"

# Create as a draft PR
gh pr create --draft

# Specify base branch
gh pr create --base <base-branch>
```

### 5. Clean Up Worktree

After a successful PR creation, delete the worktree:

```bash
# Get current worktree path
WORKTREE_PATH=$(git worktree list | grep "$(git branch --show-current)" | awk '{print $1}')

# Move to the base directory (repository root)
REPO_ROOT=$(git rev-parse --show-toplevel)

# Checkout the main branch (or specified branch)
cd "$REPO_ROOT"
git checkout main  # or develop, etc.

# Remove the worktree
git worktree remove "$WORKTREE_PATH"
```

### 6. Report Status

After completion, provide the following information to the user:

```markdown
✅ PR creation and cleanup completed

**PR URL:** <pr-url>
**Deleted worktree:** <worktree-path>
**Current branch:** main

**Next Steps:**
1. Request PR review.
2. Check CI/CD results.
3. Address review comments.
4. Merge when ready.

**Useful Commands:**
- `gh pr view` - View the current branch's PR.
- `gh pr checks` - Check CI/CD status.
- `gh pr merge` - Merge the PR (after approval).
```

### 7. Handle Edge Cases

#### Case 1: Create PR only (keep worktree)

```bash
# Use --pr-only option
./pr_and_cleanup.sh --pr-only
```

#### Case 2: Cleanup only (PR already created)

```bash
# Use --cleanup-only option
./pr_and_cleanup.sh --cleanup-only
```

#### Case 3: Force execution (ignore uncommitted changes)

```bash
# Use --force option (not recommended)
./pr_and_cleanup.sh --force
```

## Key Principles

1. **Safety First**: Warn if there are uncommitted changes.
2. **Flexibility**: Allow separate execution of PR creation and cleanup.
3. **Transparency**: Clearly report all actions to the user.
4. **Reversibility**: Branches are not deleted, allowing for restoration if needed.

## Customization Options

Users may customize the following:

- **Base Branch**: The target branch for the PR (e.g., `main`, `develop`, `staging`).
- **Return Branch**: The branch to checkout after cleanup.
- **PR Template**: Use a custom template for the PR.
- **Branch Deletion**: Whether to delete remote branches as well.

## Dependencies

- Git 2.5+ (support for worktree functionality).
- GitHub CLI (`gh`) - required for PR creation.
  ```bash
  # Installation
  brew install gh

  # Authentication
  gh auth login
  ```

## Integration with Other Skills

- **create-worktree**: Cleanup of worktrees created by this skill.
- **code-review**: Conduct code reviews after PR creation.

## Best Practices

1. **Confirm Completion**: Ensure all changes are committed before PR creation.
2. **Check CI/CD**: Immediately check CI/CD status after PR creation.
3. **Organize Branches**: Regularly delete merged branches.
4. **Utilize Draft PRs**: Share progress using draft PRs during development.

## Common Issues and Solutions

### Issue 1: GitHub CLI not authenticated

```
error: authentication required
```

**Solution**: Authenticate using GitHub CLI.

```bash
gh auth login
# Authenticate via browser or token.
```

### Issue 2: Failed to execute from worktree directory

```
fatal: cannot remove path when it is in the current directory
```

**Solution**: The script automatically moves to the repository root before deletion.

### Issue 3: Remote branch does not exist

```
error: branch 'feature/xxx' has no upstream branch
```

**Solution**: Push to remote first.

```bash
git push -u origin $(git branch --show-current)
```

### Issue 4: Base branch not found during PR creation

**Solution**: Explicitly specify the base branch.

```bash
gh pr create --base <base-branch>
```

## Advanced Options

### Delete branches as well

After PR creation and cleanup, delete local and remote branches:

```bash
# Execute after PR merge
gh pr merge --auto --squash
git worktree remove <worktree-path>
git branch -D <branch-name>
git push origin --delete <branch-name>
```

### Bulk cleanup of multiple worktrees

```bash
# List all worktrees
git worktree list

# Remove unnecessary worktrees
git worktree remove <path1>
git worktree remove <path2>

# Clean up stale worktrees
git worktree prune
```

## Notes

- Deleting the worktree does not remove the branch, allowing for recreation if needed.
- Automate branch deletion after PR merge via GitHub settings.
- `gh pr create` automatically uses the repository's PR template.
- Draft PRs can be converted to regular PRs later.