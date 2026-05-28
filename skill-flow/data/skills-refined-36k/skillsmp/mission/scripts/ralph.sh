#!/bin/bash
# ============================================================================
# Ralph - Space-Agents Execution Loop (Beads Edition)
# ============================================================================
# Named after the "Ralph Wiggum Loop" pattern: fresh agent spawned each cycle,
# state persists in Beads. Agents are compute, not memory.
#
# Usage:
#   ./ralph.sh <feature_id> [--visible]
#
# Exit codes:
#   0 - Feature complete (all tasks done)
#   1 - Feature failed (critical bug)
#   2 - Configuration error (Beads not initialized, feature not found, etc.)
# ============================================================================

set -euo pipefail

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Script location for finding sibling scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Visible mode flag (set by --visible-internal when launched from mprocs)
VISIBLE_MODE=false

# Find project root (directory containing .beads)
PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
BEADS_DIR="${PROJECT_ROOT}/.beads"
SPACE_AGENTS_DIR="${PROJECT_ROOT}/.space-agents"
NOTIFICATIONS_FILE="${SPACE_AGENTS_DIR}/comms/notifications.md"
NOTIFY_SCRIPT="${SPACE_AGENTS_DIR}/scripts/notify.sh"

# Colors for terminal output (attended mode)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ----------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------

log() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    case "$level" in
        INFO)    echo -e "${BLUE}[$timestamp]${NC} $message" ;;
        SUCCESS) echo -e "${GREEN}[$timestamp]${NC} $message" ;;
        WARNING) echo -e "${YELLOW}[$timestamp]${NC} $message" ;;
        ERROR)   echo -e "${RED}[$timestamp]${NC} $message" ;;
        *)       echo "[$timestamp] $message" ;;
    esac
}

log_capcom() {
    local feature_id="$1"
    local message="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local capcom_log="${SPACE_AGENTS_DIR}/comms/capcom.md"

    # Ensure directory exists
    mkdir -p "$(dirname "$capcom_log")"

    echo "[$timestamp] RALPH: $message" >> "$capcom_log"
}

# ----------------------------------------------------------------------------
# Safety Checks
# ----------------------------------------------------------------------------

check_prerequisites() {
    # Check .beads directory exists
    if [[ ! -d "$BEADS_DIR" ]]; then
        log ERROR "Beads directory not found: $BEADS_DIR"
        log ERROR "Run 'bd init' first to initialize Beads"
        exit 2
    fi

    # Check bd CLI is available
    if ! command -v bd &> /dev/null; then
        log ERROR "bd command not found. Please install Beads CLI."
        exit 2
    fi

    # Check claude CLI is available
    if ! command -v claude &> /dev/null; then
        log ERROR "claude CLI not found. Please install Claude Code CLI."
        exit 2
    fi
}

check_feature() {
    local feature_id="$1"

    # Check feature exists and get its status
    local feature_json
    feature_json=$(bd show "$feature_id" --json 2>/dev/null) || {
        log ERROR "Feature not found: $feature_id"
        exit 2
    }

    # Extract status from JSON (simple grep, no jq)
    local feature_status
    feature_status=$(echo "$feature_json" | grep -o '"status": *"[^"]*"' | head -1 | cut -d'"' -f4)

    if [[ -z "$feature_status" ]]; then
        log ERROR "Could not determine feature status: $feature_id"
        exit 2
    fi

    # Check feature is open or in_progress
    if [[ "$feature_status" != "open" ]] && [[ "$feature_status" != "in_progress" ]]; then
        log ERROR "Feature is not active (status: $feature_status)"
        log ERROR "Only open or in_progress features can be executed"
        exit 2
    fi

    log INFO "Feature validated: $feature_id (status: $feature_status)"
}

# ----------------------------------------------------------------------------
# Notification Functions
# ----------------------------------------------------------------------------

