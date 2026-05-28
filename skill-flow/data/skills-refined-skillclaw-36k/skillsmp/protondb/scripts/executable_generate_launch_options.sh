#!/bin/bash
# Generate launch options from actual ProtonDB user reports

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <steam_app_id> [--amd-only] [--wayland-only]"
    echo ""
    echo "Fetches launch options from ProtonDB user reports and suggests"
    echo "configurations that actually work for the community."
    echo ""
    echo "Options:"
    echo "  --amd-only      Filter for AMD GPU users only"
    echo "  --wayland-only  Filter for Wayland users only"
    echo ""
    echo "Examples:"
    echo "  $0 1285190                    # All reports for Borderlands 4"
    echo "  $0 1245620 --amd-only         # AMD-specific for Elden Ring"
    echo "  $0 892970 --amd-only --wayland-only  # AMD+Wayland for Valheim"
    exit 1
fi

APP_ID="$1"
AMD_ONLY=false
WAYLAND_ONLY=false

# Parse flags
shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --amd-only)
            AMD_ONLY=true
            shift
            ;;
        --wayland-only)
            WAYLAND_ONLY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed"
    echo "Install with: sudo pacman -S jq"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    echo "Error: curl is required but not installed"
    echo "Install with: sudo pacman -S curl"
    exit 1
fi

echo "ProtonDB Launch Options from User Reports"
echo "=========================================="
echo ""
echo "Fetching reports for App ID: $APP_ID"
if [ "$AMD_ONLY" = true ]; then
    echo "Filter: AMD GPUs only"
fi
if [ "$WAYLAND_ONLY" = true ]; then
    echo "Filter: Wayland only"
fi
echo ""

# Try community API first (may be unavailable)
echo "Attempting to fetch community reports..."
REPORTS=$(curl -s -f "https://protondb-community-api.fly.dev/reports?appId=${APP_ID}&limit=100" 2>/dev/null || echo "")

if [ -z "$REPORTS" ] || [ "$REPORTS" = "null" ]; then
    echo "⚠ Community API unavailable or no reports found"
    echo ""
    echo "Fallback: Check ProtonDB website manually"
    echo "  https://www.protondb.com/app/$APP_ID"
    echo ""
    echo "Look for reports with:"
    echo "  - AMD GPU (Radeon RX 6000/7000 series)"
    echo "  - Arch Linux or similar rolling release"
    echo "  - Recent dates (< 3 months old)"
    echo "  - Platinum/Gold ratings"
    echo ""
    echo "Common environment variables to try:"
    echo "-----------------------------------"
    echo ""
    echo "Base AMD + Wayland configuration:"
    echo "  AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco DXVK_ASYNC=1 SDL_VIDEODRIVER=wayland %command%"
    echo ""
    echo "If DirectX 12 game:"
    echo "  Add: VKD3D_CONFIG=dxr11"
    echo ""
    echo "If shader stutter:"
    echo "  Ensure: DXVK_ASYNC=1 (already included above)"
    echo ""
    echo "If window focus issues:"
    echo "  Try: gamescope -f -- (before other env vars)"
    echo ""
    echo "If compatibility issues:"
    echo "  Try: PROTON_USE_WINED3D=1 SDL_VIDEODRIVER=x11"
    echo ""
    exit 0
fi

# Parse reports
REPORT_COUNT=$(echo "$REPORTS" | jq -r '.reports | length')

if [ "$REPORT_COUNT" -eq 0 ]; then
    echo "No reports found for this game"
    exit 0
fi

echo "Found $REPORT_COUNT reports"
echo ""

# Extract and analyze launch options
echo "Analyzing user configurations..."
echo ""

# Create temporary file for analysis
TEMP_FILE=$(mktemp)
trap "rm -f \"$TEMP_FILE\"" EXIT

# Extract relevant data from reports
echo "$REPORTS" | jq -r '.reports[] |
    select(.tier == "platinum" or .tier == "gold") |
    {
        tier: .tier,
        protonVersion: .protonVersion,
        gpu: .gpu,
        os: .os,
        notes: .notes,
        specs: .specs
    }' > "$TEMP_FILE"

# Filter for AMD if requested
if [ "$AMD_ONLY" = true ]; then
    FILTERED=$(jq 'select(.gpu | test("AMD|Radeon"; "i"))' "$TEMP_FILE")
    echo "$FILTERED" > "$TEMP_FILE"
fi

