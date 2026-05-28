#!/bin/bash
#
# Setup Branch Protection for OpenShift Cluster Health MCP
#
# This script configures GitHub branch protection rules using the GitHub CLI (gh).
# It sets up protection for main and release branches with required status checks,
# review requirements, and other safety measures.
#
# Prerequisites:
# - GitHub CLI (gh) installed: https://cli.github.com/
# - Authenticated with admin permissions: gh auth login
# - Admin access to the repository
#
# Usage:
#   ./scripts/setup-branch-protection.sh

set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository details
REPO="tosin2013/openshift-cluster-health-mcp"

# Required status checks (from CI workflows)
REQUIRED_CHECKS=(
  "Test"
  "Lint"
  "Build"
  "Security"
  "Helm"
  "build-and-push"
)

# Function to print colored output
print_info() {
  echo -e "${BLUE}ℹ ${1}${NC}"
}

print_success() {
  echo -e "${GREEN}✓ ${1}${NC}"
}

print_warning() {
  echo -e "${YELLOW}⚠ ${1}${NC}"
}

print_error() {
  echo -e "${RED}✗ ${1}${NC}"
}

# Function to check prerequisites
check_prerequisites() {
  print_info "Checking prerequisites..."

  # Check if gh CLI is installed
  if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed"
    echo "Install it from: https://cli.github.com/"
    exit 1
  fi
  print_success "GitHub CLI installed"

  # Check if jq is installed
  if ! command -v jq &> /dev/null; then
    print_error "jq is not installed"
    echo "Install it from: https://jqlang.github.io/jq/"
    exit 1
  fi
  print_success "jq installed"

  # Check if authenticated
  if ! gh auth status &> /dev/null; then
    print_error "Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
  fi
  print_success "GitHub CLI authenticated"

  # Check if user has admin access
  local user_permission
  user_permission=$(gh api "/repos/${REPO}" --jq '.permissions.admin' 2>/dev/null || echo "false")

  if [[ "$user_permission" != "true" ]]; then
    print_warning "You may not have admin access to ${REPO}"
    print_warning "Branch protection setup requires admin permissions"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      exit 1
    fi
  else
    print_success "Admin access confirmed"
  fi
}

# Function to setup branch protection
setup_branch_protection() {
  local branch=$1
  local required_reviews=$2

  print_info "Setting up branch protection for: ${branch}"

  # Build the JSON payload for branch protection
  # Using heredoc to avoid escaping issues
  local payload
  payload=$(cat <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": $(printf '%s\n' "${REQUIRED_CHECKS[@]}" | jq -R . | jq -s .)
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": ${required_reviews}
  },
  "required_conversation_resolution": true,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
)

  # Apply branch protection using GitHub API
  if gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    "/repos/${REPO}/branches/${branch}/protection" \
    --input - <<< "$payload" > /dev/null 2>&1; then
    print_success "Branch protection configured for: ${branch}"
    echo "  - Required reviews: ${required_reviews}"
    echo "  - Required status checks: ${#REQUIRED_CHECKS[@]}"
    echo "  - Force push: disabled"
    echo "  - Deletions: disabled"
  else
    print_error "Failed to configure branch protection for: ${branch}"
    print_warning "This could be due to:"
    print_warning "  - Insufficient permissions"
    print_warning "  - Branch does not exist"
    print_warning "  - API rate limit exceeded"
    return 1
  fi
}

# Function to verify branch exists
verify_branch_exists() {
  local branch=$1

  if gh api "/repos/${REPO}/branches/${branch}" &> /dev/null; then
    return 0
  else
    print_warning "Branch '${branch}' does not exist in repository"
    return 1
  fi
}

# Main execution
main() {
  echo "=========================================="
  echo "  Branch Protection Setup"
  echo "  Repository: ${REPO}"
  echo "=========================================="
  echo

  # Check prerequisites
  check_prerequisites
  echo

  # Confirm before proceeding
  print_warning "This script will configure branch protection for:"
  echo "  - main (1 required approval)"
  echo "  - release-4.18 (2 required approvals)"
  echo "  - release-4.19 (2 required approvals)"
  echo "  - release-4.20 (2 required approvals)"
  echo
  print_info "Note: release-4.17 deleted on 2026-01-17 (OpenShift 4.17 EOL)"
  echo
  echo "Required status checks (${#REQUIRED_CHECKS[@]} total):"
  for check in "${REQUIRED_CHECKS[@]}"; do
    echo "  - ${check}"
  done
  echo

  read -p "Proceed with branch protection setup? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Setup cancelled by user"
    exit 0
  fi

  echo
  print_info "Starting branch protection configuration..."
  echo

  # Configure main branch (1 approval)
  if verify_branch_exists "main"; then
    setup_branch_protection "main" 1
  else
    print_error "Skipping main branch (does not exist)"
  fi
  echo

  # Configure release branches (2 approvals)
  for release in "release-4.18" "release-4.19" "release-4.20"; do
    if verify_branch_exists "$release"; then
      setup_branch_protection "$release" 2
    else
      print_warning "Skipping ${release} branch (does not exist)"
    fi
    echo
  done

  echo "=========================================="
  print_success "Branch protection setup complete!"
  echo "=========================================="
  echo
  print_info "Next steps:"
  echo "  1. Verify settings: ./scripts/verify-branch-protection.sh"
  echo "  2. Review on GitHub: https://github.com/${REPO}/settings/branches"
  echo "  3. Test with a PR to ensure protection works correctly"
  echo
  print_info "Documentation: docs/BRANCH_PROTECTION.md"
}

# Run main function
main "$@"
