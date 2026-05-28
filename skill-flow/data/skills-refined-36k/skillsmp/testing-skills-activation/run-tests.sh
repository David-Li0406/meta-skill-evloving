#!/bin/bash

# Skill Activation Testing Script
# Tests whether a skill's description triggers correctly by running test cases through Claude
#
# Usage: Run from the skill directory being tested
#   cd /path/to/skill-being-tested
#   /path/to/testing-skills-activation/run-tests.sh [--auto]
#
# Options:
#   --auto    Auto-accept all detections (non-interactive mode)
#
# Expects: test-cases.json in current directory
# Outputs: Results and report to /tmp/claude/

# Parse arguments
AUTO_MODE=false
if [ "$1" = "--auto" ]; then
    AUTO_MODE=true
fi

# Get the skill directory being tested (current directory)
SKILL_DIR="$(pwd)"
SKILL_NAME=$(basename "$SKILL_DIR")
TEST_CASES_FILE="$SKILL_DIR/test-cases.json"

# Output to /tmp/claude
OUTPUT_DIR="/tmp/claude"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RESULTS_FILE="$OUTPUT_DIR/test-results-$TIMESTAMP.json"
REPORT_FILE="$OUTPUT_DIR/test-report-$TIMESTAMP.md"

echo "========================================"
echo "Skill Activation Testing"
echo "========================================"
echo ""
echo "Skill directory: $SKILL_DIR"
echo "Skill name: $SKILL_NAME"
echo "Test cases: $TEST_CASES_FILE"
echo "Results: $RESULTS_FILE"
echo "Report: $REPORT_FILE"
echo ""

# Check if test cases file exists
if [ ! -f "$TEST_CASES_FILE" ]; then
    echo "Error: test-cases.json not found in current directory"
    echo "Please create test-cases.json in the skill directory being tested"
    echo ""
    echo "See SKILL.md for test case format"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed. Install with: sudo pacman -S jq"
    exit 1
fi

# Read test cases
TEST_COUNT=$(jq 'length' "$TEST_CASES_FILE")
echo "Found $TEST_COUNT test cases"
echo ""

# Initialize results array
echo "[]" > "$RESULTS_FILE"

BATCH_SIZE=5
BATCH_NUM=1

# Run tests in batches
for batch_start in $(seq 0 $BATCH_SIZE $((TEST_COUNT - 1))); do
    batch_end=$((batch_start + BATCH_SIZE - 1))
    if [ $batch_end -ge $TEST_COUNT ]; then
        batch_end=$((TEST_COUNT - 1))
    fi

    echo ""
    echo "========================================"
    echo "BATCH $BATCH_NUM (Tests $((batch_start + 1)) - $((batch_end + 1)))"
    echo "========================================"
    echo ""

    # Collect batch responses
    declare -A BATCH_RESPONSES
    declare -A BATCH_DATA

    # Run all tests in this batch
    for i in $(seq $batch_start $batch_end); do
        # Extract test case data
        TEST_ID=$(jq -r ".[$i].id" "$TEST_CASES_FILE")
        USER_MESSAGE=$(jq -r ".[$i].user_message" "$TEST_CASES_FILE")
        PROJECT_CONTEXT=$(jq -r ".[$i].project_context" "$TEST_CASES_FILE")
        EXPECTED_ACTIVATION=$(jq -r ".[$i].expected_activation" "$TEST_CASES_FILE")
        RATIONALE=$(jq -r ".[$i].rationale" "$TEST_CASES_FILE")

        echo "Running Test #$TEST_ID..."

        # Store test data
        BATCH_DATA[$i]="$TEST_ID|$USER_MESSAGE|$PROJECT_CONTEXT|$EXPECTED_ACTIVATION|$RATIONALE"

        # Create prompt with context
        PROMPT="You are working on a project with the following context:

Project: $PROJECT_CONTEXT

The user has sent you this message:
\"$USER_MESSAGE\"

IMPORTANT RULES:
1. This is a hypothetical scenario. Assume you have full context of the codebase.
2. DO NOT actually invoke any skills or tools. DO NOT do any work.
3. DO NOT provide solutions, code, or answers to the user's question.
4. ONLY state what your very first action would be.

If you would invoke a skill, say: 'I would invoke the [skill-name] skill'
If you would use a tool, say: 'I would use the [tool-name] tool'
If you would run a command, say: 'I would run [command]'

