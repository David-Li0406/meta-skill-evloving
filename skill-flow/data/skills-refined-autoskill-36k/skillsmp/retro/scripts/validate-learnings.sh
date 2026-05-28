#!/bin/bash
# validate-learnings.sh
# Check LEARNINGS.md and ERROR_HISTORY.md for common issues

set -e

LEARNINGS_FILE=".claude/LEARNINGS.md"
ERROR_FILE=".claude/ERROR_HISTORY.md"

echo "=== Validating Session Learning Files ==="
echo ""

# Check if files exist
if [ ! -f "$LEARNINGS_FILE" ]; then
  echo "⚠️  $LEARNINGS_FILE not found"
else
  echo "✓ $LEARNINGS_FILE exists"
fi

if [ ! -f "$ERROR_FILE" ]; then
  echo "⚠️  $ERROR_FILE not found"
else
  echo "✓ $ERROR_FILE exists"
fi

echo ""

# Check for duplicate entries in LEARNINGS.md
if [ -f "$LEARNINGS_FILE" ]; then
  echo "=== Checking for duplicates in LEARNINGS.md ==="

  # Extract headings and look for duplicates
  duplicates=$(grep -E "^##" "$LEARNINGS_FILE" | sort | uniq -d)

  if [ -n "$duplicates" ]; then
    echo "⚠️  Potential duplicate entries found:"
    echo "$duplicates"
  else
    echo "✓ No duplicate headings found"
  fi
  echo ""
fi

# Check for old entries that might be obsolete
if [ -f "$LEARNINGS_FILE" ]; then
  echo "=== Checking for potentially stale entries ==="

  # Find entries older than 90 days
  current_year=$(date +%Y)
  three_months_ago=$(date -d "90 days ago" +%Y-%m-%d 2>/dev/null || date -v-90d +%Y-%m-%d 2>/dev/null || echo "skip")

  if [ "$three_months_ago" != "skip" ]; then
    old_entries=$(grep -E "^## [0-9]{4}-[0-9]{2}-[0-9]{2}" "$LEARNINGS_FILE" | while read line; do
      date=$(echo "$line" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
      if [[ "$date" < "$three_months_ago" ]]; then
        echo "$line"
      fi
    done)

    if [ -n "$old_entries" ]; then
      echo "📅 Entries older than 90 days (consider reviewing):"
      echo "$old_entries" | head -10
      count=$(echo "$old_entries" | wc -l)
      if [ "$count" -gt 10 ]; then
        echo "... and $((count - 10)) more"
      fi
    else
      echo "✓ All entries are recent"
    fi
  else
    echo "⚠️  Date calculation not supported on this system"
  fi
  echo ""
fi

# Check format compliance in ERROR_HISTORY.md
if [ -f "$ERROR_FILE" ]; then
  echo "=== Checking ERROR_HISTORY.md format ==="

  # Check for required fields
  entries_without_severity=$(grep -c "^##" "$ERROR_FILE" || echo "0")
  entries_with_severity=$(grep -c "Severity:" "$ERROR_FILE" || echo "0")

  if [ "$entries_without_severity" -gt 0 ] && [ "$entries_with_severity" -lt "$entries_without_severity" ]; then
    echo "⚠️  Some entries may be missing Severity field"
    echo "   Found $entries_without_severity entries, only $entries_with_severity have Severity"
  else
    echo "✓ All entries have Severity field"
  fi

  entries_with_fix=$(grep -c "Fix:" "$ERROR_FILE" || echo "0")
  if [ "$entries_with_fix" -lt "$entries_without_severity" ]; then
    echo "⚠️  Some entries may be missing Fix field"
    echo "   Found $entries_without_severity entries, only $entries_with_fix have Fix"
  else
    echo "✓ All entries have Fix field"
  fi
  echo ""
fi

# Check file sizes
if [ -f "$LEARNINGS_FILE" ]; then
  size=$(wc -l < "$LEARNINGS_FILE")
  if [ "$size" -gt 500 ]; then
    echo "⚠️  LEARNINGS.md has $size lines - consider archiving old entries"
  else
    echo "✓ LEARNINGS.md size is manageable ($size lines)"
  fi
fi

if [ -f "$ERROR_FILE" ]; then
  size=$(wc -l < "$ERROR_FILE")
  if [ "$size" -gt 300 ]; then
    echo "⚠️  ERROR_HISTORY.md has $size lines - consider archiving resolved errors"
  else
    echo "✓ ERROR_HISTORY.md size is manageable ($size lines)"
  fi
fi

echo ""
echo "=== Validation Complete ==="
