#!/bin/bash
# Feature Workflow Gate Check Script (Go + Gin + Uber fx)
# Usage: ./check-gates-go-gin-fx.sh <feature-name>

set -e

FEATURE_NAME=$1

# Input validation - only allow alphanumeric, hyphens, and underscores
if [ -z "$FEATURE_NAME" ]; then
  echo "Usage: $0 <feature-name>"
  echo "Example: $0 user_profile"
  exit 1
fi

if [[ ! "$FEATURE_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Error: Feature name must contain only alphanumeric characters, hyphens, and underscores"
  exit 1
fi

# Convert snake_case to PascalCase (portable - works on macOS and Linux)
FEATURE_PASCAL=$(echo "$FEATURE_NAME" | awk -F'_' '{
  result = ""
  for (i=1; i<=NF; i++) {
    first = toupper(substr($i, 1, 1))
    rest = substr($i, 2)
    result = result first rest
  }
  print result
}')

echo "=== Feature Workflow Gate Check (fx): $FEATURE_NAME ==="
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

echo -n "  [1.4] Uber fx present: "
grep -q "go.uber.org/fx" go.mod && echo "✅" || echo "❌"
echo ""

# Gate 2: Tests Written
echo "Gate 2: TDD - Tests First"
echo -n "  [2.1] Handler test file exists: "
HANDLER_TEST="internal/handler/${FEATURE_NAME}_test.go"
test -f "$HANDLER_TEST" && echo "✅ ($HANDLER_TEST)" || echo "❌ ($HANDLER_TEST not found)"

if [ -f "$HANDLER_TEST" ]; then
  echo -n "  [2.2] Test functions count: "
  TEST_COUNT=$(grep -c "func Test" "$HANDLER_TEST" 2>/dev/null || echo "0")
  [ "$TEST_COUNT" -ge 2 ] && echo "✅ ($TEST_COUNT tests)" || echo "⚠️ ($TEST_COUNT tests, need 2+)"
fi

echo -n "  [2.3] Uses fxtest: "
grep -q "fxtest.New" "$HANDLER_TEST" 2>/dev/null && echo "✅" || echo "⚠️ (consider using fxtest)"
echo ""

# Gate 3: Implementation
echo "Gate 3: Implementation"
echo -n "  [3.1] Model exists: "
test -f "internal/model/${FEATURE_NAME}.go" && echo "✅" || echo "❌"

echo -n "  [3.2] Migration exists: "
ls migrations/*_create_${FEATURE_NAME}s.up.sql > /dev/null 2>&1 && echo "✅" || \
  ls migrations/*_${FEATURE_NAME}*.up.sql > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [3.3] DTO exists: "
test -f "internal/dto/${FEATURE_NAME}.go" && echo "✅" || echo "⚠️ (optional)"

echo -n "  [3.4] Repository exists: "
test -f "internal/repository/${FEATURE_NAME}.go" && echo "✅" || \
  test -f "internal/repository/${FEATURE_NAME}_repository.go" && echo "✅" || echo "❌"

echo -n "  [3.5] Service exists: "
test -f "internal/service/${FEATURE_NAME}.go" && echo "✅" || \
  test -f "internal/service/${FEATURE_NAME}_service.go" && echo "✅" || echo "❌"

echo -n "  [3.6] Handler exists: "
test -f "internal/handler/${FEATURE_NAME}.go" && echo "✅" || \
  test -f "internal/handler/${FEATURE_NAME}_handler.go" && echo "✅" || echo "❌"
echo ""

# Gate 3b: fx Module Registration
echo "Gate 3b: fx Module Registration"
echo -n "  [3.7] Repository module.go: "
grep -q "New${FEATURE_PASCAL}Repository" internal/repository/module.go 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.8] Service module.go: "
grep -q "New${FEATURE_PASCAL}Service" internal/service/module.go 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.9] Handler module.go: "
grep -q "New${FEATURE_PASCAL}Handler" internal/handler/module.go 2>/dev/null && echo "✅" || echo "❌"

echo -n "  [3.10] Router registration: "
grep -q "${FEATURE_PASCAL}Handler\|/${FEATURE_NAME}s\|/${FEATURE_NAME}" internal/router/router.go 2>/dev/null && echo "✅" || echo "❌"
echo ""

# Gate 4: Build
echo "Gate 4: Build & Test"
echo -n "  [4.1] Build succeeds: "
go build ./... > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.2] Vet passes: "
go vet ./... > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.3] Unit tests pass: "
go test ./... -short > /dev/null 2>&1 && echo "✅" || echo "❌"

echo -n "  [4.4] Coverage check: "
COVERAGE=$(go test ./... -cover 2>/dev/null | grep -o 'coverage: [0-9.]*' | tail -1 | grep -o '[0-9.]*' || echo "0")
if [ ! -z "$COVERAGE" ]; then
  echo "✅ (${COVERAGE}%)"
else
  echo "⚠️ (run manually)"
fi
echo ""

# Gate 5: Swagger
echo "Gate 5: Swagger Update"
echo -n "  [5.1] Swagger generation: "
if command -v swag &> /dev/null; then
  swag init -g cmd/server/main.go -o docs > /dev/null 2>&1 && echo "✅" || \
    make swagger > /dev/null 2>&1 && echo "✅" || echo "❌"
else
  make swagger > /dev/null 2>&1 && echo "✅" || echo "⚠️ (swag not found)"
fi

echo -n "  [5.2] Endpoint documented: "
grep -q "/${FEATURE_NAME}s\|/${FEATURE_NAME}" docs/swagger.json 2>/dev/null && echo "✅" || echo "❌"
echo ""

# Gate 6: Code Review
echo "Gate 6: Code Review"
echo "  [6.1] Run code review manually with superpowers:code-reviewer"
echo "  [6.2] Verify no Critical/Important issues remain"
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

echo "=== Gate Check Complete (fx) ==="
