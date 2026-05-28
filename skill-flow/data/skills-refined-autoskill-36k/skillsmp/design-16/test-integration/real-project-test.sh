#!/bin/bash
# real-project-test.sh - End-to-end integration test for Design Ops v2.0
#
# Tests the complete pipeline:
#   Spec → Validate → Generate PRP → Quality Check
#
# Usage: ./real-project-test.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGNOPS_ROOT="$(dirname "$SCRIPT_DIR")"
ENFORCEMENT_DIR="$DESIGNOPS_ROOT/enforcement"

# Test artifacts
TEST_PROJECT="$SCRIPT_DIR/test-project"
TEST_SPEC="$SCRIPT_DIR/test-spec.md"

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Design Ops v2.0 - End-to-End Integration Test${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Testing complete pipeline: Spec → Validate → PRP → Quality Check"
echo ""

# ============================================================================
# Helper Functions
# ============================================================================

run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit="$3"

    ((TESTS_RUN++))
    echo -e "${BLUE}Test $TESTS_RUN: $test_name${NC}"

    local actual_exit=0
    eval "$test_command" > /tmp/test_output.txt 2>&1 || actual_exit=$?

    if [[ "$actual_exit" == "$expected_exit" ]]; then
        echo -e "  ${GREEN}✓ PASSED${NC} (exit code: $actual_exit)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "  ${RED}✗ FAILED${NC} (expected exit: $expected_exit, got: $actual_exit)"
        echo "  --- Output ---"
        cat /tmp/test_output.txt | head -20
        echo "  --- End ---"
        ((TESTS_FAILED++))
        return 1
    fi
}

check_file_exists() {
    local file="$1"
    local description="$2"

    ((TESTS_RUN++))
    echo -e "${BLUE}Test $TESTS_RUN: $description${NC}"

    if [[ -f "$file" ]]; then
        echo -e "  ${GREEN}✓ PASSED${NC} (file exists)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "  ${RED}✗ FAILED${NC} (file not found: $file)"
        ((TESTS_FAILED++))
        return 1
    fi
}

