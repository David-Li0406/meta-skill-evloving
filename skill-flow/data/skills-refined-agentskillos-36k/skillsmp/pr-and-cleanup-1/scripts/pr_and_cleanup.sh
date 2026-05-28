#!/usr/bin/env bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MAIN_BRANCH="main"
PR_ONLY=false
CLEANUP_ONLY=false
FORCE=false
DRAFT=false
PR_TITLE=""
PR_BODY=""
BASE_BRANCH=""

# Help message
show_help() {
    cat <<EOF
Usage: $(basename "$0") [options]

Create a Pull Request and clean up the worktree.

Options:
  --pr-only                 Create PR only (keep worktree)
  --cleanup-only            Clean up worktree only (skip PR creation)
  --force                   Force cleanup even with uncommitted changes (not recommended)
  --draft                   Create as draft PR
  --title TITLE             PR title
  --body BODY               PR description
  --base BRANCH             Base branch for PR (default: main)
  --main-branch BRANCH      Branch to checkout after cleanup (default: main)
  --help                    Show this help message

Examples:
  $(basename "$0")
  $(basename "$0") --draft
  $(basename "$0") --pr-only
  $(basename "$0") --cleanup-only
  $(basename "$0") --title "feat: add user auth" --body "Implements JWT authentication"
  $(basename "$0") --base develop --main-branch develop

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --pr-only)
            PR_ONLY=true
            shift
            ;;
        --cleanup-only)
            CLEANUP_ONLY=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --draft)
            DRAFT=true
            shift
            ;;
        --title)
            PR_TITLE="$2"
            shift 2
            ;;
        --body)
            PR_BODY="$2"
            shift 2
            ;;
        --base)
            BASE_BRANCH="$2"
            shift 2
            ;;
        --main-branch)
            MAIN_BRANCH="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}" >&2
            show_help
            exit 1
            ;;
    esac
done

# Validate we're in a git repository
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo -e "${RED}Error: Not a git repository${NC}" >&2
    exit 1
fi

# Check if gh CLI is installed (only if not cleanup-only)
if [ "$CLEANUP_ONLY" = false ]; then
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}" >&2
        echo -e "${YELLOW}Install: brew install gh${NC}" >&2
        exit 1
    fi

    # Check gh authentication
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}Error: GitHub CLI is not authenticated${NC}" >&2
        echo -e "${YELLOW}Run: gh auth login${NC}" >&2
        exit 1
    fi
fi

# Get current branch and worktree info
CURRENT_BRANCH=$(git branch --show-current)
REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_DIR=$(pwd)

# Check if we're in a worktree
WORKTREE_PATH=""
if [ "$CURRENT_DIR" != "$REPO_ROOT" ]; then
    # We might be in a worktree
    WORKTREE_PATH=$(git worktree list | grep "$CURRENT_DIR" | awk '{print $1}')
fi

echo -e "${BLUE}=== Current Status ===${NC}"
echo -e "Repository root: ${GREEN}${REPO_ROOT}${NC}"
echo -e "Current branch:  ${GREEN}${CURRENT_BRANCH}${NC}"
if [ -n "$WORKTREE_PATH" ]; then
    echo -e "Worktree path:   ${GREEN}${WORKTREE_PATH}${NC}"
else
    echo -e "Worktree path:   ${YELLOW}Not in a worktree${NC}"
fi
echo ""

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ] && [ "$FORCE" = false ]; then
    echo -e "${RED}⚠️  Uncommitted changes detected:${NC}"
    git status --short
    echo ""
    echo -e "${YELLOW}Please commit your changes or use --force to ignore (not recommended)${NC}"
    exit 1
fi

