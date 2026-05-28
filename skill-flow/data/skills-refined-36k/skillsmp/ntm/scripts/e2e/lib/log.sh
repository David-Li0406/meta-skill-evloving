#!/usr/bin/env bash
# E2E Test JSON Logging Library
# Provides structured JSON logging for shell-based E2E tests.
#
# Usage:
#   source lib/log.sh
#   log_init "test-spawn"
#   log_info "Starting test"
#   log_section "Setup"
#   log_exec ntm spawn test-session --cc 2
#   log_assert_eq "$actual" "$expected" "values match"
#   log_summary

set -euo pipefail

# Global state
_LOG_TEST_NAME=""
_LOG_START_TS=""
_LOG_FILE=""
_LOG_RESULTS=()
_LOG_PASS_COUNT=0
_LOG_FAIL_COUNT=0
_LOG_SKIP_COUNT=0

# Get ISO 8601 timestamp
_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Get milliseconds since test start
_elapsed_ms() {
    local now
    now=$(date +%s)
    echo $(( (now - _LOG_START_TS) * 1000 ))
}

# Get timestamp in milliseconds (cross-platform)
_millis() {
    # Try GNU date first, fall back to seconds * 1000 on macOS
    if date +%s%3N 2>/dev/null | grep -qE '^[0-9]+$'; then
        date +%s%3N
    else
        echo "$(($(date +%s) * 1000))"
    fi
}

# Escape JSON string
_json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\r'/\\r}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

# Initialize logging for a test
# Usage: log_init "test-name"
log_init() {
    _LOG_TEST_NAME="$1"
    _LOG_START_TS=$(date +%s)
    _LOG_RESULTS=()
    _LOG_PASS_COUNT=0
    _LOG_FAIL_COUNT=0
    _LOG_SKIP_COUNT=0

    local log_dir="${E2E_LOG_DIR:-$(dirname "$0")/logs}"
    mkdir -p "$log_dir"

    local safe_name="${_LOG_TEST_NAME//\//_}"
    _LOG_FILE="${log_dir}/${safe_name}_$(date +%Y%m%d_%H%M%S).jsonl"

    _log_entry "test_start" "{\"test\":\"$(_json_escape "$_LOG_TEST_NAME")\"}"

    # Also print to stderr for visibility
    echo "=== E2E TEST: $_LOG_TEST_NAME ===" >&2
    echo "Log file: $_LOG_FILE" >&2
}

# Internal: write a log entry
_log_entry() {
    local level="$1"
    local data="$2"
    local ts
    ts=$(_timestamp)
    local elapsed
    elapsed=$(_elapsed_ms)

    local entry="{\"timestamp\":\"$ts\",\"elapsed_ms\":$elapsed,\"level\":\"$level\",\"test\":\"$(_json_escape "$_LOG_TEST_NAME")\",$data}"
    echo "$entry" >> "$_LOG_FILE"
}

# Log info message
log_info() {
    local msg="$1"
    _log_entry "info" "\"message\":\"$(_json_escape "$msg")\""
    echo "[INFO] $msg" >&2
}

# Log warning message
log_warn() {
    local msg="$1"
    _log_entry "warn" "\"message\":\"$(_json_escape "$msg")\""
    echo "[WARN] $msg" >&2
}

# Log error message
log_error() {
    local msg="$1"
    _log_entry "error" "\"message\":\"$(_json_escape "$msg")\""
    echo "[ERROR] $msg" >&2
}

# Log debug message (only if E2E_DEBUG=1)
log_debug() {
    local msg="$1"
    if [[ "${E2E_DEBUG:-0}" == "1" ]]; then
        _log_entry "debug" "\"message\":\"$(_json_escape "$msg")\""
        echo "[DEBUG] $msg" >&2
    fi
}

# Log section header
log_section() {
    local name="$1"
    _log_entry "section" "\"section\":\"$(_json_escape "$name")\""
    echo "" >&2
    echo "--- $name ---" >&2
}

