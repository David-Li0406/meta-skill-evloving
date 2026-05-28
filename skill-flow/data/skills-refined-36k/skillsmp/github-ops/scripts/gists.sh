#!/usr/bin/env bash
#
# gists.sh - Gist Operations for GitHub Ops Skill
# MCP Parity: list_gists, get_gist, create_gist, update_gist, delete_gist, fork_gist
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

LIMIT=30
JSON_OUTPUT=false
NO_CONFIRM=false

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Gist Operations - GitHub MCP Server Parity

Actions:
  list              List your gists (or a user's gists)
  view              View a gist
  create            Create a new gist
  edit              Edit a gist
  delete            Delete a gist
  fork              Fork a gist
  starred           List starred gists

Common Options:
  --id ID           Gist ID (for view/edit/delete/fork)
  --username USER   Username (for list)
  --files "f1 f2"   Files to include (space-separated paths for create)
  --description D   Gist description
  --public          Make gist public (default: secret)
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --no-confirm      Skip confirmation for destructive actions
  --help            Show this help message

Examples:
  $(basename "$0") list --limit 10
  $(basename "$0") list --username octocat
  $(basename "$0") view --id abc123
  $(basename "$0") create --files "script.sh config.json" --description "My scripts" --public
  $(basename "$0") edit --id abc123 --description "Updated description"
  $(basename "$0") delete --id abc123
  $(basename "$0") fork --id abc123
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}"; }
success() { echo -e "${GREEN}$1${NC}"; }
warn() { echo -e "${YELLOW}$1${NC}"; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --id) GIST_ID="$2"; shift 2 ;;
            --username) USERNAME="$2"; shift 2 ;;
            --files) FILES="$2"; shift 2 ;;
            --description) DESCRIPTION="$2"; shift 2 ;;
            --public) PUBLIC=true; shift ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --no-confirm) NO_CONFIRM=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

confirm() {
    [[ "$NO_CONFIRM" == "true" ]] && return 0
    echo -en "${YELLOW}$1 [y/N]: ${NC}"
    read -r response
    [[ "$response" =~ ^[Yy]$ ]]
}

# Action: List gists
action_list() {
    if [[ -n "${USERNAME:-}" ]]; then
        info "Listing gists for @$USERNAME"
        endpoint="users/$USERNAME/gists"
    else
        info "Listing your gists"
        endpoint="gists"
    fi
    
    local result
    result=$(gh api "$endpoint?per_page=$LIMIT" 2>&1) || {
        error "Failed to fetch gists"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result"
    else
        echo "$result" | jq -r '.[] | 
            "\(.id)\t\(.public | if . then "public" else "secret" end)\t\(.files | keys | .[0])\t\(.description // "(no description)" | .[0:40])\t\(.updated_at)"' \
            | column -t -s $'\t'
    fi
}

# Action: View a gist
action_view() {
    [[ -z "${GIST_ID:-}" ]] && error "Missing --id"
    
    info "Fetching gist $GIST_ID"
    
    local result
    result=$(gh gist view "$GIST_ID" --files 2>&1) || {
        error "Failed to fetch gist $GIST_ID"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "gists/$GIST_ID"
    else
        # Show gist info first
        local gist_info
        gist_info=$(gh api "gists/$GIST_ID" --jq '{id, description, public, files: (.files | keys), owner: .owner.login, created_at, updated_at, html_url}')
        echo "$gist_info" | jq -r '"
ID: \(.id)
Owner: @\(.owner)
Public: \(.public)
Description: \(.description // "(none)")
Files: \(.files | join(", "))
Created: \(.created_at)
Updated: \(.updated_at)
URL: \(.html_url)
"'
        echo "--- Contents ---"
        echo "$result"
    fi
}

# Action: Create a gist
action_create() {
    [[ -z "${FILES:-}" ]] && error "Missing --files"
    
    info "Creating gist"
    
    local -a cmd=(gh gist create)
    
    # Add files
    for file in $FILES; do
        if [[ -f "$file" ]]; then
            cmd+=("$file")
        else
            error "File not found: $file"
        fi
    done
    
    [[ -n "${DESCRIPTION:-}" ]] && cmd+=(--desc "$DESCRIPTION")
    [[ "${PUBLIC:-false}" == "true" ]] && cmd+=(--public)
    
    local result
    result=$("${cmd[@]}" 2>&1) || {
        error "Failed to create gist: $result"
    }
    
    success "Gist created: $result"
}

# Action: Edit a gist
action_edit() {
    [[ -z "${GIST_ID:-}" ]] && error "Missing --id"
    
    info "Editing gist $GIST_ID"
    
    local -a cmd=(gh gist edit "$GIST_ID")
    
    # If files provided, add them
    if [[ -n "${FILES:-}" ]]; then
        for file in $FILES; do
            if [[ -f "$file" ]]; then
                cmd+=(--add "$file")
            else
                error "File not found: $file"
            fi
        done
    fi
    
    # For description update, use API
    if [[ -n "${DESCRIPTION:-}" ]]; then
        gh api "gists/$GIST_ID" -X PATCH -f description="$DESCRIPTION" >/dev/null 2>&1 || {
            error "Failed to update description"
        }
        success "Description updated"
    fi
    
    if [[ -n "${FILES:-}" ]]; then
        "${cmd[@]}" || error "Failed to edit gist"
        success "Gist updated"
    fi
}

# Action: Delete a gist
action_delete() {
    [[ -z "${GIST_ID:-}" ]] && error "Missing --id"
    
    if ! confirm "Are you sure you want to delete gist $GIST_ID?"; then
        warn "Cancelled"
        return 0
    fi
    
    info "Deleting gist $GIST_ID"
    
    gh gist delete "$GIST_ID" 2>&1 || {
        error "Failed to delete gist $GIST_ID"
    }
    
    success "Gist $GIST_ID deleted"
}

# Action: Fork a gist
action_fork() {
    [[ -z "${GIST_ID:-}" ]] && error "Missing --id"
    
    info "Forking gist $GIST_ID"
    
    local result
    result=$(gh api "gists/$GIST_ID/forks" -X POST 2>&1) || {
        error "Failed to fork gist: $result"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result"
    else
        local url
        url=$(echo "$result" | jq -r '.html_url')
        success "Gist forked: $url"
    fi
}

# Action: List starred gists
action_starred() {
    info "Listing starred gists"
    
    local result
    result=$(gh api "gists/starred?per_page=$LIMIT" 2>&1) || {
        error "Failed to fetch starred gists"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result"
    else
        local count
        count=$(echo "$result" | jq 'length')
        if [[ "$count" == "0" ]]; then
            echo "No starred gists found."
            return 0
        fi
        
        echo "$result" | jq -r '.[] | 
            "\(.id)\t@\(.owner.login)\t\(.files | keys | .[0])\t\(.description // "(no description)" | .[0:40])"' \
            | column -t -s $'\t'
    fi
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        list) action_list ;;
        view) action_view ;;
        create) action_create ;;
        edit) action_edit ;;
        delete) action_delete ;;
        fork) action_fork ;;
        starred) action_starred ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
