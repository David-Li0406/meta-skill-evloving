#!/bin/bash
# list-confirmable.sh - List items that require user confirmation before deletion
# Makes clear distinction between Device Support (physical devices) and Simulators

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
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

echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}              ITEMS REQUIRING CONFIRMATION                     ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"

# ============================================================================
# SECTION 1: DEVICE SUPPORT (Physical Devices)
# ============================================================================
echo ""
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${MAGENTA}  DEVICE SUPPORT - Debug symbols from PHYSICAL DEVICES        ${NC}"
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  These are downloaded ${BOLD}automatically${NC} when you connect a physical"
echo -e "  iPhone, iPad, or Apple Watch to your Mac. They're used to"
echo -e "  symbolicate crash logs from those devices."
echo ""
echo -e "  ${YELLOW}If you delete these, they'll re-download next time you${NC}"
echo -e "  ${YELLOW}connect that device (can take several minutes).${NC}"
echo ""

# iOS Device Support
IOS_SUPPORT="$HOME/Library/Developer/Xcode/iOS DeviceSupport"
echo -e "${BOLD}${CYAN}iOS Device Support${NC} ($(get_dir_size "$IOS_SUPPORT"))"
echo -e "  From physical iPhones/iPads you've connected:"
echo ""
if [ -d "$IOS_SUPPORT" ]; then
    du -sh "$IOS_SUPPORT"/* 2>/dev/null | sort -hr | while read -r size path; do
        name=$(basename "$path")
        printf "    ${YELLOW}%-50s${NC} %s\n" "$name" "$size"
    done
else
    echo "    (none)"
fi
echo ""

# watchOS Device Support
WATCHOS_SUPPORT="$HOME/Library/Developer/Xcode/watchOS DeviceSupport"
if [ -d "$WATCHOS_SUPPORT" ] && [ "$(ls -A "$WATCHOS_SUPPORT" 2>/dev/null)" ]; then
    echo -e "${BOLD}${CYAN}watchOS Device Support${NC} ($(get_dir_size "$WATCHOS_SUPPORT"))"
    echo -e "  From physical Apple Watches you've connected:"
    echo ""
    du -sh "$WATCHOS_SUPPORT"/* 2>/dev/null | sort -hr | while read -r size path; do
        name=$(basename "$path")
        printf "    ${YELLOW}%-50s${NC} %s\n" "$name" "$size"
    done
    echo ""
fi

# tvOS Device Support
TVOS_SUPPORT="$HOME/Library/Developer/Xcode/tvOS DeviceSupport"
if [ -d "$TVOS_SUPPORT" ] && [ "$(ls -A "$TVOS_SUPPORT" 2>/dev/null)" ]; then
    echo -e "${BOLD}${CYAN}tvOS Device Support${NC} ($(get_dir_size "$TVOS_SUPPORT"))"
    echo -e "  From physical Apple TVs you've connected:"
    echo ""
    du -sh "$TVOS_SUPPORT"/* 2>/dev/null | sort -hr | while read -r size path; do
        name=$(basename "$path")
        printf "    ${YELLOW}%-50s${NC} %s\n" "$name" "$size"
    done
    echo ""
fi

# ============================================================================
# SECTION 2: SIMULATOR RUNTIMES (Downloaded OS Images)
# ============================================================================
echo ""
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${MAGENTA}  SIMULATOR RUNTIMES - OS images you downloaded for Simulator ${NC}"
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  These are the iOS/visionOS versions you explicitly downloaded"
echo -e "  through Xcode to run in Simulator. NOT from physical devices."
echo ""
echo -e "  ${RED}These are LARGE (5-10GB each) and slow to re-download.${NC}"
echo -e "  ${RED}Deleting removes ALL simulators using that runtime.${NC}"
echo ""

echo -e "${BOLD}${CYAN}Installed Runtimes:${NC}"
runtime_info=$(xcrun simctl runtime list 2>/dev/null)
total_line=$(echo "$runtime_info" | grep "Total Disk Images")
echo -e "  $total_line"
echo ""

# Group by OS
echo "  iOS Runtimes:"
echo "$runtime_info" | grep "^iOS" | while read -r line; do
    printf "    ${YELLOW}%s${NC}\n" "$line"
done
echo ""

echo "  visionOS Runtimes:"
echo "$runtime_info" | grep "^xrOS" | while read -r line; do
    printf "    ${YELLOW}%s${NC}\n" "$line"
done
echo ""

echo -e "  ${GREEN}Tip: Multiple versions of same OS (e.g., iOS 26.0) are often${NC}"
echo -e "  ${GREEN}beta builds you can safely remove if you have the release.${NC}"
echo ""

# ============================================================================
# SECTION 3: SIMULATOR DEVICES (Instances and Data)
# ============================================================================
echo ""
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${MAGENTA}  SIMULATOR DEVICES - Simulator instances and their app data  ${NC}"
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  These are the actual simulator instances (iPhone 16 Pro, iPad, etc.)"
echo -e "  and all the apps/data installed on them."
echo ""

SIM_DEVICES="$HOME/Library/Developer/CoreSimulator/Devices"
echo -e "${BOLD}${CYAN}Total Simulator Device Storage:${NC} $(get_dir_size "$SIM_DEVICES")"
echo ""

# Show device count summary
total_devices=$(xcrun simctl list devices 2>/dev/null | grep -cE "^\s+\S.*\(" || echo "0")
echo "  Total simulator instances: $total_devices"
echo ""
echo "  To see full list: xcrun simctl list devices"
echo ""

# Unavailable
unavailable_output=$(xcrun simctl list devices unavailable 2>/dev/null)
unavailable_count=$(echo "$unavailable_output" | grep -cE "^\s+\S.*\(" || echo "0")
if [ "$unavailable_count" -gt 0 ] 2>/dev/null; then
    echo -e "  ${RED}Unavailable Simulators: $unavailable_count${NC}"
    echo -e "  ${GREEN}Safe to remove with: xcrun simctl delete unavailable${NC}"
else
    echo -e "  ${GREEN}No unavailable simulators to clean up${NC}"
fi
echo ""

# ============================================================================
# SECTION 4: ARCHIVES
# ============================================================================
echo ""
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}${MAGENTA}  ARCHIVES - Your App Store / distribution builds             ${NC}"
echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  These are builds you created for App Store submission or"
echo -e "  ad-hoc distribution. Useful for symbolication of production crashes."
echo ""

ARCHIVES="$HOME/Library/Developer/Xcode/Archives"
echo -e "${BOLD}${CYAN}Total Archives:${NC} $(get_dir_size "$ARCHIVES")"
echo ""
if [ -d "$ARCHIVES" ]; then
    echo "  By date:"
    du -sh "$ARCHIVES"/*/ 2>/dev/null | sort -hr | while read -r size path; do
        name=$(basename "$path")
        printf "    ${YELLOW}%-20s${NC} %s\n" "$name" "$size"
    done
else
    echo "    (none)"
fi
echo ""

echo -e "${BOLD}${BLUE}================================================================${NC}"
