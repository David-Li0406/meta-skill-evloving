#!/bin/bash
set -euo pipefail

# Restore previous session context
#
# Usage:
#   bash restore-state.sh [options]
#
# Options:
#   --files-only     Load only edited files, skip full context
#   --no-files       Show context info without loading files
#   --session ID     Restore specific session by ID
#   --verbose        Show detailed restoration process

PROJECT_ROOT="${PROJECT_ROOT:-.}"
STATE_FILE="$PROJECT_ROOT/.claude/.project-state.json"
HISTORY_FILE="$PROJECT_ROOT/.claude/.session-history.json"

# Parse arguments
LOAD_FILES=true
SHOW_CONTEXT=true
SESSION_ID=""
VERBOSE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --files-only)
      SHOW_CONTEXT=false
      shift
      ;;
    --no-files)
      LOAD_FILES=false
      shift
      ;;
    --session)
      SESSION_ID="$2"
      shift 2
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Check if state file exists
if [ ! -f "$STATE_FILE" ]; then
  echo "No previous session found."
  echo ""
  echo "This appears to be your first session in this project."
  echo "Session state will be saved automatically on exit."
  exit 0
fi

# Validate JSON
if ! jq '.' "$STATE_FILE" >/dev/null 2>&1; then
  echo "Error: Session state file is corrupted." >&2
  if [ -f "$STATE_FILE.bak" ]; then
    echo "Attempting to restore from backup..." >&2
    cp "$STATE_FILE.bak" "$STATE_FILE"
    if jq '.' "$STATE_FILE" >/dev/null 2>&1; then
      echo "Backup restored successfully." >&2
    else
      echo "Backup is also corrupted. Cannot restore session." >&2
      exit 1
    fi
  else
    echo "No backup available. Cannot restore session." >&2
    exit 1
  fi
fi

# Read state
SESSION_ID_STORED=$(jq -r '.session_id' "$STATE_FILE")
TIMESTAMP=$(jq -r '.timestamp' "$STATE_FILE")
PROJECT_NAME=$(jq -r '.project_name // "Unknown Project"' "$STATE_FILE")
EDITED_FILES=$(jq -r '.edited_files[]' "$STATE_FILE" 2>/dev/null || echo "")
PHASE_NAME=$(jq -r '.phase.name // "Unknown Phase"' "$STATE_FILE")
PHASE_COMPLETION=$(jq -r '.phase.completion // 0' "$STATE_FILE")
PLAN_FILE=$(jq -r '.plan.file // null' "$STATE_FILE")
PLAN_PROGRESS=$(jq -r '.plan.progress // 0' "$STATE_FILE")
SESSION_DURATION=$(jq -r '.session_duration_minutes // 0' "$STATE_FILE")

# Calculate session age
if command -v date &>/dev/null; then
  LAST_SESSION=$(date -d "$TIMESTAMP" +%s 2>/dev/null || echo 0)
  NOW=$(date +%s)
  AGE_SECONDS=$((NOW - LAST_SESSION))
  AGE_HOURS=$((AGE_SECONDS / 3600))
  AGE_MINUTES=$(((AGE_SECONDS % 3600) / 60))

  if [ $AGE_HOURS -gt 0 ]; then
    AGE_STR="${AGE_HOURS}h ${AGE_MINUTES}m ago"
  else
    AGE_STR="${AGE_MINUTES}m ago"
  fi
else
  AGE_STR="(age unknown)"
fi

# Show context information
if $SHOW_CONTEXT; then
  echo "═══════════════════════════════════════════════"
  echo "  Resuming Project: $PROJECT_NAME"
  echo "═══════════════════════════════════════════════"
  echo ""
  echo "Last session: $AGE_STR"
  echo "Session ID: $SESSION_ID_STORED"
  echo "Duration: ${SESSION_DURATION} minutes"
  echo ""
  echo "Phase: $PHASE_NAME (${PHASE_COMPLETION}% complete)"

  # Show edited files
  if [ -n "$EDITED_FILES" ]; then
    FILE_COUNT=$(echo "$EDITED_FILES" | wc -l)
    echo ""
    echo "Files edited ($FILE_COUNT):"
    echo "$EDITED_FILES" | head -10 | while read -r file; do
      echo "  • $file"
    done
    if [ $FILE_COUNT -gt 10 ]; then
      echo "  ... and $((FILE_COUNT - 10)) more"
    fi
  fi

  # Show active todos
  TODOS=$(jq -c '.todos[]' "$STATE_FILE" 2>/dev/null || echo "")
  if [ -n "$TODOS" ]; then
    echo ""
    echo "Active todos:"
    echo "$TODOS" | while IFS= read -r todo; do
      STATUS=$(echo "$todo" | jq -r '.status')
      CONTENT=$(echo "$todo" | jq -r '.content')
      case $STATUS in
        "completed")
          echo "  ✓ $CONTENT"
          ;;
        "in_progress")
          echo "  ⏳ $CONTENT (in progress)"
          ;;
        "pending")
          echo "  ⏳ $CONTENT (pending)"
          ;;
      esac
    done
  fi

  # Show plan info
  if [ "$PLAN_FILE" != "null" ]; then
    PLAN_TOTAL=$(jq -r '.plan.total_tasks // 0' "$STATE_FILE")
    PLAN_COMPLETED=$(jq -r '.plan.completed_tasks // 0' "$STATE_FILE")
    echo ""
    echo "Plan: $PLAN_FILE (${PLAN_PROGRESS}% complete - ${PLAN_COMPLETED}/${PLAN_TOTAL} tasks)"
  fi

  # Show warnings if any
  WARNINGS=$(jq -r '.warnings[]?' "$STATE_FILE" 2>/dev/null || echo "")
  if [ -n "$WARNINGS" ]; then
    echo ""
    echo "⚠️  Warnings:"
    echo "$WARNINGS" | while IFS= read -r warning; do
      echo "  • $warning"
    done
  fi

  echo ""
  echo "───────────────────────────────────────────────"
  echo ""
fi

# Load edited files
if $LOAD_FILES; then
  if [ -z "$EDITED_FILES" ]; then
    echo "No edited files to load."
  else
    FILE_COUNT=$(echo "$EDITED_FILES" | wc -l)
    MAX_LOAD=5
    LOAD_COUNT=$((FILE_COUNT < MAX_LOAD ? FILE_COUNT : MAX_LOAD))

    echo "Loading $LOAD_COUNT most recent files..."
    echo ""

    LOADED=0
    echo "$EDITED_FILES" | head -$MAX_LOAD | while read -r file; do
      if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "  ✓ $file"
        # File will be read by Claude Code
        LOADED=$((LOADED + 1))
      else
        echo "  ✗ $file (not found)"
      fi
    done

    if [ $FILE_COUNT -gt $MAX_LOAD ]; then
      echo ""
      echo "  ... $((FILE_COUNT - MAX_LOAD)) more files available"
      echo "  Use /resume --all to load all edited files"
    fi
  fi
fi

# Display next actions
if $SHOW_CONTEXT; then
  echo ""
  echo "Continue where you left off!"
  echo ""
  echo "Quick actions:"
  echo "  /navigate --phase \"$PHASE_NAME\"  - Jump to current phase"
  if [ "$PLAN_FILE" != "null" ]; then
    echo "  /plan  - View plan progress"
  fi
  echo "  /context-summary  - Full project overview"
  echo ""
fi

exit 0