send_notification() {
    local title="$1"
    local message="$2"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Ensure notifications directory exists
    mkdir -p "$(dirname "$NOTIFICATIONS_FILE")"

    # Write to notifications file (for in-session pickup via hooks)
    echo "[$timestamp] $title: $message" >> "$NOTIFICATIONS_FILE"

    # Try macOS notification if notify.sh exists
    if [[ -x "$NOTIFY_SCRIPT" ]]; then
        "$NOTIFY_SCRIPT" "$title" "$message" 2>/dev/null || true
    else
        # Fallback: direct osascript if on macOS
        if command -v osascript &> /dev/null; then
            osascript -e "display notification \"$message\" with title \"$title\"" 2>/dev/null || true
        fi
    fi
}

# ----------------------------------------------------------------------------
# Signal File Infrastructure
# ----------------------------------------------------------------------------

create_signal_dir() {
    local feature_id="$1"
    local signal_dir="${SPACE_AGENTS_DIR}/tmp/${feature_id}/signals"
    mkdir -p "$signal_dir"
    echo "$signal_dir"
}

wait_for_signal() {
    local signal_file="$1"
    local timeout="${2:-300}"
    local waited=0

    while [[ ! -f "$signal_file" ]] && [[ $waited -lt $timeout ]]; do
        sleep 2
        waited=$((waited + 2))
    done

    [[ -f "$signal_file" ]]
}

cleanup_signals() {
    local feature_id="$1"
    local signal_dir="${SPACE_AGENTS_DIR}/tmp/${feature_id}/signals"
    rm -rf "$signal_dir"
}

# ----------------------------------------------------------------------------
# Task Management (Beads)
# ----------------------------------------------------------------------------

