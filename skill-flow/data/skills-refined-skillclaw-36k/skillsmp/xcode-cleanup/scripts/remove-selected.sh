#!/bin/bash
# remove-selected.sh - Remove user-selected Xcode cleanup items
# Usage: remove-selected.sh [options]
#
# Options:
#   --ios-device-support "version1" "version2" ...
#   --watchos-device-support "version1" "version2" ...
#   --ios-runtime "identifier1" "identifier2" ...
#   --visionos-runtime "identifier1" "identifier2" ...
#   --archives "date1" "date2" ...
#   --dry-run   Show what would be removed without actually removing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

DRY_RUN=false
IOS_DEVICE_SUPPORT=()
WATCHOS_DEVICE_SUPPORT=()
IOS_RUNTIMES=()
VISIONOS_RUNTIMES=()
ARCHIVES=()

# Parse arguments
current_option=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --ios-device-support)
            current_option="ios-device-support"
            shift
            ;;
        --watchos-device-support)
            current_option="watchos-device-support"
            shift
            ;;
        --ios-runtime)
            current_option="ios-runtime"
            shift
            ;;
        --visionos-runtime)
            current_option="visionos-runtime"
            shift
            ;;
        --archives)
            current_option="archives"
            shift
            ;;
        --*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            # Add to current option's array
            case $current_option in
                ios-device-support)
                    IOS_DEVICE_SUPPORT+=("$1")
                    ;;
                watchos-device-support)
                    WATCHOS_DEVICE_SUPPORT+=("$1")
                    ;;
                ios-runtime)
                    IOS_RUNTIMES+=("$1")
                    ;;
                visionos-runtime)
                    VISIONOS_RUNTIMES+=("$1")
                    ;;
                archives)
                    ARCHIVES+=("$1")
                    ;;
                *)
                    echo "Error: Value '$1' provided without a preceding option"
                    exit 1
                    ;;
            esac
            shift
            ;;
    esac
done

# Track totals
total_removed=0

echo ""
echo -e "${BOLD}${BLUE}================================================================${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${BOLD}${BLUE}                REMOVAL PREVIEW (DRY RUN)                      ${NC}"
else
    echo -e "${BOLD}${BLUE}                    REMOVING SELECTED ITEMS                    ${NC}"
fi
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo ""

# Remove iOS Device Support
if [ ${#IOS_DEVICE_SUPPORT[@]} -gt 0 ]; then
    echo -e "${BOLD}${CYAN}iOS Device Support (physical devices):${NC}"
    for version in "${IOS_DEVICE_SUPPORT[@]}"; do
        path="$HOME/Library/Developer/Xcode/iOS DeviceSupport/$version"
        if [ -d "$path" ]; then
            size=$(du -sh "$path" 2>/dev/null | cut -f1)
            if [ "$DRY_RUN" = true ]; then
                echo -e "  ${YELLOW}Would remove:${NC} $version ($size)"
            else
                rm -rf "$path"
                echo -e "  ${GREEN}Removed:${NC} $version ($size)"
            fi
        else
            echo -e "  ${RED}Not found:${NC} $version"
        fi
    done
    echo ""
fi

# Remove watchOS Device Support
if [ ${#WATCHOS_DEVICE_SUPPORT[@]} -gt 0 ]; then
    echo -e "${BOLD}${CYAN}watchOS Device Support (physical devices):${NC}"
    for version in "${WATCHOS_DEVICE_SUPPORT[@]}"; do
        path="$HOME/Library/Developer/Xcode/watchOS DeviceSupport/$version"
        if [ -d "$path" ]; then
            size=$(du -sh "$path" 2>/dev/null | cut -f1)
            if [ "$DRY_RUN" = true ]; then
                echo -e "  ${YELLOW}Would remove:${NC} $version ($size)"
            else
                rm -rf "$path"
                echo -e "  ${GREEN}Removed:${NC} $version ($size)"
            fi
        else
            echo -e "  ${RED}Not found:${NC} $version"
        fi
    done
    echo ""
fi

# Remove iOS Simulator Runtimes
if [ ${#IOS_RUNTIMES[@]} -gt 0 ]; then
    echo -e "${BOLD}${CYAN}iOS Simulator Runtimes:${NC}"
    for identifier in "${IOS_RUNTIMES[@]}"; do
        # Get runtime info before deleting
        runtime_info=$(xcrun simctl runtime list 2>/dev/null | grep "$identifier" || echo "")
        if [ -n "$runtime_info" ]; then
            if [ "$DRY_RUN" = true ]; then
                echo -e "  ${YELLOW}Would remove:${NC} $runtime_info"
            else
                if xcrun simctl runtime delete "$identifier" 2>/dev/null; then
                    echo -e "  ${GREEN}Removed:${NC} $identifier"
                else
                    echo -e "  ${RED}Failed to remove:${NC} $identifier"
                fi
            fi
        else
            echo -e "  ${RED}Not found:${NC} $identifier"
        fi
    done
    echo ""
fi

# Remove visionOS Simulator Runtimes
if [ ${#VISIONOS_RUNTIMES[@]} -gt 0 ]; then
    echo -e "${BOLD}${CYAN}visionOS Simulator Runtimes:${NC}"
    for identifier in "${VISIONOS_RUNTIMES[@]}"; do
        runtime_info=$(xcrun simctl runtime list 2>/dev/null | grep "$identifier" || echo "")
        if [ -n "$runtime_info" ]; then
            if [ "$DRY_RUN" = true ]; then
                echo -e "  ${YELLOW}Would remove:${NC} $runtime_info"
            else
                if xcrun simctl runtime delete "$identifier" 2>/dev/null; then
                    echo -e "  ${GREEN}Removed:${NC} $identifier"
                else
                    echo -e "  ${RED}Failed to remove:${NC} $identifier"
                fi
            fi
        else
            echo -e "  ${RED}Not found:${NC} $identifier"
        fi
    done
    echo ""
fi

# Remove Archives
if [ ${#ARCHIVES[@]} -gt 0 ]; then
    echo -e "${BOLD}${CYAN}Archives:${NC}"
    for date in "${ARCHIVES[@]}"; do
        path="$HOME/Library/Developer/Xcode/Archives/$date"
        if [ -d "$path" ]; then
            size=$(du -sh "$path" 2>/dev/null | cut -f1)
            if [ "$DRY_RUN" = true ]; then
                echo -e "  ${YELLOW}Would remove:${NC} $date ($size)"
            else
                rm -rf "$path"
                echo -e "  ${GREEN}Removed:${NC} $date ($size)"
            fi
        else
            echo -e "  ${RED}Not found:${NC} $date"
        fi
    done
    echo ""
fi

echo -e "${BOLD}${BLUE}================================================================${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}This was a dry run. No files were actually removed.${NC}"
    echo -e "${YELLOW}Run without --dry-run to perform actual removal.${NC}"
else
    echo -e "${GREEN}Removal complete!${NC}"
fi
echo -e "${BOLD}${BLUE}================================================================${NC}"
