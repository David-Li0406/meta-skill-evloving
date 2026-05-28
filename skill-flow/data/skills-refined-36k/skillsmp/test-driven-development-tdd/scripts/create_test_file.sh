#!/usr/bin/env bash
# Create a new test file with optional template
# Usage: ./create_test_file.sh <category> <test_name> [template]

set -e

CATEGORY="$1"
TEST_NAME="$2"
TEMPLATE="${3:-empty}"

if [ -z "$CATEGORY" ] || [ -z "$TEST_NAME" ]; then
    echo "Usage: $0 <category> <test_name> [template]"
    echo "Categories: parser, infer, ir-eval"
    echo "Templates: empty (default), lambda, let, match, codata, label"
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

TEST_DIR="tests/golden/$CATEGORY"
TEST_FILE="$TEST_DIR/$TEST_NAME.ziku"

# Create directory if it doesn't exist
mkdir -p "$TEST_DIR"

# Check if file already exists
if [ -f "$TEST_FILE" ]; then
    echo "Error: Test file already exists: $TEST_FILE"
    exit 1
fi

# Create test file with template
case "$TEMPLATE" in
    empty)
        echo "# Test: $TEST_NAME" > "$TEST_FILE"
        echo "" >> "$TEST_FILE"
        ;;
    lambda)
        cat > "$TEST_FILE" <<'EOF'
# Lambda expression test
let f = \x -> x + 1 in
f 5
EOF
        ;;
    let)
        cat > "$TEST_FILE" <<'EOF'
# Let binding test
let x = 42 in
x
EOF
        ;;
    match)
        cat > "$TEST_FILE" <<'EOF'
# Pattern matching test
match 42 with
| 0 -> "zero"
| n -> "nonzero"
EOF
        ;;
    codata)
        cat > "$TEST_FILE" <<'EOF'
# Codata test
codata {
  .value -> 42
}
EOF
        ;;
    label)
        cat > "$TEST_FILE" <<'EOF'
# Label/goto test
label result {
  goto(42, result)
}
EOF
        ;;
    *)
        echo "Error: Unknown template: $TEMPLATE"
        exit 1
        ;;
esac

echo "✓ Created test file: $TEST_FILE"
echo "Edit the file and run 'lake test' to generate .golden file"
