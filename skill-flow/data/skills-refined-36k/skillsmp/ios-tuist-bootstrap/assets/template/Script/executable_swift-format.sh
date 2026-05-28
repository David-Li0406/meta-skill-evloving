#!/bin/bash

set -euo pipefail

# Resolve repository root and configuration path.
SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_ROOT}/.." && pwd)"
CONFIG_PATH="${REPO_ROOT}/.swift-format"

if [ ! -f "${CONFIG_PATH}" ]; then
    echo "Error: ${CONFIG_PATH} not found." >&2
    exit 1
fi

# Determine how to invoke swift-format.
if command -v swift &> /dev/null && swift --help 2> /dev/null | grep -q "\bformat\b"; then
    SWIFT_FORMAT_CMD=("swift" "format")
elif command -v swift-format &> /dev/null; then
    SWIFT_FORMAT_CMD=("swift-format" "format")
elif xcrun --find swift-format &> /dev/null; then
    SWIFT_FORMAT_CMD=("xcrun" "swift-format" "format")
else
    echo "Error: swift-format not found. Install it and ensure it is available on your PATH." >&2
    exit 1
fi

# Format provided targets or default to the current working directory.
if [ "$#" -eq 0 ]; then
    TARGETS=(".")
else
    TARGETS=("$@")
fi

"${SWIFT_FORMAT_CMD[@]}" \
    --configuration "${CONFIG_PATH}" \
    --in-place \
    --recursive \
    "${TARGETS[@]}"
