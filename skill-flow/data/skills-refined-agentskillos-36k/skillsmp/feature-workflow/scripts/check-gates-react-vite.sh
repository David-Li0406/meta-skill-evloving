#!/bin/bash
# Feature Workflow Gate Check Script (ssak-admin-frontend)
# Usage: ./check-feature-gates.sh <feature-name>

set -e

FEATURE_NAME=$1
FEATURE_PASCAL=$(echo "$FEATURE_NAME" | sed -r 's/(^|-)([a-z])/\U\2/g')

if [ -z "$FEATURE_NAME" ]; then
  echo "Usage: $0 <feature-name>"
  echo "Example: $0 user-profile"
  exit 1
fi

echo "=== Feature Workflow Gate Check: $FEATURE_NAME ==="
echo ""

# Gate 1: Worktree Check
echo "Gate 1: Worktree Setup"
echo -n "  [1.1] Worktree exists: "
git worktree list | grep -q "$FEATURE_NAME" && echo "✅" || echo "❌"

echo -n "  [1.2] On feature branch: "
CURRENT_BRANCH=$(git branch --show-current)
[[ "$CURRENT_BRANCH" == feature/* ]] && echo "✅ ($CURRENT_BRANCH)" || echo "❌ ($CURRENT_BRANCH)"

echo -n "  [1.3] Dependencies installed: "
test -d node_modules && echo "✅" || echo "❌"
echo ""

# Gate 2: Tests Written
echo "Gate 2: TDD - Tests First"
echo -n "  [2.1] E2E test file exists: "
E2E_FILE="tests/e2e/${FEATURE_NAME}.spec.ts"
test -f "$E2E_FILE" && echo "✅ ($E2E_FILE)" || echo "❌ ($E2E_FILE not found)"

if [ -f "$E2E_FILE" ]; then
  echo -n "  [2.2] Test cases count: "
  TEST_COUNT=$(grep -c "test(" "$E2E_FILE" 2>/dev/null || echo "0")
  [ "$TEST_COUNT" -ge 2 ] && echo "✅ ($TEST_COUNT tests)" || echo "⚠️ ($TEST_COUNT tests, need 2+)"
fi
echo ""

# Gate 3: Implementation
echo "Gate 3: Implementation"
echo -n "  [3.1] Types defined: "
grep -rq "${FEATURE_PASCAL}" src/types/*.ts 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.2] Query keys: "
grep -q "${FEATURE_NAME}Keys\|${FEATURE_PASCAL}Keys" src/api/queryKeys.ts 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.3] API file: "
API_FILE="src/api/${FEATURE_NAME}.ts"
test -f "$API_FILE" && echo "✅" || echo "❌"

echo -n "  [3.4] Page component: "
PAGE_FILE="src/pages/${FEATURE_PASCAL}Page.tsx"
test -f "$PAGE_FILE" && echo "✅" || echo "❌"

echo -n "  [3.5] Route in App.tsx: "
grep -q "/${FEATURE_NAME}\|/${FEATURE_PASCAL}" src/App.tsx 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.6] Navigation in AdminLayout: "
grep -q "/${FEATURE_NAME}\|${FEATURE_PASCAL}" src/components/layout/AdminLayout.tsx 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.7] Translation (ko): "
grep -q "${FEATURE_NAME}" src/locales/ko.json 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.8] Translation (en): "
grep -q "${FEATURE_NAME}" src/locales/en.json 2>/dev/null && echo "✅" || echo "❌"

if [ -f "$API_FILE" ]; then
  echo -n "  [3.9] Toast in mutations: "
  grep -A5 "useMutation" "$API_FILE" 2>/dev/null | grep -q "toast" && echo "✅" || echo "⚠️ (check if mutation exists)"
fi
echo ""

# Gate 4: Build
echo "Gate 4: Build & Lint"
echo -n "  [4.1] TypeScript check: "
pnpm tsc --noEmit > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.2] Build: "
pnpm build > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.3] Lint: "
pnpm lint > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.4] Build output: "
test -d dist && echo "✅" || echo "❌"
echo ""

# Gate 5: Tests Pass
echo "Gate 5: Local Testing"
echo -n "  [5.1] Backend health: "
curl -s http://localhost:8100/health 2>/dev/null | grep -q "ok" && echo "✅" || echo "⚠️ (backend not running)"

echo -n "  [5.2] Frontend running: "
curl -s http://localhost:3001 > /dev/null 2>&1 && echo "✅" || echo "⚠️ (frontend not running)"

if [ -f "$E2E_FILE" ]; then
  echo -n "  [5.3] E2E tests: "
  pnpm test:e2e "$E2E_FILE" > /dev/null 2>&1 && echo "✅" || echo "❌"
fi
echo ""

# Gate 6: Code Review
echo "Gate 6: Code Review"
echo "  [6.1] Run code review manually with superpowers:code-reviewer"
echo ""

# Gate 7: Git Status
echo "Gate 7: Commit & Push"
echo -n "  [7.1] No unstaged changes: "
UNSTAGED=$(git status --porcelain | grep -v "^?" | wc -l | tr -d ' ')
[ "$UNSTAGED" -eq 0 ] && echo "✅" || echo "⚠️ ($UNSTAGED files)"

echo -n "  [7.2] Latest commit: "
git log --oneline -1

echo -n "  [7.3] Push status: "
git status | grep -q "Your branch is up to date\|nothing to commit" && echo "✅ (up to date)" || echo "⚠️ (needs push)"
echo ""

echo "=== Gate Check Complete ==="
