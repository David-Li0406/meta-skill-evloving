---
name: git-wt
description: Guide for using git-wt to manage isolated git worktrees. Use this for all code modification tasks to ensure a clean, safe, and disposable environment.
---

# git-wt Skill

`git-wt` is a wrapper around `git worktree` that simplifies creating isolated workspaces.

## Core Mandate: Safety First

**ALWAYS** use `git-wt` for creating new features, fixing bugs, or experimenting.
1.  **Isolate**: Create a new worktree for every task.
2.  **Context**: Work *only* inside the new worktree directory.
3.  **Cleanup**: Delete the worktree immediately after pushing changes or submitting a PR.

## Workflow

### 1. Create Worktree
Run this command to start a task. Always use `--copyignored` to ensure `.env` and local configs are copied.

```bash
git wt <new-branch-name> --copyignored
```

**CRITICAL:** The command will output the **absolute path** to the new worktree (e.g., `/path/to/project-wt/new-branch-name`).
You **MUST** use this path as the `workdir` for all subsequent `bash` commands and as the base for file operations (`read`, `edit`, `write`). Do not continue working in the original directory.

### 2. Work in Isolation
Perform all your edits, tests, and commits inside the new directory.

### 3. Push and PR
Push your branch to the remote.
```bash
# inside the worktree
git push -u origin <new-branch-name>
```
(Or use `gh pr create` if instructed).

### 4. Cleanup
Once the code is pushed or the PR is created, delete the local worktree to save space.
```bash
# Run this from the ORIGINAL directory, or any other directory (not inside the one being deleted)
git wt -d <new-branch-name>
```

## Command Reference

| Goal | Command |
| :--- | :--- |
| **List Worktrees** | `git wt` |
| **Start Task** | `git wt <branch> --copyignored` |
| **Start from Base** | `git wt <branch> origin/main --copyignored` |
| **Delete (Safe)** | `git wt -d <branch>` (Prevents deleting unmerged work) |
| **Delete (Force)** | `git wt -D <branch>` (Use if you want to discard changes) |
