#!/bin/bash
# log-assess-phase.sh — Log a phase readiness assessment
# Part of the Dialogue Framework
# Usage: log-assess-phase.sh <assessor> <current_phase> <target_phase> \
#                            <documentation_readiness> <knowledge_transfer_readiness> \
#                            <stakeholder_readiness> <technical_readiness> \
#                            [problem_framing_ref] [blockers] [risks] [context] [tags]
#
# Also creates a context graph node and edges for TMS integration.

set -euo pipefail

# Use Claude's project directory environment variable
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"
LOG_DIR="${PROJECT_ROOT}/.dialogue/logs/assessments"
GRAPH_NODES_DIR="${PROJECT_ROOT}/.dialogue/context-graph/nodes/artifacts"
GRAPH_EDGES_DIR_ACTOR="${PROJECT_ROOT}/.dialogue/context-graph/edges/actor-artifact"
GRAPH_EDGES_DIR_TRACE="${PROJECT_ROOT}/.dialogue/context-graph/edges/traceability"

# Validate required arguments
if [[ $# -lt 7 ]]; then
    echo "Usage: log-assess-phase.sh <assessor> <current_phase> <target_phase> \\" >&2
    echo "                           <documentation_readiness> <knowledge_transfer_readiness> \\" >&2
    echo "                           <stakeholder_readiness> <technical_readiness> \\" >&2
    echo "                           [problem_framing_ref] [blockers] [risks] [context] [tags]" >&2
    echo "" >&2
    echo "  assessor:                    ai:claude | human:<id>" >&2
    echo "  current_phase:               1-7, current SDLC phase" >&2
    echo "  target_phase:                2-7, target phase (must be > current)" >&2
    echo "  documentation_readiness:     1-5" >&2
    echo "  knowledge_transfer_readiness: 1-5" >&2
    echo "  stakeholder_readiness:       1-5" >&2
    echo "  technical_readiness:         1-5" >&2
    echo "  problem_framing_ref:         (optional) ASSESS-... ID of framing assessment" >&2
    echo "  blockers:                    (optional) Blocking issues, comma-separated" >&2
    echo "  risks:                       (optional) Identified risks, comma-separated" >&2
    echo "  context:                     (optional) Situational context" >&2
    echo "  tags:                        (optional) Comma-separated categorisation tags" >&2
    exit 1
fi

ASSESSOR="$1"
CURRENT_PHASE="$2"
TARGET_PHASE="$3"
DOC_READINESS="$4"
KNOWLEDGE_READINESS="$5"
STAKEHOLDER_READINESS="$6"
TECHNICAL_READINESS="$7"
PROBLEM_FRAMING_REF="${8:-}"
BLOCKERS="${9:-}"
RISKS="${10:-}"
CONTEXT="${11:-}"
TAGS="${12:-}"

# Validate phases (1-7)
if ! [[ "$CURRENT_PHASE" =~ ^[1-7]$ ]]; then
    echo "Error: current_phase must be 1-7, got: $CURRENT_PHASE" >&2
    exit 1
fi

if ! [[ "$TARGET_PHASE" =~ ^[2-7]$ ]]; then
    echo "Error: target_phase must be 2-7, got: $TARGET_PHASE" >&2
    exit 1
fi

if [[ "$TARGET_PHASE" -le "$CURRENT_PHASE" ]]; then
    echo "Error: target_phase ($TARGET_PHASE) must be greater than current_phase ($CURRENT_PHASE)" >&2
    exit 1
fi

# Validate readiness scores (1-5)
validate_score() {
    local name="$1"
    local value="$2"
    if ! [[ "$value" =~ ^[1-5]$ ]]; then
        echo "Error: $name must be 1-5, got: $value" >&2
        exit 1
    fi
}

validate_score "documentation_readiness" "$DOC_READINESS"
validate_score "knowledge_transfer_readiness" "$KNOWLEDGE_READINESS"
validate_score "stakeholder_readiness" "$STAKEHOLDER_READINESS"
validate_score "technical_readiness" "$TECHNICAL_READINESS"

# Generate timestamp and ID
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ID="ASSESS-$(date -u +"%Y%m%d-%H%M%S")"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Individual file for this assessment
LOG_FILE="${LOG_DIR}/${ID}.yaml"

# Calculate average score (integer arithmetic, multiply by 10 for precision)
TOTAL=$((DOC_READINESS + KNOWLEDGE_READINESS + STAKEHOLDER_READINESS + TECHNICAL_READINESS))
AVG_X10=$((TOTAL * 10 / 4))

# Check for any dimension at 1 (critical failure)
HAS_CRITICAL_FAILURE=false
if [[ "$DOC_READINESS" -eq 1 || "$KNOWLEDGE_READINESS" -eq 1 || "$STAKEHOLDER_READINESS" -eq 1 || "$TECHNICAL_READINESS" -eq 1 ]]; then
    HAS_CRITICAL_FAILURE=true
fi

# Determine recommendation
if [[ "$HAS_CRITICAL_FAILURE" == "true" ]]; then
    RECOMMENDATION="DEFER"
    RATIONALE="Critical failure: one or more dimensions scored 1"
elif [[ -n "$BLOCKERS" ]]; then
    # Blockers present - max is PROCEED_WITH_CAUTION
    if [[ $AVG_X10 -ge 30 ]]; then
        RECOMMENDATION="PROCEED_WITH_CAUTION"
        RATIONALE="Blockers present; average score ${AVG_X10}/50 meets threshold but requires attention"
    else
        RECOMMENDATION="DEFER"
        RATIONALE="Blockers present and average score ${AVG_X10}/50 below threshold"
    fi
elif [[ -z "$PROBLEM_FRAMING_REF" ]]; then
    # No problem framing - max is PROCEED_WITH_CAUTION
    if [[ $AVG_X10 -ge 40 ]]; then
        RECOMMENDATION="PROCEED_WITH_CAUTION"
        RATIONALE="Missing problem framing assessment; scores are high but framing not validated"
    elif [[ $AVG_X10 -ge 30 ]]; then
        RECOMMENDATION="PROCEED_WITH_CAUTION"
        RATIONALE="Missing problem framing assessment; average score ${AVG_X10}/50"
    else
        RECOMMENDATION="DEFER"
        RATIONALE="Missing problem framing assessment and average score ${AVG_X10}/50 below threshold"
    fi
elif [[ $AVG_X10 -ge 40 ]]; then
    RECOMMENDATION="PROCEED"
    RATIONALE="All dimensions satisfactory; average score ${AVG_X10}/50"
elif [[ $AVG_X10 -ge 30 ]]; then
    RECOMMENDATION="PROCEED_WITH_CAUTION"
    RATIONALE="Minor gaps; average score ${AVG_X10}/50"
else
    RECOMMENDATION="DEFER"
    RATIONALE="Significant gaps; average score ${AVG_X10}/50 below threshold"
fi

# Phase names for display (using function for compatibility)
# Aligned with concept_seven-phase-sdlc.md canonical names
get_phase_name() {
    case "$1" in
        1) echo "Initiation/Conception" ;;
        2) echo "Planning" ;;
        3) echo "Analysis/Requirements" ;;
        4) echo "Design/Architecture" ;;
        5) echo "Implementation/Construction" ;;
        6) echo "Testing/Validation" ;;
        7) echo "Deployment/Operations" ;;
        *) echo "Unknown" ;;
    esac
}

