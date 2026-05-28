---
name: git-st
description: Check development status - uncommitted changes, last commit, beads tasks, and PR status
invocation: /bkff:git-st
arguments: []
---

# Git Status Check

Displays comprehensive status of the current git worktree including:
- Uncommitted changes (staged and unstaged)
- Last commit information
- In-progress beads tasks
- Pull request status

## Usage

```
/bkff:git-st
```

No arguments required. Operates on the current working directory.

## Output Sections

### Working Directory
Shows the current branch name and a summary of changes:
- Number of staged files
- Number of unstaged files
- Number of untracked files

### Staged/Unstaged Changes
Lists files with their status:
- `A` - Added (new file)
- `M` - Modified
- `D` - Deleted
- `R` - Renamed
- `?` - Untracked

### Last Commit
Shows information about the most recent commit:
- Short hash
- Commit message
- Author name
- Relative date

### Beads Task
Shows any in-progress beads issues associated with the current work.

### Pull Request
If a PR exists for the current branch, shows:
- PR number and title
- Status (open/closed/merged)
- Check status (passing/failing/pending)
- URL link

## Requirements

- Must be run inside a git worktree
- `git` CLI for status and commit info
- `gh` CLI for PR status (optional - graceful fallback)
- `bd` CLI for beads task status (optional - graceful fallback)

## Examples

### With Changes
```
## Git Status

### Working Directory
- **Branch**: feature/auth-login
- **Status**: 3 files changed (2 staged, 1 unstaged)

### Staged Changes
  A  src/new-file.ts
  M  src/auth.ts

### Unstaged Changes
  M  README.md

### Last Commit
- **Hash**: abc1234
- **Message**: feat(auth): add login endpoint
- **Date**: 2 hours ago

### Pull Request
- **PR #42**: Add authentication feature
- **Status**: Open (checks passing)
```

### Clean State
```
## Git Status

### Working Directory
- **Branch**: main
- **Status**: Clean (no uncommitted changes)

### Last Commit
- **Hash**: def5678
- **Message**: chore: update dependencies
- **Date**: 1 day ago

### Pull Request
- No PR exists for this branch
```

## Implementation

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$PLUGIN_DIR/lib/common.sh"
source "$PLUGIN_DIR/lib/git-helpers.sh"

require_worktree

echo "## Git Status"
echo ""

# Working Directory
branch=$(get_current_branch)
staged=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
unstaged=$(git diff --name-only 2>/dev/null | wc -l | tr -d ' ')
untracked=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
total=$((staged + unstaged + untracked))

echo "### Working Directory"
echo "- **Branch**: $branch ($(get_branch_status "$branch"))"
if [[ $total -eq 0 ]]; then
    echo "- **Status**: Clean (no uncommitted changes)"
else
    parts=()
    [[ $staged -gt 0 ]] && parts+=("$staged staged")
    [[ $unstaged -gt 0 ]] && parts+=("$unstaged unstaged")
    [[ $untracked -gt 0 ]] && parts+=("$untracked untracked")
    echo "- **Status**: $total files changed ($(IFS=", "; echo "${parts[*]}"))"
fi
echo ""

# Staged Changes
staged_files=$(git diff --cached --name-status 2>/dev/null)
if [[ -n "$staged_files" ]]; then
    echo "### Staged Changes"
    echo "$staged_files" | while IFS=$'\t' read -r status file; do
        printf "  %s  %s\n" "$status" "$file"
    done
    echo ""
fi

# Unstaged Changes
unstaged_files=$(git diff --name-status 2>/dev/null)
if [[ -n "$unstaged_files" ]]; then
    echo "### Unstaged Changes"
    echo "$unstaged_files" | while IFS=$'\t' read -r status file; do
        printf "  %s  %s\n" "$status" "$file"
    done
    echo ""
fi

# Untracked Files
untracked_list=$(git ls-files --others --exclude-standard 2>/dev/null)
if [[ -n "$untracked_list" ]]; then
    echo "### Untracked Files"
    echo "$untracked_list" | while read -r file; do
        printf "  ?  %s\n" "$file"
    done
    echo ""
fi

# Last Commit
echo "### Last Commit"
hash=$(get_last_commit_hash)
if [[ -n "$hash" ]]; then
    echo "- **Hash**: $hash"
    echo "- **Message**: $(get_last_commit_subject)"
    echo "- **Author**: $(get_last_commit_author)"
    echo "- **Date**: $(get_last_commit_date)"
else
    echo "- No commits yet"
fi
echo ""

# Beads Task
echo "### Beads Task"
if command -v bd &>/dev/null; then
    tasks=$(bd list --status=in_progress --json 2>/dev/null || echo "[]")
    if [[ "$tasks" != "[]" && -n "$tasks" ]]; then
        id=$(echo "$tasks" | jq -r '.[0].id // empty' 2>/dev/null)
        title=$(echo "$tasks" | jq -r '.[0].title // empty' 2>/dev/null)
        [[ -n "$id" ]] && echo "- **Issue**: $id" && echo "- **Title**: $title" || echo "- No in-progress tasks"
    else
        echo "- No in-progress tasks"
    fi
else
    echo "- bd CLI not available"
fi
echo ""

# Pull Request
echo "### Pull Request"
if command -v gh &>/dev/null; then
    main_branch=$(get_main_branch 2>/dev/null || echo "main")
    if [[ "$branch" != "$main_branch" && "$branch" != "master" ]]; then
        pr_json=$(gh pr list --head "$branch" --json number,title,state,url 2>/dev/null || echo "[]")
        if [[ -n "$pr_json" && "$pr_json" != "[]" ]]; then
            number=$(echo "$pr_json" | jq -r '.[0].number')
            title=$(echo "$pr_json" | jq -r '.[0].title')
            state=$(echo "$pr_json" | jq -r '.[0].state')
            url=$(echo "$pr_json" | jq -r '.[0].url')
            echo "- **PR #$number**: $title"
            echo "- **Status**: ${state^}"
            echo "- **URL**: $url"
        else
            echo "- No PR exists for this branch"
        fi
    else
        echo "- N/A (on $branch branch)"
    fi
else
    echo "- gh CLI not available"
fi
```
