#!/bin/bash
# Get top search phrases from Yandex Wordstat

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Defaults
PHRASE=""
REGIONS=""
DEVICES="all"

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --phrase|-p) PHRASE="$2"; shift 2 ;;
        --regions|-r) REGIONS="$2"; shift 2 ;;
        --devices|-d) DEVICES="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "$PHRASE" ]]; then
    echo "Usage: top_requests.sh --phrase \"search query\" [options]"
    echo ""
    echo "Options:"
    echo "  --phrase, -p   Search phrase (required)"
    echo "  --regions, -r  Region IDs, comma-separated (optional)"
    echo "  --devices, -d  Device filter: all, desktop, phone, tablet (default: all)"
    echo ""
    echo "Examples:"
    echo "  bash scripts/top_requests.sh --phrase \"юрист по дтп\""
    echo "  bash scripts/top_requests.sh --phrase \"юрист дтп\" --regions \"1,2\""
    echo "  bash scripts/top_requests.sh --phrase \"\\\"!юрист !по !дтп\\\"\" --devices phone"
    exit 1
fi

load_config

# Escape phrase for JSON
PHRASE_ESCAPED=$(json_escape "$PHRASE")

# Build JSON params
PARAMS="{\"phrase\":\"$PHRASE_ESCAPED\""

if [[ -n "$REGIONS" ]]; then
    PARAMS="$PARAMS,\"regions\":[$REGIONS]"
fi

if [[ "$DEVICES" != "all" ]]; then
    PARAMS="$PARAMS,\"devices\":\"$DEVICES\""
fi

PARAMS="$PARAMS}"

echo "=== Yandex Wordstat: Top Requests ==="
echo "Phrase: $PHRASE"
[[ -n "$REGIONS" ]] && echo "Regions: $REGIONS"
echo "Devices: $DEVICES"
echo ""
echo "Fetching data..."

result=$(wordstat_request "topRequests" "$PARAMS")

# Check for error
if echo "$result" | grep -q '"error"'; then
    echo "Error:"
    echo "$result"
    exit 1
fi

echo ""
echo "=== Results ==="
echo ""

# Parse and display results
echo "| # | Phrase | Impressions |"
echo "|---|--------|-------------|"

count=0
# Extract phrase-count pairs
echo "$result" | grep -o '{"phrase":"[^"]*","count":[0-9]*}' | while IFS= read -r entry; do
    count=$((count + 1))

    phrase=$(echo "$entry" | grep -o '"phrase":"[^"]*"' | sed 's/"phrase":"//' | tr -d '"')
    shows=$(echo "$entry" | grep -o '"count":[0-9]*' | sed 's/"count"://')

    echo "| $count | $phrase | $(format_number "$shows") |"
done

echo ""
echo "=== Raw JSON ==="
echo "$result" | head -c 2000
echo ""
echo "[truncated if > 2000 chars]"