check_file_contains() {
    local file="$1"
    local pattern="$2"
    local description="$3"

    ((TESTS_RUN++))
    echo -e "${BLUE}Test $TESTS_RUN: $description${NC}"

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "  ${GREEN}✓ PASSED${NC} (pattern found)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "  ${RED}✗ FAILED${NC} (pattern not found: $pattern)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# ============================================================================
# Pre-flight Checks
# ============================================================================

echo -e "${BLUE}─── Pre-flight Checks ───${NC}"
echo ""

# Check required scripts exist
check_file_exists "$ENFORCEMENT_DIR/validator.sh" "validator.sh exists"
check_file_exists "$ENFORCEMENT_DIR/spec-to-prp.sh" "spec-to-prp.sh exists"
check_file_exists "$ENFORCEMENT_DIR/prp-checker.sh" "prp-checker.sh exists"
check_file_exists "$TEST_SPEC" "test-spec.md exists"

# Make scripts executable
chmod +x "$ENFORCEMENT_DIR/validator.sh" 2>/dev/null || true
chmod +x "$ENFORCEMENT_DIR/spec-to-prp.sh" 2>/dev/null || true
chmod +x "$ENFORCEMENT_DIR/prp-checker.sh" 2>/dev/null || true

echo ""

# ============================================================================
# Step 1: Initialize Test Project
# ============================================================================

echo -e "${BLUE}─── Step 1: Initialize Test Project ───${NC}"
echo ""

# Clean up previous test run
if [[ -d "$TEST_PROJECT" ]]; then
    rm -rf "$TEST_PROJECT"
fi

# Create project structure
mkdir -p "$TEST_PROJECT/docs/design"/{research,personas,journeys,specs,tests,PRPs,assets}

# Copy test spec
cp "$TEST_SPEC" "$TEST_PROJECT/docs/design/specs/S-001-user-dashboard.md"

check_file_exists "$TEST_PROJECT/docs/design/specs/S-001-user-dashboard.md" "Spec copied to project structure"

echo ""

# ============================================================================
# Step 2: Validate Spec
# ============================================================================

echo -e "${BLUE}─── Step 2: Validate Spec ───${NC}"
echo ""

SPEC_PATH="$TEST_PROJECT/docs/design/specs/S-001-user-dashboard.md"

# Test: Spec should pass validation
run_test "Spec passes universal invariant validation" \
    "\"$ENFORCEMENT_DIR/validator.sh\" \"$SPEC_PATH\"" \
    0

# Test: Validation output should show success
"$ENFORCEMENT_DIR/validator.sh" "$SPEC_PATH" > /tmp/validation_output.txt 2>&1 || true
check_file_contains "/tmp/validation_output.txt" "No blocking violations\|Spec can proceed\|✅" "Validation shows success message"

echo ""

# ============================================================================
# Step 3: Generate PRP
# ============================================================================

echo -e "${BLUE}─── Step 3: Generate PRP ───${NC}"
echo ""

PRP_OUTPUT="$TEST_PROJECT/docs/design/PRPs/user-dashboard-prp.md"

# Test: PRP generation should succeed
run_test "PRP generation completes successfully" \
    "\"$ENFORCEMENT_DIR/spec-to-prp.sh\" \"$SPEC_PATH\" --output \"$PRP_OUTPUT\" --skip-validation" \
    0

# Test: PRP file should exist
check_file_exists "$PRP_OUTPUT" "PRP file created"

# Test: PRP should have required sections
if [[ -f "$PRP_OUTPUT" ]]; then
    check_file_contains "$PRP_OUTPUT" "Success Criteria\|Success criteria" "PRP contains Success Criteria section"
    check_file_contains "$PRP_OUTPUT" "Timeline\|Phase" "PRP contains Timeline section"
    check_file_contains "$PRP_OUTPUT" "Risk\|risk" "PRP contains Risk section"
fi

echo ""

# ============================================================================
# Step 4: Quality Check PRP
# ============================================================================

echo -e "${BLUE}─── Step 4: Quality Check PRP ───${NC}"
echo ""

# Test: PRP should pass quality check
if [[ -f "$PRP_OUTPUT" ]]; then
    run_test "PRP passes quality check" \
        "\"$ENFORCEMENT_DIR/prp-checker.sh\" \"$PRP_OUTPUT\"" \
        0

    # Test: Quality score should be reasonable
    "$ENFORCEMENT_DIR/prp-checker.sh" "$PRP_OUTPUT" > /tmp/quality_output.txt 2>&1 || true
    check_file_contains "/tmp/quality_output.txt" "Quality Score\|PASSED" "Quality check shows score"
fi

echo ""

# ============================================================================
# Step 5: Test Bad Spec Rejection
# ============================================================================

echo -e "${BLUE}─── Step 5: Test Bad Spec Rejection ───${NC}"
echo ""

# Create a bad spec that should fail validation
BAD_SPEC="$TEST_PROJECT/docs/design/specs/S-002-bad-spec.md"
cat > "$BAD_SPEC" << 'EOF'
# Spec: S-002-Bad Spec

## Overview

Build something that works properly and efficiently.
The system should handle all cases seamlessly.

## Requirements

- Make it fast
- Make it good
- Update user data
- Delete old records permanently
EOF

# Test: Bad spec should fail validation
run_test "Bad spec fails validation (expected)" \
    "\"$ENFORCEMENT_DIR/validator.sh\" \"$BAD_SPEC\"" \
    1

# Test: Validation should show violations
"$ENFORCEMENT_DIR/validator.sh" "$BAD_SPEC" > /tmp/bad_validation.txt 2>&1 || true
check_file_contains "/tmp/bad_validation.txt" "VIOLATION" "Bad spec shows violations"

echo ""

# ============================================================================
# Step 6: Test Confidence Calculator
# ============================================================================

echo -e "${BLUE}─── Step 6: Test Confidence Calculator ───${NC}"
echo ""

CONF_CALC="$ENFORCEMENT_DIR/confidence-calculator.sh"

if [[ -f "$CONF_CALC" ]]; then
    chmod +x "$CONF_CALC"

    # Test: High confidence should return PROCEED
    run_test "High confidence (8.5) returns PROCEED" \
        "\"$CONF_CALC\" 0.9 0.9 0.8 0.7 0.9" \
        0

    # Test: Low confidence should return STOP
    run_test "Low confidence (3.5) returns STOP" \
        "\"$CONF_CALC\" 0.3 0.3 0.4 0.3 0.5" \
        2
else
    echo -e "  ${YELLOW}⚠ SKIPPED: confidence-calculator.sh not found${NC}"
fi

echo ""

# ============================================================================
# Summary
# ============================================================================

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Integration Test Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

echo "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ ALL INTEGRATION TESTS PASSED!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "The complete Design Ops pipeline works:"
    echo "  ✅ Spec validation enforces invariants"
    echo "  ✅ Bad specs are rejected with clear errors"
    echo "  ✅ PRP generation produces quality output"
    echo "  ✅ Quality checker validates PRPs"
    echo "  ✅ Confidence calculator provides risk assessment"
    echo ""
    echo "Next: Use Design Ops on a real project from your vault!"
    echo ""
    exit 0
else
    echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
    echo -e "${RED}  ❌ SOME TESTS FAILED${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Review the failed tests above and fix any issues."
    echo ""
    exit 1
fi
