---
name: git-branch
description: Create a new feature branch from a beads issue with proper prefix, worktree, and beads initialization
invocation: /bkff:git-branch
arguments:
  - name: issue-id
    type: string
    required: true
    description: Beads issue identifier (e.g., beads-042, tool-abc)
---

# Create Feature Branch

Creates a new git branch and worktree from a beads issue. Automatically determines the branch type prefix based on issue type and priority, pushes to origin, and initializes beads database.

## Usage

```
/bkff:git-branch <issue-id>
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `issue-id` | Yes | Beads issue ID (e.g., `beads-042`, `tool-abc`) |

## Branch Prefix Logic

| Issue Type | Priority | Branch Prefix |
|------------|----------|---------------|
| `feature` | any | `feature/` |
| `bug` | P2-P4 (medium-backlog) | `bugfix/` |
| `bug` | P0-P1 (critical-high) | `hotfix/` |
| `task` | any | `feature/` |

## What It Does

1. Validates the beads issue exists
2. Determines branch prefix from issue type/priority
3. Creates a new worktree directory (sibling to current worktree)
4. Creates and checks out the new branch
5. Pushes the branch to origin
6. Initializes beads database in new worktree
7. Syncs beads with remote

## Example Output

```
## Branch Created

- **Issue**: tool-abc - Implement user authentication
- **Branch**: feature/tool-abc-implement-user-authent
- **Worktree**: /path/to/repo/tool-abc-implement-user-
- **Pushed**: Yes

To start working: cd /path/to/repo/tool-abc-implement-user-
```

## Requirements

- Must be run inside a git worktree
- `git` CLI for branch and worktree operations
- `bd` CLI for issue retrieval and beads initialization
- `jq` for JSON parsing

## Error Cases

- **Invalid issue ID**: Shows list of valid open issues
- **Branch already exists**: Error with existing branch name
- **Worktree path exists**: Error with existing directory path
- **Push failed**: Warning (branch still created locally)

## Implementation

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$PLUGIN_DIR/lib/common.sh"
source "$PLUGIN_DIR/lib/git-helpers.sh"

require_worktree

ISSUE_ID="${1:-}"
[[ -z "$ISSUE_ID" ]] && error_exit "Usage: git-branch <issue-id>"

command -v bd &>/dev/null || error_exit "bd CLI required"

ISSUE_JSON=$(bd show "$ISSUE_ID" --json 2>/dev/null) || {
    echo "Error: Issue '$ISSUE_ID' not found." >&2
    bd list --status=open --limit=10 2>/dev/null >&2
    exit 1
}

ISSUE_TITLE=$(echo "$ISSUE_JSON" | jq -r '.title // empty')
ISSUE_TYPE=$(echo "$ISSUE_JSON" | jq -r '.issue_type // "task"')
ISSUE_PRIORITY=$(echo "$ISSUE_JSON" | jq -r '.priority // 2')

case "$ISSUE_TYPE" in
    bug) [[ "$ISSUE_PRIORITY" -le 1 ]] && BRANCH_PREFIX="hotfix" || BRANCH_PREFIX="bugfix" ;;
    *) BRANCH_PREFIX="feature" ;;
esac

SANITIZED=$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | tr -s '-' | cut -c1-30)
BRANCH_NAME="${BRANCH_PREFIX}/${ISSUE_ID}-${SANITIZED}"

git rev-parse --verify "$BRANCH_NAME" &>/dev/null && error_exit "Branch '$BRANCH_NAME' already exists"

WORKTREE_BASE=$(dirname "$(get_worktree_path)")
WORKTREE_DIR="${WORKTREE_BASE}/${ISSUE_ID}-$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | tr -s '-' | cut -c1-20)"

[[ -d "$WORKTREE_DIR" ]] && error_exit "Directory '$WORKTREE_DIR' already exists"

MAIN_BRANCH=$(get_main_branch)
info "Creating worktree for $ISSUE_ID..."
git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR" "$MAIN_BRANCH" || error_exit "Failed to create worktree"
success "Created worktree at $WORKTREE_DIR"

info "Pushing branch to origin..."
(cd "$WORKTREE_DIR" && git push -u origin "$BRANCH_NAME") || warn "Push failed"
PUSH_STATUS="${PUSH_STATUS:-Yes}"

info "Initializing beads..."
(cd "$WORKTREE_DIR" && bd init && bd sync) 2>/dev/null || warn "Beads init/sync failed"

echo ""
echo "## Branch Created"
echo "- **Issue**: $ISSUE_ID - $ISSUE_TITLE"
echo "- **Branch**: $BRANCH_NAME"
echo "- **Worktree**: $WORKTREE_DIR"
echo "- **Pushed**: $PUSH_STATUS"
echo ""
echo "To start working: cd $WORKTREE_DIR"
```
