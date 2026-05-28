#!/usr/bin/env bash
#
# GPU Detection Script for Mojo
# Detects available GPUs and recommends relevant GPU patterns
#
# Usage:
#   ./gpu-check.sh          # Human-readable output
#   ./gpu-check.sh --json   # JSON output for programmatic use
#

set -e

JSON_OUTPUT=false
if [[ "$1" == "--json" ]]; then
    JSON_OUTPUT=true
fi

# Initialize detection results
NVIDIA_AVAILABLE=false
NVIDIA_GPUS=()
NVIDIA_COMPUTE_CAPS=()
AMD_AVAILABLE=false
AMD_GPUS=()
APPLE_METAL=false
APPLE_GPU=""

# Detect NVIDIA GPUs
detect_nvidia() {
    if command -v nvidia-smi &> /dev/null; then
        local gpu_info
        gpu_info=$(nvidia-smi --query-gpu=name,compute_cap --format=csv,noheader 2>/dev/null || echo "")

        if [[ -n "$gpu_info" ]]; then
            NVIDIA_AVAILABLE=true
            while IFS=, read -r name cap; do
                name=$(echo "$name" | xargs)  # Trim whitespace
                cap=$(echo "$cap" | xargs)
                NVIDIA_GPUS+=("$name")
                NVIDIA_COMPUTE_CAPS+=("$cap")
            done <<< "$gpu_info"
        fi
    fi
}

# Detect AMD GPUs
detect_amd() {
    if command -v rocminfo &> /dev/null; then
        local gpu_info
        gpu_info=$(rocminfo 2>/dev/null | grep -E "^\s+Name:\s+gfx" || echo "")

        if [[ -n "$gpu_info" ]]; then
            AMD_AVAILABLE=true
            while read -r line; do
                local gpu_name
                gpu_name=$(echo "$line" | sed 's/.*Name:\s*//' | xargs)
                AMD_GPUS+=("$gpu_name")
            done <<< "$gpu_info"
        fi
    fi
}

# Detect Apple Metal (macOS only)
detect_apple() {
    if [[ "$(uname)" == "Darwin" ]]; then
        if system_profiler SPDisplaysDataType 2>/dev/null | grep -q "Metal Support"; then
            APPLE_METAL=true
            APPLE_GPU=$(system_profiler SPDisplaysDataType 2>/dev/null | grep "Chipset Model" | head -1 | sed 's/.*: //' || echo "Unknown")
        fi
    fi
}

# Get recommended patterns based on GPU
get_nvidia_patterns() {
    local compute_cap=$1
    local major=${compute_cap%%.*}

    case $major in
        9)
            # SM90 - Hopper (H100, H200)
            echo "gpu-tensor-cores (WGMMA), gpu-memory-access (TMA), gpu-warp"
            ;;
        10)
            # SM100 - Blackwell (B200)
            echo "gpu-tensor-cores (TCGen05), gpu-memory-access (TMA), gpu-warp"
            ;;
        8)
            # SM80/SM86/SM89 - Ampere/Ada
            echo "gpu-tensor-cores, gpu-fundamentals, gpu-synchronization"
            ;;
        *)
            echo "gpu-fundamentals, gpu-kernels"
            ;;
    esac
}

get_amd_patterns() {
    local gpu_arch=$1

    if [[ "$gpu_arch" == *"gfx94"* ]]; then
        # MI300 series
        echo "gpu-amd (MFMA), gpu-fundamentals, gpu-synchronization"
    else
        echo "gpu-amd, gpu-fundamentals"
    fi
}

# Run detection
detect_nvidia
detect_amd
detect_apple

# Output
if $JSON_OUTPUT; then
    # Build NVIDIA GPUs JSON array
    nvidia_json="[]"
    if $NVIDIA_AVAILABLE; then
        nvidia_json="["
        for i in "${!NVIDIA_GPUS[@]}"; do
            [[ $i -gt 0 ]] && nvidia_json+=","
            nvidia_json+="{\"name\":\"${NVIDIA_GPUS[$i]}\",\"compute_cap\":\"${NVIDIA_COMPUTE_CAPS[$i]}\"}"
        done
        nvidia_json+="]"
    fi

    # Build AMD GPUs JSON array
    amd_json="[]"
    if $AMD_AVAILABLE; then
        amd_json="["
        for i in "${!AMD_GPUS[@]}"; do
            [[ $i -gt 0 ]] && amd_json+=","
            amd_json+="{\"arch\":\"${AMD_GPUS[$i]}\"}"
        done
        amd_json+="]"
    fi

    cat << EOF
{
  "nvidia": {
    "available": $NVIDIA_AVAILABLE,
    "gpus": $nvidia_json
  },
  "amd": {
    "available": $AMD_AVAILABLE,
    "gpus": $amd_json
  },
  "apple": {
    "metal_available": $APPLE_METAL,
    "gpu": "$APPLE_GPU"
  },
  "recommended_patterns": {
    "nvidia_sm90": ["gpu-tensor-cores", "gpu-memory-access", "gpu-warp", "gpu-synchronization"],
    "nvidia_sm100": ["gpu-tensor-cores", "gpu-memory-access", "gpu-warp", "gpu-synchronization"],
    "amd_mi300": ["gpu-amd", "gpu-fundamentals", "gpu-synchronization"],
    "apple_metal": ["references/apple-metal/", "ffi-interop"]
  }
}
EOF
else
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                   GPU Detection                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    if $NVIDIA_AVAILABLE; then
        echo "✓ NVIDIA GPU(s) detected:"
        for i in "${!NVIDIA_GPUS[@]}"; do
            echo "  - ${NVIDIA_GPUS[$i]} (SM ${NVIDIA_COMPUTE_CAPS[$i]})"
            echo "    Patterns: $(get_nvidia_patterns "${NVIDIA_COMPUTE_CAPS[$i]}")"
        done
        echo ""
    fi

    if $AMD_AVAILABLE; then
        echo "✓ AMD GPU(s) detected:"
        for gpu in "${AMD_GPUS[@]}"; do
            echo "  - $gpu"
            echo "    Patterns: $(get_amd_patterns "$gpu")"
        done
        echo ""
    fi

    if $APPLE_METAL; then
        echo "✓ Apple Metal available:"
        echo "  - $APPLE_GPU"
        echo "    Patterns: references/apple-metal/, ffi-interop (BLAS)"
        echo ""
    fi

    if ! $NVIDIA_AVAILABLE && ! $AMD_AVAILABLE && ! $APPLE_METAL; then
        echo "✗ No GPU detected"
        echo ""
        echo "For CPU optimization, see:"
        echo "  - perf-vectorization (SIMD)"
        echo "  - perf-parallelization (multi-core)"
        echo "  - ffi-interop (BLAS libraries)"
    fi

    echo ""
    echo "GPU Pattern Summary:"
    echo "┌─────────────────┬────────────────────────────────────┐"
    echo "│ Hardware        │ Key Patterns                       │"
    echo "├─────────────────┼────────────────────────────────────┤"
    echo "│ NVIDIA SM90     │ gpu-tensor-cores (WGMMA)           │"
    echo "│ NVIDIA SM100    │ gpu-tensor-cores (TCGen05)         │"
    echo "│ AMD MI300       │ gpu-amd (MFMA)                     │"
    echo "│ Apple Silicon   │ ffi-interop, apple-metal/          │"
    echo "│ All GPUs        │ gpu-fundamentals, gpu-kernels      │"
    echo "└─────────────────┴────────────────────────────────────┘"
fi
