#!/bin/bash
# ==============================================================================
# design-ops-v3-refactored.sh - Instruction-Based Design Ops Pipeline
#
# Philosophy: Script is a VALIDATOR & INSTRUCTION GENERATOR
#   - Validates specs locally (deterministic checks)
#   - Enforces step ordering
#   - Outputs structured instructions for Claude to follow
#   - No API calls, no subprocess LLM invocations
#
# Version: 3.4-refactored
# Date: 2026-01-26
# ==============================================================================

set -e

VERSION="3.4-refactored"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_BASE="${DESIGN_OPS_BASE:-$(dirname "$SCRIPT_DIR")}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
DIM='\033[2m'
NC='\033[0m'

# Configuration
PIPELINE_STATE_DIR="${PIPELINE_STATE_DIR:-$HOME/.design-ops-state}"
INSTRUCTION_OUTPUT_DIR="${INSTRUCTION_OUTPUT_DIR:-.}"

# Source library modules
source "$SCRIPT_DIR/lib/state.sh"
source "$SCRIPT_DIR/lib/validation.sh"
source "$SCRIPT_DIR/lib/instructions.sh"

# ==============================================================================
# CORE VALIDATION FUNCTIONS (LOCAL, NO API)
# ==============================================================================

check_spec_exists() {
    local spec_file="$1"
    [[ -f "$spec_file" ]] || {
        echo -e "${RED}❌ File not found: $spec_file${NC}"
        echo -e "${YELLOW}Hint: Use absolute path or check current directory: $(pwd)${NC}"
        exit 1
    }
}

enforce_step_prerequisites() {
    local command="$1"
    local spec_file="$2"
    local state_file=$(get_state_file_path "$spec_file")
    local state=$(read_pipeline_state "$state_file")

    case "$command" in
        validate)
            if ! echo "$state" | grep -q '"stress-test"'; then
                echo -e "${RED}❌ Prerequisites not met${NC}"
                echo -e "${YELLOW}Must run stress-test first:${NC}"
                echo -e "  ${CYAN}$0 stress-test $spec_file${NC}"
                exit 1
            fi
            ;;
        generate)
            if ! echo "$state" | grep -q '"stress-test"'; then
                echo -e "${RED}❌ Prerequisites not met${NC}"
                echo -e "${YELLOW}Must run stress-test first${NC}"
                exit 1
            fi
            if ! echo "$state" | grep -q '"validate"'; then
                echo -e "${RED}❌ Prerequisites not met${NC}"
                echo -e "${YELLOW}Must run validate first${NC}"
                exit 1
            fi
            ;;
        implement)
            if ! echo "$state" | grep -q '"check"'; then
                echo -e "${RED}❌ Prerequisites not met${NC}"
                echo -e "${YELLOW}Must run check first (after generate)${NC}"
                exit 1
            fi
            ;;
    esac
}

# ==============================================================================
# COMMANDS - INSTRUCTION-BASED
# ==============================================================================

cmd_stress_test() {
    local spec_file="$1"
    local state_file=$(get_state_file_path "$spec_file")

    echo -e "${BLUE}━━━ STRESS-TEST ━━━${NC}"
    echo "Spec: $spec_file"
    echo ""

    check_spec_exists "$spec_file"

    # Run local deterministic checks
    echo -e "${BLUE}Local checks:${NC}"
    check_spec_structure "$spec_file" || {
        echo -e "${RED}❌ Spec structure issues found${NC}"
        exit 1
    }

    # Save state
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    update_pipeline_state "$state_file" "stress-test" "{\"timestamp\":\"$timestamp\",\"status\":\"pass\"}"

    # Output instruction for Claude
    echo ""
    echo -e "${CYAN}Generating instruction for completeness check...${NC}"
    generate_stress_test_instruction "$spec_file" "$INSTRUCTION_OUTPUT_DIR"

    echo ""
    echo -e "${GREEN}✅ Local checks passed${NC}"
    echo -e "${YELLOW}Next step: Review the instruction and check spec completeness${NC}"
}

cmd_validate() {
    local spec_file="$1"
    local state_file=$(get_state_file_path "$spec_file")

    echo -e "${BLUE}━━━ VALIDATE ━━━${NC}"

    check_spec_exists "$spec_file"
    enforce_step_prerequisites "validate" "$spec_file"

    # Run local structure validation
    echo -e "${BLUE}Structure validation:${NC}"
    validate_spec_structure "$spec_file" || {
        echo -e "${RED}❌ Validation failed${NC}"
        exit 1
    }

    # Save state
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    update_pipeline_state "$state_file" "validate" "{\"timestamp\":\"$timestamp\",\"status\":\"pass\"}"

    # Output instruction for Claude
    echo ""
    echo -e "${CYAN}Generating instruction for clarity check...${NC}"
    generate_validate_instruction "$spec_file" "$INSTRUCTION_OUTPUT_DIR"

    echo ""
    echo -e "${GREEN}✅ Structure validation passed${NC}"
    echo -e "${YELLOW}Next step: Review the instruction and validate against invariants${NC}"
}

