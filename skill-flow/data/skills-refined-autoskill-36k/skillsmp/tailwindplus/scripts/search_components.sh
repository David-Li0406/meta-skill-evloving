#!/bin/bash
set -euo pipefail

# Search TailwindPlus components by keyword (case-insensitive, multi-word)
# Usage: ./search_components.sh <json_file> <search_term>

if [[ $# -lt 2 ]]; then
    echo "Usage: $(basename "$0") <json_file> <search_term>" >&2
    echo "Example: $(basename "$0") /path/to/data.json \"hero\"" >&2
    echo "Example: $(basename "$0") /path/to/data.json \"pricing table\"" >&2
    exit 1
fi

DATA_FILE="$1"
SEARCH_TERM="$2"

if [[ ! -f "$DATA_FILE" ]]; then
    echo "Error: File not found: $DATA_FILE" >&2
    exit 1
fi

results=$(jq -r --arg search "$SEARCH_TERM" '
  ($search | ascii_downcase | split(" ")) as $terms |
  [.tailwindplus | paths(type == "object" and has("snippets"))] |
  map(join(".")) |
  map(select(
    . as $name |
    ($name | ascii_downcase) as $lower |
    all($terms[]; . as $term | $lower | contains($term))
  )) |
  sort
' "$DATA_FILE")

count=$(echo "$results" | jq 'length')

if [[ "$count" == "0" ]]; then
    echo "No components found matching '${SEARCH_TERM}'"
    exit 0
fi

echo "Found ${count} component(s) matching '${SEARCH_TERM}':"
echo "--------------------------------------------------"
echo "$results" | jq -r '.[]' | while read -r name; do
    echo "  ${name}"
done
