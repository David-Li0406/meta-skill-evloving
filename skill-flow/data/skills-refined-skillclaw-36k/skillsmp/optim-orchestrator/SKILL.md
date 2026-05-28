---
name: optim-orchestrator
description: Orchestrate N optimization agents with random personas for Kokkos CUDA GPU optimization. Use when optimizing GPU code, running parallel optimization experiments, or benchmarking different algorithm variants.
argument-hint: [N] [CHUNK_SIZE] [BUILD_JOBS] [TIMEOUT] [LOG_DIR]
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash(git, cmake, ctest), Read, Edit, Task, Write
---

# GPU Optimization Orchestrator V3

You are orchestrating **N optimization agents** for Kokkos CUDA GPU optimization.

## Parameters

Extract parameters from $ARGUMENTS (space-separated):
- **N** = First argument (default: 24)
- **CHUNK_SIZE** = Second argument (default: 4)
- **BUILD_JOBS** = Third argument (default: 4) - Compile with `-j{BUILD_JOBS}`
- **TIMEOUT** = Fourth argument (default: 1800) - Per-agent timeout in seconds (30 min default)
- **LOG_DIR** = Fifth argument (default: `./optim_logs`) - Directory for agent logs

Example: `/optim-orchestrator 24 4 4 1800 ./logs` → 24 agents, chunks of 4, -j4, 30min timeout, custom logs

## Key Changes in V3

1. **Session ID**: Unique timestamp per run for isolation
2. **Build from Scratch**: Always clean build directories before starting
3. **Smart Monitoring**: Progress checks every 60s, not on every action
4. **Worktree Management**: Reset worktrees to clean state at session start

## Auto-detected

- **SESSION_ID**: Unique timestamp for this run (e.g., `20260123_143000`)
- **GPU_ARCH**: Auto-detected with `nvidia-smi -L`
- **GPU_NAME**: Auto-detected for reporting

## Context

- Repository: Current directory (must be subsetix_kokkos)
- Target file: `experimental/include/experimental/subsetix/csr/set_algebra/optimized.hpp`
- Baseline: `baseline.hpp` (NEVER modify)
- Benchmark target: 3D Large (~5M rows)

## Phase 0: Setup & Session Initialization

```bash
# Get parameters
PARAMS=($ARGUMENTS)
N_AGENTS=${PARAMS[0]:-24}
CHUNK_SIZE=${PARAMS[1]:-4}
BUILD_JOBS=${PARAMS[2]:-4}
TIMEOUT=${PARAMS[3]:-1800}
LOG_DIR=${PARAMS[4]:-"./optim_logs"}

# Create session with unique ID
SESSION_ID=$(date +%Y%m%d_%H%M%S)
SESSION_LOG_DIR="$LOG_DIR/session_${SESSION_ID}"
mkdir -p "$SESSION_LOG_DIR"

# Detect GPU
GPU_INFO=$(nvidia-smi -L 2>/dev/null | head -1)
GPU_NAME=$(echo "$GPU_INFO" | sed 's/GPU 0: //;s/(UUID.*//;s/ *$//')

# Map GPU name to Kokkos architecture
case "$GPU_NAME" in
  *RTX*40*|*4070*|*4060*) GPU_ARCH="ADA89" ;;
  *RTX*30*|*3050*) GPU_ARCH="AMPERE86" ;;
  *RTX*20*|*2080*) GPU_ARCH="TURING75" ;;
  *A100*) GPU_ARCH="AMPERE80" ;;
  *H100*) GPU_ARCH="HOPPER90" ;;
  *) GPU_ARCH="AMPERE86" ;;  # Default fallback
esac

# Session log file
LOG_FILE="$SESSION_LOG_DIR/orchestrator.log"

echo "=== GPU Optimization Orchestrator V3 ===" | tee "$LOG_FILE"
echo "Session ID: $SESSION_ID" | tee -a "$LOG_FILE"
echo "GPU: $GPU_NAME ($GPU_ARCH)" | tee -a "$LOG_FILE"
echo "Agents: $N_AGENTS | Chunk: $CHUNK_SIZE | Jobs: $BUILD_JOBS" | tee -a "$LOG_FILE"
echo "Session dir: $SESSION_LOG_DIR" | tee -a "$LOG_FILE"
echo "=====================================" | tee -a "$LOG_FILE"
```

