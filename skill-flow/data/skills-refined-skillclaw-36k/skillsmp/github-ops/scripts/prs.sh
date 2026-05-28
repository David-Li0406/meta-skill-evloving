#!/usr/bin/env bash
#
# prs.sh - Pull Request Operations for GitHub Ops Skill
# MCP Parity: list_pull_requests, get_pull_request, create_pull_request, update_pull_request,
#             merge_pull_request, get_pull_request_diff, get_pull_request_files,
#             list_pull_request_reviews, create_pull_request_review, get_pull_request_status,
#             update_pull_request_branch, get_pull_request_comments, add_pull_request_review_comment
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
LIMIT=30
STATE="open"
JSON_OUTPUT=false
CONFIRM_DESTRUCTIVE=true

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Pull Request Operations - GitHub MCP Server Parity

Actions:
  list              List pull requests
  view              View PR details
  create            Create a new PR
  update            Update a PR
  close             Close a PR
  reopen            Reopen a PR
  merge             Merge a PR
  diff              View PR diff
  files             List PR files
  checks            View PR checks status
  reviews           List PR reviews
  review            Create a PR review
  comments          List PR comments
  comment           Add a review comment
  merge-status      Get merge status

Common Options:
  --owner OWNER     Repository owner
  --repo REPO       Repository name
  --number NUMBER   PR number
  --state STATE     Filter by state (open, closed, merged, all)
  --base BRANCH     Base branch
  --head BRANCH     Head branch
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") list --owner cli --repo cli --state open --limit 10
  $(basename "$0") view --owner cli --repo cli --number 123
  $(basename "$0") diff --owner cli --repo cli --number 123
  $(basename "$0") checks --owner cli --repo cli --number 123
EOF
    exit 0
}

error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}$1${NC}"
}

warn() {
    echo -e "${YELLOW}$1${NC}"
}

info() {
    echo -e "${BLUE}$1${NC}"
}

confirm() {
    if [[ "$CONFIRM_DESTRUCTIVE" == "true" ]]; then
        echo -e "${YELLOW}Warning: $1${NC}"
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Operation cancelled."
            exit 2
        fi
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --owner) OWNER="$2"; shift 2 ;;
            --repo) REPO="$2"; shift 2 ;;
            --number) NUMBER="$2"; shift 2 ;;
            --state) STATE="$2"; shift 2 ;;
            --base) BASE="$2"; shift 2 ;;
            --head) HEAD="$2"; shift 2 ;;
            --title) TITLE="$2"; shift 2 ;;
            --body) BODY="$2"; shift 2 ;;
            --author) AUTHOR="$2"; shift 2 ;;
            --label) LABEL="$2"; shift 2 ;;
            --method) METHOD="$2"; shift 2 ;;
            --event) EVENT="$2"; shift 2 ;;
            --path) FILE_PATH="$2"; shift 2 ;;
            --position) POSITION="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --comments) SHOW_COMMENTS=true; shift ;;
            --json) JSON_OUTPUT=true; shift ;;
            --no-confirm) CONFIRM_DESTRUCTIVE=false; shift ;;
            --draft) DRAFT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: List PRs
action_list() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing PRs for $OWNER/$REPO (state: $STATE, limit: $LIMIT)"
    
    local cmd="gh pr list --repo $OWNER/$REPO --state $STATE --limit $LIMIT"
    
    [[ -n "${AUTHOR:-}" ]] && cmd="$cmd --author $AUTHOR"
    [[ -n "${BASE:-}" ]] && cmd="$cmd --base $BASE"
    [[ -n "${LABEL:-}" ]] && cmd="$cmd --label \"$LABEL\""
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd="$cmd --json number,title,state,author,headRefName,baseRefName,isDraft,createdAt,updatedAt"
    fi
    
    eval "$cmd"
}

# Action: View PR
action_view() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching PR #$NUMBER from $OWNER/$REPO"
    
    local cmd="gh pr view $NUMBER --repo $OWNER/$REPO"
    
    [[ "${SHOW_COMMENTS:-false}" == "true" ]] && cmd="$cmd --comments"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd="$cmd --json number,title,body,state,author,headRefName,baseRefName,isDraft,mergeable,additions,deletions,changedFiles,commits,reviewDecision,statusCheckRollup,createdAt,updatedAt,mergedAt"
    fi
    
    eval "$cmd"
}

# Action: Create PR
action_create() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TITLE:-}" ]] && error "Missing --title"
    [[ -z "${HEAD:-}" ]] && error "Missing --head"
    
    confirm "This will create a new PR in $OWNER/$REPO"
    
    info "Creating PR: $TITLE"
    
    local base="${BASE:-main}"
    local cmd="gh pr create --repo $OWNER/$REPO --title \"$TITLE\" --head $HEAD --base $base"
    
    [[ -n "${BODY:-}" ]] && cmd="$cmd --body \"$BODY\""
    [[ "${DRAFT:-false}" == "true" ]] && cmd="$cmd --draft"
    
    eval "$cmd"
    success "PR created successfully"
}

# Action: Update PR
action_update() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    confirm "This will update PR #$NUMBER in $OWNER/$REPO"
    
    info "Updating PR #$NUMBER"
    
    local cmd="gh pr edit $NUMBER --repo $OWNER/$REPO"
    
    [[ -n "${TITLE:-}" ]] && cmd="$cmd --title \"$TITLE\""
    [[ -n "${BODY:-}" ]] && cmd="$cmd --body \"$BODY\""
    [[ -n "${BASE:-}" ]] && cmd="$cmd --base $BASE"
    
    eval "$cmd"
    success "PR updated successfully"
}

