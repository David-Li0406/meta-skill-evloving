#!/bin/bash
# Dependencies Installation Script (Unix/Mac/Linux)

set -e  # Exit on error

# Get the script's directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Navigate to the API directory
cd "$PROJECT_ROOT/apps/api"

# Check if bun is installed
if ! command -v bun &> /dev/null; then
    echo "Error: bun is not installed or not in PATH"
    echo "Please install bun from https://bun.sh"
    exit 1
fi

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found in apps/api"
    exit 1
fi

# Run installation
echo "Installing dependencies in apps/api..."
echo "Running: bun install"
echo ""
bun install

# Verify installation
if [ -d "node_modules" ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
else
    echo ""
    echo "Warning: node_modules directory not found after installation"
    exit 1
fi

exit 0
