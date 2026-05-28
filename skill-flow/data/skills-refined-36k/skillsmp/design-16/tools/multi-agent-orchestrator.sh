#!/bin/bash
#
# multi-agent-orchestrator.sh - Coordinate multi-agent Design Ops workflow
#
# Usage:
#   Full pipeline:    ./tools/multi-agent-orchestrator.sh --spec <file> --domain <domain>
#   Analysis only:    ./tools/multi-agent-orchestrator.sh --spec <file> --phase analysis
#   Generate only:    ./tools/multi-agent-orchestrator.sh --spec <file> --phase generate --analysis <file> --validation <file>
#   Review only:      ./tools/multi-agent-orchestrator.sh --prp <file> --phase review
#   Retrospective:    ./tools/multi-agent-orchestrator.sh --prp <file> --phase retrospective --outcome <summary>
#
# Options:
#   --spec <file>         Spec file to process
#   --prp <file>          PRP file (for review/retrospective)
#   --domain <domain>     Target domain (api, database, security, etc.)
#   --phase <phase>       Run specific phase only (analysis, generate, review, retrospective)
#   --output <dir>        Output directory (default: ./output)
#   --analysis <file>     Pre-existing analysis.json (for generate phase)
#   --validation <file>   Pre-existing validation.json (for generate phase)
#   --outcome <summary>   Implementation outcome (for retrospective)
#   --resume <file>       Resume from checkpoint
#   --skip <agent>        Skip specific agent
#   --force               Force proceed despite warnings
#   --verbose, -v         Show detailed output

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$SCRIPT_DIR")"
AGENTS_DIR="$DESIGN_OPS_ROOT/agents"

# Defaults
SPEC_FILE=""
PRP_FILE=""
DOMAIN="general"
PHASE="full"
OUTPUT_DIR="./output"
ANALYSIS_FILE=""
VALIDATION_FILE=""
OUTCOME=""
RESUME_FILE=""
SKIP_AGENT=""
FORCE=false
VERBOSE=false

# Timeouts (seconds)
TIMEOUT_ANALYSIS=30
TIMEOUT_VALIDATION=60
TIMEOUT_GENERATION=120
TIMEOUT_REVIEW=30
TIMEOUT_RETROSPECTIVE=60

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --spec)
            SPEC_FILE="$2"
            shift 2
            ;;
        --prp)
            PRP_FILE="$2"
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --phase)
            PHASE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --analysis)
            ANALYSIS_FILE="$2"
            shift 2
            ;;
        --validation)
            VALIDATION_FILE="$2"
            shift 2
            ;;
        --outcome)
            OUTCOME="$2"
            shift 2
            ;;
        --resume)
            RESUME_FILE="$2"
            shift 2
            ;;
        --skip)
            SKIP_AGENT="$2"
            shift 2
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            cat << 'EOF'
Multi-Agent Design Ops Orchestrator

Usage:
  Full pipeline:    ./tools/multi-agent-orchestrator.sh --spec <file> --domain <domain>
  Analysis only:    ./tools/multi-agent-orchestrator.sh --spec <file> --phase analysis
  Generate only:    ./tools/multi-agent-orchestrator.sh --spec <file> --phase generate --analysis <file> --validation <file>
  Review only:      ./tools/multi-agent-orchestrator.sh --prp <file> --phase review

Options:
  --spec <file>         Spec file to process
  --prp <file>          PRP file (for review/retrospective)
  --domain <domain>     Target domain (api, database, security, etc.)
  --phase <phase>       Run specific phase (analysis, generate, review, retrospective, full)
  --output <dir>        Output directory (default: ./output)
  --analysis <file>     Pre-existing analysis.json
  --validation <file>   Pre-existing validation.json
  --outcome <summary>   Implementation outcome (for retrospective)
  --skip <agent>        Skip specific agent
  --force               Force proceed despite warnings
  --verbose, -v         Show detailed output

Phases:
  analysis       Run spec-analyst and validator in parallel
  generate       Generate PRP from analysis results
  review         Review existing PRP for quality
  retrospective  Create retrospective from completed PRP
  full           Run complete pipeline (default)
EOF
            exit 0
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
        *)
            echo -e "${RED}Unknown argument: $1${NC}"
            exit 1
            ;;
    esac
