#!/usr/bin/env bash
#
# issues.sh - Issue Operations for GitHub Ops Skill
# MCP Parity: list_issues, get_issue, create_issue, update_issue, 
#             add_issue_comment, list_issue_comments, labels operations
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

Issue Operations - GitHub MCP Server Parity

Actions:
  list              List issues
  view              View issue details
  create            Create a new issue
  update            Update an issue
  close             Close an issue
  reopen            Reopen an issue
  comment           Add a comment to an issue
  comments          List issue comments
  add-labels        Add labels to an issue
  remove-labels     Remove labels from an issue
  labels            List repository labels
  create-label      Create a label
  delete-label      Delete a label

Common Options:
  --owner OWNER     Repository owner
  --repo REPO       Repository name
  --number NUMBER   Issue number
  --state STATE     Filter by state (open, closed, all)
  --label LABEL     Filter by label
  --assignee USER   Filter by assignee
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") list --owner cli --repo cli --state open --limit 10
  $(basename "$0") view --owner cli --repo cli --number 123
  $(basename "$0") create --owner myorg --repo myrepo --title "Bug report" --body "Description"
  $(basename "$0") comment --owner myorg --repo myrepo --number 123 --body "My comment"
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
            --label) LABEL="$2"; shift 2 ;;
            --labels) LABELS="$2"; shift 2 ;;
            --assignee) ASSIGNEE="$2"; shift 2 ;;
            --title) TITLE="$2"; shift 2 ;;
            --body) BODY="$2"; shift 2 ;;
            --name) NAME="$2"; shift 2 ;;
            --color) COLOR="$2"; shift 2 ;;
            --description) DESCRIPTION="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --comments) SHOW_COMMENTS=true; shift ;;
            --json) JSON_OUTPUT=true; shift ;;
            --no-confirm) CONFIRM_DESTRUCTIVE=false; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: List issues
action_list() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing issues for $OWNER/$REPO (state: $STATE, limit: $LIMIT)"
    
    local cmd="gh issue list --repo $OWNER/$REPO --state $STATE --limit $LIMIT"
    
    [[ -n "${LABEL:-}" ]] && cmd="$cmd --label \"$LABEL\""
    [[ -n "${ASSIGNEE:-}" ]] && cmd="$cmd --assignee $ASSIGNEE"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd="$cmd --json number,title,state,author,labels,createdAt,updatedAt"
    fi
    
    eval "$cmd"
}

# Action: View issue
action_view() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching issue #$NUMBER from $OWNER/$REPO"
    
    local cmd="gh issue view $NUMBER --repo $OWNER/$REPO"
    
    [[ "${SHOW_COMMENTS:-false}" == "true" ]] && cmd="$cmd --comments"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd="$cmd --json number,title,body,state,author,labels,assignees,milestone,createdAt,updatedAt,closedAt,comments"
    fi
    
    eval "$cmd"
}

# Action: Create issue
action_create() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TITLE:-}" ]] && error "Missing --title"
    
    confirm "This will create a new issue in $OWNER/$REPO"
    
    info "Creating issue: $TITLE"
    
    local cmd="gh issue create --repo $OWNER/$REPO --title \"$TITLE\""
    
    [[ -n "${BODY:-}" ]] && cmd="$cmd --body \"$BODY\""
    [[ -n "${LABELS:-}" ]] && cmd="$cmd --label \"$LABELS\""
    [[ -n "${ASSIGNEE:-}" ]] && cmd="$cmd --assignee $ASSIGNEE"
    
    eval "$cmd"
    success "Issue created successfully"
}

# Action: Update issue
action_update() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    confirm "This will update issue #$NUMBER in $OWNER/$REPO"
    
    info "Updating issue #$NUMBER"
    
    local cmd="gh issue edit $NUMBER --repo $OWNER/$REPO"
    
    [[ -n "${TITLE:-}" ]] && cmd="$cmd --title \"$TITLE\""
    [[ -n "${BODY:-}" ]] && cmd="$cmd --body \"$BODY\""
    
    eval "$cmd"
    success "Issue updated successfully"
}

# Action: Close issue
action_close() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    confirm "This will close issue #$NUMBER in $OWNER/$REPO"
    
    info "Closing issue #$NUMBER"
    gh issue close "$NUMBER" --repo "$OWNER/$REPO"
    success "Issue closed"
}

# Action: Reopen issue
action_reopen() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Reopening issue #$NUMBER"
    gh issue reopen "$NUMBER" --repo "$OWNER/$REPO"
    success "Issue reopened"
}

# Action: Add comment
action_comment() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    [[ -z "${BODY:-}" ]] && error "Missing --body"
    
    confirm "This will add a comment to issue #$NUMBER"
    
    info "Adding comment to issue #$NUMBER"
    gh issue comment "$NUMBER" --repo "$OWNER/$REPO" --body "$BODY"
    success "Comment added"
}

# Action: List comments
action_comments() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Listing comments for issue #$NUMBER"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/issues/$NUMBER/comments?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/issues/$NUMBER/comments?per_page=$LIMIT" \
            --jq '.[] | "[\(.created_at[0:10])] @\(.user.login): \(.body | split("\n")[0])"'
    fi
}

# Action: Add labels
action_add_labels() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    [[ -z "${LABELS:-}" ]] && error "Missing --labels"
    
    info "Adding labels to issue #$NUMBER: $LABELS"
    
    # Convert comma-separated to space-separated for gh
    local labels_array
    IFS=',' read -ra labels_array <<< "$LABELS"
    
    for label in "${labels_array[@]}"; do
        gh issue edit "$NUMBER" --repo "$OWNER/$REPO" --add-label "$label"
    done
    
    success "Labels added"
}

# Action: Remove labels
action_remove_labels() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    [[ -z "${LABELS:-}" ]] && error "Missing --labels"
    
    info "Removing labels from issue #$NUMBER: $LABELS"
    
    local labels_array
    IFS=',' read -ra labels_array <<< "$LABELS"
    
    for label in "${labels_array[@]}"; do
        gh issue edit "$NUMBER" --repo "$OWNER/$REPO" --remove-label "$label"
    done
    
    success "Labels removed"
}

# Action: List labels
action_labels() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing labels for $OWNER/$REPO"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/labels?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/labels?per_page=$LIMIT" \
            --jq '.[] | "\(.name)\t#\(.color)\t\(.description // "")"' | column -t -s $'\t'
    fi
}

# Action: Create label
action_create_label() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NAME:-}" ]] && error "Missing --name"
    
    confirm "This will create label '$NAME' in $OWNER/$REPO"
    
    local color="${COLOR:-0366d6}"
    local description="${DESCRIPTION:-}"
    
    info "Creating label: $NAME"
    gh api "repos/$OWNER/$REPO/labels" \
        -f name="$NAME" \
        -f color="$color" \
        -f description="$description"
    
    success "Label created"
}

# Action: Delete label
action_delete_label() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NAME:-}" ]] && error "Missing --name"
    
    confirm "This will DELETE label '$NAME' from $OWNER/$REPO"
    
    info "Deleting label: $NAME"
    gh api "repos/$OWNER/$REPO/labels/$NAME" -X DELETE
    success "Label deleted"
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
        comment) action_comment ;;
        comments) action_comments ;;
        add-labels) action_add_labels ;;
        remove-labels) action_remove_labels ;;
        labels) action_labels ;;
        create-label) action_create_label ;;
        delete-label) action_delete_label ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action. Use --help for usage." ;;
    esac
}

main "$@"
