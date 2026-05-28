#!/bin/bash
# spec-to-prp-llm.sh - LLM-powered spec to PRP transformation
#
# Uses Claude CLI with few-shot prompting for metadata extraction
# and chain-of-thought for intelligent transformation.
#
# Usage:
#   ./spec-to-prp-llm.sh <spec-file.md> [options]
#
# Options:
#   --output <file>     Output file path
#   --model <model>     Claude model: haiku (fast), sonnet (default), opus (best)
#   --max-retries <n>   Max review/revision cycles (default: 2)
#   --skip-review       Skip intelligent review phase
#   --verbose           Show detailed progress
#   --dry-run           Show prompts without executing

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/../prompts"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"
OUTPUT_DIR="$SCRIPT_DIR/../output"

# Defaults
MODEL_EXTRACT="haiku"      # Fast model for metadata extraction
MODEL_TRANSFORM="sonnet"   # Smart model for transformation
MODEL_REVIEW="haiku"       # Fast model for structured review
MAX_RETRIES=2
SKIP_REVIEW=false
VERBOSE=false
DRY_RUN=false

# Usage
usage() {
    echo "Usage: $0 <spec-file.md> [options]"
    echo ""
    echo "LLM-powered spec to PRP transformation using Claude CLI."
    echo "Uses tiered models: haiku for extraction/review, sonnet for transformation."
    echo ""
    echo "Options:"
    echo "  --output <file>        Output file path (default: output/<spec-name>-prp.md)"
    echo "  --model-extract <m>    Model for metadata extraction (default: haiku)"
    echo "  --model-transform <m>  Model for transformation (default: sonnet)"
    echo "  --model-review <m>     Model for review (default: haiku)"
    echo "  --all-haiku            Use haiku for all phases (fast, lower quality)"
    echo "  --all-sonnet           Use sonnet for all phases (slower, higher quality)"
    echo "  --max-retries <n>      Max review/revision cycles (default: 2)"
    echo "  --skip-review          Skip intelligent review phase"
    echo "  --verbose              Show detailed progress"
    echo "  --dry-run              Show prompts without executing"
    echo ""
    echo "Examples:"
    echo "  $0 specs/my-feature.md"
    echo "  $0 specs/api-spec.md --all-haiku --output PRPs/api-prp.md"
    echo "  $0 specs/*.md  # Process multiple (use batch-convert.sh for parallel)"
    exit 1
}

# Check for claude CLI
check_claude_cli() {
    if ! command -v claude &> /dev/null; then
        echo -e "${RED}ERROR: Claude CLI not found.${NC}"
        echo "Install Claude Code: https://claude.ai/code"
        exit 1
    fi
}

# Call Claude CLI with prompt
# Usage: call_claude "prompt" "model"
call_claude() {
    local prompt="$1"
    local model="${2:-haiku}"
    local model_flag=""

    case "$model" in
        "haiku")
            model_flag="--model claude-3-5-haiku-latest"
            ;;
        "sonnet")
            model_flag="--model claude-sonnet-4-20250514"
            ;;
        "opus")
            model_flag="--model claude-opus-4-20250514"
            ;;
    esac

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}[DRY RUN] Would call Claude ($model) with:${NC}"
        echo "$prompt" | head -50
        echo "..."
        return 0
    fi

    # Call Claude CLI with prompt via stdin
    echo "$prompt" | claude $model_flag --print 2>/dev/null
}

# Parse arguments
if [[ $# -lt 1 ]]; then
    usage
fi

SPEC_FILE="$1"
shift

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --model-extract)
            MODEL_EXTRACT="$2"
            shift 2
            ;;
        --model-transform)
            MODEL_TRANSFORM="$2"
            shift 2
            ;;
        --model-review)
            MODEL_REVIEW="$2"
            shift 2
            ;;
        --all-haiku)
            MODEL_EXTRACT="haiku"
            MODEL_TRANSFORM="haiku"
            MODEL_REVIEW="haiku"
            shift
            ;;
        --all-sonnet)
            MODEL_EXTRACT="sonnet"
            MODEL_TRANSFORM="sonnet"
            MODEL_REVIEW="sonnet"
            shift
            ;;
        --max-retries)
            MAX_RETRIES="$2"
            shift 2
            ;;
        --skip-review)
            SKIP_REVIEW=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            VERBOSE=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Validate spec file
