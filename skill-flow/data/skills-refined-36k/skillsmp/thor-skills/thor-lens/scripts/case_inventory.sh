#!/bin/bash
# List THOR Lens case contents and statistics
#
# Usage: case_inventory.sh <case_directory>
#
# Shows:
#   - Case metadata
#   - Event count
#   - Parquet file count and size
#   - Date partitions
#   - Annotation counts

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <case_directory>"
    echo ""
    echo "Shows inventory and statistics for a THOR Lens case."
    echo ""
    echo "Example: $0 ./cases/mycase"
    exit 1
fi

CASE_DIR="$1"

echo "THOR Lens Case Inventory"
echo "========================"
echo ""

# Check case directory exists
if [ ! -d "$CASE_DIR" ]; then
    echo "ERROR: Case directory not found: $CASE_DIR"
    exit 1
fi

echo "Case directory: $CASE_DIR"

# Check meta.json
META_FILE="$CASE_DIR/meta.json"
if [ ! -f "$META_FILE" ]; then
    echo "ERROR: meta.json not found - not a valid THOR Lens case"
    exit 1
fi

echo ""
echo "Metadata (meta.json)"
echo "--------------------"
jq -r '
    "  Source file:  " + (.source_file // "unknown"),
    "  Case name:    " + (.case_name // "unknown"),
    "  Event count:  " + ((.event_count // 0) | tostring),
    "  Import time:  " + (.import_time // "unknown"),
    "  Time range:   " + ((.min_time // "?") + " to " + (.max_time // "?"))
' "$META_FILE" 2>/dev/null || echo "  (could not parse meta.json)"

# Check events directory
EVENTS_DIR="$CASE_DIR/events"
if [ ! -d "$EVENTS_DIR" ]; then
    echo ""
    echo "ERROR: events/ directory not found"
    exit 1
fi

echo ""
echo "Parquet Files (events/)"
echo "-----------------------"

# Count parquet files
PARQUET_COUNT=$(find "$EVENTS_DIR" -name "*.parquet" | wc -l | tr -d ' ')
PARQUET_SIZE=$(du -sh "$EVENTS_DIR" 2>/dev/null | cut -f1)
echo "  File count:   $PARQUET_COUNT"
echo "  Total size:   $PARQUET_SIZE"

# List date partitions
echo "  Partitions:"
find "$EVENTS_DIR" -type d -name "date=*" | sort | while read -r partition; do
    DATE=$(basename "$partition" | sed 's/date=//')
    FILES=$(find "$partition" -name "*.parquet" | wc -l | tr -d ' ')
    echo "    $DATE: $FILES files"
done

# Check annotations
ANNOTATIONS_FILE="$CASE_DIR/annotations.sqlite"
if [ -f "$ANNOTATIONS_FILE" ]; then
    echo ""
    echo "Annotations (annotations.sqlite)"
    echo "---------------------------------"
    SIZE=$(stat -f%z "$ANNOTATIONS_FILE" 2>/dev/null || stat -c%s "$ANNOTATIONS_FILE" 2>/dev/null)
    echo "  File size:    $(numfmt --to=iec-i --suffix=B $SIZE 2>/dev/null || echo "$SIZE bytes")"

    # Count annotations if sqlite3 is available
    if command -v sqlite3 &>/dev/null; then
        TAGS=$(sqlite3 "$ANNOTATIONS_FILE" "SELECT COUNT(*) FROM tags" 2>/dev/null || echo "?")
        COMMENTS=$(sqlite3 "$ANNOTATIONS_FILE" "SELECT COUNT(*) FROM comments" 2>/dev/null || echo "?")
        BOOKMARKS=$(sqlite3 "$ANNOTATIONS_FILE" "SELECT COUNT(*) FROM bookmarks" 2>/dev/null || echo "?")
        EXCLUSIONS=$(sqlite3 "$ANNOTATIONS_FILE" "SELECT COUNT(*) FROM exclusion_filters" 2>/dev/null || echo "?")

        echo "  Tags:         $TAGS"
        echo "  Comments:     $COMMENTS"
        echo "  Bookmarks:    $BOOKMARKS"
        echo "  Exclusions:   $EXCLUSIONS"
    else
        echo "  (install sqlite3 for annotation counts)"
    fi
else
    echo ""
    echo "Annotations: (not created yet)"
fi

echo ""
echo "Disk Usage"
echo "----------"
du -sh "$CASE_DIR" | awk '{print "  Total:        " $1}'

echo ""
echo "Last Modified"
echo "-------------"
if [ "$(uname)" = "Darwin" ]; then
    stat -f "  %Sm" "$META_FILE"
else
    stat -c "  %y" "$META_FILE"
fi
