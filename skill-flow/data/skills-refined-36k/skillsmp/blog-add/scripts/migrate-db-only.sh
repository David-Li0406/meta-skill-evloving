#!/bin/bash
# migrate-db-only.sh - update database paths only, no device operations
set -euo pipefail

DB="$HOME/.epub/library.db"

echo "=== Database-Only Migration ==="
echo "Updating file paths in database to new year/month structure..."
echo ""

# Get all blog posts
TOTAL=$(sqlite3 "$DB" "SELECT COUNT(*) FROM books WHERE source LIKE 'feed:%' OR source = 'backfill'")
echo "Found $TOTAL blog posts"

UPDATED=0
SKIPPED=0

# Process each post
sqlite3 "$DB" "SELECT id, author, source_url, file_path FROM books WHERE source LIKE 'feed:%' OR source = 'backfill'" | while IFS='|' read -r id author source_url file_path; do
  # Extract year/month from source_url
  YEAR=""
  MONTH=""
  
  if [[ "$source_url" =~ /([0-9]{4})/([0-9]{2}) ]]; then
    YEAR="${BASH_REMATCH[1]}"
    MONTH="${BASH_REMATCH[2]}"
  elif [[ "$source_url" =~ /([0-9]{4})/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ]]; then
    YEAR="${BASH_REMATCH[1]}"
    MONTH_NAME="${BASH_REMATCH[2]}"
    case "$MONTH_NAME" in
      Jan) MONTH="01" ;; Feb) MONTH="02" ;; Mar) MONTH="03" ;; Apr) MONTH="04" ;;
      May) MONTH="05" ;; Jun) MONTH="06" ;; Jul) MONTH="07" ;; Aug) MONTH="08" ;;
      Sep) MONTH="09" ;; Oct) MONTH="10" ;; Nov) MONTH="11" ;; Dec) MONTH="12" ;;
    esac
  fi
  
  if [ -z "$YEAR" ] || [ -z "$MONTH" ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi
  
  # Generate new path
  AUTHOR_FOLDER=$(echo "$author" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')
  FILENAME=$(basename "$file_path")
  NEW_PATH="/blogs/$AUTHOR_FOLDER/$YEAR/$MONTH/$FILENAME"
  
  # Check if already correct
  if [ "$file_path" = "$NEW_PATH" ]; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi
  
  # Update database
  ESCAPED_NEW_PATH=$(echo "$NEW_PATH" | sed "s/'/''/g")
  sqlite3 "$DB" "UPDATE books SET file_path = '$ESCAPED_NEW_PATH' WHERE id = '$id'"
  UPDATED=$((UPDATED + 1))
  
  if [ $(( UPDATED % 50 )) -eq 0 ]; then
    echo "Progress: $UPDATED updated..."
  fi
done

echo ""
echo "=== Summary ==="
echo "Total: $TOTAL"
echo "Updated: $UPDATED"
echo "Skipped: $SKIPPED"
echo "✓ Database migration complete!"
