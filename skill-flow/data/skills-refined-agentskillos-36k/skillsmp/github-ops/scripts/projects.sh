#!/usr/bin/env bash
#
# projects.sh - GitHub Projects V2 Operations for GitHub Ops Skill
# MCP Parity: list_projects, get_project, get_project_items, get_project_fields
#
# Note: Projects V2 uses GraphQL API exclusively
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

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

GitHub Projects V2 Operations - GitHub MCP Server Parity

Actions:
  list              List projects (user or org)
  view              View a project
  items             List project items
  fields            List project fields
  add-item          Add an item to a project

Common Options:
  --owner OWNER     User or organization name
  --number NUMBER   Project number
  --project-id ID   Project node ID (for mutations)
  --issue URL       Issue/PR URL to add (for add-item)
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") list --owner octocat
  $(basename "$0") view --owner octocat --number 1
  $(basename "$0") items --owner octocat --number 1 --limit 20
  $(basename "$0") fields --owner octocat --number 1
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
            --owner) OWNER="$2"; shift 2 ;;
            --number) NUMBER="$2"; shift 2 ;;
            --project-id) PROJECT_ID="$2"; shift 2 ;;
            --issue) ISSUE_URL="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Helper: Determine if owner is user or org
get_owner_type() {
    local owner="$1"
    local result
    result=$(gh api "users/$owner" --jq '.type' 2>/dev/null) || echo "User"
    echo "$result"
}

# Action: List projects
action_list() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    
    info "Listing projects for $OWNER"
    
    local owner_type
    owner_type=$(get_owner_type "$OWNER")
    
    local query
    if [[ "$owner_type" == "Organization" ]]; then
        query=$(cat << EOF
query {
  organization(login: "$OWNER") {
    projectsV2(first: $LIMIT) {
      nodes {
        id
        number
        title
        shortDescription
        public
        closed
        url
        items { totalCount }
        updatedAt
      }
    }
  }
}
EOF
)
        local jq_path='.data.organization.projectsV2.nodes'
    else
        query=$(cat << EOF
query {
  user(login: "$OWNER") {
    projectsV2(first: $LIMIT) {
      nodes {
        id
        number
        title
        shortDescription
        public
        closed
        url
        items { totalCount }
        updatedAt
      }
    }
  }
}
EOF
)
        local jq_path='.data.user.projectsV2.nodes'
    fi
    
    local result
    result=$(gh api graphql -f query="$query" 2>&1) || {
        warn "Could not fetch projects. User may not have any projects."
        return 1
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq "$jq_path"
    else
        echo "$result" | jq -r "${jq_path}[] | 
            \"#\(.number)\t\(.title | .[0:40])\t\(.public | if . then \"public\" else \"private\" end)\t\(.items.totalCount) items\t\(.closed | if . then \"CLOSED\" else \"OPEN\" end)\"" \
            | column -t -s $'\t'
    fi
}

