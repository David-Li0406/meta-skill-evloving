#!/usr/bin/env bash
#
# MAX Version Detection Script
# Detects installed MAX version and recommends appropriate patterns
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

# Detect MAX version
detect_max_version() {
    if command -v max &> /dev/null; then
        local version_output
        version_output=$(max version 2>/dev/null || echo "")

        if [[ -n "$version_output" ]]; then
            # Extract version number (e.g., "25.7.0" or "26.1.0")
            local version
            version=$(echo "$version_output" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
            echo "$version"
            return 0
        fi
    fi

    # Try pixi environment
    if command -v pixi &> /dev/null; then
        local pixi_version
        pixi_version=$(pixi list 2>/dev/null | grep -E "^max\s" | awk '{print $2}' || echo "")
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
    local major=${version%%.*}

    # Nightly versions are 26.x+
    if [[ "$major" -ge 26 ]]; then
        echo "nightly"
    # Stable versions are 25.x
    elif [[ "$major" -eq 25 ]]; then
        echo "stable"
    else
        echo "unknown"
    fi
}

# Get key differences for version
get_version_differences() {
    local version_type=$1

    if [[ "$version_type" == "stable" ]]; then
        cat << 'EOF'
Stable (v25.7) specifics:
  - Batch size: Aggregate across replicas
  - Driver API: max.driver.Tensor
  - Prefill config: prefill_chunk_size
  - Context length: max_batch_context_length
  - Llama 3.2 Vision: Supported
EOF
    elif [[ "$version_type" == "nightly" ]]; then
        cat << 'EOF'
Nightly (v26.2) specifics:
  - Batch size: Per-replica with data parallelism
  - Driver API: max.driver.Buffer (renamed from Tensor)
  - Prefill config: max_batch_input_tokens
  - Context length: max_batch_total_tokens
  - Gemma3 Vision: Supported (12B, 27B)
  - New: --kvcache-ce-watermark scheduling option
EOF
    fi
}

# Main detection
VERSION=$(detect_max_version)
VERSION_TYPE=""
INSTALLED=false

if [[ -n "$VERSION" ]]; then
    INSTALLED=true
    VERSION_TYPE=$(get_version_type "$VERSION")
fi

# Output
if $JSON_OUTPUT; then
    cat << EOF
{
  "installed": $INSTALLED,
  "version": "$VERSION",
  "version_type": "$VERSION_TYPE",
  "patterns_directory": "patterns/",
  "recommendations": {
    "stable_version": "25.7",
    "nightly_version": "26.1",
    "key_differences": {
      "batch_size_semantics": {
        "stable": "aggregate_across_replicas",
        "nightly": "per_replica_with_dp"
      },
      "driver_api": {
        "stable": "max.driver.Tensor",
        "nightly": "max.driver.Buffer"
      },
      "prefill_config": {
        "stable": "prefill_chunk_size",
        "nightly": "max_batch_input_tokens"
      },
      "context_length": {
        "stable": "max_batch_context_length",
        "nightly": "max_batch_total_tokens"
      }
    }
  }
}
EOF
else
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║               MAX Version Detection                        ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    if $INSTALLED; then
        echo "✓ MAX installed: $VERSION"
        echo "  Version type: $VERSION_TYPE"
        echo ""
        echo "$(get_version_differences "$VERSION_TYPE")"
        echo ""
        echo "Essential patterns to load:"
        echo "  - serve-configuration (batch settings, scheduling)"
        echo "  - serve-kv-cache (KV cache strategy)"
        echo "  - multigpu-scaling (multi-GPU setup)"
    else
        echo "✗ MAX not found"
        echo ""
        echo "Install MAX:"
        echo "  # Stable"
        echo "  pixi add max"
        echo ""
        echo "  # Nightly"
        echo "  pixi add max --channel https://conda.modular.com/nightly"
    fi
fi
