---
name: git-worktree-management
description: Use this skill when you need to create, list, or manage git worktrees for parallel development, enabling multiple Claude Code sessions on different branches without conflicts.
---

# Git Worktree Management Skill

## Overview

This skill allows you to manage git worktrees, enabling parallel development workflows with Claude Code. You can create new worktrees for different branches, list existing worktrees, and remove them after merging.

## Commands

### Create a Worktree

When the user requests to create a new worktree, follow these steps:

1. **Check Current State**:
   - Run the following commands to gather context:
     ```bash
     pwd
     git rev-parse --show-toplevel
     git branch --show-current
     git branch -a --format='%(refname:short)'
     git worktree list
     ```

2. **Determine Branch**:
   - If a branch name is specified, use it directly.
   - If no branch is specified:
     - If on a feature/bugfix branch (not master/main/develop), use the current branch.
     - If on master/main/develop, prompt the user to specify a branch.

3. **Generate Path Slug**:
   - Create a slug for the worktree path based on the branch name, following these rules:
     - Strip common prefixes (e.g., `feature/`, `bugfix/`).
     - Extract distinctive keywords and combine them into a short slug (4-12 characters).

4. **Create the Worktree**:
   - Use the following command to create the worktree:
     ```bash
     git worktree add -b <branch-name> <worktree-path>
     ```
   - Install dependencies if necessary:
     ```bash
     cd <worktree-path> && npm install
     ```

5. **Output Success Message**:
   - If using tmux, open a new window:
     ```bash
     tmux new-window -c "<absolute-path>" -n "<branch-name>" "claude; bash"
     ```
   - If not in tmux, provide instructions to start a session:
     ```
     Worktree created successfully! To start a parallel Claude Code session, run:
     cd <absolute-path> && claude
     ```

### List Worktrees

When the user requests to list worktrees, run:
```bash
git worktree list
```
Format the output to show each worktree's branch and status.

### Remove a Worktree

When the user requests to finish or remove a worktree:
1. Check the current branch and ensure there are no uncommitted changes.
2. Merge the branch into main if necessary:
   ```bash
   git fetch origin main
   git rebase origin/main
   git checkout main
   git merge <branch>
   ```
3. Remove the worktree:
   ```bash
   git worktree remove <worktree-path>
   ```

## Important Rules

- Always check `.gitignore` before creating worktrees.
- Avoid direct work on main/master branches.
- Recommend using independent Claude sessions for each worktree.
- Regularly merge main to prevent divergence.

## Best Practices

- Manage 3-5 worktrees simultaneously for effective parallel development.
- Number terminal tabs for easy management of multiple sessions.
- Clean up merged worktrees to maintain organization.