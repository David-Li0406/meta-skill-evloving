#!/bin/bash
# Get regional search statistics from Yandex Wordstat

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Defaults
PHRASE=""
REGION_TYPE="all"
DEVICES="all"

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --phrase|-p) PHRASE="$2"; shift 2 ;;
        --region-type|-t) REGION_TYPE="$2"; shift 2 ;;
        --devices|-d) DEVICES="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "$PHRASE" ]]; then
    echo "Usage: regions_stats.sh --phrase \"search query\" [options]"
    echo ""
    echo "Options:"
    echo "  --phrase, -p       Search phrase (required)"
    echo "  --region-type, -t  Filter: cities, regions, all (default: all)"
    echo "  --devices, -d      Device filter: all, desktop, phone, tablet (default: all)"
    echo ""
    echo "Examples:"
    echo "  bash scripts/regions_stats.sh --phrase \"юрист дтп\""
    echo "  bash scripts/regions_stats.sh --phrase \"юрист\" --region-type cities"
    exit 1
fi

load_config

# Escape phrase for JSON
PHRASE_ESCAPED=$(json_escape "$PHRASE")

# Build JSON params
PARAMS="{\"phrase\":\"$PHRASE_ESCAPED\""

if [[ "$REGION_TYPE" != "all" ]]; then
    PARAMS="$PARAMS,\"regionType\":\"$REGION_TYPE\""
fi

if [[ "$DEVICES" != "all" ]]; then
    PARAMS="$PARAMS,\"devices\":\"$DEVICES\""
fi

PARAMS="$PARAMS}"

echo "=== Yandex Wordstat: Regional Statistics ==="
echo "Phrase: $PHRASE"
echo "Region type: $REGION_TYPE"
echo "Devices: $DEVICES"
echo ""
echo "Fetching data..."

result=$(wordstat_request "regions" "$PARAMS")

# Check for error
if echo "$result" | grep -q '"error"'; then
    echo "Error:"
    echo "$result"
    exit 1
fi

echo ""
echo "=== Top 30 Regions ==="
echo ""

echo "| Region ID | Count | Affinity |"
echo "|-----------|-------|----------|"

# Extract regions data (top 30) - sort by count descending
count=0
echo "$result" | grep -o '"regionId":[0-9]*,"count":[0-9]*' | sort -t: -k3 -rn | head -30 | while IFS= read -r entry; do
    count=$((count + 1))

    region_id=$(echo "$entry" | grep -o '"regionId":[0-9]*' | sed 's/"regionId"://')
    cnt=$(echo "$entry" | grep -o '"count":[0-9]*' | sed 's/"count"://')

    echo "| $region_id | $(format_number "$cnt") |"
done

echo ""
echo "Note: Use search_region.sh --name \"City\" to find region names"
echo ""
echo "=== Raw JSON (first 2000 chars) ==="
echo "$result" | head -c 2000
echo ""
echo "[truncated]"
