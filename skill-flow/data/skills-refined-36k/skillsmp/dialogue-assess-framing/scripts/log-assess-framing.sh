#!/bin/bash
# log-assess-framing.sh — Log a problem framing assessment
# Part of the Dialogue Framework
# Usage: log-assess-framing.sh <assessor> <problem_stated> <scope_bounded> <success_criteria> \
#                              <constraints_identified> <assumptions_explicit> <stakeholders_identified> \
#                              <confidence> [phase] [task_ref] [gaps_identified] [context] [tags]
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
if [[ $# -lt 8 ]]; then
    echo "Usage: log-assess-framing.sh <assessor> <problem_stated> <scope_bounded> <success_criteria> \\" >&2
    echo "                             <constraints_identified> <assumptions_explicit> <stakeholders_identified> \\" >&2
    echo "                             <confidence> [phase] [task_ref] [gaps_identified] [context] [tags]" >&2
    echo "" >&2
    echo "  assessor:               ai:claude | human:<id>" >&2
    echo "  problem_stated:         true | false" >&2
    echo "  scope_bounded:          true | false" >&2
    echo "  success_criteria:       true | false" >&2
    echo "  constraints_identified: true | false" >&2
    echo "  assumptions_explicit:   true | false" >&2
    echo "  stakeholders_identified: true | false" >&2
    echo "  confidence:             1-5" >&2
    echo "  phase:                  (optional) 1-7, current SDLC phase" >&2
    echo "  task_ref:               (optional) Task reference e.g., FW-023" >&2
    echo "  gaps_identified:        (optional) Any gaps or concerns noted" >&2
    echo "  context:                (optional) Situational context" >&2
    echo "  tags:                   (optional) Comma-separated categorisation tags" >&2
    exit 1
fi

ASSESSOR="$1"
PROBLEM_STATED="$2"
SCOPE_BOUNDED="$3"
SUCCESS_CRITERIA="$4"
CONSTRAINTS_IDENTIFIED="$5"
ASSUMPTIONS_EXPLICIT="$6"
STAKEHOLDERS_IDENTIFIED="$7"
CONFIDENCE="$8"
PHASE="${9:-}"
TASK_REF="${10:-}"
GAPS_IDENTIFIED="${11:-}"
CONTEXT="${12:-}"
TAGS="${13:-}"

# Validate boolean values
validate_bool() {
    local name="$1"
    local value="$2"
    if [[ "$value" != "true" && "$value" != "false" ]]; then
        echo "Error: $name must be true or false, got: $value" >&2
        exit 1
    fi
}

validate_bool "problem_stated" "$PROBLEM_STATED"
validate_bool "scope_bounded" "$SCOPE_BOUNDED"
validate_bool "success_criteria" "$SUCCESS_CRITERIA"
validate_bool "constraints_identified" "$CONSTRAINTS_IDENTIFIED"
validate_bool "assumptions_explicit" "$ASSUMPTIONS_EXPLICIT"
validate_bool "stakeholders_identified" "$STAKEHOLDERS_IDENTIFIED"

# Validate confidence (1-5)
if ! [[ "$CONFIDENCE" =~ ^[1-5]$ ]]; then
    echo "Error: confidence must be 1-5, got: $CONFIDENCE" >&2
    exit 1
fi

# Validate phase if provided (1-7)
if [[ -n "$PHASE" ]] && ! [[ "$PHASE" =~ ^[1-7]$ ]]; then
    echo "Error: phase must be 1-7, got: $PHASE" >&2
    exit 1
fi

# Generate timestamp and ID
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ID="ASSESS-$(date -u +"%Y%m%d-%H%M%S")"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Individual file for this assessment
LOG_FILE="${LOG_DIR}/${ID}.yaml"

# Count confirmed elements for summary
CONFIRMED_COUNT=0
MISSING_ITEMS=""

[[ "$PROBLEM_STATED" == "true" ]] && CONFIRMED_COUNT=$((CONFIRMED_COUNT + 1)) || MISSING_ITEMS="${MISSING_ITEMS}problem_stated, "
[[ "$SCOPE_BOUNDED" == "true" ]] && CONFIRMED_COUNT=$((CONFIRMED_COUNT + 1)) || MISSING_ITEMS="${MISSING_ITEMS}scope_bounded, "
[[ "$SUCCESS_CRITERIA" == "true" ]] && CONFIRMED_COUNT=$((CONFIRMED_COUNT + 1)) || MISSING_ITEMS="${MISSING_ITEMS}success_criteria, "
[[ "$CONSTRAINTS_IDENTIFIED" == "true" ]] && CONFIRMED_COUNT=$((CONFIRMED_COUNT + 1)) || MISSING_ITEMS="${MISSING_ITEMS}constraints_identified, "
[[ "$ASSUMPTIONS_EXPLICIT" == "true" ]] && CONFIRMED_COUNT=$((CONFIRMED_COUNT + 1)) || MISSING_ITEMS="${MISSING_ITEMS}assumptions_explicit, "
[[ "$STAKEHOLDERS_IDENTIFIED" == "true" ]] && CONFIRMED_COUNT=$((CONFIRMED_COUNT + 1)) || MISSING_ITEMS="${MISSING_ITEMS}stakeholders_identified, "

# Trim trailing ", "
MISSING_ITEMS="${MISSING_ITEMS%, }"

# Determine readiness recommendation
# Logic: Both confirmed count AND confidence must meet thresholds
if [[ $CONFIRMED_COUNT -eq 6 && $CONFIDENCE -ge 4 ]]; then
    RECOMMENDATION="PROCEED"
elif [[ $CONFIRMED_COUNT -ge 5 && $CONFIDENCE -ge 3 ]]; then
    RECOMMENDATION="PROCEED_WITH_CAUTION"
elif [[ $CONFIRMED_COUNT -ge 4 && $CONFIDENCE -ge 2 ]]; then
    RECOMMENDATION="ADDRESS_GAPS"
else
    RECOMMENDATION="RETURN_TO_DEFINITION"
fi

# Build YAML entry
{
    echo "id: $ID"
    echo "timestamp: \"$TIMESTAMP\""
    echo "assessment_type: PROBLEM_FRAMING"
    echo "assessor: \"$ASSESSOR\""
    if [[ -n "$PHASE" ]]; then
        echo "phase: $PHASE"
    fi
    if [[ -n "$TASK_REF" ]]; then
        echo "task_ref: \"$TASK_REF\""
    fi
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
    echo "responses:"
    echo "  # Problem framing checklist"
    echo "  problem_stated: $PROBLEM_STATED"
    echo "  scope_bounded: $SCOPE_BOUNDED"
    echo "  success_criteria: $SUCCESS_CRITERIA"
    echo "  constraints_identified: $CONSTRAINTS_IDENTIFIED"
    echo "  assumptions_explicit: $ASSUMPTIONS_EXPLICIT"
    echo "  stakeholders_identified: $STAKEHOLDERS_IDENTIFIED"
    echo "  # Overall"
    echo "  confidence: $CONFIDENCE"
    if [[ -n "$GAPS_IDENTIFIED" ]]; then
        echo "  gaps_identified: \"$GAPS_IDENTIFIED\""
    fi
    echo "summary:"
    echo "  confirmed_count: $CONFIRMED_COUNT"
    echo "  total_elements: 6"
    if [[ -n "$MISSING_ITEMS" ]]; then
        echo "  missing_items: \"$MISSING_ITEMS\""
    fi
    echo "  recommendation: $RECOMMENDATION"
} > "$LOG_FILE"

# Create context graph node (TMS integration)
if [[ -d "${PROJECT_ROOT}/.dialogue/context-graph" ]]; then
    mkdir -p "$GRAPH_NODES_DIR" "$GRAPH_EDGES_DIR_ACTOR" "$GRAPH_EDGES_DIR_TRACE"

    # Build summary for node
    SUMMARY="Framing: ${CONFIRMED_COUNT}/6, confidence: ${CONFIDENCE}/5, ${RECOMMENDATION}"

    # Create artifact node for this assessment
    NODE_FILE="${GRAPH_NODES_DIR}/${ID}.yaml"
    {
        echo "id: $ID"
        echo "node_type: ARTIFACT"
        echo "metadata:"
        echo "  artifact_type: ASSESSMENT"
        echo "  assessment_type: PROBLEM_FRAMING"
        echo "  temporal_class: Dynamic"
        echo "  content_type: text/yaml"
        echo "  title: \"Problem Framing Assessment - $(date -u +"%Y-%m-%d")\""
        echo "  summary: \"$SUMMARY\""
        echo "  location_hint: \".dialogue/logs/assessments/${ID}.yaml\""
        echo "  assessor: \"$ASSESSOR\""
        if [[ -n "$PHASE" ]]; then
            echo "  phase: $PHASE"
        fi
        echo "created: \"$TIMESTAMP\""
        echo "updated: \"$TIMESTAMP\""
        echo "status: ACTIVE"
    } > "$NODE_FILE"

    # Create CREATED edge from assessor to assessment
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
        echo "  assessment_type: PROBLEM_FRAMING"
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
            echo "  assessment_type: PROBLEM_FRAMING"
            echo "  confirmed_count: $CONFIRMED_COUNT"
            echo "  confidence: $CONFIDENCE"
            echo "  recommendation: $RECOMMENDATION"
            echo "created: \"$TIMESTAMP\""
            echo "confidence: 1.0"
        } > "$ASSESSES_EDGE_FILE"
    fi
fi

echo "$ID"
