---
name: git-worktree
description: Create a new Git worktree with a dedicated branch.
---

# Git Worktree

The following commands are available:

## Create a new branch and add a worktree
```bash
git wtab <branch-name>
```
- Create a new branch with the specified branch name and add a worktree
- The worktree is created at `../${repo_name}-worktree/${branch_name}`
- If `setup-project.sh` exists, it will be executed automatically

## Add an existing branch to a worktree
```bash
git wtac <branch-name>
```
- Add an existing branch (origin/<branch-name>) to a worktree
- The worktree is created at `../${repo_name}-worktree/${branch_name}`
- If `setup-project.sh` exists, it will be executed automatically

## Delete worktree and branch
```bash
git wtd <branch-name>
```
- Delete the worktree and also delete the branch (force delete with `-D`)
- The worktree is deleted from `../${repo_name}-worktree/${branch_name}`

