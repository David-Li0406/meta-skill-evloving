#!/bin/bash
#
# analyze-sessions.sh — Analyze pi agent session logs for patterns and summaries
#
# This script is intentionally general-purpose:
# - It can filter to a time window (last N hours)
# - It can restrict by project name (derived from session path)
# - It can restrict to sessions that used a particular tool
# - It can summarize tool usage and other basic counts
#
# Usage:
#   ./analyze-sessions.sh --hours 24 --pattern "rp_exec"
#   ./analyze-sessions.sh --hours 36 --edit-diagnostics
#   ./analyze-sessions.sh --hours 48 --tool-errors
#   ./analyze-sessions.sh --hours 24 --report
#   ./analyze-sessions.sh --hours 24 --tool-stats
#

set -e

SESSIONS_DIR="${SESSIONS_DIR:-$HOME/dot314/agent/sessions}"
HOURS=24
PATTERN=""
PROJECT_FILTER=""
TOOL_FILTER=""
MODE="search"

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  --hours N            Look back N hours (default: 24)
  --pattern REGEX      Only include sessions containing REGEX (and rank by match count)
  --project NAME       Only include sessions whose path encodes project NAME
  --tool TOOLNAME      Only include sessions that contain tool TOOLNAME ("toolName":"TOOLNAME")

Modes:
  --list               List matching session files (with size/entry counts)
  --edit-diagnostics   Summarize edit-related activity + notable signals
  --tool-errors        Show sessions with toolResult isError=true (alias: --errors)
  --tool-stats         Show tool usage counts (across matching sessions)
  --report             Compact multi-section report

Environment:
  SESSIONS_DIR         Override sessions directory (default: ~/dot314/agent/sessions)

Examples:
  $(basename "$0") --hours 36 --edit-diagnostics
  $(basename "$0") --hours 24 --pattern "apply_edits"
  $(basename "$0") --hours 48 --report --project pi-mono
  $(basename "$0") --hours 72 --tool-stats --tool rp_exec
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --hours)
            HOURS="$2"
            shift 2
            ;;
        --pattern)
            PATTERN="$2"
            MODE="pattern"
            shift 2
            ;;
        --project)
            PROJECT_FILTER="$2"
            shift 2
            ;;
        --tool)
            TOOL_FILTER="$2"
            shift 2
            ;;
        --edit-diagnostics)
            MODE="edit-diagnostics"
            shift
            ;;
        --tool-errors)
            MODE="tool-errors"
            shift
            ;;
        --errors)
            MODE="tool-errors"
            shift
            ;;
        --tool-stats)
            MODE="tool-stats"
            shift
            ;;
        --report)
            MODE="report"
            shift
            ;;
        --list)
            MODE="list"
            shift
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage
            exit 1
            ;;
    esac
done

MINUTES=$((HOURS * 60))

# Find session files within time window
find_sessions() {
    find "$SESSIONS_DIR" -type f -name "*.jsonl" -mmin -"$MINUTES" 2>/dev/null
}

# Project name is derived from session path convention:
#   .../--<project>--/...
project_from_path() {
    local file="$1"
    echo "$file" | sed 's|.*/--\([^/]*\)--/.*|\1|'
}

session_matches_filters() {
    local file="$1"

    if [[ -n "$PROJECT_FILTER" ]]; then
        local project
        project=$(project_from_path "$file")
        if [[ "$project" != "$PROJECT_FILTER" ]]; then
            return 1
        fi
    fi

    if [[ -n "$TOOL_FILTER" ]]; then
        if ! grep -q "\"toolName\":\"$TOOL_FILTER\"" "$file" 2>/dev/null; then
            return 1
        fi
    fi

    return 0
}

# Count pattern occurrences in a file
# Note: grep -c outputs 0 for no matches but exits with code 1, so we capture output and ignore exit code
count_pattern() {
    local file="$1"
    local pattern="$2"
    local count
    count=$(grep -c -E "$pattern" "$file" 2>/dev/null) || true
    echo "${count:-0}"
}

# Main modes

mode_list() {
    echo "=== Sessions from last $HOURS hours ==="
    find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi
        local size
        size=$(wc -c < "$f" | tr -d ' ')
        local lines
        lines=$(wc -l < "$f" | tr -d ' ')
        echo "$f (${lines} entries, ${size} bytes)"
    done | sort
}

mode_pattern() {
    echo "=== Sessions containing regex: $PATTERN ==="
    find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi
        if grep -q -E "$PATTERN" "$f" 2>/dev/null; then
            local count
            count=$(count_pattern "$f" "$PATTERN")
            echo "$f ($count matches)"
        fi
    done | sort -t'(' -k2 -rn
}

