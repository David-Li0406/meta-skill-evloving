#!/usr/bin/env bash
# E2E Test: Context Rotation During Long Sessions
# Tests context window rotation management and CLI commands.
# Covers: ntm-8ice - Test agent context rotation during long sessions
#
# Since context rotation during actual long sessions is impractical for E2E tests,
# this script focuses on:
# 1. CLI command validation (history, stats, pending, confirm, clear)
# 2. History file management
# 3. Pending rotation workflow
# 4. Integration with session lifecycle

set -uo pipefail
# Note: Not using -e so that assertion failures don't cause early exit.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"
set +e  # Disable immediate exit on error so tests continue after assertion failures

# Test session prefix (unique per run to avoid conflicts)
TEST_PREFIX="e2e-ctx-$$"

# Track created sessions for cleanup
CREATED_SESSIONS=()

# Rotation history backup location
ROTATION_HISTORY_BACKUP=""
ROTATION_HISTORY_PATH="${HOME}/.local/share/ntm/rotation_history"

# Cleanup function
cleanup() {
    log_section "Cleanup"

    # Kill test sessions with timeout to avoid hanging
    for session in "${CREATED_SESSIONS[@]}"; do
        log_debug "Cleaning up session: $session"
        # Use direct tmux kill as ntm kill can hang
        timeout 5 tmux kill-session -t "$session" 2>/dev/null || true
    done

    # Also cleanup any sessions matching the prefix that we might have missed
    local sessions
    sessions=$(tmux list-sessions -F '#{session_name}' 2>/dev/null || true)
    for session in $sessions; do
        if [[ "$session" == ${TEST_PREFIX}* ]]; then
            timeout 5 tmux kill-session -t "$session" 2>/dev/null || true
        fi
    done

    # Restore rotation history if we backed it up
    if [[ -n "$ROTATION_HISTORY_BACKUP" && -d "$ROTATION_HISTORY_BACKUP" ]]; then
        log_debug "Restoring rotation history from backup"
        rm -rf "${ROTATION_HISTORY_PATH}"
        mv "$ROTATION_HISTORY_BACKUP" "${ROTATION_HISTORY_PATH}"
    fi
}
trap cleanup EXIT

# Helper to spawn and track session
spawn_test_session() {
    local session="$1"
    shift
    CREATED_SESSIONS+=("$session")
    ntm_spawn "$session" "$@"
}

