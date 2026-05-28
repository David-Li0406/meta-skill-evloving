#!/bin/bash
# migrate-to-folders.sh - migrate existing blog posts to year/month folder structure
#
# Usage: ./migrate-to-folders.sh [--dry-run]

set -euo pipefail

DRY_RUN=false
if [ "${1:-}" = "--dry-run" ]; then
  DRY_RUN=true
  echo "=== DRY RUN MODE ==="
  echo ""
fi

DEVICE_IP="10.0.0.61"
DB="$HOME/.epub/library.db"

# Get all blog posts (feed:* and backfill sources)
BLOG_POSTS=$(sqlite3 "$DB" "
  SELECT id, title, author, source_url, file_path, source
  FROM books
  WHERE source LIKE 'feed:%' OR source = 'backfill'
  ORDER BY author, source_url
")

if [ -z "$BLOG_POSTS" ]; then
  echo "No blog posts found to migrate"
  exit 0
fi

TOTAL=$(echo "$BLOG_POSTS" | wc -l | tr -d ' ')
echo "Found $TOTAL blog posts to migrate"
echo ""

MIGRATED=0
FAILED=0
SKIPPED=0

while IFS='|' read -r id title author source_url file_path source; do
  # Extract year/month from source_url
  YEAR=""
  MONTH=""

  # Try numeric pattern first: /2024/01/15/
  if [[ "$source_url" =~ /([0-9]{4})/([0-9]{2})(/[0-9]{2})? ]]; then
    YEAR="${BASH_REMATCH[1]}"
    MONTH="${BASH_REMATCH[2]}"
  # Try month name pattern: /2024/Jan/15/
  elif [[ "$source_url" =~ /([0-9]{4})/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(/[0-9]{1,2})? ]]; then
    YEAR="${BASH_REMATCH[1]}"
    MONTH_NAME="${BASH_REMATCH[2]}"
    case "$MONTH_NAME" in
      Jan) MONTH="01" ;;
      Feb) MONTH="02" ;;
      Mar) MONTH="03" ;;
      Apr) MONTH="04" ;;
      May) MONTH="05" ;;
      Jun) MONTH="06" ;;
      Jul) MONTH="07" ;;
      Aug) MONTH="08" ;;
      Sep) MONTH="09" ;;
      Oct) MONTH="10" ;;
      Nov) MONTH="11" ;;
      Dec) MONTH="12" ;;
    esac
  fi
  
  if [ -z "$YEAR" ] || [ -z "$MONTH" ]; then
    echo "⚠ Skip (no date in URL): $author - $title"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi
  
  # Generate author folder name
  AUTHOR_FOLDER=$(echo "$author" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')
  
  # Determine file name (from current path)
  FILENAME=$(basename "$file_path")
  
  # Remove date prefix if present (format: YYYY-MM-DD-title.epub or YYYYMMDD-title.epub)
  CLEAN_FILENAME=$(echo "$FILENAME" | sed -E 's/^[0-9]{4}-?[0-9]{2}-?[0-9]{2}-?//') 
  
  # New path structure
  NEW_PATH="/blogs/$AUTHOR_FOLDER/$YEAR/$MONTH/$CLEAN_FILENAME"
  
  # Check if already in correct location
  if [ "$file_path" = "$NEW_PATH" ] || [ "/library.epub/$file_path" = "$NEW_PATH" ]; then
    echo "✓ Already migrated: $author - $title"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi
  
  echo "Migrating: $author - $title"
  echo "  From: $file_path"
  echo "  To:   $NEW_PATH"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN - would migrate]"
    MIGRATED=$((MIGRATED + 1))
    continue
  fi
  
  # Create folder structure on device via WiFi API
  if ! curl -sf "http://$DEVICE_IP/api/folders/blogs" >/dev/null 2>&1; then
    curl -sf -X POST "http://$DEVICE_IP/api/folders" -H "Content-Type: application/json" \
      -d "{\"path\":\"/blogs\"}" >/dev/null 2>&1 || echo "  ⚠ Failed to create /blogs"
  fi
  
  if ! curl -sf "http://$DEVICE_IP/api/folders/blogs/$AUTHOR_FOLDER" >/dev/null 2>&1; then
    curl -sf -X POST "http://$DEVICE_IP/api/folders" -H "Content-Type: application/json" \
      -d "{\"path\":\"/blogs/$AUTHOR_FOLDER\"}" >/dev/null 2>&1 || echo "  ⚠ Failed to create author folder"
  fi
  
  if ! curl -sf "http://$DEVICE_IP/api/folders/blogs/$AUTHOR_FOLDER/$YEAR" >/dev/null 2>&1; then
    curl -sf -X POST "http://$DEVICE_IP/api/folders" -H "Content-Type: application/json" \
      -d "{\"path\":\"/blogs/$AUTHOR_FOLDER/$YEAR\"}" >/dev/null 2>&1 || echo "  ⚠ Failed to create year folder"
  fi
  
  if ! curl -sf "http://$DEVICE_IP/api/folders/blogs/$AUTHOR_FOLDER/$YEAR/$MONTH" >/dev/null 2>&1; then
    curl -sf -X POST "http://$DEVICE_IP/api/folders" -H "Content-Type: application/json" \
      -d "{\"path\":\"/blogs/$AUTHOR_FOLDER/$YEAR/$MONTH\"}" >/dev/null 2>&1 || echo "  ⚠ Failed to create month folder"
  fi
  
  # Move file on device
  OLD_PATH_NORMALIZED=$(echo "$file_path" | sed 's|^/library\.epub||' | sed 's|^/||')
  curl -sf -X POST "http://$DEVICE_IP/api/files/move" -H "Content-Type: application/json" \
    -d "{\"source\":\"/$OLD_PATH_NORMALIZED\",\"destination\":\"$NEW_PATH\"}" >/dev/null 2>&1
  
  if [ $? -eq 0 ]; then
    # Update database
    ESCAPED_NEW_PATH=$(echo "$NEW_PATH" | sed "s/'/''/g")
    sqlite3 "$DB" "UPDATE books SET file_path = '$ESCAPED_NEW_PATH' WHERE id = '$id'"
    echo "  ✓ Migrated"
    MIGRATED=$((MIGRATED + 1))
  else
    echo "  ✗ Failed to move file on device"
    FAILED=$((FAILED + 1))
  fi
  
  sleep 0.5  # rate limit API calls
  
done <<< "$BLOG_POSTS"

echo ""
echo "=== Migration Summary ==="
echo "Total: $TOTAL"
echo "Migrated: $MIGRATED"
echo "Skipped: $SKIPPED"
echo "Failed: $FAILED"

if [ "$DRY_RUN" = true ]; then
  echo ""
  echo "This was a dry run. Run without --dry-run to perform actual migration."
fi
