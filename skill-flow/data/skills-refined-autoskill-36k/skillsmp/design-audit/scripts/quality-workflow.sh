#!/usr/bin/env bash
set -euo pipefail

# Quality improvement workflow for design documentation
# Identifies quality issues and generates improvement roadmap

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DESIGN_DIR="$PROJECT_ROOT/.claude/design"

echo "======================================="
echo "Design Documentation Quality Analysis"
echo "======================================="
echo ""

# Run validation first
echo "Running validation..."
if ! "$SCRIPT_DIR/validate-all-docs.sh"; then
  echo ""
  echo "❌ Quality check stopped: Fix validation errors first"
  exit 1
fi

echo ""
echo "---------------------------------------"
echo "Analyzing documentation quality..."
echo "---------------------------------------"
echo ""

# Find all markdown files
mapfile -t DESIGN_FILES < <(find "$DESIGN_DIR" -type f -name "*.md" ! -name "design.config.json" | sort)

# Statistics
TOTAL=${#DESIGN_FILES[@]}
LOW_COMPLETENESS=0
MEDIUM_COMPLETENESS=0
HIGH_COMPLETENESS=0
STUB_STATUS=0
DRAFT_STATUS=0
CURRENT_STATUS=0
ARCHIVED_STATUS=0

# Completeness distribution
for file in "${DESIGN_FILES[@]}"; do
  FRONTMATTER=$(awk 'BEGIN{found=0} /^---$/{found++; next} found==1{print} found==2{exit}' "$file")

  # Extract completeness
  COMPLETENESS=$(echo "$FRONTMATTER" | grep "^completeness:" | awk '{print $2}')

  # Extract status
  STATUS=$(echo "$FRONTMATTER" | grep "^status:" | awk '{print $2}')

  # Categorize by completeness
  if [[ -n "$COMPLETENESS" ]]; then
    if [[ "$COMPLETENESS" -lt 50 ]]; then
      LOW_COMPLETENESS=$((LOW_COMPLETENESS + 1))
      echo "📊 Low completeness ($COMPLETENESS%): $(basename "$file")"
    elif [[ "$COMPLETENESS" -lt 80 ]]; then
      MEDIUM_COMPLETENESS=$((MEDIUM_COMPLETENESS + 1))
    else
      HIGH_COMPLETENESS=$((HIGH_COMPLETENESS + 1))
    fi
  fi

  # Count by status
  case "$STATUS" in
    stub) STUB_STATUS=$((STUB_STATUS + 1)) ;;
    draft) DRAFT_STATUS=$((DRAFT_STATUS + 1)) ;;
    current) CURRENT_STATUS=$((CURRENT_STATUS + 1)) ;;
    archived) ARCHIVED_STATUS=$((ARCHIVED_STATUS + 1)) ;;
  esac
done

echo ""
echo "======================================="
echo "Quality Analysis Summary"
echo "======================================="
echo ""
echo "Total Documents: $TOTAL"
echo ""
echo "Completeness Distribution:"
echo "  High (≥80%):    $HIGH_COMPLETENESS"
echo "  Medium (50-79%): $MEDIUM_COMPLETENESS"
echo "  Low (<50%):      $LOW_COMPLETENESS"
echo ""
echo "Status Distribution:"
echo "  Current:  $CURRENT_STATUS"
echo "  Draft:    $DRAFT_STATUS"
echo "  Stub:     $STUB_STATUS"
echo "  Archived: $ARCHIVED_STATUS"
echo ""

# Calculate quality score (0-100)
if [[ "$TOTAL" -gt 0 ]]; then
  # Weight: 60% completeness, 40% status
  COMPLETENESS_SCORE=$(( (HIGH_COMPLETENESS * 100 + MEDIUM_COMPLETENESS * 65 + LOW_COMPLETENESS * 25) / TOTAL ))
  STATUS_SCORE=$(( (CURRENT_STATUS * 100 + DRAFT_STATUS * 60 + STUB_STATUS * 20 + ARCHIVED_STATUS * 80) / TOTAL ))
  OVERALL_SCORE=$(( (COMPLETENESS_SCORE * 60 + STATUS_SCORE * 40) / 100 ))

  echo "Quality Scores:"
  echo "  Completeness: $COMPLETENESS_SCORE/100"
  echo "  Status:       $STATUS_SCORE/100"
  echo "  Overall:      $OVERALL_SCORE/100"
  echo ""

  # Quality rating
  if [[ "$OVERALL_SCORE" -ge 80 ]]; then
    RATING="Excellent ✅"
  elif [[ "$OVERALL_SCORE" -ge 60 ]]; then
    RATING="Good 👍"
  elif [[ "$OVERALL_SCORE" -ge 40 ]]; then
    RATING="Fair ⚠️"
  else
    RATING="Needs Improvement ❌"
  fi

  echo "Overall Rating: $RATING"
fi

echo ""
echo "======================================="
echo "Improvement Roadmap"
echo "======================================="
echo ""

if [[ "$LOW_COMPLETENESS" -gt 0 ]]; then
  echo "1. Improve low-completeness documents ($LOW_COMPLETENESS docs <50%)"
  echo "   - Review and expand incomplete sections"
  echo "   - Add missing examples and diagrams"
  echo "   - Use design-update skill to enhance content"
fi

if [[ "$STUB_STATUS" -gt 0 ]]; then
  echo "2. Complete stub documents ($STUB_STATUS stubs)"
  echo "   - Convert stubs to drafts with initial content"
  echo "   - Or archive if no longer needed"
fi

if [[ "$DRAFT_STATUS" -gt 0 ]]; then
  echo "3. Finalize draft documents ($DRAFT_STATUS drafts)"
  echo "   - Review for accuracy and completeness"
  echo "   - Update status to 'current' when ready"
fi

echo ""
echo "Run 'pnpm run docs:maintenance' to check for stale docs"
echo "Run 'pnpm run docs:release' before releases"
echo ""
