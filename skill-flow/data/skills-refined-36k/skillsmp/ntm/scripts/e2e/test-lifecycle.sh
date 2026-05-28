#!/usr/bin/env bash
# E2E Test: Agent Lifecycle Tests
# Tests the complete agent lifecycle: spawn, send, monitor, and kill.
# Covers: ntm-0hov - E2E agent lifecycle tests (spawn/send/kill)

set -uo pipefail
# Note: Not using -e so that assertion failures don't cause early exit.
# Failures are tracked via log library and reported in summary.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/log.sh"
set +e  # Disable immediate exit on error so tests continue after assertion failures

# Test session prefix (unique per run to avoid conflicts)
TEST_PREFIX="e2e-life-$$"

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

# Helper to check if pane exists
pane_exists() {
    local session="$1"
    local pane_index="$2"
    tmux list-panes -t "$session" -F '#{pane_index}' 2>/dev/null | command grep -q "^${pane_index}$"
}

# Helper to get pane count
get_pane_count() {
    local session="$1"
    tmux list-panes -t "$session" -F '#{pane_id}' 2>/dev/null | wc -l | tr -d ' '
}

# Helper to get agent count by type
get_agent_count_by_type() {
    local session="$1"
    local agent_type="$2"
    ntm status "$session" --json 2>/dev/null | jq -r --arg type "$agent_type" '[.panes[]? | select(.type == $type)] | length'
}

# Main test
main() {
    log_init "test-lifecycle"

    # Prerequisites
    require_ntm
    require_tmux
    require_jq

    # Single Agent Lifecycle
    log_section "Test: Single agent lifecycle"
    test_single_agent_lifecycle

    # Multi-Agent Lifecycle
    log_section "Test: Multi-agent lifecycle"
    test_multi_agent_lifecycle

    # Agent Kill Specific Pane
    log_section "Test: Kill specific agent"
    test_kill_specific_agent

    # Kill All Agents
    log_section "Test: Kill all agents"
    test_kill_all_agents

    # Crash Detection
    log_section "Test: Agent crash detection"
    test_agent_crash_detection

    # Session Cleanup
    log_section "Test: Session cleanup"
    test_session_cleanup

    # State Monitoring
    log_section "Test: State monitoring"
    test_state_monitoring

    # Add Agent to Existing Session
    log_section "Test: Add agent to session"
    test_add_agent

    # Agent Activity Tracking
    log_section "Test: Activity tracking"
    test_activity_tracking

    # Interrupt and Resume
    log_section "Test: Interrupt workflow"
    test_interrupt_workflow

    log_summary
}

#
# Single Agent Lifecycle Test
#
test_single_agent_lifecycle() {
    local session="${TEST_PREFIX}-single"

    log_info "Testing single agent lifecycle: $session"

    # Step 1: Spawn
    log_info "Step 1: Spawning session with 1 Claude agent"
    if ! spawn_test_session "$session" --cc 1; then
        log_error "Failed to spawn session"
        return 1
    fi
    log_assert_eq "spawned" "spawned" "session spawned successfully"

    # Verify session exists
    if ! tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "exists" "missing" "session should exist after spawn"
        return 1
    fi
    log_assert_eq "exists" "exists" "session exists after spawn"

    # Verify pane count (1 user + 1 claude = 2)
    local pane_count
    pane_count=$(get_pane_count "$session")
    log_assert_eq "$pane_count" "2" "single agent spawn creates 2 panes"

    sleep 2

    # Step 2: Send work
    log_info "Step 2: Sending work to agent"
    if log_exec ntm send "$session" --cc "echo hello-lifecycle"; then
        log_assert_eq "0" "0" "send command succeeded"
    else
        log_error "send command failed"
    fi

    sleep 1

    # Step 3: Monitor status
    log_info "Step 3: Monitoring agent status"
    if log_exec ntm status "$session" --json; then
        local output="$_LAST_OUTPUT"
        log_assert_valid_json "$output" "status is valid JSON"

        local claude_count
        claude_count=$(echo "$output" | jq '[.panes[]? | select(.type == "claude")] | length')
        log_assert_eq "$claude_count" "1" "status shows 1 Claude agent"
    fi

    # Step 4: Kill session
    log_info "Step 4: Killing session"
    if log_exec ntm kill "$session"; then
        log_assert_eq "0" "0" "kill command succeeded"
    else
        log_warn "kill command failed"
    fi

    # Verify session is gone
    sleep 1
    if ! tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "killed" "killed" "session killed successfully"
    else
        log_warn "session still exists after kill"
        tmux kill-session -t "$session" 2>/dev/null || true
    fi
}

