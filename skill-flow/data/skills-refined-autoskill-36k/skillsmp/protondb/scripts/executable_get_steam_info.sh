#!/bin/bash
# Get Steam game information and system requirements

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <steam_app_id>"
    echo ""
    echo "Examples:"
    echo "  $0 1285190              # Get info for Borderlands 4"
    echo "  $0 1245620              # Get info for Elden Ring"
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

echo "Fetching Steam info for App ID: $APP_ID"
echo "========================================="
echo ""

# Fetch game details via ProtonDB proxy
RESPONSE=$(curl -s "https://www.protondb.com/proxy/steam/api/appdetails/?appids=${APP_ID}")

# Check if API returned valid data
SUCCESS=$(echo "$RESPONSE" | jq -r ".[\"$APP_ID\"].success")

if [ "$SUCCESS" != "true" ]; then
    echo "Error: Could not fetch Steam data for App ID $APP_ID"
    echo "This App ID may not exist or the API is unavailable"
    exit 1
fi

# Extract game data
DATA=$(echo "$RESPONSE" | jq ".[\"$APP_ID\"].data")

# Basic info
NAME=$(echo "$DATA" | jq -r '.name // "Unknown"')
TYPE=$(echo "$DATA" | jq -r '.type // "unknown"')
IS_FREE=$(echo "$DATA" | jq -r '.is_free // false')
SHORT_DESC=$(echo "$DATA" | jq -r '.short_description // "No description"')

# Platform support
WINDOWS=$(echo "$DATA" | jq -r '.platforms.windows // false')
MAC=$(echo "$DATA" | jq -r '.platforms.mac // false')
LINUX=$(echo "$DATA" | jq -r '.platforms.linux // false')

# Requirements (HTML formatted, need to parse)
MIN_REQ=$(echo "$DATA" | jq -r '.pc_requirements.minimum // "Not specified"')
REC_REQ=$(echo "$DATA" | jq -r '.pc_requirements.recommended // "Not specified"')

# Display results
echo "Game Information"
echo "----------------"
echo "Name: $NAME"
echo "Type: $TYPE"
echo "Free to Play: $IS_FREE"
echo ""

echo "Platform Support"
echo "----------------"
echo "Windows: $([ "$WINDOWS" = "true" ] && echo "Yes" || echo "No")"
echo "macOS:   $([ "$MAC" = "true" ] && echo "Yes" || echo "No")"
echo "Linux:   $([ "$LINUX" = "true" ] && echo "Yes ✓ (Native)" || echo "No (Needs Proton)")"
echo ""

echo "Description"
echo "-----------"
echo "$SHORT_DESC"
echo ""

# Parse and display system requirements
echo "System Requirements (Windows)"
echo "==============================="
echo ""

if [ "$MIN_REQ" != "Not specified" ] && [ "$MIN_REQ" != "null" ] && [ -n "$MIN_REQ" ]; then
    echo "Minimum Requirements:"
    echo "---------------------"
    # Remove HTML tags for readability
    echo "$MIN_REQ" | sed 's/<[^>]*>//g' | sed 's/&quot;/"/g' | sed 's/&amp;/\&/g'
    echo ""
fi

if [ "$REC_REQ" != "Not specified" ] && [ "$REC_REQ" != "null" ] && [ -n "$REC_REQ" ]; then
    echo "Recommended Requirements:"
    echo "-------------------------"
    echo "$REC_REQ" | sed 's/<[^>]*>//g' | sed 's/&quot;/"/g' | sed 's/&amp;/\&/g'
    echo ""
fi

# Check for Linux version
if [ "$LINUX" = "true" ]; then
    echo "Native Linux Support"
    echo "--------------------"
    echo "✓ This game has an official Linux version"
    echo "  Recommendation: Use the native version, not Proton"
    echo ""

    # Check for Linux-specific requirements if available
    LINUX_REQ=$(echo "$DATA" | jq -r '.linux_requirements.minimum // null')
    if [ "$LINUX_REQ" != "null" ] && [ -n "$LINUX_REQ" ]; then
        echo "Linux Requirements:"
        echo "$LINUX_REQ" | sed 's/<[^>]*>//g'
        echo ""
    fi
fi

# Additional info
echo "Additional Information"
echo "----------------------"

# Developers
DEVS=$(echo "$DATA" | jq -r '.developers[]? // empty' | paste -sd ", " -)
if [ -n "$DEVS" ]; then
    echo "Developers: $DEVS"
fi

# Publishers
PUBS=$(echo "$DATA" | jq -r '.publishers[]? // empty' | paste -sd ", " -)
if [ -n "$PUBS" ]; then
    echo "Publishers: $PUBS"
fi

# Release date
RELEASE_DATE=$(echo "$DATA" | jq -r '.release_date.date // "Unknown"')
echo "Release Date: $RELEASE_DATE"

# Genres
GENRES=$(echo "$DATA" | jq -r '.genres[]?.description // empty' | paste -sd ", " -)
if [ -n "$GENRES" ]; then
    echo "Genres: $GENRES"
fi

echo ""
echo "Store Page:"
echo "  https://store.steampowered.com/app/$APP_ID"
echo ""
echo "Check ProtonDB compatibility:"
echo "  scripts/check_game.sh $APP_ID"
