#!/bin/bash
# ==============================================================================
# lib/state.sh - Pipeline State Management with File Locking
#
# Manages state persistence across commands with atomic file operations.
# Uses mkdir (atomic on both macOS and Linux) as lock primitive.
# ==============================================================================

# Get state file path for a spec
get_state_file_path() {
    local spec_file="$1"
    local spec_basename
    spec_basename=$(basename "$spec_file" .md)
    mkdir -p "$PIPELINE_STATE_DIR"
    echo "$PIPELINE_STATE_DIR/${spec_basename}.state.json"
}

# Read pipeline state (returns empty JSON object if no state)
read_pipeline_state() {
    local state_file="$1"
    if [[ -f "$state_file" ]]; then
        cat "$state_file"
    else
        echo '{}'
    fi
}

# Write pipeline state with atomic file locking (macOS/Linux compatible)
write_pipeline_state() {
    local state_file="$1"
    local state_json="$2"
    local lock_dir="${state_file}.lock"
    local temp_file="${state_file}.tmp"
    local retries=0
    local max_retries=10

    # Atomic directory creation as lock primitive
    while [[ $retries -lt $max_retries ]]; do
        if mkdir "$lock_dir" 2>/dev/null; then
            # Lock acquired - write atomically
            echo "$state_json" > "$temp_file"
            mv "$temp_file" "$state_file"
            rmdir "$lock_dir"
            return 0
        fi
        retries=$((retries + 1))
        sleep 0.01
    done

    # Fallback: write without lock if unable to acquire
    echo "$state_json" > "$state_file"
}

# Update pipeline state with new command findings (atomic)
update_pipeline_state() {
    local state_file="$1"
    local command="$2"
    local findings="$3"
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    local current_state
    current_state=$(read_pipeline_state "$state_file")

    # Use python for safe JSON manipulation
    local new_state
    new_state=$(python3 << PYTHON_EOF 2>/dev/null
import json
from datetime import datetime

try:
    current = json.loads('''$current_state''')
except:
    current = {}

try:
    findings_obj = json.loads('''$findings''')
except:
    findings_obj = {}

current['$command'] = {
    'timestamp': '$timestamp',
    'findings': findings_obj
}
current['last_updated'] = '$timestamp'
current['last_command'] = '$command'

print(json.dumps(current, indent=2))
PYTHON_EOF
)

    if [[ -n "$new_state" ]]; then
        write_pipeline_state "$state_file" "$new_state"
    fi
}

# Check if a step has been completed
state_has_command() {
    local state_file="$1"
    local command="$2"
    local state
    state=$(read_pipeline_state "$state_file")
    echo "$state" | grep -q "\"$command\""
}

# Get accumulated issues count from state (used for confidence scoring)
get_accumulated_issues() {
    local state_file="$1"
    local state
    state=$(read_pipeline_state "$state_file")

    python3 << PYTHON_EOF 2>/dev/null
import json
try:
    state_obj = json.loads('''$state''')
except:
    state_obj = {}

issues = 0

# Count stress-test issues
st = state_obj.get('stress-test', {}).get('findings', {})
issues += len(st.get('invariant_violations', []))
issues += len(st.get('critical_blockers', []))

# Count validate issues
v = state_obj.get('validate', {}).get('findings', {})
issues += len(v.get('ambiguity_flags', []))

print(issues)
PYTHON_EOF
    echo "0"
}
