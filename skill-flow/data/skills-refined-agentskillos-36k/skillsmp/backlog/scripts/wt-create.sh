#!/bin/bash
# Create worktree with proper submodule handling
# Usage: wt-create.sh <branch-name> [base-dir]
#
# Arguments:
#   branch-name: Name of the branch/worktree to create
#   base-dir: Optional repo root (defaults to git root)
#
# Submodule Strategy:
#   Worktrees share .git/modules/ with the main worktree, so standard
#   `git submodule update --init --recursive` works correctly. Git will
#   create proper .git file pointers for each submodule in the worktree.
#
# Platform-Specific Copy-On-Write (CoW) Support:
#   - macOS (APFS): Uses `cp -c` for instant file cloning
#   - Linux (Btrfs/XFS/ZFS): Uses `cp --reflink=auto` for CoW clones
#   - Linux (ext4) / WSL: Falls back to regular copy (no CoW support)
#
# Exit codes:
#   0 - Success
#   1 - Submodule initialization failed (worktree created but unusable)

set -e

BRANCH="${1:?Usage: wt-create.sh <branch-name> [base-dir]}"
BASE_DIR="${2:-$(git rev-parse --show-toplevel)}"
REPO_NAME="$(basename "$BASE_DIR")"
WT_BASE="${BASE_DIR}-wt"
WORKTREE_PATH="$WT_BASE/$BRANCH"

# Detect platform and set copy command for CoW support
detect_copy_command() {
    local os_type
    os_type="$(uname -s)"

    case "$os_type" in
        Darwin)
            # macOS with APFS - use clone flag for instant CoW copies
            echo "cp -c -p -R"
            ;;
        Linux)
            # Linux - try reflink for Btrfs/XFS/ZFS, falls back gracefully on ext4
            # --reflink=auto: Uses CoW if supported, regular copy otherwise
            echo "cp --reflink=auto -p -R"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            # Windows Git Bash / MSYS2 / Cygwin - no CoW support
            echo "cp -p -R"
            ;;
        *)
            # Unknown OS - use standard copy
            echo "cp -p -R"
            ;;
    esac
}

# Get platform-specific copy command
COPY_CMD=$(detect_copy_command)

# Function to copy with CoW support and informative output
cow_copy() {
    local src="$1"
    local dst="$2"

    # Execute the copy
    if $COPY_CMD "$src" "$dst"; then
        return 0
    else
        # If CoW copy fails, fall back to regular copy
        if [[ "$COPY_CMD" != "cp -p -R" ]]; then
            echo "      (CoW copy failed, using regular copy)"
            cp -p -R "$src" "$dst"
        else
            return 1
        fi
    fi
}

# Function to verify submodules are functional (defined early for reuse)
verify_submodules() {
    local all_ok=true
    while IFS= read -r subpath; do
        if [ -d "$subpath" ]; then
            if ! git -C "$subpath" rev-parse --git-dir &>/dev/null; then
                echo "  ❌ $subpath: not a valid git repository"
                all_ok=false
            fi
        fi
    done < <(grep "path = " .gitmodules 2>/dev/null | sed 's/.*path = //')

    $all_ok
}

echo "Creating worktree: $BRANCH"
echo "  Base repo: $BASE_DIR"
echo "  Worktree path: $WORKTREE_PATH"

# Check if worktree already exists
if git -C "$BASE_DIR" worktree list | grep -q "$WORKTREE_PATH"; then
    echo "⚠️  Worktree already exists at $WORKTREE_PATH"
    # Verify submodules in existing worktree
    cd "$WORKTREE_PATH"
    if [ -f ".gitmodules" ]; then
        echo "  Verifying existing submodules..."
        if ! verify_submodules; then
            echo "⚠️  Existing worktree has broken submodules"
            echo "  Attempting repair..."
            # Use aggressive repair: deinit then reinit
            git submodule deinit -f --all 2>/dev/null || true
            git submodule update --init --recursive
        fi
    fi
    exit 0
fi

# Create worktree
if git -C "$BASE_DIR" show-ref --verify --quiet "refs/heads/$BRANCH"; then
    echo "  Branch exists, creating worktree..."
    git -C "$BASE_DIR" worktree add "$WORKTREE_PATH" "$BRANCH"
else
    echo "  Creating new branch from HEAD..."
    git -C "$BASE_DIR" worktree add -b "$BRANCH" "$WORKTREE_PATH" HEAD
