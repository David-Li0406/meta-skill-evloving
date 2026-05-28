#!/usr/bin/env bash
#
# repos.sh - Repository Operations for GitHub Ops Skill
# MCP Parity: get_file_contents, create_or_update_file, push_files, create_repository,
#             fork_repository, create_branch, list_commits, get_commit, get_tree, get_blob,
#             get_reference, create_reference, compare_commits
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
LIMIT=30
JSON_OUTPUT=false
CONFIRM_DESTRUCTIVE=true

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Repository Operations - GitHub MCP Server Parity

Actions:
  view              View repository information
  contents          Get file contents or list directory
  clone             Clone a repository
  fork              Fork a repository
  list              List repositories
  create            Create a new repository
  delete            Delete a repository
  commits           List commits
  commit            Get a specific commit
  branches          List branches
  branch            Create a branch
  tags              List tags
  default-branch    Get default branch
  tree              Get git tree
  blob              Get git blob
  ref               Get git reference
  create-ref        Create git reference
  compare           Compare two commits

Common Options:
  --owner OWNER     Repository owner
  --repo REPO       Repository name
  --path PATH       File or directory path
  --ref REF         Git reference (branch, tag, commit)
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") view --owner facebook --repo react
  $(basename "$0") contents --owner vercel --repo next.js --path package.json
  $(basename "$0") contents --owner vercel --repo next.js --path packages
  $(basename "$0") commits --owner cli --repo cli --limit 10
  $(basename "$0") branches --owner facebook --repo react
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

# Parse common arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --owner) OWNER="$2"; shift 2 ;;
            --repo) REPO="$2"; shift 2 ;;
            --path) FILE_PATH="$2"; shift 2 ;;
            --ref) REF="$2"; shift 2 ;;
            --sha) SHA="$2"; shift 2 ;;
            --branch) BRANCH="$2"; shift 2 ;;
            --base) BASE="$2"; shift 2 ;;
            --head) HEAD="$2"; shift 2 ;;
            --name) NAME="$2"; shift 2 ;;
            --description) DESCRIPTION="$2"; shift 2 ;;
            --dir) DIR="$2"; shift 2 ;;
            --type) TYPE="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --private) PRIVATE=true; shift ;;
            --json) JSON_OUTPUT=true; shift ;;
            --no-confirm) CONFIRM_DESTRUCTIVE=false; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: View repository info
action_view() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Fetching repository: $OWNER/$REPO"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh repo view "$OWNER/$REPO" --json name,description,url,stargazerCount,forkCount,isPrivate,defaultBranchRef,createdAt,updatedAt,primaryLanguage,licenseInfo
    else
        gh repo view "$OWNER/$REPO"
    fi
}

# Action: Get file contents or list directory
action_contents() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    local path="${FILE_PATH:-}"
    local ref_param=""
    [[ -n "${REF:-}" ]] && ref_param="?ref=$REF"
    
    info "Fetching contents: $OWNER/$REPO/${path:-root}"
    
    # First, check if it's a file or directory
    local api_path="repos/$OWNER/$REPO/contents/$path$ref_param"
    local response
    response=$(gh api "$api_path" 2>&1) || error "Failed to fetch contents: $response"
    
    # Check if it's an array (directory) or object (file)
    if echo "$response" | jq -e 'type == "array"' > /dev/null 2>&1; then
        # It's a directory
        if [[ "$JSON_OUTPUT" == "true" ]]; then
            echo "$response"
        else
            echo -e "${GREEN}Directory listing: $path${NC}"
            echo "$response" | jq -r '.[] | "\(.type)\t\(.name)\t\(.size // "-")"' | column -t -s $'\t'
        fi
    else
        # It's a file
        if [[ "$JSON_OUTPUT" == "true" ]]; then
            echo "$response"
        else
            # Get raw content
            gh api "$api_path" -H "Accept: application/vnd.github.raw"
        fi
    fi
}

# Action: Clone repository
action_clone() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    local target="${DIR:-$REPO}"
    
    info "Cloning repository: $OWNER/$REPO to $target"
    gh repo clone "$OWNER/$REPO" "$target"
    success "Repository cloned successfully to $target"
}

# Action: Fork repository
action_fork() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    confirm "This will fork $OWNER/$REPO to your account"
    
    info "Forking repository: $OWNER/$REPO"
    gh repo fork "$OWNER/$REPO" --clone=false
    success "Repository forked successfully"
}

# Action: List repositories
action_list() {
    local type_filter="${TYPE:-owner}"
    
    info "Listing repositories (type: $type_filter, limit: $LIMIT)"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh repo list --limit "$LIMIT" --json name,description,isPrivate,updatedAt,url
    else
        gh repo list --limit "$LIMIT"
    fi
}

# Action: Create repository
action_create() {
    [[ -z "${NAME:-}" ]] && error "Missing --name"
    
    confirm "This will create a new repository: $NAME"
    
    local visibility="--public"
    [[ "${PRIVATE:-false}" == "true" ]] && visibility="--private"
    
    local desc_flag=""
    [[ -n "${DESCRIPTION:-}" ]] && desc_flag="--description \"$DESCRIPTION\""
    
    info "Creating repository: $NAME"
    eval gh repo create "$NAME" "$visibility" $desc_flag
    success "Repository created successfully"
}