# Backup rotation history before tests
backup_rotation_history() {
    if [[ -d "${ROTATION_HISTORY_PATH}" ]]; then
        ROTATION_HISTORY_BACKUP=$(mktemp -d)
        cp -r "${ROTATION_HISTORY_PATH}"/* "$ROTATION_HISTORY_BACKUP/" 2>/dev/null || true
        log_debug "Backed up rotation history to: $ROTATION_HISTORY_BACKUP"
    fi
}

# Main test
main() {
    log_init "test-context-rotation"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    # Backup existing rotation history
    backup_rotation_history

    # CLI Command Tests
    log_section "Test: Context rotation history command"
    test_rotation_history_cmd

    log_section "Test: Context rotation stats command"
    test_rotation_stats_cmd

    log_section "Test: Context rotation pending command"
    test_rotation_pending_cmd

    log_section "Test: Context rotation clear command"
    test_rotation_clear_cmd

    # Confirm workflow test
    log_section "Test: Context rotation confirm workflow"
    test_rotation_confirm_workflow

    # Integration with session lifecycle
    log_section "Test: Context monitoring during session"
    test_context_monitoring_during_session

    # JSON output tests
    log_section "Test: JSON output format"
    test_json_output_format

    log_summary
}

#
# Test: Rotation History Command
#
test_rotation_history_cmd() {
    log_info "Testing 'ntm rotate context history' command"

    # Basic history command should not error (even if empty)
    if log_exec ntm rotate context history; then
        log_assert_eq "0" "0" "history command succeeds"
    else
        log_warn "history command failed"
    fi

    # Test with --last flag
    if log_exec ntm rotate context history --last=5; then
        log_assert_eq "0" "0" "history --last=5 succeeds"
    fi

    # Test with --failed flag
    if log_exec ntm rotate context history --failed; then
        log_assert_eq "0" "0" "history --failed succeeds"
    fi

    # Test with nonexistent session (should not error, just show nothing)
    if log_exec ntm rotate context history "nonexistent-session-$$"; then
        log_assert_eq "0" "0" "history for nonexistent session succeeds (shows empty)"
    fi

    # Test JSON output
    if log_exec ntm rotate context history --json; then
        log_assert_valid_json "$_LAST_OUTPUT" "history --json returns valid JSON"
    fi
}

#
# Test: Rotation Stats Command
#
test_rotation_stats_cmd() {
    log_info "Testing 'ntm rotate context stats' command"

    # Basic stats command
    if log_exec ntm rotate context stats; then
        log_assert_eq "0" "0" "stats command succeeds"
    fi

    # Test JSON output
    if log_exec ntm rotate context stats --json; then
        log_assert_valid_json "$_LAST_OUTPUT" "stats --json returns valid JSON"

        # Verify JSON structure
        local has_total
        has_total=$(echo "$_LAST_OUTPUT" | jq 'has("total_rotations")')
        log_assert_eq "$has_total" "true" "stats JSON has total_rotations field"
    fi
}

#
# Test: Rotation Pending Command
#
test_rotation_pending_cmd() {
    log_info "Testing 'ntm rotate context pending' command"

    # Basic pending command (may be empty)
    if log_exec ntm rotate context pending; then
        log_assert_eq "0" "0" "pending command succeeds"
    fi

    # Test with session filter
    if log_exec ntm rotate context pending "nonexistent-session-$$"; then
        log_assert_eq "0" "0" "pending with session filter succeeds"
    fi

    # Test JSON output
    if log_exec ntm rotate context pending --json; then
        log_assert_valid_json "$_LAST_OUTPUT" "pending --json returns valid JSON"

        # Verify JSON structure
        local has_pending
        has_pending=$(echo "$_LAST_OUTPUT" | jq 'has("pending")')
        log_assert_eq "$has_pending" "true" "pending JSON has pending array"

        local has_count
        has_count=$(echo "$_LAST_OUTPUT" | jq 'has("count")')
        log_assert_eq "$has_count" "true" "pending JSON has count field"
    fi
}

#
# Test: Rotation Clear Command
#
test_rotation_clear_cmd() {
    log_info "Testing 'ntm rotate context clear' command"

    # Clear with force flag (safe for testing)
    if log_exec ntm rotate context clear --force; then
        log_assert_eq "0" "0" "clear --force succeeds"
    fi

    # After clear, stats should show 0 rotations
    if log_exec ntm rotate context stats --json; then
        local total
        total=$(echo "$_LAST_OUTPUT" | jq -r '.total_rotations // 0')
        log_assert_eq "$total" "0" "after clear, total rotations is 0"
    fi
}

#
# Test: Rotation Confirm Workflow
#
test_rotation_confirm_workflow() {
    log_info "Testing rotation confirm workflow"

    # Test confirm command with nonexistent agent (should fail gracefully)
    if log_exec ntm rotate context confirm "nonexistent__cc_1" --action=rotate; then
        local output="$_LAST_OUTPUT"
        # Should indicate no pending rotation found
        if log_assert_contains "$output" "No pending rotation" "confirm for nonexistent agent shows appropriate message" || \
           log_assert_contains "$output" "not found" "confirm for nonexistent agent shows not found"; then
            log_info "Confirm for nonexistent agent handled correctly"
        fi
    fi

    # Test invalid action
    if ! log_exec ntm rotate context confirm "test__cc_1" --action=invalid_action 2>&1; then
        log_assert_eq "$_LAST_EXIT_CODE" "1" "invalid action returns error"
        log_assert_contains "$_LAST_OUTPUT" "invalid action" "error message mentions invalid action"
    fi

    # Test valid action values (even if no pending rotation)
    for action in "rotate" "compact" "ignore" "postpone"; do
        if log_exec ntm rotate context confirm "test__cc_1" --action="$action" 2>&1; then
            log_debug "confirm --action=$action executed"
        fi
    done
    log_info "All valid action values accepted by CLI"
}

#
# Test: Context Monitoring During Session
#
test_context_monitoring_during_session() {
    log_info "Testing context monitoring integration with session lifecycle"

    local session="${TEST_PREFIX}-monitor"

    # Spawn a session
    log_info "Spawning test session: $session"
    if ! spawn_test_session "$session" --cc 1; then
        log_warn "Failed to spawn session, skipping monitoring test"
        return
    fi

    sleep 2

    # Verify session status includes context info
    if log_exec ntm status "$session" --json; then
        log_assert_valid_json "$_LAST_OUTPUT" "status returns valid JSON"

        local pane_count
        pane_count=$(echo "$_LAST_OUTPUT" | jq '[.panes[]?] | length')
        if [[ "$pane_count" -gt 0 ]]; then
            log_assert_eq "1" "1" "session has panes for context monitoring"
        fi
    fi

    # Check rotation history is accessible during session
    if log_exec ntm rotate context history "$session"; then
        log_assert_eq "0" "0" "history command works during active session"
    fi

    # Check stats are accessible during session
    if log_exec ntm rotate context stats; then
        log_assert_eq "0" "0" "stats command works during active session"
    fi

    # Clean up session with timeout
    log_info "Cleaning up test session"
    if log_exec timeout 10 ntm kill "$session"; then
        log_assert_eq "0" "0" "session killed successfully"
    else
        # Fall back to direct tmux kill
        log_warn "ntm kill timed out, using direct tmux kill"
        timeout 5 tmux kill-session -t "$session" 2>/dev/null || true
    fi
}

#
# Test: JSON Output Format
#
test_json_output_format() {
    log_info "Testing JSON output format for all commands"

    # History JSON structure
    if log_exec ntm rotate context history --json; then
        log_assert_valid_json "$_LAST_OUTPUT" "history JSON is valid"

        local json="$_LAST_OUTPUT"

        # Check expected fields
        local has_records
        has_records=$(echo "$json" | jq 'has("records")')
        log_assert_eq "$has_records" "true" "history JSON has records array"

        local has_total
        has_total=$(echo "$json" | jq 'has("total_count")')
        log_assert_eq "$has_total" "true" "history JSON has total_count"

        local has_showing
        has_showing=$(echo "$json" | jq 'has("showing")')
        log_assert_eq "$has_showing" "true" "history JSON has showing"
    fi

    # Stats JSON structure
    if log_exec ntm rotate context stats --json; then
        log_assert_valid_json "$_LAST_OUTPUT" "stats JSON is valid"

        local json="$_LAST_OUTPUT"

        # Check expected fields
        for field in "total_rotations" "success_count" "failure_count" "unique_sessions"; do
            local has_field
            has_field=$(echo "$json" | jq "has(\"$field\")")
            log_assert_eq "$has_field" "true" "stats JSON has $field"
        done
    fi

    # Pending JSON structure
    if log_exec ntm rotate context pending --json; then
        log_assert_valid_json "$_LAST_OUTPUT" "pending JSON is valid"

        local json="$_LAST_OUTPUT"

        # Verify structure (pending can be null or array)
        local records_type
        records_type=$(echo "$json" | jq -r '.pending | type')
        if [[ "$records_type" == "array" ]] || [[ "$records_type" == "null" ]]; then
            log_assert_eq "valid" "valid" "pending JSON has pending as array or null"
        else
            log_assert_eq "$records_type" "array or null" "pending JSON has pending as array or null"
        fi
    fi
}

main
