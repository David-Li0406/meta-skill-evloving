#!/usr/bin/env bash
# Test memex-cli installation and basic functionality
# Usage: bash test-memex-cli.sh

set -e

echo "========================================="
echo "memex-cli Component Test Suite"
echo "========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Helper functions
pass_test() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
    ((TESTS_TOTAL++))
}

fail_test() {
    echo -e "${RED}✗${NC} $1"
    echo -e "${YELLOW}  $2${NC}"
    ((TESTS_FAILED++))
    ((TESTS_TOTAL++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: Check if memex-cli is installed
echo "[1/6] Checking memex-cli installation..."
if command -v memex-cli &> /dev/null; then
    pass_test "memex-cli is installed"
else
    fail_test "memex-cli not found" "Install with: npm install -g memex-cli"
    exit 1
fi

# Test 2: Check memex-cli version
echo ""
echo "[2/6] Checking memex-cli version..."
VERSION=$(memex-cli --version 2>&1 | head -n 1 || echo "unknown")
if [[ "$VERSION" != "unknown" ]]; then
    pass_test "memex-cli version: $VERSION"
else
    fail_test "Cannot determine memex-cli version" "Check installation integrity"
fi

# Test 3: Check help command
echo ""
echo "[3/6] Testing help command..."
if memex-cli --help &> /dev/null; then
    pass_test "Help command works"
else
    fail_test "Help command failed" "memex-cli may be corrupted"
fi

# Test 4: Check for API keys (optional but recommended)
echo ""
echo "[4/6] Checking API key configuration..."
KEYS_FOUND=0

if [[ -n "$ANTHROPIC_API_KEY" ]]; then
    pass_test "ANTHROPIC_API_KEY is set (Claude backend)"
    ((KEYS_FOUND++))
else
    warn "ANTHROPIC_API_KEY not set (Claude backend unavailable)"
fi

if [[ -n "$OPENAI_API_KEY" ]]; then
    pass_test "OPENAI_API_KEY is set (Codex backend)"
    ((KEYS_FOUND++))
else
    warn "OPENAI_API_KEY not set (Codex backend unavailable)"
fi

if [[ -n "$GOOGLE_API_KEY" ]] || [[ -n "$GEMINI_API_KEY" ]]; then
    pass_test "GOOGLE_API_KEY or GEMINI_API_KEY is set (Gemini backend)"
    ((KEYS_FOUND++))
else
    warn "GOOGLE_API_KEY/GEMINI_API_KEY not set (Gemini backend unavailable)"
fi

if [[ $KEYS_FOUND -eq 0 ]]; then
    fail_test "No API keys configured" "Set at least one: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY"
fi

# Test 5: Test basic execution (if API key available)
echo ""
echo "[5/6] Testing basic execution..."
if [[ -n "$ANTHROPIC_API_KEY" ]] || [[ -n "$OPENAI_API_KEY" ]]; then
    # Create a simple test prompt
    TEST_PROMPT="Output exactly: test_success"

    # Determine which backend to use
    if [[ -n "$OPENAI_API_KEY" ]]; then
        BACKEND="codex"
    else
        BACKEND="claude"
    fi

    # Run test (with timeout)
    echo "  Running test prompt with $BACKEND backend..."
    TEST_OUTPUT=$(timeout 30s memex-cli --backend "$BACKEND" --prompt "$TEST_PROMPT" 2>&1 || echo "FAILED")

    if [[ "$TEST_OUTPUT" == *"test_success"* ]]; then
        pass_test "Basic execution successful ($BACKEND backend)"
    else
        fail_test "Basic execution failed" "Output: $TEST_OUTPUT"
    fi
else
    warn "Skipping execution test (no API keys available)"
    ((TESTS_TOTAL++))
fi

# Test 6: Check Python dependencies for test scripts
echo ""
echo "[6/6] Checking Python dependencies..."
PYTHON_OK=true

if command -v python3 &> /dev/null; then
    pass_test "Python 3 is installed"

    # Check for required packages
    REQUIRED_PACKAGES=("yaml" "json")
    for pkg in "${REQUIRED_PACKAGES[@]}"; do
        if python3 -c "import $pkg" 2> /dev/null; then
            pass_test "Python package '$pkg' is available"
        else
            warn "Python package '$pkg' not found (may be needed for advanced tests)"
        fi
    done
else
    fail_test "Python 3 not found" "Install Python 3 for test scripts"
    PYTHON_OK=false
fi

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total tests: $TESTS_TOTAL"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "memex-cli is ready for use."
    exit 0
else
    echo -e "${RED}✗ Some tests failed.${NC}"
    echo ""
    echo "Please resolve the issues above before using memex-cli."
    exit 1
fi
