#!/bin/bash
# disk-stats.sh - Show disk space and Xcode-related storage usage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Function to format bytes to human readable
format_size() {
    local size=$1
    if [ "$size" -ge 1073741824 ]; then
        echo "$(echo "scale=1; $size / 1073741824" | bc)G"
    elif [ "$size" -ge 1048576 ]; then
        echo "$(echo "scale=1; $size / 1048576" | bc)M"
    elif [ "$size" -ge 1024 ]; then
        echo "$(echo "scale=1; $size / 1024" | bc)K"
    else
        echo "${size}B"
    fi
}

# Function to get directory size in bytes (returns 0 if doesn't exist)
get_dir_size_bytes() {
    local dir="$1"
    if [ -d "$dir" ]; then
        du -sk "$dir" 2>/dev/null | awk '{print $1 * 1024}' || echo "0"
    else
        echo "0"
    fi
}

# Function to get directory size human readable
get_dir_size() {
    local dir="$1"
    if [ -d "$dir" ]; then
        du -sh "$dir" 2>/dev/null | cut -f1 || echo "0"
    else
        echo "-"
    fi
}

echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}                    XCODE DISK SPACE REPORT                    ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo ""

# Current disk space (using diskutil for accurate APFS info)
echo -e "${BOLD}${CYAN}DISK SPACE:${NC}"
diskutil_output=$(diskutil info /)
container_total=$(echo "$diskutil_output" | grep "Container Total Space" | sed 's/.*: *//' | awk '{print $1, $2}')
container_free=$(echo "$diskutil_output" | grep "Container Free Space" | sed 's/.*: *//' | awk '{print $1, $2}')
container_total_bytes=$(echo "$diskutil_output" | grep "Container Total Space" | grep -o '([0-9]* Bytes)' | grep -o '[0-9]*')
container_free_bytes=$(echo "$diskutil_output" | grep "Container Free Space" | grep -o '([0-9]* Bytes)' | grep -o '[0-9]*')

# Calculate used and percentage
if [ -n "$container_total_bytes" ] && [ -n "$container_free_bytes" ]; then
    container_used_bytes=$((container_total_bytes - container_free_bytes))
    container_used=$(format_size $container_used_bytes)
    pct_used=$(echo "scale=1; ($container_used_bytes * 100) / $container_total_bytes" | bc)
    echo -e "  Total: ${BOLD}$container_total${NC} | Used: ${BOLD}$container_used${NC} | Free: ${BOLD}${RED}$container_free${NC} (${RED}${pct_used}% used${NC})"
else
    # Fallback to df if diskutil fails
    df -h / | awk 'NR==2 {printf "  Total: %s | Used: %s | Free: %s (%s used)\n", $2, $3, $4, $5}'
fi
echo ""

# Xcode locations
DERIVED_DATA="$HOME/Library/Developer/Xcode/DerivedData"
IOS_DEVICE_SUPPORT="$HOME/Library/Developer/Xcode/iOS DeviceSupport"
WATCHOS_DEVICE_SUPPORT="$HOME/Library/Developer/Xcode/watchOS DeviceSupport"
TVOS_DEVICE_SUPPORT="$HOME/Library/Developer/Xcode/tvOS DeviceSupport"
ARCHIVES="$HOME/Library/Developer/Xcode/Archives"
XCODE_CACHES="$HOME/Library/Caches/com.apple.dt.Xcode"
SIM_CACHES="$HOME/Library/Developer/CoreSimulator/Caches"
SIM_DEVICES="$HOME/Library/Developer/CoreSimulator/Devices"
PREVIEWS="$HOME/Library/Developer/Xcode/UserData/Previews"
SIM_RUNTIMES="/Library/Developer/CoreSimulator/Profiles/Runtimes"

# Calculate sizes
derived_size=$(get_dir_size "$DERIVED_DATA")
ios_support_size=$(get_dir_size "$IOS_DEVICE_SUPPORT")
watchos_support_size=$(get_dir_size "$WATCHOS_DEVICE_SUPPORT")
tvos_support_size=$(get_dir_size "$TVOS_DEVICE_SUPPORT")
archives_size=$(get_dir_size "$ARCHIVES")
xcode_cache_size=$(get_dir_size "$XCODE_CACHES")
sim_cache_size=$(get_dir_size "$SIM_CACHES")
sim_devices_size=$(get_dir_size "$SIM_DEVICES")
previews_size=$(get_dir_size "$PREVIEWS")
sim_runtimes_size=$(get_dir_size "$SIM_RUNTIMES")

# Calculate total bytes for summary
total_bytes=0
for dir in "$DERIVED_DATA" "$IOS_DEVICE_SUPPORT" "$WATCHOS_DEVICE_SUPPORT" "$TVOS_DEVICE_SUPPORT" "$ARCHIVES" "$XCODE_CACHES" "$SIM_CACHES" "$SIM_DEVICES" "$PREVIEWS" "$SIM_RUNTIMES"; do
    bytes=$(get_dir_size_bytes "$dir")
    total_bytes=$((total_bytes + bytes))
done

echo -e "${BOLD}${CYAN}XCODE STORAGE BREAKDOWN:${NC}"
echo ""
printf "  ${YELLOW}%-35s${NC} %10s\n" "Derived Data:" "$derived_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "iOS Device Support:" "$ios_support_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "watchOS Device Support:" "$watchos_support_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "tvOS Device Support:" "$tvos_support_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "Archives:" "$archives_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "Xcode Caches:" "$xcode_cache_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "Simulator Caches:" "$sim_cache_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "Simulator Devices:" "$sim_devices_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "SwiftUI Previews:" "$previews_size"
printf "  ${YELLOW}%-35s${NC} %10s\n" "Simulator Runtimes:" "$sim_runtimes_size"
echo ""
echo -e "  ${BOLD}${GREEN}TOTAL XCODE STORAGE:${NC} ${BOLD}$(format_size $total_bytes)${NC}"
echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
