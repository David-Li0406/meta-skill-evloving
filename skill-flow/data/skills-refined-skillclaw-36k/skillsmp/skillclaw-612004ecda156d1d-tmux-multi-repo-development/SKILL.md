---
name: tmux-multi-repo-development
description: Use this skill when you want to set up a parallel development environment across multiple repositories using tmux, ghq, and gwq.
---

# Multi-Repository Parallel Development

This skill combines `ghq`, `gwq`, and `tmux` to facilitate parallel development across multiple repositories.

## Workflow

### 1. Clone Repositories
```bash
# Clone repositories (skip if already cloned)
ghq get github.com/user/frontend-repo
ghq get github.com/user/backend-repo
```

### 2. Create Worktrees for Each Repository
```bash
# Frontend
cd $(ghq list -p | grep frontend-repo) && gwq add -b feature/api-integration

# Backend
cd $(ghq list -p | grep backend-repo) && gwq add -b feature/new-endpoint
```

### 3. Start Development Servers in Each Worktree
```bash
gwq tmux run -w feature/api-integration "npm run dev"
gwq tmux run -w feature/new-endpoint "go run main.go"
```

### 4. Check Status
```bash
# Check the status of all worktrees
gwq status -g --show-processes

# List tmux sessions
gwq tmux list
```

### 5. Execute Commands in Specific Worktrees
```bash
gwq exec feature/api-integration -- npm test
gwq exec feature/new-endpoint -- go test ./...
```

## Additional Commands for ghq
```bash
ghq list              # List repositories
ghq list -p           # Show full paths
ghq root              # Show root directory
ghq get <url>         # Clone a repository
```

## Tips
- Use `gwq status -w` for monitoring mode (auto-detect changes).
- Attach to a session with `gwq tmux attach <pattern>`.
- Clean up after work with `gwq tmux kill` followed by `gwq remove -b`.