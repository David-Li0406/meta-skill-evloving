#!/bin/bash
# git-sync-check.sh - Check git status across key repositories
# Used by github-sync skill for session start checks

set -e

# Daily rate limiting - only run once per 24 hours unless forced
LAST_RUN_FILE="$HOME/.claude/.git-sync-last-run"
REPO_CACHE_FILE="$HOME/.claude/.git-repos-cache"
REPO_CACHE_MAX_AGE=604800  # 7 days in seconds
COOLDOWN_SECONDS=86400  # 24 hours
MAX_PARALLEL_FETCH=5  # P2-PERF-001: Limit parallel git fetches

# Check if --force flag is passed
FORCE=false
if [ "$1" = "--force" ] || [ "$1" = "-f" ]; then
    FORCE=true
fi

if [ "$FORCE" = false ] && [ -f "$LAST_RUN_FILE" ]; then
    LAST_RUN=$(cat "$LAST_RUN_FILE" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    ELAPSED=$((NOW - LAST_RUN))

    if [ "$ELAPSED" -lt "$COOLDOWN_SECONDS" ]; then
        HOURS_LEFT=$(( (COOLDOWN_SECONDS - ELAPSED) / 3600 ))
        # Silently skip - don't output anything
        exit 0
    fi
fi

# Record this run
mkdir -p "$HOME/.claude"
date +%s > "$LAST_RUN_FILE"

# ANSI colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# P2-PERF-002: Use cached repo list if available and fresh
find_git_repos() {
    find "$HOME" -maxdepth 4 -name ".git" -type d 2>/dev/null | \
        grep -v "/Library/" | \
        grep -v "/.Trash/" | \
        grep -v "/node_modules/" | \
        grep -v "/.npm/" | \
        grep -v "/.cache/" | \
        grep -v "/.local/" | \
        grep -v "/.cargo/" | \
        grep -v "/.rustup/" | \
        grep -v "/vendor/" | \
        grep -v "/.gem/" | \
        grep -v "/go/pkg/" | \
        grep -v "/.cocoapods/" | \
        grep -v "/Pods/" | \
        grep -v "/.claude/" | \
        sort
}

# Check if cache is fresh (less than 7 days old)
cache_is_fresh() {
    if [ ! -f "$REPO_CACHE_FILE" ]; then
        return 1
    fi
    local cache_mtime
    cache_mtime=$(stat -f %m "$REPO_CACHE_FILE" 2>/dev/null || stat -c %Y "$REPO_CACHE_FILE" 2>/dev/null || echo 0)
    local now=$(date +%s)
    local age=$((now - cache_mtime))
    [ "$age" -lt "$REPO_CACHE_MAX_AGE" ]
}

# Get repos from cache or rebuild
REPOS=()
if [ "$FORCE" = true ] || ! cache_is_fresh; then
    # Rebuild cache
    find_git_repos > "$REPO_CACHE_FILE"
fi

while IFS= read -r repo; do
    # Get the parent directory (the actual repo, not .git)
    repo_dir=$(dirname "$repo")
    # Verify repo still exists (cache might be stale)
    [ -d "$repo_dir/.git" ] && REPOS+=("$repo_dir")
done < "$REPO_CACHE_FILE"

echo "========================================"
echo "Git Sync Status Check"
echo "========================================"
echo ""

# P2-PERF-001: Parallel git fetch with limited concurrency
echo "Fetching updates from remotes..."
running=0
for REPO in "${REPOS[@]}"; do
    if [ -d "$REPO/.git" ]; then
        (cd "$REPO" && git fetch origin 2>/dev/null) &
        ((running++))
        if [ "$running" -ge "$MAX_PARALLEL_FETCH" ]; then
            wait -n 2>/dev/null || wait  # wait -n not available on older bash
            ((running--))
        fi
    fi
done
wait  # Wait for remaining fetches
echo ""

ISSUES_FOUND=false

for REPO in "${REPOS[@]}"; do
    if [ ! -d "$REPO/.git" ]; then
        continue
    fi

    REPO_NAME=$(basename "$REPO")
    echo -e "${BLUE}[$REPO_NAME]${NC} $REPO"

    cd "$REPO"

    # Get default branch
    DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

    # Check for uncommitted changes
    UNCOMMITTED=$(git status --porcelain 2>/dev/null)
    if [ -n "$UNCOMMITTED" ]; then
        echo -e "  ${YELLOW}! Uncommitted changes:${NC}"
        echo "$UNCOMMITTED" | head -10 | sed 's/^/    /'
        COUNT=$(echo "$UNCOMMITTED" | wc -l | tr -d ' ')
        if [ "$COUNT" -gt 10 ]; then
            echo "    ... and $((COUNT - 10)) more"
        fi
        ISSUES_FOUND=true
    fi

    # Check for unpushed commits
    UNPUSHED=$(git log origin/$DEFAULT_BRANCH..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [ "$UNPUSHED" != "0" ]; then
        echo -e "  ${YELLOW}! $UNPUSHED unpushed commit(s)${NC}"
        git log origin/$DEFAULT_BRANCH..HEAD --oneline 2>/dev/null | head -5 | sed 's/^/    /'
        if [ "$UNPUSHED" -gt 5 ]; then
            echo "    ... and $((UNPUSHED - 5)) more"
        fi
        ISSUES_FOUND=true
    fi

    # Check if behind remote
    BEHIND=$(git log HEAD..origin/$DEFAULT_BRANCH --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [ "$BEHIND" != "0" ]; then
        echo -e "  ${RED}! $BEHIND commit(s) behind remote${NC}"
        git log HEAD..origin/$DEFAULT_BRANCH --oneline 2>/dev/null | head -5 | sed 's/^/    /'
        if [ "$BEHIND" -gt 5 ]; then
            echo "    ... and $((BEHIND - 5)) more"
        fi
        ISSUES_FOUND=true
    fi

    # Check for stashed changes
    STASH_COUNT=$(git stash list 2>/dev/null | wc -l | tr -d ' ')
    if [ "$STASH_COUNT" != "0" ]; then
        echo -e "  ${YELLOW}! $STASH_COUNT stashed change(s)${NC}"
        ISSUES_FOUND=true
    fi

    # If nothing found, show clean status
    if [ -z "$UNCOMMITTED" ] && [ "$UNPUSHED" = "0" ] && [ "$BEHIND" = "0" ] && [ "$STASH_COUNT" = "0" ]; then
        echo -e "  ${GREEN}✓ Clean and up to date${NC}"
    fi

    echo ""
done

echo "========================================"

# Check CI status for repos with GitHub Actions
echo ""
echo "========================================"
echo "CI Status Check"
echo "========================================"
echo ""

for REPO in "${REPOS[@]}"; do
    if [ ! -d "$REPO/.git" ]; then
        continue
    fi

    cd "$REPO"

    # Check if this repo has a GitHub remote
    GITHUB_URL=$(git remote get-url origin 2>/dev/null | grep -i github || echo "")
    if [ -z "$GITHUB_URL" ]; then
        continue
    fi

    # Extract owner/repo from URL
    REPO_SLUG=$(echo "$GITHUB_URL" | sed -E 's/.*github\.com[:/]([^/]+\/[^/.]+)(\.git)?$/\1/')
    REPO_NAME=$(basename "$REPO")

    if [ -z "$REPO_SLUG" ]; then
        continue
    fi

    echo -e "${BLUE}[$REPO_NAME]${NC}"

    # Get the last workflow run status using gh CLI
    CI_STATUS=$(gh run list --repo "$REPO_SLUG" --limit 1 --json conclusion,status,name,headBranch,createdAt 2>/dev/null || echo "")

    if [ -z "$CI_STATUS" ] || [ "$CI_STATUS" = "[]" ]; then
        echo "  No CI workflows found"
    else
        CONCLUSION=$(echo "$CI_STATUS" | grep -o '"conclusion":"[^"]*"' | head -1 | cut -d'"' -f4)
        STATUS=$(echo "$CI_STATUS" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
        WORKFLOW_NAME=$(echo "$CI_STATUS" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
        BRANCH=$(echo "$CI_STATUS" | grep -o '"headBranch":"[^"]*"' | head -1 | cut -d'"' -f4)

        if [ "$STATUS" = "in_progress" ] || [ "$STATUS" = "queued" ]; then
            echo -e "  ${YELLOW}⏳ $WORKFLOW_NAME is running on $BRANCH${NC}"
        elif [ "$CONCLUSION" = "success" ]; then
            echo -e "  ${GREEN}✓ $WORKFLOW_NAME passed on $BRANCH${NC}"
        elif [ "$CONCLUSION" = "failure" ]; then
            echo -e "  ${RED}✗ $WORKFLOW_NAME FAILED on $BRANCH${NC}"
            echo -e "  ${YELLOW}  Run 'gh run view --repo $REPO_SLUG' for details${NC}"
            ISSUES_FOUND=true
        elif [ "$CONCLUSION" = "cancelled" ]; then
            echo -e "  ${YELLOW}⊘ $WORKFLOW_NAME was cancelled on $BRANCH${NC}"
        else
            echo "  Last run: $CONCLUSION ($STATUS)"
        fi
    fi
    echo ""
done

echo "========================================"

if [ "$ISSUES_FOUND" = true ]; then
    echo -e "${YELLOW}Action may be needed. Review above.${NC}"
    exit 1
else
    echo -e "${GREEN}All checks complete.${NC}"
    exit 0
fi
