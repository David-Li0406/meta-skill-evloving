---
name: git-pretty-accept-merge
description: Git merge workflow using --no-ff flag with rebase-first strategy for clean history. Use when project's CLAUDE.md or documentation specifies this merge workflow, when merging feature branches, or when asked to follow the "pretty accept merge" or "no fast-forward merge" pattern.
---

# Git Pretty Accept Merge Workflow

This skill guides Claude through the proper git merge workflow based on the "pretty accept merge" pattern that preserves branch history and keeps commits clean.

## When to Use This Skill

Use this skill when:
- The project's CLAUDE.md or documentation specifies this as the merge workflow
- Merging feature branches that should preserve their history
- Asked to follow a "no fast-forward" or "--no-ff" merge strategy
- Working with projects that use rebase-first merge patterns

## Workflow Steps

Follow these steps in order:

### Step 1: Checkout main

```bash
git checkout main
```

### Step 2: Pull latest from origin

```bash
git pull origin main
```

### Step 3: Check if feature branch needs rebasing

Check the merge base to see if the feature branch has diverged from main:

```bash
git merge-base main <feature-branch>
git rev-parse main
```

If these return different commits, the branch needs rebasing.

### Step 4: Rebase feature branch (if needed)

If the branch needs rebasing:

```bash
git checkout <feature-branch>
git rebase main
```

Handle any conflicts that arise during rebase.

### Step 5: Merge with --no-ff

After rebasing (or if no rebase was needed):

```bash
git checkout main
git merge --no-ff <feature-branch> -m "<merge-commit-message>"
```

## Merge Commit Message Format

The merge commit should be high-level and explain what the branch accomplishes:

```
Merge branch 'feat/feature-name'

High-level summary of what this feature branch adds to the project.

Key additions:
- Bullet point 1
- Bullet point 2
- Bullet point 3
```

## Key Principles

- Always use `--no-ff` to preserve branch history
- Rebase feature branches to keep history clean
- The merge commit message should provide context for the overall feature
- Small fixes can be committed directly to main when appropriate
