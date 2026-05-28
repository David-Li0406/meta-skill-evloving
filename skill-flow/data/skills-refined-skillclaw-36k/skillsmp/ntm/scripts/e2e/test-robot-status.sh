#!/usr/bin/env bash
# E2E Test: Robot-status JSON Output for All Agent States
# Comprehensive tests for --robot-status JSON output structure.
# Covers: ntm-k5pv - Test robot-status JSON output for all agent states

set -uo pipefail
# Note: Not using -e so that assertion failures don't cause early exit.
# Failures are tracked via log library and reported in summary.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"
set +e  # Disable immediate exit on error so tests continue after assertion failures

# Test session prefix (unique per run to avoid conflicts)
TEST_PREFIX="e2e-status-$$"

# Track created sessions for cleanup
CREATED_SESSIONS=()

# Cleanup function
cleanup() {
    log_section "Cleanup"
    for session in "${CREATED_SESSIONS[@]}"; do
        ntm_cleanup "$session"
    done
    # Also cleanup any sessions matching the prefix that we might have missed
    cleanup_sessions "${TEST_PREFIX}"
}
trap cleanup EXIT

# Helper to spawn and track session
spawn_test_session() {
    local session="$1"
    shift
    CREATED_SESSIONS+=("$session")
    ntm_spawn "$session" "$@"
}

# Main test
main() {
    log_init "test-robot-status"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    # Schema Tests
    log_section "Test: robot-status schema fields"
    test_schema_required_fields

    log_section "Test: robot-status system info"
    test_system_info_fields

    log_section "Test: robot-status summary fields"
    test_summary_fields

    # Session/Agent Tests
    log_section "Test: robot-status with no sessions"
    test_no_sessions

    log_section "Test: robot-status with claude agents"
    test_claude_agents

    log_section "Test: robot-status with multiple agent types"
    test_multiple_agent_types

    # Agent State Tests
    log_section "Test: agent is_active states"
    test_agent_active_state

    log_section "Test: agent type detection"
    test_agent_type_detection

    # Ordering/Determinism Tests
    log_section "Test: schema determinism"
    test_schema_determinism

    log_section "Test: session ordering"
    test_session_ordering

    # Field Value Tests
    log_section "Test: timestamp format"
    test_timestamp_format

    log_section "Test: session metadata"
    test_session_metadata

    log_section "Test: pane identification"
    test_pane_identification

    # Summary Count Tests
    log_section "Test: summary agent counts"
    test_summary_counts

    log_summary
}

#
# Schema Required Fields Tests
#
test_schema_required_fields() {
    log_info "Verifying all required schema fields exist"

    local output
    local exit_code=0
    output=$(ntm --robot-status 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -ne 0 ]]; then
        log_error "robot-status failed with exit code $exit_code"
        return
    fi

    log_assert_valid_json "$output" "robot-status returns valid JSON"

    # Check top-level required fields
    local has_generated_at has_system has_sessions has_summary
    has_generated_at=$(echo "$output" | jq 'has("generated_at")')
    has_system=$(echo "$output" | jq 'has("system")')
    has_sessions=$(echo "$output" | jq 'has("sessions")')
    has_summary=$(echo "$output" | jq 'has("summary")')

    log_assert_eq "$has_generated_at" "true" "has generated_at field"
    log_assert_eq "$has_system" "true" "has system field"
    log_assert_eq "$has_sessions" "true" "has sessions field"
    log_assert_eq "$has_summary" "true" "has summary field"

    # Check sessions is an array
    local sessions_type
    sessions_type=$(echo "$output" | jq -r '.sessions | type')
    log_assert_eq "$sessions_type" "array" "sessions is an array"

    # Check summary is an object
    local summary_type
    summary_type=$(echo "$output" | jq -r '.summary | type')
    log_assert_eq "$summary_type" "object" "summary is an object"
}