# Phase tacit knowledge percentage (from integration_phase-specific-composition.md)
# Used to inform DEFER remediation guidance
get_phase_tacit_pct() {
    case "$1" in
        1) echo 75 ;;  # Initiation: 75% tacit
        2) echo 55 ;;  # Planning: 55% tacit
        3) echo 50 ;;  # Requirements: 50% tacit
        4) echo 40 ;;  # Design: 40% tacit
        5) echo 35 ;;  # Implementation: 35% tacit
        6) echo 30 ;;  # Testing: 30% tacit
        7) echo 30 ;;  # Operations: 30% tacit
        *) echo 50 ;;  # Default to balanced
    esac
}

# Determine recommended remediation approach based on tacit % and gap type
# Returns: DIALOGUE, MIXED, or ARTIFACT
get_remediation_approach() {
    local tacit_pct="$1"
    local gap_type="$2"

    # High tacit phases (>50%) bias toward dialogue
    # Low tacit phases (<=35%) bias toward artifact
    # Gap type modifies the base approach

    if [[ "$tacit_pct" -ge 55 ]]; then
        # High tacit phase - dialogue dominant
        case "$gap_type" in
            documentation) echo "MIXED" ;;      # Even doc gaps need dialogue in high-tacit
            knowledge)     echo "DIALOGUE" ;;
            stakeholder)   echo "DIALOGUE" ;;
            technical)     echo "MIXED" ;;
            *)             echo "DIALOGUE" ;;
        esac
    elif [[ "$tacit_pct" -ge 40 ]]; then
        # Medium tacit phase - balanced
        case "$gap_type" in
            documentation) echo "MIXED" ;;
            knowledge)     echo "DIALOGUE" ;;
            stakeholder)   echo "MIXED" ;;
            technical)     echo "MIXED" ;;
            *)             echo "MIXED" ;;
        esac
    else
        # Low tacit phase - artifact dominant
        case "$gap_type" in
            documentation) echo "ARTIFACT" ;;
            knowledge)     echo "MIXED" ;;      # Even in low-tacit, knowledge needs some dialogue
            stakeholder)   echo "MIXED" ;;
            technical)     echo "ARTIFACT" ;;
            *)             echo "ARTIFACT" ;;
        esac
    fi
}

