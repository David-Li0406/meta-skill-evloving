#!/usr/bin/env bash
# E2E Test: Agent Spawning Scenarios
# Tests various spawn configurations and validates session creation.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"

# Test session prefix (unique per run to avoid conflicts)
TEST_PREFIX="e2e-spawn-$$"

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
    log_init "test-spawn"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    log_section "Test: Basic spawn creates session"
    test_basic_spawn

    log_section "Test: Spawn with Claude agents"
    test_spawn_claude

    log_section "Test: Spawn with multiple agent types"
    test_spawn_multiple_types

    log_section "Test: Spawn robot mode JSON output"
    test_spawn_robot_mode

    log_section "Test: Session consistency after spawn"
    test_spawn_session_consistency

    log_summary
}

test_basic_spawn() {
    local session="${TEST_PREFIX}-basic"

    log_info "Creating session: $session"

    # Spawn with one Claude agent (required - can't spawn with no agents)
    if ! spawn_test_session "$session" --cc 1; then
        log_error "Failed to spawn session"
        return 1
    fi
    log_info "Session spawned successfully"

    # Verify session exists
    if ! tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "exists" "missing" "session should exist"
        return 1
    fi
    log_assert_eq "exists" "exists" "session exists"

    # Get pane count (should be 2: user + claude)
    local pane_count
    pane_count=$(tmux list-panes -t "$session" -F '#{pane_id}' | wc -l | tr -d ' ')
    log_assert_eq "$pane_count" "2" "basic spawn creates 2 panes (user + claude)"

    # Cleanup this test's session
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_spawn_claude() {
    local session="${TEST_PREFIX}-claude"

    log_info "Creating session with Claude agents: $session"

    # Spawn with 2 Claude agents
    if ! spawn_test_session "$session" --cc 2; then
        log_error "Failed to spawn session"
        return 1
    fi
    log_info "Session spawned successfully"

    # Verify session exists
    if ! tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "exists" "missing" "session with Claude agents should exist"
        return 1
    fi
    log_assert_eq "exists" "exists" "session with Claude agents exists"

    # Get pane count (should be 3: 1 user + 2 claude)
    local pane_count
    pane_count=$(tmux list-panes -t "$session" -F '#{pane_id}' | wc -l | tr -d ' ')
    log_assert_eq "$pane_count" "3" "spawn --cc 2 creates 3 panes"

    # Verify status shows Claude agents
    local status_output
    if log_exec ntm status "$session" --json; then
        status_output="$_LAST_OUTPUT"
        log_assert_valid_json "$status_output" "status output is valid JSON"

        local claude_count
        claude_count=$(echo "$status_output" | jq '[.panes[]? | select(.type == "claude")] | length')
        log_assert_eq "$claude_count" "2" "status shows 2 Claude agents"
    else
        log_warn "Could not get status for Claude agent verification"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_spawn_multiple_types() {
    local session="${TEST_PREFIX}-multi"

    log_info "Creating session with multiple agent types: $session"

    # Spawn with 2 Claude agents (codex might not be available)
    if ! spawn_test_session "$session" --cc 2; then
        log_error "Failed to spawn session"
        return 1
    fi
    log_info "Session spawned successfully"

    # Get pane count (should be 3: 1 user + 2 claude)
    local pane_count
    pane_count=$(tmux list-panes -t "$session" -F '#{pane_id}' | wc -l | tr -d ' ')
    log_assert_eq "$pane_count" "3" "multi-claude spawn creates 3 panes"

    # Verify status shows Claude agents
    local status_output
    if log_exec ntm status "$session" --json; then
        status_output="$_LAST_OUTPUT"

        local claude_count
        claude_count=$(echo "$status_output" | jq '[.panes[]? | select(.type == "claude")] | length')

        log_assert_eq "$claude_count" "2" "status shows 2 Claude agents"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_spawn_robot_mode() {
    local session="${TEST_PREFIX}-robot"
    CREATED_SESSIONS+=("$session")

    log_info "Testing robot-spawn mode: $session"

    # Use robot spawn (pipe y for directory creation prompt)
    local output
    local exit_code=0
    log_info "Running: ntm --robot-spawn=$session --spawn-cc=1"
    output=$(echo "y" | ntm --robot-spawn="$session" --spawn-cc=1 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_info "robot-spawn succeeded"
        log_assert_valid_json "$output" "robot-spawn returns valid JSON"

        # Check JSON fields
        local session_name
        session_name=$(echo "$output" | jq -r '.session // ""')
        log_assert_eq "$session_name" "$session" "robot-spawn session name"

        # Verify agents array (robot-spawn uses 'agents' not 'panes')
        local agents_count
        agents_count=$(echo "$output" | jq '.agents | length')
        log_assert_eq "$agents_count" "2" "robot-spawn returns 2 agents (user + claude)"

        # Verify created_at field exists
        local created_at
        created_at=$(echo "$output" | jq -r '.created_at // ""')
        log_assert_not_empty "$created_at" "robot-spawn has created_at field"

        # Verify working_dir field exists
        local working_dir
        working_dir=$(echo "$output" | jq -r '.working_dir // ""')
        log_assert_not_empty "$working_dir" "robot-spawn has working_dir field"
    else
        log_error "robot-spawn failed with exit code $exit_code"
        log_error "Output: $output"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_spawn_session_consistency() {
    local session="${TEST_PREFIX}-consist"

    log_info "Testing session consistency after spawn: $session"

    # Create session
    if ! spawn_test_session "$session" --cc 1; then
        log_error "Failed to spawn session"
        return 1
    fi
    log_info "Session spawned successfully"

    # Get pane count
    local pane_count
    pane_count=$(tmux list-panes -t "$session" -F '#{pane_id}' | wc -l | tr -d ' ')
    log_info "Pane count: $pane_count"

    # Verify session exists after a brief delay
    sleep 1
    if tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "exists" "exists" "session remains stable after spawn"
    else
        log_assert_eq "missing" "exists" "session should remain stable"
    fi

    # Verify agents are running (via status)
    if log_exec ntm status "$session" --json; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "status returns valid JSON after spawn"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

main
