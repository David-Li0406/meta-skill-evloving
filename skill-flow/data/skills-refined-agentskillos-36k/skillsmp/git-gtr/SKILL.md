---
name: git-gtr
description: Manage git worktrees with gtr. Use when working on multiple branches in parallel, especially with async agents.
---

# Git GTR (Git Worktree Runner)

Bash-based worktree manager that wraps `git worktree` with automation for modern dev workflows.

## Why gtr over raw git worktree

- Auto-names folders (feature/auth → feature-auth)
- Copies env files (.env, .envlocal) automatically
- Editor/AI tool integration (cursor, vscode, aider, claude-code)
- Hooks for post-create/remove actions
- Repository-scoped configuration
- Cleaner CLI syntax

## Core Commands

```sh
# Create worktree
git gtr new <branch>                    # Create from remote branch
git gtr new <branch> --from-current     # Base on current branch
git gtr new <branch> --from <ref>       # Create from commit/tag

# Navigate
git gtr go <branch>                     # Output path (use with cd)
cd "$(git gtr go my-feature)"           # Switch to worktree
cd "$(git gtr go 1)"                    # Main repository

# List & clean
git gtr list                            # Show all worktrees
git gtr clean                           # Remove stale worktrees

# Remove
git gtr rm <branch>...                  # Remove worktree(s)
git gtr rm <branch> --delete-branch     # Also delete git branch

# Open editor/AI
git gtr editor <branch>                 # Open in configured editor
git gtr ai <branch>                     # Launch AI tool
git gtr ai <branch> -- --args           # Pass tool-specific args
```

## Parallel Agent Workflow

```sh
# Multiple worktrees on same branch (for parallel agent work)
git gtr new feature-auth --force --name agent1
git gtr new feature-auth --force --name agent2

# Launch separate AI sessions
git gtr ai feature-auth-agent1
git gtr ai feature-auth-agent2

# Cleanup
git gtr rm feature-auth-agent1 feature-auth-agent2
```

## Configuration

```sh
# Set defaults (repository-scoped)
git config gtr.editor.default cursor
git config gtr.ai.default claude-code
git config gtr.copy.include ".env,.envlocal"
git config gtr.hook.postCreate "pnpm install"
```

Ref: https://github.com/coderabbitai/git-worktree-runner
