#!/bin/bash
# Test Runner Script with Coverage Analysis
# Usage: ./run_tests.sh [model_name|controller_name|all]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Rails Test Runner${NC}\n"

TARGET=${1:-all}

run_model_tests() {
    local model=$1
    echo -e "${YELLOW}Testing model: ${model}${NC}"

    if [ -f "test/models/${model}_test.rb" ]; then
        rails test "test/models/${model}_test.rb" -v
        echo -e "${GREEN}✓ Model tests passed${NC}\n"
    else
        echo -e "${RED}✗ Test file not found: test/models/${model}_test.rb${NC}\n"
        return 1
    fi
}

run_controller_tests() {
    local controller=$1
    echo -e "${YELLOW}Testing controller: ${controller}${NC}"

    if [ -f "test/controllers/${controller}_controller_test.rb" ]; then
        rails test "test/controllers/${controller}_controller_test.rb" -v
        echo -e "${GREEN}✓ Controller tests passed${NC}\n"
    else
        echo -e "${RED}✗ Test file not found: test/controllers/${controller}_controller_test.rb${NC}\n"
        return 1
    fi
}

run_all_tests() {
    echo -e "${BLUE}Running all tests...${NC}\n"

    # Run tests with verbose output
    rails test -v

    echo -e "\n${BLUE}📊 Test Coverage Summary${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Count test files
    model_tests=$(find test/models -name "*_test.rb" 2>/dev/null | wc -l)
    controller_tests=$(find test/controllers -name "*_test.rb" 2>/dev/null | wc -l)
    system_tests=$(find test/system -name "*_test.rb" 2>/dev/null | wc -l)

    # Count non-empty test files (files with actual test methods)
    model_tests_with_content=$(grep -l "def test_" test/models/*_test.rb 2>/dev/null | wc -l)
    controller_tests_with_content=$(grep -l "def test_" test/controllers/*_controller_test.rb 2>/dev/null | wc -l)

    echo -e "${YELLOW}Models:${NC} ${model_tests_with_content}/${model_tests} files have tests"
    echo -e "${YELLOW}Controllers:${NC} ${controller_tests_with_content}/${controller_tests} files have tests"
    echo -e "${YELLOW}System:${NC} ${system_tests} test files"

    # List empty test files
    echo -e "\n${BLUE}📝 Empty Test Files (need implementation):${NC}"
    find test/models test/controllers -name "*_test.rb" -exec sh -c '
        if ! grep -q "def test_" "$1" 2>/dev/null; then
            echo "  ⚠️  $1"
        fi
    ' sh {} \;
}

analyze_coverage() {
    echo -e "\n${BLUE}🔍 Coverage Analysis${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Models without tests
    echo -e "${YELLOW}Models without test files:${NC}"
    for model in app/models/*.rb; do
        model_name=$(basename "$model" .rb)
        if [ ! -f "test/models/${model_name}_test.rb" ]; then
            echo "  ⚠️  ${model_name}"
        fi
    done

    # Controllers without tests
    echo -e "\n${YELLOW}Controllers without test files:${NC}"
    for controller in app/controllers/*_controller.rb; do
        controller_name=$(basename "$controller" .rb)
        if [ ! -f "test/controllers/${controller_name}_test.rb" ]; then
            echo "  ⚠️  ${controller_name}"
        fi
    done
}

case $TARGET in
    all)
        run_all_tests
        analyze_coverage
        ;;
    *_controller|*Controller)
        # Strip _controller suffix if present
        controller_name=$(echo "$TARGET" | sed 's/_controller$//' | sed 's/Controller$//')
        run_controller_tests "${controller_name}"
        ;;
    *)
        # Assume it's a model name
        run_model_tests "$TARGET"
        ;;
esac

echo -e "\n${GREEN}✅ Test run complete!${NC}"
