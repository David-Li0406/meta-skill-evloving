#!/bin/bash
#
# run-monthly.sh - Monthly freshness check orchestrator
#
# Usage: ./tools/freshness/run-monthly.sh
#
# This script is triggered by launchd on the 1st of each month.
# It prepares context and prompts the user to run /design freshness.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
FRESHNESS_DIR="$DESIGN_OPS_ROOT/docs/freshness"
LOG_FILE="$HOME/Library/Logs/design-ops-freshness.log"

# Ensure directories exist
mkdir -p "$FRESHNESS_DIR"/{discoveries,validated,impact,actions,reports,trends}
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting monthly freshness check..."

# ============================================================================
# Step 1: Run scan of current Design Ops state
# ============================================================================
log "Step 1: Scanning current Design Ops state..."

if [[ -x "$SCRIPT_DIR/scan-design-ops.sh" ]]; then
    "$SCRIPT_DIR/scan-design-ops.sh" --output "$FRESHNESS_DIR/current-state.md" 2>&1 | tee -a "$LOG_FILE"
else
    log "Warning: scan-design-ops.sh not found or not executable"
fi

# ============================================================================
# Step 2: Check source health
# ============================================================================
log "Step 2: Checking source health..."

if [[ -x "$SCRIPT_DIR/check-source-health.sh" ]]; then
    "$SCRIPT_DIR/check-source-health.sh" 2>&1 | tee -a "$LOG_FILE"
else
    log "Warning: check-source-health.sh not found or not executable"
fi

# ============================================================================
# Step 3: Record last scan date
# ============================================================================
LAST_SCAN_FILE="$DESIGN_OPS_ROOT/config/.last-freshness-scan"
PREVIOUS_SCAN=$(cat "$LAST_SCAN_FILE" 2>/dev/null || echo "Never")
echo "$(date +%Y-%m-%d)" > "$LAST_SCAN_FILE"

log "Previous scan: $PREVIOUS_SCAN"
log "Current scan: $(date +%Y-%m-%d)"

# ============================================================================
# Step 4: Generate prompt context file
# ============================================================================
CONTEXT_FILE="$FRESHNESS_DIR/freshness-context-$(date +%Y-%m).md"

cat > "$CONTEXT_FILE" << EOF
# Freshness Check Context

> Generated: $(date '+%Y-%m-%d %H:%M:%S')
> Previous Scan: $PREVIOUS_SCAN

## Instructions

Run the following command in Claude Code:

\`\`\`
/design freshness full
\`\`\`

## Pre-gathered Context

### Current Design Ops State

$(cat "$FRESHNESS_DIR/current-state.md" 2>/dev/null || echo "Not available - run scan-design-ops.sh")

### Source Health Status

$(cat "$FRESHNESS_DIR/source-health-$(date +%Y-%m).md" 2>/dev/null || echo "Not available - run check-source-health.sh")

---

## Research Period

Research developments from **$PREVIOUS_SCAN** to **$(date +%Y-%m-%d)**.

## Focus Areas

1. Anthropic official updates (docs, cookbook, blog)
2. MCP (Model Context Protocol) changes
3. Claude Code best practices evolution
4. Agentic engineering patterns with traction

EOF

log "Context file created: $CONTEXT_FILE"

# ============================================================================
# Step 5: Notify user
# ============================================================================
log "Step 5: Sending notification..."

"$SCRIPT_DIR/send-notification.sh" 2>&1 | tee -a "$LOG_FILE" || true

# ============================================================================
# Step 6: Try to open Claude Code (optional)
# ============================================================================
if command -v claude &> /dev/null; then
    log "Claude CLI found. You can run: claude '/design freshness full'"

    # Optionally auto-launch (uncomment to enable)
    # claude --prompt "/design freshness full"
else
    log "Claude CLI not found. Open Claude Code manually and run /design freshness"
fi

# ============================================================================
# Summary
# ============================================================================
log "Monthly freshness check preparation complete."
log ""
log "Next steps:"
log "  1. Open Claude Code"
log "  2. Navigate to Design Ops directory"
log "  3. Run: /design freshness full"
log ""
log "Context file: $CONTEXT_FILE"
log "Log file: $LOG_FILE"