cmd_generate() {
    local spec_file="$1"
    local state_file=$(get_state_file_path "$spec_file")

    echo -e "${BLUE}━━━ GENERATE PRP ━━━${NC}"

    check_spec_exists "$spec_file"
    enforce_step_prerequisites "generate" "$spec_file"

    # Quick extract from spec (no LLM)
    echo -e "${BLUE}Extracting spec structure...${NC}"
    local prp_id=$(date +%Y-%m-%d)"-$(shuf -i 100-999 -n 1)"
    local domain=$(grep -i "^Domain:" "$spec_file" | cut -d: -f2 | xargs || echo "universal")

    # Save state
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    update_pipeline_state "$state_file" "generate" "{\"timestamp\":\"$timestamp\",\"status\":\"pending\",\"prp_id\":\"$prp_id\"}"

    # Output instruction for Claude
    echo -e "${CYAN}Generating instruction for PRP compilation...${NC}"
    generate_prp_instruction "$spec_file" "$prp_id" "$domain" "$INSTRUCTION_OUTPUT_DIR"

    echo ""
    echo -e "${GREEN}✅ Ready for PRP generation${NC}"
    echo -e "${YELLOW}Next step: Follow the instruction to generate PRP using structured extraction${NC}"
}

cmd_check() {
    local prp_file="$1"
    local state_file=$(get_state_file_path "${prp_file%.*}.spec.md")

    echo -e "${BLUE}━━━ CHECK PRP ━━━${NC}"

    [[ -f "$prp_file" ]] || {
        echo -e "${RED}❌ PRP file not found: $prp_file${NC}"
        exit 1
    }

    # Validate PRP structure
    echo -e "${BLUE}PRP structure validation:${NC}"
    validate_prp_structure "$prp_file" || {
        echo -e "${RED}❌ PRP validation failed${NC}"
        exit 1
    }

    # Save state
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    update_pipeline_state "$state_file" "check" "{\"timestamp\":\"$timestamp\",\"status\":\"pass\"}"

    echo ""
    echo -e "${GREEN}✅ PRP validation passed${NC}"
    echo -e "${YELLOW}Next step: Review PRP, then run 'implement' for Ralph generation${NC}"
}

cmd_implement() {
    local prp_file="$1"
    local output_dir="${2:-.}"

    echo -e "${BLUE}━━━ IMPLEMENT (RALPH GENERATION) ━━━${NC}"

    [[ -f "$prp_file" ]] || {
        echo -e "${RED}❌ PRP file not found: $prp_file${NC}"
        exit 1
    }

    # Extract phase structure from PRP
    echo -e "${BLUE}Extracting PRP structure...${NC}"
    local prp_id=$(grep "^# PRP:" "$prp_file" | cut -d: -f2 | xargs || echo "unknown")
    local phases=$(grep -c "^## Phase" "$prp_file" || echo "0")

    # Generate extraction mapping
    echo -e "${CYAN}Generating instruction for Ralph step generation...${NC}"
    generate_implement_instruction "$prp_file" "$output_dir"

    echo ""
    echo -e "${GREEN}✅ Ready for Ralph generation${NC}"
    echo -e "${YELLOW}Next step: Follow the instruction to generate ralph-steps using structured extraction${NC}"
}

# ==============================================================================
# HELP & USAGE
# ==============================================================================

usage() {
    cat << 'EOF'
Design Ops v3.4 (Refactored) - Instruction-Based Pipeline

PHILOSOPHY: Script validates locally and generates instructions.
            Claude reads instructions and executes.
            No API calls. No subprocess LLM invocations.

USAGE: design-ops-v3-refactored.sh <command> <spec-file>

CORE COMMANDS (in order):

  stress-test <spec>      Check completeness (runs local validation)
  validate <spec>         Check clarity (runs structure validation)
  generate <spec>         Generate PRP (outputs extraction instruction)
  check <prp>             Check PRP (validates structure)
  implement <prp>         Generate Ralph steps (outputs extraction instruction)

WORKFLOW:

  Step 1: ./design-ops-v3-refactored.sh stress-test specs/feature.md
          → Runs deterministic checks
          → Outputs: specs/feature.stress-test-instruction.md
          → You review the instruction, check spec completeness

  Step 2: ./design-ops-v3-refactored.sh validate specs/feature.md
          → Runs structure validation
          → Outputs: specs/feature.validate-instruction.md
          → You validate against 43 invariants

  Step 3: ./design-ops-v3-refactored.sh generate specs/feature.md
          → Extracts spec structure
          → Outputs: specs/feature.generate-instruction.md
          → You compile PRP using structured extraction

  Step 4: ./design-ops-v3-refactored.sh check PRPs/feature.prp.md
          → Validates PRP structure
          → Ready for implementation

  Step 5: ./design-ops-v3-refactored.sh implement PRPs/feature.prp.md
          → Extracts PRP structure
          → Outputs: PRPs/feature.implement-instruction.md
          → You generate ralph-steps using structured extraction

KEY PRINCIPLES:

  • Instruction-based: Script outputs instructions, Claude follows them
  • Local-first: Deterministic checks run locally, no API calls
  • Step ordering: Prerequisites enforced (can't skip steps)
  • Transparent: Instructions are readable files you can review
  • Human-controlled: You decide what to do, not the script

OPTIONS:

  --output <dir>          Output directory for instructions (default: current)
  --help                  Show this help

PHILOSOPHY:

  The script is NOT a judge. It's a CHECKLIST and INSTRUCTION GENERATOR.
  YOU are the agent. The script helps you stay on track.

EOF
    exit 1
}

# ==============================================================================
# MAIN
# ==============================================================================

[[ $# -lt 1 ]] && usage

# Parse flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --output)
            INSTRUCTION_OUTPUT_DIR="$2"
            shift 2
            ;;
        --help|-h)
            usage
            ;;
        stress-test|validate|generate|check|implement)
            COMMAND="$1"
            shift
            break
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            usage
            ;;
    esac
done

# Route to command
case "$COMMAND" in
    stress-test) cmd_stress_test "$@" ;;
    validate) cmd_validate "$@" ;;
    generate) cmd_generate "$@" ;;
    check) cmd_check "$@" ;;
    implement) cmd_implement "$@" ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        usage
        ;;
esac