done

# ============================================================================
# Helper Functions
# ============================================================================

log() {
    echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date +%H:%M:%S)] ✓${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date +%H:%M:%S)] ✗${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date +%H:%M:%S)] !${NC} $1"
}

run_agent() {
    local agent_name=$1
    local agent_script=$2
    shift 2
    local args=("$@")

    if [[ "$SKIP_AGENT" == "$agent_name" ]]; then
        log_warning "Skipping agent: $agent_name"
        return 0
    fi

    log "Running $agent_name..."

    if [[ "$VERBOSE" == "true" ]]; then
        "$agent_script" "${args[@]}"
    else
        "$agent_script" "${args[@]}" > /dev/null 2>&1
    fi

    local exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        log_success "$agent_name completed"
    else
        log_error "$agent_name failed (exit code: $exit_code)"
    fi

    return $exit_code
}

save_checkpoint() {
    local phase=$1
    local checkpoint_file="$OUTPUT_DIR/checkpoint.json"

    cat > "$checkpoint_file" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "phase": "$phase",
  "spec_file": "$SPEC_FILE",
  "prp_file": "$PRP_FILE",
  "domain": "$DOMAIN",
  "analysis_file": "$ANALYSIS_FILE",
  "validation_file": "$VALIDATION_FILE"
}
EOF

    [[ "$VERBOSE" == "true" ]] && log "Checkpoint saved: $checkpoint_file"
}

# ============================================================================
# Main
# ============================================================================

echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║      MULTI-AGENT DESIGN OPS ORCHESTRATOR                      ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# ============================================================================
# Resume from checkpoint if specified
# ============================================================================
if [[ -n "$RESUME_FILE" ]] && [[ -f "$RESUME_FILE" ]]; then
    log "Resuming from checkpoint: $RESUME_FILE"

    SPEC_FILE=$(jq -r '.spec_file // empty' "$RESUME_FILE")
    PRP_FILE=$(jq -r '.prp_file // empty' "$RESUME_FILE")
    DOMAIN=$(jq -r '.domain // "general"' "$RESUME_FILE")
    ANALYSIS_FILE=$(jq -r '.analysis_file // empty' "$RESUME_FILE")
    VALIDATION_FILE=$(jq -r '.validation_file // empty' "$RESUME_FILE")
    PHASE=$(jq -r '.phase // "full"' "$RESUME_FILE")

    log "  Spec: $SPEC_FILE"
    log "  Phase: $PHASE"
fi

# ============================================================================
# Validate inputs based on phase
# ============================================================================
case $PHASE in
    analysis|full)
        if [[ -z "$SPEC_FILE" ]] || [[ ! -f "$SPEC_FILE" ]]; then
            log_error "Spec file required for $PHASE phase"
            exit 1
        fi
        ;;
    generate)
        if [[ -z "$SPEC_FILE" ]] || [[ ! -f "$SPEC_FILE" ]]; then
            log_error "Spec file required for generate phase"
            exit 1
        fi
        if [[ -z "$ANALYSIS_FILE" ]] || [[ ! -f "$ANALYSIS_FILE" ]]; then
            log_error "Analysis file required for generate phase (--analysis)"
            exit 1
        fi
        if [[ -z "$VALIDATION_FILE" ]] || [[ ! -f "$VALIDATION_FILE" ]]; then
            log_error "Validation file required for generate phase (--validation)"
            exit 1
        fi
        ;;
    review|retrospective)
        if [[ -z "$PRP_FILE" ]] || [[ ! -f "$PRP_FILE" ]]; then
            log_error "PRP file required for $PHASE phase"
            exit 1
        fi
        if [[ "$PHASE" == "retrospective" ]] && [[ -z "$OUTCOME" ]]; then
            log_error "Outcome summary required for retrospective phase (--outcome)"
            exit 1
        fi
        ;;
esac

log "Phase:  $PHASE"
log "Domain: $DOMAIN"
log "Output: $OUTPUT_DIR"
echo ""

