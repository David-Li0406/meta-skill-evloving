#!/bin/bash
#
# validate-index.sh - Validate INDEX.md format and content
#
# Checks:
# - File exists and is readable
# - Has required header row with expected columns
# - Task IDs match PREFIX-NNN pattern
# - Status values are valid
# - Dependencies reference existing tasks
# - No duplicate task IDs
# - Worktree branches are valid format (if specified)
#
# Usage:
#   ./validate-index.sh [path/to/INDEX.md]
#   ./validate-index.sh --fix  # Attempt to fix common issues
#
# Exit codes:
#   0 - Valid
#   1 - Invalid (errors found)
#   2 - File not found or not readable
#

set -eo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INDEX_FILE=""
FIX_MODE=false
VERBOSE=false

# Counters
ERRORS=0
WARNINGS=0

# Valid status values
VALID_STATUSES=("Ready" "In Progress" "In Review" "Review" "Complete" "Blocked" "Changes Requested")

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --fix)
      FIX_MODE=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      echo "Usage: validate-index.sh [options] [path/to/INDEX.md]"
      echo ""
      echo "Options:"
      echo "  --fix        Attempt to fix common issues"
      echo "  -v, --verbose  Show detailed output"
      echo "  -h, --help   Show this help"
      echo ""
      echo "If no path is provided, looks for tasks/INDEX.md in current directory"
      echo "or git repository root."
      exit 0
      ;;
    *)
      INDEX_FILE="$1"
      shift
      ;;
  esac
done

# Find INDEX.md if not specified
if [[ -z "$INDEX_FILE" ]]; then
  # Try current directory
  if [[ -f "tasks/INDEX.md" ]]; then
    INDEX_FILE="tasks/INDEX.md"
  else
    # Try git root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
    if [[ -n "$repo_root" && -f "$repo_root/tasks/INDEX.md" ]]; then
      INDEX_FILE="$repo_root/tasks/INDEX.md"
    fi
  fi
fi

# Output helpers
log_error() {
  echo -e "${RED}ERROR:${NC} $1" >&2
  ERRORS=$((ERRORS + 1))
}

log_warning() {
  echo -e "${YELLOW}WARNING:${NC} $1" >&2
  WARNINGS=$((WARNINGS + 1))
}

log_info() {
  if [[ "$VERBOSE" == "true" ]]; then
    echo -e "${BLUE}INFO:${NC} $1"
  fi
}

log_success() {
  echo -e "${GREEN}✓${NC} $1"
}

# Check file exists
if [[ -z "$INDEX_FILE" ]]; then
  log_error "INDEX.md not found. Specify path or run from project root."
  echo ""
  echo "Expected location: tasks/INDEX.md"
  echo ""
  echo "To create the tasks directory structure, run:"
  echo "  /design:init"
  exit 2
fi

if [[ ! -f "$INDEX_FILE" ]]; then
  log_error "File not found: $INDEX_FILE"
  exit 2
fi

if [[ ! -r "$INDEX_FILE" ]]; then
  log_error "File not readable: $INDEX_FILE"
  exit 2
fi

echo "Validating: $INDEX_FILE"
echo ""

# Parse and validate
declare -a TASK_IDS=()
declare -a ALL_DEPS=()
HEADER_FOUND=false
LINE_NUM=0

