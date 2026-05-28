---
name: simple-git-worktrees
description: This skill should be used when the user asks to "create worktree", "remove worktree", "work in worktree", "switch to worktree", "clean up worktree", mentions "repo--branch pattern", or during plan execution when worktree isolation is needed. Documents the sibling directory worktree pattern for simple, safe git worktree workflows.
allowed-tools: Read, Bash, AskUserQuestion
---

# Simple Git Worktrees

Guide Claude in creating and managing git worktrees using a simple sibling directory pattern.

## When to Use Worktrees

Use worktrees for:
- Parallel development on multiple branches
- Reviewing PRs while preserving current work
- Running tests on different branches simultaneously
- Isolating experimental changes

## The Sibling Directory Pattern

Worktrees are created as sibling directories alongside the main repository following the `repo--branch` naming convention:

```
parent/
  ├── my-project/          # Main repository
  ├── my-project--feature/ # Worktree for 'feature' branch
  ├── my-project--bugfix/  # Worktree for 'bugfix' branch
  └── my-project--review/  # Worktree for reviewing PR
```

**Benefits:**
- Lives alongside main repo (easy to find and navigate)
- Name encodes branch (self-documenting, no guesswork)
- No special permissions needed (just sibling directories)
- Standard shell tools work (cd, ls, find)
- Pattern validation prevents accidental deletions

## Creating Worktrees

### Basic Creation

Use `worktree-manager.sh` for safe, validated creation:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

# Create worktree for branch
BRANCH="feature-name"
WORKTREE_PATH=$(create_worktree "$BRANCH")

# Switch to worktree
cd "$WORKTREE_PATH"
```

**What happens:**
1. Calculates sibling path: `../repo--branch`
2. Checks if path already exists (prevents overwrites)
3. Creates worktree with new branch: `git worktree add -b "$BRANCH" "$PATH"`
4. Returns full path to worktree

**Manual creation (without script):**

```bash
# Get current repo name
REPO_BASE="$(basename "$PWD")"
BRANCH="feature-name"

# Calculate sibling path
WORKTREE_PATH="../${REPO_BASE}--${BRANCH}"

# Create worktree
git worktree add -b "$BRANCH" "$WORKTREE_PATH"

# Switch to it
cd "$WORKTREE_PATH"
```

### Creating from Existing Branch

Create worktree for branch that already exists:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

REPO_BASE="$(basename "$PWD")"
EXISTING_BRANCH="main"
WORKTREE_PATH="../${REPO_BASE}--review-main"

# Create without -b flag (branch exists)
git worktree add "$WORKTREE_PATH" "$EXISTING_BRANCH"
cd "$WORKTREE_PATH"
```

## Removing Worktrees

**CRITICAL: Always check for unpushed commits before removing worktrees.**

### Safe Removal with Validation

Use `remove_worktree()` for safety-checked removal:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

# MUST be inside a worktree directory (not main repo)
cd "../repo--feature"

# Remove with safety checks
remove_worktree
```

**Safety checks performed:**
1. Confirms currently in worktree (not main repo)
2. Validates directory matches `repo--branch` pattern
3. Checks for unpushed commits (prevents data loss)
4. Removes worktree and deletes branch

### Manual Removal Process

If removing manually (without script):

```bash
# 1. Verify in worktree
if git rev-parse --git-dir | grep -q "worktrees"; then
  echo "In worktree"
else
  echo "ERROR: Not in worktree"
  exit 1
fi

# 2. Get current directory name
WORKTREE_DIR="$(basename "$PWD")"

# 3. Parse pattern
if [[ "$WORKTREE_DIR" == *--* ]]; then
  REPO="${WORKTREE_DIR%%--*}"
  BRANCH="${WORKTREE_DIR#*--}"
else
  echo "ERROR: Invalid pattern (missing --)"
  exit 1
fi

# 4. Check for unpushed commits
if ! git push --dry-run 2>&1 | grep -q "Everything up-to-date"; then
  echo "ERROR: Unpushed commits detected"
  echo "Push first: git push origin $BRANCH"
  exit 1
fi

# 5. Return to main repo
cd "../$REPO"

# 6. Remove worktree and branch
git worktree remove "$WORKTREE_DIR"
git branch -d "$BRANCH"
```

## Safety Features

### Unpushed Commit Detection

Before removing any worktree, verify work is pushed:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

# Check if worktree has unpushed commits
if check_unpushed_commits "$WORKTREE_PATH"; then
  echo "Safe to remove"
else
  echo "Has unpushed commits - push first"
fi
```

