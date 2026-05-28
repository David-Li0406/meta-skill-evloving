#!/bin/bash

################################################################################
# merge-and-release.sh
#
# Complete workflow: Merge a PR and automatically create a semantic versioned
# release tag with GitHub release notes.
#
# Usage: ./scripts/merge-and-release.sh <PR_NUMBER> [options]
#        Or from skill: ./.github/skills/github-pull-request/scripts/merge-and-release.sh <PR_NUMBER>
#
# Options:
#   --no-tag    Don't create a git tag (just merge)
#   --dry-run   Show what would happen without making changes
#   --help      Show this help message
#
# Examples:
#   ./scripts/merge-and-release.sh 42                # Merge PR #42 and create release
#   ./scripts/merge-and-release.sh 45 --dry-run      # Preview what would happen
#   ./scripts/merge-and-release.sh 42 --no-tag       # Just merge, no release
#
# Prerequisites:
#   - GitHub CLI (gh) installed and authenticated
#   - Git configured locally
#   - Current branch has no uncommitted changes
#
# Exit Codes:
#   0 - Success
#   1 - Missing PR number or invalid arguments
#   2 - PR not in OPEN state
#   3 - PR has merge conflicts
#   4 - PR checks/reviews not approved
#   5 - Git operation failed
#
################################################################################

set -euo pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Configuration
DRY_RUN=false
CREATE_TAG=true
VERBOSE=false

# Parse arguments
PR_NUMBER=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --help)
      head -n 27 "$0" | tail -n +2
      exit 0
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --no-tag)
      CREATE_TAG=false
      shift
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    [0-9]*)
      PR_NUMBER=$1
      shift
      ;;
    *)
      echo "❌ Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate PR number
if [ -z "$PR_NUMBER" ]; then
  echo -e "${RED}❌ Error: PR number required${NC}"
  echo "Usage: $0 <PR_NUMBER> [options]"
  exit 1
fi

# Helper functions
log_info() {
  echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
  echo -e "${GREEN}✓${NC} $*"
}

log_warning() {
  echo -e "${YELLOW}⚠${NC} $*"
}

log_error() {
  echo -e "${RED}❌${NC} $*"
}

log_step() {
  echo -e "\n${BLUE}→${NC} $*"
}