# Get specific remediation actions based on approach and gap
get_remediation_actions() {
    local approach="$1"
    local gap_type="$2"
    local phase="$3"

    case "$gap_type" in
        documentation)
            if [[ "$approach" == "DIALOGUE" || "$approach" == "MIXED" ]]; then
                echo "Convene working session to articulate missing documentation"
                echo "Elicit tacit understanding from key stakeholders"
            fi
            if [[ "$approach" == "ARTIFACT" || "$approach" == "MIXED" ]]; then
                echo "Review and complete required artifacts"
                echo "Update specifications with missing details"
            fi
            ;;
        knowledge)
            echo "Conduct knowledge transfer sessions with domain experts"
            echo "Pair with experienced team members"
            if [[ "$phase" -le 3 ]]; then
                echo "Facilitate stakeholder interviews to capture tacit understanding"
            else
                echo "Review code/design with original authors"
            fi
            ;;
        stakeholder)
            echo "Convene stakeholder alignment workshop"
            echo "Clarify and document areas of disagreement"
            if [[ "$phase" -le 2 ]]; then
                echo "Re-establish shared vision and success criteria"
            else
                echo "Review requirements with stakeholders for validation"
            fi
            ;;
        technical)
            if [[ "$approach" == "DIALOGUE" || "$approach" == "MIXED" ]]; then
                echo "Discuss technical constraints with architecture team"
            fi
            echo "Resolve blocking dependencies"
            echo "Update technical feasibility assessment"
            ;;
    esac
}

CURRENT_PHASE_NAME=$(get_phase_name "$CURRENT_PHASE")
TARGET_PHASE_NAME=$(get_phase_name "$TARGET_PHASE")

# If DEFER, calculate remediation guidance
DEFER_GUIDANCE=""
if [[ "$RECOMMENDATION" == "DEFER" ]]; then
    # Get phase tacit percentage
    PHASE_TACIT_PCT=$(get_phase_tacit_pct "$CURRENT_PHASE")

    # Identify primary gap (lowest scoring dimension)
    PRIMARY_GAP="documentation"
    PRIMARY_GAP_SCORE=$DOC_READINESS

    if [[ "$KNOWLEDGE_READINESS" -lt "$PRIMARY_GAP_SCORE" ]]; then
        PRIMARY_GAP="knowledge"
        PRIMARY_GAP_SCORE=$KNOWLEDGE_READINESS
    fi
    if [[ "$STAKEHOLDER_READINESS" -lt "$PRIMARY_GAP_SCORE" ]]; then
        PRIMARY_GAP="stakeholder"
        PRIMARY_GAP_SCORE=$STAKEHOLDER_READINESS
    fi
    if [[ "$TECHNICAL_READINESS" -lt "$PRIMARY_GAP_SCORE" ]]; then
        PRIMARY_GAP="technical"
        PRIMARY_GAP_SCORE=$TECHNICAL_READINESS
    fi

    # Identify secondary gaps (any dimension scoring <= 2)
    SECONDARY_GAPS=""
    if [[ "$DOC_READINESS" -le 2 && "$PRIMARY_GAP" != "documentation" ]]; then
        SECONDARY_GAPS="${SECONDARY_GAPS}documentation,"
    fi
    if [[ "$KNOWLEDGE_READINESS" -le 2 && "$PRIMARY_GAP" != "knowledge" ]]; then
        SECONDARY_GAPS="${SECONDARY_GAPS}knowledge,"
    fi
    if [[ "$STAKEHOLDER_READINESS" -le 2 && "$PRIMARY_GAP" != "stakeholder" ]]; then
        SECONDARY_GAPS="${SECONDARY_GAPS}stakeholder,"
    fi
    if [[ "$TECHNICAL_READINESS" -le 2 && "$PRIMARY_GAP" != "technical" ]]; then
        SECONDARY_GAPS="${SECONDARY_GAPS}technical,"
    fi
    # Remove trailing comma
    SECONDARY_GAPS="${SECONDARY_GAPS%,}"

    # Determine recommended approach
    REMEDIATION_APPROACH=$(get_remediation_approach "$PHASE_TACIT_PCT" "$PRIMARY_GAP")

    # Flag that we have defer guidance to output
    DEFER_GUIDANCE="yes"