# Action: Close PR
action_close() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    confirm "This will close PR #$NUMBER in $OWNER/$REPO"
    
    info "Closing PR #$NUMBER"
    gh pr close "$NUMBER" --repo "$OWNER/$REPO"
    success "PR closed"
}

# Action: Reopen PR
action_reopen() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Reopening PR #$NUMBER"
    gh pr reopen "$NUMBER" --repo "$OWNER/$REPO"
    success "PR reopened"
}

# Action: Merge PR
action_merge() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    confirm "This will MERGE PR #$NUMBER in $OWNER/$REPO"
    
    local method="${METHOD:-merge}"
    
    info "Merging PR #$NUMBER (method: $method)"
    
    case "$method" in
        merge) gh pr merge "$NUMBER" --repo "$OWNER/$REPO" --merge ;;
        squash) gh pr merge "$NUMBER" --repo "$OWNER/$REPO" --squash ;;
        rebase) gh pr merge "$NUMBER" --repo "$OWNER/$REPO" --rebase ;;
        *) error "Unknown merge method: $method (use merge, squash, or rebase)" ;;
    esac
    
    success "PR merged"
}

# Action: View diff
action_diff() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching diff for PR #$NUMBER"
    gh pr diff "$NUMBER" --repo "$OWNER/$REPO"
}

# Action: List files
action_files() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Listing files for PR #$NUMBER"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/pulls/$NUMBER/files?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/pulls/$NUMBER/files?per_page=$LIMIT" \
            --jq '.[] | "\(.status)\t\(.filename)\t+\(.additions)/-\(.deletions)"' | column -t -s $'\t'
    fi
}

# Action: View checks
action_checks() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching checks for PR #$NUMBER"
    gh pr checks "$NUMBER" --repo "$OWNER/$REPO"
}

# Action: List reviews
action_reviews() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Listing reviews for PR #$NUMBER"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/pulls/$NUMBER/reviews"
    else
        gh api "repos/$OWNER/$REPO/pulls/$NUMBER/reviews" \
            --jq '.[] | "[\(.state)] @\(.user.login): \(.body // "(no comment)")"'
    fi
}

# Action: Create review
action_review() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    [[ -z "${EVENT:-}" ]] && error "Missing --event (approve, comment, request_changes)"
    
    confirm "This will submit a review on PR #$NUMBER"
    
    info "Creating review on PR #$NUMBER"
    
    local cmd="gh pr review $NUMBER --repo $OWNER/$REPO"
    
    case "$EVENT" in
        approve) cmd="$cmd --approve" ;;
        comment) cmd="$cmd --comment" ;;
        request_changes) cmd="$cmd --request-changes" ;;
        *) error "Unknown event: $EVENT (use approve, comment, or request_changes)" ;;
    esac
    
    [[ -n "${BODY:-}" ]] && cmd="$cmd --body \"$BODY\""
    
    eval "$cmd"
    success "Review submitted"
}

# Action: List comments
action_comments() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Listing comments for PR #$NUMBER"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/pulls/$NUMBER/comments?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/pulls/$NUMBER/comments?per_page=$LIMIT" \
            --jq '.[] | "[\(.created_at[0:10])] @\(.user.login) on \(.path):\(.line // .original_line): \(.body | split("\n")[0])"'
    fi
}

# Action: Add review comment
action_comment() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    [[ -z "${BODY:-}" ]] && error "Missing --body"
    [[ -z "${FILE_PATH:-}" ]] && error "Missing --path (file path)"
    [[ -z "${POSITION:-}" ]] && error "Missing --position (line number)"
    
    confirm "This will add a review comment on PR #$NUMBER"
    
    info "Adding comment to PR #$NUMBER at $FILE_PATH:$POSITION"
    
    # Get the latest commit SHA
    local commit_id
    commit_id=$(gh api "repos/$OWNER/$REPO/pulls/$NUMBER" --jq '.head.sha')
    
    gh api "repos/$OWNER/$REPO/pulls/$NUMBER/comments" \
        -f body="$BODY" \
        -f path="$FILE_PATH" \
        -F line="$POSITION" \
        -f commit_id="$commit_id"
    
    success "Comment added"
}

# Action: Get merge status
action_merge_status() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching merge status for PR #$NUMBER"
    
    gh api "repos/$OWNER/$REPO/pulls/$NUMBER" \
        --jq '{
            mergeable: .mergeable,
            mergeable_state: .mergeable_state,
            rebaseable: .rebaseable,
            merged: .merged,
            merged_by: .merged_by.login,
            merge_commit_sha: .merge_commit_sha
        }'
}

main() {
    [[ $# -eq 0 ]] && usage
    
    local action="$1"
    shift
    
    parse_args "$@"
    
    case "$action" in
        list) action_list ;;
        view) action_view ;;
        create) action_create ;;
        update) action_update ;;
        close) action_close ;;
        reopen) action_reopen ;;
        merge) action_merge ;;
        diff) action_diff ;;
        files) action_files ;;
        checks) action_checks ;;
        reviews) action_reviews ;;
        review) action_review ;;
        comments) action_comments ;;
        comment) action_comment ;;
        merge-status) action_merge_status ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action. Use --help for usage." ;;
    esac
}

main "$@"