# Main workflow
main() {
  log_step "Merge and Release Workflow for PR #$PR_NUMBER"
  
  if [ "$DRY_RUN" = true ]; then
    log_warning "DRY RUN MODE - No changes will be made"
  fi

  # Step 1: Verify PR exists and is accessible
  log_step "Step 1/7: Verifying PR #$PR_NUMBER..."
  
  if ! PR_STATE=$(gh pr view "$PR_NUMBER" --json state --jq '.state' 2>/dev/null); then
    log_error "PR #$PR_NUMBER not found or inaccessible"
    exit 2
  fi
  
  if [ "$PR_STATE" != "OPEN" ]; then
    log_error "PR #$PR_NUMBER is not OPEN (current state: $PR_STATE)"
    exit 2
  fi
  
  log_success "PR #$PR_NUMBER is OPEN"

  # Step 2: Check merge status
  log_step "Step 2/7: Checking merge compatibility..."
  
  MERGE_STATUS=$(gh pr view "$PR_NUMBER" --json mergeStateStatus --jq '.mergeStateStatus')
  MERGEABLE=$(gh pr view "$PR_NUMBER" --json mergeable --jq '.mergeable')
  
  if [ "$MERGEABLE" != "MERGEABLE" ]; then
    log_error "PR is not mergeable (status: $MERGE_STATUS)"
    exit 3
  fi
  
  if [ "$MERGE_STATUS" != "CLEAN" ]; then
    log_error "PR has conflicts or failing checks (status: $MERGE_STATUS)"
    exit 3
  fi
  
  log_success "PR is mergeable and clean"

  # Step 3: Get PR information
  log_step "Step 3/7: Fetching PR information..."
  
  PR_TITLE=$(gh pr view "$PR_NUMBER" --json title --jq '.title')
  PR_URL=$(gh pr view "$PR_NUMBER" --json url --jq '.url')
  PR_BRANCH=$(gh pr view "$PR_NUMBER" --json headRefName --jq '.headRefName')
  
  log_info "Title: $PR_TITLE"
  log_info "Branch: $PR_BRANCH"

  # Step 4: Calculate version
  log_step "Step 4/7: Calculating next version..."
  
  # Get current version
  CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
  CURRENT_VERSION=${CURRENT_TAG#v}
  
  # Parse version components
  MAJOR=$(echo "$CURRENT_VERSION" | cut -d. -f1)
  MINOR=$(echo "$CURRENT_VERSION" | cut -d. -f2)
  PATCH=$(echo "$CURRENT_VERSION" | cut -d. -f3)
  
  # Determine bump type from PR title (Conventional Commits)
  if [[ "$PR_TITLE" =~ ^feat ]]; then
    BUMP_TYPE="MINOR"
    NEXT_VERSION="v$MAJOR.$((MINOR+1)).0"
  else
    # Default to PATCH for fixes, chores, etc.
    BUMP_TYPE="PATCH"
    NEXT_VERSION="v$MAJOR.$MINOR.$((PATCH+1))"
  fi
  
  log_info "Current version: $CURRENT_TAG"
  log_info "Bump type: $BUMP_TYPE"
  log_info "Next version: $NEXT_VERSION"

  # Step 5: Merge PR (or simulate if dry-run)
  log_step "Step 5/7: Merging PR #$PR_NUMBER..."
  
  if [ "$DRY_RUN" = false ]; then
    if ! gh pr merge "$PR_NUMBER" --squash --delete-branch 2>/dev/null; then
      log_error "Failed to merge PR #$PR_NUMBER"
      exit 5
    fi
    
    log_success "PR merged successfully"
    
    # Update local main branch
    git fetch origin main
    git checkout main
    git pull origin main
  else
    log_warning "Would merge PR #$PR_NUMBER with squash strategy"
  fi

  # Step 6: Create git tag (if enabled and not dry-run)
  if [ "$CREATE_TAG" = true ]; then
    log_step "Step 6/7: Creating release tag..."
    
    if [ "$DRY_RUN" = false ]; then
      # Get merge commit
      MERGE_COMMIT=$(git rev-parse HEAD)
      RELEASE_DATE=$(date -u +'%Y-%m-%d %H:%M:%S UTC')
      
      # Create annotated tag with release notes
      TAG_MESSAGE="Release $NEXT_VERSION

Merged PR #$PR_NUMBER: $PR_TITLE
Merge Commit: $MERGE_COMMIT

Release Date: $RELEASE_DATE"

      if ! git tag -a "$NEXT_VERSION" -m "$TAG_MESSAGE"; then
        log_error "Failed to create git tag"
        exit 5
      fi
      
      log_success "Tag $NEXT_VERSION created locally"
      
      # Push tag
      if ! git push origin "$NEXT_VERSION"; then
        log_error "Failed to push tag to remote"
        exit 5
      fi
      
      log_success "Tag pushed to remote"
    else
      log_warning "Would create and push tag: $NEXT_VERSION"
    fi
  else
    log_info "Skipping tag creation (--no-tag flag set)"
  fi

  # Step 7: Create GitHub Release (if not dry-run)
  if [ "$CREATE_TAG" = true ] && [ "$DRY_RUN" = false ]; then
    log_step "Step 7/7: Creating GitHub release..."
    
    RELEASE_NOTES="## What's New

Merged PR #$PR_NUMBER: [$PR_TITLE]($PR_URL)

### Changes
See PR #$PR_NUMBER for detailed changes included in this release.

**Merge Commit**: \`$MERGE_COMMIT\`"

    if gh release create "$NEXT_VERSION" \
      --title "Release $NEXT_VERSION" \
      --notes "$RELEASE_NOTES"; then
      
      RELEASE_URL="https://github.com/JordiNodeJS/thesimpsonsapi/releases/tag/$NEXT_VERSION"
      log_success "GitHub release created"
      log_info "Release URL: $RELEASE_URL"
    else
      log_warning "Failed to create GitHub release (tag was created successfully)"
    fi
  else
    if [ "$CREATE_TAG" = true ]; then
      log_warning "Would create GitHub release for $NEXT_VERSION"
    fi
  fi

  # Summary
  log_step "Workflow Complete"
  
  if [ "$DRY_RUN" = false ]; then
    echo ""
    echo -e "${GREEN}Summary:${NC}"
    echo "  • PR #$PR_NUMBER merged with squash"
    if [ "$CREATE_TAG" = true ]; then
      echo "  • Release $NEXT_VERSION created"
      echo "  • Version bump: $CURRENT_TAG → $NEXT_VERSION ($BUMP_TYPE)"
    fi
    echo ""
    log_success "All steps completed successfully!"
  else
    echo ""
    log_warning "This was a dry run. No changes were made."
    echo "Run without --dry-run to apply changes."
  fi
}

# Run main workflow
main
