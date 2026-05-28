#!/usr/bin/env bash
# chezmoi-sync-auto.sh - Non-interactive sync for Claude Code
# Usage: chezmoi-sync-auto.sh [commit-message] [--add-new file1 file2 ...]
#
# Re-adds all modified tracked files in current directory,
# optionally adds specified new files, commits, and pushes.
#
# When adding new files with private permissions (600/700), the script
# will warn and prompt for confirmation before proceeding.

set -euo pipefail

COMMIT_MSG="Update $(basename "$PWD") config"
NEW_FILES=()
PARSING_NEW=false

# Parse arguments
for arg in "$@"; do
    if [[ "$arg" == "--add-new" ]]; then
        PARSING_NEW=true
        continue
    fi

    if $PARSING_NEW; then
        NEW_FILES+=("$arg")
    else
        COMMIT_MSG="$arg"
    fi
done

# Check chezmoi is available
command -v chezmoi &> /dev/null || { echo "Error: chezmoi not found" >&2; exit 1; }

SOURCE_PATH="$(chezmoi source-path)"
echo "Syncing to chezmoi source: $SOURCE_PATH"

# Re-add all modified files in current directory
# Only suppress the specific "not in source state" warning for untracked files
echo "Re-adding modified files..."
if ! chezmoi re-add . 2>&1 | grep -v "not in source state"; then
    : # Ignore grep exit code when no output
fi

# Check if a file has private permissions (only owner has access)
is_private_file() {
    local file="$1"
    local perms
    perms=$(stat -c "%a" "$file" 2>/dev/null) || return 1

    # Check if group and others have no permissions (last two digits are 00)
    [[ "${perms: -2}" == "00" ]]
}

# Get human-readable permissions
get_perms_display() {
    local file="$1"
    stat -c "%a (%A)" "$file" 2>/dev/null || echo "unknown"
}

# Add any specified new files (with private permission check)
for file in "${NEW_FILES[@]}"; do
    if [[ ! -e "$file" ]]; then
        echo "Warning: File not found: $file" >&2
        continue
    fi

    # Check for private permissions on new files
    if is_private_file "$file"; then
        perms_display=$(get_perms_display "$file")
        echo ""
        echo "WARNING: File has private permissions!"
        echo "  File: $file"
        echo "  Permissions: $perms_display"
        echo ""
        echo "Private permissions (600/700) mean only the owner can access this file."
        echo "Chezmoi will add this with a 'private_' prefix, preserving these permissions."
        echo ""
        read -r -p "Add this file with private permissions? [y/N]: " confirm

        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "Skipping: $file"
            continue
        fi
    fi

    echo "Adding new file: $file"
    chezmoi add "$file"
done

# Commit and push
cd "$SOURCE_PATH"

# Stage all changes first, then check if there's anything to commit
git add -A

if git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

echo "Changes:"
git status --short
git commit -m "$COMMIT_MSG"
git push

echo "Done: changes committed and pushed"
