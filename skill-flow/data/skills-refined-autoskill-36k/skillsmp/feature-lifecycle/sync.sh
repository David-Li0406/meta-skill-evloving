#!/bin/bash
# feature-lifecycle/sync.sh
# The "Save Button". Runs ci-lite, then commits and pushes.

set -e

MESSAGE="$1"
WIP_MODE=0

if [ "$1" == "--wip" ]; then
  WIP_MODE=1
  MESSAGE="$2"
fi

if [ -z "$MESSAGE" ]; then
  echo "Usage: sync-feature [options] <message>"
  echo "Options:"
  echo "  --wip    Force save even if CI fails (marks commit as [WIP])"
  exit 1
fi

echo "🔄 Syncing feature..."

# 1. Run CI Lite (The Guardrail)
echo "🧪 Running CI-Lite..."
if make ci-lite; then
  echo "✅ CI Passed."
else
  if [ "$WIP_MODE" -eq 1 ]; then
    echo "⚠️  CI Failed, but --wip used. Saving anyway..."
    MESSAGE="[WIP] ${MESSAGE}"
  else
    echo "❌ COMMIT BLOCKED: CI-LITE FAILED"
    echo ""
    echo "🚨 ACTION REQUIRED: Fix errors above."
    echo "   Or use 'sync-feature --wip "..."' to force save."
    exit 1
  fi
fi

# 2. Commit & Push
git add .
git commit -m "${MESSAGE}"
git push origin HEAD

echo "✅ Saved to remote."

