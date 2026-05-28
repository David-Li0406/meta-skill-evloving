#!/bin/bash
# analyze-derived-data.sh - Analyze DerivedData folders with git worktree detection

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

DERIVED_DATA="$HOME/Library/Developer/Xcode/DerivedData"

# Check if DerivedData exists
if [ ! -d "$DERIVED_DATA" ]; then
    echo "No DerivedData folder found at $DERIVED_DATA"
    exit 0
fi

echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}                 DERIVED DATA ANALYSIS                         ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo ""

# Track totals
total_active=0
total_orphaned=0
active_size_kb=0
orphaned_size_kb=0

# Process each project folder (skip cache folders)
for dir in "$DERIVED_DATA"/*/; do
    folder_name=$(basename "$dir")

    # Skip cache/system folders
    if [[ "$folder_name" == *"Cache"* ]] || [[ "$folder_name" == *"noindex"* ]] || [[ "$folder_name" == "."* ]]; then
        continue
    fi

    plist="$dir/info.plist"
    if [ ! -f "$plist" ]; then
        continue
    fi

    # Extract workspace path
    workspace=$(/usr/libexec/PlistBuddy -c "Print :WorkspacePath" "$plist" 2>/dev/null || echo "")
    if [ -z "$workspace" ]; then
        continue
    fi

    project_dir=$(dirname "$workspace")
    size=$(du -sh "$dir" 2>/dev/null | cut -f1 || echo "?")
    size_kb=$(du -sk "$dir" 2>/dev/null | cut -f1 || echo "0")

    # Determine worktree status
    worktree_status=""
    is_orphaned=false

    if [ -d "$project_dir" ]; then
        # Path exists - check if it's a worktree
        git_root=$(git -C "$project_dir" rev-parse --show-toplevel 2>/dev/null || echo "")

        if [ -n "$git_root" ]; then
            # It's a git repo - check worktree list
            worktree_paths=$(git -C "$git_root" worktree list 2>/dev/null | awk '{print $1}')

            if echo "$worktree_paths" | grep -q "^${project_dir}$"; then
                worktree_status="${GREEN}ACTIVE WORKTREE${NC}"
                total_active=$((total_active + 1))
                active_size_kb=$((active_size_kb + size_kb))
            else
                worktree_status="${YELLOW}PATH EXISTS (not a worktree)${NC}"
                total_active=$((total_active + 1))
                active_size_kb=$((active_size_kb + size_kb))
            fi
        else
            # Not a git repo
            worktree_status="${YELLOW}PATH EXISTS (not a git repo)${NC}"
            total_active=$((total_active + 1))
            active_size_kb=$((active_size_kb + size_kb))
        fi
    else
        # Path doesn't exist - orphaned
        worktree_status="${RED}ORPHANED${NC}"
        is_orphaned=true
        total_orphaned=$((total_orphaned + 1))
        orphaned_size_kb=$((orphaned_size_kb + size_kb))
    fi

    # Output
    echo -e "${BOLD}$folder_name${NC}"
    echo -e "  Path: $project_dir"
    echo -e "  Size: $size"
    echo -e "  Status: $worktree_status"
    if [ "$is_orphaned" = true ]; then
        echo -e "  ${RED}>>> Safe to delete${NC}"
    fi
    echo ""
done

# Summary
echo -e "${BOLD}${BLUE}----------------------------------------------------------------${NC}"
echo -e "${BOLD}${CYAN}SUMMARY:${NC}"
echo ""

# Convert KB to human readable
if [ $active_size_kb -ge 1048576 ]; then
    active_size="$(echo "scale=1; $active_size_kb / 1048576" | bc)G"
elif [ $active_size_kb -ge 1024 ]; then
    active_size="$(echo "scale=1; $active_size_kb / 1024" | bc)M"
else
    active_size="${active_size_kb}K"
fi

if [ $orphaned_size_kb -ge 1048576 ]; then
    orphaned_size="$(echo "scale=1; $orphaned_size_kb / 1048576" | bc)G"
elif [ $orphaned_size_kb -ge 1024 ]; then
    orphaned_size="$(echo "scale=1; $orphaned_size_kb / 1024" | bc)M"
else
    orphaned_size="${orphaned_size_kb}K"
fi

echo -e "  ${GREEN}Active/Protected:${NC} $total_active folders ($active_size)"
echo -e "  ${RED}Orphaned (safe to delete):${NC} $total_orphaned folders ($orphaned_size)"
echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