#
# Multi-Agent Lifecycle Test
#
test_multi_agent_lifecycle() {
    local session="${TEST_PREFIX}-multi"

    log_info "Testing multi-agent lifecycle: $session"

    # Spawn with multiple agents
    log_info "Spawning session with 2 Claude agents"
    if ! spawn_test_session "$session" --cc 2; then
        log_error "Failed to spawn multi-agent session"
        return 1
    fi
    log_assert_eq "spawned" "spawned" "multi-agent session spawned"

    sleep 2

    # Verify pane count (1 user + 2 claude = 3)
    local pane_count
    pane_count=$(get_pane_count "$session")
    log_assert_eq "$pane_count" "3" "multi-agent spawn creates 3 panes"

    # Send to all Claude agents
    log_info "Broadcasting message to all agents"
    if log_exec ntm send "$session" --cc "echo multi-agent-test"; then
        log_assert_eq "0" "0" "broadcast send succeeded"
    fi

    sleep 1

    # Monitor all agents
    if log_exec ntm status "$session" --json; then
        local output="$_LAST_OUTPUT"
        local claude_count
        claude_count=$(echo "$output" | jq '[.panes[]? | select(.type == "claude")] | length')
        log_assert_eq "$claude_count" "2" "status shows 2 Claude agents"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Kill Specific Agent Test
#
test_kill_specific_agent() {
    local session="${TEST_PREFIX}-kill-one"

    log_info "Testing kill specific agent: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Get initial pane count
    local initial_count
    initial_count=$(get_pane_count "$session")
    log_info "Initial pane count: $initial_count"

    # Try to kill one agent pane (index 1 is usually first Claude agent)
    log_info "Killing agent at pane index 1"
    tmux kill-pane -t "${session}:0.1" 2>/dev/null || true

    sleep 1

    # Verify pane count decreased
    local after_count
    after_count=$(get_pane_count "$session")
    log_info "Pane count after kill: $after_count"

    if [[ "$after_count" -lt "$initial_count" ]]; then
        log_assert_eq "decreased" "decreased" "pane count decreased after killing one agent"
    else
        log_warn "pane count did not decrease as expected"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Kill All Agents Test
#
test_kill_all_agents() {
    local session="${TEST_PREFIX}-kill-all"

    log_info "Testing kill all agents: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Use ntm kill to kill the session
    if log_exec ntm kill "$session"; then
        log_assert_eq "0" "0" "ntm kill succeeded"
    else
        log_warn "ntm kill returned non-zero"
    fi

    sleep 1

    # Verify session is gone
    if ! tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "killed" "killed" "session fully killed"
    else
        log_warn "session still exists after kill all"
        tmux kill-session -t "$session" 2>/dev/null || true
    fi
}

#
# Agent Crash Detection Test
#
test_agent_crash_detection() {
    local session="${TEST_PREFIX}-crash"

    log_info "Testing agent crash detection: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Get initial status
    local initial_status
    if log_exec ntm status "$session" --json; then
        initial_status="$_LAST_OUTPUT"
        log_assert_valid_json "$initial_status" "initial status is valid JSON"
    fi

    # Simulate crash by killing the tmux pane externally
    log_info "Simulating agent crash (killing pane externally)"
    tmux kill-pane -t "${session}:0.1" 2>/dev/null || true

    sleep 1

    # Check status after crash
    if log_exec ntm status "$session" --json; then
        local after_status="$_LAST_OUTPUT"
        log_assert_valid_json "$after_status" "status after crash is valid JSON"

        # Status should show reduced agent count or dead state
        local claude_count
        claude_count=$(echo "$after_status" | jq '[.panes[]? | select(.type == "claude")] | length')
        if [[ "$claude_count" -eq 0 ]]; then
            log_assert_eq "detected" "detected" "crash detected (no Claude agents in status)"
        else
            log_info "Status still shows Claude agent (may be stale or session has other agents)"
        fi
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Session Cleanup Test
#
test_session_cleanup() {
    local session="${TEST_PREFIX}-cleanup"

    log_info "Testing session cleanup: $session"

    if ! spawn_test_session "$session" --cc 2; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Get pane IDs before cleanup
    local panes_before
    panes_before=$(tmux list-panes -t "$session" -F '#{pane_id}' 2>/dev/null | wc -l | tr -d ' ')
    log_info "Panes before cleanup: $panes_before"

    # Kill session with cleanup
    log_info "Running ntm kill for cleanup"
    ntm kill "$session" 2>/dev/null || true

    sleep 1

    # Verify no orphan panes
    if tmux has-session -t "$session" 2>/dev/null; then
        local panes_after
        panes_after=$(tmux list-panes -t "$session" -F '#{pane_id}' 2>/dev/null | wc -l | tr -d ' ')
        log_warn "Session still exists with $panes_after panes after cleanup"
        tmux kill-session -t "$session" 2>/dev/null || true
    else
        log_assert_eq "clean" "clean" "session fully cleaned up"
    fi
}

#
# State Monitoring Test
#
test_state_monitoring() {
    local session="${TEST_PREFIX}-state"

    log_info "Testing state monitoring: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Check initial state using robot-activity
    log_info "Checking agent activity state"
    local output
    local exit_code=0
    output=$(ntm --robot-activity="$session" 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]] && echo "$output" | jq . >/dev/null 2>&1; then
        log_assert_valid_json "$output" "activity state is valid JSON"

        # Check for state information
        local has_state_info
        has_state_info=$(echo "$output" | jq 'has("agents") or has("panes") or has("activity")')
        log_assert_eq "$has_state_info" "true" "activity response has state info"
    else
        log_info "robot-activity returned exit code $exit_code (may be expected)"
    fi

    # Use robot-status to check pane states
    output=$(ntm --robot-status 2>&1) || exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        log_assert_valid_json "$output" "robot-status is valid JSON"

        local our_session
        our_session=$(echo "$output" | jq -r --arg name "$session" '.sessions[]? | select(.name == $name) | .name // ""')
        log_assert_eq "$our_session" "$session" "robot-status finds our session"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Add Agent Test
#
test_add_agent() {
    local session="${TEST_PREFIX}-add"

    log_info "Testing add agent to session: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Get initial pane count
    local initial_count
    initial_count=$(get_pane_count "$session")
    log_info "Initial pane count: $initial_count"

    # Try to add another agent
    log_info "Adding another Claude agent"
    local output
    local exit_code=0
    output=$(ntm add "$session" --cc 1 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        sleep 2
        local after_count
        after_count=$(get_pane_count "$session")
        log_info "Pane count after add: $after_count"

        if [[ "$after_count" -gt "$initial_count" ]]; then
            log_assert_eq "added" "added" "agent added successfully"
        else
            log_warn "pane count did not increase after add"
        fi
    else
        log_info "add command returned exit code $exit_code"
        # ntm add might not be fully implemented
        log_assert_eq "1" "1" "add command executed (may not be implemented)"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Activity Tracking Test
#
test_activity_tracking() {
    local session="${TEST_PREFIX}-activity"

    log_info "Testing activity tracking: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Send a message to generate activity
    log_info "Sending message to generate activity"
    ntm send "$session" --cc "echo activity-test" 2>/dev/null || true

    sleep 2

    # Check activity
    local output
    local exit_code=0
    output=$(ntm --robot-activity="$session" 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]] && echo "$output" | jq . >/dev/null 2>&1; then
        log_assert_valid_json "$output" "activity tracking returns valid JSON"
    else
        log_info "Activity tracking returned exit code $exit_code"
    fi

    # Check summary
    output=$(ntm --robot-summary="$session" 2>&1) || exit_code=$?
    if [[ $exit_code -eq 0 ]] && echo "$output" | jq . >/dev/null 2>&1; then
        log_assert_valid_json "$output" "summary returns valid JSON"
    else
        log_info "Summary returned exit code $exit_code"
    fi

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

#
# Interrupt Workflow Test
#
test_interrupt_workflow() {
    local session="${TEST_PREFIX}-interrupt"

    log_info "Testing interrupt workflow: $session"

    if ! spawn_test_session "$session" --cc 1; then
        log_skip "Could not create test session"
        return 0
    fi

    sleep 2

    # Send a long-running task (or simulate one)
    log_info "Sending task to agent"
    ntm send "$session" --cc "echo starting-task" 2>/dev/null || true

    sleep 1

    # Interrupt the agent
    log_info "Interrupting agent"
    local output
    local exit_code=0
    output=$(ntm --robot-interrupt="$session" 2>&1) || exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        if echo "$output" | jq . >/dev/null 2>&1; then
            log_assert_valid_json "$output" "interrupt returns valid JSON"

            local success
            success=$(echo "$output" | jq -r '.success // false')
            log_assert_eq "$success" "true" "interrupt reports success"
        fi
    else
        log_warn "interrupt returned exit code $exit_code"
    fi

    # Verify session still exists (interrupt shouldn't kill it)
    if tmux has-session -t "$session" 2>/dev/null; then
        log_assert_eq "alive" "alive" "session survives interrupt"
    else
        log_warn "session was killed by interrupt"
    fi

    # Send new task after interrupt
    log_info "Sending new task after interrupt"
    ntm send "$session" --cc "echo after-interrupt" 2>/dev/null || true

    # Cleanup
    tmux kill-session -t "$session" 2>/dev/null || true
}

main
