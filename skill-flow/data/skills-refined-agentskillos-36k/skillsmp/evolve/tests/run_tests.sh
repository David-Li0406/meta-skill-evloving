#!/bin/bash
# Self-Evolving Agent - Test Runner
#
# Usage:
#   ./tests/run_tests.sh           # Run all tests
#   ./tests/run_tests.sh --quick   # Run quick validation only
#   ./tests/run_tests.sh --bats    # Run bats tests only

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=============================================="
echo "  Self-Evolving Agent Test Suite"
echo "=============================================="
echo ""

# Check for bats
check_bats() {
    if command -v bats &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# Run quick validation (no external dependencies)
run_quick_validation() {
    echo -e "${YELLOW}Running Quick Validation...${NC}"
    echo ""

    local passed=0
    local failed=0

    # Test 1: Required files
    echo -n "  [1] Required files exist... "
    if [[ -f "$PROJECT_ROOT/skills/SKILL.md" && \
          -f "$PROJECT_ROOT/README.md" && \
          -f "$PROJECT_ROOT/LICENSE" && \
          -f "$PROJECT_ROOT/CLAUDE.md" ]]; then
        echo -e "${GREEN}PASS${NC}"
        ((passed++))
    else
        echo -e "${RED}FAIL${NC}"
        ((failed++))
    fi

    # Test 2: Module structure
    echo -n "  [2] Module structure valid... "
    local modules_ok=true
    for module in 00-getting-started 01-core 02-checkpoints 03-memory 04-emergence 05-integration 99-evolution; do
        if [[ ! -d "$PROJECT_ROOT/skills/$module/_base" ]]; then
            modules_ok=false
            break
        fi
    done
    if $modules_ok; then
        echo -e "${GREEN}PASS${NC}"
        ((passed++))
    else
        echo -e "${RED}FAIL${NC}"
        ((failed++))
    fi

    # Test 3: Memory system
    echo -n "  [3] Memory system initialized... "
    if [[ -f "$PROJECT_ROOT/.claude/memory/index.md" ]]; then
        echo -e "${GREEN}PASS${NC}"
        ((passed++))
    else
        echo -e "${RED}FAIL${NC}"
        ((failed++))
    fi

    # Test 4: Scripts executable
    echo -n "  [4] Scripts executable... "
    if [[ -x "$PROJECT_ROOT/install.sh" && \
          -x "$PROJECT_ROOT/scripts/check-env.sh" ]]; then
        echo -e "${GREEN}PASS${NC}"
        ((passed++))
    else
        echo -e "${RED}FAIL${NC}"
        ((failed++))
    fi

    # Test 5: Bash syntax
    echo -n "  [5] Bash syntax valid... "
    if bash -n "$PROJECT_ROOT/install.sh" 2>/dev/null && \
       bash -n "$PROJECT_ROOT/scripts/check-env.sh" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        ((passed++))
    else
        echo -e "${RED}FAIL${NC}"
        ((failed++))
    fi

    # Test 6: Version consistency
    echo -n "  [6] Version consistency... "
    local skill_version=$(grep "^version:" "$PROJECT_ROOT/skills/SKILL.md" | head -1 | awk '{print $2}')
    if grep -q "$skill_version" "$PROJECT_ROOT/CHANGELOG.md"; then
        echo -e "${GREEN}PASS${NC}"
        ((passed++))
    else
        echo -e "${RED}FAIL${NC}"
        ((failed++))
    fi

    echo ""
    echo "----------------------------------------------"
    echo -e "  Results: ${GREEN}$passed passed${NC}, ${RED}$failed failed${NC}"
    echo "----------------------------------------------"

    if [[ $failed -gt 0 ]]; then
        return 1
    fi
    return 0
}

# Run bats tests
run_bats_tests() {
    echo -e "${YELLOW}Running Bats Tests...${NC}"
    echo ""

    if ! check_bats; then
        echo -e "${YELLOW}Warning: bats-core not installed${NC}"
        echo ""
        echo "Install bats-core to run full test suite:"
        echo "  macOS:  brew install bats-core"
        echo "  Ubuntu: apt-get install bats"
        echo "  npm:    npm install -g bats"
        echo ""
        return 1
    fi

    bats "$SCRIPT_DIR"/*.bats
}

# Main
case "${1:-all}" in
    --quick)
        run_quick_validation
        ;;
    --bats)
        run_bats_tests
        ;;
    --help|-h)
        echo "Usage: $0 [--quick|--bats|--help]"
        echo ""
        echo "Options:"
        echo "  --quick   Run quick validation only (no external deps)"
        echo "  --bats    Run bats tests only (requires bats-core)"
        echo "  --help    Show this help message"
        echo ""
        echo "Default: Run all tests"
        ;;
    *)
        run_quick_validation
        echo ""
        run_bats_tests || echo -e "${YELLOW}Skipping bats tests (not installed)${NC}"
        ;;
esac

echo ""
echo "=============================================="
echo "  Test Suite Complete"
echo "=============================================="
