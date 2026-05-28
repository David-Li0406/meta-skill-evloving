---
name: optim-profile
description: GPU profiling specialist agent. Uses existing CMake presets (profiling-nsight-cuda) to analyze top optimization candidates. Use after benchmarks to identify bottlenecks and improvement opportunities.
argument-hint: [N] [TOP_K] [PRESET]
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash(cmake, ncu, nsys), Read
---

# GPU Profiling Specialist Agent

You are the **GPU profiling specialist agent**. You use existing CMake profiling presets to analyze optimization candidates and identify bottlenecks.

## Parameters

Extract parameters from $ARGUMENTS (space-separated):
- **N** = First argument (default: 24) - Total number of agents
- **TOP_K** = Second argument (default: 5) - Profile top K best agents
- **PRESET** = Third argument (default: "profiling-nsight-cuda") - Which profiling preset to use

Available presets (from CMakePresets.json):
- `profiling-nsight-cuda` - Nsight Compute for kernel analysis
- `profiling-nsight-cuda-release` - Nsight with Release + symbols
- `experimental-perf-serial` - Linux perf (CPU)
- `experimental-perf-openmp` - Linux perf + OpenMP
- `experimental-serial-profile` - Kokkos profiling tools

Example: `/optim-profile 24 3 profiling-nsight-cuda` → Profile top 3 agents with Nsight

## Context

- Worktrees: `/home/sbstndbs/subsetix_kokkos_optimized_opt01` to `optimized_opt{N}`
- Top K agents: Determined from benchmark results (or agent IDs if specified)
- Profiling builds require recompilation with specific preset

## Workflow

```bash
# Get parameters
PARAMS=($ARGUMENTS)
N_AGENTS=${PARAMS[0]:-24}
TOP_K=${PARAMS[1]:-5}
PRESET=${PARAMS[2]:-"profiling-nsight-cuda"}

# Detect GPU
GPU_ARCH=$(nvidia-smi -L 2>/dev/null | grep -oP 'NVIDIA \K[^ ]+' | tr '[:lower:]' '[:upper:]')

echo "=== GPU Profiling Specialist ==="
echo "Preset: $PRESET"
echo "Top K: $TOP_K"
echo "=============================="

# Determine which agents to profile
# In a real scenario, this would read from benchmark results
# For now, assume we profile the first TOP_K worktrees that have successful builds
for i in $(seq -f "%02g" 1 $TOP_K); do
  WORKTREE="/home/sbstndbs/subsetix_kokkos_optimized_opt${i}"

  if [ ! -d "$WORKTREE" ]; then
    echo "⚠️  Worktree optimized_opt${i} not found, skipping"
    continue
  fi

  echo "=== Profiling optimized_opt${i} ==="
  cd "$WORKTREE"

  # Clean previous build
  rm -rf build-profiling-*

  # Configure with profiling preset
  cmake --preset $PRESET -DKokkos_ARCH_${GPU_ARCH}=ON

  # Build with profiling
  cmake --build $PRESET -j4

  # Run profiling
  if [ "$PRESET" = "profiling-nsight-cuda" ]; then
    # Use Nsight Compute for kernel analysis
    ncu --set full \
        --export profile_optimized_opt${i} \
        ./experimental/benchmarks/experimental_unified_comparison_benchmark \
          --benchmark_filter="3D_Large" \
          --benchmark_repetitions=3

    echo "Profile saved to profile_optimized_opt${i}.ncu-rep"
  elif [ "$PRESET" = "profiling-nsight-cuda-release" ]; then
    # Release + symbols for better performance
    ncu --set full \
        --export profile_optimized_opt${i}_release \
        ./experimental/benchmarks/experimental_unified_comparison_benchmark \
          --benchmark_filter="3D_Large" \
          --benchmark_repetitions=3

    echo "Profile saved to profile_optimized_opt${i}_release.ncu-rep"
  fi

  # Extract key metrics from profile
  echo "Key metrics for optimized_opt${i}:"
  # Parse ncu output to extract occupancy, memory bandwidth, etc.
  # (This would typically use ncu --csv to export metrics)

  echo ""
done

echo "=== Profiling Summary ==="
echo "Profiled $TOP_K agents with preset: $PRESET"
echo "Profiles saved in respective worktree directories"
```

## Metrics to Extract

When using Nsight Compute, look for:
- **GPU Occupancy**: Percentage of maximum (target > 50%)
- **Memory Bandwidth**: GB/s utilized vs peak (target > 30%)
- **Warp Efficiency**: Percentage of warps active (target > 80%)
- **Branch Divergence**: Percentage (lower is better)

## Available CMake Presets

From CMakePresets.json in the repository:
```json
{
  "experimental-perf-serial": "Linux perf, experimental only",
  "experimental-perf-openmp": "Linux perf + OpenMP",
  "experimental-serial-profile": "Kokkos profiling tools",
  "profiling-nsight-cuda": "Nsight GPU profiling",
  "profiling-nsight-cuda-release": "Nsight with Release + symbols"
}
```

## Important Notes

1. **REBUILD REQUIRED**: Profiling requires recompilation with specific preset
2. **GPU SPECIFIC**: Most profiling presets are GPU-specific (check preset name)
3. **NCU OUTPUT**: Nsight Compute generates `.ncu-rep` files
4. **METRICS**: Extract occupancy, bandwidth, warp efficiency from reports
5. **NON-DESTRUCTIVE**: You don't modify code, only profile

Return JSON with profiling summary and top findings.
