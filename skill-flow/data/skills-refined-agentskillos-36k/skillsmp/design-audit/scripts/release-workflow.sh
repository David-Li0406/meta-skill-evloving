#!/usr/bin/env bash
set -euo pipefail

# Release workflow for design documentation
# Validates all docs are ready for release

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DESIGN_DIR="$PROJECT_ROOT/.claude/design"

echo "==================================="
echo "Design Documentation Release Check"
echo "==================================="
echo ""

# Run validation on all docs
echo "Step 1: Validating all design documentation..."
if ! "$SCRIPT_DIR/validate-all-docs.sh"; then
  echo ""
  echo "❌ Release check failed: Validation errors found"
  echo "Please fix all validation errors before releasing"
  exit 1
fi

echo ""
echo "Step 2: Checking for stub status documents..."
STUB_COUNT=0

# Find all markdown files
mapfile -t DESIGN_FILES < <(find "$DESIGN_DIR" -type f -name "*.md" ! -name "design.config.json" | sort)

for file in "${DESIGN_FILES[@]}"; do
  # Extract status from frontmatter
  STATUS=$(awk 'BEGIN{found=0} /^---$/{found++; next} found==1{print} found==2{exit}' "$file" | grep "^status:" | awk '{print $2}')

  if [[ "$STATUS" == "stub" ]]; then
    echo "⚠️  Stub status: $file"
    STUB_COUNT=$((STUB_COUNT + 1))
  fi
done

if [[ "$STUB_COUNT" -gt 0 ]]; then
  echo ""
  echo "⚠️  Warning: $STUB_COUNT documents with 'stub' status"
  echo "Consider updating or archiving stub documents before release"
fi

echo ""
echo "Step 3: Checking completeness scores..."
LOW_COMPLETENESS_COUNT=0

for file in "${DESIGN_FILES[@]}"; do
  # Extract completeness from frontmatter
  COMPLETENESS=$(awk 'BEGIN{found=0} /^---$/{found++; next} found==1{print} found==2{exit}' "$file" | grep "^completeness:" | awk '{print $2}')

  if [[ -n "$COMPLETENESS" ]] && [[ "$COMPLETENESS" -lt 50 ]]; then
    echo "⚠️  Low completeness ($COMPLETENESS%): $file"
    LOW_COMPLETENESS_COUNT=$((LOW_COMPLETENESS_COUNT + 1))
  fi
done

if [[ "$LOW_COMPLETENESS_COUNT" -gt 0 ]]; then
  echo ""
  echo "⚠️  Warning: $LOW_COMPLETENESS_COUNT documents with completeness < 50%"
  echo "Consider completing documentation before release"
fi

echo ""
echo "==================================="
echo "Release Check Summary"
echo "==================================="
echo "Total design docs: ${#DESIGN_FILES[@]}"
echo "Stub status: $STUB_COUNT"
echo "Low completeness: $LOW_COMPLETENESS_COUNT"
echo ""

if [[ "$STUB_COUNT" -eq 0 ]] && [[ "$LOW_COMPLETENESS_COUNT" -eq 0 ]]; then
  echo "✅ All design documentation is ready for release!"
  exit 0
else
  echo "⚠️  Release check completed with warnings"
  echo "Review warnings above before proceeding with release"
  exit 0
fi
