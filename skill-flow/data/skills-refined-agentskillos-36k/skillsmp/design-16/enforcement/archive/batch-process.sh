#!/bin/bash
# batch-process.sh - Process multiple specs in parallel
#
# Outer parallelism layer - runs spec-to-prp-auto.sh on multiple specs simultaneously.
# Uses background jobs for parallelization.
#
# Usage:
#   ./batch-process.sh specs/*.md [--workers 4] [--threshold 95]
#   ./batch-process.sh --specs-dir ./specs --output-dir ./PRPs

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Defaults
MAX_WORKERS=4
THRESHOLD=95
MAX_ITERATIONS=5
OUTPUT_DIR=""
SPECS_DIR=""
VERBOSE=false
SPEC_FILES=()

usage() {
    echo "Usage: $0 <spec-files...> [options]"
    echo "       $0 --specs-dir <dir> [options]"
    echo ""
    echo "Process multiple specs in parallel using the Ralph auto-loop."
    echo ""
    echo "Options:"
    echo "  --specs-dir <dir>     Directory containing spec files"
    echo "  --output-dir <dir>    Output directory for PRPs"
    echo "  --workers <N>         Max parallel workers (default: 4)"
    echo "  --threshold <N>       Quality threshold (default: 95)"
    echo "  --max-iterations <N>  Max iterations per spec (default: 5)"
    echo "  --verbose             Show detailed progress"
    echo ""
    echo "Examples:"
    echo "  $0 specs/phase1.md specs/phase2.md specs/phase3.md"
    echo "  $0 specs/*.md --workers 4 --threshold 95"
    echo "  $0 --specs-dir ./specs --output-dir ./PRPs"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --specs-dir) SPECS_DIR="$2"; shift 2 ;;
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        --workers) MAX_WORKERS="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --max-iterations) MAX_ITERATIONS="$2"; shift 2 ;;
        --verbose) VERBOSE=true; shift ;;
        --help|-h) usage ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
        *)
            # Assume it's a spec file
            SPEC_FILES+=("$1")
            shift
            ;;
    esac
done

# If specs-dir specified, find all .md files
if [[ -n "$SPECS_DIR" ]]; then
    [[ ! -d "$SPECS_DIR" ]] && { echo -e "${RED}ERROR: Specs directory not found: $SPECS_DIR${NC}"; exit 1; }
    while IFS= read -r -d '' file; do
        SPEC_FILES+=("$file")
    done < <(find "$SPECS_DIR" -maxdepth 1 -name "*.md" -type f -print0 | sort -z)
fi

