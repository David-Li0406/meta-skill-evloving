#!/bin/bash
# Check ProtonDB rating and game compatibility

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <steam_app_id>"
    echo ""
    echo "Examples:"
    echo "  $0 1285190              # Check Borderlands 4"
    echo "  $0 1245620              # Check Elden Ring"
    exit 1
fi

APP_ID="$1"

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

echo "Checking ProtonDB for App ID: $APP_ID"
echo "========================================="
echo ""

# Fetch ProtonDB summary
SUMMARY=$(curl -s "https://www.protondb.com/api/v1/reports/summaries/${APP_ID}.json")

# Check if API returned data
if [ -z "$SUMMARY" ] || [ "$SUMMARY" = "null" ]; then
    echo "Error: No ProtonDB data found for App ID $APP_ID"
    echo "This game may not be in the ProtonDB database yet."
    exit 1
fi

# Extract fields
TIER=$(echo "$SUMMARY" | jq -r '.tier // "unknown"')
CONFIDENCE=$(echo "$SUMMARY" | jq -r '.confidence // "unknown"')
SCORE=$(echo "$SUMMARY" | jq -r '.score // "0"')
TOTAL_REPORTS=$(echo "$SUMMARY" | jq -r '.total // "0"')
BEST_TIER=$(echo "$SUMMARY" | jq -r '.bestReportedTier // "unknown"')
TRENDING_TIER=$(echo "$SUMMARY" | jq -r '.trendingTier // "unknown"')

# Display results
echo "ProtonDB Rating"
echo "---------------"
echo "Overall Tier:    $TIER"
echo "Best Tier:       $BEST_TIER"
echo "Trending:        $TRENDING_TIER"
echo "Score:           $SCORE"
echo "Confidence:      $CONFIDENCE"
echo "Total Reports:   $TOTAL_REPORTS"
echo ""

# Rating interpretation
echo "Tier Meanings"
echo "-------------"
case "$TIER" in
    "native")
        echo "✓ Native Linux Support - Official Linux version available"
        echo "  Recommendation: Use native version, not Proton"
        ;;
    "platinum")
        echo "✓ Platinum - Works perfectly out of the box"
        echo "  Recommendation: Should work with Proton Stable"
        ;;
    "gold")
        echo "✓ Gold - Works with minor tweaks"
        echo "  Recommendation: Check launch options on ProtonDB"
        ;;
    "silver")
        echo "⚠ Silver - Runs with workarounds"
        echo "  Recommendation: Check ProtonDB for required configuration"
        ;;
    "bronze")
        echo "⚠ Bronze - Runs poorly with significant issues"
        echo "  Recommendation: May not be worth playing on Linux"
        ;;
    "borked")
        echo "✗ Borked - Does not run"
        echo "  Recommendation: Not playable on Linux currently"
        ;;
    *)
        echo "? Unknown tier: $TIER"
        ;;
esac
echo ""

# Confidence interpretation
echo "Confidence Level"
echo "----------------"
case "$CONFIDENCE" in
    "strong")
        echo "Strong confidence - $TOTAL_REPORTS reports, very reliable"
        ;;
    "moderate")
        echo "Moderate confidence - $TOTAL_REPORTS reports, fairly reliable"
        ;;
    "weak")
        echo "Weak confidence - $TOTAL_REPORTS reports, limited data"
        ;;
    *)
        echo "Unknown confidence level"
        ;;
esac
echo ""

# Quick recommendation
echo "Quick Recommendation"
echo "--------------------"

if [ "$TIER" = "native" ]; then
    echo "Use the native Linux version (don't use Proton)"
elif [ "$TIER" = "platinum" ] || [ "$TIER" = "gold" ]; then
    echo "Should work well on Linux!"
    echo "Suggested Proton: Stable or Experimental"
    echo "Check ProtonDB for optimal launch options"
elif [ "$TIER" = "silver" ]; then
    echo "Playable but may need configuration"
    echo "Suggested Proton: Try Experimental or Proton-GE"
    echo "Check ProtonDB for required workarounds"
    echo ""
    echo "Proton-GE Recommendation"
    echo "------------------------"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    MANAGER_SCRIPT="$SCRIPT_DIR/manage_proton_ge.sh"

    if [ -f "$MANAGER_SCRIPT" ] && [ -x "$MANAGER_SCRIPT" ]; then
        "$MANAGER_SCRIPT" get-recommended "$APP_ID" 2>/dev/null || {
            echo "Install Proton-GE for better compatibility:"
            echo "  scripts/manage_proton_ge.sh install"
        }
    else
        echo "Suggested: Install Proton-GE for better compatibility"
        echo ""
        echo "Proton-GE includes:"
        echo "  - Additional game-specific patches"
        echo "  - Video codec support"
        echo "  - Faster compatibility updates"
        echo ""
        echo "Install with: scripts/manage_proton_ge.sh install"
    fi
elif [ "$TIER" = "bronze" ] || [ "$TIER" = "borked" ]; then
    echo "Not recommended for Linux gaming"
    echo "Check ProtonDB for any recent improvements"
else
    echo "Unable to determine recommendation"
fi

echo ""
echo "View full reports:"
echo "  https://www.protondb.com/app/$APP_ID"
echo ""
echo "Get Steam info:"
echo "  scripts/get_steam_info.sh $APP_ID"
