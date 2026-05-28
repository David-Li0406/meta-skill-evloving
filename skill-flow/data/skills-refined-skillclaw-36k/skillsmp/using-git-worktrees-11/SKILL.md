---
name: using-git-worktrees
description: You are an expert user of git worktrees.  You interact with git worktrees to implement tasks.
---

# Using Git Worktrees Skill

This skill guides interaction with git worktrees, you will you the git cli for working with worktrees.

## Reference help for 'git worktree' command

```bash
git worktree add [-f] [--detach] [--checkout] [--lock [--reason <string>]]
                        [-b <new-branch>] <path> [<commit-ish>]
   or: git worktree list [-v | --porcelain [-z]]
   or: git worktree lock [--reason <string>] <worktree>
   or: git worktree move <worktree> <new-path>
   or: git worktree prune [-n] [-v] [--expire <expire>]
   or: git worktree remove [-f] <worktree>
   or: git worktree repair [<path>...]
   or: git worktree unlock <worktree>
```

## IMPORTANT Using A Git Worktree with Submodules

There are some important considerations when using a git worktree with a project that has submodules:

How They Work Together

1. Submodules are repository-wide: Submodules are tracked in the main repository's .git/modules/ directory, which is shared across all worktrees. This means all worktrees see the same submodule repositories.
2. Each worktree can check out different submodule commits: While the submodule repositories themselves are shared, each worktree can have the submodule checked out at different commits, just like any other file in the repository.
3. Initialization required per worktree: When you create a new worktree, you'll need to run git submodule update --init in that worktree to populate the submodule directories.

Common Workflow

1. Create a new worktree (e.g. git worktree add ../my-worktree branch-name)
2. Navigate to the new worktree (e.g. cd ../my-worktree)
3. Initialize and update submodules (e.g. git submodule update --init --recursive)

Potential Issues

- Detached HEAD states: Submodules in worktrees can sometimes end up in detached HEAD states, requiring manual checkout
- Nested worktrees: You cannot create a worktree inside a submodule's directory
- Update carefully: When updating submodules, be aware that changes affect the shared submodule repository.

## Using Git Worktrees Workflow

1. Create the worktree.
2. Navigate to the worktree folder.
3. Check for the usage of git submodules by checking for a .gitmodules file.
4. Initialize and update submodules.

## Using Git Worktrees Notes

- Executing scripts in a git worktree may require one "cd" before calling the script and then another "cd" after to return to the original directory. E.g. cd /private/tmp/claude/graphlessdb-issue-164 && git pull origin main && cd /users/blah/github/graphlessdb.  Put another way you will need to cd into the worktree folder before each execution of a script and then you will need to cd back to the original folder to reset the pwd back to what it was before.
- Check for existing branches before creating one. Use `git worktree add <path> <existing-branch>` if branch exists, not -b flag
- Create new git worktrees under the folder /tmp/claude/.
