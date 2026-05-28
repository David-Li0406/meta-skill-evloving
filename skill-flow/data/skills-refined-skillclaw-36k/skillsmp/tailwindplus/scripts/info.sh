#!/bin/bash
set -euo pipefail

# Display TailwindPlus data file metadata
# Usage: ./info.sh <json_file>

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

echo "TailwindPlus Data Information"
echo "=================================================="
echo "Data file: ${DATA_FILE}"

jq -r '
  "Version: \(.version)",
  "Downloaded at: \(.downloaded_at)",
  "Component count: \(.component_count)",
  "Download duration: \(.download_duration)",
  "Downloader version: \(.downloader_version)"
' "$DATA_FILE"
