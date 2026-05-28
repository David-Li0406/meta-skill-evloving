#!/usr/bin/env bash
#
# discussions.sh - Discussion Operations for GitHub Ops Skill
# MCP Parity: list_discussions, get_discussion, get_discussion_comments, get_discussion_categories
#
# Note: Discussions use GraphQL API exclusively
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

Discussion Operations - GitHub MCP Server Parity

Actions:
  list              List discussions in a repository
  view              View a specific discussion
  comments          List comments on a discussion
  categories        List discussion categories
  create            Create a new discussion

Common Options:
  --owner OWNER     Repository owner (required)
  --repo REPO       Repository name (required)
  --number NUMBER   Discussion number (for view/comments)
  --category CAT    Category slug (for list/create)
  --title TITLE     Discussion title (for create)
  --body BODY       Discussion body (for create)
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") list --owner vercel --repo next.js --limit 10
  $(basename "$0") view --owner vercel --repo next.js --number 12345
  $(basename "$0") categories --owner vercel --repo next.js
  $(basename "$0") comments --owner vercel --repo next.js --number 12345
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
            --repo) REPO="$2"; shift 2 ;;
            --number) NUMBER="$2"; shift 2 ;;
            --category) CATEGORY="$2"; shift 2 ;;
            --title) TITLE="$2"; shift 2 ;;
            --body) BODY="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: List discussions
action_list() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing discussions in $OWNER/$REPO"
    
    local category_filter=""
    if [[ -n "${CATEGORY:-}" ]]; then
        category_filter=", categoryId: \"$CATEGORY\""
    fi
    
    local query
    query=$(cat << EOF
query {
  repository(owner: "$OWNER", name: "$REPO") {
    discussions(first: $LIMIT, orderBy: {field: CREATED_AT, direction: DESC}$category_filter) {
      nodes {
        number
        title
        author { login }
        category { name slug }
        createdAt
        updatedAt
        answerChosenAt
        comments { totalCount }
        upvoteCount
        url
      }
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$query" 2>&1) || {
        warn "Could not fetch discussions. Discussions may not be enabled."
        return 1
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq '.data.repository.discussions.nodes'
    else
        echo "$result" | jq -r '.data.repository.discussions.nodes[] | 
            "#\(.number)\t\(.title | .[0:50])\t\(.category.name)\t@\(.author.login)\t\(.comments.totalCount) comments"' \
            | column -t -s $'\t'
    fi
}

# Action: View a discussion
action_view() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching discussion #$NUMBER in $OWNER/$REPO"
    
    local query
    query=$(cat << EOF
query {
  repository(owner: "$OWNER", name: "$REPO") {
    discussion(number: $NUMBER) {
      number
      title
      body
      author { login }
      category { name slug }
      createdAt
      updatedAt
      answerChosenAt
      upvoteCount
      url
      comments { totalCount }
      labels(first: 10) { nodes { name } }
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$query" 2>&1) || {
        error "Could not fetch discussion #$NUMBER"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq '.data.repository.discussion'
    else
        local disc
        disc=$(echo "$result" | jq '.data.repository.discussion')
        echo "$disc" | jq -r '"
Title: \(.title)
Number: #\(.number)
Category: \(.category.name)
Author: @\(.author.login)
Created: \(.createdAt)
Upvotes: \(.upvoteCount)
Comments: \(.comments.totalCount)
URL: \(.url)
Labels: \((.labels.nodes | map(.name) | join(", ")) // "none")
Answered: \(.answerChosenAt // "no")

--- Body ---
\(.body)"'
    fi
}

# Action: List comments on a discussion
action_comments() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching comments for discussion #$NUMBER"
    
    local query
    query=$(cat << EOF
query {
  repository(owner: "$OWNER", name: "$REPO") {
    discussion(number: $NUMBER) {
      comments(first: $LIMIT) {
        nodes {
          author { login }
          body
          createdAt
          isAnswer
          upvoteCount
          replies(first: 5) {
            nodes {
              author { login }
              body
              createdAt
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
        error "Could not fetch comments for discussion #$NUMBER"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq '.data.repository.discussion.comments.nodes'
    else
        echo "$result" | jq -r '.data.repository.discussion.comments.nodes[] | 
            "\n@\(.author.login) • \(.createdAt)\(.isAnswer | if . then " ✓ ANSWER" else "" end)\n\(.body)\n---"'
    fi
}

# Action: List discussion categories
action_categories() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Fetching discussion categories for $OWNER/$REPO"
    
    local query
    query=$(cat << EOF
query {
  repository(owner: "$OWNER", name: "$REPO") {
    discussionCategories(first: 25) {
      nodes {
        id
        name
        slug
        description
        emoji
        emojiHTML
        isAnswerable
      }
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$query" 2>&1) || {
        warn "Could not fetch discussion categories. Discussions may not be enabled."
        return 1
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq '.data.repository.discussionCategories.nodes'
    else
        echo "$result" | jq -r '.data.repository.discussionCategories.nodes[] | 
            "\(.emoji // "•") \(.name)\t\(.slug)\t\(.isAnswerable | if . then "Q&A" else "" end)\t\(.description // "")"' \
            | column -t -s $'\t'
    fi
}

# Action: Create a discussion
action_create() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${TITLE:-}" ]] && error "Missing --title"
    [[ -z "${BODY:-}" ]] && error "Missing --body"
    [[ -z "${CATEGORY:-}" ]] && error "Missing --category (use categories action to find slug)"
    
    info "Creating discussion in $OWNER/$REPO"
    
    # First, get the repository ID and category ID
    local repo_query
    repo_query=$(cat << EOF
query {
  repository(owner: "$OWNER", name: "$REPO") {
    id
    discussionCategories(first: 25) {
      nodes {
        id
        slug
      }
    }
  }
}
EOF
)
    
    local repo_info
    repo_info=$(gh api graphql -f query="$repo_query" 2>&1) || {
        error "Could not fetch repository information"
    }
    
    local repo_id category_id
    repo_id=$(echo "$repo_info" | jq -r '.data.repository.id')
    category_id=$(echo "$repo_info" | jq -r --arg cat "$CATEGORY" \
        '.data.repository.discussionCategories.nodes[] | select(.slug == $cat) | .id')
    
    if [[ -z "$category_id" ]]; then
        error "Category '$CATEGORY' not found. Use 'categories' action to list available categories."
    fi
    
    # Escape the body for JSON
    local escaped_body escaped_title
    escaped_body=$(echo "$BODY" | jq -sR .)
    escaped_title=$(echo "$TITLE" | jq -sR .)
    
    local mutation
    mutation=$(cat << EOF
mutation {
  createDiscussion(input: {
    repositoryId: "$repo_id",
    categoryId: "$category_id",
    title: $escaped_title,
    body: $escaped_body
  }) {
    discussion {
      number
      url
      title
    }
  }
}
EOF
)
    
    local result
    result=$(gh api graphql -f query="$mutation" 2>&1) || {
        error "Failed to create discussion: $result"
    }
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo "$result" | jq '.data.createDiscussion.discussion'
    else
        local disc
        disc=$(echo "$result" | jq '.data.createDiscussion.discussion')
        success "Discussion created successfully!"
        echo "$disc" | jq -r '"#\(.number): \(.title)\n\(.url)"'
    fi
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        list) action_list ;;
        view) action_view ;;
        comments) action_comments ;;
        categories) action_categories ;;
        create) action_create ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