## Phase 1: Prepare Worktrees (Reset to Clean State)

```bash
cd /home/sbstndbs/subsetix_kokkos

# Clean up worktrees from previous sessions
for i in $(seq -f "%02g" 1 $N_AGENTS); do
  WORKTREE="../subsetix_kokkos_optimized_opt${i}"

  # Remove existing worktree
  if git worktree list | grep -q "optimized_opt${i}"; then
    echo "Removing old worktree optimized_opt${i}..." | tee -a "$LOG_FILE"
    git worktree remove "$WORKTREE" --force 2>&1 | tee -a "$LOG_FILE" || true
    git branch -D "feature/optimized-opt${i}" 2>/dev/null || true
  fi

  # Create fresh worktree from current HEAD
  echo "Creating fresh worktree optimized_opt${i}..." | tee -a "$LOG_FILE"
  git worktree add "$WORKTREE" -b "feature/optimized-opt${i}-session-${SESSION_ID}" >> "$LOG_FILE" 2>&1

  # Clean any existing builds
  rm -rf "$WORKTREE/build-experimental-cuda"

  # Verify optimized.hpp exists
  if [ ! -f "$WORKTREE/experimental/include/experimental/subsetix/csr/set_algebra/optimized.hpp" ]; then
    echo "ERROR: optimized.hpp not found in $WORKTREE" | tee -a "$LOG_FILE"
    exit 1
  fi
done

echo "✓ Prepared $N_AGENTS clean worktrees" | tee -a "$LOG_FILE"
```

## Phase 2: Generate N Personas

For each agent, generate a random profile with 6 cursors:

```python
import random

def generate_persona(agent_id: int) -> dict:
    # Cursor 1: Risk (weighted)
    risk = random.choices(
        ["Conservative", "Moderate", "Aggressive", "Experimental"],
        weights=[0.25, 0.40, 0.25, 0.10]
    )[0]

    # Cursor 2: Expertise
    expertise = random.choice([
        "KokkosSpecialist", "GPUArchitect", "AlgorithmExpert",
        "MemoryArchitect", "SystemsThinker", "ParallelismExpert",
        "DataStructureSpecialist"
    ])

    # Cursor 3: OptType
    opt_type = random.choice([
        "QuickWin", "KokkosPattern", "GPUHwSpecific",
        "Algorithmic", "Structural", "MemoryLayout", "LatencyHiding"
    ])

    # Cursor 4: Style (weighted)
    style = random.choices(
        ["Analytical", "Experimental", "Incremental", "Hybrid"],
        weights=[0.2, 0.3, 0.2, 0.3]
    )[0]

    # Cursor 5: Scope
    scope = random.choice(["Local", "Regional", "Global"])

    # Cursor 6: Innovation (weighted)
    innovation = random.choices(
        ["Proven", "Novel", "Wild"],
        weights=[0.4, 0.4, 0.2]
    )[0]

    return {
        "agent_id": f"{agent_id:02d}",
        "risk": risk,
        "expertise": expertise,
        "opt_type": opt_type,
        "style": style,
        "scope": scope,
        "innovation": innovation
    }
```

Save personas to `$SESSION_LOG_DIR/personas.json`

## Phase 3: Launch Agents (Chunks)

Launch N agents in chunks of CHUNK_SIZE using the Task tool.

**IMPORTANT - Build from Scratch:**
Each agent MUST start with a clean build:
```bash
# Before building, ensure clean state
rm -rf build-experimental-cuda
cmake --preset experimental-cuda -DKokkos_ARCH_${GPU_ARCH}=ON
cmake --build --preset experimental-cuda -j${BUILD_JOBS}
```

