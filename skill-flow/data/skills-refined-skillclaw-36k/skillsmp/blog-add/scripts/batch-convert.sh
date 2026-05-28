#!/bin/bash
# batch-convert.sh - convert multiple URLs to epub with deduplication and error handling
#
# Usage: ./batch-convert.sh <urls-file> <author> [parallel-workers]

set -euo pipefail

URLS_FILE="$1"
AUTHOR="$2"
WORKERS="${3:-4}"
EPUB_CLI="$HOME/Developer/utils/epub"
LOG_FILE="/tmp/epub-conversion-$(date +%Y%m%d-%H%M%S).log"
FAILED_FILE="/tmp/epub-conversion-failed.txt"
SUCCESS_FILE="/tmp/epub-conversion-success.txt"

if [ ! -f "$URLS_FILE" ]; then
  echo "Error: URLs file not found: $URLS_FILE"
  exit 1
fi

# init files
> "$FAILED_FILE"
> "$SUCCESS_FILE"

TOTAL=$(wc -l < "$URLS_FILE" | tr -d ' ')
echo "Converting $TOTAL URLs for author: $AUTHOR"
echo "Workers: $WORKERS"
echo "Log: $LOG_FILE"
echo ""

# deduplicate against existing library
echo "Checking for existing URLs in library..."
DEDUPED_FILE="/tmp/urls-deduped-$$.txt"
> "$DEDUPED_FILE"

cat "$URLS_FILE" | while read url; do
  if [ -z "$url" ]; then
    continue
  fi

  # Escape single quotes in URL for SQL
  ESCAPED_URL=$(echo "$url" | sed "s/'/''/g")
  EXISTS=$(sqlite3 ~/.epub/library.db "SELECT id FROM books WHERE sourceUrl = '$ESCAPED_URL'" 2>/dev/null || echo "")

  if [ -z "$EXISTS" ]; then
    echo "$url" >> "$DEDUPED_FILE"
  else
    echo "Skip (exists): $url" | tee -a "$LOG_FILE"
  fi
done

DEDUPED_COUNT=$(wc -l < "$DEDUPED_FILE" | tr -d ' ')
SKIPPED=$((TOTAL - DEDUPED_COUNT))

echo "URLs to convert: $DEDUPED_COUNT (skipped $SKIPPED existing)"
echo ""

if [ "$DEDUPED_COUNT" -eq 0 ]; then
  echo "✓ All URLs already exist in library"
  exit 0
fi

# conversion function
convert_url() {
  local url="$1"
  local author="$2"
  local log="$3"

  echo "Converting: $url" | tee -a "$log"

  if cd "$EPUB_CLI" && node ./bin/run.js url "$url" --author "$author" >> "$log" 2>&1; then
    echo "✓ $url" >> "$SUCCESS_FILE"
    echo "✓ Success: $url" | tee -a "$log"
    return 0
  else
    echo "✗ $url" >> "$FAILED_FILE"
    echo "✗ Failed: $url" | tee -a "$log"
    return 1
  fi
}

export -f convert_url
export EPUB_CLI
export LOG_FILE
export FAILED_FILE
export SUCCESS_FILE

# parallel conversion
echo "Starting parallel conversion with $WORKERS workers..."
cat "$DEDUPED_FILE" | xargs -P "$WORKERS" -I {} bash -c "convert_url '{}' '$AUTHOR' '$LOG_FILE'; sleep 1"

# summary
echo ""
echo "=== Conversion Summary ==="
SUCCESS_COUNT=$(wc -l < "$SUCCESS_FILE" 2>/dev/null | tr -d ' ' || echo 0)
FAILED_COUNT=$(wc -l < "$FAILED_FILE" 2>/dev/null | tr -d ' ' || echo 0)

echo "Total: $TOTAL URLs"
echo "Skipped (existing): $SKIPPED"
echo "Attempted: $DEDUPED_COUNT"
echo "Success: $SUCCESS_COUNT"
echo "Failed: $FAILED_COUNT"

if [ "$FAILED_COUNT" -gt 0 ]; then
  echo ""
  echo "Failed URLs saved to: $FAILED_FILE"
  echo "You can retry with:"
  echo "  ./batch-convert.sh $FAILED_FILE '$AUTHOR' $WORKERS"
fi

# post-conversion cleanup
echo ""
echo "Running post-conversion cleanup..."

# update source to backfill
sqlite3 ~/.epub/library.db "
  UPDATE books
  SET source = 'backfill'
  WHERE author = '$AUTHOR' AND source = 'url'
" 2>/dev/null || echo "⚠ Cleanup warning (non-fatal)"

# verify final count
FINAL_COUNT=$(sqlite3 ~/.epub/library.db "SELECT COUNT(*) FROM books WHERE author = '$AUTHOR'" 2>/dev/null || echo 0)
echo "✓ Total posts for $AUTHOR in library: $FINAL_COUNT"

# check for missing authors
MISSING=$(sqlite3 ~/.epub/library.db "SELECT COUNT(*) FROM books WHERE author IS NULL OR author = 'Unknown'" 2>/dev/null || echo 0)
if [ "$MISSING" -gt 0 ]; then
  echo "⚠ Warning: $MISSING books with missing/unknown author"
fi

# cleanup temp files
rm -f "$DEDUPED_FILE"

echo ""
echo "Log: $LOG_FILE"
if [ "$FAILED_COUNT" -eq 0 ]; then
  echo "✓ All conversions successful!"
  exit 0
else
  echo "⚠ Some conversions failed, check log for details"
  exit 1
fi
