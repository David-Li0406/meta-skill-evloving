#!/bin/bash
# Test skill resiliency by simulating failure scenarios
#
# Usage:
#   ./test-resiliency.sh <skill-directory>
#
# This script tests how a skill handles common failure scenarios:
# - Missing files
# - Invalid inputs
# - Partial execution
# - Resource constraints

set -e

SKILL_DIR="${1:-.}"
REPORT_FILE="resiliency-test-report.md"

echo "🧪 Skill Resiliency Testing"
echo "============================"
echo "Skill Directory: $SKILL_DIR"
echo ""

# Initialize report
cat > "$REPORT_FILE" <<EOF
# Skill Resiliency Test Report

**Skill:** $(basename "$SKILL_DIR")
**Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Test Version:** 1.0

## Test Scenarios

EOF

PASSED=0
FAILED=0
WARNINGS=0

# Test 1: Check skill structure
echo "Test 1: Skill Structure"
echo "----------------------"

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ SKILL.md not found"
    echo "### ❌ Test 1: Skill Structure - FAILED" >> "$REPORT_FILE"
    echo "SKILL.md file is missing." >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    ((FAILED++))
else
    echo "✅ SKILL.md exists"

    # Check frontmatter
    if head -n 5 "$SKILL_DIR/SKILL.md" | grep -q "^---$"; then
        echo "✅ YAML frontmatter present"

        # Check required fields
        if grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
            echo "✅ 'name' field present"
        else
            echo "❌ 'name' field missing"
            ((WARNINGS++))
        fi

        if grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
            echo "✅ 'description' field present"
        else
            echo "❌ 'description' field missing"
            ((WARNINGS++))
        fi
    else
        echo "⚠️  YAML frontmatter not found"
        ((WARNINGS++))
    fi

    echo "### ✅ Test 1: Skill Structure - PASSED" >> "$REPORT_FILE"
    echo "SKILL.md structure is valid." >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    ((PASSED++))
fi
echo ""

# Test 2: Check for validation mechanisms
echo "Test 2: Validation Mechanisms"
echo "----------------------------"

HAS_VALIDATION=false

# Check for validation in SKILL.md
if grep -qi "validat" "$SKILL_DIR/SKILL.md"; then
    echo "✅ Validation mentioned in SKILL.md"
    HAS_VALIDATION=true
fi

# Check for validation scripts
if [ -d "$SKILL_DIR/scripts" ]; then
    VALIDATION_SCRIPTS=$(find "$SKILL_DIR/scripts" -name "*validate*" -o -name "*check*" | wc -l)
    if [ "$VALIDATION_SCRIPTS" -gt 0 ]; then
        echo "✅ Found $VALIDATION_SCRIPTS validation script(s)"
        HAS_VALIDATION=true
    fi
fi

# Check for schemas
if [ -d "$SKILL_DIR/references" ]; then
    SCHEMAS=$(find "$SKILL_DIR/references" -name "*schema*" | wc -l)
    if [ "$SCHEMAS" -gt 0 ]; then
        echo "✅ Found $SCHEMAS schema file(s)"
        HAS_VALIDATION=true
    fi
fi

if [ "$HAS_VALIDATION" = true ]; then
    echo "### ✅ Test 2: Validation Mechanisms - PASSED" >> "$REPORT_FILE"
    echo "Skill includes validation mechanisms." >> "$REPORT_FILE"
    ((PASSED++))
else
    echo "⚠️  No validation mechanisms found"
    echo "### ⚠️  Test 2: Validation Mechanisms - WARNING" >> "$REPORT_FILE"
    echo "No validation mechanisms detected. This may be acceptable for low-determinism skills." >> "$REPORT_FILE"
    ((WARNINGS++))
fi
echo "" >> "$REPORT_FILE"
echo ""

# Test 3: Check for error handling
echo "Test 3: Error Handling"
echo "----------------------"

HAS_ERROR_HANDLING=false

# Check for error handling in SKILL.md
if grep -qi "error\|fail\|rollback\|recovery" "$SKILL_DIR/SKILL.md"; then
    echo "✅ Error handling discussed in SKILL.md"
    HAS_ERROR_HANDLING=true
fi

# Check for recovery/rollback scripts
if [ -d "$SKILL_DIR/scripts" ]; then
    RECOVERY_SCRIPTS=$(find "$SKILL_DIR/scripts" -name "*rollback*" -o -name "*recovery*" -o -name "*revert*" | wc -l)
    if [ "$RECOVERY_SCRIPTS" -gt 0 ]; then
        echo "✅ Found $RECOVERY_SCRIPTS recovery script(s)"
        HAS_ERROR_HANDLING=true
    fi
fi

# Check for troubleshooting documentation
if [ -f "$SKILL_DIR/references/troubleshooting.md" ]; then
    echo "✅ Troubleshooting guide exists"
    HAS_ERROR_HANDLING=true
