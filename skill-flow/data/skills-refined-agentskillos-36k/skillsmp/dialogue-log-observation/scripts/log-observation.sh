#!/bin/bash
# log-observation.sh — Append an observation entry to the observation log
# Part of the Dialogue Framework
# Usage: log-observation.sh <type> <observer> <subject> <value> [context] [tags]
#
# Also creates a context graph node and CREATED edge for TMS integration (FW-028).

set -euo pipefail

# Use Claude's project directory environment variable
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
LOG_DIR="${PROJECT_ROOT}/.dialogue/logs/observations"
GRAPH_NODES_DIR="${PROJECT_ROOT}/.dialogue/context-graph/nodes/artifacts"
GRAPH_EDGES_DIR="${PROJECT_ROOT}/.dialogue/context-graph/edges/actor-artifact"

# Validate required arguments
if [[ $# -lt 4 ]]; then
    echo "Usage: log-observation.sh <type> <observer> <subject> <value> [context] [tags]" >&2
    echo "  type:     MEASUREMENT | STATE | EVENT" >&2
    echo "  observer: ai:claude | human:<id>" >&2
    echo "  subject:  Brief description of what was observed" >&2
    echo "  value:    The observed data/state" >&2
    echo "  context:  (optional) Additional context" >&2
    echo "  tags:     (optional) Comma-separated tags" >&2
    exit 1
fi

TYPE="$1"
OBSERVER="$2"
SUBJECT="$3"
VALUE="$4"
CONTEXT="${5:-}"
TAGS="${6:-}"

# Validate type
if [[ "$TYPE" != "MEASUREMENT" && "$TYPE" != "STATE" && "$TYPE" != "EVENT" ]]; then
    echo "Error: type must be MEASUREMENT, STATE, or EVENT" >&2
    exit 1
fi

# Generate timestamp and ID
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ID="OBS-$(date -u +"%Y%m%d-%H%M%S")"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Individual file for this observation
LOG_FILE="${LOG_DIR}/${ID}.yaml"

# Build YAML entry (single file per observation)
{
    echo "id: $ID"
    echo "timestamp: \"$TIMESTAMP\""
    echo "type: $TYPE"
    echo "observer: \"$OBSERVER\""
    echo "subject: \"$SUBJECT\""
    echo "value: \"$VALUE\""
    if [[ -n "$CONTEXT" ]]; then
        echo "context: \"$CONTEXT\""
    fi
    if [[ -n "$TAGS" ]]; then
        # Convert comma-separated tags to YAML array
        IFS=',' read -ra TAG_ARRAY <<< "$TAGS"
        printf 'tags: ['
        for i in "${!TAG_ARRAY[@]}"; do
            if [[ $i -gt 0 ]]; then printf ', '; fi
            printf '"%s"' "$(echo "${TAG_ARRAY[$i]}" | xargs)"
        done
        printf ']\n'
    fi
} > "$LOG_FILE"

# Create context graph node (FW-028 TMS integration)
if [[ -d "${PROJECT_ROOT}/.dialogue/context-graph" ]]; then
    mkdir -p "$GRAPH_NODES_DIR" "$GRAPH_EDGES_DIR"

    # Create artifact node for this observation
    NODE_FILE="${GRAPH_NODES_DIR}/${ID}.yaml"
    {
        echo "id: $ID"
        echo "node_type: ARTIFACT"
        echo "metadata:"
        echo "  artifact_type: OBSERVATION"
        echo "  observation_type: $TYPE"
        echo "  temporal_class: Ephemeral"
        echo "  content_type: text/yaml"
        echo "  title: \"$SUBJECT\""
        echo "  summary: \"$VALUE\""
        echo "  location_hint: \".dialogue/logs/observations/${ID}.yaml\""
        echo "  observer: \"$OBSERVER\""
        echo "created: \"$TIMESTAMP\""
        echo "updated: \"$TIMESTAMP\""
        echo "status: ACTIVE"
    } > "$NODE_FILE"

    # Create CREATED edge from observer to observation
    # Sanitise observer ID for filename (replace : with -)
    OBSERVER_SANITISED="${OBSERVER//:/-}"
    EDGE_ID="created-${OBSERVER_SANITISED}-${ID}"
    EDGE_FILE="${GRAPH_EDGES_DIR}/${EDGE_ID}.yaml"
    {
        echo "id: $EDGE_ID"
        echo "source: \"$OBSERVER\""
        echo "target: $ID"
        echo "edge_type: CREATED"
        echo "metadata:"
        echo "  timestamp: \"$TIMESTAMP\""
        echo "  observation_type: $TYPE"
        echo "created: \"$TIMESTAMP\""
        echo "confidence: 1.0"
    } > "$EDGE_FILE"
fi

echo "$ID"
