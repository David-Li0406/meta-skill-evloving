#!/bin/bash
#
# Verify Branch Protection for OpenShift Cluster Health MCP
#
# This script verifies that GitHub branch protection rules are correctly configured.
# It checks protection status, required checks, and review requirements.
#
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated
#
# Usage:
#   ./scripts/verify-branch-protection.sh

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

# Expected status checks
EXPECTED_CHECKS=(
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

# Function to check if gh CLI and jq are available
check_gh_cli() {
  if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed"
    echo "Install it from: https://cli.github.com/"
    exit 1
  fi

  if ! command -v jq &> /dev/null; then
    print_error "jq is not installed"
    echo "Install it from: https://jqlang.github.io/jq/"
    exit 1
  fi

  if ! gh auth status &> /dev/null; then
    print_error "Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
  fi
}

# Function to verify branch protection
verify_branch() {
  local branch=$1
  local expected_reviews=$2
  local issues=0

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  print_info "Verifying branch: ${branch}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Check if branch exists
  if ! gh api "/repos/${REPO}/branches/${branch}" &> /dev/null; then
    print_error "Branch does not exist"
    return 1
  fi
  print_success "Branch exists"

  # Get branch protection status
  local protection_data
  if ! protection_data=$(gh api "/repos/${REPO}/branches/${branch}/protection" 2>/dev/null); then
    print_error "No branch protection configured"
    print_info "Run: ./scripts/setup-branch-protection.sh"
    return 1
  fi
  print_success "Branch protection enabled"

  # Verify required status checks
  local status_checks
  status_checks=$(echo "$protection_data" | jq -r '.required_status_checks.contexts[]' 2>/dev/null || echo "")

  if [[ -z "$status_checks" ]]; then
    print_error "No required status checks configured"
    ((issues++)) || true
  else
    print_success "Required status checks configured"
    echo "  Checks ($(echo "$status_checks" | wc -l)):"
    while IFS= read -r check; do
      echo "    - ${check}"
    done <<< "$status_checks"

    # Verify expected checks are present
    for expected in "${EXPECTED_CHECKS[@]}"; do
      if echo "$status_checks" | grep -q "^${expected}$"; then
        : # Check found, no action needed
      else
        print_warning "  Missing expected check: ${expected}"
        ((issues++)) || true
      fi
    done
  fi

  # Verify strict status checks
  local strict
  strict=$(echo "$protection_data" | jq -r '.required_status_checks.strict' 2>/dev/null || echo "false")
  if [[ "$strict" == "true" ]]; then
    print_success "Require branches to be up to date: enabled"
  else
    print_error "Require branches to be up to date: disabled"
    ((issues++)) || true
  fi

  # Verify pull request reviews
  local pr_reviews
  pr_reviews=$(echo "$protection_data" | jq -r '.required_pull_request_reviews' 2>/dev/null || echo "null")

  if [[ "$pr_reviews" == "null" || "$pr_reviews" == "" ]]; then
    print_error "No pull request review requirements"
    ((issues++)) || true
  else
    local actual_reviews
    actual_reviews=$(echo "$pr_reviews" | jq -r '.required_approving_review_count' 2>/dev/null || echo "0")

    if [[ "$actual_reviews" -eq "$expected_reviews" ]]; then
      print_success "Required approving reviews: ${actual_reviews} (expected: ${expected_reviews})"
    else
      print_error "Required approving reviews: ${actual_reviews} (expected: ${expected_reviews})"
      ((issues++)) || true
    fi

    local dismiss_stale
    dismiss_stale=$(echo "$pr_reviews" | jq -r '.dismiss_stale_reviews' 2>/dev/null || echo "false")
    if [[ "$dismiss_stale" == "true" ]]; then
      print_success "Dismiss stale reviews: enabled"
    else
      print_warning "Dismiss stale reviews: disabled"
      ((issues++)) || true
    fi

    local require_code_owners
    require_code_owners=$(echo "$pr_reviews" | jq -r '.require_code_owner_reviews' 2>/dev/null || echo "false")
    if [[ "$require_code_owners" == "true" ]]; then
      print_success "Require code owner reviews: enabled"
    else
      print_warning "Require code owner reviews: disabled"
      ((issues++)) || true
    fi
  fi

  # Verify conversation resolution
  local require_conversation_resolution
  require_conversation_resolution=$(echo "$protection_data" | jq -r '.required_conversation_resolution.enabled' 2>/dev/null || echo "false")
  if [[ "$require_conversation_resolution" == "true" ]]; then
    print_success "Require conversation resolution: enabled"
  else
    print_warning "Require conversation resolution: disabled"
    ((issues++)) || true
  fi

  # Verify enforce admins
  local enforce_admins
  enforce_admins=$(echo "$protection_data" | jq -r '.enforce_admins.enabled' 2>/dev/null || echo "false")
  if [[ "$enforce_admins" == "true" ]]; then
    print_success "Enforce for administrators: enabled (can bypass)"
  else
    print_warning "Enforce for administrators: disabled"
  fi

  # Verify force push settings
  local allow_force_pushes
  allow_force_pushes=$(echo "$protection_data" | jq -r '.allow_force_pushes.enabled' 2>/dev/null || echo "true")
  if [[ "$allow_force_pushes" == "false" ]]; then
    print_success "Allow force pushes: disabled"
  else
    print_error "Allow force pushes: enabled (should be disabled)"
    ((issues++)) || true
  fi

  # Verify deletion settings
  local allow_deletions
  allow_deletions=$(echo "$protection_data" | jq -r '.allow_deletions.enabled' 2>/dev/null || echo "true")
  if [[ "$allow_deletions" == "false" ]]; then
    print_success "Allow deletions: disabled"
  else
    print_error "Allow deletions: enabled (should be disabled)"
    ((issues++)) || true
  fi

  echo
  if [[ $issues -eq 0 ]]; then
    print_success "All verifications passed for ${branch}"
  else
    print_warning "${issues} issue(s) found for ${branch}"
  fi
  echo

  return $issues
}

# Main execution
main() {
  echo "=========================================="
  echo "  Branch Protection Verification"
  echo "  Repository: ${REPO}"
  echo "=========================================="
  echo

  # Check prerequisites
  check_gh_cli
  echo

  print_info "Note: release-4.17 deleted on 2026-01-17 (OpenShift 4.17 EOL)"
  echo

  local total_issues=0

  # Verify main branch (1 approval)
  if verify_branch "main" 1; then
    : # Success
  else
    ((total_issues++)) || true
  fi

  # Verify release branches (2 approvals)
  for release in "release-4.18" "release-4.19" "release-4.20"; do
    if gh api "/repos/${REPO}/branches/${release}" &> /dev/null; then
      if verify_branch "$release" 2; then
        : # Success
      else
        ((total_issues++)) || true
      fi
    else
      print_info "Skipping ${release} (branch does not exist)"
      echo
    fi
  done

  echo "=========================================="
  if [[ $total_issues -eq 0 ]]; then
    print_success "All branch protections verified successfully!"
  else
    print_warning "Verification completed with issues"
    print_info "Run setup script to fix: ./scripts/setup-branch-protection.sh"
  fi
  echo "=========================================="
  echo
  print_info "View settings on GitHub:"
  echo "  https://github.com/${REPO}/settings/branches"
  echo

  return $total_issues
}

# Run main function
main "$@"