Your response should be ONE sentence describing your intended first action, nothing more."

        # Run claude with the prompt
        RESPONSE=$(echo "$PROMPT" | claude -p 2>&1)
        BATCH_RESPONSES[$i]="$RESPONSE"
    done

    echo ""
    echo "Batch complete! Now reviewing results..."
    echo ""

    # Review batch results
    for i in $(seq $batch_start $batch_end); do
        IFS='|' read -r TEST_ID USER_MESSAGE PROJECT_CONTEXT EXPECTED_ACTIVATION RATIONALE <<< "${BATCH_DATA[$i]}"
        RESPONSE="${BATCH_RESPONSES[$i]}"

        echo "========================================="
        echo "Test Case #$TEST_ID"
        echo "Message: $USER_MESSAGE"
        echo "Context: $PROJECT_CONTEXT"
        echo "Expected: $EXPECTED_ACTIVATION"
        echo "-----------------------------------------"
        echo "Response: ${RESPONSE:0:300}..."
        echo ""

        # Use Claude to evaluate whether the response indicates skill invocation
        # This is more accurate than grep patterns
        EVAL_PROMPT="You are evaluating whether a Claude response explicitly mentions invoking a specific skill.

Skill being tested: $SKILL_NAME

Claude's response to evaluate:
\"$RESPONSE\"

Does this response explicitly mention invoking or using the '$SKILL_NAME' skill? Look for phrases like:
- 'invoke the $SKILL_NAME skill'
- 'use the $SKILL_NAME skill'
- 'I would use $SKILL_NAME'
- 'the $SKILL_NAME skill'

IMPORTANT: Only answer YES if the response explicitly mentions the skill BY NAME. Using related tools or commands (like 'bd' commands) does NOT count - we only care about explicit skill invocation.

Answer with ONLY 'YES' or 'NO' - nothing else."

        EVAL_RESULT=$(echo "$EVAL_PROMPT" | claude -p --model haiku 2>&1)

        ACTUAL_ACTIVATION="false"
        if echo "$EVAL_RESULT" | grep -i -q "^YES"; then
            ACTUAL_ACTIVATION="true"
            echo "✓ Claude evaluation: skill would be invoked"
        else
            echo "✗ Claude evaluation: skill would NOT be invoked"
        fi

        echo ""

        if [ "$AUTO_MODE" = "true" ]; then
            # Auto-accept detection in non-interactive mode
            echo "(Auto mode - accepting detection)"
        else
            echo "Correct? (y/n/override): "
            read -r VALIDATION_INPUT

            # Allow manual override
            if [ "$VALIDATION_INPUT" = "override" ]; then
                echo "Manual override - Did the skill activate? (y/n): "
                read -r OVERRIDE_INPUT
                if [ "$OVERRIDE_INPUT" = "y" ]; then
                    ACTUAL_ACTIVATION="true"
                else
                    ACTUAL_ACTIVATION="false"
                fi
            elif [ "$VALIDATION_INPUT" = "n" ]; then
                # Flip the detection
                if [ "$ACTUAL_ACTIVATION" = "true" ]; then
                    ACTUAL_ACTIVATION="false"
                else
                    ACTUAL_ACTIVATION="true"
                fi
            fi
        fi

        # Determine if test passed
        TEST_PASSED="false"
        if [ "$ACTUAL_ACTIVATION" = "$EXPECTED_ACTIVATION" ]; then
            TEST_PASSED="true"
            echo "✓ PASS"
        else
            echo "✗ FAIL"
        fi

        # Save result
        RESULT=$(jq -n \
            --arg id "$TEST_ID" \
            --arg message "$USER_MESSAGE" \
            --arg context "$PROJECT_CONTEXT" \
            --argjson expected "$EXPECTED_ACTIVATION" \
            --argjson actual "$ACTUAL_ACTIVATION" \
            --argjson passed "$TEST_PASSED" \
            --arg rationale "$RATIONALE" \
            --arg response "$RESPONSE" \
            '{
                id: $id,
                user_message: $message,
                project_context: $context,
                expected_activation: $expected,
                actual_activation: $actual,
                test_passed: $passed,
                rationale: $rationale,
                claude_response: $response
            }')

        # Append to results file
        TEMP_FILE=$(mktemp)
        jq --argjson result "$RESULT" '. += [$result]' "$RESULTS_FILE" > "$TEMP_FILE"
        mv "$TEMP_FILE" "$RESULTS_FILE"

        echo ""
    done

    BATCH_NUM=$((BATCH_NUM + 1))
done

# Generate report
echo "Generating report..."

