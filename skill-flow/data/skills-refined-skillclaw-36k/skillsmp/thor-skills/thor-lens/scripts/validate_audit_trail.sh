#!/bin/bash
# Validate THOR v11 audit trail file before import
#
# Usage: validate_audit_trail.sh <path_to_audit_trail>
#
# Checks:
#   - File exists and is non-empty
#   - Gzip integrity (if .gz)
#   - JSONL format (first N lines parse as JSON)
#   - Basic content structure
#
# Exit codes:
#   0 = Valid audit trail
#   1 = File not found or empty
#   2 = Gzip integrity failure
#   3 = Not valid JSONL
#   4 = Wrong format (not audit trail)

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_audit_trail>"
    echo ""
    echo "Validates a THOR v11 audit trail file for THOR Lens import."
    exit 1
fi

FILE="$1"
LINES_TO_CHECK=10

echo "Validating: $FILE"
echo "---"

# Check file exists
if [ ! -f "$FILE" ]; then
    echo "ERROR: File not found: $FILE"
    exit 1
fi

# Check file is not empty
SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)
if [ "$SIZE" -eq 0 ]; then
    echo "ERROR: File is empty"
    exit 1
fi
echo "Size: $(numfmt --to=iec-i --suffix=B $SIZE 2>/dev/null || echo "$SIZE bytes")"

# Determine if gzipped
IS_GZ=0
if [[ "$FILE" == *.gz ]]; then
    IS_GZ=1
    echo "Format: Gzip compressed"

    # Check gzip integrity
    if ! gzip -t "$FILE" 2>/dev/null; then
        echo "ERROR: Gzip integrity check failed"
        exit 2
    fi
    echo "Gzip: OK"
else
    echo "Format: Plain JSONL"
fi

# Read first N lines
if [ "$IS_GZ" -eq 1 ]; then
    FIRST_LINES=$(zcat "$FILE" 2>/dev/null | head -n $LINES_TO_CHECK)
else
    FIRST_LINES=$(head -n $LINES_TO_CHECK "$FILE")
fi

# Check we got content
if [ -z "$FIRST_LINES" ]; then
    echo "ERROR: Could not read content"
    exit 3
fi

# Check each line is valid JSON
LINE_NUM=0
PARSE_ERRORS=0
while IFS= read -r line; do
    LINE_NUM=$((LINE_NUM + 1))
    if ! echo "$line" | jq -e . >/dev/null 2>&1; then
        echo "ERROR: Line $LINE_NUM is not valid JSON"
        PARSE_ERRORS=$((PARSE_ERRORS + 1))
    fi
done <<< "$FIRST_LINES"

if [ "$PARSE_ERRORS" -gt 0 ]; then
    echo "ERROR: $PARSE_ERRORS of $LINE_NUM lines failed JSON parsing"
    exit 3
fi
echo "JSON: OK (checked $LINE_NUM lines)"

# Check for audit trail structure (has 'type' and 'object' fields)
FIRST_LINE=$(echo "$FIRST_LINES" | head -1)
HAS_TYPE=$(echo "$FIRST_LINE" | jq -e 'has("type")' 2>/dev/null || echo "false")
HAS_OBJECT=$(echo "$FIRST_LINE" | jq -e 'has("object")' 2>/dev/null || echo "false")

if [ "$HAS_TYPE" != "true" ] || [ "$HAS_OBJECT" != "true" ]; then
    echo ""
    echo "WARNING: This may not be a THOR audit trail file."
    echo "  Expected fields: 'type', 'object'"
    echo "  Found: $(echo "$FIRST_LINE" | jq -c 'keys' 2>/dev/null)"
    echo ""
    echo "  Regular THOR logs have: 'level', 'message', 'module'"
    echo "  Audit trails have: 'type', 'object', 'timestamps'"
    exit 4
fi
echo "Structure: Valid audit trail format"

# Extract some stats
if [ "$IS_GZ" -eq 1 ]; then
    TOTAL_LINES=$(zcat "$FILE" 2>/dev/null | wc -l | tr -d ' ')
else
    TOTAL_LINES=$(wc -l < "$FILE" | tr -d ' ')
fi
echo "Records: $TOTAL_LINES"

# Try to extract time range
FIRST_TS=$(echo "$FIRST_LINE" | jq -r '.timestamps | to_entries[0].value // empty' 2>/dev/null | head -1)
if [ -n "$FIRST_TS" ]; then
    echo "First timestamp: $FIRST_TS"
fi

# Extract hostname if present
HOSTNAME=$(echo "$FIRST_LINE" | jq -r '.hostname // empty' 2>/dev/null)
if [ -n "$HOSTNAME" ]; then
    echo "Hostname: $HOSTNAME"
fi

echo "---"
echo "VALID: File is a valid THOR v11 audit trail"
exit 0
