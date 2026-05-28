#!/usr/bin/env bash
#
# users.sh - User Operations for GitHub Ops Skill
# MCP Parity: get_me, get_user
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

User Operations - GitHub MCP Server Parity

Actions:
  me                Get current authenticated user
  profile           Get user profile
  followers         List followers
  following         List following
  repos             List user's repositories
  gists             List user's gists
  emails            Get authenticated user's emails

Common Options:
  --username USER   Username
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") me
  $(basename "$0") profile --username octocat
  $(basename "$0") followers --username octocat --limit 10
  $(basename "$0") repos --username torvalds
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}"; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --username) USERNAME="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

action_me() {
    info "Fetching current user"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api user
    else
        gh api user --jq '{
            login: .login,
            name: .name,
            email: .email,
            company: .company,
            location: .location,
            bio: .bio,
            public_repos: .public_repos,
            followers: .followers,
            following: .following,
            created_at: .created_at
        }'
    fi
}

action_profile() {
    [[ -z "${USERNAME:-}" ]] && error "Missing --username"
    
    info "Fetching profile for @$USERNAME"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "users/$USERNAME"
    else
        gh api "users/$USERNAME" --jq '{
            login: .login,
            name: .name,
            company: .company,
            location: .location,
            bio: .bio,
            public_repos: .public_repos,
            followers: .followers,
            following: .following,
            created_at: .created_at,
            html_url: .html_url
        }'
    fi
}

action_followers() {
    local user="${USERNAME:-}"
    local endpoint
    
    if [[ -z "$user" ]]; then
        endpoint="user/followers"
        info "Listing your followers"
    else
        endpoint="users/$user/followers"
        info "Listing followers for @$user"
    fi
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "$endpoint?per_page=$LIMIT"
    else
        gh api "$endpoint?per_page=$LIMIT" --jq '.[].login'
    fi
}

action_following() {
    local user="${USERNAME:-}"
    local endpoint
    
    if [[ -z "$user" ]]; then
        endpoint="user/following"
        info "Listing who you follow"
    else
        endpoint="users/$user/following"
        info "Listing who @$user follows"
    fi
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "$endpoint?per_page=$LIMIT"
    else
        gh api "$endpoint?per_page=$LIMIT" --jq '.[].login'
    fi
}

action_repos() {
    [[ -z "${USERNAME:-}" ]] && error "Missing --username"
    
    info "Listing repos for @$USERNAME"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "users/$USERNAME/repos?per_page=$LIMIT&sort=updated"
    else
        gh api "users/$USERNAME/repos?per_page=$LIMIT&sort=updated" \
            --jq '.[] | "\(.name)\t\(.stargazers_count) stars\t\(.language // "-")\t\(.description // "" | .[0:50])"' | column -t -s $'\t'
    fi
}

action_gists() {
    [[ -z "${USERNAME:-}" ]] && error "Missing --username"
    
    info "Listing gists for @$USERNAME"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "users/$USERNAME/gists?per_page=$LIMIT"
    else
        gh api "users/$USERNAME/gists?per_page=$LIMIT" \
            --jq '.[] | "\(.id)\t\(.public)\t\(.description // "(no description)" | .[0:50])"' | column -t -s $'\t'
    fi
}

action_emails() {
    info "Fetching your email addresses"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api user/emails
    else
        gh api user/emails --jq '.[] | "\(.email)\t\(if .primary then "PRIMARY" else "" end)\t\(if .verified then "verified" else "unverified" end)"' | column -t -s $'\t'
    fi
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        me) action_me ;;
        profile) action_profile ;;
        followers) action_followers ;;
        following) action_following ;;
        repos) action_repos ;;
        gists) action_gists ;;
        emails) action_emails ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
