---
name: parallel-worktree
description: |
  Git worktree workflow for parallel development.
  Start new features or bug fixes in isolated worktrees,
  enabling multiple Claude sessions to run simultaneously.
  Use when: starting new feature development, needing parallel work,
  or managing worktree creation/listing/completion.
---

# Parallel Worktree Development

Git worktree parallel development workflow skill.
Inspired by Boris Cherny's workflow and Claude Code Desktop features.

## Operations

### Create New Worktree

When user requests "create a new worktree", "start working on feature-xxx", etc.:

1. Check if `.gitignore` contains `.worktree/`
   - If not, suggest adding it
2. Confirm branch name (ask if not specified)
3. Create worktree:
   ```bash
   git worktree add .worktree/<branch> -b <branch>
   ```
4. Install dependencies and verify build:
   ```bash
   cd .worktree/<branch> && pnpm install && pnpm build
   ```
5. On success, present the command to start a new terminal session:
   ```
   cd .worktree/<branch> && claude
   ```

### List Worktrees

When user requests "list worktrees", "show parallel sessions", etc.:

```bash
git worktree list
```

Format the output nicely and explain each worktree's branch and status.

### Finish Worktree

When user requests "finish worktree", "merge this work", etc.:

1. Check current branch
2. If there are uncommitted changes, suggest committing
3. Fetch latest main and rebase:
   ```bash
   git fetch origin main
   git rebase origin/main
   ```
4. Checkout main and merge:
   ```bash
   git checkout main
   git merge <branch>
   ```
5. Remove worktree:
   ```bash
   git worktree remove .worktree/<branch>
   ```

### Switch Worktree

When user requests "switch worktree", "move to feature-xxx", etc.:

1. Check existing worktrees with `git worktree list`
2. If the specified branch worktree exists:
   - Present the command to navigate to that directory
3. If it doesn't exist:
   - Ask if user wants to create a new one

## Important Rules

- Always check `.gitignore` before creating worktrees
- If build fails, report and stop
- Never use force delete (`--force`)
- Avoid direct work on main/master branches
- Recommend working in each worktree with an independent Claude session

## Best Practices

### Boris Cherny's Parallel Development Style

- Manage 3-5 worktrees simultaneously
- Number each terminal tab for easy management
- Assign independent tasks to each worktree
- Regularly merge main to prevent divergence

### Recommended Structure

```
project/                  # Main repository (design/review)
├── .worktree/
│   ├── feature-auth/     # Claude session #1
│   ├── feature-api/      # Claude session #2
│   └── bugfix-123/       # Claude session #3
```

## Related Files

- `.worktreeinclude`: Configuration for files to copy to worktrees
- `.gitignore`: Excludes `.worktree/`
