#!/usr/bin/env bash
# Analyze stack health and suggest actions
# Part of stackit Claude Code skill

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=== Stack Health Analysis ==="
echo

# Check if stackit is installed
if ! command -v stackit &> /dev/null; then
    echo -e "${RED}❌ stackit not found${NC}"
    echo "→ Install from: https://github.com/getstackit/stackit"
    exit 1
fi

# Check if in git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not a git repository${NC}"
    exit 1
fi

# Check if stackit is initialized
if ! stackit log > /dev/null 2>&1; then
    echo -e "${RED}❌ Stackit not initialized in this repository${NC}"
    echo "→ Run: stackit init"
    exit 1
fi

echo -e "${BLUE}Current Stack:${NC}"
stackit log
echo

echo -e "${BLUE}Health Checks:${NC}"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    echo "→ Run: git status"
    echo "→ Consider: git add . && stackit modify"
    echo
fi

# Check for branches without PRs
# Count branches marked with ● (no PR) in stackit log output
branches_no_pr=$(stackit log 2>/dev/null | grep -c "●" || true)
if [ "$branches_no_pr" -gt 0 ]; then
    echo -e "${YELLOW}ℹ️  $branches_no_pr branch(es) without PRs${NC}"
    echo "→ Run: stackit submit --stack"
    echo
fi

# Check if sync needed (look for merged PRs)
if stackit log full 2>&1 | grep -qi "merged\|closed"; then
    echo -e "${YELLOW}ℹ️  Some PRs have been merged/closed${NC}"
    echo "→ Run: stackit sync --restack"
    echo
fi

# Check for rebase in progress
if [ -d "$(git rev-parse --git-dir)/rebase-merge" ] || [ -d "$(git rev-parse --git-dir)/rebase-apply" ]; then
    echo -e "${RED}⚠️  Rebase in progress${NC}"
    echo "→ Resolve conflicts and run: stackit continue"
    echo "→ Or abort with: stackit abort"
    echo
fi

# Get current branch
current_branch=$(git branch --show-current)

# Check if on trunk
trunk_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
if [ "$current_branch" = "$trunk_branch" ]; then
    echo -e "${YELLOW}ℹ️  Currently on trunk branch ($trunk_branch)${NC}"
    echo "→ Consider: stackit checkout (to switch to a feature branch)"
    echo
fi

# Check for large branches that might need splitting
echo -e "${BLUE}Branch Size Analysis:${NC}"
large_branch_found=false

# Get list of tracked branches (non-trunk branches in the stack)
tracked_branches=$(stackit log --no-interactive 2>/dev/null | grep -oE '[a-zA-Z0-9_/-]+' | grep -v "^main$\|^master$\|^$trunk_branch$" | sort -u)

for branch in $tracked_branches; do
    # Skip if branch doesn't exist
    if ! git rev-parse --verify "$branch" > /dev/null 2>&1; then
        continue
    fi

    # Get parent branch (the branch this one is based on)
    parent=$(git log --format=%D "$branch" -1 2>/dev/null | grep -oE 'origin/[^,]+' | head -1 | sed 's|origin/||' || echo "$trunk_branch")
    if [ -z "$parent" ]; then
        parent="$trunk_branch"
    fi

    # Calculate diff stats against merge-base with trunk
    merge_base=$(git merge-base "$trunk_branch" "$branch" 2>/dev/null || echo "")
    if [ -n "$merge_base" ]; then
        # Get stats: files changed, insertions, deletions
        stats=$(git diff --shortstat "$merge_base".."$branch" 2>/dev/null || echo "")
        if [ -n "$stats" ]; then
            files_changed=$(echo "$stats" | grep -oE '[0-9]+ file' | grep -oE '[0-9]+' || echo "0")
            insertions=$(echo "$stats" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
            deletions=$(echo "$stats" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")
            total_lines=$((insertions + deletions))

            # Warn if branch is large (>500 lines or >10 files)
            if [ "$total_lines" -gt 500 ] || [ "$files_changed" -gt 10 ]; then
                if [ "$large_branch_found" = false ]; then
                    large_branch_found=true
                fi
                echo -e "${YELLOW}⚠️  Large branch: $branch${NC}"
                echo "   $files_changed files, +$insertions/-$deletions lines ($total_lines total)"
                echo "→ Consider: stackit split (to break into smaller PRs)"
                echo
            fi
        fi
    fi
done

if [ "$large_branch_found" = false ]; then
    echo -e "${GREEN}✓ All branches are reasonably sized${NC}"
    echo
fi

# Run stackit doctor for additional diagnostics
echo -e "${BLUE}Running stackit doctor:${NC}"
if stackit doctor > /dev/null 2>&1; then
    echo -e "${GREEN}✓ No issues detected${NC}"
else
    echo -e "${YELLOW}⚠️  Stackit doctor found issues${NC}"
    echo "→ Run: stackit doctor (for details)"
    echo
fi

echo
echo "=== Analysis Complete ==="

# Suggest next action based on state
echo
echo -e "${BLUE}Suggested Next Steps:${NC}"

if [ "$branches_no_pr" -gt 0 ]; then
    echo "1. Submit branches: stackit submit --stack"
elif stackit log full 2>&1 | grep -qi "merged\|closed"; then
    echo "1. Sync with trunk: stackit sync --restack"
elif ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "1. Commit changes: git add . && stackit modify"
else
    echo -e "${GREEN}✓ Stack is healthy! Ready for development.${NC}"
fi
