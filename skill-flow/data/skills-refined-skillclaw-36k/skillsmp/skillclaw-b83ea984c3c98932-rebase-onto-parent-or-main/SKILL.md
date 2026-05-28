---
name: rebase-onto-parent-or-main
description: Use this skill when you need to rebase your branch onto an updated parent branch or main after the parent PR has been merged.
---

# Rebase Your Branch onto Parent or Main

Rebase your branch onto the main branch or an updated parent branch, ensuring that only your commits are retained.

## Usage

```
/rebase-onto-parent-or-main
/rebase-onto-parent-or-main feature/old-parent    # Specify the old parent branch
```

## Instructions

### 1. Understand the Situation

Determine if your branch is based on a parent branch that has been merged into main or if it needs to be rebased onto an updated parent branch.

### 2. Identify the Parent Branch

If not provided, check the current PR base:

```bash
# Get current branch
git branch --show-current

# Check PR base branch
gh pr view --json baseRefName --jq '.baseRefName'
```

If the base is `main`, proceed with rebasing onto main. If the base is an old parent branch, confirm the branch with the user.

### 3. Check Current State

Ensure there are no uncommitted changes:

```bash
git status --porcelain
```

Stash or commit any uncommitted changes before proceeding.

### 4. Fetch Latest Changes

Fetch the latest changes from the remote:

```bash
git fetch origin
```

### 5. Find Your Commits

Identify which commits are uniquely yours:

```bash
# List commits on your branch not in main or the updated parent
git log origin/main..HEAD --oneline
```

### 6. Rebase onto Main or Updated Parent

If the parent has been merged into main:

```bash
git rebase origin/main
```

If rebasing onto an updated parent branch:

```bash
# Use --onto to rebase only your commits onto the new parent
git rebase --onto origin/{parent-branch} $(git merge-base HEAD origin/{parent-branch}) HEAD
```

If conflicts occur, resolve them as follows:

1. List conflicting files: `git diff --name-only --diff-filter=U`
2. Resolve each conflict
3. Stage resolved files: `git add {file}`
4. Continue the rebase: `git rebase --continue`

### 7. Force Push

After a successful rebase, force push your changes:

```bash
git push --force-with-lease
```

### 8. Update PR Base (if needed)

If the PR base branch needs updating, run:

```bash
gh pr edit --base main  # or gh pr edit --base {parent-branch}
```

### 9. Report Result

Inform the user of the outcome:
- Successfully rebased onto main or the updated parent branch
- Updated PR to target the correct base
- X commits remain after rebase
- Force pushed to origin