# Validate we have specs
[[ ${#SPEC_FILES[@]} -eq 0 ]] && { echo -e "${RED}ERROR: No spec files provided${NC}"; usage; }

# Set default output dir
[[ -z "$OUTPUT_DIR" ]] && OUTPUT_DIR="$SCRIPT_DIR/../output"
mkdir -p "$OUTPUT_DIR"

# Create work directory for tracking
WORK_DIR=$(mktemp -d)
trap "rm -rf $WORK_DIR" EXIT

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              BATCH SPEC-TO-PRP PROCESSOR                      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Specs:      ${CYAN}${#SPEC_FILES[@]} files${NC}"
echo -e "Output:     ${CYAN}$OUTPUT_DIR${NC}"
echo -e "Workers:    ${CYAN}$MAX_WORKERS${NC}"
echo -e "Threshold:  ${CYAN}$THRESHOLD%${NC}"
echo ""

# List specs
echo -e "${BLUE}Specs to process:${NC}"
for spec in "${SPEC_FILES[@]}"; do
    echo -e "  ${CYAN}$(basename "$spec")${NC}"
done
echo ""

# Process function for a single spec
process_spec() {
    local spec_file="$1"
    local index="$2"
    local basename=$(basename "$spec_file" .md)
    local output_file="$OUTPUT_DIR/${basename}-prp.md"
    local log_file="$WORK_DIR/log_${index}.txt"
    local result_file="$WORK_DIR/result_${index}.json"

    # Run auto-loop
    "$SCRIPT_DIR/spec-to-prp-auto.sh" \
        "$spec_file" \
        --output "$output_file" \
        --threshold "$THRESHOLD" \
        --max-iterations "$MAX_ITERATIONS" \
        > "$log_file" 2>&1

    local exit_code=$?

    # Extract final score from log
    local score=$(grep -o 'Score:.*[0-9]\+%' "$log_file" | tail -1 | grep -o '[0-9]\+' | head -1)
    local iterations=$(grep -o 'Iterations:.*[0-9]\+' "$log_file" | grep -o '[0-9]\+' | head -1)

    # Write result
    cat > "$result_file" << EOF
{
  "spec": "$spec_file",
  "output": "$output_file",
  "score": ${score:-0},
  "iterations": ${iterations:-0},
  "exit_code": $exit_code,
  "status": "$([ $exit_code -eq 0 ] && echo 'PASS' || echo 'FAIL')"
}
EOF

    return $exit_code
}

# Launch workers in parallel
echo -e "${BLUE}Processing specs in parallel...${NC}"
echo ""

PIDS=()
SPEC_INDICES=()
START_TIME=$(date +%s)

for i in "${!SPEC_FILES[@]}"; do
    spec="${SPEC_FILES[$i]}"
    basename=$(basename "$spec")

    echo -e "${MAGENTA}  [$((i+1))/${#SPEC_FILES[@]}] Starting: $basename${NC}"

    process_spec "$spec" "$i" &
    PIDS+=($!)
    SPEC_INDICES+=($i)

    # Respect max workers
    while [[ ${#PIDS[@]} -ge $MAX_WORKERS ]]; do
        # Wait for any job to finish
        for j in "${!PIDS[@]}"; do
            if ! kill -0 "${PIDS[$j]}" 2>/dev/null; then
                # Job finished
                wait "${PIDS[$j]}" || true
                idx="${SPEC_INDICES[$j]}"
                spec_name=$(basename "${SPEC_FILES[$idx]}")

                # Check result
                result_file="$WORK_DIR/result_${idx}.json"
                if [[ -f "$result_file" ]]; then
                    status=$(grep -o '"status":\s*"[^"]*"' "$result_file" | cut -d'"' -f4)
                    score=$(grep -o '"score":\s*[0-9]*' "$result_file" | grep -o '[0-9]*')
                    if [[ "$status" == "PASS" ]]; then
                        echo -e "${GREEN}  ✓ $spec_name: ${score}%${NC}"
                    else
                        echo -e "${YELLOW}  ⚠ $spec_name: ${score}%${NC}"
                    fi
                fi

                # Remove from arrays
                unset 'PIDS[j]'
                unset 'SPEC_INDICES[j]'
                PIDS=("${PIDS[@]}")
                SPEC_INDICES=("${SPEC_INDICES[@]}")
                break
            fi
        done
        sleep 0.5
    done
done

# Wait for remaining jobs
for j in "${!PIDS[@]}"; do
    wait "${PIDS[$j]}" || true
    idx="${SPEC_INDICES[$j]}"
    spec_name=$(basename "${SPEC_FILES[$idx]}")

    result_file="$WORK_DIR/result_${idx}.json"
    if [[ -f "$result_file" ]]; then
        status=$(grep -o '"status":\s*"[^"]*"' "$result_file" | cut -d'"' -f4)
        score=$(grep -o '"score":\s*[0-9]*' "$result_file" | grep -o '[0-9]*')
        if [[ "$status" == "PASS" ]]; then
            echo -e "${GREEN}  ✓ $spec_name: ${score}%${NC}"
        else
            echo -e "${YELLOW}  ⚠ $spec_name: ${score}%${NC}"
        fi
    fi
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Aggregate results
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

TOTAL=0
PASSED=0
TOTAL_SCORE=0

echo -e "${BLUE}Results:${NC}"
echo ""
printf "  %-30s %8s %8s %s\n" "SPEC" "SCORE" "ITERS" "STATUS"
printf "  %-30s %8s %8s %s\n" "────────────────────────────" "─────" "─────" "──────"

for i in "${!SPEC_FILES[@]}"; do
    result_file="$WORK_DIR/result_${i}.json"
    spec_name=$(basename "${SPEC_FILES[$i]}" .md)

    if [[ -f "$result_file" ]]; then
        status=$(grep -o '"status":\s*"[^"]*"' "$result_file" | cut -d'"' -f4)
        score=$(grep -o '"score":\s*[0-9]*' "$result_file" | grep -o '[0-9]*')
        iters=$(grep -o '"iterations":\s*[0-9]*' "$result_file" | grep -o '[0-9]*')

        TOTAL=$((TOTAL + 1))
        [[ "$status" == "PASS" ]] && PASSED=$((PASSED + 1))
        TOTAL_SCORE=$((TOTAL_SCORE + ${score:-0}))

        if [[ "$status" == "PASS" ]]; then
            printf "  %-30s ${GREEN}%7s%%${NC} %8s ${GREEN}%s${NC}\n" "$spec_name" "${score:-0}" "${iters:-0}" "PASS"
        else
            printf "  %-30s ${YELLOW}%7s%%${NC} %8s ${YELLOW}%s${NC}\n" "$spec_name" "${score:-0}" "${iters:-0}" "FAIL"
        fi
    fi
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

AVG_SCORE=0
[[ $TOTAL -gt 0 ]] && AVG_SCORE=$((TOTAL_SCORE / TOTAL))

echo ""
echo -e "  Total:     ${CYAN}$TOTAL specs${NC}"
echo -e "  Passed:    ${GREEN}$PASSED${NC} / $TOTAL"
echo -e "  Avg Score: ${CYAN}$AVG_SCORE%${NC}"
echo -e "  Duration:  ${CYAN}${DURATION}s${NC}"
echo ""

if [[ $PASSED -eq $TOTAL ]]; then
    echo -e "${GREEN}  ✓ All specs passed quality threshold!${NC}"
    EXIT_CODE=0
else
    FAILED=$((TOTAL - PASSED))
    echo -e "${YELLOW}  ⚠ $FAILED spec(s) did not reach threshold${NC}"
    EXIT_CODE=1
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "PRPs saved to: ${CYAN}$OUTPUT_DIR${NC}"
echo ""

exit $EXIT_CODE
