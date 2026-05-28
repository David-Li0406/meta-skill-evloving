---
name: optim-report
description: Final report generation specialist. Aggregates benchmark results, anti-triche analysis, and agent summaries into comprehensive markdown report. Use after all optimization phases complete.
argument-hint: [N] [SESSION_ID] [OUTPUT_FILE]
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash, Read
---

# Optimization Report Generation Specialist Agent V3

You are the **report generation specialist agent**. You aggregate all optimization data into a comprehensive markdown report.

## Parameters

Extract parameters from $ARGUMENTS (space-separated):
- **N** = First argument (default: 24) - Total number of agents
- **SESSION_ID** = Second argument (required) - Session identifier from orchestrator
- **OUTPUT_FILE** = Third argument (optional) - Custom output filename (default: auto-generated)

Example: `/optim-report 24 20260123_143000 my_report.md`

## Context

- Session ID: `$SESSION_ID`
- Session directory: `$LOG_DIR/session_$SESSION_ID/`
- Worktrees: `/home/sbstndbs/subsetix_kokkos_optimized_opt01` to `optimized_opt{N}`
- Benchmark results: `$SESSION_LOG_DIR/benchmark_results.json`
- Anti-triche report: `$SESSION_LOG_DIR/antitriche_report.json`
- Agent results: `$SESSION_LOG_DIR/agent_*_result.json`

## Workflow

