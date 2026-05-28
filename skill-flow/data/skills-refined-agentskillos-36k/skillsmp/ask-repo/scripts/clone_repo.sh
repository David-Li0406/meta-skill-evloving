#!/bin/bash
# Clone a GitHub repo to /tmp/ask-repo/ for analysis
# Usage: clone_repo.sh <github-url>

set -e

CACHE_DIR="/tmp/ask-repo"
MAX_AGE_HOURS=24

# Clean up old clones
cleanup_old() {
    if [ -d "$CACHE_DIR" ]; then
        find "$CACHE_DIR" -maxdepth 1 -type d -mmin +$((MAX_AGE_HOURS * 60)) -exec rm -rf {} \; 2>/dev/null || true
    fi
}

# Parse GitHub URL to get owner and repo
parse_url() {
    local url="$1"

    # Handle various GitHub URL formats:
    # https://github.com/owner/repo
    # https://github.com/owner/repo.git
    # git@github.com:owner/repo.git
    # owner/repo

    if [[ "$url" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
        echo "${BASH_REMATCH[1]}-${BASH_REMATCH[2]}"
    elif [[ "$url" =~ ^([^/]+)/([^/]+)$ ]]; then
        # Simple owner/repo format
        echo "$1" | tr '/' '-'
    else
        echo "error"
    fi
}

# Normalize URL for git clone
normalize_url() {
    local url="$1"

    # If it's already a full URL, use it
    if [[ "$url" =~ ^https?:// ]] || [[ "$url" =~ ^git@ ]]; then
        # Remove trailing .git if present, then add it back for consistency
        echo "${url%.git}.git"
    elif [[ "$url" =~ ^([^/]+)/([^/]+)$ ]]; then
        # Convert owner/repo to full HTTPS URL
        echo "https://github.com/$url.git"
    else
        echo ""
    fi
}

main() {
    if [ -z "$1" ]; then
        echo "Usage: clone_repo.sh <github-url>"
        echo ""
        echo "Examples:"
        echo "  clone_repo.sh https://github.com/anthropics/claude-code"
        echo "  clone_repo.sh anthropics/claude-code"
        exit 1
    fi

    local url="$1"
    local repo_name=$(parse_url "$url")
    local git_url=$(normalize_url "$url")

    if [ "$repo_name" = "error" ] || [ -z "$git_url" ]; then
        echo "Error: Could not parse GitHub URL: $url"
        exit 1
    fi

    local target_dir="$CACHE_DIR/$repo_name"

    # Create cache directory
    mkdir -p "$CACHE_DIR"

    # Clean up old repos
    cleanup_old

    # Check if already cloned
    if [ -d "$target_dir/.git" ]; then
        echo "Already cloned: $target_dir"
        echo "$target_dir"
        exit 0
    fi

    # Clone with depth 1 for speed
    echo "Cloning $git_url to $target_dir..."
    if git clone --depth 1 "$git_url" "$target_dir" 2>&1; then
        echo ""
        echo "Cloned successfully: $target_dir"
        echo "$target_dir"
    else
        echo "Error: Failed to clone $git_url"
        echo "If this is a private repo, ensure you have SSH keys or a token configured."
        exit 1
    fi
}

main "$@"
