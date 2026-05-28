---
name: git-sync
description: Sync with remote using smart rebase/merge selection based on push status
invocation: /bkff:git-sync
arguments:
  - name: source-branch
    type: string
    required: false
    description: Branch to sync from (default: main)
---

# Sync with Remote

Fetches from origin and integrates changes from a source branch. Automatically chooses rebase (for unpushed branches) or merge (for pushed branches) strategy.

## Usage

```
/bkff:git-sync [source-branch]
```

## Strategy Selection

| Condition | Strategy |
|-----------|----------|
| Branch not pushed to origin | Rebase (clean history) |
| Branch already pushed to origin | Merge (preserve history) |

## Example Output

```
## Sync Complete (Rebase)

### Fetch
- ✓ Fetched from origin

### Strategy
- **Mode**: Rebase (branch not yet pushed)
- **Source**: main

### Result
- **Status**: Up to date with main
```

## Requirements

- Must be run inside a git worktree
- `git` CLI with rerere enabled recommended
- No uncommitted changes

## Implementation

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$PLUGIN_DIR/lib/common.sh"
source "$PLUGIN_DIR/lib/git-helpers.sh"

require_worktree

SOURCE_BRANCH="${1:-$(get_main_branch)}"
CURRENT_BRANCH=$(get_current_branch)

# Check for uncommitted changes
if has_changes; then
    error_exit "You have uncommitted changes. Commit or stash before syncing."
fi

# Prevent syncing main onto itself
if [[ "$CURRENT_BRANCH" == "$SOURCE_BRANCH" ]]; then
    error_exit "Already on $SOURCE_BRANCH. Nothing to sync."
fi

echo "## Sync Process"
echo ""

# FR-018: Fetch from origin
echo "### Fetch"
info "Fetching from origin..."
if git fetch origin --prune; then
    echo "- ✓ Fetched from origin"
else
    error_exit "Fetch failed. Check network connection."
fi
echo ""

# Verify source branch exists
if ! git rev-parse --verify "origin/$SOURCE_BRANCH" &>/dev/null; then
    error_exit "Branch '$SOURCE_BRANCH' not found on origin."
fi

# FR-019: Determine if branch has been pushed
echo "### Strategy"
if is_branch_pushed "$CURRENT_BRANCH"; then
    STRATEGY="merge"
    echo "- **Mode**: Merge (branch already pushed to origin)"
else
    STRATEGY="rebase"
    echo "- **Mode**: Rebase (branch not yet pushed)"
fi
echo "- **Source**: $SOURCE_BRANCH"
echo "- **Target**: $CURRENT_BRANCH"
echo ""

# Enable rerere for conflict resolution
git config rerere.enabled true

# FR-020/FR-021: Execute strategy
echo "### Result"
if [[ "$STRATEGY" == "rebase" ]]; then
    # FR-020: Rebase for unpushed branches
    info "Rebasing onto origin/$SOURCE_BRANCH..."
    if git rebase "origin/$SOURCE_BRANCH"; then
        COMMITS=$(git rev-list --count "origin/$SOURCE_BRANCH..HEAD" 2>/dev/null || echo "0")
        echo "- **Commits rebased**: $COMMITS"
        echo "- **Conflicts**: None"
        echo "- **Status**: Up to date with $SOURCE_BRANCH"
        echo ""
        success "Branch rebased successfully. Ready to push."
    else
        echo "- **Status**: Conflicts require resolution"
        echo ""
        echo "### Conflicts"
        git diff --name-only --diff-filter=U | while read -r file; do
            echo "- $file"
        done
        echo ""
        echo "### Next Steps"
        echo "1. Resolve conflicts in the files above"
        echo "2. Stage resolved files: git add <file>"
        echo "3. Continue rebase: git rebase --continue"
        echo ""
        echo "Or abort: git rebase --abort"
        exit 1
    fi
else
    # FR-021: Merge for pushed branches
    info "Merging origin/$SOURCE_BRANCH..."
    if git merge "origin/$SOURCE_BRANCH" -m "Merge $SOURCE_BRANCH into $CURRENT_BRANCH"; then
        MERGE_HASH=$(git rev-parse --short HEAD)
        echo "- **Merge commit**: $MERGE_HASH"
        echo "- **Conflicts**: None"
        echo "- **Status**: Up to date with $SOURCE_BRANCH"
        echo ""
        success "Branch merged successfully."
    else
        echo "- **Status**: Conflicts require resolution"
        echo ""
        echo "### Conflicts"
        git diff --name-only --diff-filter=U | while read -r file; do
            echo "- $file"
        done
        echo ""
        echo "### Next Steps"
        echo "1. Resolve conflicts in the files above"
        echo "2. Stage resolved files: git add <file>"
        echo "3. Complete merge: git commit"
        echo ""
        echo "Or abort: git merge --abort"
        exit 1
    fi
fi
```