# Action: Delete repository
action_delete() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    confirm "This will PERMANENTLY DELETE $OWNER/$REPO. This cannot be undone!"
    
    info "Deleting repository: $OWNER/$REPO"
    gh repo delete "$OWNER/$REPO" --yes
    success "Repository deleted"
}

# Action: List commits
action_commits() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing commits for $OWNER/$REPO (limit: $LIMIT)"
    
    local ref_param=""
    [[ -n "${REF:-}" ]] && ref_param="--ref $REF"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/commits?per_page=$LIMIT" --jq '.[] | {sha: .sha, message: .commit.message, author: .commit.author.name, date: .commit.author.date}'
    else
        gh api "repos/$OWNER/$REPO/commits?per_page=$LIMIT" --jq '.[] | "\(.sha[0:7]) \(.commit.author.date[0:10]) \(.commit.author.name): \(.commit.message | split("\n")[0])"'
    fi
}

# Action: Get specific commit
action_commit() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${SHA:-}" ]] && error "Missing --sha"
    
    info "Fetching commit: $SHA"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/commits/$SHA"
    else
        gh api "repos/$OWNER/$REPO/commits/$SHA" --jq '{sha: .sha, message: .commit.message, author: .commit.author.name, date: .commit.author.date, files: [.files[].filename]}'
    fi
}

# Action: List branches
action_branches() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing branches for $OWNER/$REPO"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/branches?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/branches?per_page=$LIMIT" --jq '.[].name'
    fi
}

# Action: Create branch
action_branch() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${BRANCH:-}" ]] && error "Missing --branch"
    
    # Get SHA to branch from
    local from_sha="${SHA:-}"
    if [[ -z "$from_sha" ]]; then
        # Get default branch SHA
        from_sha=$(gh api "repos/$OWNER/$REPO" --jq '.default_branch' | xargs -I {} gh api "repos/$OWNER/$REPO/git/ref/heads/{}" --jq '.object.sha')
    fi
    
    confirm "This will create branch '$BRANCH' from $from_sha"
    
    info "Creating branch: $BRANCH"
    gh api "repos/$OWNER/$REPO/git/refs" -f ref="refs/heads/$BRANCH" -f sha="$from_sha"
    success "Branch created: $BRANCH"
}

# Action: List tags
action_tags() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing tags for $OWNER/$REPO"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/tags?per_page=$LIMIT"
    else
        gh api "repos/$OWNER/$REPO/tags?per_page=$LIMIT" --jq '.[].name'
    fi
}

# Action: Get default branch
action_default_branch() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    gh api "repos/$OWNER/$REPO" --jq '.default_branch'
}

# Action: Get git tree
action_tree() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${SHA:-}" ]] && error "Missing --sha (tree SHA)"
    
    info "Fetching tree: $SHA"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/git/trees/$SHA"
    else
        gh api "repos/$OWNER/$REPO/git/trees/$SHA" --jq '.tree[] | "\(.mode) \(.type) \(.sha[0:7]) \(.path)"'
    fi
}

# Action: Get git blob
action_blob() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${SHA:-}" ]] && error "Missing --sha (blob SHA)"
    
    info "Fetching blob: $SHA"
    
    # Get blob and decode content
    gh api "repos/$OWNER/$REPO/git/blobs/$SHA" --jq '.content' | base64 -d
}

# Action: Get git reference
action_ref() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${REF:-}" ]] && error "Missing --ref"
    
    info "Fetching ref: $REF"
    
    gh api "repos/$OWNER/$REPO/git/ref/$REF"
}

# Action: Create git reference
action_create_ref() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${REF:-}" ]] && error "Missing --ref"
    [[ -z "${SHA:-}" ]] && error "Missing --sha"
    
    confirm "This will create ref '$REF' pointing to $SHA"
    
    info "Creating ref: $REF"
    gh api "repos/$OWNER/$REPO/git/refs" -f ref="refs/$REF" -f sha="$SHA"
    success "Reference created: $REF"
}

# Action: Compare commits
action_compare() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${BASE:-}" ]] && error "Missing --base"
    [[ -z "${HEAD:-}" ]] && error "Missing --head"
    
    info "Comparing $BASE...$HEAD"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/compare/$BASE...$HEAD"
    else
        gh api "repos/$OWNER/$REPO/compare/$BASE...$HEAD" --jq '{
            status: .status,
            ahead_by: .ahead_by,
            behind_by: .behind_by,
            total_commits: .total_commits,
            files_changed: (.files | length),
            commits: [.commits[] | {sha: .sha[0:7], message: .commit.message | split("\n")[0]}]
        }'
    fi
}

# Main entry point
main() {
    [[ $# -eq 0 ]] && usage
    
    local action="$1"
    shift
    
    parse_args "$@"
    
    case "$action" in
        view) action_view ;;
        contents) action_contents ;;
        clone) action_clone ;;
        fork) action_fork ;;
        list) action_list ;;
        create) action_create ;;
        delete) action_delete ;;
        commits) action_commits ;;
        commit) action_commit ;;
        branches) action_branches ;;
        branch) action_branch ;;
        tags) action_tags ;;
        default-branch) action_default_branch ;;
        tree) action_tree ;;
        blob) action_blob ;;
        ref) action_ref ;;
        create-ref) action_create_ref ;;
        compare) action_compare ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action. Use --help for usage." ;;
    esac
}

main "$@"
