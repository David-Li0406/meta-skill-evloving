---
name: git-worktree
description: Use this skill to manage Git worktrees for isolated parallel development, allowing you to create, list, switch, and clean up worktrees easily.
---

# Git Worktree Manager

This skill provides a unified interface for managing Git worktrees across your development workflow. Whether you're reviewing PRs in isolation or working on features in parallel, this skill handles all the complexity.

## What This Skill Does

- **Create worktrees** from the main branch with clear branch names
- **List worktrees** with current status
- **Switch between worktrees** for parallel work
- **Clean up completed worktrees** automatically
- **Interactive confirmations** at each step
- **Automatic .gitignore management** for worktree directory
- **Automatic .env file copying** from the main repo to new worktrees

## CRITICAL: Always Use the Manager Script

**NEVER call `git worktree add` directly.** Always use the `worktree-manager.sh` script.

The script handles critical setup that raw git commands don't:
1. Copies `.env`, `.env.local`, `.env.test`, etc. from the main repo
2. Ensures `.worktrees` is in `.gitignore`
3. Creates a consistent directory structure

```bash
# ✅ CORRECT - Always use the script
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-name

# ❌ WRONG - Never do this directly
git worktree add .worktrees/feature-name -b feature-name main
```

## When to Use This Skill

Use this skill in these scenarios:

1. **Code Review (`/workflows:review`)**: If NOT already on the target branch (PR branch or requested branch), offer a worktree for isolated review.
2. **Feature Work (`/workflows:work`)**: Always ask if the user wants a parallel worktree or live branch work.
3. **Parallel Development**: When working on multiple features simultaneously.
4. **Cleanup**: After completing work in a worktree.

## How to Use

### In Claude Code Workflows

The skill is automatically called from `/workflows:review` and `/workflows:work` commands:

```
# For review: offers worktree if not on PR branch
# For work: always asks - new branch or worktree?
```

### Manual Usage

You can also invoke the skill directly from bash:

```bash
# Create a new worktree (copies .env files automatically)
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create feature-login

# List all worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list

# Switch to a worktree
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch feature-login

# Clean up completed worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```