if [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}ERROR: Spec file not found: $SPEC_FILE${NC}"
    exit 1
fi

# Set output file
SPEC_BASENAME=$(basename "$SPEC_FILE" .md)
if [[ -z "$OUTPUT_FILE" ]]; then
    mkdir -p "$OUTPUT_DIR"
    OUTPUT_FILE="$OUTPUT_DIR/${SPEC_BASENAME}-prp.md"
fi

# Check Claude CLI
check_claude_cli

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  LLM-Powered Spec-to-PRP Generator${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Spec: ${CYAN}$SPEC_FILE${NC}"
echo -e "Models: extract=${CYAN}$MODEL_EXTRACT${NC}, transform=${CYAN}$MODEL_TRANSFORM${NC}, review=${CYAN}$MODEL_REVIEW${NC}"
echo ""

# Read spec content
SPEC_CONTENT=$(cat "$SPEC_FILE")

# Read template structure (just the section headers for reference)
TEMPLATE_STRUCTURE=$(grep -E "^#+\s" "$TEMPLATES_DIR/prp-base.md" | head -30)

# ============================================================================
# PHASE 1: Metadata Extraction (Few-Shot)
# ============================================================================

echo -e "${BLUE}[1/3] Extracting metadata (few-shot prompting)...${NC}"

METADATA_PROMPT=$(cat "$PROMPTS_DIR/metadata-extraction.md")
METADATA_PROMPT="${METADATA_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"

if [[ "$VERBOSE" == "true" ]]; then
    echo -e "${CYAN}   Calling Claude ($MODEL_EXTRACT) for metadata extraction...${NC}"
fi

METADATA_RESULT=$(call_claude "$METADATA_PROMPT" "$MODEL_EXTRACT")

# Extract JSON from response (handle markdown code blocks)
METADATA_JSON=$(echo "$METADATA_RESULT" | sed -n '/```json/,/```/p' | sed '1d;$d')
if [[ -z "$METADATA_JSON" ]]; then
    # Try without code blocks
    METADATA_JSON=$(echo "$METADATA_RESULT" | grep -o '{.*}' | head -1)
fi

if [[ -z "$METADATA_JSON" ]]; then
    echo -e "${YELLOW}   Warning: Could not parse metadata JSON, using defaults${NC}"
    METADATA_JSON='{"project_type":"base","domain":"universal","complexity":5,"thinking_level":"Think"}'
fi

if [[ "$VERBOSE" == "true" ]]; then
    echo -e "${CYAN}   Metadata: $METADATA_JSON${NC}"
fi

echo -e "${GREEN}   ✓ Metadata extracted${NC}"

# ============================================================================
# PHASE 2: Intelligent Transformation (Chain of Thought)
# ============================================================================

echo -e "${BLUE}[2/3] Transforming spec to PRP (chain-of-thought)...${NC}"

TRANSFORM_PROMPT=$(cat "$PROMPTS_DIR/spec-transformation.md")
TRANSFORM_PROMPT="${TRANSFORM_PROMPT//\{\{METADATA\}\}/$METADATA_JSON}"
TRANSFORM_PROMPT="${TRANSFORM_PROMPT//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
TRANSFORM_PROMPT="${TRANSFORM_PROMPT//\{\{TEMPLATE_STRUCTURE\}\}/$TEMPLATE_STRUCTURE}"

if [[ "$VERBOSE" == "true" ]]; then
    echo -e "${CYAN}   Calling Claude ($MODEL_TRANSFORM) for transformation...${NC}"
fi

PRP_CONTENT=$(call_claude "$TRANSFORM_PROMPT" "$MODEL_TRANSFORM")

# Clean up markdown code blocks if present
PRP_CONTENT=$(echo "$PRP_CONTENT" | sed '/^```markdown$/d' | sed '/^```$/d')

echo -e "${GREEN}   ✓ PRP generated${NC}"

# ============================================================================
# PHASE 3: Intelligent Review (Evaluation Loop)
# ============================================================================

if [[ "$SKIP_REVIEW" == "false" ]]; then
    echo -e "${BLUE}[3/3] Intelligent review...${NC}"

    REVIEW_PROMPT_TEMPLATE=$(cat "$PROMPTS_DIR/prp-review.md")

    RETRY_COUNT=0
    REVIEW_PASSED=false

    while [[ $RETRY_COUNT -lt $MAX_RETRIES ]] && [[ "$REVIEW_PASSED" == "false" ]]; do
        RETRY_COUNT=$((RETRY_COUNT + 1))

        if [[ "$VERBOSE" == "true" ]]; then
            echo -e "${CYAN}   Review iteration $RETRY_COUNT/$MAX_RETRIES...${NC}"
        fi

        REVIEW_PROMPT="${REVIEW_PROMPT_TEMPLATE//\{\{SPEC_CONTENT\}\}/$SPEC_CONTENT}"
        REVIEW_PROMPT="${REVIEW_PROMPT//\{\{PRP_CONTENT\}\}/$PRP_CONTENT}"

        REVIEW_RESULT=$(call_claude "$REVIEW_PROMPT" "$MODEL_REVIEW")

        # Extract JSON from response
        REVIEW_JSON=$(echo "$REVIEW_RESULT" | sed -n '/```json/,/```/p' | sed '1d;$d')
        if [[ -z "$REVIEW_JSON" ]]; then
            REVIEW_JSON=$(echo "$REVIEW_RESULT" | grep -o '{.*}')
        fi

        # Check status
        if echo "$REVIEW_JSON" | grep -q '"overall_status":\s*"PASS"'; then
            REVIEW_PASSED=true
            echo -e "${GREEN}   ✓ Review passed${NC}"
        else
            # Extract quality score if available
            QUALITY_SCORE=$(echo "$REVIEW_JSON" | grep -o '"quality_score":\s*[0-9]*' | grep -o '[0-9]*')
            echo -e "${YELLOW}   Review found issues (score: ${QUALITY_SCORE:-unknown})${NC}"

            if [[ $RETRY_COUNT -lt $MAX_RETRIES ]]; then
                # Revision prompt
                REVISION_PROMPT="The PRP review found issues. Please revise the PRP to address them.

Review feedback:
$REVIEW_JSON

Original spec:
$SPEC_CONTENT

Current PRP:
$PRP_CONTENT

Output the revised PRP (complete markdown, no code blocks):"

                if [[ "$VERBOSE" == "true" ]]; then
                    echo -e "${CYAN}   Revising PRP ($MODEL_TRANSFORM)...${NC}"
                fi

                PRP_CONTENT=$(call_claude "$REVISION_PROMPT" "$MODEL_TRANSFORM")
                PRP_CONTENT=$(echo "$PRP_CONTENT" | sed '/^```markdown$/d' | sed '/^```$/d')
            fi
        fi
    done

    if [[ "$REVIEW_PASSED" == "false" ]]; then
        echo -e "${YELLOW}   ⚠ Review did not pass after $MAX_RETRIES attempts${NC}"
        echo -e "${YELLOW}   PRP may need manual refinement${NC}"
    fi
else
    echo -e "${YELLOW}[3/3] Skipping review (--skip-review)${NC}"
fi

# ============================================================================
# Write Output
# ============================================================================

echo ""
echo -e "${BLUE}Writing output...${NC}"

mkdir -p "$(dirname "$OUTPUT_FILE")"
echo "$PRP_CONTENT" > "$OUTPUT_FILE"

echo -e "${GREEN}✓ PRP saved to: ${CYAN}$OUTPUT_FILE${NC}"

# ============================================================================
# Summary
# ============================================================================

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Generation Complete${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Output: ${CYAN}$OUTPUT_FILE${NC}"
echo -e "Models: extract=${CYAN}$MODEL_EXTRACT${NC}, transform=${CYAN}$MODEL_TRANSFORM${NC}, review=${CYAN}$MODEL_REVIEW${NC}"
echo ""

# Count any remaining placeholders
PLACEHOLDER_COUNT=$(grep -cE "\[FILL_|{{" "$OUTPUT_FILE" 2>/dev/null || echo "0")
if [[ "$PLACEHOLDER_COUNT" -gt 0 ]]; then
    echo -e "${YELLOW}Note: $PLACEHOLDER_COUNT placeholders may remain - review output${NC}"
fi

echo ""
echo -e "${GREEN}Done!${NC}"
