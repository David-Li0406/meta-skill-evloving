---
name: Worktree Feature Development
description: This skill should be used when the user asks to "start a new feature", "create feature branch in worktree", "set up isolated feature development", "work on feature in separate directory", or mentions git worktree for feature isolation.
version: 0.1.0
---

## Purpose

Create a new git worktree for isolated feature development with a dedicated branch. This allows working on features in parallel without stashing or switching branches in the main repository.

## Workflow

1. Prompt user for feature name if not provided
2. Create feature branch from current branch (or specified base)
3. Create git worktree in sibling directory: `../<repo>-<feature-name>`
4. Navigate (cd) into the new worktree directory

## Instructions

When the user wants to start a new feature in a worktree:

### Step 1: Gather Information
Ask the user for the feature name if not already provided. Optionally ask which branch to base the feature on (default: current branch).

### Step 2: Create the Worktree
Execute the following commands:

```bash
# Determine values
FEATURE_NAME="<user-provided-name>"
BASE_BRANCH=$(git branch --show-current)
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
WORKTREE_PATH="../${REPO_NAME}-${FEATURE_NAME}"

# Create worktree with new feature branch
git worktree add -b "feature/${FEATURE_NAME}" "${WORKTREE_PATH}" "${BASE_BRANCH}"
```

### Step 3: Navigate to Worktree
Change to the new worktree directory:

```bash
cd "${WORKTREE_PATH}"
```

### Step 4: Confirm Success
Inform the user that the worktree has been created and they are now working in the isolated feature directory.

## User Prompts

- **Feature name**: Required. Ask "What would you like to name this feature?" if not provided.
- **Base branch**: Optional. Default to current branch. Ask "Which branch should this feature be based on?" only if the user seems uncertain.

## Example Usage

User: "Start a new feature called user-auth"

Result:
- Creates branch `feature/user-auth` based on current branch
- Creates worktree at `../repo-name-user-auth`
- Changes directory to the new worktree
