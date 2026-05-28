#!/usr/bin/env bash
set -euo pipefail

# Usage: validate-design-doc.sh <file-path>
# Exit codes: 0 = valid, 1 = invalid

FILE="$1"

# Extract module from path: .claude/design/{module}/{file}.md
MODULE=$(echo "$FILE" | sed -n 's|.claude/design/\([^/]*\)/.*|\1|p')

if [[ -z "$MODULE" ]]; then
  echo "Error: Could not extract module from path: $FILE" >&2
  exit 1
fi

# Extract filename
FILENAME=$(basename "$FILE")

# Skip design.config.json
if [[ "$FILENAME" == "design.config.json" ]]; then
  echo "⏭️  Skipped: $FILE (config file)"
  exit 0
fi

# Check if file exists
if [[ ! -f "$FILE" ]]; then
  echo "Error: File not found: $FILE" >&2
  exit 1
fi

# Validate frontmatter exists
if ! grep -q "^---" "$FILE"; then
  echo "Error: Missing frontmatter in $FILE" >&2
  exit 1
fi

# Extract and validate required fields (between the two --- markers)
# Use awk to extract frontmatter (works on both GNU and BSD)
FRONTMATTER=$(awk 'BEGIN{found=0} /^---$/{found++; next} found==1{print} found==2{exit}' "$FILE")

REQUIRED_FIELDS=("status" "module" "category" "created" "updated" "last-synced" "completeness")
for field in "${REQUIRED_FIELDS[@]}"; do
  if ! echo "$FRONTMATTER" | grep -q "^$field:"; then
    echo "Error: Missing required field '$field' in $FILE" >&2
    exit 1
  fi
done

# Validate status value
STATUS=$(echo "$FRONTMATTER" | grep "^status:" | awk '{print $2}')
VALID_STATUSES=("stub" "draft" "current" "archived")
STATUS_VALID=0
for valid_status in "${VALID_STATUSES[@]}"; do
  if [[ "$STATUS" == "$valid_status" ]]; then
    STATUS_VALID=1
    break
  fi
done
if [[ "$STATUS_VALID" -eq 0 ]]; then
  echo "Error: Invalid status '$STATUS' in $FILE" >&2
  echo "Valid values: ${VALID_STATUSES[*]}" >&2
  exit 1
fi

# Validate completeness is 0-100
COMPLETENESS=$(echo "$FRONTMATTER" | grep "^completeness:" | awk '{print $2}')
if [[ ! "$COMPLETENESS" =~ ^[0-9]+$ ]] || [[ "$COMPLETENESS" -lt 0 ]] || [[ "$COMPLETENESS" -gt 100 ]]; then
  echo "Error: Invalid completeness '$COMPLETENESS' in $FILE (must be 0-100)" >&2
  exit 1
fi

# Success
echo "✅ Validated: $FILE"
exit 0
