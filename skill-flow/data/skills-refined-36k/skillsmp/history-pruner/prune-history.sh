#!/bin/bash

# Claude Code History Pruner
# Prunes old conversation history to save disk space

set -e

PROJECTS_DIR="$HOME/.claude/projects"
LOG_FILE="$HOME/.claude/prune-history.log"
MODE="${1:-conservative}"
DRY_RUN=false

if [[ "$1" == "--dry-run" ]] || [[ "$2" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "DRY RUN - No changes will be made"
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if jq is available
if ! command -v jq &> /dev/null; then
    log "ERROR: jq is required but not installed. Install with: brew install jq"
    exit 1
fi

log "Starting history pruning (mode: $MODE)"

# Calculate cutoff timestamps
if [[ "$MODE" == "aggressive" ]]; then
    FULL_HISTORY_DAYS=3
    TRUNCATE_LENGTH=200
    REMOVE_THINKING_DAYS=7
else
    # Conservative (default)
    FULL_HISTORY_DAYS=7
    TRUNCATE_LENGTH=500
    REMOVE_THINKING_DAYS=14
fi

# macOS date syntax - ISO format for comparison
CUTOFF_DATE=$(date -v-${FULL_HISTORY_DAYS}d -u +%Y-%m-%dT%H:%M:%S)
THINKING_CUTOFF_DATE=$(date -v-${REMOVE_THINKING_DAYS}d -u +%Y-%m-%dT%H:%M:%S)

log "Keeping full history from last $FULL_HISTORY_DAYS days"
log "Truncating tool_results to $TRUNCATE_LENGTH chars for older entries"

# Find large project files (>10MB)
TOTAL_SAVED=0

find "$PROJECTS_DIR" -name "*.jsonl" -size +10M 2>/dev/null | while read -r FILE; do
    ORIGINAL_SIZE=$(du -m "$FILE" | cut -f1)
    FILENAME=$(basename "$FILE")

    log "Processing: $FILENAME (${ORIGINAL_SIZE}MB)"

    if [[ "$DRY_RUN" == true ]]; then
        # P2-PERF-003: Count both in a single jq pass
        read -r OLD_TOOL_RESULTS OLD_THINKING < <(jq -r --arg cutoff "$CUTOFF_DATE" --arg thinking_cutoff "$THINKING_CUTOFF_DATE" '
            reduce inputs as $item (
                {"tool_results": 0, "thinking": 0};
                if $item.timestamp then
                    if $item.timestamp < $cutoff and $item.type == "user" then
                        .tool_results += ([$item.message.content[]? | select(.type == "tool_result")] | length)
                    elif $item.timestamp < $thinking_cutoff and $item.type == "assistant" then
                        .thinking += ([$item.message.content[]? | select(.type == "thinking")] | length)
                    else . end
                else . end
            ) | "\(.tool_results) \(.thinking)"
        ' -n "$FILE" 2>/dev/null || echo "0 0")
        log "  Would truncate $OLD_TOOL_RESULTS tool_results, $OLD_THINKING thinking blocks"
        continue
    fi

    # Create backup
    cp "$FILE" "${FILE}.bak"

    # Process file with jq - truncate nested tool_results and thinking blocks
    jq -c --arg cutoff "$CUTOFF_DATE" --arg thinking_cutoff "$THINKING_CUTOFF_DATE" --argjson trunclen "$TRUNCATE_LENGTH" '
        if .timestamp and (.timestamp < $cutoff) then
            # Truncate tool_results in user messages
            if .type == "user" and .message.content then
                .message.content = [.message.content[] |
                    if .type == "tool_result" then
                        if .content | type == "string" then
                            .content = (.content[:$trunclen] + "... [pruned]")
                        elif .content | type == "array" then
                            .content = [.content[] | if type == "string" then .[:$trunclen] + "... [pruned]" else . end]
                        else
                            .
                        end
                    else
                        .
                    end
                ]
            # Truncate thinking blocks in assistant messages (older threshold)
            elif .type == "assistant" and .message.content and (.timestamp < $thinking_cutoff) then
                .message.content = [.message.content[] |
                    if .type == "thinking" then
                        .thinking = "[pruned]"
                    else
                        .
                    end
                ]
            else
                .
            end
        else
            .
        end
    ' "$FILE" > "${FILE}.pruned" 2>/dev/null

    # Verify line count matches
    ORIGINAL_LINES=$(wc -l < "$FILE")
    PRUNED_LINES=$(wc -l < "${FILE}.pruned")

    if [[ "$ORIGINAL_LINES" -eq "$PRUNED_LINES" ]]; then
        mv "${FILE}.pruned" "$FILE"
        rm -f "${FILE}.bak"

        NEW_SIZE=$(du -m "$FILE" | cut -f1)
        SAVED=$((ORIGINAL_SIZE - NEW_SIZE))
        TOTAL_SAVED=$((TOTAL_SAVED + SAVED))

        log "  Reduced: ${ORIGINAL_SIZE}MB -> ${NEW_SIZE}MB (saved ${SAVED}MB)"
    else
        log "  ERROR: Line count mismatch, restoring backup"
        mv "${FILE}.bak" "$FILE"
        rm -f "${FILE}.pruned"
    fi
done

log "Pruning complete. Total space saved: ~${TOTAL_SAVED}MB"
