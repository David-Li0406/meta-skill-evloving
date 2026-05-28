---
name: rebase-branch
description: Use this skill to rebase your current branch onto an updated parent branch or main after the parent PR has been merged.
---

# Rebase Current Branch

Rebase your current branch onto an updated parent branch or main after the parent PR has been merged.

## Usage

```
/rebase-branch
/rebase-branch <parent-branch>    # Specify the parent branch if needed
```

## Instructions

### 1. Understand the Situation

Determine if your branch is based on a parent branch that has been updated or merged. You need to:
- Rebase onto the updated parent or main
- Keep only YOUR commits (not the parent's commits)

### 2. Identify the Parent Branch

If not provided, try to determine the parent:

```bash
# Get current branch
git branch --show-current

# Check PR base branch
gh pr view --json baseRefName --jq '.baseRefName'
```

If the base is `main`, and the parent has been merged, you will need to rebase onto main.

### 3. Check Current State

```bash
git status --porcelain
git branch --show-current
```

Stash or commit uncommitted changes before proceeding.

### 4. Fetch Latest Changes

Fetch the latest changes from the parent branch or main:

```bash
git fetch origin <parent-branch>  # or main if applicable
```

### 5. Find Your Commits

Identify which commits are uniquely yours (not from the merged or updated parent):

```bash
# List commits on your branch not in main or the parent
git log origin/<parent-branch>..HEAD --oneline
```

### 6. Rebase onto the Updated Parent or Main

If the parent has been merged into main, rebase onto main:

```bash
git rebase origin/main
```

If rebasing onto an updated parent branch:

```bash
git rebase --onto origin/<parent-branch> $(git merge-base HEAD origin/<parent-branch>) HEAD
```

If that doesn't work cleanly, consider an interactive rebase:

```bash
git rebase -i origin/<parent-branch>
```

### 7. Handle Conflicts

If conflicts occur:

1. List conflicting files: `git diff --name-only --diff-filter=U`
2. Resolve each conflict
3. Stage resolved files: `git add {file}`
4. Continue: `git rebase --continue`

If stuck, abort and ask for guidance: `git rebase --abort`

### 8. Force Push

After a successful rebase, force push your changes:

```bash
git push --force-with-lease
```

### 9. Update PR Base (if needed)

If the PR base branch needs updating:

```bash
gh pr edit --base <parent-branch>  # or main if applicable
```

### 10. Report Result

Inform the user:
- Successfully rebased onto the updated parent or main
- Conflicts resolved (if any)
- Force pushed to origin