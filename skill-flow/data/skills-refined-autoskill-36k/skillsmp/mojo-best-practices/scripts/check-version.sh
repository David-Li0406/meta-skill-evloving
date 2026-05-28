#!/usr/bin/env bash
#
# Mojo Version Detection Script
# Detects installed Mojo version and recommends appropriate patterns
#
# Usage:
#   ./check-version.sh          # Human-readable output
#   ./check-version.sh --json   # JSON output for programmatic use
#

set -e

JSON_OUTPUT=false
if [[ "$1" == "--json" ]]; then
    JSON_OUTPUT=true
fi

# Detect Mojo version
detect_mojo_version() {
    if command -v mojo &> /dev/null; then
        local version_output
        version_output=$(mojo --version 2>/dev/null || echo "")

        if [[ -n "$version_output" ]]; then
            # Extract version number (e.g., "25.7.0" or "0.26.1")
            local version
            version=$(echo "$version_output" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
            echo "$version"
            return 0
        fi
    fi

    # Try pixi environment
    if command -v pixi &> /dev/null; then
        local pixi_version
        pixi_version=$(pixi list 2>/dev/null | grep -E "^mojo\s" | awk '{print $2}' || echo "")
        if [[ -n "$pixi_version" ]]; then
            echo "$pixi_version"
            return 0
        fi
    fi

    echo ""
    return 1
}

# Determine version type (stable/nightly)
get_version_type() {
    local version=$1

    # Nightly versions start with 0. (e.g., 0.26.1)
    if [[ "$version" == 0.* ]]; then
        echo "nightly"
    # Stable versions are 25.x or higher year-based versions
    elif [[ "$version" =~ ^[0-9]{2}\.[0-9] ]]; then
        echo "stable"
    else
        echo "unknown"
    fi
}

# Get recommended patterns directory
get_patterns_dir() {
    local version_type=$1

    case $version_type in
        stable)
            echo "patterns/ + patterns/stable/"
            ;;
        nightly)
            echo "patterns/ + patterns/nightly/"
            ;;
        *)
            echo "patterns/"
            ;;
    esac
}

# Main detection
VERSION=$(detect_mojo_version)
VERSION_TYPE=""
PATTERNS_DIR=""
INSTALLED=false

if [[ -n "$VERSION" ]]; then
    INSTALLED=true
    VERSION_TYPE=$(get_version_type "$VERSION")
    PATTERNS_DIR=$(get_patterns_dir "$VERSION_TYPE")
fi

# Output
if $JSON_OUTPUT; then
    cat << EOF
{
  "installed": $INSTALLED,
  "version": "$VERSION",
  "version_type": "$VERSION_TYPE",
  "patterns_directory": "$PATTERNS_DIR",
  "recommendations": {
    "stable_version": "25.7",
    "nightly_version": "0.26.2",
    "key_differences": {
      "constants": {
        "stable": "alias",
        "nightly": "comptime"
      },
      "alignment": {
        "stable": "not available",
        "nightly": "@align(N)"
      },
      "typed_errors": {
        "stable": "not available",
        "nightly": "raises CustomError"
      }
    }
  }
}
EOF
else
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              Mojo Version Detection                        ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    if $INSTALLED; then
        echo "✓ Mojo installed: $VERSION"
        echo "  Version type: $VERSION_TYPE"
        echo ""
        echo "Recommended patterns:"
        echo "  $PATTERNS_DIR"
        echo ""

        if [[ "$VERSION_TYPE" == "stable" ]]; then
            echo "Key syntax for stable:"
            echo "  - Use 'alias' for compile-time constants"
            echo "  - @fieldwise_init for struct initialization"
            echo "  - var/deinit for ownership transfer"
        elif [[ "$VERSION_TYPE" == "nightly" ]]; then
            echo "Key syntax for nightly:"
            echo "  - Use 'comptime' for compile-time constants (alias deprecated)"
            echo "  - @align(N) for struct alignment"
            echo "  - 'raises CustomError' for typed errors"
            echo "  - 'fn abort() -> Never' for never type"
        fi
    else
        echo "✗ Mojo not found"
        echo ""
        echo "Install Mojo:"
        echo "  # Stable"
        echo "  pixi add max"
        echo ""
        echo "  # Nightly"
        echo "  pixi add max --channel https://conda.modular.com/nightly"
    fi
fi
