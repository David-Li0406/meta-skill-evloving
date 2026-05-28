#!/usr/bin/env bash
set -euo pipefail

# dirty-repo-bootstrap/snapshot.sh
# Safe WIP snapshot workflow for dirty repositories
# See SKILL.md for full documentation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
BRANCH_NAME=""
COMMIT_MESSAGE="wip: snapshot before next task"
VERBOSE="${VERBOSE:-0}"

# Colors for output (no secrets)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
  cat <<EOF
Usage: $0 [options]

Safe WIP snapshot workflow for dirty repositories.

Options:
  --branch-name <name>    Custom WIP branch name (default: auto-generated)
  --message <msg>         Custom commit message (default: "wip: snapshot before next task")
  --verbose               Enable verbose output
  -h, --help              Show this help message

Examples:
  # Auto-generate branch name and snapshot
  $0

  # Custom branch name
  $0 --branch-name wip/my-custom-branch

  # Custom commit message
  $0 --message "wip: snapshot before refactoring auth"

Exit codes:
  0  Success (snapshot created and pushed)
  1  Repository is already clean (no snapshot needed)
  2  Git operation failed
  3  Beads sync failed

EOF
  exit 0
}

log_info() {
  echo -e "${GREEN}✓${NC} $*"
}

log_warn() {
  echo -e "${YELLOW}⚠${NC} $*"
}

log_error() {
  echo -e "${RED}✗${NC} $*"
}

log_verbose() {
  if [[ "$VERBOSE" == "1" ]]; then
    echo "  $*"
  fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --branch-name)
      BRANCH_NAME="$2"
      shift 2
      ;;
    --message)
      COMMIT_MESSAGE="$2"
      shift 2
      ;;
    --verbose)
      VERBOSE=1
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      log_error "Unknown option: $1"
      usage
      ;;
  esac
done

# Verify we're in a git repository
if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  log_error "Not a git repository. Please run this from within a git repo."
  exit 2
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_ROOT")"
cd "$REPO_ROOT"

log_verbose "Repository: $REPO_ROOT"

# Check if repo is dirty
if [[ -z "$(git status --porcelain)" ]]; then
  log_info "Repository is already clean. No snapshot needed."
  exit 1
fi

log_warn "Repository has uncommitted changes. Creating WIP snapshot..."

# Auto-generate branch name if not provided
if [[ -z "$BRANCH_NAME" ]]; then
  HOSTNAME="$(hostname -s 2>/dev/null || echo "unknown")"
  DATE="$(date +%Y-%m-%d)"
  BRANCH_NAME="wip/${HOSTNAME}-${DATE}-${REPO_NAME}"
  log_verbose "Auto-generated branch name: $BRANCH_NAME"
fi

# Save current branch (if any)
CURRENT_BRANCH=""
if CURRENT_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null)"; then
  log_verbose "Current branch: $CURRENT_BRANCH"
else
  log_verbose "Currently in detached HEAD state"
fi

# Create WIP branch
log_info "Creating WIP branch: $BRANCH_NAME"
if ! git checkout -b "$BRANCH_NAME" 2>/dev/null; then
  # Branch might already exist, try checking it out
  log_warn "Branch $BRANCH_NAME already exists, checking it out..."
  if ! git checkout "$BRANCH_NAME"; then
    log_error "Failed to checkout branch $BRANCH_NAME"
    exit 2
  fi
fi

# Check if .beads/issues.jsonl is modified
BEADS_MODIFIED=0
if git status --porcelain | grep -q ".beads/issues.jsonl"; then
  BEADS_MODIFIED=1
  log_warn "Detected .beads/issues.jsonl modifications. Running 'bd sync' first..."

  if ! command -v bd >/dev/null 2>&1; then
    log_error "Beads CLI (bd) not found, but .beads/issues.jsonl is modified."
    log_error "Please install Beads CLI or manually sync before committing."
    exit 3
  fi

  if ! bd sync; then
    log_error "Beads sync failed. Cannot safely commit .beads/issues.jsonl."
    log_error "Please resolve Beads sync issues manually."
    exit 3
  fi

  log_info "Beads sync completed successfully"
fi

# Add all changes
log_info "Adding all changes..."
if ! git add -A; then
  log_error "Failed to add changes"
  exit 2
fi

# Commit changes
log_info "Committing snapshot..."
if ! git commit -m "$COMMIT_MESSAGE"; then
  log_error "Failed to commit changes"
  exit 2
fi

# Push to origin
log_info "Pushing WIP branch to origin..."
if ! git push -u origin HEAD; then
  log_error "Failed to push WIP branch to origin"
  log_error "You may need to use: git push --force-with-lease origin HEAD"
  exit 2
fi

# Return to previous branch or main/master
if [[ -n "$CURRENT_BRANCH" ]] && [[ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]]; then
  log_info "Returning to branch: $CURRENT_BRANCH"
  if ! git checkout "$CURRENT_BRANCH"; then
    log_warn "Failed to return to $CURRENT_BRANCH, staying on $BRANCH_NAME"
  fi
else
  # Try to checkout main or master
  for branch in main master; do
    if git show-ref --verify --quiet "refs/heads/$branch"; then
      log_info "Checking out $branch branch..."
      if git checkout "$branch"; then
        log_info "Pulling latest from origin/$branch..."
        git pull origin "$branch" || log_warn "Failed to pull from origin/$branch"
        break
      fi
    fi
  done
fi

log_info "WIP snapshot created successfully!"
log_info "  Branch: $BRANCH_NAME"
log_info "  Commit: $(git log -1 --oneline "$BRANCH_NAME" | head -1)"
log_info ""
log_info "To continue working on this WIP later:"
log_info "  git checkout $BRANCH_NAME"
log_info ""
log_info "To delete this WIP branch later:"
log_info "  git branch -D $BRANCH_NAME"
log_info "  git push origin --delete $BRANCH_NAME"

exit 0