while IFS= read -r line; do
  LINE_NUM=$((LINE_NUM + 1))

  # Skip empty lines
  [[ -z "$line" ]] && continue

  # Skip non-table lines
  [[ ! "$line" =~ ^\|.*\|$ ]] && continue

  # Check for header row
  if [[ "$line" =~ ^[[:space:]]*\|[[:space:]]*ID[[:space:]]*\| ]]; then
    # Validate header has expected columns
    if [[ "$line" =~ ID.*Title.*Status.*Dependencies.*Worktree ]]; then
      log_info "Line $LINE_NUM: Found valid task table header"
      HEADER_FOUND=true
    else
      log_warning "Line $LINE_NUM: Header row found but missing expected columns"
      echo "  Expected: | ID | Title | Status | Dependencies | Worktree |"
      echo "  Found:    $line"
    fi
    continue
  fi

  # Skip separator rows
  [[ "$line" =~ ^[[:space:]]*\|[[:space:]]*[-:]+[[:space:]]*\| ]] && continue

  # Skip if we haven't found the header yet
  [[ "$HEADER_FOUND" != "true" ]] && continue

  # Parse table row
  line="${line#|}"
  line="${line%|}"

  id=""
  title=""
  status=""
  deps=""
  worktree=""
  i=0
  OLD_IFS="$IFS"
  IFS='|'
  for col in $line; do
    col=$(echo "$col" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    case $i in
      0) id="$col" ;;
      1) title="$col" ;;
      2) status="$col" ;;
      3) deps="$col" ;;
      4) worktree="$col" ;;
    esac
    i=$((i + 1))
  done
  IFS="$OLD_IFS"

  # Skip non-task rows (doesn't match ID pattern)
  if [[ ! "$id" =~ ^[A-Z]+-[0-9]+$ ]]; then
    log_info "Line $LINE_NUM: Skipping non-task row (ID: '$id')"
    continue
  fi

  log_info "Line $LINE_NUM: Validating task $id"

  # Check for duplicate ID
  for existing_id in "${TASK_IDS[@]}"; do
    if [[ "$existing_id" == "$id" ]]; then
      log_error "Line $LINE_NUM: Duplicate task ID '$id'"
    fi
  done
  TASK_IDS+=("$id")

  # Validate title is not empty
  if [[ -z "$title" ]]; then
    log_error "Line $LINE_NUM: Task $id has empty title"
  fi

  # Validate status
  status_valid=false
  for valid_status in "${VALID_STATUSES[@]}"; do
    if [[ "$status" == "$valid_status" ]]; then
      status_valid=true
      break
    fi
  done
  if [[ "$status_valid" != "true" ]]; then
    log_error "Line $LINE_NUM: Task $id has invalid status '$status'"
    echo "  Valid statuses: ${VALID_STATUSES[*]}"
  fi

  # Collect dependencies for later validation
  if [[ -n "$deps" && "$deps" != "-" && "$deps" != "None" && "$deps" != "none" ]]; then
    for dep in $(echo "$deps" | tr ',' ' '); do
      dep=$(echo "$dep" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      if [[ "$dep" =~ ^[A-Z]+-[0-9]+$ ]]; then
        ALL_DEPS+=("$id:$dep")
      elif [[ -n "$dep" ]]; then
        log_warning "Line $LINE_NUM: Task $id has malformed dependency '$dep'"
      fi
    done
  fi

  # Validate worktree format (if specified)
  if [[ -n "$worktree" && "$worktree" != "-" ]]; then
    # Should be a valid branch name
    if [[ ! "$worktree" =~ ^[a-zA-Z0-9/_-]+$ ]]; then
      log_warning "Line $LINE_NUM: Task $id has unusual worktree branch name '$worktree'"
    fi
  fi

done < "$INDEX_FILE"

# Check header was found
if [[ "$HEADER_FOUND" != "true" ]]; then
  log_error "No task table header found"
  echo "  Expected header: | ID | Title | Status | Dependencies | Worktree |"
fi

# Validate all dependencies reference existing tasks
echo ""
log_info "Validating dependency references..."
for dep_ref in "${ALL_DEPS[@]}"; do
  task_id="${dep_ref%%:*}"
  dep_id="${dep_ref##*:}"

  dep_found=false
  for existing_id in "${TASK_IDS[@]}"; do
    if [[ "$existing_id" == "$dep_id" ]]; then
      dep_found=true
      break
    fi
  done

  if [[ "$dep_found" != "true" ]]; then
    log_error "Task $task_id depends on non-existent task '$dep_id'"
  fi
done

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "Validation Summary"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Tasks found: ${#TASK_IDS[@]}"
echo "Errors:      $ERRORS"
echo "Warnings:    $WARNINGS"
echo ""

if [[ $ERRORS -gt 0 ]]; then
  echo -e "${RED}VALIDATION FAILED${NC}"
  echo ""
  echo "Fix the errors above and run validation again."
  exit 1
elif [[ $WARNINGS -gt 0 ]]; then
  echo -e "${YELLOW}VALIDATION PASSED WITH WARNINGS${NC}"
  echo ""
  echo "Consider addressing the warnings above."
  exit 0
else
  echo -e "${GREEN}VALIDATION PASSED${NC}"
  exit 0
fi