fi

# Build YAML entry
{
    echo "id: $ID"
    echo "timestamp: \"$TIMESTAMP\""
    echo "assessment_type: PHASE_READINESS"
    echo "assessor: \"$ASSESSOR\""
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
    echo "  current_phase: $CURRENT_PHASE"
    echo "  current_phase_name: \"$CURRENT_PHASE_NAME\""
    echo "  target_phase: $TARGET_PHASE"
    echo "  target_phase_name: \"$TARGET_PHASE_NAME\""
    echo "  # Component assessment references"
    echo "  component_assessments:"
    if [[ -n "$PROBLEM_FRAMING_REF" ]]; then
        echo "    problem_framing: \"$PROBLEM_FRAMING_REF\""
    else
        echo "    problem_framing: null"
    fi
    echo "    stakeholder_alignment: null  # FW-041 not yet implemented"
    echo "    ttkm: null  # FW-041 not yet implemented"
    echo "    daily_checks: []  # TODO: auto-populate from recent assessments"
    echo "  # Readiness scores (1-5)"
    echo "  documentation_readiness: $DOC_READINESS"
    echo "  knowledge_transfer_readiness: $KNOWLEDGE_READINESS"
    echo "  stakeholder_readiness: $STAKEHOLDER_READINESS"
    echo "  technical_readiness: $TECHNICAL_READINESS"
    echo "  # Recommendation"
    echo "  recommendation: $RECOMMENDATION"
    echo "  rationale: \"$RATIONALE\""
    if [[ -n "$BLOCKERS" ]]; then
        # Convert comma-separated blockers to YAML array
        IFS=',' read -ra BLOCKER_ARRAY <<< "$BLOCKERS"
        printf '  blockers: ['
        for i in "${!BLOCKER_ARRAY[@]}"; do
            if [[ $i -gt 0 ]]; then printf ', '; fi
            printf '"%s"' "$(echo "${BLOCKER_ARRAY[$i]}" | xargs)"
        done
        printf ']\n'
    else
        echo "  blockers: []"
    fi
    if [[ -n "$RISKS" ]]; then
        # Convert comma-separated risks to YAML array
        IFS=',' read -ra RISK_ARRAY <<< "$RISKS"
        printf '  risks: ['
        for i in "${!RISK_ARRAY[@]}"; do
            if [[ $i -gt 0 ]]; then printf ', '; fi
            printf '"%s"' "$(echo "${RISK_ARRAY[$i]}" | xargs)"
        done
        printf ']\n'
    else
        echo "  risks: []"
    fi
    # DEFER remediation guidance (only when recommendation is DEFER)
    if [[ -n "$DEFER_GUIDANCE" ]]; then
        echo "  # Remediation guidance for DEFER recommendation"
        echo "  defer_guidance:"
        echo "    primary_gap: $PRIMARY_GAP"
        echo "    primary_gap_score: $PRIMARY_GAP_SCORE"
        if [[ -n "$SECONDARY_GAPS" ]]; then
            # Convert to YAML array
            IFS=',' read -ra SEC_GAP_ARRAY <<< "$SECONDARY_GAPS"
            printf '    secondary_gaps: ['
            for i in "${!SEC_GAP_ARRAY[@]}"; do
                if [[ $i -gt 0 ]]; then printf ', '; fi
                printf '"%s"' "${SEC_GAP_ARRAY[$i]}"
            done
            printf ']\n'
        else
            echo "    secondary_gaps: []"
        fi
        echo "    phase_tacit_percentage: $PHASE_TACIT_PCT"
        echo "    recommended_approach: $REMEDIATION_APPROACH"
        echo "    specific_actions:"
        # Get and output remediation actions
        while IFS= read -r action; do
            if [[ -n "$action" ]]; then
                echo "      - \"$action\""
            fi
        done < <(get_remediation_actions "$REMEDIATION_APPROACH" "$PRIMARY_GAP" "$CURRENT_PHASE")
        echo "    restart_point:"
        echo "      phase: $CURRENT_PHASE"
        echo "      phase_name: \"$CURRENT_PHASE_NAME\""
        echo "      focus: \"Address $PRIMARY_GAP gaps before re-assessing\""
    fi
    echo "  # Approval (to be filled after human review)"
    echo "  approved_by: null"
    echo "  approval_timestamp: null"
    echo "  approval_conditions: null"
    echo "summary:"
    echo "  average_score: \"$(echo "scale=1; $TOTAL / 4" | bc)\""
    echo "  recommendation: $RECOMMENDATION"
    echo "  transition: \"Phase $CURRENT_PHASE -> Phase $TARGET_PHASE\""
} > "$LOG_FILE"

