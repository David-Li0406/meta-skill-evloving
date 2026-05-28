#!/bin/bash
set -euo pipefail

LOG="/tmp/ntm-e2e-spawn-assign-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

log() {
  local level="$1"
  shift
  echo "[$(date -Iseconds)] [$level] $*"
}

log_info() { log "INFO" "$@"; }
log_debug() { log "DEBUG" "$@"; }
log_pass() { log "PASS" "$@"; }
log_fail() { log "FAIL" "$@"; }

log_info "Starting ntm spawn --assign E2E test"
log_info "Log file: $LOG"

if ! command -v br >/dev/null 2>&1; then
  log_fail "br not installed"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  log_fail "jq not installed"
  exit 1
fi

BASE_DIR="/tmp/ntm-spawn-assign-test-$$"
SESSION="ntm-spawn-assign-$$"
PROJECT_DIR="${BASE_DIR}/${SESSION}"
CONFIG_DIR="${BASE_DIR}/config"
CONFIG_PATH="${CONFIG_DIR}/config.toml"

log_info "Setup: creating test workspace"
mkdir -p "$PROJECT_DIR" "$CONFIG_DIR"
cd "$PROJECT_DIR"

cat > "$CONFIG_PATH" <<EOF
projects_base = "$BASE_DIR"

[agents]
claude = "bash"
codex = "bash"
gemini = "bash"
EOF

log_info "Initializing beads"
br init >/dev/null

declare -A BEAD_MAP
for i in 1 2 3 4; do
  log_debug "Creating bead $i"
  out="$(br create "Spawn assign bead $i" -t task -p 2 --json)"
  bead_id="$(echo "$out" | jq -r '.[0].id // .id // empty')"
  if [[ -z "$bead_id" ]]; then
    log_fail "Failed to parse bead id from: $out"
    exit 1
  fi
  BEAD_MAP["$bead_id"]=1
done

br sync --flush-only >/dev/null

log_info "Step 1: spawn --assign"
log_debug "Running ntm spawn --assign"
RESULT="$(NTM_PROJECTS_BASE="$BASE_DIR" ntm --config "$CONFIG_PATH" --json spawn "$SESSION" --cc=2 --no-user --assign --strategy=round-robin)"
log_debug "Spawn output: $RESULT"

log_info "Step 2: verify spawn"
agent_count="$(echo "$RESULT" | jq -r '.spawn.agent_counts.claude // 0')"
if [[ "$agent_count" -lt 2 ]]; then
  log_fail "Expected at least 2 Claude agents, got $agent_count"
  exit 1
fi
log_pass "Spawned $agent_count Claude agents"

log_info "Step 3: verify assignments"
assigned_count="$(echo "$RESULT" | jq -r '.assign.summary.assigned_count // 0')"
if [[ "$assigned_count" -lt 2 ]]; then
  log_fail "Expected at least 2 assignments, got $assigned_count"
  exit 1
fi
log_pass "Assigned $assigned_count beads"

log_info "Step 4: verify assignment bead IDs"
assignment_ids="$(echo "$RESULT" | jq -r '.assign.assignments[].bead_id')"
if [[ -z "$assignment_ids" ]]; then
  log_fail "No assignments returned"
  exit 1
fi

while IFS= read -r bead_id; do
  if [[ -z "${BEAD_MAP[$bead_id]:-}" ]]; then
    log_fail "Unexpected bead_id in assignments: $bead_id"
    exit 1
  fi
done <<< "$assignment_ids"

log_pass "All assignments match created beads"

log_info "Cleanup: killing session"
NTM_PROJECTS_BASE="$BASE_DIR" ntm --config "$CONFIG_PATH" kill -f "$SESSION" >/dev/null || true

log_info "Cleanup: removing test workspace"
rm -rf "$BASE_DIR"

log_pass "ntm spawn --assign E2E test passed"
