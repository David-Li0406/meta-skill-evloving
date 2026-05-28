#!/bin/bash
set -euo pipefail

# List all TailwindPlus components organized by category
# Usage: ./list_components.sh <json_file>

if [[ $# -lt 1 ]]; then
    echo "Usage: $(basename "$0") <json_file>" >&2
    echo "Example: $(basename "$0") /path/to/tailwindplus-components-*.json" >&2
    exit 1
fi

DATA_FILE="$1"

if [[ ! -f "$DATA_FILE" ]]; then
    echo "Error: File not found: $DATA_FILE" >&2
    exit 1
fi

# Get total count and list components grouped by category
jq -r '
  .component_count as $total |
  [.tailwindplus | paths(type == "object" and has("snippets"))] |
  group_by(.[0]) |
  "TailwindPlus Components (\($total) total):",
  "--------------------------------------------------",
  (.[] |
    .[0][0] as $category |
    (. | length) as $count |
    "\n## \($category) (\($count) components)",
    (.[] | "  - " + (.[1:] | join(".")))
  )
' "$DATA_FILE"
