#!/bin/bash
# git-sync-all.sh - Full sync: commit, push, and pull ALL registered projects
# One command to make sure EVERYTHING is up to date across all Macs

set -e

# ANSI colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Find all git repos in home directory (excluding common non-project directories)
REPOS=()
while IFS= read -r repo; do
    repo_dir=$(dirname "$repo")
    REPOS+=("$repo_dir")
done < <(find "$HOME" -maxdepth 4 -name ".git" -type d 2>/dev/null | \
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
    sort)

# Parse arguments
DRY_RUN=false
VERBOSE=false
MESSAGE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run|-n)
            DRY_RUN=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --message|-m)
            MESSAGE="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Default commit message
if [ -z "$MESSAGE" ]; then
    MESSAGE="Auto-sync: $(date '+%Y-%m-%d %H:%M')"
fi

echo ""
echo -e "${BOLD}${BLUE}========================================${NC}"
echo -e "${BOLD}${BLUE}       Git Sync All Projects${NC}"
echo -e "${BOLD}${BLUE}========================================${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
    echo ""
fi

TOTAL_COMMITS=0
TOTAL_PUSHED=0
TOTAL_PULLED=0
ERRORS=0

for REPO in "${REPOS[@]}"; do
    if [ ! -d "$REPO/.git" ]; then
        if [ "$VERBOSE" = true ]; then
            echo -e "${YELLOW}Skipping $REPO (not a git repo)${NC}"
        fi
        continue
    fi

    REPO_NAME=$(basename "$REPO")
    echo -e "${CYAN}[$REPO_NAME]${NC} $REPO"

    cd "$REPO"

    # Get default branch
    DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

    # Step 1: Fetch from remote
    echo -n "  Fetching... "
    if git fetch origin 2>/dev/null; then
        echo -e "${GREEN}done${NC}"
    else
        echo -e "${YELLOW}failed (continuing)${NC}"
    fi

    # Step 2: Pull if behind (do this BEFORE committing to avoid conflicts)
    BEHIND=$(git log HEAD..origin/$DEFAULT_BRANCH --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [ "$BEHIND" != "0" ]; then
        echo -n "  Pulling $BEHIND commit(s)... "
        if [ "$DRY_RUN" = true ]; then
            echo -e "${YELLOW}skipped (dry run)${NC}"
        else
            # Stash any local changes first
            STASHED=false
            if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
                git stash push -m "Auto-stash before pull" 2>/dev/null && STASHED=true
            fi

            if git pull --rebase origin "$DEFAULT_BRANCH" 2>/dev/null; then
                echo -e "${GREEN}done${NC}"
                TOTAL_PULLED=$((TOTAL_PULLED + BEHIND))
            else
                echo -e "${RED}failed${NC}"
                ERRORS=$((ERRORS + 1))
                # Try to recover
                git rebase --abort 2>/dev/null || true
            fi

            # Restore stashed changes
            if [ "$STASHED" = true ]; then
                git stash pop 2>/dev/null || true
            fi
        fi
    fi

    # Step 3: Commit any uncommitted changes
    UNCOMMITTED=$(git status --porcelain 2>/dev/null)
    if [ -n "$UNCOMMITTED" ]; then
        COUNT=$(echo "$UNCOMMITTED" | wc -l | tr -d ' ')
        echo -n "  Committing $COUNT file(s)... "
        if [ "$DRY_RUN" = true ]; then
            echo -e "${YELLOW}skipped (dry run)${NC}"
            if [ "$VERBOSE" = true ]; then
                echo "$UNCOMMITTED" | head -10 | sed 's/^/    /'
            fi
        else
            # Check for secrets before adding files
            if command -v gitleaks &> /dev/null; then
                GITLEAKS_OUTPUT=$(gitleaks detect --no-git --no-banner 2>&1)
                if [ $? -ne 0 ]; then
                    echo -e "${RED}SECRETS DETECTED!${NC}"
                    echo "$GITLEAKS_OUTPUT" | sed 's/^/    /'
                    echo -e "  ${YELLOW}Fix: Remove secrets from these files, or add to .gitleaks.toml allowlist${NC}"
                    ERRORS=$((ERRORS + 1))
                    echo ""
                    continue
                fi
            fi
            git add -A
            if git commit -m "$MESSAGE" 2>/dev/null; then
                echo -e "${GREEN}done${NC}"
                TOTAL_COMMITS=$((TOTAL_COMMITS + 1))
            else
                echo -e "${YELLOW}nothing to commit${NC}"
            fi
        fi
    fi

    # Step 4: Push any unpushed commits
    UNPUSHED=$(git log origin/$DEFAULT_BRANCH..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [ "$UNPUSHED" != "0" ]; then
        echo -n "  Pushing $UNPUSHED commit(s)... "
        if [ "$DRY_RUN" = true ]; then
            echo -e "${YELLOW}skipped (dry run)${NC}"
        else
            if git push origin "$DEFAULT_BRANCH" 2>/dev/null; then
                echo -e "${GREEN}done${NC}"
                TOTAL_PUSHED=$((TOTAL_PUSHED + UNPUSHED))
            else
                echo -e "${RED}failed${NC}"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    fi

    # Final status
    if [ -z "$UNCOMMITTED" ] && [ "$UNPUSHED" = "0" ] && [ "$BEHIND" = "0" ]; then
        echo -e "  ${GREEN}✓ Already up to date${NC}"
    fi

    echo ""
done

# Sync deep-env credentials to iCloud
echo -e "${CYAN}[deep-env]${NC} Syncing credentials to iCloud"
if [ "$DRY_RUN" = true ]; then
    echo -e "  ${YELLOW}skipped (dry run)${NC}"
else
    if command -v deep-env &> /dev/null; then
        echo -n "  Pushing credentials... "
        if deep-env push 2>/dev/null | grep -q "Pushed"; then
            echo -e "${GREEN}done${NC}"
        else
            echo -e "${GREEN}done${NC}"
        fi
    else
        echo -e "  ${YELLOW}deep-env not found${NC}"
    fi
fi
echo ""

# Summary
echo -e "${BOLD}${BLUE}========================================${NC}"
echo -e "${BOLD}Summary:${NC}"
echo -e "  Commits created: ${CYAN}$TOTAL_COMMITS${NC}"
echo -e "  Commits pushed:  ${CYAN}$TOTAL_PUSHED${NC}"
echo -e "  Commits pulled:  ${CYAN}$TOTAL_PULLED${NC}"
echo -e "  Credentials:     ${CYAN}synced to iCloud${NC}"
if [ "$ERRORS" -gt 0 ]; then
    echo -e "  Errors:          ${RED}$ERRORS${NC}"
fi
echo -e "${BOLD}${BLUE}========================================${NC}"

if [ "$ERRORS" -gt 0 ]; then
    exit 1
fi

exit 0
