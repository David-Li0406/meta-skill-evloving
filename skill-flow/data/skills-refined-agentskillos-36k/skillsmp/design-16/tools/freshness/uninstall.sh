#!/bin/bash
#
# uninstall.sh - Remove Design Ops freshness system
#
# Usage: ./tools/freshness/uninstall.sh [--keep-data]

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.designops.freshness.plist"

KEEP_DATA=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-data)
            KEEP_DATA=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--keep-data]"
            echo ""
            echo "Options:"
            echo "  --keep-data    Keep freshness data (only remove schedule)"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

echo ""
echo -e "${CYAN}Uninstalling Design Ops Freshness System...${NC}"
echo ""

# ============================================================================
# Step 1: Unload and remove launchd plist
# ============================================================================
echo -e "${YELLOW}[1/2] Removing launchd schedule...${NC}"

PLIST_FILE="$LAUNCH_AGENTS_DIR/$PLIST_NAME"

if [[ -f "$PLIST_FILE" ]]; then
    launchctl unload "$PLIST_FILE" 2>/dev/null || true
    rm "$PLIST_FILE"
    echo -e "${GREEN}  ✓ Removed launchd plist${NC}"
else
    echo "  Plist not found, skipping"
fi

# ============================================================================
# Step 2: Remove data (optional)
# ============================================================================
if [[ "$KEEP_DATA" == "false" ]]; then
    echo -e "${YELLOW}[2/2] Removing freshness data...${NC}"

    # Confirm
    echo -n "  Remove all freshness data? (y/N) "
    read -r confirm

    if [[ "$confirm" == "y" ]] || [[ "$confirm" == "Y" ]]; then
        rm -rf "$DESIGN_OPS_ROOT/docs/freshness"
        rm -f "$DESIGN_OPS_ROOT/config/.last-freshness-scan"
        echo -e "${GREEN}  ✓ Removed freshness data${NC}"
    else
        echo "  Keeping freshness data"
    fi
else
    echo -e "${YELLOW}[2/2] Keeping freshness data (--keep-data)${NC}"
fi

echo ""
echo -e "${GREEN}Uninstall complete.${NC}"
echo ""
echo "Note: Source registry (config/source-registry.yaml) was preserved."
echo "Delete manually if no longer needed."
