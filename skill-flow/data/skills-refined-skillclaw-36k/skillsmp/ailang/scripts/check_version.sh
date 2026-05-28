#!/usr/bin/env bash
# Check AILANG installation and version

set -euo pipefail

if ! command -v ailang &> /dev/null; then
    echo "AILANG is not installed"
    echo ""
    echo "Install with:"
    echo "  ./skills/ailang/scripts/install.sh"
    echo ""
    echo "Or download from:"
    echo "  https://github.com/sunholo-data/ailang/releases"
    exit 1
fi

VERSION=$(ailang --version 2>&1 || echo "unknown")
LOCATION=$(which ailang)

echo "AILANG installed"
echo "  Version:  $VERSION"
echo "  Location: $LOCATION"