# Action: View a project
action_view() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching project #$NUMBER for $OWNER"
    
    local owner_type
    owner_type=$(get_owner_type "$OWNER")
    
    local owner_field="user"
    [[ "$owner_type" == "Organization" ]] && owner_field="organization"
    
    local query
    query=$(cat << EOF
query {
  ${owner_field}(login: "$OWNER") {
    projectV2(number: $NUMBER) {
      id
      number
      title
      shortDescription
      readme
      public
      closed
      url
      creator { login }
      items { totalCount }
      fields(first: 20) { totalCount }
      createdAt
      updatedAt
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$query" 2>&1) || {
        error "Could not fetch project #$NUMBER"
    }
    
    local jq_path=".data.${owner_field}.projectV2"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq "$jq_path"
    else
        echo "$result" | jq -r "${jq_path} | \"
Title: \(.title)
Number: #\(.number)
ID: \(.id)
Description: \(.shortDescription // \"(none)\")
Public: \(.public)
Status: \(.closed | if . then \"CLOSED\" else \"OPEN\" end)
Creator: @\(.creator.login)
Items: \(.items.totalCount)
Fields: \(.fields.totalCount)
Created: \(.createdAt)
Updated: \(.updatedAt)
URL: \(.url)

--- Readme ---
\(.readme // \"(no readme)\")\""
    fi
}

# Action: List project items
action_items() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching items for project #$NUMBER"
    
    local owner_type
    owner_type=$(get_owner_type "$OWNER")
    
    local owner_field="user"
    [[ "$owner_type" == "Organization" ]] && owner_field="organization"
    
    local query
    query=$(cat << EOF
query {
  ${owner_field}(login: "$OWNER") {
    projectV2(number: $NUMBER) {
      items(first: $LIMIT) {
        nodes {
          id
          type
          content {
            ... on Issue {
              number
              title
              state
              repository { nameWithOwner }
            }
            ... on PullRequest {
              number
              title
              state
              repository { nameWithOwner }
            }
            ... on DraftIssue {
              title
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldTextValue {
                text
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2FieldCommon { name } }
              }
              ... on ProjectV2ItemFieldDateValue {
                date
                field { ... on ProjectV2FieldCommon { name } }
              }
            }
          }
        }
      }
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$query" 2>&1) || {
        error "Could not fetch project items"
    }
    
    local jq_path=".data.${owner_field}.projectV2.items.nodes"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq "$jq_path"
    else
        echo "$result" | jq -r "${jq_path}[] | 
            \"\(.type)\t\(.content.repository.nameWithOwner // \"Draft\")#\(.content.number // \"\")\t\(.content.title)\t\(.content.state // \"DRAFT\")\"" \
            | column -t -s $'\t'
    fi
}

# Action: List project fields
action_fields() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching fields for project #$NUMBER"
    
    local owner_type
    owner_type=$(get_owner_type "$OWNER")
    
    local owner_field="user"
    [[ "$owner_type" == "Organization" ]] && owner_field="organization"
    
    local query
    query=$(cat << EOF
query {
  ${owner_field}(login: "$OWNER") {
    projectV2(number: $NUMBER) {
      fields(first: 50) {
        nodes {
          ... on ProjectV2FieldCommon {
            id
            name
            dataType
          }
          ... on ProjectV2SingleSelectField {
            id
            name
            dataType
            options { id name }
          }
          ... on ProjectV2IterationField {
            id
            name
            dataType
            configuration {
              iterations { id title startDate duration }
            }
          }
        }
      }
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$query" 2>&1) || {
        error "Could not fetch project fields"
    }
    
    local jq_path=".data.${owner_field}.projectV2.fields.nodes"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq "$jq_path"
    else
        echo "$result" | jq -r "${jq_path}[] | select(.name != null) |
            \"\(.name)\t\(.dataType)\t\(.id)\t\((.options // []) | map(.name) | join(\", \") | .[0:40])\"" \
            | column -t -s $'\t'
    fi
}

# Action: Add item to project
action_add_item() {
    [[ -z "${PROJECT_ID:-}" ]] && error "Missing --project-id (use 'view' to get project ID)"
    [[ -z "${ISSUE_URL:-}" ]] && error "Missing --issue (URL to issue or PR)"
    
    info "Adding item to project"
    
    # First, get the node ID of the issue/PR
    # Parse owner/repo/number from URL
    local issue_info
    if [[ "$ISSUE_URL" =~ github.com/([^/]+)/([^/]+)/(issues|pull)/([0-9]+) ]]; then
        local issue_owner="${BASH_REMATCH[1]}"
        local issue_repo="${BASH_REMATCH[2]}"
        local issue_type="${BASH_REMATCH[3]}"
        local issue_number="${BASH_REMATCH[4]}"
    else
        error "Invalid issue/PR URL format"
    fi
    
    local node_query
    if [[ "$issue_type" == "issues" ]]; then
        node_query="query { repository(owner: \"$issue_owner\", name: \"$issue_repo\") { issue(number: $issue_number) { id } } }"
        local node_id
        node_id=$(gh api graphql -f query="$node_query" --jq '.data.repository.issue.id' 2>&1) || {
            error "Could not find issue"
        }
    else
        node_query="query { repository(owner: \"$issue_owner\", name: \"$issue_repo\") { pullRequest(number: $issue_number) { id } } }"
        local node_id
        node_id=$(gh api graphql -f query="$node_query" --jq '.data.repository.pullRequest.id' 2>&1) || {
            error "Could not find pull request"
        }
    fi
    
    # Add to project
    local mutation
    mutation=$(cat << EOF
mutation {
  addProjectV2ItemById(input: {
    projectId: "$PROJECT_ID",
    contentId: "$node_id"
  }) {
    item {
      id
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$mutation" 2>&1) || {
        error "Failed to add item: $result"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result"
    else
        success "Item added to project"
        echo "$result" | jq -r '.data.addProjectV2ItemById.item.id'
    fi
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        list) action_list ;;
        view) action_view ;;
        items) action_items ;;
        fields) action_fields ;;
        add-item) action_add_item ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
