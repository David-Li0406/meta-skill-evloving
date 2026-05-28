#!/bin/bash
# launch-subagent.sh - Launch a sub-agent as child of current session
#
# Usage: launch-subagent.sh "Title" "Prompt" [options]
#
# Options:
#   --mcp <name>       Attach MCP (can repeat)
#   --wait             Poll until complete, return output
#   --timeout <sec>    Wait timeout (default: 300)
#   --init-timeout <s> Claude init timeout (default: 15)
#
# Examples:
#   launch-subagent.sh "Research" "Find info about X"
#   launch-subagent.sh "Task" "Do Y" --mcp exa --mcp firecrawl
#   launch-subagent.sh "Query" "Answer Z" --wait --timeout 120

set -e

# Parse arguments
TITLE=""
PROMPT=""
MCPS=()
WAIT=false
TIMEOUT=300
INIT_TIMEOUT=15

while [ $# -gt 0 ]; do
    case "$1" in
        --mcp)
            MCPS+=("$2")
            shift 2
            ;;
        --wait)
            WAIT=true
            shift
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --init-timeout)
            INIT_TIMEOUT="$2"
            shift 2
            ;;
        *)
            if [ -z "$TITLE" ]; then
                TITLE="$1"
            elif [ -z "$PROMPT" ]; then
                PROMPT="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$TITLE" ] || [ -z "$PROMPT" ]; then
    echo "Usage: launch-subagent.sh \"Title\" \"Prompt\" [--mcp name] [--wait]" >&2
    exit 1
fi

# Detect current session - parse JSON properly without grep hack
CURRENT_OUTPUT=$(agent-deck session current --json 2>/dev/null) || {
    echo "Error: Not in an agent-deck session" >&2
    exit 1
}

# Extract JSON (last valid JSON object in output)
CURRENT_JSON=$(echo "$CURRENT_OUTPUT" | grep -E '^\{' | tail -1)

if [ -z "$CURRENT_JSON" ]; then
    echo "Error: Could not parse session info" >&2
    exit 1
fi

PARENT=$(echo "$CURRENT_JSON" | jq -r '.session // empty')
PROFILE=$(echo "$CURRENT_JSON" | jq -r '.profile // empty')

if [ -z "$PARENT" ]; then
    echo "Error: Not in an agent-deck session" >&2
    exit 1
fi

# Create work directory with better sanitization
# Remove all non-alphanumeric chars except dash, convert to lowercase
SAFE_TITLE=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')

# Fallback if title becomes empty after sanitization
if [ -z "$SAFE_TITLE" ]; then
    SAFE_TITLE="subagent-$(date +%s)"
fi

# Use TMPDIR if set, otherwise /tmp
WORK_DIR="${TMPDIR:-/tmp}/${SAFE_TITLE}"
mkdir -p "$WORK_DIR"

# Build command as array (safe, no eval needed)
ADD_ARGS=(-p "$PROFILE" add -t "$TITLE" --parent "$PARENT" -c claude)
for mcp in "${MCPS[@]}"; do
    ADD_ARGS+=(--mcp "$mcp")
done
ADD_ARGS+=("$WORK_DIR")

# Create and start session (using array expansion, not eval)
agent-deck "${ADD_ARGS[@]}"
agent-deck -p "$PROFILE" session start "$TITLE"

# Get tmux session name for readiness check
TMUX_SESSION=$(agent-deck -p "$PROFILE" session show "$TITLE" 2>/dev/null | grep '^Tmux:' | awk '{print $2}')

# Wait for Claude to be ready (configurable timeout)
echo "Waiting for Claude to initialize..."
for ((i=1; i<=INIT_TIMEOUT; i++)); do
    # Check if Claude is showing a prompt (has substantial content)
    PANE_CONTENT=$(tmux capture-pane -t "$TMUX_SESSION" -p 2>/dev/null | tail -5) || true

    # Claude is ready when it shows the project path or prompt
    if echo "$PANE_CONTENT" | grep -qE "(>|claude|Claude Code|$WORK_DIR)" 2>/dev/null; then
        sleep 2  # Extra buffer for stability
        break
    fi
    sleep 1
done

# Send prompt
agent-deck -p "$PROFILE" session send "$TITLE" "$PROMPT"

echo ""
echo "Sub-agent launched:"
echo "  Title:   $TITLE"
echo "  Parent:  $PARENT"
echo "  Profile: $PROFILE"
echo "  Path:    $WORK_DIR"
if [ ${#MCPS[@]} -gt 0 ]; then
    echo "  MCPs:    ${MCPS[*]}"
fi
echo ""
echo "Check output with: agent-deck session output \"$TITLE\""

# If --wait, poll until complete
if [ "$WAIT" = "true" ]; then
    echo ""
    echo "Waiting for completion (timeout: ${TIMEOUT}s)..."

    START_TIME=$(date +%s)
    while true; do
        # Get status, handle both unicode and text formats
        STATUS_LINE=$(agent-deck -p "$PROFILE" session show "$TITLE" 2>/dev/null | grep '^Status:' || true)

        # Check for waiting status (both unicode ◐ and text "waiting")
        if echo "$STATUS_LINE" | grep -qE '(◐|waiting|idle)'; then
            echo "Complete!"
            echo ""
            echo "=== Response ==="
            agent-deck -p "$PROFILE" session output "$TITLE"
            exit 0
        fi

        ELAPSED=$(($(date +%s) - START_TIME))
        if [ $ELAPSED -ge $TIMEOUT ]; then
            echo "Timeout after ${TIMEOUT}s (session still running)" >&2
            echo "Check later with: agent-deck session output \"$TITLE\""
            exit 1
        fi

        sleep 5
    done
fi
