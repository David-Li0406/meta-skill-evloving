---
name: git-worktree-management
description: Use this skill to manage git worktrees (create, list, switch, cleanup) and copy .env files for parallel feature work, isolated review, or clean workspace.
---

# Worktree Management

Use the manager script for all worktree actions.

```bash
bash <path_to_worktree_script> <command> [args]
```

Commands:
- `create <name> [base]`
- `list`
- `switch <name>` (prints path)
- `cleanup`
- `copy-env <name>`

Safety notes:
- `create` does not change the current branch.
- `cleanup` does not force-remove worktrees and does not delete branches.
- `cleanup` deletes the worktree directory (including ignored files); removal fails if the worktree is not clean.
- `.env*` files are copied with no overwrite (symlinks skipped).
- Refuses to operate if `.worktrees/` or any worktree path component is a symlink.
- `copy-env` only targets registered worktrees.
- `origin` fetch is optional; local base refs are allowed.
- Fetch from `origin` only when base looks like a branch.
- Worktrees live under `.worktrees/`.