#!/usr/bin/env bash
# linear-audit: enrich-batch.sh
# Batch enrich issues without context using issue-context skill

set -euo pipefail

# Parse arguments
TEAM="${1:-}"
LIMIT="${2:-10}"
DRY_RUN="${3:-false}"

if [ -z "$TEAM" ]; then
  echo "Usage: enrich-batch.sh <TEAM> [limit] [--dry-run]"
  echo "  TEAM: ARB, KUM, KOT, SIN, WEB, SAY, SQU, PAL"
  echo "  limit: max issues to enrich (default: 10)"
  echo "  --dry-run: show issues without enriching"
  exit 1
fi

# Check for --dry-run flag
if [ "$LIMIT" = "--dry-run" ]; then
  DRY_RUN="true"
  LIMIT="10"
elif [ "${3:-}" = "--dry-run" ]; then
  DRY_RUN="true"
fi

echo "=== Batch Enrichment: $TEAM ==="
echo "Limit: $LIMIT"
echo "Dry run: $DRY_RUN"
echo ""

# Find issues without context
echo "=== Finding Issues Without Context ==="

ENRICHMENT_QUEUE=()

# Get issues and check for context markers
ISSUES=$(linear issue list --team "$TEAM" --limit 50 --json -q | jq -r '.[].identifier')

COUNT=0
for ISSUE in $ISSUES; do
  if [ $COUNT -ge "$LIMIT" ]; then
    break
  fi

  # Check for context markers
  MARKERS=$(linear comment list "$ISSUE" --json -q 2>/dev/null | jq -r '.[].body' | grep -c "issue-context:" || echo "0")

  if [ "$MARKERS" -eq 0 ]; then
    # Get issue title for display
    TITLE=$(linear issue view "$ISSUE" --json -q 2>/dev/null | jq -r '.title' || echo "Unknown")
    echo "  $ISSUE: $TITLE"
    ENRICHMENT_QUEUE+=("$ISSUE")
    ((COUNT++))
  fi
done

echo ""
echo "Found ${#ENRICHMENT_QUEUE[@]} issues needing enrichment"

if [ ${#ENRICHMENT_QUEUE[@]} -eq 0 ]; then
  echo "No issues need enrichment. All issues have context markers."
  exit 0
fi

if [ "$DRY_RUN" = "true" ]; then
  echo ""
  echo "=== Dry Run Complete ==="
  echo "Would enrich:"
  for ISSUE in "${ENRICHMENT_QUEUE[@]}"; do
    echo "  - $ISSUE"
  done
  exit 0
fi

# Enrich issues
echo ""
echo "=== Enriching Issues ==="

# Map team to project path
get_project_path() {
  case $1 in
    ARB) echo ~/Developer/arbor/arbor-xyz ;;
    KUM) echo ~/Developer/kumori/kumori-xyz ;;
    KOT) echo ~/Developer/koto/koto-xyz ;;
    SIN) echo ~/Developer/sine/sine-xyz ;;
    WEB) echo ~/Developer/webs/webs-xyz ;;
    SAY) echo ~/Developer/saya/saya-xyz ;;
    SQU) echo ~/Developer/squish/squish-xyz ;;
    PAL) echo ~/Developer/pal/pal-xyz ;;
    *) echo "unknown" ;;
  esac
}

PROJECT_PATH=$(get_project_path "$TEAM")

if [ "$PROJECT_PATH" = "unknown" ] || [ ! -d "$PROJECT_PATH" ]; then
  echo "Error: Cannot find project path for $TEAM"
  exit 1
fi

cd "$PROJECT_PATH"
echo "Working directory: $PROJECT_PATH"
echo ""

ENRICHED=0
FAILED=0

for ISSUE in "${ENRICHMENT_QUEUE[@]}"; do
  echo "Enriching $ISSUE..."

  # Note: issue-context is a skill, not a CLI command
  # In practice, this would invoke the skill through Claude/agent
  # For now, we'll create a placeholder that shows what would happen

  # Get issue details
  ISSUE_JSON=$(linear issue view "$ISSUE" --json -q 2>/dev/null || echo "{}")
  TITLE=$(echo "$ISSUE_JSON" | jq -r '.title // "Unknown"')
  DESCRIPTION=$(echo "$ISSUE_JSON" | jq -r '.description // ""')

  echo "  Title: $TITLE"

  # Placeholder for actual enrichment
  # In real usage, this would invoke issue-context skill which:
  # 1. Analyzes the issue
  # 2. Gathers codebase context
  # 3. Creates analysis comment
  # 4. Creates agent prompt comment
  # 5. Posts to Linear

  echo "  [Would invoke issue-context skill here]"
  echo "  Status: pending (manual enrichment needed)"

  ((ENRICHED++))

  # Rate limit
  sleep 2
done

echo ""
echo "=== Batch Enrichment Complete ==="
echo "Enriched: $ENRICHED"
echo "Failed: $FAILED"
echo ""
echo "Note: This script identifies issues needing enrichment."
echo "Actual enrichment requires running the issue-context skill"
echo "through Claude Code or another agent."
echo ""
echo "To enrich manually, run in Claude Code:"
echo "  Use issue-context skill on $TEAM issues: ${ENRICHMENT_QUEUE[*]}"
