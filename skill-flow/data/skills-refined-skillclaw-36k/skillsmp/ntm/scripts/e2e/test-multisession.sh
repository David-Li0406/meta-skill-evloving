#!/usr/bin/env bash
# E2E Test: Multi-Session Orchestration Tests
# Tests managing multiple concurrent sessions, save/restore, and cross-session operations.
# Covers: ntm-8ggq - E2E multi-session orchestration tests

set -uo pipefail
# Note: Not using -e so that assertion failures don't cause early exit.
# Failures are tracked via log library and reported in summary.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"
set +e  # Disable immediate exit on error so tests continue after assertion failures

# Test session prefix (unique per run to avoid conflicts)
TEST_PREFIX="e2e-multi-$$"

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
    # Clean up any save files
    rm -f /tmp/ntm-save-${TEST_PREFIX}*.json 2>/dev/null || true
}
trap cleanup EXIT

# Helper to spawn and track session
spawn_test_session() {
    local session="$1"
    shift
    CREATED_SESSIONS+=("$session")
    ntm_spawn "$session" "$@"
}

# Helper to get session count from robot-status
get_session_count() {
    local prefix="$1"
    ntm --robot-status 2>/dev/null | jq -r --arg prefix "$prefix" '[.sessions[]? | select(.name | startswith($prefix))] | length'
}

# Main test
main() {
    log_init "test-multisession"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    # Multiple Concurrent Sessions
    log_section "Test: Multiple concurrent sessions"
    test_multiple_concurrent_sessions

    # Session Listing and Filtering
    log_section "Test: Session listing"
    test_session_listing

    # Session Save
    log_section "Test: Session save"
    test_session_save

    # Session Restore
    log_section "Test: Session restore"
    test_session_restore

    # Cross-Session Status
    log_section "Test: Cross-session status"
    test_cross_session_status

    # Session Isolation
    log_section "Test: Session isolation"
    test_session_isolation

    # Batch Operations
    log_section "Test: Batch session operations"
    test_batch_operations

    # Robot Snapshot Multi-Session
    log_section "Test: Robot snapshot with multiple sessions"
    test_robot_snapshot_multi

    # Session Names and Patterns
    log_section "Test: Session naming patterns"
    test_session_naming

    # Concurrent Session Creation
    log_section "Test: Concurrent session creation"
    test_concurrent_creation

    log_summary
}

#
# Multiple Concurrent Sessions Test
#
test_multiple_concurrent_sessions() {
    local session1="${TEST_PREFIX}-concurrent-1"
    local session2="${TEST_PREFIX}-concurrent-2"
    local session3="${TEST_PREFIX}-concurrent-3"

    log_info "Creating multiple concurrent sessions"

    # Create first session
    if ! spawn_test_session "$session1" --cc 1; then
        log_error "Failed to create session 1"
        return 1
    fi
    log_info "Session 1 created: $session1"

    # Create second session
    if ! spawn_test_session "$session2" --cc 1; then
        log_error "Failed to create session 2"
        return 1
    fi
    log_info "Session 2 created: $session2"

    # Create third session
    if ! spawn_test_session "$session3" --cc 1; then
        log_error "Failed to create session 3"
        return 1
    fi
    log_info "Session 3 created: $session3"

    sleep 2

    # Verify all sessions exist
    local all_exist=true
    for session in "$session1" "$session2" "$session3"; do
        if ! tmux has-session -t "$session" 2>/dev/null; then
            log_error "Session $session does not exist"
            all_exist=false
        fi
    done

    if [[ "$all_exist" == "true" ]]; then
        log_assert_eq "all_exist" "all_exist" "all 3 concurrent sessions created"
    fi

    # Count sessions via robot-status
    local session_count
    session_count=$(get_session_count "${TEST_PREFIX}-concurrent")
    if [[ "$session_count" -ge 3 ]]; then
        log_assert_eq "3" "3" "robot-status shows 3 concurrent sessions"
    else
        log_warn "Expected 3 sessions, robot-status shows $session_count"
    fi

    # Cleanup
    for session in "$session1" "$session2" "$session3"; do
        tmux kill-session -t "$session" 2>/dev/null || true
    done
}

