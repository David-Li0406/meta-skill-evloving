#!/bin/bash

# Find mise executable
if command -v mise &> /dev/null; then
    MISE_PATH=$(command -v mise)
elif [ -x "/opt/homebrew/bin/mise" ]; then
    MISE_PATH="/opt/homebrew/bin/mise"
elif [ -x "$HOME/.local/bin/mise" ]; then
    MISE_PATH="$HOME/.local/bin/mise"
elif [ -x "/usr/local/bin/mise" ]; then
    MISE_PATH="/usr/local/bin/mise"
else
    echo "Error: mise not found in PATH or common locations"
    exit 1
fi

echo "Using mise at: $MISE_PATH"

# Run SwiftLint with auto-fix
echo "Running SwiftLint with auto-fix..."
"$MISE_PATH" exec -- swiftlint --fix --config .swiftlint.yml

# Run SwiftLint for reporting
echo "Running SwiftLint for reporting..."
"$MISE_PATH" exec -- swiftlint --config .swiftlint.yml
