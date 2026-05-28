---
name: managing-git-worktrees
description: Creates and manages Git worktrees for parallel development workflows. Use when working on multiple features simultaneously, reviewing PRs without disrupting current work, or setting up parallel AI agent sessions.
---

# Managing Git Worktrees

## Table of Contents
- [Overview](#overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Workflow](#workflow)
- [Reference Files](#reference-files)

## Overview

Git worktrees allow you to have multiple working directories from a single repository, enabling parallel development without switching branches or stashing changes. Each worktree has its own working directory and can be on a different branch, but all worktrees share the same Git history and objects.

**Key Benefits:**
- Work on multiple features/bugs simultaneously
- Review PRs without disrupting current work
- Run parallel Claude Code sessions on separate tasks
- Compare different implementation approaches side-by-side

**Important Considerations:**
- Each worktree duplicates the working directory (disk space required)
- Each worktree needs independent dependency installation (`npm install`)
- Build artifacts and `node_modules` are per-worktree
- `.gitignore` is shared across all worktrees

## When to Use This Skill

**Use this skill when:**
- User explicitly requests worktree creation, setup, or management
- User wants to work on multiple features/tasks in parallel
- User asks to set up parallel AI agent workflows or multiple Claude Code sessions
- User mentions needing to review a PR while maintaining current work
- User wants to compare different implementation approaches side-by-side

**Do NOT use for:**
- Simple branch switching (use `git checkout` instead)
- Single-task linear workflows
- Temporary work (suggest `git stash` instead)

## Workflow

When this skill is invoked, follow these steps in order:

### Step 1: Assess Current State

First, gather context about the repository and existing worktrees:

```bash
# Check current worktrees
git worktree list

# Check current branch and status
git status

# Verify we're in the main repository
git rev-parse --show-toplevel
```

**Ask the user:**
- What parallel tasks need to be done?
- Are there specific branch names to use?
- What naming convention is preferred for worktree directories?

**Example interaction:**
```
User: "I need to work on the search feature while fixing a metadata bug"

Claude: "I can set up two worktrees for parallel development.

Current analysis:
- Repository: my-project
- Current branch: main
- Existing worktrees: 1 (main worktree only)

What would you like to name the branches?
- For search feature: [suggest: feature/search]
- For metadata bug: [suggest: fix/metadata-parsing]
```

### Step 2: Propose Worktree Structure

Based on user input, propose a structure following this pattern:

**Naming Convention:** `{project}-{task-description}`
**Directory Organization:** All worktrees at same level as main repo

**Example proposal:**
```
Current: my-project (branch: main)

Proposed worktrees:
1. ../my-project-search-feature
   Branch: feature/search

2. ../my-project-metadata-fix
   Branch: fix/metadata-parsing

Commands to execute:
git worktree add -b feature/search ../my-project-search-feature
git worktree add -b fix/metadata-parsing ../my-project-metadata-fix

After creation, each worktree will need:
cd ../my-project-search-feature && npm install
cd ../my-project-metadata-fix && npm install

Proceed with creation? (y/N)
```

**Present this proposal to the user and wait for approval before executing.**

### Step 3: Execute Worktree Creation

After user approval, execute the commands with validation:

```bash
# Create each worktree
git worktree add -b {branch-name} {worktree-path}
```

**Validation checklist after each creation:**
1. ✓ Verify creation: `git worktree list`
2. ✓ Verify branch tracking: `git -C {path} branch -vv`
3. ✓ Confirm clean state: `git -C {path} status`

**For each created worktree, inform the user:**
```
✓ Created: {worktree-path}
  Branch: {branch-name}
  Status: Clean working directory

Next steps:
  cd {worktree-path}
  npm install
  npm test  # Verify setup
```

### Step 4: Provide Environment Setup Guidance

**For Node.js projects:**

```bash
# Navigate to worktree
cd {worktree-path}

# Install dependencies
npm install

# Verify setup
npm test
npm run build  # If applicable
```

**Important reminders:**
- Each worktree has independent `node_modules` and build artifacts
- If the project uses `.env` files, copy them: `cp ../.env.example .env`
- Changes to `package.json` require running `npm install` in each worktree
- `.gitignore` is shared across all worktrees

### Step 5: Provide Cleanup Instructions

Explain the cleanup process for when work is complete:

```bash
# After merging the feature (from main worktree)
cd /path/to/my-project  # or use: cd -
git checkout main
git merge {branch-name}
git push

# Remove the worktree
git worktree remove {worktree-path}

# Delete the branch (if no longer needed)
git branch -d {branch-name}
git push origin --delete {branch-name}

# Clean up any stale references
git worktree prune
```

**Cleanup checklist:**
- [ ] Feature/fix merged to main branch
- [ ] Changes pushed to remote
- [ ] Worktree removed
- [ ] Local branch deleted
- [ ] Remote branch deleted (if applicable)
- [ ] Stale references pruned

## Reference Files

For detailed information, see:

- **[REFERENCE.md](references/REFERENCE.md)** - Command reference, error handling, and monitoring
- **[SCENARIOS.md](references/SCENARIOS.md)** - Common workflow scenarios with examples
- **[SCRIPTS.md](references/SCRIPTS.md)** - Automation scripts for frequent operations

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git worktree add <path> <branch>` | Create worktree from existing branch |
| `git worktree add -b <branch> <path>` | Create worktree with new branch |
| `git worktree list` | Show all worktrees |
| `git worktree remove <path>` | Delete worktree |
| `git worktree prune` | Clean up stale references |

## Node.js Project Notes

**Dependency Management:**
- Run `npm install` in each new worktree after creation
- After `package.json` changes: `npm install` in all active worktrees

**Build Artifacts:**
- Each worktree has independent `dist/` or `build/` directory
- Run `npm run build` separately in each worktree

**Test Isolation:**
- Tests run independently per worktree
- Use `npm test` to verify each worktree setup

## Best Practices

1. **Naming**: Use descriptive, consistent names (`{project}-{task}`)
2. **Organization**: Keep all worktrees at same directory level as main repo
3. **Cleanup**: Remove worktrees immediately after merging
4. **Verification**: Always run `git worktree list` before/after operations
5. **Dependencies**: Run `npm install` in each new worktree
6. **Branch tracking**: Create branches with worktrees using `-b` flag
7. **Disk awareness**: Remind user each worktree duplicates working directory
