#!/bin/bash
set -euo pipefail

# Git Ship - Complete git workflow automation
# Usage: ship.sh [command] [options]
#
# Commands:
#   ship     - Full workflow: commit → push → PR → CI wait → results (default)
#   full     - Full workflow including merge
#   commit   - Review changes for commit
#   pr       - Push and create PR
#   wait     - Wait for CI checks
#   status   - Fetch CI status and PR comments
#   merge    - Merge PR with cleanup

# Configuration
DEFAULT_WAIT_MINUTES=8
DEFAULT_MERGE_STRATEGY="squash"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
ACTION="${1:-ship}"
PLAN_FILE=""
WAIT_MINUTES=$DEFAULT_WAIT_MINUTES
MERGE_STRATEGY=$DEFAULT_MERGE_STRATEGY
AUTO_MERGE=false
DELETE_BRANCH=true

# Skip first arg if it's a command
case "${1:-}" in
    ship|full|commit|pr|wait|status|merge)
        shift || true
        ;;
esac

while [[ $# -gt 0 ]]; do
    case $1 in
        --plan)
            PLAN_FILE="$2"
            shift 2
            ;;
        --wait)
            WAIT_MINUTES="${2%m}"
            shift 2
            ;;
        --merge|--strategy)
            MERGE_STRATEGY="$2"
            shift 2
            ;;
        --auto-merge)
            AUTO_MERGE=true
            shift
            ;;
        --no-delete-branch)
            DELETE_BRANCH=false
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Helper functions
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if we're on a feature branch (not main/master)
check_branch() {
    local branch
    branch=$(git branch --show-current)

    if [[ "$branch" == "main" || "$branch" == "master" ]]; then
        print_error "Cannot ship from $branch. Create a feature branch first."
        echo "Suggestion: git checkout -b feat/my-feature"
        exit 1
    fi

    echo "$branch"
}

# Get the main branch name (main or master)
get_main_branch() {
    if git show-ref --verify --quiet refs/heads/main; then
        echo "main"
    elif git show-ref --verify --quiet refs/heads/master; then
        echo "master"
    else
        echo "main"  # Default assumption
    fi
}

# Review changes for commit
review_changes() {
    print_header "Staged Changes"
    git diff --cached --stat 2>/dev/null || echo "No staged changes"

    print_header "Unstaged Changes"
    git diff --stat 2>/dev/null || echo "No unstaged changes"

    print_header "Untracked Files"
    git status --porcelain 2>/dev/null | grep "^??" | sed 's/^?? //' || echo "No untracked files"
}

# Wait for CI checks with timeout
wait_for_ci() {
    local pr_number=$1
    local timeout_seconds=$((WAIT_MINUTES * 60))

    echo "Waiting up to ${WAIT_MINUTES} minutes for CI checks..."
    echo ""

    # Use timeout command if available
    if command -v timeout &> /dev/null; then
        if timeout "$timeout_seconds" gh pr checks "$pr_number" --watch --fail-fast 2>/dev/null; then
            print_success "All CI checks passed!"
            return 0
        else
            local exit_code=$?
            if [[ $exit_code -eq 124 ]]; then
                print_warning "Timeout waiting for CI after ${WAIT_MINUTES} minutes"
                echo ""
                echo "Options:"
                echo "1. Continue waiting: ship.sh wait --wait 15m"
                echo "2. Check GitHub Actions: gh run view"
                echo "3. Enable auto-merge: ship.sh merge --auto-merge"
                return 2
            else
                print_error "CI checks failed"
                echo ""
                echo "View details: gh pr checks $pr_number"
                return 1
            fi
        fi
    else
        # Fallback without timeout command
        if gh pr checks "$pr_number" --watch --fail-fast 2>/dev/null; then
            print_success "All CI checks passed!"
            return 0
        else
            print_error "CI checks failed or timed out"
            return 1
        fi
    fi
}

# Fetch PR status including CI, comments, and reviews
fetch_status() {
    local pr_number=$1

    print_header "CI Status"
    if ! gh pr checks "$pr_number" 2>/dev/null; then
        echo "No checks found or checks still pending"
    fi

    print_header "PR Comments"
    local comments
    comments=$(gh pr view "$pr_number" --json comments --jq '.comments[] | "[\(.author.login)] \(.body | split("\n")[0])"' 2>/dev/null || true)
    if [[ -n "$comments" ]]; then
        echo "$comments"
    else
        echo "No comments"
    fi

    print_header "Review Status"
    local reviews
    reviews=$(gh pr view "$pr_number" --json reviews --jq '.reviews[] | "[\(.author.login)] \(.state)"' 2>/dev/null || true)
    if [[ -n "$reviews" ]]; then
        echo "$reviews"
    else
        echo "No reviews yet"
    fi
}

