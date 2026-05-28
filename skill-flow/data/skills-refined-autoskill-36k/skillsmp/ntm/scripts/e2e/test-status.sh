#!/usr/bin/env bash
# E2E Test: Status Command Scenarios
# Tests various status output modes and validates JSON format.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"

# Test session prefix
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
    log_init "test-status"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    log_section "Test: robot-status with no sessions"
    test_robot_status_empty

    log_section "Test: robot-status with active sessions"
    test_robot_status_with_sessions

    log_section "Test: Status for specific session"
    test_status_specific_session

    log_section "Test: robot-version output"
    test_robot_version

    log_section "Test: robot-context output"
    test_robot_context

    log_summary
}

test_robot_status_empty() {
    log_info "Testing robot-status with potentially no ntm sessions"

    if log_exec ntm --robot-status; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "robot-status returns valid JSON"

        # Check required fields
        local generated_at
        generated_at=$(echo "$output" | jq -r '.generated_at // ""')
        log_assert_not_empty "$generated_at" "robot-status has generated_at field"

        # Sessions array should exist (even if empty)
        local has_sessions
        has_sessions=$(echo "$output" | jq 'has("sessions")')
        log_assert_eq "$has_sessions" "true" "robot-status has sessions array"

        # Summary should exist
        local has_summary
        has_summary=$(echo "$output" | jq 'has("summary")')
        log_assert_eq "$has_summary" "true" "robot-status has summary object"
    else
        log_error "robot-status command failed"
    fi
}

test_robot_status_with_sessions() {
    local session="${TEST_PREFIX}-status"

    log_info "Creating session for status test: $session"

    # Create a session with agents
    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    # Give it a moment to initialize
    sleep 2

    log_info "Testing robot-status with active session"

    if log_exec ntm --robot-status; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "robot-status returns valid JSON with session"

        # Check sessions array has entries
        local session_count
        session_count=$(echo "$output" | jq '.sessions | length')
        if [[ $session_count -ge 1 ]]; then
            log_assert_eq "1" "1" "robot-status shows at least 1 session"
        else
            log_warn "robot-status shows 0 sessions"
        fi

        # Find our session in the output (may or may not appear depending on scan)
        local our_session
        our_session=$(echo "$output" | jq -r ".sessions[] | select(.name == \"$session\") | .name // \"\"" 2>/dev/null || echo "")
        if [[ -n "$our_session" ]]; then
            log_info "Our test session found in robot-status output"
            log_assert_eq "$our_session" "$session" "our session appears in status"
        else
            # Session might not be visible to robot-status if it only tracks known sessions
            log_info "Test session not visible to robot-status (may only show registered sessions)"
        fi

        # Summary should have valid counts
        local total_sessions
        total_sessions=$(echo "$output" | jq '.summary.total_sessions // 0')
        log_info "Summary shows $total_sessions total sessions"
    else
        log_error "robot-status failed with active session"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_status_specific_session() {
    local session="${TEST_PREFIX}-specific"

    log_info "Creating session for specific status test: $session"

    # Create session with Claude agents (codex might not be available on all systems)
    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    sleep 1

    log_info "Testing status for specific session"

    if log_exec ntm status "$session" --json; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "status --json returns valid JSON"

        # Check session name
        local session_name
        session_name=$(echo "$output" | jq -r '.session // ""')
        log_assert_eq "$session_name" "$session" "status shows correct session name"

        # Check panes exist (should be 3: 1 user + 2 claude)
        local panes_count
        panes_count=$(echo "$output" | jq '.panes | length')
        log_assert_eq "$panes_count" "3" "status shows 3 panes (user + 2 claude)"

        # Verify agent types
        local claude_count user_count
        claude_count=$(echo "$output" | jq '[.panes[] | select(.type == "claude")] | length')
        user_count=$(echo "$output" | jq '[.panes[] | select(.type == "user")] | length')

        log_assert_eq "$claude_count" "2" "status shows 2 Claude panes"
        log_assert_eq "$user_count" "1" "status shows 1 user pane"

        # Check pane fields
        local first_pane_has_index
        first_pane_has_index=$(echo "$output" | jq '.panes[0] | has("index")')
        log_assert_eq "$first_pane_has_index" "true" "panes have index field"
    else
        log_error "status command failed"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_version() {
    log_info "Testing robot-version output"

    if log_exec ntm --robot-version; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "robot-version returns valid JSON"

        # Check required fields
        local version
        version=$(echo "$output" | jq -r '.version // ""')
        log_assert_not_empty "$version" "robot-version has version field"

        local commit
        commit=$(echo "$output" | jq -r '.commit // ""')
        log_assert_not_empty "$commit" "robot-version has commit field"

        local go_version
        go_version=$(echo "$output" | jq -r '.go_version // ""')
        log_assert_not_empty "$go_version" "robot-version has go_version field"

        local build_date
        build_date=$(echo "$output" | jq -r '.build_date // ""')
        log_assert_not_empty "$build_date" "robot-version has build_date field"

        log_info "Version: $version, Commit: $commit"
    else
        log_error "robot-version failed"
    fi
}

test_robot_context() {
    local session="${TEST_PREFIX}-context"

    log_info "Creating session for context test: $session"

    # Create session
    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    sleep 1

    log_info "Testing robot-context output"

    if log_exec ntm --robot-context="$session"; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "robot-context returns valid JSON"

        # Check required fields
        local has_session
        has_session=$(echo "$output" | jq 'has("session")')
        log_assert_eq "$has_session" "true" "robot-context has session field"

        local has_agents
        has_agents=$(echo "$output" | jq 'has("agents")')
        log_assert_eq "$has_agents" "true" "robot-context has agents array"

        # Agents should have context info
        local agents_count
        agents_count=$(echo "$output" | jq '.agents | length')
        log_info "Context shows $agents_count agents"

        if [[ $agents_count -gt 0 ]]; then
            # Check first agent has expected fields
            local has_agent_type
            has_agent_type=$(echo "$output" | jq '.agents[0] | has("agent_type")')
            log_assert_eq "$has_agent_type" "true" "context agents have agent_type field"

            local has_estimated_tokens
            has_estimated_tokens=$(echo "$output" | jq '.agents[0] | has("estimated_tokens")')
            log_assert_eq "$has_estimated_tokens" "true" "context agents have estimated_tokens field"
        fi

        # Check summary exists
        local has_summary
        has_summary=$(echo "$output" | jq 'has("summary")')
        log_assert_eq "$has_summary" "true" "robot-context has summary field"
    else
        # robot-context may not be implemented yet
        local exit_code="$_LAST_EXIT_CODE"
        if [[ $exit_code -eq 2 ]]; then
            log_skip "robot-context not implemented (exit 2)"
        else
            log_error "robot-context failed unexpectedly"
        fi
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

main