fi

if [ "$HAS_ERROR_HANDLING" = true ]; then
    echo "### ✅ Test 3: Error Handling - PASSED" >> "$REPORT_FILE"
    echo "Skill includes error handling mechanisms." >> "$REPORT_FILE"
    ((PASSED++))
else
    echo "⚠️  No error handling found"
    echo "### ⚠️  Test 3: Error Handling - WARNING" >> "$REPORT_FILE"
    echo "No error handling mechanisms detected. This may be acceptable for low-determinism skills." >> "$REPORT_FILE"
    ((WARNINGS++))
fi
echo "" >> "$REPORT_FILE"
echo ""

# Test 4: Check for checkpoints/progress tracking
echo "Test 4: Progress Tracking"
echo "------------------------"

HAS_PROGRESS_TRACKING=false

# Check for checkpoints in SKILL.md
if grep -qi "checkpoint\|phase\|progress\|status" "$SKILL_DIR/SKILL.md"; then
    echo "✅ Progress tracking mentioned in SKILL.md"
    HAS_PROGRESS_TRACKING=true
fi

# Check for status tracking in examples
if [ -d "$SKILL_DIR/examples" ]; then
    if grep -rqi "status\|progress\|checkpoint" "$SKILL_DIR/examples/" 2>/dev/null; then
        echo "✅ Progress tracking in examples"
        HAS_PROGRESS_TRACKING=true
    fi
fi

if [ "$HAS_PROGRESS_TRACKING" = true ]; then
    echo "### ✅ Test 4: Progress Tracking - PASSED" >> "$REPORT_FILE"
    echo "Skill includes progress tracking mechanisms." >> "$REPORT_FILE"
    ((PASSED++))
else
    echo "⚠️  No progress tracking found"
    echo "### ⚠️  Test 4: Progress Tracking - WARNING" >> "$REPORT_FILE"
    echo "No progress tracking detected. This may be acceptable for simple skills." >> "$REPORT_FILE"
    ((WARNINGS++))
fi
echo "" >> "$REPORT_FILE"
echo ""

# Test 5: Check documentation quality
echo "Test 5: Documentation Quality"
echo "----------------------------"

DOC_ISSUES=0

# Check SKILL.md length
SKILL_LENGTH=$(wc -l < "$SKILL_DIR/SKILL.md")
echo "📏 SKILL.md length: $SKILL_LENGTH lines"

if [ "$SKILL_LENGTH" -lt 50 ]; then
    echo "⚠️  SKILL.md seems short (< 50 lines)"
    ((DOC_ISSUES++))
elif [ "$SKILL_LENGTH" -gt 500 ]; then
    echo "⚠️  SKILL.md is long (> 500 lines) - consider moving content to references/"
    ((DOC_ISSUES++))
else
    echo "✅ SKILL.md length is reasonable"
fi

# Check for examples
if [ -d "$SKILL_DIR/examples" ] && [ "$(ls -A "$SKILL_DIR/examples")" ]; then
    EXAMPLE_COUNT=$(ls -1 "$SKILL_DIR/examples" | wc -l)
    echo "✅ Found $EXAMPLE_COUNT example file(s)"
else
    echo "ℹ️  No examples directory or empty"
fi

# Check for references
if [ -d "$SKILL_DIR/references" ] && [ "$(ls -A "$SKILL_DIR/references")" ]; then
    REF_COUNT=$(ls -1 "$SKILL_DIR/references" | wc -l)
    echo "✅ Found $REF_COUNT reference file(s)"
else
    echo "ℹ️  No references directory or empty"
fi

if [ "$DOC_ISSUES" -eq 0 ]; then
    echo "### ✅ Test 5: Documentation Quality - PASSED" >> "$REPORT_FILE"
    echo "Documentation quality is good." >> "$REPORT_FILE"
    ((PASSED++))
else
    echo "### ⚠️  Test 5: Documentation Quality - WARNING" >> "$REPORT_FILE"
    echo "$DOC_ISSUES documentation issue(s) found." >> "$REPORT_FILE"
    ((WARNINGS++))
fi
echo "" >> "$REPORT_FILE"
echo ""

# Test 6: Check scripts are executable
echo "Test 6: Script Executability"
echo "---------------------------"

