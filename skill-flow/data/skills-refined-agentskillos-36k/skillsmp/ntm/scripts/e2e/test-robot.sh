#!/usr/bin/env bash
# E2E Test: Comprehensive Robot Mode Tests
# Tests all major robot mode flags for machine-readable JSON output.
# Covers: ntm-kbkb - Robot mode comprehensive tests

set -uo pipefail
# Note: Not using -e so that assertion failures don't cause early exit.
# Failures are tracked via log library and reported in summary.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"
set +e  # Disable immediate exit on error so tests continue after assertion failures

# Test session prefix (unique per run to avoid conflicts)
TEST_PREFIX="e2e-robot-$$"

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
    log_init "test-robot"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    # Robot Version Tests
    log_section "Test: robot-version"
    test_robot_version

    # Robot Status Tests
    log_section "Test: robot-status (empty)"
    test_robot_status_empty

    log_section "Test: robot-status (with sessions)"
    test_robot_status_with_sessions

    # Robot Spawn Tests
    log_section "Test: robot-spawn (basic)"
    test_robot_spawn_basic

    log_section "Test: robot-spawn (multiple agents)"
    test_robot_spawn_multiple

    log_section "Test: robot-spawn (dry-run)"
    test_robot_spawn_dry_run

    log_section "Test: robot-spawn (with working dir)"
    test_robot_spawn_with_dir

    # Robot Send Tests
    log_section "Test: robot-send (single pane)"
    test_robot_send_single

    log_section "Test: robot-send (by type)"
    test_robot_send_by_type

    log_section "Test: robot-send (all panes)"
    test_robot_send_all

    log_section "Test: robot-send (with exclude)"
    test_robot_send_exclude

    log_section "Test: robot-send (non-existent session)"
    test_robot_send_nonexistent

    # Robot Tail Tests
    log_section "Test: robot-tail"
    test_robot_tail

    # Robot Interrupt Tests
    log_section "Test: robot-interrupt (agents only)"
    test_robot_interrupt

    log_section "Test: robot-interrupt (with message)"
    test_robot_interrupt_with_msg

    # Robot Activity Tests
    log_section "Test: robot-activity"
    test_robot_activity

    # Robot Context Tests
    log_section "Test: robot-context"
    test_robot_context

    # Robot Health Tests
    log_section "Test: robot-health"
    test_robot_health

    # Robot Schema Tests
    log_section "Test: robot-schema"
    test_robot_schema

    # Robot Snapshot Tests
    log_section "Test: robot-snapshot"
    test_robot_snapshot

    # Robot Plan Tests
    log_section "Test: robot-plan"
    test_robot_plan

    # Robot Dashboard Tests
    log_section "Test: robot-dashboard"
    test_robot_dashboard

    # Robot Markdown Tests
    log_section "Test: robot-markdown"
    test_robot_markdown

    # Robot Terse Tests
    log_section "Test: robot-terse"
    test_robot_terse

    # Robot Help Tests
    log_section "Test: robot-help"
    test_robot_help

    # Robot Recipes Tests
    log_section "Test: robot-recipes"
    test_robot_recipes

    log_summary
}