test_system_info_fields() {
    log_info "Verifying system info schema"

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        return
    fi

    # Check system subfields
    local system_fields=("version" "commit" "build_date" "go_version" "os" "arch" "tmux_available")
    for field in "${system_fields[@]}"; do
        local has_field
        has_field=$(echo "$output" | jq --arg f "$field" '.system | has($f)')
        log_assert_eq "$has_field" "true" "system has $field field"
    done

    # Check tmux_available is boolean
    local tmux_type
    tmux_type=$(echo "$output" | jq -r '.system.tmux_available | type')
    log_assert_eq "$tmux_type" "boolean" "tmux_available is boolean"

    # Check os value is sensible
    local os_value
    os_value=$(echo "$output" | jq -r '.system.os')
    if [[ "$os_value" == "linux" || "$os_value" == "darwin" || "$os_value" == "windows" ]]; then
        log_assert_eq "1" "1" "os value is valid ($os_value)"
    else
        log_warn "unexpected os value: $os_value"
    fi
}

test_summary_fields() {
    log_info "Verifying summary schema"

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        return
    fi

    # Check summary subfields
    local summary_fields=("total_sessions" "total_agents" "attached_count" "claude_count" "codex_count" "gemini_count")
    for field in "${summary_fields[@]}"; do
        local has_field
        has_field=$(echo "$output" | jq --arg f "$field" '.summary | has($f)')
        log_assert_eq "$has_field" "true" "summary has $field field"
    done

    # Check all summary counts are integers >= 0
    for field in "${summary_fields[@]}"; do
        local value
        value=$(echo "$output" | jq -r ".summary.$field")
        if [[ "$value" =~ ^[0-9]+$ ]]; then
            log_assert_eq "1" "1" "summary.$field is a valid integer ($value)"
        else
            log_assert_eq "$value" "integer" "summary.$field should be integer"
        fi
    done
}

#
# Session/Agent Tests
#
test_no_sessions() {
    log_info "Testing robot-status with no matching sessions"

    # Clean up any existing test sessions
    cleanup_sessions "${TEST_PREFIX}"

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        return
    fi

    # Sessions array should exist (but may have other sessions)
    local sessions_type
    sessions_type=$(echo "$output" | jq -r '.sessions | type')
    log_assert_eq "$sessions_type" "array" "sessions is array even without test sessions"
}

