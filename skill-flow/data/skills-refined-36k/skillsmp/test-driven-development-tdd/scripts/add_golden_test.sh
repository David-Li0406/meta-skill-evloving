#!/usr/bin/env bash
# Add a new golden test to GoldenTest.lean
# Usage: ./add_golden_test.sh <category> <test_name>

set -e

CATEGORY="$1"
TEST_NAME="$2"

if [ -z "$CATEGORY" ] || [ -z "$TEST_NAME" ]; then
    echo "Usage: $0 <category> <test_name>"
    echo "Categories: parser, infer, ir-eval"
    exit 1
fi

# Validate category
case "$CATEGORY" in
    parser|infer|ir-eval)
        ;;
    *)
        echo "Error: Invalid category. Must be one of: parser, infer, ir-eval"
        exit 1
        ;;
esac

# Determine the list name
if [ "$CATEGORY" = "ir-eval" ]; then
    LIST_NAME="irEvalTests"
else
    LIST_NAME="${CATEGORY}Tests"
fi

# Check if test already exists
if grep -q "\"$TEST_NAME\"" tests/GoldenTest.lean; then
    echo "Warning: Test '$TEST_NAME' already exists in GoldenTest.lean"
    exit 1
fi

# Add test name to the appropriate list in GoldenTest.lean
# Find the list and add the test name before the closing bracket
# Handle both macOS (BSD sed) and Linux (GNU sed)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "/def $LIST_NAME : List String :=/,/^\]/s/\(.*\)\]/\1\n   \"$TEST_NAME\"]/" tests/GoldenTest.lean
else
    sed -i "/def $LIST_NAME : List String :=/,/^\]/s/\(.*\)\]/\1\n   \"$TEST_NAME\"]/" tests/GoldenTest.lean
fi

echo "✓ Added '$TEST_NAME' to $LIST_NAME in GoldenTest.lean"
echo "Next steps:"
echo "  1. Create tests/golden/$CATEGORY/$TEST_NAME.ziku"
echo "  2. Run 'lake test' to generate .golden file"