# Calculate metrics using simpler jq filters
TOTAL_TESTS=$(jq '[.[] | select(has("test_passed"))] | length' "$RESULTS_FILE")
PASSED_TESTS=$(jq '[.[] | select(.test_passed == true)] | length' "$RESULTS_FILE")
FAILED_TESTS=$(jq '[.[] | select(.test_passed == false)] | length' "$RESULTS_FILE")
TRUE_POSITIVES=$(jq '[.[] | select(.expected_activation == true and .actual_activation == true)] | length' "$RESULTS_FILE")
TRUE_NEGATIVES=$(jq '[.[] | select(.expected_activation == false and .actual_activation == false)] | length' "$RESULTS_FILE")
FALSE_POSITIVES=$(jq '[.[] | select(.expected_activation == false and .actual_activation == true)] | length' "$RESULTS_FILE")
FALSE_NEGATIVES=$(jq '[.[] | select(.expected_activation == true and .actual_activation == false)] | length' "$RESULTS_FILE")

# Calculate accuracy percentage (handle division by zero)
if [ "$TOTAL_TESTS" -gt 0 ]; then
    ACCURACY=$(awk "BEGIN {printf \"%.0f\", ($PASSED_TESTS * 100 / $TOTAL_TESTS)}")
else
    ACCURACY="0"
fi

# Generate markdown report
cat > "$REPORT_FILE" << EOF
# Skill Activation Test Report

**Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Skill Directory:** $SKILL_DIR

## Summary

- **Total Tests:** $TOTAL_TESTS
- **Passed:** $PASSED_TESTS
- **Failed:** $FAILED_TESTS
- **Accuracy:** ${ACCURACY}%

## Confusion Matrix

|                    | Activated (Actual) | Not Activated (Actual) |
|--------------------|-------------------|------------------------|
| **Should Activate (Expected)** | $TRUE_POSITIVES (TP) | $FALSE_NEGATIVES (FN) |
| **Should NOT Activate (Expected)** | $FALSE_POSITIVES (FP) | $TRUE_NEGATIVES (TN) |

## Metrics

- **True Positives:** $TRUE_POSITIVES (correctly activated)
- **True Negatives:** $TRUE_NEGATIVES (correctly didn't activate)
- **False Positives:** $FALSE_POSITIVES (activated when shouldn't)
- **False Negatives:** $FALSE_NEGATIVES (didn't activate when should)

## Failed Test Cases

EOF

# Add failed test details to report
jq -r '.[] | select(.test_passed == false) |
"### Test #\(.id): \(if .actual_activation then "False Positive" else "False Negative" end)

**User Message:** \(.user_message)

**Project Context:** \(.project_context)

**Expected:** \(if .expected_activation then "Should activate" else "Should NOT activate" end)

**Actual:** \(if .actual_activation then "Activated" else "Did not activate" end)

**Rationale:** \(.rationale)

**Claude Response Preview:** \(.claude_response[:300])...

---
"' "$RESULTS_FILE" >> "$REPORT_FILE"

# If no failures, note that
if [ "$FAILED_TESTS" -eq 0 ]; then
    echo "No failed test cases! All tests passed. ✓" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

## Analysis

$(if [ "$FALSE_POSITIVES" -gt 0 ]; then
    echo "**False Positives:** The skill activated $FALSE_POSITIVES times when it shouldn't have. This suggests the description is too broad and needs tightening."
    echo ""
fi)
$(if [ "$FALSE_NEGATIVES" -gt 0 ]; then
    echo "**False Negatives:** The skill failed to activate $FALSE_NEGATIVES times when it should have. This suggests missing trigger keywords or patterns in the description."
    echo ""
fi)

## Recommendations

$(if [ "$FALSE_POSITIVES" -gt 0 ]; then
    echo "- Add negative examples to exclude out-of-scope scenarios"
    echo "- Tighten the description to be more specific about when to activate"
fi)
$(if [ "$FALSE_NEGATIVES" -gt 0 ]; then
    echo "- Add specific library/framework names mentioned in failed cases"
    echo "- Include trigger keywords from failed test messages"
fi)
$(if [ "$FAILED_TESTS" -eq 0 ]; then
    echo "No improvements needed - skill is activating correctly! 🎉"
fi)

## Next Steps

1. Review failed test cases above
2. Update skill description in SKILL.md based on recommendations
3. Re-run tests to measure improvement
4. Target: 90%+ accuracy

---

**Files:**
- Results: \`$(basename "$RESULTS_FILE")\`
- Test cases: \`test-cases.json\`
EOF

echo ""
echo "========================================="
echo "Test run complete!"
echo ""
echo "Results saved to: $RESULTS_FILE"
echo "Report saved to: $REPORT_FILE"
echo ""
echo "Summary:"
echo "  Total: $TOTAL_TESTS"
echo "  Passed: $PASSED_TESTS"
echo "  Failed: $FAILED_TESTS"
echo "  Accuracy: ${ACCURACY}%"
echo ""
echo "View report: cat $REPORT_FILE"
