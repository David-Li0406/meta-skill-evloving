#!/bin/bash
# log-decision.sh — Append a decision entry to the decision log
# Part of the Dialogue Framework
# Usage: log-decision.sh <type> <actor> <subject> <outcome> <rationale> [context] [tags] [ref]
#
# Also creates a context graph node and CREATED edge for TMS integration (FW-028).

set -euo pipefail

# Use Claude's project directory environment variable
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
LOG_DIR="${PROJECT_ROOT}/.dialogue/logs/decisions"
GRAPH_NODES_DIR="${PROJECT_ROOT}/.dialogue/context-graph/nodes/artifacts"
GRAPH_EDGES_DIR="${PROJECT_ROOT}/.dialogue/context-graph/edges/actor-artifact"

# Validate required arguments
if [[ $# -lt 5 ]]; then
    echo "Usage: log-decision.sh <type> <actor> <subject> <outcome> <rationale> [context] [tags] [ref]" >&2
    echo "  type:      OPERATIONAL | TACTICAL | DESIGN | ADR" >&2
    echo "  actor:     ai:claude | human:<id>" >&2
    echo "  subject:   Brief description of what the decision concerns" >&2
    echo "  outcome:   What was decided/done" >&2
    echo "  rationale: Single-line reasoning (REQUIRED for DESIGN/ADR)" >&2
    echo "  context:   Additional context (REQUIRED for DESIGN/ADR, optional otherwise)" >&2
    echo "  tags:      (optional) Comma-separated tags" >&2
    echo "  ref:       (optional) Reference to related document (e.g., ADR-001)" >&2
    exit 1
fi

TYPE="$1"
ACTOR="$2"
SUBJECT="$3"
OUTCOME="$4"
RATIONALE="$5"
CONTEXT="${6:-}"
TAGS="${7:-}"
REF="${8:-}"

# Validate type
if [[ "$TYPE" != "OPERATIONAL" && "$TYPE" != "TACTICAL" && "$TYPE" != "DESIGN" && "$TYPE" != "ADR" ]]; then
    echo "Error: type must be OPERATIONAL, TACTICAL, DESIGN, or ADR" >&2
    exit 1
fi

# DESIGN and ADR types require rationale and context
if [[ "$TYPE" == "DESIGN" || "$TYPE" == "ADR" ]]; then
    if [[ -z "$RATIONALE" ]]; then
        echo "Error: DESIGN and ADR decisions require rationale" >&2
        exit 1
    fi
    if [[ -z "$CONTEXT" ]]; then
        echo "Error: DESIGN and ADR decisions require context" >&2
        exit 1
    fi
fi

# Generate timestamp and ID
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ID="DEC-$(date -u +"%Y%m%d-%H%M%S")"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Individual file for this decision
LOG_FILE="${LOG_DIR}/${ID}.yaml"

# Build YAML entry (single file per decision)
{
    echo "id: $ID"
    echo "timestamp: \"$TIMESTAMP\""
    echo "type: $TYPE"
    echo "actor: \"$ACTOR\""
    echo "subject: \"$SUBJECT\""
    echo "outcome: \"$OUTCOME\""
    echo "rationale: \"$RATIONALE\""
    if [[ -n "$CONTEXT" ]]; then
        echo "context: \"$CONTEXT\""
    fi
    if [[ -n "$REF" ]]; then
        echo "ref: \"$REF\""
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

    # Create artifact node for this decision
    NODE_FILE="${GRAPH_NODES_DIR}/${ID}.yaml"
    {
        echo "id: $ID"
        echo "node_type: ARTIFACT"
        echo "metadata:"
        echo "  artifact_type: DECISION"
        echo "  decision_type: $TYPE"
        echo "  temporal_class: Ephemeral"
        echo "  content_type: text/yaml"
        echo "  title: \"$SUBJECT\""
        echo "  summary: \"$OUTCOME\""
        echo "  location_hint: \".dialogue/logs/decisions/${ID}.yaml\""
        echo "  author: \"$ACTOR\""
        echo "created: \"$TIMESTAMP\""
        echo "updated: \"$TIMESTAMP\""
        echo "status: ACTIVE"
    } > "$NODE_FILE"

    # Create CREATED edge from actor to decision
    # Sanitise actor ID for filename (replace : with -)
    ACTOR_SANITISED="${ACTOR//:/-}"
    EDGE_ID="created-${ACTOR_SANITISED}-${ID}"
    EDGE_FILE="${GRAPH_EDGES_DIR}/${EDGE_ID}.yaml"
    {
        echo "id: $EDGE_ID"
        echo "source: \"$ACTOR\""
        echo "target: $ID"
        echo "edge_type: CREATED"
        echo "metadata:"
        echo "  timestamp: \"$TIMESTAMP\""
        echo "  decision_type: $TYPE"
        echo "created: \"$TIMESTAMP\""
        echo "confidence: 1.0"
    } > "$EDGE_FILE"
fi

echo "$ID"
