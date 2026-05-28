#!/bin/bash
set -euo pipefail

# files-to-items.sh - Parse markdown files back to Item JSON
#
# Usage: files-to-items.sh <dir>
#
# Reads all .md files in dir, extracts frontmatter and response yaml,
# outputs JSON array of items to stdout

DIR="${1:?Usage: files-to-items.sh <dir>}"

# Check directory exists
if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory not found: $DIR" >&2
  exit 1
fi

# Process all .md files
echo "["
first=true
for file in "$DIR"/*.md; do
  [[ -e "$file" ]] || continue

  if [[ "$first" == "true" ]]; then
    first=false
  else
    echo ","
  fi

  # Extract frontmatter (between --- markers)
  FRONTMATTER=$(awk '/^---$/{if(f)exit;f=1;next}f' "$file")

  # Extract response yaml (between ```yaml and ``` in # Response section)
  RESPONSE_YAML=$(awk '/^# Response/,/^# /{
    if(/^```yaml$/){f=1;next}
    if(/^```$/){f=0}
    if(f)print
  }' "$file")

  # Parse frontmatter with yq/python
  ITEM=$(echo "$FRONTMATTER" | python3 -c '
import sys, json, yaml
data = yaml.safe_load(sys.stdin.read())
print(json.dumps(data))
')

  # Parse response yaml
  RESPONSE=$(echo "$RESPONSE_YAML" | python3 -c '
import sys, json, yaml
data = yaml.safe_load(sys.stdin.read()) or {}
print(json.dumps(data))
')

  # Combine into item structure
  echo "$ITEM" | jq --argjson response "$RESPONSE" '. + {response: $response}'

done
echo "]"