get_next_task() {
    local feature_id="$1"

    # Get next ready task under this feature
    # bd ready returns only unblocked issues
    local ready_tasks
    ready_tasks=$(bd ready -t task --json 2>/dev/null) || {
        log ERROR "bd ready failed"
        return 1
    }

    # Find first task whose ID starts with feature_id (hierarchical naming)
    # Extract IDs and titles using grep on the flat JSON output
    local task_id=""
    local task_title=""

    # Get all IDs from the JSON
    while IFS= read -r line; do
        if [[ "$line" =~ \"id\":\ *\"([^\"]+)\" ]]; then
            local current_id="${BASH_REMATCH[1]}"
            # Check if this ID starts with our feature ID
            if [[ "$current_id" == "${feature_id}."* ]]; then
                task_id="$current_id"
            fi
        elif [[ -n "$task_id" ]] && [[ "$line" =~ \"title\":\ *\"([^\"]+)\" ]]; then
            task_title="${BASH_REMATCH[1]}"
            echo "${task_id}|${task_title}|"
            return 0
        fi
    done <<< "$ready_tasks"

    # No task found
    return 0
}

mark_task_in_progress() {
    local task_id="$1"

    bd update "$task_id" --status in_progress || {
        log ERROR "Failed to mark task in_progress: $task_id"
        return 1
    }
}

mark_task_complete() {
    local task_id="$1"

    bd close "$task_id" --reason "Completed by Ralph" || {
        log ERROR "Failed to close task: $task_id"
        return 1
    }

    # Sync changes
    bd sync || log WARNING "bd sync failed (will retry later)"
}

mark_task_failed() {
    local task_id="$1"
    local reason="${2:-Task failed}"
    local feature_id="$3"

    # Beads has no "failed" status. Create a blocking bug instead.
    local bug_id
    bug_id=$(bd create "BLOCKER: $reason" -t bug --parent "$feature_id" 2>&1 | grep -o 'Created issue: [^ ]*' | cut -d' ' -f3) || {
        log ERROR "Failed to create blocking bug"
        return 1
    }

    # Link bug as blocker for the task
    bd dep add "$task_id" "$bug_id" || {
        log ERROR "Failed to link bug as blocker"
        return 1
    }

    log WARNING "Created blocking bug: $bug_id"

    # Sync changes
    bd sync || log WARNING "bd sync failed (will retry later)"
}

get_feature_info() {
    local feature_id="$1"

    # Returns: feature title
    local feature_json
    feature_json=$(bd show "$feature_id" --json 2>/dev/null) || {
        echo "Unknown Feature"
        return
    }

    echo "$feature_json" | grep -o '"title": *"[^"]*"' | head -1 | cut -d'"' -f4
}

check_feature_complete() {
    local feature_id="$1"

    # Check if any tasks under this feature are still open/in_progress
    # Filter by ID prefix (hierarchical: feature.1, feature.2, etc.)
    local open_output in_progress_output
    open_output=$(bd list -t task --status open --json 2>/dev/null || echo "[]")
    in_progress_output=$(bd list -t task --status in_progress --json 2>/dev/null || echo "[]")

    local open_tasks in_progress_tasks
    open_tasks=$(echo "$open_output" | grep -c "\"id\": *\"${feature_id}\." 2>/dev/null || true)
    in_progress_tasks=$(echo "$in_progress_output" | grep -c "\"id\": *\"${feature_id}\." 2>/dev/null || true)

    # Ensure valid numbers
    open_tasks=${open_tasks:-0}
    open_tasks=${open_tasks//[^0-9]/}
    [[ -z "$open_tasks" ]] && open_tasks=0

    in_progress_tasks=${in_progress_tasks:-0}
    in_progress_tasks=${in_progress_tasks//[^0-9]/}
    [[ -z "$in_progress_tasks" ]] && in_progress_tasks=0

    [[ "$open_tasks" -eq 0 ]] && [[ "$in_progress_tasks" -eq 0 ]]
}

mark_feature_complete() {
    local feature_id="$1"

    bd close "$feature_id" --reason "All tasks completed" || {
        log ERROR "Failed to close feature: $feature_id"
        return 1
    }

    # Sync changes
    bd sync || log WARNING "bd sync failed (will retry later)"
}

check_critical_bugs() {
    local feature_id="$1"

    # Check for any open bugs with severity:critical label under this feature
    local bug_output
    bug_output=$(bd list -t bug --status open --json 2>/dev/null || echo "[]")

    local critical_count
    critical_count=$(echo "$bug_output" | grep -c '"severity:critical"' 2>/dev/null || true)

    # Ensure we have a valid number
    critical_count=${critical_count:-0}
    critical_count=${critical_count//[^0-9]/}
    [[ -z "$critical_count" ]] && critical_count=0

    [[ "$critical_count" -gt 0 ]]
}

# ----------------------------------------------------------------------------
# Bug Creation
# ----------------------------------------------------------------------------

create_bug() {
    local severity="$1"
    local feature_id="$2"
    local task_id="$3"
    local source="$4"
    local description="$5"

    local severity_label="severity:info"
    case "$severity" in
        0) severity_label="severity:critical" ;;
        1) severity_label="severity:blocker" ;;
        2) severity_label="severity:warning" ;;
        3) severity_label="severity:info" ;;
    esac

    local bug_id
    bug_id=$(bd create "[$source] $description" -t bug --parent "$feature_id" --label "$severity_label" 2>&1 | grep -o 'Created issue: [^ ]*' | cut -d' ' -f3) || {
        log ERROR "Failed to create bug"
        return 1
    }

    # If task_id provided, link bug as blocker
    if [[ -n "$task_id" ]]; then
        bd dep add "$task_id" "$bug_id" || log WARNING "Failed to link bug to task"
    fi

    log WARNING "Bug created: $bug_id ($severity_label) - $description"

    # Sync changes
    bd sync || log WARNING "bd sync failed (will retry later)"
}

# ----------------------------------------------------------------------------
# Pod Spawning
# ----------------------------------------------------------------------------

spawn_pod_visible() {
    local task_id="$1"
    local pod_prompt="$2"
    local pod_agent="$3"
    local feature_id="$4"
    local tmp_dir="${SPACE_AGENTS_DIR}/tmp/${feature_id}"
    local signal_dir="${tmp_dir}/signals"

    # Ensure tmp directories exist
    mkdir -p "$signal_dir"

    # Write prompt to file (avoids quoting issues with mprocs)
    local prompt_file="${tmp_dir}/prompts/${task_id}.txt"
    mkdir -p "$(dirname "$prompt_file")"
    echo "$pod_prompt" > "$prompt_file"

    # Build claude command (escape quotes for JSON)
    local cmd
    if [[ -f "$pod_agent" ]]; then
        cmd="cd ${PROJECT_ROOT} && claude --dangerously-skip-permissions --system-prompt \\\"\$(cat ${pod_agent})\\\" \\\"\$(cat ${prompt_file})\\\""
    else
        cmd="cd ${PROJECT_ROOT} && claude --dangerously-skip-permissions \\\"\$(cat ${prompt_file})\\\""
    fi

    # Spawn via mprocs ctl (connect to server started by ralph-visible.sh)
    log INFO "Adding Pod to mprocs: Pod-${task_id}"
    mprocs --server 127.0.0.1:4050 --ctl "{\"c\": \"add-proc\", \"cmd\": \"$cmd\", \"name\": \"Pod-${task_id}\"}"

    # Wait for signal file
    local signal_file="${signal_dir}/${task_id}.done"
    log INFO "Waiting for Pod completion signal: ${signal_file}"

    if wait_for_signal "$signal_file" 600; then
        log SUCCESS "Pod signaled completion"
        rm -f "$signal_file"
        return 0
    else
        log ERROR "Pod timed out (10 min) waiting for signal"
        return 1
    fi
}

spawn_pod() {
    local task_id="$1"
    local task_title="$2"
    local task_description="$3"
    local feature_id="$4"

    log INFO "Spawning Pod for task: $task_title"

    # Simple prompt that invokes the /pod skill
    # The skill handles context loading, crew dispatch, and handover
    local pod_prompt="Run /mission-pod ${task_id} ${feature_id}"

    local exit_code=0

    if [[ "$VISIBLE_MODE" == "true" ]]; then
        # Visible mode: spawn via mprocs, wait for signal
        spawn_pod_visible "$task_id" "$pod_prompt" "" "$feature_id" || exit_code=$?
    else
        # Headless mode: run claude with the prompt
        echo "$pod_prompt" | claude -p --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Task,Skill" 2>&1 || exit_code=$?
    fi

    return $exit_code
}

# ----------------------------------------------------------------------------
# Main Execution Loop
# ----------------------------------------------------------------------------

main() {
    local feature_id=""
    local visible_flag=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --visible)
                visible_flag=true
                shift
                ;;
            --visible-internal)
                # Called by ralph-visible.sh, already inside mprocs
                VISIBLE_MODE=true
                shift
                ;;
            --attended)
                # Legacy flag, kept for backward compatibility
                shift
                ;;
            -*)
                echo "Unknown option: $1"
                exit 2
                ;;
            *)
                if [[ -z "$feature_id" ]]; then
                    feature_id="$1"
                fi
                shift
                ;;
        esac
    done

    # Validate arguments
    if [[ -z "$feature_id" ]]; then
        echo "Usage: ralph.sh <feature_id> [--visible]"
        echo ""
        echo "Options:"
        echo "  feature_id   The Beads ID of the feature to execute"
        echo "  --visible    Run in visible mode (mprocs TUI for real-time pod visibility)"
        exit 2
    fi

    # If --visible and not already internal, launch wrapper
    if [[ "$visible_flag" == "true" ]] && [[ "$VISIBLE_MODE" != "true" ]]; then
        exec "${SCRIPT_DIR}/ralph-visible.sh" "$feature_id"
    fi

    # Set global FEATURE_ID for use by helper functions
    FEATURE_ID="$feature_id"

    # Run prerequisites
    check_prerequisites
    check_feature "$FEATURE_ID"

    # Mark feature as in_progress
    bd update "$FEATURE_ID" --status in_progress 2>/dev/null || true

    # Get feature info for logging
    local feature_title
    feature_title=$(get_feature_info "$feature_id")

    log INFO "============================================"
    log INFO "RALPH LOOP STARTING"
    log INFO "============================================"
    log INFO "Feature: $feature_title ($feature_id)"
    log INFO "============================================"

    log_capcom "$feature_id" "Ralph loop starting"

    local iteration=0
    local max_iterations=100  # Safety limit

    # Main execution loop
    while true; do
        iteration=$((iteration + 1))

        # Safety: prevent infinite loops
        if [[ $iteration -gt $max_iterations ]]; then
            log ERROR "Max iterations ($max_iterations) reached. Halting."
            create_bug 0 "$feature_id" "" "Ralph" "Max iterations reached - possible infinite loop"
            send_notification "Space-Agents" "Ralph halted: max iterations reached"
            exit 1
        fi

        log INFO "--- Iteration $iteration ---"

        # Check for critical bugs before continuing
        if check_critical_bugs "$feature_id"; then
            log ERROR "Critical bug detected. Halting Ralph loop."
            log_capcom "$feature_id" "Ralph halted: critical bug detected"
            send_notification "Space-Agents CRITICAL" "Feature halted due to critical bug"
            exit 1
        fi

        # Get next ready task
        local task_row
        task_row=$(get_next_task "$feature_id")

        # Check if queue is empty
        if [[ -z "$task_row" ]]; then
            log INFO "No ready tasks remaining"

            # Check if feature is complete
            if check_feature_complete "$feature_id"; then
                mark_feature_complete "$feature_id"
                log SUCCESS "============================================"
                log SUCCESS "FEATURE COMPLETE: $feature_title"
                log SUCCESS "============================================"
                log_capcom "$feature_id" "Feature complete: $feature_id"
                send_notification "Space-Agents" "Feature complete: $feature_title"
                exit 0
            else
                # Some tasks may be blocked
                log WARNING "No ready tasks, but feature not fully complete"
                log WARNING "Check blocked tasks and bugs"
                log_capcom "$feature_id" "Ralph stopped: no ready tasks, some may be blocked"
                send_notification "Space-Agents" "Feature stalled: check blocked tasks"
                exit 1
            fi
        fi

        # Parse task data
        local task_id task_title task_description
        IFS='|' read -r task_id task_title task_description <<< "$task_row"

        log INFO "Selected task: $task_title ($task_id)"
        log_capcom "$feature_id" "Starting task: $task_id - $task_title"

        # Mark task as in_progress
        mark_task_in_progress "$task_id"

        # Spawn Pod for this task
        local pod_exit_code=0
        spawn_pod "$task_id" "$task_title" "$task_description" "$feature_id" || pod_exit_code=$?

        # Handle Pod exit code
        case $pod_exit_code in
            0)
                # Success
                log SUCCESS "Pod completed task: $task_title"
                mark_task_complete "$task_id"
                log_capcom "$feature_id" "Task complete: $task_id"
                ;;
            1)
                # Blocker - task failed, but try next
                log WARNING "Pod reported blocker for: $task_title"
                mark_task_failed "$task_id" "Pod reported blocker" "$feature_id"
                log_capcom "$feature_id" "Task blocked: $task_id"
                log INFO "Continuing to next task..."
                ;;
            2)
                # Critical - halt the loop
                log ERROR "Pod reported CRITICAL failure for: $task_title"
                create_bug 0 "$feature_id" "$task_id" "Pod" "Critical failure - Ralph loop halted"
                log_capcom "$feature_id" "CRITICAL: Ralph halted at task $task_id"
                send_notification "Space-Agents CRITICAL" "Feature halted: $task_title"
                exit 1
                ;;
            *)
                # Unknown exit code - treat as blocker
                log WARNING "Pod exited with unexpected code: $pod_exit_code"
                mark_task_failed "$task_id" "Unexpected exit code: $pod_exit_code" "$feature_id"
                log_capcom "$feature_id" "Task blocked (exit $pod_exit_code): $task_id"
                log INFO "Continuing to next task..."
                ;;
        esac

        # Brief pause between iterations (prevents hammering)
        sleep 2
    done
}

# ----------------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------------

main "$@"
