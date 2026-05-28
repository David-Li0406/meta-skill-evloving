---
name: finishing-a-development-branch
description: Guide completion of development work by presenting merge/PR options. Use when "I'm done", "merge this", "create PR", "finish up", or when implementation is complete and tests pass.
allowed-tools: Read, Bash, AskUserQuestion, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Finishing a Development Branch

Guide completion of development work by presenting clear options.

## When Invoked

After code review passes, tests pass, work is ready to integrate.

**Invoked by:**
- Post-swarm actions (after ExitPlanMode completes)
- Direct user request ("I'm done", "merge this", "create PR")

## Step 1: Verify Tests

```bash
npm test  # or cargo test / pytest / go test ./...
```

If tests fail: Stop. Cannot proceed until tests pass.

## Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null && BASE="main" || \
git merge-base HEAD master 2>/dev/null && BASE="master" || \
BASE="unknown"
```

If unknown, ask user which branch.

## Step 3: Present Options

Use AskUserQuestion:

```claude
AskUserQuestion:
  header: "Integration"
  question: "Work complete. How to proceed?"
  multiSelect: false
  options:
    - label: "Merge locally"
      description: "Rebase onto base, fast-forward merge (linear history)"
    - label: "Create PR"
      description: "Push branch and create Pull Request"
    - label: "Keep as-is"
      description: "Preserve branch and worktree for later"
    - label: "Discard"
      description: "Delete branch and all commits"
```

## Step 4: Execute Choice

### Option: Merge locally

Uses rebase for linear history (stacked-diffs approach):

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

FEATURE="$(git branch --show-current)"

# Safety check: uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "Error: Uncommitted changes. Commit first."
  exit 1
fi

# SAFETY: Push branch to remote BEFORE rebase (prevents data loss)
echo "Pushing branch to remote before rebase..."
git push -u origin "$FEATURE" || {
  echo "ERROR: Failed to push. Cannot proceed."
  echo "This prevents data loss - all work must be on remote before rebase."
  exit 1
}

# Verify push succeeded by comparing SHAs
LOCAL_SHA=$(git rev-parse "$FEATURE")
REMOTE_SHA=$(git ls-remote origin "$FEATURE" | cut -f1)
if [[ "$LOCAL_SHA" != "$REMOTE_SHA" ]]; then
  echo "ERROR: Local and remote are out of sync. Push may have failed."
  exit 1
fi
echo "Branch pushed successfully. Safe to proceed."

# Store original SHA for recovery reference
ORIGINAL_SHA="$LOCAL_SHA"

# Fetch latest changes
git fetch origin

# Rebase feature branch onto base (linear history)
echo "Rebasing $FEATURE onto origin/$BASE..."
if ! git rebase "origin/$BASE"; then
  echo ""
  echo "ERROR: Rebase conflict detected. Aborting rebase."

  # Abort to restore working state
  git rebase --abort

  echo ""
  echo "Your branch has been restored to its original state."
  echo "Original commit: $ORIGINAL_SHA"
  echo "Remote backup: origin/$FEATURE"
  echo ""
  echo "To resolve manually:"
  echo "  1. git rebase origin/$BASE"
  echo "  2. Resolve conflicts in each file"
  echo "  3. git add <resolved-files>"
  echo "  4. git rebase --continue"
  echo "  5. Re-run this merge process"
  exit 1
fi

echo "Rebase successful."

# Force push rebased branch (safe - we have backup on remote)
echo "Force pushing rebased branch..."
if ! git push --force-with-lease origin "$FEATURE"; then
  echo "ERROR: Force push failed."
  echo "This may happen if someone else pushed to this branch."
  echo "Your rebased changes are still local."
  echo "Remote backup exists at origin/$FEATURE (pre-rebase)"
  exit 1
fi

# Get main repo path
MAIN_REPO="$(get_main_worktree)"

# If in worktree, go to main repo for the merge
if ! is_main_repo; then
  cd "$MAIN_REPO"
fi

# Checkout base and fast-forward merge (no merge commit)
git checkout "$BASE"
git pull origin "$BASE" 2>/dev/null || true

echo "Fast-forward merging $FEATURE into $BASE..."
if ! git merge --ff-only "origin/$FEATURE"; then
  echo "ERROR: Fast-forward merge failed."
  echo "This should not happen after a successful rebase."
  echo "The base branch may have changed. Try again."
  exit 1
fi

npm test  # verify merged result
```

If tests pass and was in worktree:

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

# Clean up worktree if we were in one (not main repo)
if ! is_main_repo; then
  # remove_worktree has safety checks for unpushed commits
  remove_worktree
fi
```

Skip to Step 5.

### Option: Create PR

```bash
FEATURE=$(git branch --show-current)
git push -u origin $FEATURE
gh pr create --title "[title]" --body "## Summary\n[changes]\n\n## Tests\n- All passing"
```

Proceed to Step 5.

### Option: Keep as-is

Report branch and worktree location. Skip Step 5. Return.

### Option: Discard

**First, check for unpushed commits and warn user:**

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

FEATURE="$(git branch --show-current)"

# Check if branch has unpushed commits
if ! git ls-remote --heads origin "$FEATURE" 2>/dev/null | grep -q .; then
  echo "WARNING: Branch '$FEATURE' has NEVER been pushed to remote!"
  echo "Discarding will PERMANENTLY delete all work on this branch."
elif [[ -n "$(git log origin/$FEATURE..$FEATURE --oneline 2>/dev/null)" ]]; then
  echo "WARNING: Branch '$FEATURE' has unpushed commits:"
  git log "origin/$FEATURE..$FEATURE" --oneline
  echo "Discarding will PERMANENTLY delete these commits."
fi
```

Then confirm with AskUserQuestion:

```claude
AskUserQuestion:
  header: "Confirm"
  question: "Discard all work on this branch? This CANNOT be undone."
  multiSelect: false
  options:
    - label: "Yes, discard permanently"
      description: "Delete branch and all commits - NO recovery possible"
    - label: "Cancel"
      description: "Return to integration options"
```

**If user confirms discard:**

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-manager.sh"

FEATURE="$(git branch --show-current)"

# If in worktree, go to main repo first
if ! is_main_repo; then
  WORKTREE_PATH="$(pwd)"
  MAIN_REPO="$(get_main_worktree)"
  cd "$MAIN_REPO"
  # Force remove worktree (user explicitly confirmed discard)
  git worktree remove --force "$WORKTREE_PATH"
fi

# Force delete branch (user explicitly confirmed discard)
git checkout "$BASE"
git branch -D "$FEATURE"
```

Proceed to Step 5.

## Step 5: Report Completion

Report:

```text
Branch finished:
- Action: [Merged / PR created / Discarded]
- Branch: [name]
- Worktree: [cleaned up / preserved]
```

Return to caller.
