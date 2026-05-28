#!/bin/bash
# next-id.sh — Get the next available task ID for a prefix
# Part of the Dialogue Framework
# Usage: next-id.sh <PREFIX>
#   PREFIX: Task ID prefix (SH, CD, FW, DOC, VAL, or custom 2-4 letter prefix)
#
# Outputs the next available ID (e.g., FW-018 if FW-017 exists)

set -euo pipefail

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
TASKS_DIR="${PROJECT_ROOT}/.dialogue/tasks"

# Validate arguments
if [[ $# -lt 1 ]]; then
    echo "Usage: next-id.sh <PREFIX>" >&2
    echo "  PREFIX: 2-4 uppercase letters (e.g., SH, CD, FW, DOC, VAL)" >&2
    exit 1
fi

PREFIX="$1"

# Validate prefix format (2-4 uppercase letters)
if [[ ! "$PREFIX" =~ ^[A-Z]{2,4}$ ]]; then
    echo "Error: PREFIX must be 2-4 uppercase letters (e.g., SH, FW, DOC)" >&2
    exit 1
fi

# Ensure tasks directory exists
mkdir -p "$TASKS_DIR"

# Find highest existing ID for this prefix
max_num=0

for file in "$TASKS_DIR"/${PREFIX}-*.yaml; do
    [[ -f "$file" ]] || continue

    # Extract filename without path and extension
    filename=$(basename "$file" .yaml)

    # Extract number part (after PREFIX-)
    if [[ "$filename" =~ ^${PREFIX}-([0-9]+)$ ]]; then
        num="${BASH_REMATCH[1]}"
        # Remove leading zeros for comparison
        num=$((10#$num))
        if [[ $num -gt $max_num ]]; then
            max_num=$num
        fi
    fi
done

# Next ID is max + 1, zero-padded to 3 digits
next_num=$((max_num + 1))
next_id=$(printf "%s-%03d" "$PREFIX" "$next_num")

echo "$next_id"