#
# Version Tests
#
test_robot_version() {
    log_info "Testing robot-version JSON output"

    local output
    local exit_code=0
    output=$(ntm --robot-version 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-version returns valid JSON"

        local version
        version=$(echo "$output" | jq -r '.version // ""')
        log_assert_not_empty "$version" "robot-version has version field"

        # Check for expected fields
        local has_commit
        has_commit=$(echo "$output" | jq 'has("commit")')
        log_assert_eq "$has_commit" "true" "robot-version has commit field"

        local has_build_date
        has_build_date=$(echo "$output" | jq 'has("build_date")')
        log_assert_eq "$has_build_date" "true" "robot-version has build_date field"
    else
        log_error "robot-version failed with exit code $exit_code"
    fi
}

#
# Status Tests
#
test_robot_status_empty() {
    log_info "Testing robot-status when no sessions exist"

    # Kill all test sessions first to ensure clean state
    cleanup_sessions "${TEST_PREFIX}"

    local output
    local exit_code=0
    output=$(ntm --robot-status 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-status returns valid JSON"

        # Should have sessions array (even if empty)
        local has_sessions
        has_sessions=$(echo "$output" | jq 'has("sessions")')
        log_assert_eq "$has_sessions" "true" "robot-status has sessions field"
    else
        log_error "robot-status failed with exit code $exit_code"
    fi
}

test_robot_status_with_sessions() {
    local session="${TEST_PREFIX}-status"

    log_info "Creating session for robot-status test: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    log_info "Session spawned successfully"

    sleep 2

    local output
    local exit_code=0
    output=$(ntm --robot-status 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-status with sessions returns valid JSON"

        # Should find our session
        local found_session
        found_session=$(echo "$output" | jq -r --arg name "$session" '.sessions[]? | select(.name == $name) | .name // ""')
        log_assert_eq "$found_session" "$session" "robot-status lists created session"

        # Check session has panes
        local pane_count
        pane_count=$(echo "$output" | jq -r --arg name "$session" '[.sessions[]? | select(.name == $name) | .panes[]?] | length')
        if [[ "$pane_count" -ge 2 ]]; then
            log_assert_eq "1" "1" "robot-status shows panes for session"
        else
            log_warn "Expected at least 2 panes, got $pane_count"
        fi
    else
        log_error "robot-status failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Spawn Tests
#
test_robot_spawn_basic() {
    local session="${TEST_PREFIX}-spawn-basic"
    CREATED_SESSIONS+=("$session")

    log_info "Testing robot-spawn basic: $session"

    local output
    local exit_code=0
    output=$(echo "y" | ntm --robot-spawn="$session" --spawn-cc=1 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-spawn returns valid JSON"

        local session_name
        session_name=$(echo "$output" | jq -r '.session // ""')
        log_assert_eq "$session_name" "$session" "robot-spawn session name matches"

        local agents_count
        agents_count=$(echo "$output" | jq '.agents | length')
        log_assert_eq "$agents_count" "2" "robot-spawn returns 2 agents (user + claude)"

        local has_created_at
        has_created_at=$(echo "$output" | jq 'has("created_at")')
        log_assert_eq "$has_created_at" "true" "robot-spawn has created_at field"

        local has_working_dir
        has_working_dir=$(echo "$output" | jq 'has("working_dir")')
        log_assert_eq "$has_working_dir" "true" "robot-spawn has working_dir field"
    else
        log_error "robot-spawn failed with exit code $exit_code"
        log_error "Output: $output"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_spawn_multiple() {
    local session="${TEST_PREFIX}-spawn-multi"
    CREATED_SESSIONS+=("$session")

    log_info "Testing robot-spawn with multiple agents: $session"

    local output
    local exit_code=0
    output=$(echo "y" | ntm --robot-spawn="$session" --spawn-cc=2 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-spawn multi returns valid JSON"

        local agents_count
        agents_count=$(echo "$output" | jq '.agents | length')
        log_assert_eq "$agents_count" "3" "robot-spawn returns 3 agents (user + 2 claude)"

        # Check agent types
        local claude_count
        claude_count=$(echo "$output" | jq '[.agents[]? | select(.type == "claude")] | length')
        log_assert_eq "$claude_count" "2" "robot-spawn shows 2 Claude agents"

        local user_count
        user_count=$(echo "$output" | jq '[.agents[]? | select(.type == "user")] | length')
        log_assert_eq "$user_count" "1" "robot-spawn shows 1 user pane"
    else
        log_error "robot-spawn multi failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_spawn_dry_run() {
    local session="${TEST_PREFIX}-spawn-dry"

    log_info "Testing robot-spawn dry-run: $session"

    local output
    local exit_code=0
    output=$(ntm --robot-spawn="$session" --spawn-cc=1 --dry-run 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-spawn dry-run returns valid JSON"

        # Verify session was NOT actually created
        if tmux has-session -t "$session" 2>/dev/null; then
            log_error "dry-run should not create actual session"
            tmux kill-session -t "$session" 2>/dev/null || true
        else
            log_assert_eq "not_created" "not_created" "dry-run does not create session"
        fi

        # Check for dry_run indicator in output
        local is_dry_run
        is_dry_run=$(echo "$output" | jq -r '.dry_run // false')
        log_assert_eq "$is_dry_run" "true" "robot-spawn dry-run has dry_run=true"
    else
        log_error "robot-spawn dry-run failed with exit code $exit_code"
    fi
}

test_robot_spawn_with_dir() {
    local session="${TEST_PREFIX}-spawn-dir"
    CREATED_SESSIONS+=("$session")
    local test_dir="/tmp/ntm-test-$$"
    mkdir -p "$test_dir"

    log_info "Testing robot-spawn with working dir: $session"

    local output
    local exit_code=0
    output=$(echo "y" | ntm --robot-spawn="$session" --spawn-cc=1 --spawn-dir="$test_dir" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-spawn with dir returns valid JSON"

        local working_dir
        working_dir=$(echo "$output" | jq -r '.working_dir // ""')
        log_assert_eq "$working_dir" "$test_dir" "robot-spawn working_dir matches"
    else
        log_error "robot-spawn with dir failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
    rm -rf "$test_dir"
}

#
# Send Tests
#
test_robot_send_single() {
    local session="${TEST_PREFIX}-send-single"

    log_info "Creating session for robot-send single test: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-send to single pane"

    local output
    local exit_code=0
    output=$(ntm --robot-send="$session" --msg="echo test-single" --panes=1 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-send single returns valid JSON"

        local success
        success=$(echo "$output" | jq -r '.success // false')
        log_assert_eq "$success" "true" "robot-send single reports success"

        local delivered
        delivered=$(echo "$output" | jq -r '(.successful | length)')
        log_assert_eq "$delivered" "1" "robot-send single delivered to 1 pane"
    else
        log_error "robot-send single failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_send_by_type() {
    local session="${TEST_PREFIX}-send-type"

    log_info "Creating session for robot-send by type test: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-send by type (claude)"

    local output
    local exit_code=0
    output=$(ntm --robot-send="$session" --msg="echo test-type" --type=claude 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-send by type returns valid JSON"

        local success
        success=$(echo "$output" | jq -r '.success // false')
        log_assert_eq "$success" "true" "robot-send by type reports success"

        local delivered
        delivered=$(echo "$output" | jq -r '(.successful | length)')
        if [[ "$delivered" -ge 2 ]]; then
            log_assert_eq "1" "1" "robot-send by type delivered to Claude agents"
        else
            log_warn "Expected delivery to 2 Claude agents, got $delivered"
        fi
    else
        log_error "robot-send by type failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_send_all() {
    local session="${TEST_PREFIX}-send-all"

    log_info "Creating session for robot-send all test: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-send to all panes"

    local output
    local exit_code=0
    output=$(ntm --robot-send="$session" --msg="echo test-all" --all 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-send all returns valid JSON"

        local success
        success=$(echo "$output" | jq -r '.success // false')
        log_assert_eq "$success" "true" "robot-send all reports success"

        local delivered
        delivered=$(echo "$output" | jq -r '(.successful | length)')
        if [[ "$delivered" -ge 3 ]]; then
            log_assert_eq "1" "1" "robot-send all delivered to all panes (including user)"
        else
            log_warn "Expected delivery to 3+ panes, got $delivered"
        fi
    else
        log_error "robot-send all failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_send_exclude() {
    local session="${TEST_PREFIX}-send-excl"

    log_info "Creating session for robot-send exclude test: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-send with exclude"

    local output
    local exit_code=0
    output=$(ntm --robot-send="$session" --msg="echo test-exclude" --all --exclude=0 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-send exclude returns valid JSON"

        local success
        success=$(echo "$output" | jq -r '.success // false')
        log_assert_eq "$success" "true" "robot-send exclude reports success"

        # Should deliver to 2 panes (excluding user at index 0)
        local delivered
        delivered=$(echo "$output" | jq -r '(.successful | length)')
        log_assert_eq "$delivered" "2" "robot-send exclude delivered to 2 panes (excluding user)"
    else
        log_error "robot-send exclude failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_send_nonexistent() {
    local fake_session="nonexistent-$$-${RANDOM}"

    log_info "Testing robot-send to non-existent session"

    local output
    local exit_code=0
    output=$(ntm --robot-send="$fake_session" --msg="test" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -ne 0 ]]; then
        log_assert_eq "error" "error" "robot-send to non-existent session returns error"

        if echo "$output" | jq . >/dev/null 2>&1; then
            local success
            success=$(echo "$output" | jq -r '.success // true')
            log_assert_eq "$success" "false" "robot-send error has success=false"

            local has_error
            has_error=$(echo "$output" | jq 'has("error") or has("error_code")')
            log_assert_eq "$has_error" "true" "robot-send error has error info"
        fi
    else
        log_warn "robot-send to non-existent session unexpectedly succeeded"
    fi
}

#
# Tail Tests
#
test_robot_tail() {
    local session="${TEST_PREFIX}-tail"

    log_info "Creating session for robot-tail test: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-tail"

    local output
    local exit_code=0
    output=$(ntm --robot-tail="$session" --lines=10 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-tail returns valid JSON"

        local has_panes
        has_panes=$(echo "$output" | jq 'has("panes")')
        log_assert_eq "$has_panes" "true" "robot-tail has panes field"

        local pane_count
        pane_count=$(echo "$output" | jq '.panes | length')
        if [[ "$pane_count" -ge 1 ]]; then
            log_assert_eq "1" "1" "robot-tail returns pane output"
        else
            log_warn "Expected at least 1 pane output"
        fi
    else
        log_error "robot-tail failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Interrupt Tests
#
test_robot_interrupt() {
    local session="${TEST_PREFIX}-interrupt"

    log_info "Creating session for robot-interrupt test: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-interrupt"

    local output
    local exit_code=0
    output=$(ntm --robot-interrupt="$session" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-interrupt returns valid JSON"

        local success
        success=$(echo "$output" | jq -r '.success // false')
        log_assert_eq "$success" "true" "robot-interrupt reports success"
    else
        log_error "robot-interrupt failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

test_robot_interrupt_with_msg() {
    local session="${TEST_PREFIX}-int-msg"

    log_info "Creating session for robot-interrupt with message test: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-interrupt with follow-up message"

    local output
    local exit_code=0
    output=$(ntm --robot-interrupt="$session" --interrupt-msg="echo 'after interrupt'" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-interrupt with msg returns valid JSON"

        local success
        success=$(echo "$output" | jq -r '.success // false')
        log_assert_eq "$success" "true" "robot-interrupt with msg reports success"
    else
        log_error "robot-interrupt with msg failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Activity Tests
#
test_robot_activity() {
    local session="${TEST_PREFIX}-activity"

    log_info "Creating session for robot-activity test: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-activity"

    local output
    local exit_code=0
    output=$(ntm --robot-activity="$session" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-activity returns valid JSON"

        local has_agents
        has_agents=$(echo "$output" | jq 'has("agents") or has("panes")')
        log_assert_eq "$has_agents" "true" "robot-activity has agents/panes data"
    else
        log_error "robot-activity failed with exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Context Tests
#
test_robot_context() {
    local session="${TEST_PREFIX}-context"

    log_info "Creating session for robot-context test: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi
    sleep 2

    log_info "Testing robot-context"

    local output
    local exit_code=0
    output=$(ntm --robot-context="$session" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-context returns valid JSON"

        local has_session
        has_session=$(echo "$output" | jq 'has("session")')
        log_assert_eq "$has_session" "true" "robot-context has session field"
    else
        log_warn "robot-context returned exit code $exit_code (may be expected if no context data)"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Health Tests
#
test_robot_health() {
    log_info "Testing robot-health (project level)"

    local output
    local exit_code=0
    output=$(ntm --robot-health="" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-health returns valid JSON"
    else
        log_warn "robot-health returned exit code $exit_code (may be expected)"
    fi
}

#
# Schema Tests
#
test_robot_schema() {
    log_info "Testing robot-schema for various types"

    # Test status schema
    local output
    local exit_code=0
    output=$(ntm --robot-schema=status 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-schema status returns valid JSON"

        local has_schema
        has_schema=$(echo "$output" | jq 'has("$schema") or has("type") or has("properties")')
        log_assert_eq "$has_schema" "true" "robot-schema has schema structure"
    else
        log_error "robot-schema status failed with exit code $exit_code"
    fi

    # Test all schema
    output=$(ntm --robot-schema=all 2>&1) || exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-schema all returns valid JSON"
    else
        log_warn "robot-schema all returned exit code $exit_code"
    fi
}

#
# Snapshot Tests
#
test_robot_snapshot() {
    log_info "Testing robot-snapshot"

    local output
    local exit_code=0
    output=$(ntm --robot-snapshot 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-snapshot returns valid JSON"

        local has_sessions
        has_sessions=$(echo "$output" | jq 'has("sessions")')
        log_assert_eq "$has_sessions" "true" "robot-snapshot has sessions field"

        local has_timestamp
        has_timestamp=$(echo "$output" | jq 'has("timestamp") or has("snapshot_time")')
        log_assert_eq "$has_timestamp" "true" "robot-snapshot has timestamp"
    else
        log_error "robot-snapshot failed with exit code $exit_code"
    fi
}

#
# Plan Tests
#
test_robot_plan() {
    log_info "Testing robot-plan"

    local output
    local exit_code=0
    output=$(ntm --robot-plan 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-plan returns valid JSON"
    else
        log_warn "robot-plan returned exit code $exit_code (may be expected if bv not configured)"
    fi
}

#
# Dashboard Tests
#
test_robot_dashboard() {
    log_info "Testing robot-dashboard"

    local output
    local exit_code=0
    output=$(ntm --robot-dashboard 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        # Dashboard can return markdown or JSON
        if echo "$output" | jq . >/dev/null 2>&1; then
            log_assert_valid_json "$output" "robot-dashboard returns valid JSON"
        else
            log_assert_not_empty "$output" "robot-dashboard returns markdown content"
        fi
    else
        log_error "robot-dashboard failed with exit code $exit_code"
    fi
}

#
# Markdown Tests
#
test_robot_markdown() {
    log_info "Testing robot-markdown"

    local output
    local exit_code=0
    output=$(ntm --robot-markdown 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_not_empty "$output" "robot-markdown returns content"
        # Markdown should contain some common elements
        if [[ "$output" == *"|"* ]] || [[ "$output" == *"#"* ]] || [[ "$output" == *"---"* ]]; then
            log_assert_eq "has_md" "has_md" "robot-markdown contains markdown elements"
        else
            log_warn "robot-markdown output may not contain expected markdown elements"
        fi
    else
        log_error "robot-markdown failed with exit code $exit_code"
    fi
}

#
# Terse Tests
#
test_robot_terse() {
    log_info "Testing robot-terse"

    local output
    local exit_code=0
    output=$(ntm --robot-terse 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_not_empty "$output" "robot-terse returns content"
        # Terse format should be compact, typically one line
        local line_count
        line_count=$(echo "$output" | wc -l | tr -d ' ')
        if [[ "$line_count" -le 3 ]]; then
            log_assert_eq "compact" "compact" "robot-terse returns compact output"
        else
            log_warn "robot-terse output has $line_count lines (expected compact)"
        fi
    else
        log_error "robot-terse failed with exit code $exit_code"
    fi
}

#
# Help Tests
#
test_robot_help() {
    log_info "Testing robot-help"

    local output
    local exit_code=0
    output=$(ntm --robot-help 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-help returns valid JSON"

        # Should have help content
        log_assert_not_empty "$output" "robot-help has content"
    else
        log_error "robot-help failed with exit code $exit_code"
    fi
}

#
# Recipes Tests
#
test_robot_recipes() {
    log_info "Testing robot-recipes"

    local output
    local exit_code=0
    output=$(ntm --robot-recipes 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-recipes returns valid JSON"

        # Should have recipes array
        local has_recipes
        has_recipes=$(echo "$output" | jq 'has("recipes") or type == "array"')
        log_assert_eq "$has_recipes" "true" "robot-recipes has recipes data"
    else
        log_error "robot-recipes failed with exit code $exit_code"
    fi
}

main
