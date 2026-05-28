#!/usr/bin/env bash
# Create alpha-forge worktree with ADR-style naming
# ADR: /docs/adr/2025-12-14-alpha-forge-worktree-management.md
#
# Modes:
#   new    - Create new branch + worktree (atomic)
#   remote - Track remote branch in worktree
#   local  - Use existing local branch
#
# Usage:
#   New:    create-worktree.sh --mode new --slug <slug> --type <type> --base <base>
#   Remote: create-worktree.sh --mode remote --branch <remote-branch>
#   Local:  create-worktree.sh --mode local --branch <branch>
#
# Examples:
#   create-worktree.sh --mode new --slug sharpe-statistical-validation --type feat --base main
#   create-worktree.sh --mode remote --branch origin/feat/2025-12-10-existing
#   create-worktree.sh --mode local --branch feat/2025-12-15-my-feature

set -euo pipefail

# Dynamic worktree detection (ADR: 2025-12-29-ralph-constraint-scanning.md)
# Uses git rev-parse --git-common-dir instead of hardcoded path
detect_alpha_forge_root() {
    local git_common_dir
    git_common_dir=$(git rev-parse --git-common-dir 2>/dev/null || echo "")

    if [[ -z "$git_common_dir" ]]; then
        echo ""
        return
    fi

    if [[ "$git_common_dir" == ".git" ]]; then
        # Main worktree - we're in the repo root
        pwd
    else
        # Linked worktree - git-common-dir points to main's .git
        dirname "$git_common_dir"
    fi
}

# Defaults
MODE=""
SLUG=""
TYPE=""
BASE=""
BRANCH=""
AF_ROOT="${AF_ROOT:-$(detect_alpha_forge_root)}"
WORKTREE_BASE="${WORKTREE_BASE:-$HOME/eon}"

# Fallback to legacy path if detection fails
if [[ -z "$AF_ROOT" ]]; then
    AF_ROOT="$HOME/eon/alpha-forge"
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --slug)
            SLUG="$2"
            shift 2
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --base)
            BASE="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        *)
            # Legacy support: first positional arg is branch (local mode)
            if [[ -z "$BRANCH" ]]; then
                BRANCH="$1"
                MODE="${MODE:-local}"
            fi
            shift
            ;;
    esac
done

# Validate mode
if [[ -z "$MODE" ]]; then
    echo "Error: --mode required (new|remote|local)" >&2
    echo "" >&2
    echo "Usage:" >&2
    echo "  New:    create-worktree.sh --mode new --slug <slug> --type <type> --base <base>" >&2
    echo "  Remote: create-worktree.sh --mode remote --branch <remote-branch>" >&2
    echo "  Local:  create-worktree.sh --mode local --branch <branch>" >&2
    exit 1
fi

# Validate alpha-forge repo exists
if [[ ! -d "$AF_ROOT/.git" ]]; then
    echo "Error: alpha-forge repo not found at $AF_ROOT" >&2
    exit 1
fi

cd "$AF_ROOT"

