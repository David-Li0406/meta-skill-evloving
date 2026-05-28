---
name: git
description: Git operations, conflict resolution, history management, and Git workflows. Use for complex Git operations and version control tasks.
allowed-tools: Bash
---

# Git Skill

Advanced Git operations and workflows.

## 1. Branch Management

```bash
# Create and switch branch
git checkout -b feature/new-feature

# Rename branch
git branch -m old-name new-name

# Delete branch
git branch -d feature-branch  # Safe delete
git branch -D feature-branch  # Force delete

# List branches
git branch -a  # All branches
git branch -r  # Remote branches
```

## 2. Commit Management

```bash
# Amend last commit
git commit --amend -m "New message"

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Cherry-pick commit
git cherry-pick <commit-hash>

# Revert commit
git revert <commit-hash>

# Reset (careful!)
git reset --soft HEAD~1  # Keep changes staged
git reset --mixed HEAD~1  # Keep changes unstaged
git reset --hard HEAD~1  # Discard changes
```

## 3. Conflict Resolution

```bash
# During merge conflict
git status  # See conflicted files

# Edit conflicted files, then:
git add <resolved-file>
git commit

# Abort merge
git merge --abort

# Use specific version
git checkout --ours <file>    # Keep your changes
git checkout --theirs <file>  # Use their changes
```

## 4. Stash Operations

```bash
# Stash changes
git stash save "work in progress"

# List stashes
git stash list

# Apply stash
git stash apply stash@{0}
git stash pop  # Apply and remove

# Drop stash
git stash drop stash@{0}

# Create branch from stash
git stash branch new-branch
```

## 5. History and Search

```bash
# View history
git log --oneline --graph --all
git log --author="name"
git log --since="2 weeks ago"

# Search commits
git log --grep="bug fix"
git log -S "function_name"  # Search code changes

# Show changes
git show <commit-hash>
git diff HEAD~1 HEAD

# Find when bug introduced
git bisect start
git bisect bad  # Current is bad
git bisect good <commit-hash>  # Test and mark
git bisect reset
```

## 6. Remote Operations

```bash
# Add remote
git remote add origin https://github.com/user/repo.git

# Fetch and pull
git fetch origin
git pull origin main

# Push
git push origin feature-branch
git push -u origin feature-branch  # Set upstream

# Delete remote branch
git push origin --delete feature-branch
```

## 7. Workflows

**Feature Branch Workflow:**
```bash
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
# Create PR, then merge
```

**Git Flow:**
```bash
# Start feature
git checkout -b feature/name develop

# Finish feature
git checkout develop
git merge --no-ff feature/name
git branch -d feature/name

# Start release
git checkout -b release/1.0.0 develop
# ... prepare release ...
git checkout main
git merge --no-ff release/1.0.0
git tag -a 1.0.0
git checkout develop
git merge --no-ff release/1.0.0
```

## 8. Useful Aliases

```bash
# Add to ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    lg = log --oneline --graph --all --decorate
```

## 9. Cleanup

```bash
# Remove untracked files
git clean -fd

# Prune remote branches
git remote prune origin

# Delete merged branches
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d
```

## When to Use This Skill

Use `/git` for complex Git operations, conflict resolution, and version control workflows.
