#!/bin/bash
# Feature Workflow Gate Check Script (Go + Gin)
# Usage: ./check-gates-go-gin.sh <feature-name>

set -e

FEATURE_NAME=$1
FEATURE_PASCAL=$(echo "$FEATURE_NAME" | sed -r 's/(^|_)([a-z])/\U\2/g')

if [ -z "$FEATURE_NAME" ]; then
  echo "Usage: $0 <feature-name>"
  echo "Example: $0 user_profile"
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

echo -n "  [1.3] Dependencies verified: "
go mod verify > /dev/null 2>&1 && echo "✅" || echo "❌"
echo ""

# Gate 2: Tests Written
echo "Gate 2: TDD - Tests First"
echo -n "  [2.1] Handler test file exists: "
HANDLER_TEST="internal/handlers/${FEATURE_NAME}_handler_test.go"
test -f "$HANDLER_TEST" && echo "✅ ($HANDLER_TEST)" || echo "❌ ($HANDLER_TEST not found)"

if [ -f "$HANDLER_TEST" ]; then
  echo -n "  [2.2] Test functions count: "
  TEST_COUNT=$(grep -c "func Test" "$HANDLER_TEST" 2>/dev/null || echo "0")
  [ "$TEST_COUNT" -ge 2 ] && echo "✅ ($TEST_COUNT tests)" || echo "⚠️ ($TEST_COUNT tests, need 2+)"
fi
echo ""

# Gate 3: Implementation
echo "Gate 3: Implementation"
echo -n "  [3.1] Model exists: "
test -f "internal/models/${FEATURE_NAME}.go" && echo "✅" || echo "❌"

echo -n "  [3.2] Migration exists: "
ls migrations/*_create_${FEATURE_NAME}s.up.sql > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [3.3] Repository exists: "
test -f "internal/repository/${FEATURE_NAME}_repository.go" && echo "✅" || echo "❌"

echo -n "  [3.4] Service exists: "
test -f "internal/services/${FEATURE_NAME}_service.go" && echo "✅" || echo "❌"

echo -n "  [3.5] Handler exists: "
test -f "internal/handlers/${FEATURE_NAME}_handler.go" && echo "✅" || echo "❌"

echo -n "  [3.6] Mock added: "
grep -q "Mock${FEATURE_PASCAL}Repository" internal/testutil/mocks.go 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.7] fx repo registration: "
grep -q "New${FEATURE_PASCAL}Repository" internal/app/repository.go 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.8] fx service registration: "
grep -q "New${FEATURE_PASCAL}Service" internal/app/service.go 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.9] fx handler registration: "
grep -q "New${FEATURE_PASCAL}Handler" internal/app/handler.go 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.10] Router registration: "
grep -q "/${FEATURE_NAME}s" internal/router/router.go 2>/dev/null && echo "✅" || echo "❌"
echo ""

# Gate 4: Build
echo "Gate 4: Build & Test"
echo -n "  [4.1] Build succeeds: "
go build ./... > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.2] Vet passes: "
go vet ./... > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.3] Unit tests pass: "
go test ./... -short > /dev/null 2>&1 && echo "✅" || echo "❌"
echo ""

# Gate 5: Swagger
echo "Gate 5: Swagger Update"
echo -n "  [5.1] Swagger generation: "
make swagger > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [5.2] Endpoint documented: "
grep -q "/${FEATURE_NAME}s" docs/swagger.json 2>/dev/null && echo "✅" || echo "❌"
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
