#!/usr/bin/env bash
set -euo pipefail

# Usage: update-timestamp.sh <file-path>
# Updates the 'updated' field in frontmatter to current date

FILE="$1"
TODAY=$(date +%Y-%m-%d)

# Extract filename
FILENAME=$(basename "$FILE")

# Skip design.config.json
if [[ "$FILENAME" == "design.config.json" ]]; then
  exit 0
fi

# Check if file exists
if [[ ! -f "$FILE" ]]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

# Check if frontmatter exists
if ! grep -q "^---" "$FILE"; then
  echo "Error: Missing frontmatter in $FILE" >&2
  exit 1
fi

# Check if 'updated' field exists
if ! grep -q "^updated:" "$FILE"; then
  echo "Error: Missing 'updated' field in $FILE" >&2
  exit 1
fi

# Get current updated value
CURRENT_UPDATED=$(grep "^updated:" "$FILE" | awk '{print $2}')

# Only update if different from today
if [[ "$CURRENT_UPDATED" == "$TODAY" ]]; then
  exit 0
fi

# Update the 'updated' field using sed (compatible with both GNU and BSD sed)
if sed --version >/dev/null 2>&1; then
  # GNU sed
  sed -i "s/^updated: .*/updated: $TODAY/" "$FILE"
else
  # BSD sed (macOS)
  sed -i '' "s/^updated: .*/updated: $TODAY/" "$FILE"
fi

echo "✅ Updated timestamp in $FILE to $TODAY"
exit 0
