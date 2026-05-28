---
name: git-worktree
description: Use this skill to manage Git worktrees for isolated parallel development, including creating, listing, switching, and cleaning up worktrees with an interactive interface.
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
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create <feature-name>

# ❌ WRONG - Never do this directly
git worktree add .worktrees/<feature-name> -b <feature-name> main
```

## When to Use This Skill

Use this skill in these scenarios:

1. **Code Review (`/workflows:review`)**: If NOT already on the PR branch, offer a worktree for isolated review.
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
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create <feature-name>

# List all worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list

# Switch to a worktree
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch <feature-name>

# Copy .env files to an existing worktree (if they weren't copied)
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh copy-env <feature-name>

# Clean up completed worktrees
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

## Commands

### `create <branch-name> [from-branch]`

Creates a new worktree with the given branch name.

**Options:**
- `branch-name` (required): The name for the new branch and worktree
- `from-branch` (optional): Base branch to create from (defaults to `main`)

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create <feature-name>
```

**What happens:**
1. Checks if the worktree already exists
2. Updates the base branch from remote
3. Creates a new worktree and branch
4. **Copies all .env files from the main repo** (.env, .env.local, .env.test, etc.)
5. Shows the path for cd-ing to the worktree

### `list` or `ls`

Lists all available worktrees with their branches and current status.

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list
```

**Output shows:**
- Worktree name
- Branch name
- Which is current (marked with ✓)
- Main repo status

### `switch <name>` or `go <name>`

Switches to an existing worktree and cd's into it.

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch <feature-name>
```

**Optional:**
- If the name is not provided, lists available worktrees and prompts for selection.

### `cleanup` or `clean`

Interactively cleans up inactive worktrees with confirmation.

**Example:**
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

**What happens:**
1. Lists all inactive worktrees
2. Asks for confirmation
3. Removes selected worktrees
4. Cleans up empty directories

## Workflow Examples

### Code Review with Worktree

```bash
# Claude Code recognizes you're not on the PR branch
# Offers: "Use worktree for isolated review? (y/n)"

# You respond: yes
# Script runs (copies .env files automatically):
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create <pr-branch-name>

# You're now in isolated worktree for review with all env vars
cd .worktrees/<pr-branch-name>

# After review, return to main:
cd ../..
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

### Parallel Feature Development

```bash
# For first feature (copies .env files):
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create <feature-1-name>

# Later, start second feature (also copies .env files):
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh create <feature-2-name>

# List what you have:
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list

# Switch between them as needed:
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh switch <feature-1-name>

# Return to main and cleanup when done:
cd .
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

## Key Design Principles

### KISS (Keep It Simple, Stupid)

- **One manager script** handles all worktree operations
- **Simple commands** with sensible defaults
- **Interactive prompts** prevent accidental operations
- **Clear naming** using branch names directly

### Opinionated Defaults

- Worktrees always created from **main** (unless specified)
- Worktrees stored in **.worktrees/** directory
- Branch name becomes worktree name
- **.gitignore** automatically managed

### Safety First

- **Confirms before creating** worktrees
- **Confirms before cleanup** to prevent accidental removal
- **Won't remove current worktree**
- **Clear error messages** for issues

## Integration with Workflows

### `/workflows:review`

Instead of always creating a worktree:

```
1. Check current branch
2. If ALREADY on PR branch → stay there, no worktree needed
3. If DIFFERENT branch → offer worktree:
   "Use worktree for isolated review? (y/n)"
   - yes → call git-worktree skill
   - no → proceed with PR diff on current branch
```

### `/workflows:work`

Always offer choice:

```
1. Ask: "How do you want to work?
   1. New branch on current worktree (live work)
   2. Worktree (parallel work)"

2. If choice 1 → create new branch normally
3. If choice 2 → call git-worktree skill to create from main
```

## Troubleshooting

### "Worktree already exists"

If you see this, the script will ask if you want to switch to it instead.

### "Cannot remove worktree: it is the current worktree"

Switch out of the worktree first (to main repo), then cleanup:

```bash
cd $(git rev-parse --show-toplevel)
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

### Lost in a worktree?

See where you are:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh list
```

### .env files missing in worktree?

If a worktree was created without .env files (e.g., via raw `git worktree add`), copy them:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/git-worktree/scripts/worktree-manager.sh copy-env <feature-name>
```

Navigate back to main:

```bash
cd $(git rev-parse --show-toplevel)
```

## Technical Details

### Directory Structure

```
.worktrees/
├── <feature-1-name>/          # Worktree 1
│   ├── .git
│   ├── app/
│   └── ...
├── <feature-2-name>/          # Worktree 2
│   ├── .git
│   ├── app/
│   └── ...
└── ...

.gitignore (updated to include .worktrees)
```

### How It Works

- Uses `git worktree add` for isolated environments
- Each worktree has its own branch
- Changes in one worktree don't affect others
- Share git history with the main repo
- Can push from any worktree

### Performance

- Worktrees are lightweight (just file system links)
- No repository duplication
- Shared git objects for efficiency
- Much faster than cloning or stashing/switching