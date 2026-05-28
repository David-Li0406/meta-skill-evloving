#!/bin/bash
#
# Sync reference repositories for Dify plugin development
#
# This script:
#   1. Clones or pulls the three key reference repositories
#   2. Parses docker-compose.yaml to extract service versions
#   3. Switches each repo to the corresponding git tag
#
# Usage:
#   ./sync_repos.sh                    # Sync all repos with auto-detected versions
#   ./sync_repos.sh --pull-only        # Only pull latest, don't switch tags
#   ./sync_repos.sh --show-versions    # Show current docker-compose versions
#
# Configuration:
#   Set DIFY_REPOS_BASE to customize the base directory (default: ~/playground/dify-repo)
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
header() { echo -e "\n${BLUE}=== $1 ===${NC}\n"; }

# Configuration - can be overridden by environment variables
DIFY_REPOS_BASE="${DIFY_REPOS_BASE:-$HOME/playground/dify-repo}"

# Repository definitions
declare -A REPOS=(
    ["dify"]="https://github.com/langgenius/dify.git"
    ["dify-plugin-daemon"]="https://github.com/langgenius/dify-plugin-daemon.git"
    ["dify-official-plugins"]="https://github.com/langgenius/dify-official-plugins.git"
)

# Check if command exists
has_command() {
    command -v "$1" &> /dev/null
}

# Ensure base directory exists
ensure_base_dir() {
    if [[ ! -d "$DIFY_REPOS_BASE" ]]; then
        info "Creating base directory: $DIFY_REPOS_BASE"
        mkdir -p "$DIFY_REPOS_BASE"
    fi
}

# Clone or pull a repository
sync_repo() {
    local name="$1"
    local url="${REPOS[$name]}"
    local path="$DIFY_REPOS_BASE/$name"

    if [[ -z "$url" ]]; then
        error "Unknown repository: $name"
    fi

    if [[ -d "$path/.git" ]]; then
        info "Pulling latest for $name..."
        cd "$path"

        # Stash any local changes
        if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
            warn "Stashing local changes in $name"
            git stash push -m "auto-stash by sync_repos.sh"
        fi

        # Fetch all tags and branches
        git fetch --all --tags --prune

        # Get current branch
        local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "HEAD")

        # If on main/master, pull latest
        if [[ "$current_branch" == "main" || "$current_branch" == "master" ]]; then
            git pull origin "$current_branch" --rebase || warn "Failed to pull $name"
        fi
    else
        info "Cloning $name..."
        git clone "$url" "$path"
    fi

    info "✓ $name synced"
}

# Get docker-compose file path
get_compose_file() {
    local compose_file="$DIFY_REPOS_BASE/dify/docker/docker-compose.yaml"

    if [[ ! -f "$compose_file" ]]; then
        compose_file="$DIFY_REPOS_BASE/dify/docker-compose.yaml"
    fi

    echo "$compose_file"
}

# Parse docker-compose.yaml to extract image versions
# Returns version for a given image pattern (strips suffixes like -local)
get_compose_version() {
    local compose_file=$(get_compose_file)
    local image_pattern="$1"

    if [[ ! -f "$compose_file" ]]; then
        warn "docker-compose.yaml not found"
        return 1
    fi

    # Extract version from image tag (e.g., langgenius/dify-api:0.8.0 -> 0.8.0)
    # Also handles versions with suffixes like 0.5.2-local -> 0.5.2
    grep -E "image:.*$image_pattern:" "$compose_file" 2>/dev/null | \
        head -1 | \
        sed -E 's/.*:([0-9]+\.[0-9]+\.[0-9]+).*/\1/' || echo ""
}

# Show all versions from docker-compose
show_versions() {
    local compose_file="$DIFY_REPOS_BASE/dify/docker/docker-compose.yaml"

    if [[ ! -f "$compose_file" ]]; then
        compose_file="$DIFY_REPOS_BASE/dify/docker-compose.yaml"
    fi

    if [[ ! -f "$compose_file" ]]; then
        error "docker-compose.yaml not found. Please sync the dify repo first."
    fi

    header "Docker Compose Image Versions"

    # Extract all image lines with versions
    grep -E "^\s+image:" "$compose_file" | while read -r line; do
        echo "  $line"
    done

    echo
    info "Compose file: $compose_file"
}

