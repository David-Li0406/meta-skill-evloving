#!/bin/bash
# feature-lifecycle/finish.sh
# The "Handoff Button". Rebase, Verify, PR.

set -e

echo "🏁 Finishing feature..."

# 1. Sync with Master
echo "🔄 Rebasing on origin/master..."
git fetch origin
git rebase origin/master

# 2. Run Verification (The Middle Loop)
echo "🔬 Running Verification (verify-pr)..."
if make verify-pr; then
  echo "✅ Verification Passed."
else
  echo "❌ PR BLOCKED: VERIFICATION FAILED"
  echo "   See artifacts/verification/report.md for details."
  exit 1
fi

# 3. Create PR
echo "📮 Creating Pull Request..."
gh pr create --fill

echo "✅ PR Created. Waiting for review."
