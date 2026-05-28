#!/bin/bash
# MixSeek Debug Environment Variable Checker
# Usage: bash .skills/mixseek-debug/scripts/check-debug-env.sh

echo "=== MixSeek Debug Environment Variables ==="
echo ""

# Check MIXSEEK_VERBOSE
echo "MIXSEEK_VERBOSE:"
if [ -n "$MIXSEEK_VERBOSE" ]; then
    echo "  Value: $MIXSEEK_VERBOSE"
    if [ "$MIXSEEK_VERBOSE" = "1" ] || [ "${MIXSEEK_VERBOSE,,}" = "true" ]; then
        echo "  Status: ENABLED (Unified debug mode active)"
        echo "  Effects:"
        echo "    - MCP tool call logs"
        echo "    - mixseek.member_agents logger (DEBUG)"
        echo "    - claudecode_model logger (DEBUG)"
    else
        echo "  Status: Set but not enabled (use '1' or 'true')"
    fi
else
    echo "  Status: NOT SET"
fi
echo ""

# Check CLAUDECODE_MODEL_LOG_LEVEL
echo "CLAUDECODE_MODEL_LOG_LEVEL:"
if [ -n "$CLAUDECODE_MODEL_LOG_LEVEL" ]; then
    echo "  Value: $CLAUDECODE_MODEL_LOG_LEVEL"
    if [ "${CLAUDECODE_MODEL_LOG_LEVEL^^}" = "DEBUG" ]; then
        echo "  Status: ENABLED (claudecode-model DEBUG logging)"
    else
        echo "  Status: Set to $CLAUDECODE_MODEL_LOG_LEVEL"
    fi
else
    echo "  Status: NOT SET (uses INFO by default)"
fi
echo ""

# Check MIXSEEK_LOGFIRE
echo "MIXSEEK_LOGFIRE:"
if [ -n "$MIXSEEK_LOGFIRE" ]; then
    echo "  Value: $MIXSEEK_LOGFIRE"
    if [ "$MIXSEEK_LOGFIRE" = "1" ] || [ "${MIXSEEK_LOGFIRE,,}" = "true" ]; then
        echo "  Status: ENABLED (Logfire instrumentation active)"
        echo "  Note: Requires logfire.configure() to be called in Python"
    else
        echo "  Status: Set but not enabled (use '1' or 'true')"
    fi
else
    echo "  Status: NOT SET"
fi
echo ""

# Check MIXSEEK_WORKSPACE (for log file location)
echo "MIXSEEK_WORKSPACE:"
if [ -n "$MIXSEEK_WORKSPACE" ]; then
    echo "  Value: $MIXSEEK_WORKSPACE"
    LOGS_DIR="$MIXSEEK_WORKSPACE/logs"
    if [ -d "$LOGS_DIR" ]; then
        echo "  Logs directory: $LOGS_DIR (exists)"
        LOG_FILES=$(ls -1 "$LOGS_DIR"/member-agent-*.log 2>/dev/null | wc -l)
        if [ "$LOG_FILES" -gt 0 ]; then
            echo "  Log files found: $LOG_FILES"
            echo "  Latest log:"
            ls -lt "$LOGS_DIR"/member-agent-*.log 2>/dev/null | head -1 | awk '{print "    " $NF}'
        else
            echo "  No member-agent log files found yet"
        fi
    else
        echo "  Logs directory: $LOGS_DIR (does not exist)"
    fi
else
    echo "  Status: NOT SET"
    echo "  Note: Log files will be written to current directory"
fi
echo ""

# Summary
echo "=== Summary ==="
ACTIVE_COUNT=0

if [ -n "$MIXSEEK_VERBOSE" ] && { [ "$MIXSEEK_VERBOSE" = "1" ] || [ "${MIXSEEK_VERBOSE,,}" = "true" ]; }; then
    echo "  [x] MIXSEEK_VERBOSE is enabled"
    ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
else
    echo "  [ ] MIXSEEK_VERBOSE is not enabled"
fi

if [ -n "$CLAUDECODE_MODEL_LOG_LEVEL" ] && [ "${CLAUDECODE_MODEL_LOG_LEVEL^^}" = "DEBUG" ]; then
    echo "  [x] CLAUDECODE_MODEL_LOG_LEVEL=DEBUG"
    ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
else
    echo "  [ ] CLAUDECODE_MODEL_LOG_LEVEL is not DEBUG"
fi

if [ -n "$MIXSEEK_LOGFIRE" ] && { [ "$MIXSEEK_LOGFIRE" = "1" ] || [ "${MIXSEEK_LOGFIRE,,}" = "true" ]; }; then
    echo "  [x] MIXSEEK_LOGFIRE is enabled"
    ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
else
    echo "  [ ] MIXSEEK_LOGFIRE is not enabled"
fi

echo ""
echo "Active debug features: $ACTIVE_COUNT/3"

if [ "$ACTIVE_COUNT" -eq 0 ]; then
    echo ""
    echo "Tip: To enable verbose debugging, run:"
    echo "  export MIXSEEK_VERBOSE=1"
fi
