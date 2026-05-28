#!/bin/bash
# shellcheck shell=bash
# create-adr.sh — Create an Architecture Decision Record with decision log cross-reference
# Part of the Dialogue Framework
# Usage: create-adr.sh <title> <actor> <context> <decision> <alternatives> <consequences> <rationale> [tags]

set -euo pipefail

# Use Claude's environment variables for portability
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT must be set}"

ADR_DIR="${PROJECT_ROOT}/decisions"
LOG_SCRIPT="${PLUGIN_ROOT}/skills/dialogue-log-decision/scripts/log-decision.sh"

# Validate required arguments
if [[ $# -lt 7 ]]; then
    echo "Usage: create-adr.sh <title> <actor> <context> <decision> <alternatives> <consequences> <rationale> [tags]" >&2
    echo "  title:        Short descriptive title" >&2
    echo "  actor:        human:<id> | ai:claude" >&2
    echo "  context:      What issue motivated this decision?" >&2
    echo "  decision:     What change are we making?" >&2
    echo "  alternatives: Alternatives considered with pros/cons" >&2
    echo "  consequences: What becomes easier or harder?" >&2
    echo "  rationale:    Why is this the right choice?" >&2
    echo "  tags:         (optional) Comma-separated tags" >&2
    exit 1
fi

TITLE="$1"
ACTOR="$2"
CONTEXT="$3"
DECISION="$4"
ALTERNATIVES="$5"
CONSEQUENCES="$6"
RATIONALE="$7"
TAGS="${8:-}"

# Validate actor format
if [[ ! "$ACTOR" =~ ^(human:[a-zA-Z0-9_-]+|ai:[a-zA-Z0-9_-]+)$ ]]; then
    echo "Error: actor must be 'human:<id>' or 'ai:<id>' (e.g., human:pidster, ai:claude)" >&2
    exit 1
fi

# Ensure decisions directory exists
mkdir -p "$ADR_DIR"

# Determine next ADR number (robust handling of empty directory and leading zeros)
LAST_ADR=0
if compgen -G "$ADR_DIR/ADR-*.md" > /dev/null 2>&1; then
    # Extract numbers, strip leading zeros for arithmetic, find max
    LAST_ADR=$(ls -1 "$ADR_DIR"/ADR-*.md | sed 's/.*ADR-0*\([0-9][0-9]*\).*/\1/' | sort -n | tail -1)
fi
NEXT_NUM=$((LAST_ADR + 1))
ADR_NUM=$(printf "%03d" "$NEXT_NUM")

# Slugify title for filename
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
ADR_ID="ADR-${ADR_NUM}"
ADR_FILE="${ADR_DIR}/${ADR_ID}-${SLUG}.md"

# Get current date
DATE=$(date +"%Y-%m-%d")

# Create ADR file (using heredoc with proper escaping)
# Note: ADR files are Markdown, not YAML, so special characters are generally safe
# However, we should be cautious with the header metadata
cat > "$ADR_FILE" << EOF
# ${ADR_ID}: ${TITLE}

Date: ${DATE}
Status: Proposed
Actor: ${ACTOR}

## Context

${CONTEXT}

## Decision

${DECISION}

## Alternatives Considered

${ALTERNATIVES}

## Consequences

${CONSEQUENCES}

## Rationale

${RATIONALE}
EOF

# Output ADR info
echo "${ADR_ID}: ${ADR_FILE}"

# Log cross-reference to decision log
if [[ -f "$LOG_SCRIPT" && -x "$LOG_SCRIPT" ]]; then
    # Truncate rationale for decision log (keep it concise)
    SHORT_RATIONALE="${RATIONALE:0:200}"
    if [[ ${#RATIONALE} -gt 200 ]]; then
        SHORT_RATIONALE="${SHORT_RATIONALE}..."
    fi

    DEC_ID=$("$LOG_SCRIPT" "ADR" "$ACTOR" "$TITLE" "Created ${ADR_ID}" "$SHORT_RATIONALE" "$CONTEXT" "${TAGS:-architecture}" "$ADR_ID") || {
        echo "Warning: Failed to log cross-reference to decision log" >&2
    }
    if [[ -n "${DEC_ID:-}" ]]; then
        echo "${DEC_ID}: Cross-reference logged"
    fi
else
    echo "Warning: Could not log cross-reference (log-decision.sh not found at $LOG_SCRIPT)" >&2
fi
