#!/bin/bash
# log-daily-check.sh — Log a daily check assessment for developer experience
# Part of the Dialogue Framework
# Usage: log-daily-check.sh <assessor> <made_progress> <learned_something> <felt_supported> <had_agency> \
#                           <experienced_blockers> <context_switching> <unclear_requirements> \
#                           <session_quality> [task_ref] [notes]
#
# Also creates a context graph node and CREATED edge for TMS integration.

set -euo pipefail

# Use Claude's project directory environment variable
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
LOG_DIR="${PROJECT_ROOT}/.dialogue/logs/assessments"
GRAPH_NODES_DIR="${PROJECT_ROOT}/.dialogue/context-graph/nodes/artifacts"
GRAPH_EDGES_DIR_ACTOR="${PROJECT_ROOT}/.dialogue/context-graph/edges/actor-artifact"
GRAPH_EDGES_DIR_TRACE="${PROJECT_ROOT}/.dialogue/context-graph/edges/traceability"

# Validate required arguments
if [[ $# -lt 9 ]]; then
    echo "Usage: log-daily-check.sh <assessor> <made_progress> <learned_something> <felt_supported> <had_agency> \\" >&2
    echo "                          <experienced_blockers> <context_switching> <unclear_requirements> \\" >&2
    echo "                          <session_quality> [task_ref] [notes]" >&2
    echo "" >&2
    echo "  assessor:             ai:claude | human:<id>" >&2
    echo "  made_progress:        true | false" >&2
    echo "  learned_something:    true | false" >&2
    echo "  felt_supported:       true | false" >&2
    echo "  had_agency:           true | false" >&2
    echo "  experienced_blockers: true | false" >&2
    echo "  context_switching:    true | false" >&2
    echo "  unclear_requirements: true | false" >&2
    echo "  session_quality:      1-5" >&2
    echo "  task_ref:             (optional) Task reference e.g., FW-023" >&2
    echo "  notes:                (optional) Free-text reflection" >&2
    exit 1
fi

ASSESSOR="$1"
MADE_PROGRESS="$2"
LEARNED_SOMETHING="$3"
FELT_SUPPORTED="$4"
HAD_AGENCY="$5"
EXPERIENCED_BLOCKERS="$6"
CONTEXT_SWITCHING="$7"
UNCLEAR_REQUIREMENTS="$8"
SESSION_QUALITY="$9"
TASK_REF="${10:-}"
NOTES="${11:-}"

# Validate boolean values
validate_bool() {
    local name="$1"
    local value="$2"
    if [[ "$value" != "true" && "$value" != "false" ]]; then
        echo "Error: $name must be true or false, got: $value" >&2
        exit 1
    fi
}

validate_bool "made_progress" "$MADE_PROGRESS"
validate_bool "learned_something" "$LEARNED_SOMETHING"
validate_bool "felt_supported" "$FELT_SUPPORTED"
validate_bool "had_agency" "$HAD_AGENCY"
validate_bool "experienced_blockers" "$EXPERIENCED_BLOCKERS"
validate_bool "context_switching" "$CONTEXT_SWITCHING"
validate_bool "unclear_requirements" "$UNCLEAR_REQUIREMENTS"

# Validate session_quality (1-5)
if ! [[ "$SESSION_QUALITY" =~ ^[1-5]$ ]]; then
    echo "Error: session_quality must be 1-5, got: $SESSION_QUALITY" >&2
    exit 1
fi

# Generate timestamp and ID
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ID="ASSESS-$(date -u +"%Y%m%d-%H%M%S")"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Individual file for this assessment
LOG_FILE="${LOG_DIR}/${ID}.yaml"

# Count good/bad indicators for summary
GOOD_COUNT=0
BAD_COUNT=0
GOOD_ITEMS=""
BAD_ITEMS=""

[[ "$MADE_PROGRESS" == "true" ]] && GOOD_COUNT=$((GOOD_COUNT + 1)) && GOOD_ITEMS="${GOOD_ITEMS}progress, "
[[ "$LEARNED_SOMETHING" == "true" ]] && GOOD_COUNT=$((GOOD_COUNT + 1)) && GOOD_ITEMS="${GOOD_ITEMS}learning, "
[[ "$FELT_SUPPORTED" == "true" ]] && GOOD_COUNT=$((GOOD_COUNT + 1)) && GOOD_ITEMS="${GOOD_ITEMS}support, "
[[ "$HAD_AGENCY" == "true" ]] && GOOD_COUNT=$((GOOD_COUNT + 1)) && GOOD_ITEMS="${GOOD_ITEMS}agency, "

[[ "$EXPERIENCED_BLOCKERS" == "true" ]] && BAD_COUNT=$((BAD_COUNT + 1)) && BAD_ITEMS="${BAD_ITEMS}blockers, "
[[ "$CONTEXT_SWITCHING" == "true" ]] && BAD_COUNT=$((BAD_COUNT + 1)) && BAD_ITEMS="${BAD_ITEMS}context-switching, "
[[ "$UNCLEAR_REQUIREMENTS" == "true" ]] && BAD_COUNT=$((BAD_COUNT + 1)) && BAD_ITEMS="${BAD_ITEMS}unclear-requirements, "

# Trim trailing ", "
GOOD_ITEMS="${GOOD_ITEMS%, }"
BAD_ITEMS="${BAD_ITEMS%, }"

# Build YAML entry
{
    echo "id: $ID"
    echo "timestamp: \"$TIMESTAMP\""
    echo "assessment_type: DAILY_CHECK"
    echo "assessor: \"$ASSESSOR\""
    if [[ -n "$TASK_REF" ]]; then
        echo "task_ref: \"$TASK_REF\""
    fi
    echo "responses:"
    echo "  # Good day indicators (C-6 Developer Thriving)"
    echo "  made_progress: $MADE_PROGRESS"
    echo "  learned_something: $LEARNED_SOMETHING"
    echo "  felt_supported: $FELT_SUPPORTED"
    echo "  had_agency: $HAD_AGENCY"
    echo "  # Bad day indicators (C-7 'Bad Days')"
    echo "  experienced_blockers: $EXPERIENCED_BLOCKERS"
    echo "  context_switching: $CONTEXT_SWITCHING"
    echo "  unclear_requirements: $UNCLEAR_REQUIREMENTS"
    echo "  # Overall"
    echo "  session_quality: $SESSION_QUALITY"
    if [[ -n "$NOTES" ]]; then
        echo "  notes: \"$NOTES\""
    fi
    echo "summary:"
    echo "  good_count: $GOOD_COUNT"
    echo "  bad_count: $BAD_COUNT"
    if [[ -n "$GOOD_ITEMS" ]]; then
        echo "  good_items: \"$GOOD_ITEMS\""
    fi
    if [[ -n "$BAD_ITEMS" ]]; then
        echo "  bad_items: \"$BAD_ITEMS\""
    fi
} > "$LOG_FILE"

# Create context graph node (TMS integration)
if [[ -d "${PROJECT_ROOT}/.dialogue/context-graph" ]]; then
    mkdir -p "$GRAPH_NODES_DIR" "$GRAPH_EDGES_DIR_ACTOR" "$GRAPH_EDGES_DIR_TRACE"

    # Build summary for node
    SUMMARY="Session quality: ${SESSION_QUALITY}/5, good: ${GOOD_COUNT}, bad: ${BAD_COUNT}"

    # Create artifact node for this assessment
    NODE_FILE="${GRAPH_NODES_DIR}/${ID}.yaml"
    {
        echo "id: $ID"
        echo "node_type: ARTIFACT"
        echo "metadata:"
        echo "  artifact_type: ASSESSMENT"
        echo "  assessment_type: DAILY_CHECK"
        echo "  temporal_class: Ephemeral"
        echo "  content_type: text/yaml"
        echo "  title: \"Daily Check - $(date -u +"%Y-%m-%d")\""
        echo "  summary: \"$SUMMARY\""
        echo "  location_hint: \".dialogue/logs/assessments/${ID}.yaml\""
        echo "  assessor: \"$ASSESSOR\""
        echo "created: \"$TIMESTAMP\""
        echo "updated: \"$TIMESTAMP\""
        echo "status: ACTIVE"
    } > "$NODE_FILE"

    # Create CREATED edge from assessor to assessment
    # Sanitise assessor ID for filename (replace : with -)
    ASSESSOR_SANITISED="${ASSESSOR//:/-}"
    EDGE_ID="created-${ASSESSOR_SANITISED}-${ID}"
    EDGE_FILE="${GRAPH_EDGES_DIR_ACTOR}/${EDGE_ID}.yaml"
    {
        echo "id: $EDGE_ID"
        echo "source: \"$ASSESSOR\""
        echo "target: $ID"
        echo "edge_type: CREATED"
        echo "metadata:"
        echo "  timestamp: \"$TIMESTAMP\""
        echo "  assessment_type: DAILY_CHECK"
        echo "created: \"$TIMESTAMP\""
        echo "confidence: 1.0"
    } > "$EDGE_FILE"

    # Create ASSESSES edge to task if task_ref provided
    if [[ -n "$TASK_REF" ]]; then
        ASSESSES_EDGE_ID="assesses-${ID}-${TASK_REF}"
        ASSESSES_EDGE_FILE="${GRAPH_EDGES_DIR_TRACE}/${ASSESSES_EDGE_ID}.yaml"
        {
            echo "id: $ASSESSES_EDGE_ID"
            echo "source: $ID"
            echo "target: \"$TASK_REF\""
            echo "edge_type: ASSESSES"
            echo "metadata:"
            echo "  assessment_type: DAILY_CHECK"
            echo "  session_quality: $SESSION_QUALITY"
            echo "created: \"$TIMESTAMP\""
            echo "confidence: 1.0"
        } > "$ASSESSES_EDGE_FILE"
    fi
fi

echo "$ID"
