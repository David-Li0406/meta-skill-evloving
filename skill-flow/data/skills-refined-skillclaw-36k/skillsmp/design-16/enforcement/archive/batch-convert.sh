#!/bin/bash
# batch-convert.sh - Parallel spec to PRP conversion
#
# Converts multiple specs to PRPs in parallel using background jobs.
#
# Usage:
#   ./batch-convert.sh <spec-dir-or-files> [options]
#
# Examples:
#   ./batch-convert.sh specs/                    # All specs in directory
#   ./batch-convert.sh specs/*.md                # Glob pattern
#   ./batch-convert.sh spec1.md spec2.md spec3.md  # Specific files
#   ./batch-convert.sh specs/ --parallel 4       # Limit parallelism

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
CONVERTER="$SCRIPT_DIR/spec-to-prp-llm.sh"
OUTPUT_DIR="$SCRIPT_DIR/../output"
LOG_DIR="$OUTPUT_DIR/logs"

# Defaults
PARALLEL_JOBS=0  # 0 = unlimited
MODEL="sonnet"
SKIP_REVIEW=false

# Usage
usage() {
    echo "Usage: $0 <spec-dir-or-files> [options]"
    echo ""
    echo "Parallel spec to PRP conversion."
    echo ""
    echo "Arguments:"
    echo "  <spec-dir>    Directory containing .md spec files"
    echo "  <files...>    One or more spec files"
    echo ""
    echo "Options:"
    echo "  --parallel <n>    Max parallel jobs (default: unlimited)"
    echo "  --model <model>   Claude model: haiku, sonnet (default), opus"
    echo "  --output <dir>    Output directory (default: output/)"
    echo "  --skip-review     Skip intelligent review phase"
    echo "  --dry-run         Show what would be done"
    echo ""
    echo "Examples:"
    echo "  $0 specs/                           # All specs in directory"
    echo "  $0 specs/phase*.md                  # Glob pattern"
    echo "  $0 specs/ --parallel 4 --model haiku"
    exit 1
}

# Parse arguments
SPEC_FILES=()
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --parallel)
            PARALLEL_JOBS="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --skip-review)
            SKIP_REVIEW=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            usage
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
        *)
            # Check if it's a directory or file
            if [[ -d "$1" ]]; then
                # Add all .md files from directory
                for f in "$1"/*.md; do
                    [[ -f "$f" ]] && SPEC_FILES+=("$f")
                done
            elif [[ -f "$1" ]]; then
                SPEC_FILES+=("$1")
            else
                # Could be a glob pattern that expanded
                SPEC_FILES+=("$1")
            fi
            shift
            ;;
    esac
done

# Validate
if [[ ${#SPEC_FILES[@]} -eq 0 ]]; then
    echo -e "${RED}ERROR: No spec files found${NC}"
    usage
fi

# Filter to only existing .md files
VALID_FILES=()
for f in "${SPEC_FILES[@]}"; do
    if [[ -f "$f" ]] && [[ "$f" == *.md ]]; then
        VALID_FILES+=("$f")
    fi
done

if [[ ${#VALID_FILES[@]} -eq 0 ]]; then
    echo -e "${RED}ERROR: No valid .md spec files found${NC}"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Batch Spec-to-PRP Conversion${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Specs to convert: ${CYAN}${#VALID_FILES[@]}${NC}"
echo -e "Model: ${CYAN}$MODEL${NC}"
echo -e "Parallel jobs: ${CYAN}${PARALLEL_JOBS:-unlimited}${NC}"
echo -e "Output: ${CYAN}$OUTPUT_DIR${NC}"
echo ""

# List files
echo -e "${BLUE}Files:${NC}"
for f in "${VALID_FILES[@]}"; do
    echo "  - $(basename "$f")"
done
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}[DRY RUN] Would convert ${#VALID_FILES[@]} files${NC}"
    exit 0
fi

# Create directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

# Track jobs
declare -A PIDS
declare -A RESULTS
START_TIME=$(date +%s)

# Convert function
convert_spec() {
    local spec_file="$1"
    local basename=$(basename "$spec_file" .md)
    local output_file="$OUTPUT_DIR/${basename}-prp.md"
    local log_file="$LOG_DIR/${basename}.log"

    local args="--model $MODEL --output $output_file"
    if [[ "$SKIP_REVIEW" == "true" ]]; then
        args="$args --skip-review"
    fi

    # Run converter and capture exit code
    "$CONVERTER" "$spec_file" $args > "$log_file" 2>&1
    return $?
}

echo -e "${BLUE}Starting conversions...${NC}"
echo ""

# Launch jobs
RUNNING=0
COMPLETED=0
FAILED=0

for spec_file in "${VALID_FILES[@]}"; do
    basename=$(basename "$spec_file" .md)

    # Wait if at parallel limit
    if [[ $PARALLEL_JOBS -gt 0 ]] && [[ $RUNNING -ge $PARALLEL_JOBS ]]; then
        # Wait for any job to finish
        wait -n 2>/dev/null || true
        RUNNING=$((RUNNING - 1))
    fi

    echo -e "  ${CYAN}Starting:${NC} $basename"

    # Launch in background
    convert_spec "$spec_file" &
    PIDS["$basename"]=$!
    RUNNING=$((RUNNING + 1))
done

# Wait for all jobs and collect results
echo ""
echo -e "${BLUE}Waiting for completions...${NC}"

for basename in "${!PIDS[@]}"; do
    pid=${PIDS[$basename]}
    if wait $pid; then
        RESULTS["$basename"]="SUCCESS"
        COMPLETED=$((COMPLETED + 1))
        echo -e "  ${GREEN}✓${NC} $basename"
    else
        RESULTS["$basename"]="FAILED"
        FAILED=$((FAILED + 1))
        echo -e "  ${RED}✗${NC} $basename (see logs/$basename.log)"
    fi
done

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Summary
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Batch Conversion Complete${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Duration: ${CYAN}${DURATION}s${NC}"
echo -e "Total:    ${CYAN}${#VALID_FILES[@]}${NC}"
echo -e "Success:  ${GREEN}$COMPLETED${NC}"
if [[ $FAILED -gt 0 ]]; then
    echo -e "Failed:   ${RED}$FAILED${NC}"
fi
echo ""

# List outputs
echo -e "${BLUE}Generated PRPs:${NC}"
for basename in "${!RESULTS[@]}"; do
    if [[ "${RESULTS[$basename]}" == "SUCCESS" ]]; then
        echo "  $OUTPUT_DIR/${basename}-prp.md"
    fi
done

if [[ $FAILED -gt 0 ]]; then
    echo ""
    echo -e "${BLUE}Failed conversions (check logs):${NC}"
    for basename in "${!RESULTS[@]}"; do
        if [[ "${RESULTS[$basename]}" == "FAILED" ]]; then
            echo "  $LOG_DIR/${basename}.log"
        fi
    done
fi

echo ""
echo -e "${GREEN}Done!${NC}"

# Exit with error if any failed
[[ $FAILED -eq 0 ]]
