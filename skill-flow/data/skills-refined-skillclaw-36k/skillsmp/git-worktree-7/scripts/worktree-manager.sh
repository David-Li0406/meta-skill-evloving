#!/usr/bin/env bash
set -euo pipefail

# Git Worktree Manager
# Manages worktrees with automatic .env copying and cleanup

WORKTREE_DIR=".worktrees"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}→${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}!${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1" >&2; }

# Find git root
git_root() {
    git rev-parse --show-toplevel 2>/dev/null || {
        log_error "Not in a git repository"
        exit 1
    }
}

# Ensure .worktrees is in .gitignore
ensure_gitignore() {
    local root
    root=$(git_root)
    local gitignore="$root/.gitignore"

    if [[ ! -f "$gitignore" ]] || ! grep -q "^\.worktrees/?$" "$gitignore" 2>/dev/null; then
        echo ".worktrees/" >> "$gitignore"
        log_info "Added .worktrees/ to .gitignore"
    fi
}

# Copy .env files to worktree
copy_env_files() {
    local target_dir="$1"
    local root
    root=$(git_root)
    local copied=0

    for env_file in "$root"/.env*; do
        [[ -e "$env_file" ]] || continue
        local filename
        filename=$(basename "$env_file")

        # Skip .env.example
        [[ "$filename" == ".env.example" ]] && continue

        local target="$target_dir/$filename"
        if [[ -f "$target" ]]; then
            log_warn "$filename already exists in worktree, skipping"
        else
            cp "$env_file" "$target"
            ((copied++))
        fi
    done

    if [[ $copied -gt 0 ]]; then
        log_success "Copied $copied .env file(s)"
    fi
}

# Create a new worktree
cmd_create() {
    local branch="${1:-}"
    local base_branch="main"

    # Parse arguments
    shift || true
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --from)
                base_branch="${2:-main}"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [[ -z "$branch" ]]; then
        log_error "Usage: worktree-manager.sh create <branch> [--from <base>]"
        exit 1
    fi

    local root
    root=$(git_root)
    local worktree_path="$root/$WORKTREE_DIR/$branch"

    if [[ -d "$worktree_path" ]]; then
        log_error "Worktree already exists: $worktree_path"
        exit 1
    fi

    ensure_gitignore

    # Check if branch exists
    if git show-ref --verify --quiet "refs/heads/$branch" 2>/dev/null; then
        log_info "Using existing branch: $branch"
        git worktree add "$worktree_path" "$branch"
    else
        log_info "Creating new branch: $branch from $base_branch"
        git worktree add -b "$branch" "$worktree_path" "$base_branch"
    fi

    copy_env_files "$worktree_path"

    log_success "Created worktree at: $worktree_path"
    echo "$worktree_path"
}

# List all worktrees
cmd_list() {
    local root
    root=$(git_root)

    echo ""
    log_info "Worktrees:"
    echo ""

    git worktree list --porcelain | while read -r line; do
        if [[ "$line" == worktree\ * ]]; then
            local path="${line#worktree }"
            local branch=""
            local is_main=false

            # Read next lines for branch info
            while read -r detail; do
                [[ -z "$detail" ]] && break
                if [[ "$detail" == branch\ * ]]; then
                    branch="${detail#branch refs/heads/}"
                fi
            done

            if [[ "$path" == "$root" ]]; then
                is_main=true
            fi

            if $is_main; then
                echo -e "  ${GREEN}●${NC} $branch ${BLUE}(main checkout)${NC}"
                echo -e "    $path"
            else
                echo -e "  ${YELLOW}○${NC} $branch"
                echo -e "    $path"
            fi
            echo ""
        fi
    done
}

# Switch to a worktree (output path)
cmd_switch() {
    local branch="${1:-}"

    if [[ -z "$branch" ]]; then
        log_error "Usage: worktree-manager.sh switch <branch>"
        exit 1
    fi

    local root
    root=$(git_root)
    local worktree_path="$root/$WORKTREE_DIR/$branch"

    if [[ ! -d "$worktree_path" ]]; then
        log_error "Worktree not found: $branch"
        log_info "Available worktrees:"
        cmd_list
        exit 1
    fi

    echo "$worktree_path"
}

# Copy env files to existing worktree
cmd_copy_env() {
    local branch="${1:-}"

    if [[ -z "$branch" ]]; then
        log_error "Usage: worktree-manager.sh copy-env <branch>"
        exit 1
    fi

    local root
    root=$(git_root)
    local worktree_path="$root/$WORKTREE_DIR/$branch"

    if [[ ! -d "$worktree_path" ]]; then
        log_error "Worktree not found: $branch"
        exit 1
    fi

    copy_env_files "$worktree_path"
}

# Cleanup worktrees
cmd_cleanup() {
    local target="${1:-}"
    local root
    root=$(git_root)
    local current_dir
    current_dir=$(pwd)

    if [[ "$target" == "--all" ]]; then
        log_warn "This will remove ALL worktrees in $WORKTREE_DIR/"
        read -r -p "Are you sure? [y/N] " confirm
        [[ "$confirm" =~ ^[Yy]$ ]] || exit 0

        for dir in "$root/$WORKTREE_DIR"/*; do
            [[ -d "$dir" ]] || continue
            local name
            name=$(basename "$dir")

            if [[ "$current_dir" == "$dir"* ]]; then
                log_warn "Skipping $name (currently in this worktree)"
                continue
            fi

            git worktree remove "$dir" --force 2>/dev/null || true
            log_success "Removed: $name"
        done
        return
    fi

    if [[ -z "$target" ]]; then
        log_error "Usage: worktree-manager.sh cleanup <branch> or --all"
        exit 1
    fi

    local worktree_path="$root/$WORKTREE_DIR/$target"

    if [[ ! -d "$worktree_path" ]]; then
        log_error "Worktree not found: $target"
        exit 1
    fi

    if [[ "$current_dir" == "$worktree_path"* ]]; then
        log_error "Cannot remove worktree you're currently in"
        log_info "cd to main checkout first"
        exit 1
    fi

    read -r -p "Remove worktree '$target'? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 0

    git worktree remove "$worktree_path" --force
    log_success "Removed worktree: $target"
}

# Help
cmd_help() {
    cat <<EOF
Git Worktree Manager

Usage: worktree-manager.sh <command> [options]

Commands:
  create <branch> [--from <base>]   Create new worktree (default base: main)
  list, ls                          List all worktrees
  switch, go <branch>               Output worktree path (use with cd)
  copy-env <branch>                 Copy .env files to existing worktree
  cleanup, clean <branch>           Remove a worktree
  cleanup --all                     Remove all worktrees
  help                              Show this help

Examples:
  worktree-manager.sh create feature-x
  worktree-manager.sh create hotfix --from release
  cd \$(worktree-manager.sh go feature-x)
  worktree-manager.sh cleanup feature-x
EOF
}

# Main
main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        create)
            cmd_create "$@"
            ;;
        list|ls)
            cmd_list
            ;;
        switch|go)
            cmd_switch "$@"
            ;;
        copy-env|env)
            cmd_copy_env "$@"
            ;;
        cleanup|clean)
            cmd_cleanup "$@"
            ;;
        help|--help|-h)
            cmd_help
            ;;
        *)
            log_error "Unknown command: $cmd"
            cmd_help
            exit 1
            ;;
    esac
}

main "$@"
