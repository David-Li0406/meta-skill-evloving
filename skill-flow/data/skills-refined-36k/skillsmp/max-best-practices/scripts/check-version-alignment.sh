#!/bin/bash
# Check MAX and Mojo version alignment
# Run this script to detect version mismatches that cause kernel compilation failures

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== MAX/Mojo Version Alignment Check ==="
echo ""

# Detect if we're in a pixi environment
PIXI_ENV=""
if [ -n "$PIXI_PROJECT_ROOT" ]; then
    PIXI_ENV="yes"
    echo -e "${GREEN}Running inside pixi environment${NC}"
    echo "Project root: $PIXI_PROJECT_ROOT"
elif [ -f "pixi.toml" ]; then
    echo -e "${YELLOW}Warning: pixi.toml found but not running inside pixi environment${NC}"
    echo "Run with: pixi run ./scripts/check-version-alignment.sh"
    echo "Or: pixi shell (then run this script)"
    echo ""
fi

# Get Mojo version
echo ""
echo "Checking Mojo version..."
if command -v mojo &> /dev/null; then
    MOJO_VERSION=$(mojo --version 2>/dev/null | head -1)
    MOJO_MAJOR_MINOR=$(echo "$MOJO_VERSION" | grep -oE '[0-9]+\.[0-9]+' | head -1)
    echo "  Mojo: $MOJO_VERSION"
else
    echo -e "${RED}  Mojo: NOT FOUND${NC}"
    MOJO_MAJOR_MINOR=""
fi

# Get MAX Python package version
echo ""
echo "Checking MAX Python package..."
if python3 -c "import max" 2>/dev/null; then
    # Try to get version from pip
    MAX_PIP_VERSION=$(pip show max 2>/dev/null | grep "^Version:" | cut -d' ' -f2 || echo "")
    if [ -z "$MAX_PIP_VERSION" ]; then
        # Try with pip3
        MAX_PIP_VERSION=$(pip3 show max 2>/dev/null | grep "^Version:" | cut -d' ' -f2 || echo "")
    fi

    if [ -n "$MAX_PIP_VERSION" ]; then
        echo "  MAX (pip): $MAX_PIP_VERSION"
        MAX_MAJOR_MINOR=$(echo "$MAX_PIP_VERSION" | grep -oE '^[0-9]+\.[0-9]+' | head -1)

        # Check if nightly
        if [[ "$MAX_PIP_VERSION" == *"dev"* ]]; then
            echo -e "  ${YELLOW}Detected: NIGHTLY version${NC}"
            IS_NIGHTLY="yes"
        else
            echo -e "  ${GREEN}Detected: STABLE version${NC}"
            IS_NIGHTLY="no"
        fi
    else
        echo "  MAX (pip): Could not determine version"
        MAX_MAJOR_MINOR=""
    fi
else
    echo -e "${RED}  MAX: NOT FOUND (import max failed)${NC}"
    MAX_MAJOR_MINOR=""
fi

# Get MAX conda package version (if in pixi/conda)
echo ""
echo "Checking MAX conda package..."
if command -v pixi &> /dev/null && [ -f "pixi.toml" ]; then
    MAX_CONDA_VERSION=$(pixi list 2>/dev/null | grep "^max " | awk '{print $2}' || echo "")
    if [ -n "$MAX_CONDA_VERSION" ]; then
        echo "  MAX (conda): $MAX_CONDA_VERSION"
        MAX_CONDA_MAJOR_MINOR=$(echo "$MAX_CONDA_VERSION" | grep -oE '^[0-9]+\.[0-9]+' | head -1)
    else
        echo "  MAX (conda): Not installed via conda/pixi"
    fi
fi

# Version alignment check
echo ""
echo "=== Version Alignment Analysis ==="
echo ""

ISSUES_FOUND=0

# Check Mojo vs MAX alignment
if [ -n "$MOJO_VERSION" ] && [ -n "$MAX_MAJOR_MINOR" ]; then
    # Normalize: Mojo uses 0.XX.Y.Z format, MAX uses XX.Y.Z format
    # Mojo 0.25.7.0 should match MAX 25.7
    # Extract the XX.Y part from Mojo version (e.g., 0.25.7.0 -> 25.7)
    MOJO_NORMALIZED=$(echo "$MOJO_VERSION" | grep -oE '^0\.([0-9]+\.[0-9]+)' | sed 's/^0\.//')

    if [ "$MOJO_NORMALIZED" = "$MAX_MAJOR_MINOR" ]; then
        echo -e "${GREEN}OK: Mojo and MAX versions are aligned (Mojo $MOJO_NORMALIZED / MAX $MAX_MAJOR_MINOR)${NC}"
    else
        echo -e "${RED}MISMATCH: Mojo ($MOJO_NORMALIZED) and MAX ($MAX_MAJOR_MINOR) versions differ!${NC}"
        echo ""
        echo "This will cause kernel compilation failures with errors like:"
        echo "  - 'no matching function in call to foreach'"
        echo "  - 'callee parameter func has different type'"
        echo "  - 'failed to infer parameter'"
        ISSUES_FOUND=1
    fi
fi

# Check for global vs local version conflicts
if [ -n "$PIXI_ENV" ] && [ -n "$MAX_CONDA_VERSION" ] && [ -n "$MAX_PIP_VERSION" ]; then
    if [ "$MAX_CONDA_VERSION" != "$MAX_PIP_VERSION" ]; then
        echo -e "${RED}CONFLICT: Different MAX versions in conda ($MAX_CONDA_VERSION) vs pip ($MAX_PIP_VERSION)${NC}"
        echo "This can happen if you have a global pip install mixing with pixi."
        ISSUES_FOUND=1
    fi
fi

echo ""
echo "=== Recommendations ==="
echo ""

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}No version issues detected.${NC}"
else
    echo "To fix version mismatches:"
    echo ""
    echo "1. Use pixi for all MAX/Mojo development:"
    echo "   pixi init"
    echo "   pixi add max"
    echo "   pixi shell  # Always work inside the shell"
    echo ""
    echo "2. If using pip directly, ensure versions match:"
    echo "   # For stable:"
    echo "   pip install max==25.7.0"
    echo ""
    echo "   # For nightly:"
    echo "   pip install --upgrade max --index-url https://whl.modular.com/nightly/simple/"
    echo ""
    echo "3. Remove conflicting global installs:"
    echo "   pip uninstall max  # Remove global install"
    echo "   # Then use pixi exclusively"
fi

echo ""
echo "=== API Quick Reference for Your Version ==="
echo ""

if [ "$IS_NIGHTLY" = "yes" ]; then
    echo "You're on NIGHTLY. Use these APIs:"
    echo "  DeviceRef: DeviceRef.CPU() / DeviceRef.GPU()"
    echo "  foreach:   fn[width: Int](idx) -> SIMD[dtype, width]"
    echo "  Buffer:    max.driver.Buffer"
    echo "  ops.custom: ops.custom(name, device, values, out_types)"
else
    echo "You're on STABLE (v25.7). Use these APIs:"
    echo "  DeviceRef: DeviceRef.from_device(device)"
    echo "  foreach:   fn[width: Int, element_alignment: Int](idx) -> SIMD[dtype, width]"
    echo "  Tensor:    max.driver.Tensor (not Buffer)"
    echo "  ops.custom: ops.custom(name, values, out_types)"
fi

echo ""
exit $ISSUES_FOUND