# ============================================================================
# Phase: Analysis (spec-analyst + validator in parallel)
# ============================================================================
if [[ "$PHASE" == "analysis" ]] || [[ "$PHASE" == "full" ]]; then
    echo -e "${CYAN}━━━ Phase 1: Analysis ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    ANALYSIS_FILE="$OUTPUT_DIR/analysis.json"
    VALIDATION_FILE="$OUTPUT_DIR/validation.json"

    # Run spec-analyst and validator in parallel using background processes
    log "Starting parallel analysis..."

    ANALYST_PID=""
    VALIDATOR_PID=""
    ANALYST_EXIT=0
    VALIDATOR_EXIT=0

    # Start spec-analyst in background
    (
        bash "$AGENTS_DIR/spec-analyst.sh" "$SPEC_FILE" \
            --domain "$DOMAIN" \
            --output "$OUTPUT_DIR" \
            ${VERBOSE:+--verbose}
    ) &
    ANALYST_PID=$!

    # Start validator in background
    (
        bash "$AGENTS_DIR/validator.sh" "$SPEC_FILE" \
            --domain "$DOMAIN" \
            --output "$OUTPUT_DIR" \
            ${VERBOSE:+--verbose}
    ) &
    VALIDATOR_PID=$!

    # Wait for both to complete
    wait $ANALYST_PID || ANALYST_EXIT=$?
    wait $VALIDATOR_PID || VALIDATOR_EXIT=$?

    if [[ $ANALYST_EXIT -ne 0 ]]; then
        log_error "spec-analyst failed"
        [[ "$FORCE" != "true" ]] && exit 1
    else
        log_success "spec-analyst completed"
    fi

    if [[ $VALIDATOR_EXIT -ne 0 ]]; then
        if [[ $VALIDATOR_EXIT -eq 2 ]]; then
            log_error "validator found critical violations"
            [[ "$FORCE" != "true" ]] && exit 1
        else
            log_warning "validator completed with warnings"
        fi
    else
        log_success "validator completed"
    fi

    save_checkpoint "analysis"
    echo ""

    # Extract results
    if [[ -f "$ANALYSIS_FILE" ]]; then
        COMPLETENESS=$(jq -r '.completeness_score' "$ANALYSIS_FILE")
        THINKING=$(jq -r '.thinking_level.recommended' "$ANALYSIS_FILE")
        log "Analysis results: Completeness=$COMPLETENESS%, Thinking=$THINKING"
    fi

    if [[ -f "$VALIDATION_FILE" ]]; then
        CONFIDENCE=$(jq -r '.confidence_score' "$VALIDATION_FILE")
        VIOLATIONS=$(jq -r '.summary.critical + .summary.major' "$VALIDATION_FILE")
        log "Validation results: Confidence=$CONFIDENCE%, Violations=$VIOLATIONS"
    fi

    echo ""
fi

# ============================================================================
# Phase: Generation
# ============================================================================
if [[ "$PHASE" == "generate" ]] || [[ "$PHASE" == "full" ]]; then
    echo -e "${CYAN}━━━ Phase 2: Generation ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # Set default paths if not provided
    [[ -z "$ANALYSIS_FILE" ]] && ANALYSIS_FILE="$OUTPUT_DIR/analysis.json"
    [[ -z "$VALIDATION_FILE" ]] && VALIDATION_FILE="$OUTPUT_DIR/validation.json"

    # Verify inputs exist
    if [[ ! -f "$ANALYSIS_FILE" ]] || [[ ! -f "$VALIDATION_FILE" ]]; then
        log_error "Analysis or validation file missing. Run analysis phase first."
        exit 1
    fi

    # Check confidence threshold
    CONFIDENCE=$(jq -r '.confidence_score' "$VALIDATION_FILE")
    if [[ $CONFIDENCE -lt 50 ]] && [[ "$FORCE" != "true" ]]; then
        log_warning "Confidence score ($CONFIDENCE%) is below threshold (50%)"
        log_warning "Use --force to proceed anyway"
        exit 1
    fi

    run_agent "prp-generator" "$AGENTS_DIR/prp-generator.sh" \
        "$SPEC_FILE" \
        --analysis "$ANALYSIS_FILE" \
        --validation "$VALIDATION_FILE" \
        --output "$OUTPUT_DIR"

    # Find generated PRP
    PRP_FILE=$(ls -t "$OUTPUT_DIR"/prp-*.md 2>/dev/null | head -1 || true)

    if [[ -z "$PRP_FILE" ]]; then
        log_error "PRP generation failed - no output file"
        exit 1
    fi

    save_checkpoint "generate"
    echo ""