# Filter for Wayland if requested
if [ "$WAYLAND_ONLY" = true ]; then
    FILTERED=$(jq 'select(.notes | test("wayland"; "i"))' "$TEMP_FILE")
    echo "$FILTERED" > "$TEMP_FILE"
fi

FILTERED_COUNT=$(jq -s 'length' "$TEMP_FILE")

if [ "$FILTERED_COUNT" -eq 0 ]; then
    echo "No reports match your filters"
    echo "Try without --amd-only or --wayland-only"
    exit 0
fi

echo "Found $FILTERED_COUNT Platinum/Gold reports matching filters"
echo ""

# Extract environment variables and launch options from notes
echo "Common Configuration Patterns"
echo "=============================="
echo ""

# Parse environment variables from notes
ENV_VARS=$(jq -r '.notes' "$TEMP_FILE" | grep -oE '(AMD_VULKAN_ICD|RADV_PERFTEST|DXVK_ASYNC|VKD3D_CONFIG|SDL_VIDEODRIVER|PROTON_[A-Z_]+|mesa_glthread|vblank_mode)=[^ ]+' | sort | uniq -c | sort -rn || echo "")

if [ -n "$ENV_VARS" ]; then
    echo "Environment Variables (by frequency):"
    echo "--------------------------------------"
    echo "$ENV_VARS" | head -20
    echo ""
fi

# Extract Proton versions
echo "Proton Versions Used:"
echo "---------------------"
jq -r '.protonVersion' "$TEMP_FILE" | sort | uniq -c | sort -rn | head -10
echo ""

# Highlight Proton-GE versions specifically
echo "Proton-GE Versions:"
echo "-------------------"
GE_VERSIONS=$(jq -r '.protonVersion' "$TEMP_FILE" 2>/dev/null | \
    grep -iE "GE-Proton|Proton-GE" | sort | uniq -c | sort -rn)

if [ -n "$GE_VERSIONS" ]; then
    echo "$GE_VERSIONS"
    echo ""

    MOST_COMMON_GE=$(echo "$GE_VERSIONS" | head -1 | awk '{print $2}')
    USAGE_COUNT=$(echo "$GE_VERSIONS" | head -1 | awk '{print $1}')

    echo "Most commonly used: $MOST_COMMON_GE ($USAGE_COUNT reports)"
    echo ""
    echo "Install this version:"
    echo "  scripts/manage_proton_ge.sh install $MOST_COMMON_GE"
else
    echo "No Proton-GE versions found in filtered reports"
    echo ""
    echo "Consider trying latest Proton-GE:"
    echo "  scripts/manage_proton_ge.sh install"
fi

echo ""

# Extract GPU models
echo "GPU Models in Reports:"
echo "----------------------"
jq -r '.gpu' "$TEMP_FILE" | sort | uniq -c | sort -rn | head -10
echo ""

# Try to construct recommended launch options
echo "Recommended Launch Options"
echo "=========================="
echo ""

# Count most common environment variables
MOST_COMMON_VARS=$(echo "$ENV_VARS" | head -10 | awk '{print $2}' | tr '\n' ' ')

if [ -n "$MOST_COMMON_VARS" ]; then
    echo "Based on successful user reports:"
    echo "---------------------------------"
    echo "$MOST_COMMON_VARS %command%"
    echo ""
    echo "Note: Review the environment variables above and adjust as needed"
    echo ""
    echo "Optional additions:"
    echo "  gamemoderun - CPU governor optimization"
    echo "  mangohud - Performance overlay"
else
    echo "Could not extract specific launch options from reports"
    echo ""
    echo "Generic AMD + Wayland recommendation:"
    echo "AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco DXVK_ASYNC=1 SDL_VIDEODRIVER=wayland %command%"
fi

echo ""
echo "Detailed Report Excerpts"
echo "========================"
echo ""

# Show snippets from top reports
jq -r 'select(.notes != null and .notes != "") |
    "GPU: \(.gpu)\n" +
    "OS: \(.os)\n" +
    "Proton: \(.protonVersion)\n" +
    "Rating: \(.tier)\n" +
    "Notes: \(.notes)\n" +
    "---"' "$TEMP_FILE" | head -50

echo ""
echo "Full Report Details"
echo "==================="
echo "Visit ProtonDB for complete reports and discussions:"
echo "  https://www.protondb.com/app/$APP_ID"
echo ""
echo "Filter ProtonDB by:"
echo "  - GPU: AMD Radeon"
echo "  - Distribution: Arch Linux"
echo "  - Rating: Platinum, Gold"
echo "  - Date: Last 3 months"
