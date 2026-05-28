---
name: git-worktrees
description: Use when starting work that needs isolated branches or parallel feature development using git worktrees.
allowed-tools: ["shell", "read_file"]
metadata:
  short-description: Create and manage git worktrees safely
---

# Git Worktrees

**Read these references:**
- `~/.config/agent/core/behavior.md` - Safety and verification
- `~/.config/agent/core/methodology.md` - Structured workflow

## Overview

Git worktrees provide isolated working directories for parallel branches without switching context.

**Core principle:** Safe directory selection + verification before use.

## Directory Selection

1. Prefer existing `.worktrees/` (hidden)
2. Else use `worktrees/` if present
3. Else check `CLAUDE.md` for guidance
4. Else ask user for preferred location

## Safety Verification

For project-local worktrees:

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

If not ignored, add to `.gitignore` before continuing.

## Create Worktree

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
# Choose path based on directory selection
# Example (project-local):
path=".worktrees/<branch-name>"

# Preflight checks
if [ -e "$path" ]; then
    echo "Error: $path already exists" >&2
    # Ask user whether to reuse or choose a new path
fi

if git show-ref --verify --quiet refs/heads/<branch-name>; then
    echo "Warning: branch <branch-name> already exists" >&2
    # Ask user whether to reuse or choose a new name
fi

git worktree add "$path" -b <branch-name>
cd "$path"
```

## Project Setup

Auto-detect and run setup:

```bash
if [ -f package.json ]; then npm install; fi
if [ -f Cargo.toml ]; then cargo build; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi
if [ -f go.mod ]; then go mod download; fi
```

## Baseline Verification

Run the project’s standard tests. If failures occur, report and ask whether to proceed or investigate.

## Arguments

Target: ${ARGUMENTS}
