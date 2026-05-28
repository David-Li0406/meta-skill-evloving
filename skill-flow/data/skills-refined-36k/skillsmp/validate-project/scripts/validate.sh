#!/bin/bash
# Validation script for AI/MCP monorepo projects
# Level 3 resource - loaded on-demand when full script needed
set -e

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 Validating project..."

# Track failures
FAILED=0

# Function to report step status
report_step() {
    local step_name="$1"
    local status="$2"
    if [ "$status" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $step_name"
    else
        echo -e "${RED}✗${NC} $step_name"
        FAILED=1
    fi
}

# Detect project type
if [ -f "go.mod" ]; then
    echo "📦 Detected Go project"

    # 1. Generate code
    if grep -rq "go:generate" *.go 2>/dev/null || grep -rq "go:generate" **/*.go 2>/dev/null; then
        go generate ./... 2>/dev/null
        report_step "go generate" $?
    else
        echo -e "${YELLOW}⊘${NC} go generate (no directives found)"
    fi

    # 2. Tidy dependencies
    go mod tidy
    report_step "go mod tidy" $?

    # 3. Format code
    go fmt ./...
    report_step "go fmt" $?

    # 4. Lint
    if [ -f ".golangci.yml" ] || [ -f ".golangci.yaml" ]; then
        golangci-lint run
        report_step "golangci-lint" $?
    else
        echo -e "${YELLOW}⊘${NC} golangci-lint (no config found)"
    fi

    # 5. Vet
    go vet ./...
    report_step "go vet" $?

    # 6. Test
    go test -short ./...
    report_step "go test -short" $?
fi

# Frontend validation
if [ -d "ui/user" ] && [ -f "ui/user/package.json" ]; then
    echo ""
    echo "📦 Detected frontend (ui/user)"
    cd ui/user

    if command -v pnpm &> /dev/null; then
        pnpm run ci 2>/dev/null || pnpm run lint && pnpm run check
        report_step "frontend validation" $?
    else
        echo -e "${YELLOW}⊘${NC} pnpm not found, skipping frontend"
    fi

    cd - > /dev/null
fi

# Clean check
echo ""
echo "🧹 Checking for uncommitted changes..."
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo -e "${RED}✗${NC} Uncommitted changes detected:"
    git status --short
    FAILED=1
else
    echo -e "${GREEN}✓${NC} Working directory clean"
fi

# Final report
echo ""
if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}✅ All validations passed!${NC}"
    echo "Ready to commit."
    exit 0
else
    echo -e "${RED}❌ Validation failed${NC}"
    echo "Fix the issues above and run validation again."
    exit 1
fi
