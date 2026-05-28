---
name: worktree-management
description: Use this skill when you need to manage worktrees and tmux sessions, including starting servers, checking statuses, and cleaning up after work.
---

# Worktree Management

This skill allows you to manage worktrees and tmux sessions effectively, including starting development servers, checking the status of worktrees, and cleaning up after tasks.

## Starting a Development Server

Use this section to start a long-running process in a tmux session within a worktree.

### Arguments
- `$ARGUMENTS`: `<worktree-pattern> <command>` format
  - Example: `feature/new-feature "npm run dev"`

### Steps
1. Start a command in a tmux session within the worktree:
   ```bash
   gwq tmux run -w <worktree-pattern> "<command>"
   ```

2. Check the list of sessions:
   ```bash
   gwq tmux list
   ```

3. Attach to a session for log monitoring:
   ```bash
   gwq tmux attach <pattern>
   ```

### Options
- Custom session ID: `gwq tmux run --id <name> "<command>"`
- Run while attached: `gwq tmux run --no-detach "<command>"`
- Auto-cleanup on completion: `gwq tmux run --auto-cleanup "<command>"`

## Checking Worktree Status

Use this section to check the status of worktrees and running processes.

### Steps
1. List worktrees in the current repository:
   ```bash
   gwq list -v
   ```

2. List worktrees across all repositories:
   ```bash
   gwq list -g
   ```

3. Check the status of all worktrees (including modified files):
   ```bash
   gwq status
   ```

4. Show running process information:
   ```bash
   gwq status -g --show-processes
   ```

5. List tmux sessions:
   ```bash
   gwq tmux list
   ```

### Options
- Watch mode (auto-update): `gwq status -w`
- Detailed view for a specific worktree: `gwq get <pattern>`

## Cleaning Up Worktrees

Use this section to clean up worktrees and tmux sessions after completing tasks.

### Arguments
- `$ARGUMENTS`: worktree pattern (e.g., `feature/old-feature`)

### Steps
1. End the tmux session:
   ```bash
   gwq tmux kill <pattern>
   ```

2. Remove the worktree (keeping the branch):
   ```bash
   gwq remove <pattern>
   ```

3. Remove the worktree and branch together:
   ```bash
   gwq remove -b <pattern>
   ```

4. Clean up orphaned worktree references:
   ```bash
   gwq prune
   ```

### Options
- Force removal (even with uncommitted changes): `gwq remove -f <pattern>`

### Notes
- Before deletion, check for changes with `gwq status`.
- If there are important changes, commit them before deletion.
- **Important**: Do not run `gwq remove` from within the worktree directory. Move to the main repository directory first:
  ```bash
  cd $(gwq get master)  # or cd ~/ghq/github.com/<owner>/<repo>
  gwq remove -b <pattern>
  ```

### Example of Complete Cleanup
```bash
# 1. End the session
gwq tmux kill feature/done

# 2. Move to the main repository
cd $(gwq get master)

# 3. Remove the worktree and branch
gwq remove -b feature/done

# 4. Clean up orphaned worktree references
gwq prune
```