# Check for unpushed commits (only if not cleanup-only)
if [ "$CLEANUP_ONLY" = false ]; then
    UNPUSHED=$(git log @{u}.. 2>/dev/null | wc -l | tr -d ' ')
    if [ "$UNPUSHED" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  You have ${UNPUSHED} unpushed commit(s)${NC}"
        echo -e "${YELLOW}Pushing to remote...${NC}"
        git push -u origin "$CURRENT_BRANCH"
        echo ""
    fi
fi

# Create PR if not cleanup-only
PR_URL=""
if [ "$CLEANUP_ONLY" = false ]; then
    echo -e "${BLUE}=== Creating Pull Request ===${NC}"

    # Build gh pr create command
    GH_CMD="gh pr create"

    if [ "$DRAFT" = true ]; then
        GH_CMD="$GH_CMD --draft"
    fi

    if [ -n "$PR_TITLE" ]; then
        GH_CMD="$GH_CMD --title \"$PR_TITLE\""
    fi

    if [ -n "$PR_BODY" ]; then
        GH_CMD="$GH_CMD --body \"$PR_BODY\""
    fi

    if [ -n "$BASE_BRANCH" ]; then
        GH_CMD="$GH_CMD --base \"$BASE_BRANCH\""
    fi

    # Execute PR creation
    echo -e "${YELLOW}Running: $GH_CMD${NC}"
    if eval "$GH_CMD"; then
        PR_URL=$(gh pr view --json url --jq .url)
        echo -e "${GREEN}✅ Pull Request created successfully!${NC}"
        echo -e "${BLUE}PR URL: ${PR_URL}${NC}"
        echo ""
    else
        echo -e "${RED}❌ Failed to create Pull Request${NC}" >&2
        exit 1
    fi
fi

# Clean up worktree if not pr-only
if [ "$PR_ONLY" = false ]; then
    if [ -n "$WORKTREE_PATH" ]; then
        echo -e "${BLUE}=== Cleaning Up Worktree ===${NC}"

        # Change to repo root
        cd "$REPO_ROOT"
        echo -e "Changed to repository root: ${GREEN}${REPO_ROOT}${NC}"

        # Checkout main branch
        echo -e "Checking out ${GREEN}${MAIN_BRANCH}${NC}..."
        if git checkout "$MAIN_BRANCH" 2>/dev/null; then
            echo -e "${GREEN}✅ Checked out ${MAIN_BRANCH}${NC}"
        else
            echo -e "${YELLOW}⚠️  Branch ${MAIN_BRANCH} not found, staying in current location${NC}"
        fi

        # Remove worktree
        echo -e "Removing worktree: ${YELLOW}${WORKTREE_PATH}${NC}..."
        if git worktree remove "$WORKTREE_PATH" --force 2>/dev/null; then
            echo -e "${GREEN}✅ Worktree removed successfully${NC}"
        else
            # Try without --force
            if git worktree remove "$WORKTREE_PATH" 2>/dev/null; then
                echo -e "${GREEN}✅ Worktree removed successfully${NC}"
            else
                echo -e "${RED}❌ Failed to remove worktree${NC}" >&2
                echo -e "${YELLOW}Try manually: git worktree remove ${WORKTREE_PATH} --force${NC}" >&2
                exit 1
            fi
        fi
    else
        echo -e "${YELLOW}⚠️  Not in a worktree, skipping cleanup${NC}"
    fi
fi

# Print summary
echo ""
echo -e "${GREEN}=== Summary ===${NC}"

if [ "$CLEANUP_ONLY" = false ] && [ -n "$PR_URL" ]; then
    echo -e "${GREEN}✅ PR Created:${NC} ${PR_URL}"
fi

if [ "$PR_ONLY" = false ] && [ -n "$WORKTREE_PATH" ]; then
    echo -e "${GREEN}✅ Worktree Cleaned:${NC} ${WORKTREE_PATH}"
    echo -e "${GREEN}✅ Current Branch:${NC} ${MAIN_BRANCH}"
fi

echo ""
echo -e "${BLUE}=== Next Steps ===${NC}"

if [ "$CLEANUP_ONLY" = false ]; then
    echo -e "1. Review your PR: ${YELLOW}gh pr view${NC}"
    echo -e "2. Check CI/CD status: ${YELLOW}gh pr checks${NC}"
    echo -e "3. Request review: ${YELLOW}gh pr edit --add-reviewer @username${NC}"
    echo -e "4. Merge when ready: ${YELLOW}gh pr merge${NC}"
fi

echo -e ""
echo -e "${BLUE}=== Useful Commands ===${NC}"
echo -e "- View PR: ${YELLOW}gh pr view${NC}"
echo -e "- Check CI/CD: ${YELLOW}gh pr checks${NC}"
echo -e "- List worktrees: ${YELLOW}git worktree list${NC}"
echo -e "- Prune stale worktrees: ${YELLOW}git worktree prune${NC}"
echo ""
