---
name: git-worktree-management
description: Use this skill when you need to set up a Git worktree for parallel development, ensuring proper branch management and adherence to workflow rules.
---

# Skill body

## Purpose

This skill automates the setup of a Git worktree for parallel development, allowing you to work on multiple features simultaneously without affecting the main branch.

## When to Use

Use this skill when:
- Starting development on a new feature.
- You want to work on multiple feature branches concurrently.
- You need to maintain the state of the main branch while experimenting with changes.

## Instructions

### 1. Validate Environment

Check if you are in a Git repository and list existing worktrees:

```bash
git rev-parse --git-dir 2>/dev/null || echo "Not a git repository"
git worktree list
```

### 2. Determine Feature Name

Obtain a feature name from the user or suggest one based on the task. Good feature names should:
- Be descriptive (e.g., `user-authentication`, `api-rate-limiting`).
- Avoid spaces and special characters.

### 3. Create Worktree

Create a new worktree and branch:

```bash
FEATURE_NAME="<feature-name>"
BRANCH_NAME="feature/${FEATURE_NAME}"
WORKTREE_DIR=".worktrees/${FEATURE_NAME}"

# Check if the branch already exists
if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
  git worktree add "${WORKTREE_DIR}" "${BRANCH_NAME}"
else
  git worktree add -b "${BRANCH_NAME}" "${WORKTREE_DIR}"
fi
```

### 4. Create Symbolic Link for Settings

After creating the worktree, create a symbolic link for the settings file:

```bash
MAIN_REPO=$(git worktree list --porcelain | grep -m 1 "worktree" | cut -d' ' -f2)
rm -f "${WORKTREE_DIR}/.claude/settings.local.json"
ln -s "${MAIN_REPO}/.claude/settings.local.json" "${WORKTREE_DIR}/.claude/settings.local.json"
```

### 5. Report Status

Inform the user about the created worktree:

```markdown
✅ Worktree created successfully.

**Location:** .worktrees/<feature-name>/
**Branch:** feature/<feature-name>

**Next Steps:**
1. `cd .worktrees/<feature-name>/` to navigate to the directory.
2. Continue development as usual.
3. When done, use the `pr-and-cleanup` skill for PR creation and cleanup.
```

### 6. Handle Edge Cases

If a worktree already exists at the specified path:

```bash
if [ -d "${WORKTREE_DIR}" ]; then
  echo "⚠️ Worktree already exists at ${WORKTREE_DIR}. Would you like to use the existing worktree or create a new one with a different name?"
fi
```

## Key Principles

1. **Simplicity**: Avoid project-specific configurations.
2. **Safety**: Do not overwrite existing worktrees.
3. **Standard Naming**: Use `feature/` as the default prefix for branch names.
4. **Flexibility**: Allow customization of branch and directory names.

## Customization Options

Ask the user if they want to customize:
- Branch prefix (e.g., `feature/`, `bugfix/`).
- Worktree base directory (other than `.worktrees/`).
- Base branch (other than `main`).