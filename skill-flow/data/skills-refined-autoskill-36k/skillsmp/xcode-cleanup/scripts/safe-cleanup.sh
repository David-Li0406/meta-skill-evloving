#!/bin/bash
# safe-cleanup.sh - Clean items that are safe to delete without confirmation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}                    SAFE CLEANUP                               ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo ""

# Track bytes cleaned
total_cleaned=0

# Function to get size in KB before cleaning
get_size_kb() {
    local dir="$1"
    if [ -d "$dir" ]; then
        du -sk "$dir" 2>/dev/null | cut -f1 || echo "0"
    else
        echo "0"
    fi
}

# Function to format KB to human readable
format_kb() {
    local kb=$1
    if [ "$kb" -ge 1048576 ]; then
        echo "$(echo "scale=1; $kb / 1048576" | bc)G"
    elif [ "$kb" -ge 1024 ]; then
        echo "$(echo "scale=1; $kb / 1024" | bc)M"
    else
        echo "${kb}K"
    fi
}

# 1. Xcode Caches
XCODE_CACHES="$HOME/Library/Caches/com.apple.dt.Xcode"
size_kb=$(get_size_kb "$XCODE_CACHES")
total_cleaned=$((total_cleaned + size_kb))
echo -e "${CYAN}Xcode Caches:${NC} $(format_kb $size_kb)"
if [ -d "$XCODE_CACHES" ] && [ "$(ls -A "$XCODE_CACHES" 2>/dev/null)" ]; then
    rm -rf "$XCODE_CACHES"/* 2>/dev/null
    echo -e "  ${GREEN}Cleaned${NC}"
else
    echo -e "  ${YELLOW}Already empty${NC}"
fi
echo ""

# 2. Simulator Caches
SIM_CACHES="$HOME/Library/Developer/CoreSimulator/Caches"
size_kb=$(get_size_kb "$SIM_CACHES")
total_cleaned=$((total_cleaned + size_kb))
echo -e "${CYAN}Simulator Caches:${NC} $(format_kb $size_kb)"
if [ -d "$SIM_CACHES" ] && [ "$(ls -A "$SIM_CACHES" 2>/dev/null)" ]; then
    rm -rf "$SIM_CACHES"/* 2>/dev/null
    echo -e "  ${GREEN}Cleaned${NC}"
else
    echo -e "  ${YELLOW}Already empty${NC}"
fi
echo ""

# 3. SwiftUI Previews
PREVIEWS="$HOME/Library/Developer/Xcode/UserData/Previews"
size_kb=$(get_size_kb "$PREVIEWS")
total_cleaned=$((total_cleaned + size_kb))
echo -e "${CYAN}SwiftUI Previews:${NC} $(format_kb $size_kb)"
if [ -d "$PREVIEWS" ] && [ "$(ls -A "$PREVIEWS" 2>/dev/null)" ]; then
    rm -rf "$PREVIEWS"/* 2>/dev/null
    echo -e "  ${GREEN}Cleaned${NC}"
else
    echo -e "  ${YELLOW}Already empty${NC}"
fi
echo ""

# 4. Module Cache
MODULE_CACHE="$HOME/Library/Developer/Xcode/DerivedData/ModuleCache.noindex"
size_kb=$(get_size_kb "$MODULE_CACHE")
total_cleaned=$((total_cleaned + size_kb))
echo -e "${CYAN}Module Cache:${NC} $(format_kb $size_kb)"
if [ -d "$MODULE_CACHE" ] && [ "$(ls -A "$MODULE_CACHE" 2>/dev/null)" ]; then
    rm -rf "$MODULE_CACHE"/* 2>/dev/null
    echo -e "  ${GREEN}Cleaned${NC}"
else
    echo -e "  ${YELLOW}Already empty${NC}"
fi
echo ""

# 5. Orphaned Derived Data (projects that no longer exist)
echo -e "${CYAN}Orphaned Derived Data:${NC}"
DERIVED_DATA="$HOME/Library/Developer/Xcode/DerivedData"
orphan_count=0
orphan_cleaned=0

if [ -d "$DERIVED_DATA" ]; then
    for dir in "$DERIVED_DATA"/*/; do
        folder_name=$(basename "$dir")

        # Skip cache folders
        if [[ "$folder_name" == *"Cache"* ]] || [[ "$folder_name" == *"noindex"* ]] || [[ "$folder_name" == "."* ]]; then
            continue
        fi

        plist="$dir/info.plist"
        if [ ! -f "$plist" ]; then
            continue
        fi

        # Get workspace path
        workspace=$(/usr/libexec/PlistBuddy -c "Print :WorkspacePath" "$plist" 2>/dev/null || echo "")
        if [ -z "$workspace" ]; then
            continue
        fi

        project_dir=$(dirname "$workspace")

        # Check if path exists - if not, it's orphaned
        if [ ! -d "$project_dir" ]; then
            size_kb=$(get_size_kb "$dir")
            total_cleaned=$((total_cleaned + size_kb))
            orphan_cleaned=$((orphan_cleaned + size_kb))
            orphan_count=$((orphan_count + 1))

            echo -e "  ${RED}Removing:${NC} $folder_name ($(format_kb $size_kb))"
            echo -e "    Was: $project_dir"
            rm -rf "$dir"
        fi
    done
fi

if [ $orphan_count -eq 0 ]; then
    echo -e "  ${YELLOW}No orphaned folders found${NC}"
else
    echo -e "  ${GREEN}Removed $orphan_count orphaned folders ($(format_kb $orphan_cleaned))${NC}"
fi
echo ""

# Summary
echo -e "${BOLD}${BLUE}----------------------------------------------------------------${NC}"
echo -e "${BOLD}${GREEN}TOTAL CLEANED: $(format_kb $total_cleaned)${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"
