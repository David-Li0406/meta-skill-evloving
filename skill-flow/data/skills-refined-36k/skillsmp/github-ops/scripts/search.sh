#!/usr/bin/env bash
#
# search.sh - Search Operations for GitHub Ops Skill
# MCP Parity: search_repositories, search_code, search_issues, search_users, search_commits
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

LIMIT=30
JSON_OUTPUT=false

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Search Operations - GitHub MCP Server Parity

Actions:
  repos             Search repositories
  code              Search code
  issues            Search issues
  prs               Search pull requests
  users             Search users
  commits           Search commits

Common Options:
  --query QUERY     Search query (required)
  --sort FIELD      Sort by field
  --order ORDER     Sort order (asc, desc)
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") repos --query "language:go stars:>1000" --sort stars
  $(basename "$0") code --query "useState repo:facebook/react" --limit 10
  $(basename "$0") issues --query "is:open label:bug repo:cli/cli"
  $(basename "$0") users --query "location:london followers:>100"
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}"; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --query) QUERY="$2"; shift 2 ;;
            --sort) SORT="$2"; shift 2 ;;
            --order) ORDER="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: Search repositories
action_repos() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    info "Searching repositories: $QUERY"
    
    # Split query into array for proper argument handling
    # shellcheck disable=SC2086
    local -a cmd=(gh search repos $QUERY --limit "$LIMIT")
    [[ -n "${SORT:-}" ]] && cmd+=(--sort "$SORT")
    [[ -n "${ORDER:-}" ]] && cmd+=(--order "$ORDER")
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd+=(--json fullName,description,stargazersCount,forksCount,updatedAt,language,isArchived)
    fi
    
    "${cmd[@]}"
}

# Action: Search code
action_code() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    info "Searching code: $QUERY"
    
    # shellcheck disable=SC2086
    local -a cmd=(gh search code $QUERY --limit "$LIMIT")
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd+=(--json repository,path,textMatches)
    fi
    
    "${cmd[@]}"
}

# Action: Search issues
action_issues() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    info "Searching issues: $QUERY"
    
    # shellcheck disable=SC2086
    local -a cmd=(gh search issues $QUERY --limit "$LIMIT")
    [[ -n "${SORT:-}" ]] && cmd+=(--sort "$SORT")
    [[ -n "${ORDER:-}" ]] && cmd+=(--order "$ORDER")
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd+=(--json repository,number,title,state,author,labels,createdAt,updatedAt)
    fi
    
    "${cmd[@]}"
}

# Action: Search PRs
action_prs() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    info "Searching pull requests: $QUERY"
    
    # shellcheck disable=SC2086
    local -a cmd=(gh search prs $QUERY --limit "$LIMIT")
    [[ -n "${SORT:-}" ]] && cmd+=(--sort "$SORT")
    [[ -n "${ORDER:-}" ]] && cmd+=(--order "$ORDER")
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd+=(--json repository,number,title,state,author,isDraft,createdAt,updatedAt)
    fi
    
    "${cmd[@]}"
}

# Action: Search users
action_users() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    info "Searching users: $QUERY"
    
    # gh search doesn't have users, use API
    local q
    q=$(echo "$QUERY" | jq -sRr @uri)
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "search/users?q=$q&per_page=$LIMIT"
    else
        gh api "search/users?q=$q&per_page=$LIMIT" \
            --jq '.items[] | "@\(.login)\t\(.type)\t\(.html_url)"' | column -t -s $'\t'
    fi
}

# Action: Search commits
action_commits() {
    [[ -z "${QUERY:-}" ]] && error "Missing --query"
    
    info "Searching commits: $QUERY"
    
    # shellcheck disable=SC2086
    local -a cmd=(gh search commits $QUERY --limit "$LIMIT")
    [[ -n "${SORT:-}" ]] && cmd+=(--sort "$SORT")
    [[ -n "${ORDER:-}" ]] && cmd+=(--order "$ORDER")
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cmd+=(--json repository,sha,commit)
    fi
    
    "${cmd[@]}"
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        repos) action_repos ;;
        code) action_code ;;
        issues) action_issues ;;
        prs) action_prs ;;
        users) action_users ;;
        commits) action_commits ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