# Execute a command and log it
# Usage: log_exec command args...
# Returns the command's exit code
log_exec() {
    local cmd=("$@")
    local cmd_str="${cmd[*]}"
    local start_ts
    start_ts=$(_millis)

    _log_entry "exec_start" "\"command\":\"$(_json_escape "$cmd_str")\""
    echo "[EXEC] $cmd_str" >&2

    local output
    local exit_code=0
    output=$("${cmd[@]}" 2>&1) || exit_code=$?

    local end_ts
    end_ts=$(_millis)
    local duration_ms=$((end_ts - start_ts))

    # Truncate very long output for the log
    local log_output="$output"
    if [[ ${#log_output} -gt 2000 ]]; then
        log_output="${log_output:0:2000}...(truncated)"
    fi

    _log_entry "exec_end" "\"command\":\"$(_json_escape "$cmd_str")\",\"exit_code\":$exit_code,\"duration_ms\":$duration_ms,\"output\":\"$(_json_escape "$log_output")\""

    if [[ $exit_code -eq 0 ]]; then
        echo "[EXIT] success (0)" >&2
    else
        echo "[EXIT] failed ($exit_code)" >&2
    fi

    # Store output in global for caller to use
    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    return $exit_code
}

# Get last command output
get_last_output() {
    echo "$_LAST_OUTPUT"
}

# Get last exit code
get_last_exit_code() {
    echo "$_LAST_EXIT_CODE"
}

# Assert equality
# Usage: log_assert_eq "$actual" "$expected" "description"
log_assert_eq() {
    local actual="$1"
    local expected="$2"
    local desc="$3"

    if [[ "$actual" == "$expected" ]]; then
        _log_entry "assert" "\"type\":\"eq\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"pass\",\"actual\":\"$(_json_escape "$actual")\",\"expected\":\"$(_json_escape "$expected")\""
        echo "[PASS] $desc" >&2
        ((_LOG_PASS_COUNT++)) || true
        return 0
    else
        _log_entry "assert" "\"type\":\"eq\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"fail\",\"actual\":\"$(_json_escape "$actual")\",\"expected\":\"$(_json_escape "$expected")\""
        echo "[FAIL] $desc (got: $actual, expected: $expected)" >&2
        ((_LOG_FAIL_COUNT++)) || true
        return 1
    fi
}

# Assert not empty
# Usage: log_assert_not_empty "$value" "description"
log_assert_not_empty() {
    local value="$1"
    local desc="$2"

    if [[ -n "$value" ]]; then
        _log_entry "assert" "\"type\":\"not_empty\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"pass\""
        echo "[PASS] $desc (not empty)" >&2
        ((_LOG_PASS_COUNT++)) || true
        return 0
    else
        _log_entry "assert" "\"type\":\"not_empty\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"fail\""
        echo "[FAIL] $desc (was empty)" >&2
        ((_LOG_FAIL_COUNT++)) || true
        return 1
    fi
}

# Assert contains substring
# Usage: log_assert_contains "$haystack" "$needle" "description"
log_assert_contains() {
    local haystack="$1"
    local needle="$2"
    local desc="$3"

    if [[ "$haystack" == *"$needle"* ]]; then
        _log_entry "assert" "\"type\":\"contains\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"pass\",\"needle\":\"$(_json_escape "$needle")\""
        echo "[PASS] $desc" >&2
        ((_LOG_PASS_COUNT++)) || true
        return 0
    else
        _log_entry "assert" "\"type\":\"contains\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"fail\",\"needle\":\"$(_json_escape "$needle")\""
        echo "[FAIL] $desc (substring not found: $needle)" >&2
        ((_LOG_FAIL_COUNT++)) || true
        return 1
    fi
}

# Assert command succeeds
# Usage: log_assert_success command args...
log_assert_success() {
    local desc="command succeeds: $*"

    if log_exec "$@"; then
        _log_entry "assert" "\"type\":\"success\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"pass\""
        echo "[PASS] $desc" >&2
        ((_LOG_PASS_COUNT++)) || true
        return 0
    else
        _log_entry "assert" "\"type\":\"success\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"fail\",\"exit_code\":$_LAST_EXIT_CODE"
        echo "[FAIL] $desc (exit code: $_LAST_EXIT_CODE)" >&2
        ((_LOG_FAIL_COUNT++)) || true
        return 1
    fi
}

# Assert command fails
# Usage: log_assert_fails command args...
log_assert_fails() {
    local desc="command fails: $*"

    if ! log_exec "$@"; then
        _log_entry "assert" "\"type\":\"fails\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"pass\",\"exit_code\":$_LAST_EXIT_CODE"
        echo "[PASS] $desc (exited with $_LAST_EXIT_CODE as expected)" >&2
        ((_LOG_PASS_COUNT++)) || true
        return 0
    else
        _log_entry "assert" "\"type\":\"fails\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"fail\""
        echo "[FAIL] $desc (expected failure but got success)" >&2
        ((_LOG_FAIL_COUNT++)) || true
        return 1
    fi
}

# Assert JSON is valid
# Usage: log_assert_valid_json "$json" "description"
log_assert_valid_json() {
    local json="$1"
    local desc="$2"

    if echo "$json" | jq . >/dev/null 2>&1; then
        _log_entry "assert" "\"type\":\"valid_json\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"pass\""
        echo "[PASS] $desc (valid JSON)" >&2
        ((_LOG_PASS_COUNT++)) || true
        return 0
    else
        _log_entry "assert" "\"type\":\"valid_json\",\"description\":\"$(_json_escape "$desc")\",\"result\":\"fail\""
        echo "[FAIL] $desc (invalid JSON)" >&2
        ((_LOG_FAIL_COUNT++)) || true
        return 1
    fi
}

# Assert JSON field equals value
# Usage: log_assert_json_eq "$json" ".field" "expected" "description"
log_assert_json_eq() {
    local json="$1"
    local path="$2"
    local expected="$3"
    local desc="$4"

    local actual
    actual=$(echo "$json" | jq -r "$path" 2>/dev/null) || actual=""

    log_assert_eq "$actual" "$expected" "$desc"
}

# Skip a test with reason
log_skip() {
    local reason="$1"
    _log_entry "skip" "\"reason\":\"$(_json_escape "$reason")\""
    echo "[SKIP] $reason" >&2
    ((_LOG_SKIP_COUNT++)) || true
}

# Write test summary and return appropriate exit code
log_summary() {
    local total=$((_LOG_PASS_COUNT + _LOG_FAIL_COUNT + _LOG_SKIP_COUNT))
    local end_ts
    end_ts=$(_timestamp)
    local duration_ms
    duration_ms=$(_elapsed_ms)

    local result="pass"
    if [[ $_LOG_FAIL_COUNT -gt 0 ]]; then
        result="fail"
    fi

    _log_entry "test_end" "\"result\":\"$result\",\"total\":$total,\"passed\":$_LOG_PASS_COUNT,\"failed\":$_LOG_FAIL_COUNT,\"skipped\":$_LOG_SKIP_COUNT,\"duration_ms\":$duration_ms"

    echo "" >&2
    echo "=== TEST SUMMARY: $_LOG_TEST_NAME ===" >&2
    echo "Result: $result" >&2
    echo "Passed: $_LOG_PASS_COUNT" >&2
    echo "Failed: $_LOG_FAIL_COUNT" >&2
    echo "Skipped: $_LOG_SKIP_COUNT" >&2
    echo "Duration: ${duration_ms}ms" >&2
    echo "Log: $_LOG_FILE" >&2

    # Output final JSON summary to stdout (for CI parsing)
    cat <<EOF
{"test":"$(_json_escape "$_LOG_TEST_NAME")","result":"$result","passed":$_LOG_PASS_COUNT,"failed":$_LOG_FAIL_COUNT,"skipped":$_LOG_SKIP_COUNT,"duration_ms":$duration_ms,"log_file":"$(_json_escape "$_LOG_FILE")"}
EOF

    if [[ $_LOG_FAIL_COUNT -gt 0 ]]; then
        return 1
    fi
    return 0
}

# Cleanup helper - kills sessions matching pattern
# Usage: cleanup_sessions "test-*"
cleanup_sessions() {
    local pattern="$1"
    log_debug "Cleaning up sessions matching: $pattern"

    local sessions
    sessions=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E "^${pattern}" || true)

    for session in $sessions; do
        log_debug "Killing session: $session"
        tmux kill-session -t "$session" 2>/dev/null || true
    done
}

# Wait for condition with timeout
# Usage: wait_for timeout_seconds "description" command args...
wait_for() {
    local timeout="$1"
    local desc="$2"
    shift 2

    log_debug "Waiting up to ${timeout}s for: $desc"

    local start
    start=$(date +%s)
    local deadline=$((start + timeout))
    local attempt=0

    while [[ $(date +%s) -lt $deadline ]]; do
        ((attempt++)) || true
        if "$@" >/dev/null 2>&1; then
            log_debug "Condition met after $attempt attempts"
            return 0
        fi
        sleep 0.5
    done

    log_warn "Timeout waiting for: $desc (after $attempt attempts)"
    return 1
}

# Check if ntm binary is available
require_ntm() {
    if ! command -v ntm &>/dev/null; then
        log_error "ntm binary not found in PATH"
        exit 1
    fi
    log_debug "ntm binary found: $(command -v ntm)"
}

# Check if tmux is available
require_tmux() {
    if ! command -v tmux &>/dev/null; then
        log_error "tmux not installed"
        exit 1
    fi
    log_debug "tmux found: $(tmux -V)"
}

# Check if jq is available
require_jq() {
    if ! command -v jq &>/dev/null; then
        log_error "jq not installed"
        exit 1
    fi
    log_debug "jq found: $(jq --version)"
}

# Spawn an ntm session, auto-answering directory creation prompts
# Usage: ntm_spawn session_name [args...]
# Returns: 0 on success, 1 on failure
ntm_spawn() {
    local session="$1"
    shift
    local args=("$@")

    log_debug "Spawning session: $session with args: ${args[*]}"

    # Pipe 'y' to auto-create directory if needed
    local output
    local exit_code=0
    output=$(echo "y" | ntm spawn "$session" "${args[@]}" 2>&1) || exit_code=$?

    _LAST_OUTPUT="$output"
    _LAST_EXIT_CODE=$exit_code

    if [[ $exit_code -eq 0 ]]; then
        log_debug "Session $session spawned successfully"
    else
        log_debug "Session $session spawn failed: $output"
    fi

    return $exit_code
}

# Kill an ntm session and clean up created directory if it's a test session
# Usage: ntm_cleanup session_name
ntm_cleanup() {
    local session="$1"

    log_debug "Cleaning up session: $session"

    # Kill the tmux session
    tmux kill-session -t "$session" 2>/dev/null || true

    # If it's a test session, clean up the created directory
    # Only clean up if it's in a temp-like location or matches test pattern
    if [[ "$session" == e2e-* || "$session" == test-* ]]; then
        local potential_dir="/Users/jemanuel/projects/$session"
        if [[ -d "$potential_dir" ]]; then
            log_debug "Removing test directory: $potential_dir"
            rm -rf "$potential_dir" 2>/dev/null || true
        fi
    fi
}
