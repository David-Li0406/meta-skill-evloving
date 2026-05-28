---
name: manage-stacked-prs-using-graphite
description: Use this skill when managing stacked pull requests with Graphite CLI (gt) to streamline your version control workflow, ensuring atomic commits and logical dependencies.
---

# Skill body

## Overview

Graphite CLI (gt) simplifies the management of stacked pull requests (PRs) on GitHub, allowing you to create, modify, and submit PRs that build on each other. This skill is essential for breaking down large features into manageable, reviewable chunks.

## Core Workflow

### 1. Check Graphite Status

Before starting, ensure Graphite is active in your repository:

```bash
bash skills/use-graphite/scripts/graphite-detect.sh
```

### 2. Create a New Branch

To create a new branch with changes:

```bash
gt create --all -m "description"  # Create branch with staged changes
```

### 3. Submit a Pull Request

To submit your changes as a PR:

```bash
gt submit --no-interactive  # Push and create/update PR
```

### 4. Create Stacked PRs

When working on multiple related changes, create a stack of PRs:

```bash
gt create --all -m "Add feature step 1"
gt submit --no-interactive
gt create --all -m "Add feature step 2"
gt submit --no-interactive --stack  # Submit entire stack
```

### 5. Modify Existing Branches

To amend changes in the current branch:

```bash
gt modify  # Amend staged changes to current commit
```

### 6. Sync and Restack

To sync your branches and clean up merged branches:

```bash
gt sync  # Pull latest changes and rebase open PRs
```

### 7. Conflict Resolution

If you encounter conflicts, resolve them and continue:

```bash
gt continue  # Continue after resolving conflicts
```

## Key Concepts

- **Atomic PRs**: Each PR should represent a single, coherent change.
- **Logical Dependencies**: Structure your PRs in a way that each builds on the previous one.
- **Restacking**: Automatically rebase dependent branches when the parent changes.

## Common Patterns

### Addressing Review Feedback

If you receive feedback on a PR:

```bash
gt modify --all  # Make necessary changes
gt submit --no-interactive  # Resubmit the PR
```

### Navigating the Stack

To navigate between branches in your stack:

```bash
gt up  # Move to parent branch
gt down  # Move to child branch
gt log  # View stack structure
```