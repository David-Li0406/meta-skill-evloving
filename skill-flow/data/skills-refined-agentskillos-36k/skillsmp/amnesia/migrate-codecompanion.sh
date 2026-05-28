#!/usr/bin/env bash
#
# Migrate codecompanion-history summaries to amnesia database
#

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SUMMARIES_DIR="${1:-$HOME/codecompanion-history/summaries}"

# Check summaries directory exists
if [[ ! -d "$SUMMARIES_DIR" ]]; then
    echo "ERROR: Summaries directory not found: $SUMMARIES_DIR"
    echo "Usage: $0 [/path/to/summaries]"
    exit 1
fi

# Count files
COUNT=$(find "$SUMMARIES_DIR" -name "*.md" -type f | wc -l | tr -d ' ')
echo "Found $COUNT markdown files in $SUMMARIES_DIR"
echo ""

# Process each file
IMPORTED=0
for file in "$SUMMARIES_DIR"/*.md; do
    [[ -f "$file" ]] || continue
    
    filename=$(basename "$file")
    id="${filename%.md}"
    
    # Extract title (first # heading)
    title=$(grep -m1 "^# " "$file" | sed 's/^# //' || echo "Untitled")
    
    # Read full content as summary (these files ARE summaries)
    content=$(cat "$file")
    
    # Skip empty files
    [[ -z "$content" ]] && continue
    
    # Extract tags from content if present (look for ## Tags section)
    tags=$(grep -A1 "^## Tags" "$file" 2>/dev/null | tail -1 | tr -d ' ' || echo "")
    
    # If no tags section, try to infer from content
    if [[ -z "$tags" ]]; then
        tags="imported,codecompanion"
    else
        tags="$tags,imported"
    fi
    
    echo "Importing: $title ($id)"
    
    # Save to amnesia (content is the summary, no full_content for imported ones)
    echo "$content" | "$SCRIPT_DIR/save.sh" --title "$title" --tags "$tags" --id "cc_$id" 2>/dev/null
    
    ((IMPORTED++))
done

echo ""
echo "Migration complete: $IMPORTED memories imported"