fi

# Initialize submodules
echo ""
echo "Initializing submodules..."
cd "$WORKTREE_PATH"

# Check if there are submodules to initialize
if [ ! -f ".gitmodules" ]; then
    echo "  No submodules found"
    echo ""
    echo "✅ Worktree ready: $WORKTREE_PATH"
    exit 0
fi

# Standard submodule initialization
# Worktrees share .git/modules/ so this should work without --reference
echo "  Running git submodule update --init --recursive..."
if git submodule update --init --recursive; then
    echo "  ✅ Submodules initialized"
else
    echo ""
    echo "  ⚠️  Submodule initialization failed!"
    echo "  This may be due to network issues or repository access."
    echo ""
    echo "  Attempting fallback: copying from main repo..."

    # Fallback: copy submodule contents and fix .git pointers
    MAIN_GIT_DIR=$(git rev-parse --git-common-dir)
    SUBMODULE_ERRORS=0

    # Show platform info for copy operation
    echo "  Using copy command: $COPY_CMD"
    case "$(uname -s)" in
        Darwin)
            echo "  (macOS APFS - instant CoW clones)"
            ;;
        Linux)
            # Check if reflink is actually supported
            local fs_type
            fs_type=$(df -T "$BASE_DIR" 2>/dev/null | tail -1 | awk '{print $2}')
            case "$fs_type" in
                btrfs|xfs|zfs)
                    echo "  (Linux $fs_type - CoW reflinks enabled)"
                    ;;
                *)
                    echo "  (Linux $fs_type - CoW not supported, using regular copy)"
                    ;;
            esac
            ;;
        *)
            echo "  (Standard copy - no CoW support)"
            ;;
    esac
    echo ""

    while IFS= read -r subpath; do
        src="$BASE_DIR/$subpath"
        dst="$WORKTREE_PATH/$subpath"

        if [ -d "$src" ] && [ ! -z "$(ls -A "$src" 2>/dev/null)" ]; then
            echo "    Copying $subpath..."
            rm -rf "$dst"
            mkdir -p "$(dirname "$dst")"
            cow_copy "$src" "$dst"

            # Fix the .git file pointer to use absolute path
            if [ -f "$dst/.git" ]; then
                # Get module path from the worktree's git dir
                WT_GIT_DIR=$(git rev-parse --git-dir)
                MODULE_DIR="$WT_GIT_DIR/modules/$subpath"

                if [ -d "$MODULE_DIR" ]; then
                    echo "gitdir: $MODULE_DIR" > "$dst/.git"
                    echo "      Fixed .git pointer → $MODULE_DIR"
                else
                    # Try the common dir's modules
                    COMMON_MODULE_DIR="$MAIN_GIT_DIR/modules/$subpath"
                    if [ -d "$COMMON_MODULE_DIR" ]; then
                        echo "gitdir: $COMMON_MODULE_DIR" > "$dst/.git"
                        echo "      Fixed .git pointer → $COMMON_MODULE_DIR"
                    else
                        echo "      ⚠️  Could not find module directory for $subpath"
                        ((SUBMODULE_ERRORS++))
                    fi
                fi
            fi
        else
            echo "    ⚠️  Source not found: $src"
            ((SUBMODULE_ERRORS++))
        fi
    done < <(grep "path = " .gitmodules 2>/dev/null | sed 's/.*path = //')

    if [ $SUBMODULE_ERRORS -gt 0 ]; then
        echo ""
        echo "  ⚠️  $SUBMODULE_ERRORS submodule(s) could not be initialized"
    else
        echo "  ✅ Submodules copied with fixed pointers"
    fi
fi

# Verify all submodules are functional
echo ""
echo "Verifying submodules..."
if verify_submodules; then
    echo "✅ All submodules verified"
else
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo " ⚠️  SUBMODULE VERIFICATION FAILED"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    echo "Some submodules are not properly initialized. Git commands may fail."
    echo ""
    echo "To fix manually, run in the worktree:"
    echo "  cd $WORKTREE_PATH"
    echo "  git submodule update --init --recursive"
    echo ""
    echo "If that fails, try:"
    echo "  git submodule deinit -f --all"
    echo "  git submodule update --init --recursive"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    exit 1
fi

echo ""
echo "✅ Worktree ready: $WORKTREE_PATH"