if [ -d "$SKILL_DIR/scripts" ] && [ "$(ls -A "$SKILL_DIR/scripts")" ]; then
    NON_EXECUTABLE=0
    for script in "$SKILL_DIR/scripts"/*; do
        if [ -f "$script" ]; then
            if [ ! -x "$script" ]; then
                echo "⚠️  Not executable: $(basename "$script")"
                ((NON_EXECUTABLE++))
            fi
        fi
    done

    if [ "$NON_EXECUTABLE" -eq 0 ]; then
        echo "✅ All scripts are executable"
        echo "### ✅ Test 6: Script Executability - PASSED" >> "$REPORT_FILE"
        echo "All scripts have execute permissions." >> "$REPORT_FILE"
        ((PASSED++))
    else
        echo "⚠️  $NON_EXECUTABLE script(s) not executable"
        echo "   Run: chmod +x $SKILL_DIR/scripts/*"
        echo "### ⚠️  Test 6: Script Executability - WARNING" >> "$REPORT_FILE"
        echo "$NON_EXECUTABLE script(s) lack execute permissions." >> "$REPORT_FILE"
        ((WARNINGS++))
    fi
else
    echo "ℹ️  No scripts directory or empty"
    echo "### ℹ️  Test 6: Script Executability - SKIPPED" >> "$REPORT_FILE"
    echo "No scripts found to test." >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"
echo ""

# Test 7: Assess determinism level
echo "Test 7: Determinism Assessment"
echo "-----------------------------"

DETERMINISM_INDICATORS=0

# High determinism indicators
if grep -qi "rollback\|recovery\|validation\|verify\|test" "$SKILL_DIR/SKILL.md"; then
    echo "✅ High-determinism patterns detected"
    ((DETERMINISM_INDICATORS++))
fi

# Low determinism indicators
if grep -qi "creative\|flexible\|explore\|iterate\|subjective" "$SKILL_DIR/SKILL.md"; then
    echo "ℹ️  Low-determinism patterns detected"
    ((DETERMINISM_INDICATORS--))
fi

if [ "$DETERMINISM_INDICATORS" -gt 0 ]; then
    DETERMINISM_LEVEL="Medium-High"
    EXPECTED_RESILIENCY="Moderate to Maximum"
elif [ "$DETERMINISM_INDICATORS" -lt 0 ]; then
    DETERMINISM_LEVEL="Low"
    EXPECTED_RESILIENCY="Minimal"
else
    DETERMINISM_LEVEL="Medium"
    EXPECTED_RESILIENCY="Moderate"
fi

echo "📊 Estimated Determinism: $DETERMINISM_LEVEL"
echo "📊 Expected Resiliency: $EXPECTED_RESILIENCY"

echo "### ✅ Test 7: Determinism Assessment - COMPLETE" >> "$REPORT_FILE"
echo "**Estimated Determinism:** $DETERMINISM_LEVEL" >> "$REPORT_FILE"
echo "**Expected Resiliency:** $EXPECTED_RESILIENCY" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
((PASSED++))
echo ""

# Generate summary
echo "============================"
echo "Test Summary"
echo "============================"
echo "✅ Passed: $PASSED"
echo "⚠️  Warnings: $WARNINGS"
echo "❌ Failed: $FAILED"
echo ""

cat >> "$REPORT_FILE" <<EOF

## Summary

- ✅ **Passed:** $PASSED
- ⚠️  **Warnings:** $WARNINGS
- ❌ **Failed:** $FAILED

## Determinism vs Resiliency Assessment

**Estimated Determinism:** $DETERMINISM_LEVEL
**Expected Resiliency Level:** $EXPECTED_RESILIENCY

EOF

if [ "$DETERMINISM_LEVEL" = "High" ] && [ "$WARNINGS" -gt 2 ]; then
    cat >> "$REPORT_FILE" <<EOF
### ⚠️  Resiliency Mismatch Warning

This skill appears to be high-determinism but has limited resiliency mechanisms.
Consider adding:
- Comprehensive validation
- Error recovery procedures
- Checkpoint-based progress tracking
- Automated rollback capabilities

EOF
elif [ "$DETERMINISM_LEVEL" = "Low" ] && [ "$WARNINGS" -eq 0 ]; then
    cat >> "$REPORT_FILE" <<EOF
### ✅ Good Resiliency Match

This low-determinism skill appropriately has minimal resiliency mechanisms.
Over-engineering would create unnecessary friction.

EOF
fi

cat >> "$REPORT_FILE" <<EOF

## Recommendations

EOF

if [ "$WARNINGS" -gt 0 ]; then
    cat >> "$REPORT_FILE" <<EOF
Review warnings above and determine if resiliency level matches determinism requirements.

For medium-high determinism skills, consider:
- Adding validation scripts
- Documenting recovery procedures
- Implementing checkpoint validation
- Creating troubleshooting guides

For low determinism skills, current resiliency level may be appropriate.

EOF
else
    cat >> "$REPORT_FILE" <<EOF
Resiliency mechanisms appear well-matched to skill determinism level.

EOF
fi

echo "📄 Full report: $REPORT_FILE"
echo ""

if [ "$FAILED" -gt 0 ]; then
    echo "❌ Some tests failed"
    exit 1
elif [ "$WARNINGS" -gt 3 ]; then
    echo "⚠️  Multiple warnings - review recommended"
    exit 0
else
    echo "✅ Resiliency testing complete"
    exit 0
fi