# Merge the PR with cleanup
merge_pr() {
    local pr_number=$1
    local strategy=$2
    local delete_branch=$3

    print_header "Merging PR #$pr_number"
    echo "Strategy: $strategy"

    # Check if PR is mergeable
    local mergeable
    mergeable=$(gh pr view "$pr_number" --json mergeable --jq '.mergeable' 2>/dev/null || echo "UNKNOWN")

    if [[ "$mergeable" == "CONFLICTING" ]]; then
        print_error "PR has merge conflicts"
        echo ""
        echo "To resolve:"
        echo "1. git fetch origin"
        echo "2. git rebase origin/$(get_main_branch)"
        echo "3. Resolve conflicts in your editor"
        echo "4. git add <resolved-files>"
        echo "5. git rebase --continue"
        echo "6. git push --force-with-lease"
        echo "7. ship.sh merge --strategy $strategy"
        return 1
    fi

    if [[ "$mergeable" == "UNKNOWN" ]]; then
        print_warning "Merge status unknown. Attempting merge anyway..."
    fi

    # Build merge args
    local merge_args="--$strategy"
    if [[ "$delete_branch" == "true" ]]; then
        merge_args="$merge_args --delete-branch"
    fi

    # Perform merge
    if gh pr merge "$pr_number" $merge_args; then
        print_success "PR merged successfully!"

        # Clean up local branch
        local current_branch
        current_branch=$(git branch --show-current)
        local main_branch
        main_branch=$(get_main_branch)

        if [[ "$current_branch" != "$main_branch" ]]; then
            print_header "Cleaning up local branch"
            git checkout "$main_branch"
            git pull origin "$main_branch"
            git branch -d "$current_branch" 2>/dev/null && print_success "Local branch deleted" || echo "Note: Local branch may have unmerged changes"
            print_success "Switched to $main_branch and pulled latest"
        fi

        return 0
    else
        print_error "Merge failed"
        return 1
    fi
}

# Enable auto-merge
enable_auto_merge() {
    local pr_number=$1
    local strategy=$2

    print_header "Enabling Auto-Merge"

    if gh pr merge "$pr_number" --auto --"$strategy"; then
        print_success "Auto-merge enabled. PR will merge when all checks pass."
        return 0
    else
        print_error "Failed to enable auto-merge"
        echo "Note: Auto-merge requires branch protection rules to be configured"
        return 1
    fi
}

# Get current PR number
get_pr_number() {
    local pr_number
    pr_number=$(gh pr view --json number --jq '.number' 2>/dev/null || echo "")

    if [[ -z "$pr_number" ]]; then
        print_error "No PR found for current branch"
        echo "Create a PR first: ship.sh pr"
        exit 1
    fi

    echo "$pr_number"
}

# Main execution based on action
case $ACTION in
    commit)
        review_changes
        echo ""
        echo "Ready to commit. Generate a conventional commit message based on these changes."
        echo ""
        echo "Format: <type>(<scope>): <description>"
        echo "Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore"
        ;;

    pr)
        BRANCH=$(check_branch)
        print_header "Pushing to origin"
        git push -u origin "$BRANCH"
        print_success "Branch pushed"
        echo ""
        echo "Ready to create PR. Generate a PR description with:"
        echo "- Summary of changes"
        echo "- Type of change"
        echo "- Testing notes"
        echo "- Related issues"
        ;;

    wait)
        PR_NUMBER=$(get_pr_number)
        wait_for_ci "$PR_NUMBER"
        ;;

    status)
        PR_NUMBER=$(get_pr_number)
        fetch_status "$PR_NUMBER"
        ;;

    merge)
        PR_NUMBER=$(get_pr_number)

        if [[ "$AUTO_MERGE" == "true" ]]; then
            enable_auto_merge "$PR_NUMBER" "$MERGE_STRATEGY"
        else
            merge_pr "$PR_NUMBER" "$MERGE_STRATEGY" "$DELETE_BRANCH"
        fi
        ;;

    full)
        BRANCH=$(check_branch)
        review_changes

        print_header "Full Ship Workflow"
        echo "Branch: $BRANCH"
        echo "Plan: ${PLAN_FILE:-none}"
        echo "CI Wait: ${WAIT_MINUTES} minutes"
        echo "Merge Strategy: $MERGE_STRATEGY"
        echo "Auto-Merge: $AUTO_MERGE"
        echo ""
        echo "Steps to execute:"
        echo "1. Stage all changes: git add ."
        echo "2. Create commit with conventional message"
        echo "3. Push to origin: git push -u origin $BRANCH"
        echo "4. Create PR with gh pr create"
        echo "5. Wait for CI: ship.sh wait"
        echo "6. Merge: ship.sh merge --strategy $MERGE_STRATEGY"
        echo "7. Report results"
        ;;

    ship|*)
        BRANCH=$(check_branch)
        review_changes

        print_header "Ship Workflow"
        echo "Branch: $BRANCH"
        echo "Plan: ${PLAN_FILE:-none}"
        echo "CI Wait: ${WAIT_MINUTES} minutes"
        echo ""
        echo "Steps to execute:"
        echo "1. Stage all changes: git add ."
        echo "2. Create commit with conventional message"
        echo "3. Push to origin: git push -u origin $BRANCH"
        echo "4. Create PR with gh pr create"
        echo "5. Wait for CI: ship.sh wait"
        echo "6. Fetch and report results: ship.sh status"
        echo ""
        echo "To also merge after CI passes, use: ship.sh full --merge squash"
        ;;
esac