mode_edit_diagnostics() {
    echo "=== Edit Diagnostics (last $HOURS hours) ==="
    echo ""

    local edit_action_patterns="apply_edits|\"name\":\"Edit\"|\"toolName\":\"rp_exec\""

    # Signals often associated with edits not applying cleanly (string-level heuristics)
    local edit_outcome_patterns=(
        "search block not found"
        "0 edits applied"
        "no changes"
        "oldText.*not found"
        "didn.t match"
        "not match"
    )

    # Phrases that often indicate iteration/retry, without assuming intent
    local iteration_phrase_patterns=(
        "let me try"
        "try again"
        "different approach"
        "try another"
        "try smaller"
        "narrow it down"
    )

    local outcome_regex
    outcome_regex=$(IFS='|'; echo "${edit_outcome_patterns[*]}")

    local iteration_regex
    iteration_regex=$(IFS='|'; echo "${iteration_phrase_patterns[*]}")

    find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi

        local edit_action_count
        edit_action_count=$(count_pattern "$f" "$edit_action_patterns")

        local outcome_signal_count
        outcome_signal_count=$(count_pattern "$f" "$outcome_regex")

        local iteration_signal_count
        iteration_signal_count=$(count_pattern "$f" "$iteration_regex")

        # Show sessions with meaningful edit activity + at least one notable signal
        if [[ "$edit_action_count" -gt 3 && "$outcome_signal_count" -gt 0 ]] || [[ "$iteration_signal_count" -gt 2 ]]; then
            echo "----------------------------------------"
            echo "File: $f"
            echo "  Edit-related actions: $edit_action_count"
            echo "  Outcome signals: $outcome_signal_count"
            echo "  Iteration phrases: $iteration_signal_count"
            echo ""

            if [[ "$outcome_signal_count" -gt 0 ]]; then
                echo "  Outcome signal samples:"
                grep -o -E "$outcome_regex.{0,50}" "$f" 2>/dev/null | head -3 | sed 's/^/    /'
                echo ""
            fi
        fi
    done
}

mode_tool_errors() {
    echo "=== Sessions with toolResult isError=true (last $HOURS hours) ==="
    echo ""

    find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi

        local tool_errors
        tool_errors=$(count_pattern "$f" "\"isError\":true|\"isError\": true")

        if [[ "$tool_errors" -gt 0 ]]; then
            echo "$f"
            echo "  toolResult entries marked isError=true: $tool_errors"
            echo ""
        fi
    done
}

mode_tool_stats() {
    echo "=== Tool Usage Stats (last $HOURS hours) ==="
    echo ""

    local tmpfile
    tmpfile=$(mktemp)

    # Aggregate tool usage across matching sessions
    find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi
        grep -o '"toolName":"[^"]*"' "$f" 2>/dev/null
    done | sort | uniq -c | sort -rn > "$tmpfile"

    echo "Tool call counts:"
    head -20 "$tmpfile" | sed 's/^/  /'

    rm -f "$tmpfile"
}

mode_report() {
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║           Session Analysis Report — Last $HOURS hours              ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo ""

    local session_count
    session_count=$(find_sessions | while read -r f; do
        if session_matches_filters "$f"; then
            echo "$f"
        fi
    done | wc -l | tr -d ' ')

    local total_size
    total_size=$(find_sessions | while read -r f; do
        if session_matches_filters "$f"; then
            cat "$f"
        fi
    done 2>/dev/null | wc -c | tr -d ' ')

    local total_mb
    total_mb=$((total_size / 1024 / 1024))

    echo "Filters:"
    echo "  Sessions dir: $SESSIONS_DIR"
    echo "  Project: ${PROJECT_FILTER:-<any>}"
    echo "  Tool: ${TOOL_FILTER:-<any>}"
    echo ""

    echo "Summary:"
    echo "  Sessions: $session_count"
    echo "  Total size: ${total_mb}MB"
    echo ""

    echo "Sessions by project (top 10):"
    find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi
        project_from_path "$f"
    done | sort | uniq -c | sort -rn | head -10 | sed 's/^/  /'
    echo ""

    echo "Tool usage (top 20):"
    local tmpfile
    tmpfile=$(mktemp)
    find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi
        grep -o '"toolName":"[^"]*"' "$f" 2>/dev/null
    done | sort | uniq -c | sort -rn > "$tmpfile"
    head -20 "$tmpfile" | sed 's/^/  /'
    rm -f "$tmpfile"
    echo ""

    echo "toolResult isError=true (total count):"
    local error_total
    error_total=$(find_sessions | while read -r f; do
        if ! session_matches_filters "$f"; then
            continue
        fi
        count_pattern "$f" "\"isError\":true|\"isError\": true"
    done | awk '{sum+=$1}END{print sum+0}')
    echo "  $error_total"

    echo ""
    echo "════════════════════════════════════════════════════════════════════"
}

# Run selected mode
case $MODE in
    list)
        mode_list
        ;;
    pattern)
        mode_pattern
        ;;
    edit-diagnostics)
        mode_edit_diagnostics
        ;;
    tool-errors)
        mode_tool_errors
        ;;
    tool-stats)
        mode_tool_stats
        ;;
    report)
        mode_report
        ;;
    *)
        echo "No mode selected. Use --help for usage."
        exit 1
        ;;
esac
