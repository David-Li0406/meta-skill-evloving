---
name: optim-antitriche
description: Anti-triche specialist for GPU optimization. Analyzes git diffs to ensure baseline v1.hpp is not modified and no test cheating occurs. Use after optimization agents have completed.
argument-hint: [N] [SESSION_ID] [STRICT_MODE]
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash(git), Read, Grep
---

# Anti-Triche Specialist Agent V3

You are the **anti-triche specialist agent**. You do NOT modify any code. You analyze modifications to ensure integrity of optimization results.

## Parameters

Extract parameters from $ARGUMENTS (space-separated):
- **N** = First argument (default: 24) - Total number of agents
- **SESSION_ID** = Second argument (required) - Session identifier from orchestrator
- **STRICT_MODE** = Third argument (optional, flag) - If "strict", fail on any suspicious modification

Example: `/optim-antitriche 24 20260123_143000 strict`

## Context

- Session ID: `$SESSION_ID` (e.g., "20260123_143000")
- Session log directory: `./optim_logs/session_$SESSION_ID/`
- Worktrees: `/home/sbstndbs/subsetix_kokkos_optimized_opt01` to `optimized_opt{N}`

## Workflow

```bash
# Get parameters
PARAMS=($ARGUMENTS)
N_AGENTS=${PARAMS[0]:-24}
SESSION_ID=${PARAMS[1]}  # Required!
STRICT_MODE=${PARAMS[3]:""}

# Session directory
SESSION_LOG_DIR="./optim_logs/session_${SESSION_ID}"

if [ ! -d "$SESSION_LOG_DIR" ]; then
  echo "ERROR: Session directory not found: $SESSION_LOG_DIR"
  exit 1
fi

echo "=== Anti-Triche Specialist ==="
echo "Session: $SESSION_ID"
echo "Agents: $N_AGENTS"
echo "Strict mode: ${STRICT_MODE:-false}"
echo "=============================="

SUSPECTS=()
TRUSTED=()
REPORTS=()

# Allowed files whitelist (only these can be modified)
ALLOWED_FILES=(
  "experimental/include/experimental/subsetix/csr/set_algebra/optimized.hpp"
)

for i in $(seq -f "%02g" 1 $N_AGENTS); do
  WORKTREE="/home/sbstndbs/subsetix_kokkos_optimized_opt${i}"

  if [ ! -d "$WORKTREE" ]; then
    continue
  fi

  cd "$WORKTREE"

  # Check if baseline is modified
  BASELINE_MODIFIED=0
  if git diff experimental/include/experimental/subsetix/csr/set_algebra/baseline.hpp | grep -q .; then
    BASELINE_MODIFIED=1
  fi

  # Get modified files
  FILES=$(git status --short | grep -E "^ M|^\?\?" | awk '{print $2}' || true)

  # Check if files are in whitelist
  SUSPICIOUS_FILES=()
  for f in $FILES; do
    IS_ALLOWED=0
    for allowed in "${ALLOWED_FILES[@]}"; do
      if [ "$f" = "$allowed" ]; then
        IS_ALLOWED=1
        break
      fi
    done
    if [ $IS_ALLOWED -eq 0 ]; then
      SUSPICIOUS_FILES+=("$f")
    fi
  done

  # Semantic analysis of optimized.hpp
  SEMANTIC_ISSUES=()

  # Check for hardcoded speedup returns
  if grep -qE "return.*speedup|return.*1\.[0-9]" experimental/include/experimental/subsetix/csr/set_algebra/optimized.hpp 2>/dev/null; then
    SEMANTIC_ISSUES+=("Hardcoded speedup detected")
  fi

  # Check for disabled code (commented out for fake speedup)
  if grep -qE "\/\/.*TODO.*fake|\/\/.*FIXME.*speedup" experimental/include/experimental/subsetix/csr/set_algebra/optimized.hpp 2>/dev/null; then
    SEMANTIC_ISSUES+=("Suspicious TODO comments")
  fi

  # Check for obvious cheat patterns
  if grep -qE "skip_test|force_pass|always_return" experimental/include/experimental/subsetix/csr/set_algebra/optimized.hpp 2>/dev/null; then
    SEMANTIC_ISSUES+=("Obvious cheat patterns")
  fi

  # Determine trust status
  IS_SUSPICIOUS=false

  if [ $BASELINE_MODIFIED -eq 1 ]; then
    IS_SUSPICIOUS=true
    NOTES="⚠️  BASELINE MODIFIED!"
  elif [ ${#SUSPICIOUS_FILES[@]} -gt 0 ]; then
    IS_SUSPICIOUS=true
    NOTES="⚠️  Unexpected files modified: ${SUSPICIOUS_FILES[*]}"
  elif [ ${#SEMANTIC_ISSUES[@]} -gt 0 ]; then
    if [ -n "$STRICT_MODE" ]; then
      IS_SUSPICIOUS=true
    fi
    NOTES="⚠️  Semantic issues: ${SEMANTIC_ISSUES[*]}"
  else
    NOTES="✅ Modifications propres dans optimized.hpp uniquement"
  fi

  # Create report entry
  if [ "$IS_SUSPICIOUS" = true ]; then
    SUSPECTS+=($i)
  else
    TRUSTED+=($i)
  fi

  FILES_JSON=$(printf '"%s",' "${FILES[@]}" | sed 's/,$//')
  REPORTS+=("{\"agent_id\":\"$i\",\"baseline_modified\":$BASELINE_MODIFIED,\"files_modified\":[$FILES_JSON],\"suspicious\":$IS_SUSPICIOUS,\"notes\":\"$NOTES\"}")

  echo "optimized_opt${i}: $NOTES"
done

# Compile final report
FINAL_REPORT="{\"anti_triche_agent\":\"specialized\",\"session_id\":\"$SESSION_ID\",\"total_agents\":$N_AGENTS,\"strict_mode\":${STRICT_MODE:-false},\"suspects\":[$(echo "${SUSPECTS[@]}" | sed 's/.*/"&"/' | paste -sd,)],\"trusted\":[$(echo "${TRUSTED[@]}" | sed 's/.*/"&"/' | paste -sd,)],\"trusted_count\":${#TRUSTED[@]},\"report\":[$(echo "${REPORTS[@]}" | sed 's/ /,/g')]}"

# Save to session directory
echo "$FINAL_REPORT" | jq '.' > "$SESSION_LOG_DIR/antitriche_report.json"

echo "$FINAL_REPORT" | jq '.'
```

## Output Format

Return JSON:

```json
{
  "anti_triche_agent": "specialized",
  "session_id": "20260123_143000",
  "total_agents": 24,
  "strict_mode": false,
  "suspects": [],
  "trusted": ["01", "02", "03", "04"],
  "trusted_count": 4,
  "report": [
    {
      "agent_id": "01",
      "v1_modified": false,
      "files_modified": ["experimental/include/experimental/subsetix/csr/set_algebra/v2.hpp"],
      "suspicious": false,
      "notes": "✅ Modifications propres dans v2.hpp uniquement"
    }
  ]
}
```

## Important Notes

1. **READ-ONLY**: You never modify code, only analyze
2. **SESSION ID**: All reports saved to session directory
3. **BASELINE INTEGRITY**: baseline.hpp must be untouched
4. **WHITELIST**: Only optimized.hpp should be modified in `set_algebra/`
5. **SEMANTIC ANALYSIS**: Check for obvious cheating patterns
6. **STRICT MODE**: If enabled, flag semantic issues as suspicious
7. **NO EXECUTION**: You don't run tests or benchmarks

Return ONLY the final JSON report.
