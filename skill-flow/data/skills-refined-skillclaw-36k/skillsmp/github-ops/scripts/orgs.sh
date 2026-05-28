#!/usr/bin/env bash
#
# orgs.sh - Organization Operations for GitHub Ops Skill
# MCP Parity: list_org_members, get_org, list_org_teams
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

Organization Operations - GitHub MCP Server Parity

Actions:
  view              View organization info
  members           List organization members
  teams             List organization teams
  team              View a team
  team-members      List team members
  repos             List organization repositories

Common Options:
  --org ORG         Organization name
  --team TEAM       Team slug
  --role ROLE       Filter by role (admin, member, all)
  --type TYPE       Repository type (all, public, private)
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") view --org github
  $(basename "$0") members --org github --limit 10
  $(basename "$0") teams --org microsoft
  $(basename "$0") repos --org facebook --type public
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}"; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --org) ORG="$2"; shift 2 ;;
            --team) TEAM="$2"; shift 2 ;;
            --role) ROLE="$2"; shift 2 ;;
            --type) TYPE="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

action_view() {
    [[ -z "${ORG:-}" ]] && error "Missing --org"
    
    info "Fetching organization: $ORG"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "orgs/$ORG"
    else
        gh api "orgs/$ORG" --jq '{
            login: .login,
            name: .name,
            description: .description,
            location: .location,
            email: .email,
            public_repos: .public_repos,
            followers: .followers,
            created_at: .created_at,
            html_url: .html_url
        }'
    fi
}

action_members() {
    [[ -z "${ORG:-}" ]] && error "Missing --org"
    
    info "Listing members of $ORG"
    
    local url="orgs/$ORG/members?per_page=$LIMIT"
    [[ -n "${ROLE:-}" ]] && url="$url&role=$ROLE"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "$url"
    else
        gh api "$url" --jq '.[].login'
    fi
}

action_teams() {
    [[ -z "${ORG:-}" ]] && error "Missing --org"
    
    info "Listing teams in $ORG"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "orgs/$ORG/teams?per_page=$LIMIT"
    else
        gh api "orgs/$ORG/teams?per_page=$LIMIT" \
            --jq '.[] | "\(.slug)\t\(.name)\t\(.description // "" | .[0:40])"' | column -t -s $'\t'
    fi
}

action_team() {
    [[ -z "${ORG:-}" ]] && error "Missing --org"
    [[ -z "${TEAM:-}" ]] && error "Missing --team"
    
    info "Fetching team: $ORG/$TEAM"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "orgs/$ORG/teams/$TEAM"
    else
        gh api "orgs/$ORG/teams/$TEAM" --jq '{
            slug: .slug,
            name: .name,
            description: .description,
            privacy: .privacy,
            permission: .permission,
            members_count: .members_count,
            repos_count: .repos_count
        }'
    fi
}

action_team_members() {
    [[ -z "${ORG:-}" ]] && error "Missing --org"
    [[ -z "${TEAM:-}" ]] && error "Missing --team"
    
    info "Listing members of team $ORG/$TEAM"
    
    local url="orgs/$ORG/teams/$TEAM/members?per_page=$LIMIT"
    [[ -n "${ROLE:-}" ]] && url="$url&role=$ROLE"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "$url"
    else
        gh api "$url" --jq '.[].login'
    fi
}

action_repos() {
    [[ -z "${ORG:-}" ]] && error "Missing --org"
    
    info "Listing repositories in $ORG"
    
    local type="${TYPE:-all}"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "orgs/$ORG/repos?type=$type&per_page=$LIMIT&sort=updated"
    else
        gh api "orgs/$ORG/repos?type=$type&per_page=$LIMIT&sort=updated" \
            --jq '.[] | "\(.name)\t\(.visibility)\t\(.stargazers_count) stars\t\(.language // "-")"' | column -t -s $'\t'
    fi
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        view) action_view ;;
        members) action_members ;;
        teams) action_teams ;;
        team) action_team ;;
        team-members) action_team_members ;;
        repos) action_repos ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
