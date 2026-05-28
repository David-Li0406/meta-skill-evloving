#!/usr/bin/env bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
WORKTREE_BASE_DIR=".worktrees"
BRANCH_PREFIX="feature"
BASE_BRANCH="main"

# Help message
show_help() {
    cat <<EOF
Usage: $(basename "$0") <feature-name> [options]

Create a Git worktree for parallel development.

Arguments:
  feature-name          Name of the feature (required)

Options:
  --branch-prefix PREFIX    Branch prefix (default: feature)
  --base-branch BRANCH      Base branch to branch from (default: main)
  --worktree-dir DIR        Base directory for worktrees (default: .worktrees)
  --help                    Show this help message

Examples:
  $(basename "$0") user-authentication
  $(basename "$0") api-rate-limiting --base-branch develop
  $(basename "$0") hotfix-bug-123 --branch-prefix hotfix

EOF
}

# Parse arguments
FEATURE_NAME=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --branch-prefix)
            BRANCH_PREFIX="$2"
            shift 2
            ;;
        --base-branch)
            BASE_BRANCH="$2"
            shift 2
            ;;
        --worktree-dir)
            WORKTREE_BASE_DIR="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        -*)
            echo -e "${RED}Error: Unknown option $1${NC}" >&2
            show_help
            exit 1
            ;;
        *)
            if [ -z "$FEATURE_NAME" ]; then
                FEATURE_NAME="$1"
            else
                echo -e "${RED}Error: Multiple feature names provided${NC}" >&2
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate feature name
if [ -z "$FEATURE_NAME" ]; then
    echo -e "${RED}Error: Feature name is required${NC}" >&2
    show_help
    exit 1
fi

# Validate we're in a git repository
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo -e "${RED}Error: Not a git repository${NC}" >&2
    exit 1
fi

# Construct paths
BRANCH_NAME="${BRANCH_PREFIX}/${FEATURE_NAME}"
WORKTREE_DIR="${WORKTREE_BASE_DIR}/${FEATURE_NAME}"

echo -e "${BLUE}=== Creating Worktree ===${NC}"
echo -e "Feature name: ${GREEN}${FEATURE_NAME}${NC}"
echo -e "Branch name:  ${GREEN}${BRANCH_NAME}${NC}"
echo -e "Directory:    ${GREEN}${WORKTREE_DIR}${NC}"
echo -e "Base branch:  ${GREEN}${BASE_BRANCH}${NC}"
echo ""

# Check if worktree directory already exists
if [ -d "$WORKTREE_DIR" ]; then
    echo -e "${YELLOW}Warning: Directory ${WORKTREE_DIR} already exists${NC}"
    echo -e "${YELLOW}Please choose a different name or remove the existing directory${NC}"
    exit 1
fi

# Check if branch exists
if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
    echo -e "${YELLOW}Branch ${BRANCH_NAME} already exists, using existing branch${NC}"
    git worktree add "$WORKTREE_DIR" "$BRANCH_NAME"
else
    echo -e "${GREEN}Creating new branch ${BRANCH_NAME} from ${BASE_BRANCH}${NC}"

    # Check if base branch exists
    if ! git show-ref --verify --quiet "refs/heads/${BASE_BRANCH}"; then
        # Try remote branch
        if git show-ref --verify --quiet "refs/remotes/origin/${BASE_BRANCH}"; then
            echo -e "${YELLOW}Base branch ${BASE_BRANCH} not found locally, using origin/${BASE_BRANCH}${NC}"
            git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR" "origin/${BASE_BRANCH}"
        else
            echo -e "${RED}Error: Base branch ${BASE_BRANCH} not found${NC}" >&2
            exit 1
        fi
    else
        git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR" "$BASE_BRANCH"
    fi
fi

echo ""
echo -e "${GREEN}✅ Worktree created successfully!${NC}"
echo ""
echo -e "${BLUE}=== Next Steps ===${NC}"
echo -e "1. Change directory:"
echo -e "   ${YELLOW}cd ${WORKTREE_DIR}${NC}"
echo ""
echo -e "2. Start development:"
echo -e "   - Make your changes"
echo -e "   - Commit as usual: ${YELLOW}git add . && git commit${NC}"
echo -e "   - Push when ready: ${YELLOW}git push -u origin ${BRANCH_NAME}${NC}"
echo ""
echo -e "3. When finished, use the pr-and-cleanup skill or:"
echo -e "   - Create PR: ${YELLOW}gh pr create${NC}"
echo -e "   - Remove worktree: ${YELLOW}git worktree remove ${WORKTREE_DIR}${NC}"
echo ""
echo -e "${BLUE}=== Useful Commands ===${NC}"
echo -e "- List all worktrees: ${YELLOW}git worktree list${NC}"
echo -e "- Remove this worktree: ${YELLOW}git worktree remove ${WORKTREE_DIR}${NC}"
echo -e "- Prune stale worktrees: ${YELLOW}git worktree prune${NC}"
echo ""
