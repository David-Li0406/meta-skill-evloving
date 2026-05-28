#!/bin/bash
# list-cleanup-targets.sh - List all cleanup targets with sizes and details

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Function to get directory size
get_dir_size() {
    local dir="$1"
    if [ -d "$dir" ]; then
        du -sh "$dir" 2>/dev/null | cut -f1 || echo "-"
    else
        echo "-"
    fi
}

# Function to list directory contents with sizes
list_with_sizes() {
    local dir="$1"
    local max_items="${2:-10}"
    if [ -d "$dir" ]; then
        du -sh "$dir"/* 2>/dev/null | sort -hr | head -n "$max_items" | while read -r size name; do
            basename_name=$(basename "$name")
            printf "    %-50s %s\n" "$basename_name" "$size"
        done
    fi
}

echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}                  XCODE CLEANUP TARGETS                        ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"

# ============================================================================
# SAFE TO DELETE (No confirmation needed)
# ============================================================================
echo ""
echo -e "${BOLD}${GREEN}SAFE TO DELETE (caches, auto-regenerated):${NC}"
echo ""

# Xcode Caches
XCODE_CACHES="$HOME/Library/Caches/com.apple.dt.Xcode"
echo -e "  ${CYAN}Xcode Caches:${NC} $(get_dir_size "$XCODE_CACHES")"
echo "    Location: $XCODE_CACHES"
echo ""

# Simulator Caches
SIM_CACHES="$HOME/Library/Developer/CoreSimulator/Caches"
echo -e "  ${CYAN}Simulator Caches:${NC} $(get_dir_size "$SIM_CACHES")"
echo "    Location: $SIM_CACHES"
echo ""

# SwiftUI Previews
PREVIEWS="$HOME/Library/Developer/Xcode/UserData/Previews"
echo -e "  ${CYAN}SwiftUI Previews:${NC} $(get_dir_size "$PREVIEWS")"
echo "    Location: $PREVIEWS"
echo ""

# Module Cache
MODULE_CACHE="$HOME/Library/Developer/Xcode/DerivedData/ModuleCache.noindex"
echo -e "  ${CYAN}Module Cache:${NC} $(get_dir_size "$MODULE_CACHE")"
echo "    Location: $MODULE_CACHE"
echo ""

# ============================================================================
# DEVICE SUPPORT (Requires confirmation)
# ============================================================================
echo -e "${BOLD}${YELLOW}DEVICE SUPPORT (confirm before deleting):${NC}"
echo -e "  ${RED}Warning: Takes time to re-download when connecting devices${NC}"
echo ""

# iOS Device Support
IOS_SUPPORT="$HOME/Library/Developer/Xcode/iOS DeviceSupport"
echo -e "  ${CYAN}iOS Device Support:${NC} $(get_dir_size "$IOS_SUPPORT")"
if [ -d "$IOS_SUPPORT" ]; then
    echo "    Versions:"
    list_with_sizes "$IOS_SUPPORT" 15
fi
echo ""

# watchOS Device Support
WATCHOS_SUPPORT="$HOME/Library/Developer/Xcode/watchOS DeviceSupport"
echo -e "  ${CYAN}watchOS Device Support:${NC} $(get_dir_size "$WATCHOS_SUPPORT")"
if [ -d "$WATCHOS_SUPPORT" ]; then
    echo "    Versions:"
    list_with_sizes "$WATCHOS_SUPPORT" 10
fi
echo ""

# tvOS Device Support
TVOS_SUPPORT="$HOME/Library/Developer/Xcode/tvOS DeviceSupport"
echo -e "  ${CYAN}tvOS Device Support:${NC} $(get_dir_size "$TVOS_SUPPORT")"
if [ -d "$TVOS_SUPPORT" ]; then
    echo "    Versions:"
    list_with_sizes "$TVOS_SUPPORT" 10
fi
echo ""

# ============================================================================
# SIMULATORS (Requires confirmation)
# ============================================================================
echo -e "${BOLD}${YELLOW}SIMULATORS (confirm before deleting):${NC}"
echo -e "  ${RED}Warning: Runtimes are large downloads (several GB each)${NC}"
echo ""

# Simulator Runtimes
SIM_RUNTIMES="/Library/Developer/CoreSimulator/Profiles/Runtimes"
echo -e "  ${CYAN}Simulator Runtimes:${NC} $(get_dir_size "$SIM_RUNTIMES")"
if [ -d "$SIM_RUNTIMES" ]; then
    echo "    Installed runtimes:"
    xcrun simctl runtime list 2>/dev/null | grep -E "iOS|watchOS|tvOS|visionOS" | head -20 | while read -r line; do
        echo "      $line"
    done
fi
echo ""

# Unavailable simulators
echo -e "  ${CYAN}Unavailable Simulators:${NC}"
unavailable_count=$(xcrun simctl list devices unavailable 2>/dev/null | grep -c "unavailable" || echo "0")
echo "    Count: $unavailable_count devices"
echo "    Command to delete: xcrun simctl delete unavailable"
echo ""

# ============================================================================
# ARCHIVES (Requires confirmation)
# ============================================================================
echo -e "${BOLD}${YELLOW}ARCHIVES (confirm before deleting):${NC}"
echo -e "  ${RED}Warning: These are your release builds${NC}"
echo ""

ARCHIVES="$HOME/Library/Developer/Xcode/Archives"
echo -e "  ${CYAN}Archives:${NC} $(get_dir_size "$ARCHIVES")"
if [ -d "$ARCHIVES" ]; then
    echo "    By date:"
    list_with_sizes "$ARCHIVES" 10
fi
echo ""

# ============================================================================
# DERIVED DATA (Mixed - depends on worktree status)
# ============================================================================
echo -e "${BOLD}${YELLOW}DERIVED DATA (see analyze-derived-data.sh for details):${NC}"
echo ""

DERIVED_DATA="$HOME/Library/Developer/Xcode/DerivedData"
echo -e "  ${CYAN}Total Derived Data:${NC} $(get_dir_size "$DERIVED_DATA")"
echo "    Location: $DERIVED_DATA"
echo "    Note: Run analyze-derived-data.sh to see which folders are safe to delete"
echo ""

echo -e "${BOLD}${BLUE}================================================================${NC}"