**What it checks:**
1. Branch exists on remote (has been pushed at least once)
2. No commits exist locally that aren't on remote
3. Prevents accidental data loss

### Pattern Validation

Validate directory names before operations:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

# Validate naming pattern
if validate_worktree_pattern "myrepo--feature"; then
  echo "Valid worktree pattern"
else
  echo "Invalid pattern - should be repo--branch"
fi
```

**Valid patterns:**
- `repo--branch`
- `my-repo--my-feature`
- `project123--bugfix-auth`

**Invalid patterns:**
- `repo` (no `--` separator)
- `--branch` (missing repo name)
- `repo--` (missing branch name)

### Repository Detection

Determine if currently in main repo or worktree:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

if is_main_repo; then
  echo "In main repository"
else
  echo "In linked worktree"
fi
```

Use this to prevent operations in wrong location.

## Integration with Plan Execution

When executing implementation plans via `/dev-workflow:execute-plan`, worktrees provide isolation:

**Workflow:**
1. User runs `/dev-workflow:execute-plan plan-file.md`
2. Command detects if in main repo
3. Asks user: "Create isolated worktree session for this work?"
4. If yes:
   - Creates worktree: `../repo--branch`
   - Switches to worktree: `cd ../repo--branch`
   - Continues execution in worktree (current session)
5. Work proceeds isolated from main repo
6. After completion, option to merge or create PR

**No Terminal spawning:** Everything happens in current session.

## Common Workflows

### Reviewing a Pull Request

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

# Fetch PR branch
git fetch origin pull/123/head:pr-123

# Create worktree for review
WORKTREE_PATH=$(create_worktree "pr-123")
cd "$WORKTREE_PATH"

# Review code, run tests, etc.

# When done
remove_worktree
```

### Parallel Development

```bash
# Main repo: working on feature-a
cd ~/projects/myapp

# Need to fix urgent bug without losing feature-a work
cd ..
WORKTREE_PATH=$(create_worktree "hotfix-login")
cd "myapp--hotfix-login"

# Fix bug, commit, push
git add .
git commit -m "fix: login validation"
git push origin hotfix-login

# Return to main work
cd ../myapp
```

### Cleaning Up Old Worktrees

List all worktrees:

```bash
git worktree list
```

For each old worktree:

```bash
cd ../repo--old-branch
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"
remove_worktree  # Includes safety checks
```

## Troubleshooting

### "Path exists" Error

**Problem:** Trying to create worktree but path already exists

**Solution:** Remove or rename existing directory first

```bash
# Check what's there
ls -la ../repo--branch

# If it's an old worktree
cd ../repo--branch
remove_worktree

# If it's not a worktree, manually remove
rm -rf ../repo--branch
```

### "Not in worktree" Error

**Problem:** Trying to remove from main repo

**Solution:** Only run `remove_worktree()` from inside a worktree directory

```bash
# Check current location
pwd
basename "$(pwd)"  # Should match repo--branch pattern

# Navigate to worktree first
cd ../repo--branch
remove_worktree
```

### "Invalid pattern" Error

**Problem:** Directory doesn't match `repo--branch` naming

**Solution:** Only remove worktrees created with standard pattern

This error prevents accidental deletion of unrelated directories.

### "Unpushed commits" Error

**Problem:** Worktree has commits not pushed to remote

**Solution:** Push commits before removing

```bash
# Push commits
git push origin branch-name

# Then remove
remove_worktree
```

## Quick Reference

**Create worktree:**
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"
WORKTREE_PATH=$(create_worktree "branch-name")
cd "$WORKTREE_PATH"
```

**Remove worktree:**
```bash
cd ../repo--branch
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"
remove_worktree
```

**List worktrees:**
```bash
git worktree list
```

**Check for unpushed commits:**
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"
check_unpushed_commits "$WORKTREE_PATH"
```

**Validate pattern:**
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"
validate_worktree_pattern "$(basename "$PWD")"
```

**Detect if in worktree:**
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"
is_main_repo && echo "main" || echo "worktree"
```

## Best Practices

1. **Always source worktree-manager.sh** - Use helper functions for safety
2. **Check for unpushed commits** - Never lose work by removing too early
3. **Follow naming pattern** - Keep `repo--branch` convention for clarity
4. **Clean up regularly** - Remove merged worktrees to avoid clutter
5. **One worktree per branch** - Don't create multiple worktrees for same branch
6. **Stay in current session** - No need for new terminals or windows
7. **Push before removing** - Safety check prevents data loss
