#!/bin/bash
# run-tests.sh - Test suite for validator.sh
#
# Runs validator against test specs and verifies expected results.
# Exit code: 0 if all tests pass, 1 if any fail.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="$SCRIPT_DIR/../validator.sh"
DOMAINS_DIR="$SCRIPT_DIR/../../domains"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Invariant Validator Test Suite${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Check validator exists
if [[ ! -f "$VALIDATOR" ]]; then
    echo -e "${RED}ERROR: validator.sh not found at $VALIDATOR${NC}"
    exit 1
fi

# Make validator executable
chmod +x "$VALIDATOR"

# Function to run a test
run_test() {
    local test_name="$1"
    local spec_file="$2"
    local domain_args="$3"
    local expected_exit_code="$4"
    local expected_violations="$5"
    local expected_warnings="$6"

    ((TESTS_RUN++))

    echo -e "${BLUE}Test: $test_name${NC}"
    echo "  Spec: $spec_file"
    if [[ -n "$domain_args" ]]; then
        echo "  Domain: $domain_args"
    fi
    echo "  Expected: exit=$expected_exit_code, violations=$expected_violations, warnings=$expected_warnings"

    # Run validator and capture output
    local output
    local actual_exit_code=0

    if [[ -n "$domain_args" ]]; then
        output=$("$VALIDATOR" "$spec_file" --domain "$DOMAINS_DIR/$domain_args" 2>&1) || actual_exit_code=$?
    else
        output=$("$VALIDATOR" "$spec_file" 2>&1) || actual_exit_code=$?
    fi

    # Count violations and warnings from output
    local actual_violations
    local actual_warnings
    actual_violations=$(echo "$output" | grep -c "❌ VIOLATION" || true)
    actual_warnings=$(echo "$output" | grep -c "⚠️  WARNING" || true)
    actual_violations=${actual_violations:-0}
    actual_warnings=${actual_warnings:-0}

    # Check results
    local test_passed=true
    local failure_reasons=""

    if [[ "$actual_exit_code" != "$expected_exit_code" ]]; then
        test_passed=false
        failure_reasons="${failure_reasons}\n    - Exit code: expected $expected_exit_code, got $actual_exit_code"
    fi

    # For violations, check if actual meets minimum expected
    # (specs may trigger more violations than the specific ones we're testing)
    if [[ "$actual_violations" -lt "$expected_violations" ]]; then
        test_passed=false
        failure_reasons="${failure_reasons}\n    - Violations: expected at least $expected_violations, got $actual_violations"
    fi

    # For warnings, check if actual meets minimum expected
    if [[ "$actual_warnings" -lt "$expected_warnings" ]]; then
        test_passed=false
        failure_reasons="${failure_reasons}\n    - Warnings: expected at least $expected_warnings, got $actual_warnings"
    fi

    if [[ "$test_passed" == true ]]; then
        echo -e "  ${GREEN}✓ PASSED${NC} (violations=$actual_violations, warnings=$actual_warnings)"
        ((TESTS_PASSED++))
    else
        echo -e "  ${RED}✗ FAILED${NC}"
        echo -e "${RED}$failure_reasons${NC}"
        echo ""
        echo "  --- Validator Output (truncated) ---"
        echo "$output" | head -50
        echo "  --- End Output ---"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# ============================================================================
# Test 1: Bad Universal Spec (should fail with violations)
# ============================================================================
run_test \
    "bad-spec-universal.md (10 universal invariant violations)" \
    "$SCRIPT_DIR/bad-spec-universal.md" \
    "" \
    1 \
    10 \
    0

# ============================================================================
# Test 2: Good Universal Spec (should pass clean)
# ============================================================================
run_test \
    "good-spec-universal.md (all universal invariants pass)" \
    "$SCRIPT_DIR/good-spec-universal.md" \
    "" \
    0 \
    0 \
    0

# ============================================================================
# Test 3: Bad Capability Spec (should fail with skill gap violations)
# ============================================================================
run_test \
    "bad-spec-capability.md (skill gap + universal violations)" \
    "$SCRIPT_DIR/bad-spec-capability.md" \
    "skill-gap-transcendence.md" \
    1 \
    5 \
    0

# ============================================================================
# Test 4: Bad Consumer Spec (triggers both universal violations and domain warnings)
# ============================================================================
run_test \
    "bad-spec-consumer.md (consumer product + universal violations)" \
    "$SCRIPT_DIR/bad-spec-consumer.md" \
    "consumer-product.md" \
    1 \
    5 \
    3

# ============================================================================
# Test 5: Bad Construction Spec (triggers both universal violations and domain warnings)
# ============================================================================
run_test \
    "bad-spec-construction.md (construction + universal violations)" \
    "$SCRIPT_DIR/bad-spec-construction.md" \
    "physical-construction.md" \
    1 \
    5 \
    1

# ============================================================================
# Summary
# ============================================================================
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ $TESTS_FAILED test(s) failed${NC}"
    exit 1
fi