fi

# ============================================================================
# Phase: Review
# ============================================================================
if [[ "$PHASE" == "review" ]] || [[ "$PHASE" == "full" ]]; then
    echo -e "${CYAN}━━━ Phase 3: Review ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # Find PRP if not set
    if [[ -z "$PRP_FILE" ]]; then
        PRP_FILE=$(ls -t "$OUTPUT_DIR"/prp-*.md 2>/dev/null | head -1 || true)
    fi

    if [[ -z "$PRP_FILE" ]] || [[ ! -f "$PRP_FILE" ]]; then
        log_error "No PRP file found for review"
        exit 1
    fi

    run_agent "reviewer" "$AGENTS_DIR/reviewer.sh" \
        "$PRP_FILE" \
        --output "$OUTPUT_DIR"

    REVIEW_EXIT=$?
    REVIEW_FILE="$OUTPUT_DIR/review.json"

    if [[ -f "$REVIEW_FILE" ]]; then
        REVIEW_STATUS=$(jq -r '.status' "$REVIEW_FILE")
        REVIEW_SCORE=$(jq -r '.score' "$REVIEW_FILE")

        case $REVIEW_STATUS in
            approved)
                log_success "PRP approved (score: $REVIEW_SCORE)"
                ;;
            needs_work)
                log_warning "PRP needs work (score: $REVIEW_SCORE)"
                if [[ "$FORCE" != "true" ]]; then
                    log "Review issues in: $REVIEW_FILE"
                    exit 1
                fi
                ;;
            rejected)
                log_error "PRP rejected (score: $REVIEW_SCORE)"
                exit 1
                ;;
        esac
    fi

    save_checkpoint "review"
    echo ""
fi

# ============================================================================
# Phase: Retrospective
# ============================================================================
if [[ "$PHASE" == "retrospective" ]]; then
    echo -e "${CYAN}━━━ Phase 4: Retrospective ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    run_agent "retrospective" "$AGENTS_DIR/retrospective.sh" \
        "$PRP_FILE" \
        --outcome "$OUTCOME" \
        --domain "$DOMAIN" \
        --output "$OUTPUT_DIR"

    save_checkpoint "retrospective"
    echo ""
fi

# ============================================================================
# Summary
# ============================================================================
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                      ORCHESTRATION COMPLETE                   ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Output Directory:${NC} $OUTPUT_DIR"
echo ""
echo -e "${BLUE}Generated Files:${NC}"

[[ -f "$OUTPUT_DIR/analysis.json" ]] && echo "  - analysis.json"
[[ -f "$OUTPUT_DIR/validation.json" ]] && echo "  - validation.json"
[[ -n "$PRP_FILE" ]] && [[ -f "$PRP_FILE" ]] && echo "  - $(basename "$PRP_FILE")"
[[ -f "$OUTPUT_DIR/review.json" ]] && echo "  - review.json"
[[ -f "$OUTPUT_DIR/checkpoint.json" ]] && echo "  - checkpoint.json"

# List any retrospective files
for f in "$OUTPUT_DIR"/retrospective-*.md "$OUTPUT_DIR"/invariant-proposals.json; do
    [[ -f "$f" ]] && echo "  - $(basename "$f")"
done

echo ""

# Final status
if [[ -f "$OUTPUT_DIR/review.json" ]]; then
    STATUS=$(jq -r '.status' "$OUTPUT_DIR/review.json")
    case $STATUS in
        approved)
            echo -e "${GREEN}Status: PRP APPROVED - Ready for implementation${NC}"
            ;;
        needs_work)
            echo -e "${YELLOW}Status: PRP NEEDS WORK - Review feedback and iterate${NC}"
            ;;
        rejected)
            echo -e "${RED}Status: PRP REJECTED - Significant rework required${NC}"
            ;;
    esac
elif [[ -f "$VALIDATION_FILE" ]]; then
    CONFIDENCE=$(jq -r '.confidence_score' "$VALIDATION_FILE")
    echo -e "${BLUE}Validation Confidence: ${CONFIDENCE}%${NC}"
fi

echo ""
exit 0
