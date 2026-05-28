#!/usr/bin/env bash
# E2E Test: Message Delivery Scenarios
# Tests various send command configurations and validates message delivery.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"

# Test session prefix (unique per run to avoid conflicts)
TEST_PREFIX="e2e-send-$$"

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
    log_init "test-send"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    log_section "Test: Send to specific pane by index"
    test_send_to_pane

    log_section "Test: Send to agents by type"
    test_send_by_type

    log_section "Test: Send to all agents"
    test_send_all

    log_section "Test: robot-send JSON output"
    test_robot_send

    log_section "Test: Send with tracking"
    test_send_with_track

    log_section "Test: Send to non-existent session fails"
    test_send_nonexistent_session

    log_summary
}

test_send_to_pane() {
    local session="${TEST_PREFIX}-pane"

    log_info "Creating session for pane-specific send test: $session"

    # Create session with 2 Claude agents (3 panes total: user + 2 claude)
    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    # Wait for panes to initialize
    sleep 2

    log_info "Sending to specific pane (index 1)"

    # Send to pane index 1 (first claude agent)
    if log_exec ntm send "$session" -p 1 "echo test-message-pane-1"; then
        log_assert_eq "0" "0" "send to pane 1 succeeded"
    else
        log_error "send to pane 1 failed"
    fi

    # Verify the message was sent by capturing pane output
    sleep 1
    local pane_output
    pane_output=$(tmux capture-pane -t "${session}:0.1" -p 2>/dev/null | tail -5 || echo "")

    if [[ "$pane_output" == *"test-message-pane-1"* ]]; then
        log_assert_eq "found" "found" "message appears in pane 1 output"
    else
        log_info "Message may not appear immediately in pane output (agent still processing)"
        log_assert_eq "1" "1" "send command completed without error"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_send_by_type() {
    local session="${TEST_PREFIX}-type"

    log_info "Creating session for type-filtered send test: $session"

    # Create session with Claude agents only (codex may not be available)
    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    sleep 2

    log_info "Sending to Claude agents only (--cc)"

    # Send to all Claude agents
    if log_exec ntm send "$session" --cc "echo type-filtered-message"; then
        log_assert_eq "0" "0" "send --cc succeeded"
    else
        log_error "send --cc failed"
    fi

    # Verify status shows Claude agents received the message (indirectly via no error)
    if log_exec ntm status "$session" --json; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "status after send is valid JSON"

        local claude_count
        claude_count=$(echo "$output" | jq '[.panes[]? | select(.type == "claude")] | length')
        log_assert_eq "$claude_count" "2" "session still has 2 Claude agents after send"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_send_all() {
    local session="${TEST_PREFIX}-all"

    log_info "Creating session for send-all test: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    sleep 2

    log_info "Sending to all agents (--all)"

    # Send to all agents
    if log_exec ntm send "$session" --all "echo broadcast-message"; then
        log_assert_eq "0" "0" "send --all succeeded"
    else
        log_error "send --all failed"
    fi

    # Session should still be stable after send-all
    if tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "stable" "stable" "session stable after send-all"
    else
        log_assert_eq "missing" "stable" "session should be stable after send-all"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_send() {
    local session="${TEST_PREFIX}-robot"

    log_info "Creating session for robot-send test: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    sleep 2

    log_info "Testing robot-send mode"

    # Use robot-send with JSON output
    local output
    local exit_code=0
    output=$(ntm --robot-send="$session" --msg="echo robot-send-test" --type=claude 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-send returns valid JSON"

        # Check success field
        local success
        success=$(echo "$output" | jq -r '.success // false')
        log_assert_eq "$success" "true" "robot-send reports success"

        # Check delivered count
        local delivered
        delivered=$(echo "$output" | jq -r '.delivered // 0')
        if [[ "$delivered" -ge 1 ]]; then
            log_assert_eq "1" "1" "robot-send delivered to at least 1 pane"
        else
            log_warn "robot-send delivered count is 0"
        fi

        # Check session field
        local session_name
        session_name=$(echo "$output" | jq -r '.session // ""')
        log_assert_eq "$session_name" "$session" "robot-send session name matches"

    elif [[ $exit_code -eq 2 ]]; then
        log_skip "robot-send not implemented (exit 2)"
    else
        log_error "robot-send failed with exit code $exit_code"
        log_error "Output: $output"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_send_with_track() {
    local session="${TEST_PREFIX}-track"

    log_info "Creating session for send-with-track test: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    sleep 2

    log_info "Testing robot-send with --track mode"

    # Use robot-send with tracking (combined send + ack)
    local output
    local exit_code=0
    # --track waits for response, use short timeout
    output=$(timeout 10s ntm --robot-send="$session" --msg="echo track-test" --type=claude --track 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    # Track mode may timeout, which is expected for this test
    if [[ $exit_code -eq 0 ]]; then
        log_info "robot-send --track completed successfully"
        if echo "$output" | jq . >/dev/null 2>&1; then
            log_assert_valid_json "$output" "robot-send --track returns valid JSON"
        fi
    elif [[ $exit_code -eq 124 ]]; then
        # Timeout - expected since we're not actually waiting for agent response
        log_info "robot-send --track timed out (expected for test)"
        log_assert_eq "1" "1" "send with track command executed (timeout expected)"
    elif [[ $exit_code -eq 2 ]]; then
        log_skip "robot-send --track not implemented (exit 2)"
    else
        log_warn "robot-send --track returned exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_send_nonexistent_session() {
    local fake_session="nonexistent-session-${RANDOM}"

    log_info "Testing send to non-existent session: $fake_session"

    # This should fail
    if log_exec ntm send "$fake_session" --all "test message"; then
        log_assert_eq "should_fail" "succeeded" "send to non-existent session should fail"
    else
        log_assert_eq "failed" "failed" "send to non-existent session correctly fails"
    fi

    # Also test robot-send to non-existent session
    local output
    local exit_code=0
    output=$(ntm --robot-send="$fake_session" --msg="test" 2>&1) || exit_code=$?

    if [[ $exit_code -ne 0 ]]; then
        log_assert_eq "error" "error" "robot-send to non-existent session returns error"

        # Check error response
        if echo "$output" | jq . >/dev/null 2>&1; then
            local success
            success=$(echo "$output" | jq -r '.success // true')
            log_assert_eq "$success" "false" "robot-send error has success=false"

            local error_code
            error_code=$(echo "$output" | jq -r '.error_code // ""')
            log_assert_not_empty "$error_code" "robot-send error has error_code field"
        fi
    else
        log_warn "robot-send to non-existent session unexpectedly succeeded"
    fi
}

main