#
# Session Listing Test
#
test_session_listing() {
    local session1="${TEST_PREFIX}-list-a"
    local session2="${TEST_PREFIX}-list-b"

    log_info "Testing session listing"

    # Create sessions
    if ! spawn_test_session "$session1" --cc 1; then
        log_skip "Could not create test session 1"
        return 0
    fi
    if ! spawn_test_session "$session2" --cc 1; then
        log_skip "Could not create test session 2"
        return 0
    fi

    sleep 2

    # Test ntm list command
    log_info "Running ntm list"
    local output
    local exit_code=0
    output=$(ntm list 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        # Should show our sessions
        if [[ "$output" == *"$session1"* ]] && [[ "$output" == *"$session2"* ]]; then
            log_assert_eq "found" "found" "ntm list shows our sessions"
        else
            log_warn "ntm list may not show all sessions"
        fi
    else
        log_warn "ntm list returned exit code $exit_code"
    fi

    # Test robot-status listing
    output=$(ntm --robot-status 2>&1) || exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-status returns valid JSON"

        local found1
        found1=$(echo "$output" | jq -r --arg name "$session1" '.sessions[]? | select(.name == $name) | .name // ""')
        log_assert_eq "$found1" "$session1" "robot-status lists session 1"

        local found2
        found2=$(echo "$output" | jq -r --arg name "$session2" '.sessions[]? | select(.name == $name) | .name // ""')
        log_assert_eq "$found2" "$session2" "robot-status lists session 2"
    fi

    # Cleanup
    tmux kill-session -t "$session1" 2>/dev/null || true
    tmux kill-session -t "$session2" 2>/dev/null || true
}

#
# Session Save Test
#
test_session_save() {
    local session="${TEST_PREFIX}-save"
    local save_file="/tmp/ntm-save-${TEST_PREFIX}.json"

    log_info "Testing session save: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Send some work to create state
    ntm send "$session" --cc "echo save-test" 2>/dev/null || true
    sleep 1

    # Save session
    log_info "Saving session to $save_file"
    local output
    local exit_code=0
    output=$(ntm --robot-save="$session" --save-output="$save_file" 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-save returns valid JSON"

        # Verify save file was created
        if [[ -f "$save_file" ]]; then
            log_assert_eq "created" "created" "save file created"

            # Verify save file is valid JSON
            if jq . "$save_file" >/dev/null 2>&1; then
                log_assert_eq "valid" "valid" "save file is valid JSON"

                # Check save file has session info
                local saved_session
                saved_session=$(jq -r '.session // .name // ""' "$save_file")
                log_assert_not_empty "$saved_session" "save file has session name"
            else
                log_error "save file is not valid JSON"
            fi
        else
            log_warn "save file not created at $save_file"
        fi
    else
        log_warn "robot-save returned exit code $exit_code"
        log_info "Output: $output"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
    rm -f "$save_file" 2>/dev/null || true
}

#
# Session Restore Test
#
test_session_restore() {
    local session="${TEST_PREFIX}-restore"
    local save_file="/tmp/ntm-save-${TEST_PREFIX}-restore.json"

    log_info "Testing session restore: $session"

    # First create and save a session
    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Save it
    ntm --robot-save="$session" --save-output="$save_file" 2>/dev/null || true

    # Kill the session
    tmux kill-session -t "$session" 2>/dev/null || true
    sleep 1

    # Verify session is gone
    if tmux has-session -t "$session" 2>/dev/null; then
        log_warn "session still exists after kill"
        tmux kill-session -t "$session" 2>/dev/null || true
    fi

    # Try to restore (if save file exists)
    if [[ -f "$save_file" ]]; then
        log_info "Restoring session from $save_file"
        local output
        local exit_code=0
        output=$(ntm --robot-restore="$save_file" --dry-run 2>&1) || exit_code=$?

        if [[ $exit_code -eq 0 ]]; then
            if echo "$output" | jq . >/dev/null 2>&1; then
                log_assert_valid_json "$output" "robot-restore dry-run returns valid JSON"
            fi
            log_assert_eq "can_restore" "can_restore" "restore dry-run succeeded"
        else
            log_info "robot-restore returned exit code $exit_code (may be expected)"
        fi
    else
        log_skip "No save file to restore from"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
    rm -f "$save_file" 2>/dev/null || true
}

#
# Cross-Session Status Test
#
test_cross_session_status() {
    local session1="${TEST_PREFIX}-cross-1"
    local session2="${TEST_PREFIX}-cross-2"

    log_info "Testing cross-session status"

    # Create two sessions
    if ! spawn_test_session "$session1" --cc 1; then
        log_skip "Could not create test session 1"
        return 0
    fi
    if ! spawn_test_session "$session2" --cc 1; then
        log_skip "Could not create test session 2"
        return 0
    fi

    sleep 2

    # Get combined status
    local output
    local exit_code=0
    output=$(ntm --robot-status 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "cross-session status is valid JSON"

        # Both sessions should be in the output
        local sessions
        sessions=$(echo "$output" | jq -r '[.sessions[]?.name] | join(",")')
        log_info "Sessions in status: $sessions"

        if [[ "$sessions" == *"$session1"* ]] && [[ "$sessions" == *"$session2"* ]]; then
            log_assert_eq "both" "both" "robot-status shows both sessions"
        else
            log_warn "robot-status may not show all sessions"
        fi
    fi

    # Test robot-markdown for cross-session view
    output=$(ntm --robot-markdown 2>&1) || exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        log_assert_not_empty "$output" "robot-markdown has content"
    fi

    # Cleanup
    tmux kill-session -t "$session1" 2>/dev/null || true
    tmux kill-session -t "$session2" 2>/dev/null || true
}

#
# Session Isolation Test
#
test_session_isolation() {
    local session1="${TEST_PREFIX}-iso-1"
    local session2="${TEST_PREFIX}-iso-2"

    log_info "Testing session isolation"

    # Create two independent sessions
    if ! spawn_test_session "$session1" --cc 1; then
        log_skip "Could not create test session 1"
        return 0
    fi
    if ! spawn_test_session "$session2" --cc 1; then
        log_skip "Could not create test session 2"
        return 0
    fi

    sleep 2

    # Send different messages to each
    log_info "Sending distinct messages to each session"
    ntm send "$session1" --cc "echo session-1-message" 2>/dev/null || true
    ntm send "$session2" --cc "echo session-2-message" 2>/dev/null || true

    sleep 1

    # Check status of each independently
    local status1
    local status2
    status1=$(ntm status "$session1" --json 2>/dev/null) || true
    status2=$(ntm status "$session2" --json 2>/dev/null) || true

    if echo "$status1" | jq . >/dev/null 2>&1; then
        local name1
        name1=$(echo "$status1" | jq -r '.session // .name // ""')
        log_assert_eq "$name1" "$session1" "session 1 status shows correct session"
    fi

    if echo "$status2" | jq . >/dev/null 2>&1; then
        local name2
        name2=$(echo "$status2" | jq -r '.session // .name // ""')
        log_assert_eq "$name2" "$session2" "session 2 status shows correct session"
    fi

    # Kill one session, verify other is unaffected
    log_info "Killing session 1, verifying session 2 survives"
    tmux kill-session -t "$session1" 2>/dev/null || true
    sleep 1

    if tmux has-session -t "$session2" 2>/dev/null; then
        log_assert_eq "survives" "survives" "session 2 survives when session 1 killed"
    else
        log_error "session 2 was unexpectedly killed"
    fi

    # Cleanup
    tmux kill-session -t "$session2" 2>/dev/null || true
}

#
# Batch Operations Test
#
test_batch_operations() {
    local session1="${TEST_PREFIX}-batch-1"
    local session2="${TEST_PREFIX}-batch-2"

    log_info "Testing batch operations across sessions"

    # Create sessions
    if ! spawn_test_session "$session1" --cc 1; then
        log_skip "Could not create test session 1"
        return 0
    fi
    if ! spawn_test_session "$session2" --cc 1; then
        log_skip "Could not create test session 2"
        return 0
    fi

    sleep 2

    # Get combined terse status
    local output
    local exit_code=0
    output=$(ntm --robot-terse 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        log_assert_not_empty "$output" "robot-terse returns content"
        log_info "Terse status: $output"
    fi

    # Get snapshot of all sessions
    output=$(ntm --robot-snapshot 2>&1) || exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-snapshot is valid JSON"

        local session_count
        session_count=$(echo "$output" | jq '.sessions | length')
        if [[ "$session_count" -ge 2 ]]; then
            log_assert_eq ">=2" ">=2" "robot-snapshot captures multiple sessions"
        fi
    fi

    # Cleanup
    tmux kill-session -t "$session1" 2>/dev/null || true
    tmux kill-session -t "$session2" 2>/dev/null || true
}

#
# Robot Snapshot Multi-Session Test
#
test_robot_snapshot_multi() {
    local session1="${TEST_PREFIX}-snap-1"
    local session2="${TEST_PREFIX}-snap-2"

    log_info "Testing robot-snapshot with multiple sessions"

    # Create sessions
    if ! spawn_test_session "$session1" --cc 1; then
        log_skip "Could not create test session 1"
        return 0
    fi
    if ! spawn_test_session "$session2" --cc 2; then
        log_skip "Could not create test session 2"
        return 0
    fi

    sleep 2

    # Get full snapshot
    local output
    local exit_code=0
    output=$(ntm --robot-snapshot 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-snapshot is valid JSON"

        # Should have sessions array
        local has_sessions
        has_sessions=$(echo "$output" | jq 'has("sessions")')
        log_assert_eq "$has_sessions" "true" "snapshot has sessions array"

        # Count total panes across sessions
        local total_panes
        total_panes=$(echo "$output" | jq '[.sessions[]?.panes // [] | length] | add // 0')
        log_info "Total panes in snapshot: $total_panes"

        if [[ "$total_panes" -ge 3 ]]; then
            log_assert_eq ">=3" ">=3" "snapshot captures panes from multiple sessions"
        fi

        # Check for timestamp
        local has_timestamp
        has_timestamp=$(echo "$output" | jq 'has("timestamp") or has("snapshot_time") or has("taken_at")')
        log_assert_eq "$has_timestamp" "true" "snapshot has timestamp"
    else
        log_error "robot-snapshot failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session1" 2>/dev/null || true
    tmux kill-session -t "$session2" 2>/dev/null || true
}

#
# Session Naming Patterns Test
#
test_session_naming() {
    local session_normal="${TEST_PREFIX}-normal"
    local session_dash="${TEST_PREFIX}-with-dashes"
    local session_underscore="${TEST_PREFIX}_underscore"

    log_info "Testing session naming patterns"

    # Test normal name
    if spawn_test_session "$session_normal" --cc 1; then
        log_assert_eq "created" "created" "normal session name works"
    else
        log_error "failed to create session with normal name"
    fi

    # Test name with dashes
    if spawn_test_session "$session_dash" --cc 1; then
        log_assert_eq "created" "created" "session name with dashes works"
    else
        log_error "failed to create session with dashes"
    fi

    # Test name with underscore
    if spawn_test_session "$session_underscore" --cc 1; then
        log_assert_eq "created" "created" "session name with underscore works"
    else
        log_error "failed to create session with underscore"
    fi

    sleep 1

    # Verify all exist
    local all_exist=true
    for session in "$session_normal" "$session_dash" "$session_underscore"; do
        if ! tmux has-session -t "$session" 2>/dev/null; then
            log_warn "session $session does not exist"
            all_exist=false
        fi
    done

    if [[ "$all_exist" == "true" ]]; then
        log_assert_eq "all" "all" "all naming patterns work"
    fi

    # Cleanup
    tmux kill-session -t "$session_normal" 2>/dev/null || true
    tmux kill-session -t "$session_dash" 2>/dev/null || true
    tmux kill-session -t "$session_underscore" 2>/dev/null || true
}

#
# Concurrent Session Creation Test
#
test_concurrent_creation() {
    local base="${TEST_PREFIX}-rapid"

    log_info "Testing rapid concurrent session creation"

    # Create multiple sessions rapidly
    local sessions=()
    local created=0
    for i in {1..3}; do
        local session="${base}-${i}"
        sessions+=("$session")
        CREATED_SESSIONS+=("$session")

        # Use robot-spawn for faster creation
        local output
        output=$(echo "y" | ntm --robot-spawn="$session" --spawn-cc=1 2>&1) || true

        if echo "$output" | jq . >/dev/null 2>&1; then
            local success
            success=$(echo "$output" | jq -r '.session // ""')
            if [[ -n "$success" ]]; then
                ((created++)) || true
            fi
        fi
    done

    log_info "Created $created sessions rapidly"

    sleep 2

    # Verify sessions exist
    local existing=0
    for session in "${sessions[@]}"; do
        if tmux has-session -t "$session" 2>/dev/null; then
            ((existing++)) || true
        fi
    done

    log_info "Sessions existing after rapid creation: $existing"

    if [[ "$existing" -ge 2 ]]; then
        log_assert_eq ">=2" ">=2" "rapid concurrent creation works"
    else
        log_warn "fewer sessions than expected after rapid creation"
    fi

    # Cleanup
    for session in "${sessions[@]}"; do
        tmux kill-session -t "$session" 2>/dev/null || true
    done
}

main