**SMART MONITORING:**
- Check progress every ~60 seconds (not on every action)
- Look for heartbeat signals in logs
- If no progress for 120s, consider agent stuck

**TIMEOUT HANDLING:**
- Per-agent timeout is generous (default 30 min)
- Check agent status periodically
- If timeout exceeded, mark as failed and continue

**AGENT TASK TEMPLATE:**
```text
You are optimization agent {agent_id} with persona:
{persona_json}

WORKTREE: /home/sbstndbs/subsetix_kokkos_optimized_opt{agent_id:02d}
TARGET: experimental/include/experimental/subsetix/csr/set_algebra/optimized.hpp
GPU: $GPU_ARCH

STEPS:
1. Read optimized.hpp and analyze according to your persona
2. Find ONE optimization matching your profile
3. Implement the optimization
4. Clean build: rm -rf build-experimental-cuda
5. Configure: cmake --preset experimental-cuda -DKokkos_ARCH_$GPU_ARCH=ON
6. Build: cmake --build --preset experimental-cuda -j$BUILD_JOBS
7. Test: ctest --preset experimental-cuda --output-on-failure
8. Return JSON result

Return ONLY this JSON format:
{
  "agent_id": "{agent_id:02d}",
  "persona": {...},
  "optimization": {"name": "...", "description": "..."},
  "status": "success|build_failed|tests_failed",
  "log_file": "..."
}
```

## Phase 4: Monitor and Collect

**Smart monitoring loop:**
```bash
# Check progress every 60 seconds
while true; do
  sleep 60

  # Check for heartbeat (recent log activity)
  for i in $(seq -f "%02g" 1 $N_AGENTS); do
    LOG="$SESSION_LOG_DIR/agent_${i}.log"
    if [ -f "$LOG" ]; then
      LAST_ACTIVITY=$(stat -c %Y "$LOG")
      NOW=$(date +%s)
      ELAPSED=$((NOW - LAST_ACTIVITY))

      # Alert if no activity for 2 minutes
      if [ $ELAPSED -gt 120 ]; then
        echo "⚠️  Agent $i appears stuck (no activity for ${ELAPSED}s)" | tee -a "$LOG_FILE"
      fi
    fi
  done

  # Check if all agents completed
  PENDING=$(find "$SESSION_LOG_DIR" -name "agent_*_result.json" 2>/dev/null | wc -l)
  if [ $PENDING -eq $N_AGENTS ]; then
    break
  fi
done
```

## Phase 5: Final Summary

Save results to `$SESSION_LOG_DIR/results.json`:

```json
{
  "session_id": "$SESSION_ID",
  "orchestrator": "v3",
  "gpu_arch": "$GPU_ARCH",
  "n_agents": $N_AGENTS,
  "successful": 4,
  "failed": 0,
  "optimizations": [...],
  "results": [
    {"agent_id": "01", "status": "success", "optimization": {...}},
    ...
  ]
}
```

## Return Format

```json
{
  "orchestrator": "v3",
  "session_id": "$SESSION_ID",
  "gpu_arch": "$GPU_ARCH",
  "n_agents": $N_AGENTS,
  "successful": N,
  "failed": M,
  "session_dir": "$SESSION_LOG_DIR",
  "log_file": "$LOG_FILE",
  "results_file": "$SESSION_LOG_DIR/results.json",
  "next_steps": [
    "Run benchmark specialist: /optim-benchmark $N_AGENTS $SESSION_ID",
    "Run anti-triche: /optim-antitriche $N_AGENTS $SESSION_ID",
    "Generate report: /optim-report $N_AGENTS $SESSION_LOG_DIR"
  ]
}
```

## Session Directory Structure

```
$LOG_DIR/
└── session_20260123_143000/
    ├── orchestrator.log           # Main orchestrator log
    ├── personas.json              # Generated personas
    ├── results.json               # Final results
    ├── agent_01.log               # Individual agent logs
    ├── agent_01_result.json       # Agent results
    ├── agent_02.log
    ├── agent_02_result.json
    └── ...
```