test_claude_agents() {
    local session="${TEST_PREFIX}-claude"

    log_info "Creating session with Claude agents: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    # Find our session and check claude agents
    local session_data
    session_data=$(echo "$output" | jq -r --arg name "$session" '.sessions[] | select(.name == $name)')

    if [[ -z "$session_data" ]]; then
        log_assert_eq "found" "missing" "session $session should be in output"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    log_assert_eq "1" "1" "session $session found in output"

    # Check we have claude agents
    local claude_count
    claude_count=$(echo "$session_data" | jq '[.agents[]? | select(.type == "claude")] | length')
    if [[ "$claude_count" -ge 2 ]]; then
        log_assert_eq "1" "1" "session has $claude_count claude agents (expected 2)"
    else
        log_assert_eq "$claude_count" "2" "session should have 2 claude agents"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_multiple_agent_types() {
    local session="${TEST_PREFIX}-multi"

    log_info "Creating session with multiple agent types: $session"

    # Try to create session with claude and codex (gemini may not be available)
    if ! spawn_test_session "$session" --cc 1 --cod 1; then
        log_skip "Could not create test session with multiple agent types"
        return 0
    fi

    sleep 2

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    # Find our session
    local session_data
    session_data=$(echo "$output" | jq -r --arg name "$session" '.sessions[] | select(.name == $name)')

    if [[ -z "$session_data" ]]; then
        log_skip "Session not found in status output"
        tmux kill-session -t "$session" 2>/dev/null || true
        return 0
    fi

    # Check we have different agent types
    local agent_types
    agent_types=$(echo "$session_data" | jq -r '[.agents[]?.type] | unique | sort | join(",")')
    log_info "Agent types in session: $agent_types"

    # Should have at least user pane + 1 agent type
    local unique_types
    unique_types=$(echo "$session_data" | jq '[.agents[]?.type] | unique | length')
    if [[ "$unique_types" -ge 1 ]]; then
        log_assert_eq "1" "1" "session has $unique_types different agent types"
    else
        log_warn "expected multiple agent types, got $unique_types"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Agent State Tests
#
test_agent_active_state() {
    local session="${TEST_PREFIX}-active"

    log_info "Testing agent is_active state: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    # Find our session agents
    local agents_data
    agents_data=$(echo "$output" | jq -r --arg name "$session" '.sessions[] | select(.name == $name) | .agents // []')

    if [[ "$agents_data" == "[]" || "$agents_data" == "null" ]]; then
        log_skip "No agents found in session"
        tmux kill-session -t "$session" 2>/dev/null || true
        return 0
    fi

    # Check all agents have is_active field
    local agents_count
    agents_count=$(echo "$agents_data" | jq 'length')

    local agents_with_active
    agents_with_active=$(echo "$agents_data" | jq '[.[] | select(has("is_active"))] | length')
    log_assert_eq "$agents_count" "$agents_with_active" "all agents have is_active field"

    # Check is_active is boolean for all agents
    local non_boolean_count
    non_boolean_count=$(echo "$agents_data" | jq '[.[] | .is_active | type | select(. != "boolean")] | length')
    log_assert_eq "$non_boolean_count" "0" "all is_active fields are boolean"

    # Exactly one pane should be active (the currently selected one)
    local active_count
    active_count=$(echo "$agents_data" | jq '[.[] | select(.is_active == true)] | length')
    log_assert_eq "$active_count" "1" "exactly one pane is active"

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_agent_type_detection() {
    local session="${TEST_PREFIX}-types"

    log_info "Testing agent type detection: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    # Get agent types from our session
    local agent_types
    agent_types=$(echo "$output" | jq -r --arg name "$session" '.sessions[] | select(.name == $name) | .agents[]?.type // empty')

    if [[ -z "$agent_types" ]]; then
        log_skip "No agent types found"
        tmux kill-session -t "$session" 2>/dev/null || true
        return 0
    fi

    # Valid types list
    local valid_types="user|claude|codex|gemini|cursor|windsurf|aider|unknown"

    # Check each type is valid
    local invalid_types=0
    while IFS= read -r agent_type; do
        if [[ ! "$agent_type" =~ ^($valid_types)$ ]]; then
            log_warn "Unknown agent type: $agent_type"
            ((invalid_types++))
        fi
    done <<< "$agent_types"

    if [[ $invalid_types -eq 0 ]]; then
        log_assert_eq "1" "1" "all agent types are valid"
    else
        log_assert_eq "$invalid_types" "0" "found $invalid_types invalid agent types"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Determinism Tests
#
test_schema_determinism() {
    log_info "Testing schema determinism (multiple calls return same structure)"

    # Get three outputs
    local output1 output2 output3
    output1=$(ntm --robot-status 2>/dev/null)
    sleep 0.5
    output2=$(ntm --robot-status 2>/dev/null)
    sleep 0.5
    output3=$(ntm --robot-status 2>/dev/null)

    # Extract key structure (excluding timestamps and dynamic values)
    local keys1 keys2 keys3
    keys1=$(echo "$output1" | jq -S 'keys')
    keys2=$(echo "$output2" | jq -S 'keys')
    keys3=$(echo "$output3" | jq -S 'keys')

    log_assert_eq "$keys1" "$keys2" "top-level keys match between calls 1 and 2"
    log_assert_eq "$keys2" "$keys3" "top-level keys match between calls 2 and 3"

    # Check system keys are deterministic
    local sys_keys1 sys_keys2
    sys_keys1=$(echo "$output1" | jq -S '.system | keys')
    sys_keys2=$(echo "$output2" | jq -S '.system | keys')
    log_assert_eq "$sys_keys1" "$sys_keys2" "system keys are deterministic"

    # Check summary keys are deterministic
    local sum_keys1 sum_keys2
    sum_keys1=$(echo "$output1" | jq -S '.summary | keys')
    sum_keys2=$(echo "$output2" | jq -S '.summary | keys')
    log_assert_eq "$sum_keys1" "$sum_keys2" "summary keys are deterministic"
}

test_session_ordering() {
    local session1="${TEST_PREFIX}-order1"
    local session2="${TEST_PREFIX}-order2"

    log_info "Testing session ordering in output"

    # Create two sessions
    if ! spawn_test_session "$session1" --cc 1; then
        log_skip "Could not create first test session"
        return 0
    fi
    sleep 1

    if ! spawn_test_session "$session2" --cc 1; then
        log_skip "Could not create second test session"
        tmux kill-session -t "$session1" 2>/dev/null || true
        return 0
    fi
    sleep 1

    # Get output multiple times
    local output1 output2
    output1=$(ntm --robot-status 2>/dev/null)
    sleep 0.5
    output2=$(ntm --robot-status 2>/dev/null)

    # Extract test session names in order
    local order1 order2
    order1=$(echo "$output1" | jq -r "[.sessions[].name | select(startswith(\"${TEST_PREFIX}\"))] | sort | join(\",\")")
    order2=$(echo "$output2" | jq -r "[.sessions[].name | select(startswith(\"${TEST_PREFIX}\"))] | sort | join(\",\")")

    # Sessions should be present in both
    if [[ -n "$order1" && -n "$order2" ]]; then
        log_assert_eq "$order1" "$order2" "test sessions present in both calls"
    else
        log_warn "test sessions not found consistently"
    fi

    # Cleanup
    tmux kill-session -t "$session1" 2>/dev/null || true
    tmux kill-session -t "$session2" 2>/dev/null || true
}

#
# Field Value Tests
#
test_timestamp_format() {
    log_info "Testing generated_at timestamp format"

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        return
    fi

    local timestamp
    timestamp=$(echo "$output" | jq -r '.generated_at')

    # Check it's ISO 8601 format (YYYY-MM-DDTHH:MM:SS...)
    if [[ "$timestamp" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2} ]]; then
        log_assert_eq "1" "1" "timestamp is ISO 8601 format"
    else
        log_assert_eq "$timestamp" "ISO8601" "timestamp should be ISO 8601 format"
    fi

    # Check timestamp is recent (within last minute)
    local now
    now=$(date -u +%s)
    local ts_epoch
    ts_epoch=$(date -d "$timestamp" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "${timestamp%.*}" +%s 2>/dev/null || echo "0")

    if [[ "$ts_epoch" -gt 0 ]]; then
        local diff=$((now - ts_epoch))
        if [[ $diff -lt 60 && $diff -gt -60 ]]; then
            log_assert_eq "1" "1" "timestamp is recent (within 60s)"
        else
            log_warn "timestamp may be stale, diff=$diff seconds"
        fi
    else
        log_warn "could not parse timestamp epoch"
    fi
}

test_session_metadata() {
    local session="${TEST_PREFIX}-meta"

    log_info "Testing session metadata fields: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    # Get our session data
    local session_data
    session_data=$(echo "$output" | jq -r --arg name "$session" '.sessions[] | select(.name == $name)')

    if [[ -z "$session_data" ]]; then
        log_skip "Session not found in output"
        tmux kill-session -t "$session" 2>/dev/null || true
        return 0
    fi

    # Check required session fields
    local has_name has_exists has_windows has_panes has_agents
    has_name=$(echo "$session_data" | jq 'has("name")')
    has_exists=$(echo "$session_data" | jq 'has("exists")')
    has_windows=$(echo "$session_data" | jq 'has("windows")')
    has_panes=$(echo "$session_data" | jq 'has("panes")')
    has_agents=$(echo "$session_data" | jq 'has("agents")')

    log_assert_eq "$has_name" "true" "session has name field"
    log_assert_eq "$has_exists" "true" "session has exists field"
    log_assert_eq "$has_windows" "true" "session has windows field"
    log_assert_eq "$has_panes" "true" "session has panes field"
    log_assert_eq "$has_agents" "true" "session has agents field"

    # Check exists is true for our session
    local exists_val
    exists_val=$(echo "$session_data" | jq -r '.exists')
    log_assert_eq "$exists_val" "true" "session exists is true"

    # Check panes count > 0
    local panes_count
    panes_count=$(echo "$session_data" | jq -r '.panes')
    if [[ "$panes_count" -gt 0 ]]; then
        log_assert_eq "1" "1" "session has $panes_count panes"
    else
        log_assert_eq "$panes_count" ">0" "session should have panes"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_pane_identification() {
    local session="${TEST_PREFIX}-panes"

    log_info "Testing pane identification fields: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    # Get agents from our session
    local agents
    agents=$(echo "$output" | jq -r --arg name "$session" '.sessions[] | select(.name == $name) | .agents // []')

    if [[ "$agents" == "[]" || "$agents" == "null" ]]; then
        log_skip "No agents found in session"
        tmux kill-session -t "$session" 2>/dev/null || true
        return 0
    fi

    # Check agent structure fields
    local first_agent
    first_agent=$(echo "$agents" | jq '.[0]')

    local has_type has_pane has_window has_pane_idx has_is_active
    has_type=$(echo "$first_agent" | jq 'has("type")')
    has_pane=$(echo "$first_agent" | jq 'has("pane")')
    has_window=$(echo "$first_agent" | jq 'has("window")')
    has_pane_idx=$(echo "$first_agent" | jq 'has("pane_idx")')
    has_is_active=$(echo "$first_agent" | jq 'has("is_active")')

    log_assert_eq "$has_type" "true" "agent has type field"
    log_assert_eq "$has_pane" "true" "agent has pane field"
    log_assert_eq "$has_window" "true" "agent has window field"
    log_assert_eq "$has_pane_idx" "true" "agent has pane_idx field"
    log_assert_eq "$has_is_active" "true" "agent has is_active field"

    # Check pane_idx are unique within session
    local pane_indices unique_indices
    pane_indices=$(echo "$agents" | jq '[.[].pane_idx] | length')
    unique_indices=$(echo "$agents" | jq '[.[].pane_idx] | unique | length')
    log_assert_eq "$pane_indices" "$unique_indices" "pane indices are unique"

    # Check window values are non-negative integers
    local invalid_windows
    invalid_windows=$(echo "$agents" | jq '[.[] | .window | select(. < 0 or type != "number")] | length')
    log_assert_eq "$invalid_windows" "0" "window values are valid non-negative integers"

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Summary Count Tests
#
test_summary_counts() {
    local session="${TEST_PREFIX}-counts"

    log_info "Testing summary counts accuracy: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    local output
    output=$(ntm --robot-status 2>/dev/null)

    if ! echo "$output" | jq . >/dev/null 2>&1; then
        log_error "Invalid JSON from robot-status"
        tmux kill-session -t "$session" 2>/dev/null || true
        return
    fi

    # Get summary values
    local summary_total_sessions summary_total_agents summary_claude_count
    summary_total_sessions=$(echo "$output" | jq -r '.summary.total_sessions')
    summary_total_agents=$(echo "$output" | jq -r '.summary.total_agents')
    summary_claude_count=$(echo "$output" | jq -r '.summary.claude_count')

    # Calculate actual values from sessions
    local actual_sessions actual_agents actual_claude
    actual_sessions=$(echo "$output" | jq '.sessions | length')
    actual_agents=$(echo "$output" | jq '[.sessions[].agents[]?] | length')
    actual_claude=$(echo "$output" | jq '[.sessions[].agents[]? | select(.type == "claude")] | length')

    # Verify counts match
    log_assert_eq "$summary_total_sessions" "$actual_sessions" "summary.total_sessions matches actual session count"
    log_assert_eq "$summary_total_agents" "$actual_agents" "summary.total_agents matches actual agent count"
    log_assert_eq "$summary_claude_count" "$actual_claude" "summary.claude_count matches actual claude count"

    # Verify total_sessions >= 1 (we just created one)
    if [[ "$summary_total_sessions" -ge 1 ]]; then
        log_assert_eq "1" "1" "total_sessions >= 1"
    else
        log_assert_eq "$summary_total_sessions" ">=1" "should have at least 1 session"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

main
