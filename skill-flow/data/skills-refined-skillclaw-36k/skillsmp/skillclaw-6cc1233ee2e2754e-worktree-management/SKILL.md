---
name: worktree-management
description: Use this skill when you want to manage worktrees and tmux sessions, including starting development servers, checking statuses, and cleaning up after work.
---

# Skill body

## Worktree Development Server Launch

Use this section to start a development server in a tmux session.

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

3. Attach to a session (for log monitoring, etc.):
   ```bash
   gwq tmux attach <pattern>
   ```

### Options
- Custom session ID: `gwq tmux run --id <name> "<command>"`
- Run while attached: `gwq tmux run --no-detach "<command>"`
- Auto-cleanup on completion: `gwq tmux run --auto-cleanup "<command>"`

### Examples
```bash
# Frontend development server
gwq tmux run -w feature/ui "npm run dev"

# Backend server
gwq tmux run -w feature/api "go run main.go"

# Test watcher
gwq tmux run -w feature/test "npm run test:watch"
```

## Worktree Status Check

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

### Output Example
```
gwq status -g --show-processes
────────────────────────────────────
repo: frontend
  feature/ui [modified: 3 files]
    └─ tmux: npm run dev (pid: 12345)

repo: backend
  feature/api [clean]
    └─ tmux: go run main.go (pid: 12346)
```

## Worktree Cleanup

Use this section to clean up worktrees and tmux sessions after work is completed.

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

3. Remove both the worktree and the branch:
   ```bash
   gwq remove -b <pattern>
   ```

4. Clean up unnecessary worktree information:
   ```bash
   gwq prune
   ```

### Options
- Force removal (even with uncommitted changes): `gwq remove -f <pattern>`

### Notes
- Before deletion, check for changes with `gwq status`.
- If there are important changes, commit them before deletion.
- **Important**: `gwq remove` cannot be executed from within the target worktree directory. Move to the main repository directory first:
  ```bash
  cd $(gwq get master)  # or cd ~/ghq/github.com/<owner>/<repo>
  gwq remove -b <pattern>
  ```

### Complete Cleanup Example
```bash
# 1. End the session
gwq tmux kill feature/done

# 2. Move to the main repository
cd $(gwq get master)

# 3. Remove the worktree and branch
gwq remove -b feature/done

# 4. Clean up isolated worktree references
gwq prune
```