#!/bin/bash
TEMPLATE="$1"

echo "Parameters:"
# Handle both old format (.parameters) and new format (.parameterGroups)
if jq -e '.parameterGroups' "$TEMPLATE" > /dev/null 2>&1; then
  jq -r '.parameterGroups | to_entries[] | .key as $group | .value.parameters | keys[] | "  [\($group)] \(.)"' "$TEMPLATE"
elif jq -e '.parameters' "$TEMPLATE" > /dev/null 2>&1; then
  jq -r '.parameters | keys[]' "$TEMPLATE"
else
  echo "  (none)"
fi

echo ""
echo "Conditions:"
jq -r '.conditions[]?.name // empty' "$TEMPLATE"