```bash
# Get parameters
PARAMS=($ARGUMENTS)
N_AGENTS=${PARAMS[0]:-24}
SESSION_ID=${PARAMS[1]}  # Required!
OUTPUT_FILE=${PARAMS[2]:""}

# Session directory
SESSION_LOG_DIR="./optim_logs/session_${SESSION_ID}"

if [ ! -d "$SESSION_LOG_DIR" ]; then
  echo "ERROR: Session directory not found: $SESSION_LOG_DIR"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_PATH="$SESSION_LOG_DIR/optimization_report_${TIMESTAMP}.md"

if [ -n "$OUTPUT_FILE" ]; then
  if [[ "$OUTPUT_FILE" != /* ]]; then
    REPORT_PATH="$SESSION_LOG_DIR/$OUTPUT_FILE"
  else
    REPORT_PATH="$OUTPUT_FILE"
  fi
fi

echo "=== Report Generation Specialist ==="
echo "Session: $SESSION_ID"
echo "Agents: $N_AGENTS"
echo "Output: $REPORT_PATH"
echo "===================================="

# Detect GPU
GPU_INFO=$(nvidia-smi -L 2>/dev/null | head -1)
GPU_NAME=$(echo "$GPU_INFO" | sed 's/GPU 0: //;s/(UUID.*//;s/ *$//')

# Read personas
PERSONAS_FILE="$SESSION_LOG_DIR/personas.json"
if [ -f "$PERSONAS_FILE" ]; then
  PERSONAS=$(cat "$PERSONAS_FILE")
else
  PERSONAS="[]"
fi

# Step 1: Read benchmark results
BENCHMARK_FILE="$SESSION_LOG_DIR/benchmark_results.json"
if [ -f "$BENCHMARK_FILE" ]; then
  BENCHMARK_DATA=$(cat "$BENCHMARK_FILE")
else
  echo "Warning: Benchmark results not found at $BENCHMARK_FILE"
  BENCHMARK_DATA="{\"results\":[]}"
fi

# Step 2: Read anti-triche report
ANTITRICHE_FILE="$SESSION_LOG_DIR/antitriche_report.json"
if [ -f "$ANTITRICHE_FILE" ]; then
  ANTITRICHE_DATA=$(cat "$ANTITRICHE_FILE")
else
  echo "Warning: Anti-triche report not found at $ANTITRICHE_FILE"
  ANTITRICHE_DATA="{\"report\":[]}"
fi

# Step 3: Collect agent results
AGENT_RESULTS=()
for i in $(seq -f "%02g" 1 $N_AGENTS); do
  RESULT_FILE="$SESSION_LOG_DIR/agent_${i}_result.json"
  if [ -f "$RESULT_FILE" ]; then
    AGENT_RESULTS+=("$(cat "$RESULT_FILE")")
  fi
done

# Generate markdown report
cat > "$REPORT_PATH" << EOF
# GPU Optimization Report - Session $SESSION_ID

**Generated**: $(date)
**GPU**: $GPU_NAME
**Total Agents**: $N_AGENTS

## Executive Summary

EOF

# Calculate statistics
SUCCESS_COUNT=$(echo "$AGENT_RESULTS" | jq -r '[.status] | select(. == "success") | length' 2>/dev/null || echo "0")
TOTAL_COUNT=${#AGENT_RESULTS[@]}
SPEEDUP_SUM=$(echo "$BENCHMARK_DATA" | jq -r '[.results[].speedup] | add' 2>/dev/null || echo "0")
SPEEDUP_COUNT=$(echo "$BENCHMARK_DATA" | jq -r '[.results[].speedup] | length' 2>/dev/null || echo "1")

if [ "$SPEEDUP_COUNT" -gt 0 ]; then
  AVG_SPEEDUP=$(python3 -c "print(f'{$SPEEDUP_SUM/$SPEEDUP_COUNT:.2f}')")
else
  AVG_SPEEDUP="N/A"
fi

cat >> "$REPORT_PATH" << EOF
| Metric | Value |
|--------|-------|
| Total Agents | $N_AGENTS |
| Successful Optimizations | $SUCCESS_COUNT |
| Completion Rate | $(python3 -c "print(f'{100*$SUCCESS_COUNT/$N_AGENTS:.1f}%')") |
| Average Speedup | ${AVG_SPEEDUP}x |

## Configuration

| Parameter | Value |
|-----------|-------|
| Session ID | \`$SESSION_ID\` |
| Total Agents | $N_AGENTS |
| GPU | $GPU_NAME |

EOF

# Benchmark Results Section
echo "## Benchmark Results" >> "$REPORT_PATH"
echo "" >> "$REPORT_PATH"

# Extract benchmark results
if [ -f "$BENCHMARK_FILE" ]; then
  echo "| Agent | Baseline (ms) | Optimized (ms) | Speedup | Status |" >> "$REPORT_PATH"
  echo "|-------|---------------|----------------|---------|--------|" >> "$REPORT_PATH"

  for i in $(seq -f "%02g" 1 $N_AGENTS); do
    BENCH_FILE="$SESSION_LOG_DIR/benchmark_${i}.json"
    if [ -f "$BENCH_FILE" ]; then
      BASELINE=$(cat "$BENCH_FILE" | jq -r '.benchmarks[] | select(.name | contains("Baseline_3D_Large")) | .mean' 2>/dev/null || echo "N/A")
      OPTIMIZED=$(cat "$BENCH_FILE" | jq -r '.benchmarks[] | select(.name | contains("Optimized_3D_Large")) | .mean' 2>/dev/null || echo "N/A")
      SPD=$(cat "$BENCH_FILE" | jq -r '.benchmarks[] | select(.name | contains("Optimized_3D_Large")) | .mean' | \
        xargs -I {} python3 -c "print(f'{float($(cat "$BENCH_FILE" | jq -r '.benchmarks[] | select(.name | contains("Baseline_3D_Large")) | .mean')')/float({}):.2f}')" 2>/dev/null || echo "N/A")
      echo "| $i | $BASELINE | $OPTIMIZED | ${SPD}x | ✓ |" >> "$REPORT_PATH"
    fi
  done
else
  echo "No benchmark results available." >> "$REPORT_PATH"
fi

echo "" >> "$REPORT_PATH"

# Anti-Triche Section
echo "## Anti-Triche Analysis" >> "$REPORT_PATH"
echo "" >> "$REPORT_PATH"

if [ -f "$ANTITRICHE_FILE" ]; then
  TRUSTED_COUNT=$(cat "$ANTITRICHE_FILE" | jq -r '.trusted_count')
  SUSPECTS_COUNT=$(cat "$ANTITRICHE_FILE" | jq -r '.suspects | length')

  echo "- **Trusted Agents**: $TRUSTED_COUNT / $N_AGENTS" >> "$REPORT_PATH"
  echo "- **Suspect Agents**: $SUSPECTS_COUNT" >> "$REPORT_PATH"

  if [ "$SUSPECTS_COUNT" -gt 0 ]; then
    SUSPECTS=$(cat "$ANTITRICHE_FILE" | jq -r '.suspects[]')
    echo "- **Suspect IDs**: $(echo $SUSPECTS | paste -sd,)" >> "$REPORT_PATH"
  fi
else
  echo "No anti-triche analysis available." >> "$REPORT_PATH"
fi

echo "" >> "$REPORT_PATH"

# Agent Details Section
echo "## Agent Details" >> "$REPORT_PATH"
echo "" >> "$REPORT_PATH"
echo "| Agent | Persona | Risk | Expertise | OptType | Status | Optimization |" >> "$REPORT_PATH"
echo "|-------|---------|------|-----------|---------|--------|--------------|" >> "$REPORT_PATH"

for i in $(seq -f "%02g" 1 $N_AGENTS); do
  # Get persona
  PERSONA=$(echo "$PERSONAS" | jq -r ".[] | select(.agent_id == \"$i\")")

  # Get result
  RESULT_FILE="$SESSION_LOG_DIR/agent_${i}_result.json"
  if [ -f "$RESULT_FILE" ]; then
    RESULT=$(cat "$RESULT_FILE")
    STATUS=$(echo "$RESULT" | jq -r '.status')
    OPT_NAME=$(echo "$RESULT" | jq -r '.optimization.name // "N/A"')
    OPT_DESC=$(echo "$RESULT" | jq -r '.optimization.description // "N/A"')
  else
    STATUS="unknown"
    OPT_NAME="N/A"
    OPT_DESC="N/A"
  fi

  RISK=$(echo "$PERSONA" | jq -r '.risk // "N/A"')
  EXPERTISE=$(echo "$PERSONA" | jq -r '.expertise // "N/A"')
  OPT_TYPE=$(echo "$PERSONA" | jq -r '.opt_type // "N/A"')

  if [ "$STATUS" = "success" ]; then
    STATUS="✅"
  elif [ "$STATUS" = "build_failed" ]; then
    STATUS="❌ Build"
  elif [ "$STATUS" = "tests_failed" ]; then
    STATUS="⚠️  Tests"
  else
    STATUS="? $STATUS"
  fi

  echo "| $i | (persona) | $RISK | $EXPERTISE | $OPT_TYPE | $STATUS | $OPT_NAME |" >> "$REPORT_PATH"
done

# Recommendations
echo "" >> "$REPORT_PATH"
echo "## Recommendations" >> "$REPORT_PATH"
echo "" >> "$REPORT_PATH"
echo "1. Review the top performing optimizations above" >> "$REPORT_PATH"
echo "2. Check agent logs for detailed implementation notes" >> "$REPORT_PATH"
echo "3. Run anti-triche analysis if not already done" >> "$REPORT_PATH"
echo "4. Consider combining compatible optimizations" >> "$REPORT_PATH"

# Appendix
echo "" >> "$REPORT_PATH"
echo "## Appendix" >> "$REPORT_PATH"
echo "" >> "$REPORT_PATH"
echo "### Session Files" >> "$REPORT_PATH"
echo "- Session directory: \`$SESSION_LOG_DIR\`" >> "$REPORT_PATH"
echo "- Orchestrator log: \`orchestrator.log\`" >> "$REPORT_PATH"
echo "- Personas: \`personas.json\`" >> "$REPORT_PATH"
echo "- Benchmark results: \`benchmark_results.json\`" >> "$REPORT_PATH"
echo "- Anti-triche report: \`antitriche_report.json\`" >> "$REPORT_PATH"
echo "" >> "$REPORT_PATH"
echo "### Agent Logs" >> "$REPORT_PATH"
for i in $(seq -f "%02g" 1 $N_AGENTS); do
  if [ -f "$SESSION_LOG_DIR/agent_${i}.log" ]; then
    echo "- [Agent $i log](agent_${i}.log)" >> "$REPORT_PATH"
  fi
done

echo "Report generated: $REPORT_PATH"
```

## Output Format

Return confirmation:
```json
{
  "report_agent": "specialized",
  "session_id": "$SESSION_ID",
  "report_path": "$REPORT_PATH",
  "agents_analyzed": $N_AGENTS,
  "successful_builds": $SUCCESS_COUNT
}
```

Generate comprehensive markdown report with all sections filled.