# Create context graph node (TMS integration)
if [[ -d "${PROJECT_ROOT}/.dialogue/context-graph" ]]; then
    mkdir -p "$GRAPH_NODES_DIR" "$GRAPH_EDGES_DIR_ACTOR" "$GRAPH_EDGES_DIR_TRACE"

    # Build summary for node
    AVG_DISPLAY=$(echo "scale=1; $TOTAL / 4" | bc)
    SUMMARY="Phase $CURRENT_PHASE->$TARGET_PHASE: ${RECOMMENDATION}, avg: ${AVG_DISPLAY}/5"

    # Create artifact node for this assessment
    NODE_FILE="${GRAPH_NODES_DIR}/${ID}.yaml"
    {
        echo "id: $ID"
        echo "node_type: ARTIFACT"
        echo "metadata:"
        echo "  artifact_type: ASSESSMENT"
        echo "  assessment_type: PHASE_READINESS"
        echo "  temporal_class: Standing"
        echo "  content_type: text/yaml"
        echo "  title: \"Phase Readiness - ${CURRENT_PHASE_NAME} -> ${TARGET_PHASE_NAME}\""
        echo "  summary: \"$SUMMARY\""
        echo "  location_hint: \".dialogue/logs/assessments/${ID}.yaml\""
        echo "  assessor: \"$ASSESSOR\""
        echo "  current_phase: $CURRENT_PHASE"
        echo "  target_phase: $TARGET_PHASE"
        echo "  recommendation: $RECOMMENDATION"
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
        echo "  assessment_type: PHASE_READINESS"
        echo "created: \"$TIMESTAMP\""
        echo "confidence: 1.0"
    } > "$EDGE_FILE"

    # Create ASSESSES edge to problem framing if referenced
    if [[ -n "$PROBLEM_FRAMING_REF" ]]; then
        ASSESSES_EDGE_ID="assesses-${ID}-${PROBLEM_FRAMING_REF}"
        ASSESSES_EDGE_FILE="${GRAPH_EDGES_DIR_TRACE}/${ASSESSES_EDGE_ID}.yaml"
        {
            echo "id: $ASSESSES_EDGE_ID"
            echo "source: $ID"
            echo "target: \"$PROBLEM_FRAMING_REF\""
            echo "edge_type: REFERENCES"
            echo "metadata:"
            echo "  relationship: component_assessment"
            echo "  component_type: problem_framing"
            echo "created: \"$TIMESTAMP\""
            echo "confidence: 1.0"
        } > "$ASSESSES_EDGE_FILE"
    fi
fi

echo "$ID"
