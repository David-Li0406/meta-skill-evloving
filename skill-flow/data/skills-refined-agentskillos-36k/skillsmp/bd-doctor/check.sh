#!/bin/bash
# bd-doctor check - Verify Beads workflow health

set -e

echo "🔍 Beads Doctor - Health Check"

ISSUES_FOUND=0

# Check 1: JSONL timestamp skew (most common issue)
echo ""
echo "📋 Checking Beads JSONL sync..."
if bd sync --dry-run 2>&1 | grep -q "JSONL is newer"; then
  echo "⚠️  JSONL timestamp skew detected"
  echo "   Cause: Daemon auto-exported between your changes and sync"
  echo "   Fix: bd export --force (resolves timing issue)"
  ISSUES_FOUND=$((ISSUES_FOUND + 1))
elif bd sync --dry-run 2>&1 | grep -q "Pushing directly to master is blocked"; then
  echo "⚠️  Attempting to push JSONL to protected branch"
  echo "   Cause: Running bd sync on master branch"
  echo "   Fix: Use 'bd export --force' on master (no push), or switch to feature branch"
  ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
  echo "✅ Beads JSONL in sync with database"
fi

# Check 2: Unstaged JSONL changes
echo ""
echo "📋 Checking for unstaged Beads changes..."
# Check for unstaged changes only (second character is M or D)
if git status --porcelain 2>/dev/null | grep "^.M .beads/issues.jsonl" || \
   git status --porcelain 2>/dev/null | grep "^.D .beads/issues.jsonl"; then
  echo "⚠️  .beads/issues.jsonl has unstaged changes"
  echo "   Stage with: git add .beads/issues.jsonl"
  ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
  echo "✅ No unstaged Beads changes"
fi

# Check 3: Branch/Issue alignment
echo ""
echo "📋 Checking branch/issue alignment..."
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
if [[ $BRANCH =~ ^feature-bd-([a-z0-9]+) ]]; then
  ISSUE_ID="${BASH_REMATCH[1]}"
  if bd show "bd-$ISSUE_ID" &>/dev/null; then
    echo "✅ Branch feature-bd-$ISSUE_ID matches Beads issue bd-$ISSUE_ID"
  else
    echo "⚠️  On branch feature-bd-$ISSUE_ID but issue bd-$ISSUE_ID not found"
    echo "   Possible causes:"
    echo "   - Issue was closed/deleted"
    echo "   - Working on wrong branch"
    echo "   - Need to create issue: bd create \"Task name\" --type task"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi
elif [[ $BRANCH == "master" ]] || [[ $BRANCH == "main" ]]; then
  echo "ℹ️  On $BRANCH branch (no Beads issue expected)"
else
  echo "ℹ️  On non-Beads branch: $BRANCH (custom branch, no issue tracking)"
fi

# Check 4: Feature-Key trailer in recent commits
echo ""
echo "📋 Checking Feature-Key trailers..."
RECENT_COMMIT=$(git log -1 --format=%B 2>/dev/null || echo "")
if [[ -n "$RECENT_COMMIT" ]] && ! echo "$RECENT_COMMIT" | grep -q "Feature-Key:"; then
  # Only warn if on feature branch
  if [[ $BRANCH =~ ^feature- ]]; then
    echo "⚠️  Recent commit missing Feature-Key trailer"
    echo "   Use sync-feature-branch skill for proper commit format"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  else
    echo "✅ Not on feature branch (Feature-Key not required)"
  fi
else
  echo "✅ Feature-Key trailer present or not required"
fi

echo ""
echo "═══════════════════════════════════════"
if [[ $ISSUES_FOUND -eq 0 ]]; then
  echo "✅ All Beads checks passed! Healthy workflow."
  exit 0
else
  echo "❌ Found $ISSUES_FOUND Beads issue(s)"
  echo ""
  echo "Run: ~/.agent/skills/bd-doctor/fix.sh    # to auto-fix"
  exit 1
fi
