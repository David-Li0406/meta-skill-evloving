---
name: git-workflow-guide
description: Use this skill when you need guidance on Git branching strategies, naming conventions, and merging operations.
---

# Git Workflow Guide

> **Language**: [English](../../../../../skills/claude-code/git-workflow-guide/SKILL.md) | 中文

**Version**: 1.0.0  
**Last Updated**: 2025-12-24  
**Applicable Scope**: Claude Code Skills

---

## Purpose

This skill provides guidance on Git branching strategies, naming conventions, and merging operations.

## Quick Reference

### Workflow Strategy Selection

| Deployment Frequency | Recommended Strategy          |
|----------------------|-------------------------------|
| Multiple times daily  | Trunk-Based Development       |
| Weekly to bi-weekly   | GitHub Flow                   |
| Monthly or longer      | GitFlow                       |

### Branch Naming Conventions

```
<type>/<short-description>
```

| Type        | Purpose                          | Example                     |
|-------------|----------------------------------|-----------------------------|
| `feature/`  | New feature                      | `feature/oauth-login`       |
| `fix/` or `bugfix/` | Bug fix                  | `fix/memory-leak`          |
| `hotfix/`   | Emergency production fix         | `hotfix/security-patch`    |
| `refactor/` | Code refactoring                 | `refactor/extract-service` |
| `docs/`     | Documentation changes            | `docs/api-reference`       |
| `test/`     | New tests                        | `test/integration-tests`    |
| `chore/`    | Maintenance tasks                | `chore/update-dependencies` |
| `release/`  | Release preparation              | `release/v1.2.0`          |

### Naming Rules

1. **Use lowercase**
2. **Use hyphens to separate words**
3. **Descriptive but concise**

## Detailed Guide

For complete standards, refer to:
- [Git Workflow Strategies](./git-workflow.md)
- [Branch Naming Reference](./branch-naming.md)

## Pre-Branch Creation Checklist

Before creating a new branch:

1. **Check for unmerged branches**
   ```bash
   git branch --no-merged main
   ```

2. **Sync the latest code**
   ```bash
   git checkout main
   git pull origin main
   ```

3. **Ensure tests pass**
   ```bash
   npm test  # or your project's test command
   ```

4. **Create a branch with the correct naming**
   ```bash
   git checkout -b feature/description
   ```

## Merge Strategy Quick Guide

| Strategy                | When to Use                          |
|-------------------------|--------------------------------------|
| **Merge Commit** (`--no-ff`) | Long-term features, GitFlow releases |
| **Squash Merge**       | Feature branches, clean history      |
| **Rebase + FF**       | Trunk-Based, short-lived branches    |

## Examples

### Creating a Feature Branch

```bash
# Good examples
git checkout -b feature/user-authentication
git checkout -b fix/null-pointer-in-payment
git checkout -b hotfix/critical-data-loss

# Bad examples
git checkout -b 123              # Lacks descriptiveness
git checkout -b Fix-Bug          # Not lowercase
git checkout -b myFeature        # Missing type prefix
```

### Merging Workflow (GitHub Flow)

```bash
# 1. Create a branch from main
git checkout main
git pull origin main
git checkout -b feature/user-profile

# 2. Make changes and commit
git add .
git commit -m "feat(profile): add avatar upload"
git push -u origin feature/user-profile

# 3. Create a PR and merge via GitHub/GitLab UI

# 4. After merging, delete the branch
git checkout main
git pull origin main
git branch -d feature/user-profile
```

### Handling Merge Conflicts

```bash
# 1. Update your branch with main
git checkout feature/my-feature
git merge main
# Resolve conflicts as necessary
```