# Switch repository to a specific tag
switch_to_tag() {
    local name="$1"
    local tag="$2"
    local path="$DIFY_REPOS_BASE/$name"

    if [[ -z "$tag" ]]; then
        warn "No tag specified for $name, staying on current branch"
        return 0
    fi

    if [[ ! -d "$path/.git" ]]; then
        error "Repository $name not found at $path"
    fi

    cd "$path"

    # Check if tag exists
    if git rev-parse "refs/tags/$tag" &>/dev/null; then
        info "Switching $name to tag: $tag"
        git checkout "tags/$tag" -q
        info "✓ $name now at $tag"
    elif git rev-parse "refs/tags/v$tag" &>/dev/null; then
        # Try with 'v' prefix
        info "Switching $name to tag: v$tag"
        git checkout "tags/v$tag" -q
        info "✓ $name now at v$tag"
    else
        warn "Tag $tag not found in $name, available tags:"
        git tag --sort=-v:refname | head -10
    fi
}

# Detect and switch to matching versions
auto_switch_versions() {
    header "Auto-detecting versions from docker-compose"

    # Get dify version from dify-api image
    local dify_version=$(get_compose_version "dify-api")
    # Get plugin-daemon version from its own image
    local daemon_version=$(get_compose_version "dify-plugin-daemon")

    # Switch dify repo
    if [[ -n "$dify_version" ]]; then
        info "Detected dify-api version: $dify_version"
        switch_to_tag "dify" "$dify_version"
    else
        warn "Could not detect dify version"
    fi

    # Switch dify-plugin-daemon repo
    if [[ -n "$daemon_version" ]]; then
        info "Detected dify-plugin-daemon version: $daemon_version"
        switch_to_tag "dify-plugin-daemon" "$daemon_version"
    else
        warn "Could not detect dify-plugin-daemon version"
    fi

    # dify-official-plugins typically follows dify main version or stays on main
    # Try dify version first, then stay on main if not found
    if [[ -n "$dify_version" ]]; then
        switch_to_tag "dify-official-plugins" "$dify_version"
    else
        info "dify-official-plugins will stay on main branch"
    fi
}

# Main function
main() {
    local pull_only=false
    local show_versions_only=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --pull-only)
                pull_only=true
                shift
                ;;
            --show-versions)
                show_versions_only=true
                shift
                ;;
            --base)
                DIFY_REPOS_BASE="$2"
                shift 2
                ;;
            --help|-h)
                echo "Usage: $0 [options]"
                echo
                echo "Options:"
                echo "  --pull-only       Only pull latest, don't switch tags"
                echo "  --show-versions   Show docker-compose image versions"
                echo "  --base <path>     Set base directory for repos"
                echo "  --help            Show this help"
                echo
                echo "Environment:"
                echo "  DIFY_REPOS_BASE   Base directory (default: ~/playground/dify-repo)"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    # Check dependencies
    if ! has_command git; then
        error "git is required but not installed"
    fi

    echo "========================================"
    echo "Dify Reference Repository Sync"
    echo "========================================"
    echo
    info "Base directory: $DIFY_REPOS_BASE"

    # Show versions only
    if [[ "$show_versions_only" == true ]]; then
        show_versions
        exit 0
    fi

    # Ensure base directory exists
    ensure_base_dir

    # Sync all repositories
    header "Syncing Repositories"
    for repo in "${!REPOS[@]}"; do
        sync_repo "$repo"
    done

    # Switch to matching versions unless --pull-only
    if [[ "$pull_only" == false ]]; then
        auto_switch_versions
    fi

    header "Summary"
    for repo in "${!REPOS[@]}"; do
        local path="$DIFY_REPOS_BASE/$repo"
        if [[ -d "$path/.git" ]]; then
            cd "$path"
            local ref=$(git describe --tags --exact-match 2>/dev/null || git rev-parse --abbrev-ref HEAD)
            echo "  $repo: $ref"
        fi
    done

    echo
    info "Sync complete!"
}

main "$@"
