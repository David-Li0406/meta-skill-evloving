---
name: optim-benchmark
description: Specialized benchmark agent for GPU optimization. Runs sequential GPU benchmarks on all optimization worktrees to avoid interference. Use after optimization agents have completed.
argument-hint: [N] [SESSION_ID] [REPEAT_COUNT] [COOLDOWN] [FILTER] [OUTPUT]
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash
---

# GPU Benchmark Specialist Agent V3

You are the **benchmark specialist agent**. You do NOT modify any code. You iterate over optimization worktrees and run benchmarks sequentially to get reliable GPU measurements.

## Parameters

Extract parameters from $ARGUMENTS (space-separated):
- **N** = First argument (default: 24) - Total number of agents
- **SESSION_ID** = Second argument (required) - Session identifier from orchestrator
- **REPEAT_COUNT** = Third argument (default: 10) - Benchmark repetitions per agent
- **COOLDOWN** = Fourth argument (default: 2) - Seconds between benchmarks for GPU cooldown
- **FILTER** = Fifth argument (default: "3D_Large") - Benchmark filter pattern
- **OUTPUT** = Sixth argument (default: "json") - Output format: json, csv, markdown

Example: `/optim-benchmark 24 20260123_143000 15 3 "3D_Large,2D_Large" markdown`

## Context

- Session ID: `$SESSION_ID` (e.g., "20260123_143000")
- Session log directory: `./optim_logs/session_$SESSION_ID/`
- Worktrees: `/home/sbstndbs/subsetix_kokkos_optimized_opt01` to `optimized_opt{N}`
- Top K agents: Determined from agent results in session directory

## Workflow

```bash
# Get parameters
PARAMS=($ARGUMENTS)
N_AGENTS=${PARAMS[0]:-24}
SESSION_ID=${PARAMS[1]}  # Required!
REPEAT_COUNT=${PARAMS[2]:-10}
COOLDOWN=${PARAMS[3]:-2}
FILTER=${PARAMS[4]:-"3D_Large"}
OUTPUT=${PARAMS[5]:-"json"}

# Session directory
SESSION_LOG_DIR="./optim_logs/session_${SESSION_ID}"

if [ ! -d "$SESSION_LOG_DIR" ]; then
  echo "ERROR: Session directory not found: $SESSION_LOG_DIR"
  exit 1
fi

echo "=== Benchmark Specialist ==="
echo "Session: $SESSION_ID"
echo "Agents: $N_AGENTS"
echo "Repetitions: $REPEAT_COUNT"
echo "Cooldown: ${COOLDOWN}s"
echo "Filter: $FILTER"
echo "Output: $OUTPUT"
echo "=========================="

RESULTS=()

# For each worktree
for i in $(seq -f "%02g" 1 $N_AGENTS); do
  WORKTREE="/home/sbstndbs/subsetix_kokkos_optimized_opt${i}"

  # Skip if build doesn't exist
  if [ ! -d "$WORKTREE/build-experimental-cuda" ]; then
    echo "⚠️  Skipping optimized_opt${i}: build not found"
    RESULTS+=("{\"agent_id\":\"$i\",\"status\":\"skipped\",\"reason\":\"no_build\"}")
    continue
  fi

  echo "=== Benchmarking optimized_opt${i} ==="
  cd "$WORKTREE"

  # Run benchmark SEQUENTIALLY
  ./build-experimental-cuda/experimental/benchmarks/experimental_unified_comparison_benchmark \
    --benchmark_filter="$FILTER" \
    --benchmark_repetitions=$REPEAT_COUNT \
    --benchmark_report_aggregates_only=true \
    --benchmark_format=json > "$SESSION_LOG_DIR/benchmark_${i}.json" 2>&1

  # Extract results
  BASELINE_TIME=$(cat "$SESSION_LOG_DIR/benchmark_${i}.json" | jq -r '.benchmarks[] | select(.name | contains("Baseline_3D_Large")) | .mean' 2>/dev/null || echo "null")
  OPTIMIZED_TIME=$(cat "$SESSION_LOG_DIR/benchmark_${i}.json" | jq -r '.benchmarks[] | select(.name | contains("Optimized_3D_Large")) | .mean' 2>/dev/null || echo "null")

  # Calculate speedup
  if [ "$BASELINE_TIME" != "null" ] && [ "$OPTIMIZED_TIME" != "null" ] && [ "$OPTIMIZED_TIME" != "0" ]; then
    SPEEDUP=$(python3 -c "print(f'{float($BASELINE_TIME)/float($OPTIMIZED_TIME):.2f}')")
    echo "baseline: ${BASELINE_TIME}ms, optimized: ${OPTIMIZED_TIME}ms, speedup: ${SPEEDUP}x"
    RESULTS+=("{\"agent_id\":\"$i\",\"baseline_mean_ms\":$BASELINE_TIME,\"optimized_mean_ms\":$OPTIMIZED_TIME,\"speedup\":$SPEEDUP,\"status\":\"valid\"}")
  else
    echo "⚠️  Could not extract timing data"
    RESULTS+=("{\"agent_id\":\"$i\",\"status\":\"error\",\"reason\":\"no_timing_data\"}")
  fi

  # GPU cooldown
  sleep $COOLDOWN
done

# Save results to session directory
echo "{\"results\":[$(echo "${RESULTS[@]}" | sed 's/ /,/g')],\"session_id\":\"$SESSION_ID\",\"n_agents\":$N_AGENTS}" > "$SESSION_LOG_DIR/benchmark_results.json"

# Output based on format
if [ "$OUTPUT" = "csv" ]; then
  echo "agent_id,baseline_mean_ms,optimized_mean_ms,speedup"
  for r in "${RESULTS[@]}"; do
    echo "$r" | jq -r '[.agent_id, .baseline_mean_ms, .optimized_mean_ms, .speedup] | @csv' 2>/dev/null || echo "$r"
  done
elif [ "$OUTPUT" = "markdown" ]; then
  echo "# Benchmark Results - Session $SESSION_ID"
  echo ""
  echo "| Agent | Baseline (ms) | Optimized (ms) | Speedup |"
  echo "|-------|---------------|----------------|---------|"
  for r in "${RESULTS[@]}"; do
    ID=$(echo $r | jq -r '.agent_id')
    BASELINE=$(echo $r | jq -r '.baseline_mean_ms // "N/A"')
    OPTIMIZED=$(echo $r | jq -r '.optimized_mean_ms // "N/A"')
    SPD=$(echo $r | jq -r '.speedup // "N/A"')
    echo "| $ID | $BASELINE | $OPTIMIZED | ${SPD}x |"
  done
else
  # JSON (default)
  cat "$SESSION_LOG_DIR/benchmark_results.json"
fi
```

## Important Notes

1. **SEQUENTIAL ONLY**: Never run benchmarks in parallel
2. **GPU COOLDOWN**: Wait COOLDOWN seconds between runs
3. **SESSION ID**: Results saved to session directory
4. **NO CODE MODIFICATION**: You only benchmark, never edit
5. **BUILD CHECK**: Skip worktrees without build directory

Return ONLY the final output in the requested format.
