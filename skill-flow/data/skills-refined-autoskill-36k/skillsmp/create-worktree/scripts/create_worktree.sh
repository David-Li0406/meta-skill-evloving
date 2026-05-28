#!/bin/bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Usage
usage() {
    echo "Usage: $0 <feature-name>"
    echo ""
    echo "Creates a git worktree for parallel feature development."
    echo ""
    echo "Arguments:"
    echo "  feature-name    Name of the feature (e.g., svg-export, domain-highlight)"
    echo ""
    echo "Example:"
    echo "  $0 svg-export"
    echo ""
    echo "This will create:"
    echo "  - Branch: feature/svg-export"
    echo "  - Worktree: .worktrees/svg-export/"
    exit 1
}

# Check arguments
if [ $# -lt 1 ]; then
    log_error "Feature name is required"
    usage
fi

FEATURE_NAME="$1"
BRANCH_NAME="feature/${FEATURE_NAME}"
WORKTREE_DIR=".worktrees/${FEATURE_NAME}"

# Get the root directory of the repository
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

log_info "Creating worktree for feature: ${FEATURE_NAME}"
log_info "Branch: ${BRANCH_NAME}"
log_info "Worktree directory: ${WORKTREE_DIR}"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    log_error "Not a git repository"
    exit 1
fi

# Check if worktree already exists
if [ -d "${WORKTREE_DIR}" ]; then
    log_error "Worktree already exists: ${WORKTREE_DIR}"
    log_info "To remove it, run: git worktree remove ${WORKTREE_DIR}"
    exit 1
fi

# Check if branch already exists
if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
    log_warn "Branch ${BRANCH_NAME} already exists"
    log_info "Creating worktree from existing branch..."
    git worktree add "${WORKTREE_DIR}" "${BRANCH_NAME}"
else
    log_step "Creating new branch and worktree..."
    git worktree add -b "${BRANCH_NAME}" "${WORKTREE_DIR}" main
fi

log_info "Worktree created successfully"

# Setup Python venv in worktree
log_step "Setting up Python venv in worktree..."
cd "${WORKTREE_DIR}"

if [ -f "requirements.txt" ] || [ -d "api" ]; then
    python3 -m venv venv
    source venv/bin/activate
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_info "Python dependencies installed"
    fi
    deactivate
    log_info "Python venv created: ${WORKTREE_DIR}/venv"
else
    log_warn "No requirements.txt found, skipping venv setup"
fi

# Print summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} Worktree created successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Location: ${REPO_ROOT}/${WORKTREE_DIR}"
echo "Branch:   ${BRANCH_NAME}"
echo ""
echo "To start working:"
echo "  cd ${WORKTREE_DIR}"
echo "  source venv/bin/activate"
echo "  npm run dev"
echo ""
echo "To remove worktree when done:"
echo "  git worktree remove ${WORKTREE_DIR}"
echo ""
