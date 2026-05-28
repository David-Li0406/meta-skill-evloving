#!/bin/sh
# Search Iconify for icons
# Usage: search-icons.sh <search-term> [limit]
#
# Examples:
#   search-icons.sh "health sync"
#   search-icons.sh "fitness" 20

set -e

SEARCH_TERM="${1:?Usage: search-icons.sh <search-term> [limit]}"
LIMIT="${2:-10}"

# URL encode the search term
ENCODED_TERM=$(printf "%s" "$SEARCH_TERM" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))")

printf "=== Searching Iconify for: %s ===\n\n" "$SEARCH_TERM"

# Create temp file for API response
RESPONSE_FILE=$(mktemp)
trap 'rm -f "$RESPONSE_FILE"' EXIT

# Fetch from API
printf "Fetching results...\n"
HTTP_CODE=$(curl -s -w "%{http_code}" -o "$RESPONSE_FILE" \
    "https://api.iconify.design/search?query=${ENCODED_TERM}&limit=${LIMIT}")

# Check HTTP status
if [ "$HTTP_CODE" != "200" ]; then
    printf "Error: API returned HTTP %s\n" "$HTTP_CODE"
    exit 1
fi

# Validate JSON before parsing
if ! python3 -c "import json; json.load(open('$RESPONSE_FILE'))" 2>/dev/null; then
    printf "Error: API returned invalid JSON\n"
    cat "$RESPONSE_FILE"  # Show response for debugging
    exit 1
fi

# Process valid response
python3 - "$RESPONSE_FILE" << 'PYEOF'
import json, sys

with open(sys.argv[1]) as f:
    data = json.load(f)

icons = data.get('icons', [])
collections = data.get('collections', {})

if not icons:
    print("No icons found.")
    sys.exit(0)

print(f"Found {data.get('total', len(icons))} icons (showing {len(icons)}):\n")

for i, icon in enumerate(icons, 1):
    parts = icon.split(':')
    collection_id = parts[0]
    icon_name = parts[1] if len(parts) > 1 else ''

    collection_info = collections.get(collection_id, {})
    collection_name = collection_info.get('name', collection_id)
    license_info = collection_info.get('license', {})
    license_name = license_info.get('title', 'Unknown')

    print(f"{i}. {icon}")
    print(f"   Collection: {collection_name}")
    print(f"   License: {license_name}")
    print(f"   Preview: https://icon-sets.iconify.design/{collection_id}/{icon_name}/")
    print()

if icons:
    print("\nTo generate icons, run:")
    print(f"  generate-app-icons.sh {icons[0]}")
PYEOF