# Mode-specific validation and execution
case "$MODE" in
    new)
        # Mode 1: New branch from description (atomic creation)
        if [[ -z "$SLUG" || -z "$TYPE" || -z "$BASE" ]]; then
            echo "Error: --mode new requires --slug, --type, and --base" >&2
            exit 1
        fi

        DATE=$(date +%Y-%m-%d)
        BRANCH="${TYPE}/${DATE}-${SLUG}"
        WORKTREE_NAME="alpha-forge.worktree-${DATE}-${SLUG}"
        WORKTREE_PATH="${WORKTREE_BASE}/${WORKTREE_NAME}"

        # Check if branch already exists
        if git show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
            echo "Error: Branch '$BRANCH' already exists" >&2
            echo "Use --mode local to create worktree for existing branch" >&2
            exit 1
        fi

        # Check if worktree path already exists
        if [[ -d "$WORKTREE_PATH" ]]; then
            echo "Error: Worktree already exists at $WORKTREE_PATH" >&2
            exit 1
        fi

        # Validate base branch exists on remote
        if ! git show-ref --verify --quiet "refs/remotes/origin/$BASE" 2>/dev/null; then
            echo "Error: Base branch 'origin/$BASE' not found" >&2
            echo "" >&2
            echo "Available remote branches:" >&2
            git branch -r --format='  %(refname:short)' | head -20 >&2
            exit 1
        fi

        # Atomic branch + worktree creation
        echo "Creating new branch and worktree..."
        echo "  Branch: $BRANCH"
        echo "  Base:   origin/$BASE"
        echo "  Path:   $WORKTREE_PATH"

        git worktree add -b "$BRANCH" "$WORKTREE_PATH" "origin/$BASE"
        ;;

    remote)
        # Mode 2: Track remote branch
        if [[ -z "$BRANCH" ]]; then
            echo "Error: --mode remote requires --branch <remote-branch>" >&2
            exit 1
        fi

        # Strip origin/ prefix if present for local branch name
        REMOTE_BRANCH="$BRANCH"
        LOCAL_BRANCH="${BRANCH#origin/}"

        # Extract date and slug from branch name
        if [[ "$LOCAL_BRANCH" =~ ^(feat|fix|refactor|chore)/([0-9]{4}-[0-9]{2}-[0-9]{2})-(.+)$ ]]; then
            DATE="${BASH_REMATCH[2]}"
            SLUG="${BASH_REMATCH[3]}"
        elif [[ "$LOCAL_BRANCH" =~ ^(feat|fix|refactor|chore)/(.+)$ ]]; then
            DATE=$(date +%Y-%m-%d)
            SLUG="${BASH_REMATCH[2]}"
        else
            DATE=$(date +%Y-%m-%d)
            SLUG="${LOCAL_BRANCH##*/}"
        fi

        WORKTREE_NAME="alpha-forge.worktree-${DATE}-${SLUG}"
        WORKTREE_PATH="${WORKTREE_BASE}/${WORKTREE_NAME}"

        # Validate remote branch exists
        if ! git show-ref --verify --quiet "refs/remotes/$REMOTE_BRANCH" 2>/dev/null; then
            echo "Error: Remote branch '$REMOTE_BRANCH' not found" >&2
            echo "" >&2
            echo "Available remote branches:" >&2
            git branch -r --format='  %(refname:short)' | head -20 >&2
            exit 1
        fi

        # Check if worktree path already exists
        if [[ -d "$WORKTREE_PATH" ]]; then
            echo "Error: Worktree already exists at $WORKTREE_PATH" >&2
            exit 1
        fi

        # Create tracking branch + worktree
        echo "Creating tracking branch and worktree..."
        echo "  Remote: $REMOTE_BRANCH"
        echo "  Local:  $LOCAL_BRANCH"
        echo "  Path:   $WORKTREE_PATH"

        git worktree add -b "$LOCAL_BRANCH" "$WORKTREE_PATH" "$REMOTE_BRANCH"
        BRANCH="$LOCAL_BRANCH"
        ;;

    local)
        # Mode 3: Existing local branch
        if [[ -z "$BRANCH" ]]; then
            echo "Error: --mode local requires --branch <branch>" >&2
            exit 1
        fi

        # Extract date and slug from branch name
        if [[ "$BRANCH" =~ ^(feat|fix|refactor|chore)/([0-9]{4}-[0-9]{2}-[0-9]{2})-(.+)$ ]]; then
            DATE="${BASH_REMATCH[2]}"
            SLUG="${BASH_REMATCH[3]}"
        elif [[ "$BRANCH" =~ ^(feat|fix|refactor|chore)/(.+)$ ]]; then
            DATE=$(date +%Y-%m-%d)
            SLUG="${BASH_REMATCH[2]}"
        else
            DATE=$(date +%Y-%m-%d)
            SLUG="${BRANCH##*/}"
        fi

        WORKTREE_NAME="alpha-forge.worktree-${DATE}-${SLUG}"
        WORKTREE_PATH="${WORKTREE_BASE}/${WORKTREE_NAME}"

        # Validate local branch exists
        if ! git show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
            echo "Error: Local branch '$BRANCH' not found" >&2
            echo "" >&2
            echo "Available local branches:" >&2
            git branch --format='  %(refname:short)' | head -20 >&2
            exit 1
        fi

        # Check if worktree path already exists
        if [[ -d "$WORKTREE_PATH" ]]; then
            echo "Error: Worktree already exists at $WORKTREE_PATH" >&2
            exit 1
        fi

        # Check if branch already has a worktree
        EXISTING_WT=$(git worktree list | grep "\[$BRANCH\]" | awk '{print $1}' || true)
        if [[ -n "$EXISTING_WT" ]]; then
            echo "Error: Branch '$BRANCH' already has a worktree at $EXISTING_WT" >&2
            exit 1
        fi

        # Create worktree for existing branch
        echo "Creating worktree for existing branch..."
        echo "  Branch: $BRANCH"
        echo "  Path:   $WORKTREE_PATH"

        git worktree add "$WORKTREE_PATH" "$BRANCH"
        ;;

    *)
        echo "Error: Unknown mode '$MODE'. Use: new|remote|local" >&2
        exit 1
        ;;
esac

# Generate tab name from slug
ACRONYM=$(echo "$SLUG" | tr '-' '\n' | cut -c1 | tr -d '\n' | tr '[:upper:]' '[:lower:]')
TAB_NAME="AF-${ACRONYM}"

# Create .envrc for direnv (auto-load environment variables)
ENVRC_PATH="${WORKTREE_PATH}/.envrc"
ENV_SHARED="${WORKTREE_BASE}/.env.alpha-forge"

if [[ -f "$ENV_SHARED" ]]; then
    cat > "$ENVRC_PATH" << EOF
# alpha-forge worktree direnv config
# Auto-generated by create-worktree.sh

# Load shared alpha-forge secrets (ClickHouse, API keys, etc.)
dotenv ${ENV_SHARED}

# Worktree-specific overrides can be added below
EOF
    echo "  Created .envrc (loads shared secrets)"

    # Auto-allow direnv if available
    if command -v direnv &> /dev/null; then
        (cd "$WORKTREE_PATH" && direnv allow) 2>/dev/null || true
    fi
else
    echo "  Note: No shared .env found at $ENV_SHARED"
    echo "        Create it to auto-load secrets in worktrees"
fi

echo ""
echo "✓ Worktree created successfully"
echo ""
echo "  Path:   $WORKTREE_PATH"
echo "  Branch: $BRANCH"
echo "  Tab:    $TAB_NAME"
echo ""
echo "  Note: Restart iTerm2 to see the new tab in your layout."
