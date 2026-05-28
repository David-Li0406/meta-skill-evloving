#!/bin/bash
# Validate Python syntax and run basic linting checks
#
# Usage: validate-python.sh <file_path>
#
# Arguments:
#   file_path: Path to the Python file to validate
#
# Exit codes:
#   0: Validation passed
#   1: Validation failed
#   2: Invalid arguments

set -e

# Check for required argument
if [ -z "$1" ]; then
    echo "Error: file_path argument is required"
    echo "Usage: validate-python.sh <file_path>"
    exit 2
fi

FILE_PATH="$1"

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File not found: $FILE_PATH"
    exit 1
fi

# Check if file is a Python file
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
    echo "Warning: File does not have .py extension: $FILE_PATH"
fi

echo "Validating Python file: $FILE_PATH"
echo "=========================================="

# Run Python syntax check
echo "Running syntax check..."
if python -m py_compile "$FILE_PATH"; then
    echo "✓ Syntax check passed"
else
    echo "✗ Syntax check failed"
    exit 1
fi

# Run ruff if available
if command -v ruff &> /dev/null; then
    echo ""
    echo "Running ruff linter..."
    if ruff check "$FILE_PATH"; then
        echo "✓ Ruff check passed"
    else
        echo "✗ Ruff check found issues"
        # Don't exit with error for linting issues, just report them
    fi
else
    echo ""
    echo "Note: ruff not installed, skipping linting"
fi

echo ""
echo "=========================================="
echo "Validation complete"
exit 0

