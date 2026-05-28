#!/bin/bash
# bd-doctor fix - Auto-fix common Beads workflow issues

set -e

echo "🔧 Beads Doctor - Fixing issues..."

FIXED=0

# Fix 1: JSONL timestamp skew
echo ""
echo "📋 Fixing JSONL sync..."
if bd sync --dry-run 2>&1 | grep -q "JSONL is newer"; then
  echo "Running: bd export --force"
  bd export --force
  echo "✅ JSONL exported (timestamp skew resolved)"
  FIXED=$((FIXED + 1))
elif bd sync --dry-run 2>&1 | grep -q "Pushing directly to master is blocked"; then
  echo "Running: bd export --force (no push on master)"
  bd export --force
  echo "✅ JSONL exported without pushing to master"
  FIXED=$((FIXED + 1))
else
  echo "✅ JSONL already in sync"
fi

# Fix 2: Stage unstaged JSONL
echo ""
echo "📋 Staging Beads changes..."
# Check for unstaged changes only (second character is M or D)
if git status --porcelain 2>/dev/null | grep "^.M .beads/issues.jsonl" || \
   git status --porcelain 2>/dev/null | grep "^.D .beads/issues.jsonl"; then
  echo "Running: git add .beads/issues.jsonl"
  git add .beads/issues.jsonl
  echo "✅ Beads JSONL staged"
  FIXED=$((FIXED + 1))
else
  echo "✅ No unstaged Beads changes"
fi

# Fix 3: Branch/Issue mismatch - can't auto-fix, only warn
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
if [[ $BRANCH =~ ^feature-bd-([a-z0-9]+) ]]; then
  ISSUE_ID="${BASH_REMATCH[1]}"
  if ! bd show "bd-$ISSUE_ID" &>/dev/null; then
    echo ""
    echo "⚠️  Cannot auto-fix: Branch feature-bd-$ISSUE_ID but issue bd-$ISSUE_ID not found"
    echo "   Manual action required:"
    echo "   - Create issue: bd create \"Task name\" --type task"
    echo "   - OR switch branch: git checkout feature-bd-{correct-id}"
  fi
fi

echo ""
echo "═══════════════════════════════════════"
if [[ $FIXED -eq 0 ]]; then
  echo "ℹ️  Nothing to fix (already healthy)"
else
  echo "✅ Fixed $FIXED Beads issue(s)"
  echo ""
  echo "Next: Verify with 'bd sync' or continue workflow"
fi
