#!/bin/bash

# Add a condition to a Remote Config template
# Usage: bash add-condition.sh <template_file> <condition_name> <condition_expression> <tag_color> <output_file>

TEMPLATE="$1"
NAME="$2"
EXPRESSION="$3"
TAG_COLOR="${4:-BLUE}"
OUTPUT="$5"

if [ -z "$TEMPLATE" ] || [ -z "$NAME" ] || [ -z "$EXPRESSION" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: bash add-condition.sh <template_file> <condition_name> <condition_expression> <tag_color> <output_file>"
  echo ""
  echo "Example:"
  echo "  bash add-condition.sh template.json \"isIndiaLocation\" \"app.customSignal['country'].exactlyMatches(['IN'])\" \"INDIGO\" updated-template.json"
  exit 1
fi

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
  echo "Error: Template file '$TEMPLATE' not found"
  exit 1
fi

# Add condition using jq with proper quote handling
jq --arg name "$NAME" \
   --arg expr "$EXPRESSION" \
   --arg color "$TAG_COLOR" \
   '.conditions += [{
     "name": $name,
     "expression": $expr,
     "tagColor": $color
   }]' "$TEMPLATE" > "$OUTPUT"

if [ $? -eq 0 ]; then
  echo "✅ Condition '$NAME' added successfully"
  echo "Output: $OUTPUT"
  echo ""
  echo "New condition:"
  jq --arg name "$NAME" '.conditions[] | select(.name == $name)' "$OUTPUT"
else
  echo "❌ Failed to add condition"
  exit 1
fi
