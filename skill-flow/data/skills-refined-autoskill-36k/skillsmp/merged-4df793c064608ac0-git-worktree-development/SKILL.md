---
name: git-worktree-development
description: Use this skill when managing multiple Git worktrees for parallel development, including creating worktrees, managing dependencies, synchronizing files, and orchestrating services across branches.
---

# Git Worktree Development - Comprehensive Guide

This guide covers advanced patterns for developing across multiple Git worktrees simultaneously using the `gw` CLI tool.

## Table of Contents

1. [Git Worktree Fundamentals](#1-git-worktree-fundamentals)
2. [Creating and Managing Worktrees with gw](#2-creating-and-managing-worktrees-with-gw)
3. [Navigating Between Worktrees](#3-navigating-between-worktrees)
4. [Dependency Management](#4-dependency-management)
5. [File Synchronization](#5-file-synchronization)
6. [Database and Service Management](#6-database-and-service-management)
7. [Testing Workflows](#7-testing-workflows)
8. [Cleanup and Maintenance](#8-cleanup-and-maintenance)
9. [Troubleshooting Common Issues](#9-troubleshooting-common-issues)

---

## 1. Git Worktree Fundamentals

### What are Git Worktrees?

Git worktrees allow you to have multiple working directories attached to a single repository. Instead of switching branches in your current directory, you can check out different branches in separate directories simultaneously.

### When Worktrees Shine

Worktrees are ideal for:
- Parallel feature development
- Hotfix workflows
- Code reviews
- Testing multiple versions or configurations simultaneously
- Long-running experiments

### Worktree Limitations and Gotchas

**What worktrees share:**
- Git repository (.git directory)
- Commit history and objects
- Branches and tags

**What worktrees DON'T share:**
- Working directory files
- Untracked files
- node_modules (unless symlinked)

---

## 2. Creating and Managing Worktrees with gw

### The `gw add` Command

The `gw add` command is an enhanced version of `git worktree add` with automatic file copying:

```bash
# Create worktree for existing branch
gw add feature-auth

# Create worktree with new branch
gw add feature-payments -b feature-payments
```

### Auto-Copying Files

When creating worktrees with `gw add`, files configured in `.gw/config.json` are automatically copied, such as environment files and secrets.

### Manual File Copying with `gw sync`

If you need to copy files later or from a different source:

```bash
# Copy specific files from main to current worktree
gw sync feature-auth .env
```

---

## 3. Navigating Between Worktrees

### Using `gw cd` for Quick Navigation

The `gw cd` command provides smart navigation to worktrees:

```bash
# Full worktree name
gw cd feature-authentication

# Partial match
gw cd feat    # Matches feature-authentication if it's first
```

### IDE Workspace Management

Open each worktree as a separate window in your IDE or use multi-root workspaces.

---

## 4. Dependency Management

### Understanding the Problem

Each worktree has independent working files, including `node_modules`, leading to duplicated dependencies.

### Strategies for Dependency Management

1. **Accept Duplication**: Each worktree installs independently.
2. **Use pnpm**: A content-addressable store that deduplicates packages.
3. **Symlink node_modules**: Only works if all worktrees need identical dependencies.

### Post-Add Hook for Auto-Install

Automatically install dependencies when adding a new worktree:

```bash
gw init --post-add "npm install"
```

---

## 5. File Synchronization

### Using `gw sync`

Sync files between worktrees without recreating them:

```bash
# Sync all autoCopyFiles from config
gw sync feat/user-auth

# Sync specific file from main to feature branch
gw sync feat/user-auth .env
```

### Common Sync Patterns

- Update secrets across all worktrees
- Propagate config changes
- Hot-swap environment configurations

---

## 6. Database and Service Management

### Database Isolation Strategies

1. **Separate databases per worktree**: Each worktree has its own database.
2. **Docker Compose per worktree**: Use different configurations for each worktree.
3. **Shared database with schema prefixes**: Use different schemas for each worktree.

### Port Management

Avoid port conflicts between worktrees by assigning different ports in `.env` files.

---

## 7. Testing Workflows

### Parallel Testing Across Environments

Test the same feature in multiple environments:

```bash
# Create test worktrees
gw add test-node18 --force
gw add test-node20 --force
```

### CI/CD Integration

Integrate with CI/CD tools like GitHub Actions to run tests across multiple environments.

---

## 8. Cleanup and Maintenance

### Removing Worktrees

Safely remove worktrees:

```bash
# Remove worktree
gw remove feature-completed
```

### Cleaning Up Stale Worktrees

Automatically remove old worktrees:

```bash
# Preview what would be removed
gw clean --dry-run

# Remove stale worktrees
gw clean
```

### Pruning Stale Worktree References

Clean up references to worktrees that no longer exist:

```bash
gw prune
```

---

## 9. Troubleshooting Common Issues

### "Worktree already exists" Errors

If you encounter this error, list existing worktrees and remove the old one first:

```bash
gw list
gw remove feature-auth
```

### Locked Worktree Recovery

Unlock a worktree if you cannot remove it:

```bash
gw unlock feature-x
gw remove feature-x
```

### Corrupted Worktree State

Repair worktree administrative files if you encounter issues:

```bash
gw repair
```

---

## Summary

You now understand:
- Managing parallel development workflows effectively
- Dependency strategies (pnpm recommended)
- Keeping files in sync with `gw sync`
- Database and service isolation patterns
- Parallel testing across environments
- Cleanup and maintenance strategies
- Troubleshooting common issues

### Next Steps

1. Set up pnpm for efficient dependency management.
2. Configure post-add hooks for automatic setup.
3. Create team guidelines for worktree usage.

### Additional Resources

- [Getting Started Example](./examples/getting-started.md)
- [Parallel Development Example](./examples/parallel-development.md)
- [Troubleshooting Guide](./examples/troubleshooting-worktrees.md)

---

*Part of the [gw-tools skills collection](../README.md)*