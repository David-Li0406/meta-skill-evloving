#!/bin/bash
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

#
# Terraform Provider Parallel Test Execution Script
#
# Runs acceptance tests concurrently per test file to speed up execution.
# Supports filtering, concurrency control, and detailed reporting.
#
# Usage:
#   ./run_tests_parallel.sh [OPTIONS]
#
# Options:
#   -d, --dir DIR           Test directory (default: ./internal/provider)
#   -p, --pattern PATTERN   Test pattern to match (default: TestAcc)
#   -c, --concurrency N     Max concurrent test files (default: 4)
#   -t, --timeout DURATION  Timeout per test file (default: 30m)
#   -f, --file FILE         Run only tests from specific file
#   -C, --cleanup           Run cleanup before tests (requires BCM credentials)
#   -S, --stagger SECONDS   Delay between starting each test file (default: 2)
#   --resources-only        Run only resource tests
#   --data-sources-only     Run only data source tests
#   --verbose               Show detailed test output
#   --no-color              Disable colored output
#   -h, --help              Show this help message
#
# Examples:
#   # Run all acceptance tests with 4 concurrent files
#   ./run_tests_parallel.sh
#
#   # Run with cleanup before tests (requires BCM credentials)
#   ./run_tests_parallel.sh --cleanup
#
#   # Run all 21 test files in parallel (max concurrency)
#   ./run_tests_parallel.sh -c 21 -t 30m 2>&1 | tail -100
#
#   # Run with full output logging to file
#   ./run_tests_parallel.sh -c 21 2>&1 | tee test-results.log
#
#   # Run only resource tests with higher concurrency and cleanup
#   ./run_tests_parallel.sh --resources-only -c 8 --cleanup
#
#   # Run tests matching specific pattern
#   ./run_tests_parallel.sh -p "TestAccCMPartSoftwareImage"
#
#   # Run tests from specific file
#   ./run_tests_parallel.sh -f resource_cmpart_softwareimage_test.go
#
# IMPORTANT: Always pipe output for visibility:
#   - Use "| tail -100" to see last 100 lines of output
#   - Use "| tee logfile.log" to see output AND save to file
#   - DO NOT run in background - you need to see test progress
#
# RECOMMENDED: Auto-log and tail pattern:
#   LOG_FILE=/tmp/test-results.log
#   ./run_tests_parallel.sh -c 21 > "$LOG_FILE" 2>&1 &
#   tail -f "$LOG_FILE"
#

set -euo pipefail

# Auto-logging feature: if LOG_TO_FILE is set, redirect all output
if [ -n "${LOG_TO_FILE:-}" ]; then
    exec > >(tee "$LOG_TO_FILE") 2>&1
    echo "Logging to: $LOG_TO_FILE"
fi

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
TEST_DIR="./internal/provider"
TEST_PATTERN="TestAcc"
CONCURRENCY=15
TIMEOUT="30m"
SPECIFIC_FILE=""
CLEANUP=true
STAGGER_DELAY=5
RESOURCES_ONLY=false
DATA_SOURCES_ONLY=false
VERBOSE=false
NO_COLOR=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dir)
            TEST_DIR="$2"
            shift 2
            ;;
        -p|--pattern)
            TEST_PATTERN="$2"
            shift 2
            ;;
        -c|--concurrency)
            CONCURRENCY="$2"
            shift 2
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -f|--file)
            SPECIFIC_FILE="$2"
            shift 2
            ;;
        -C|--cleanup)
            CLEANUP=true
            shift
            ;;
        -S|--stagger)
            STAGGER_DELAY="$2"
            shift 2
            ;;
        --resources-only)
            RESOURCES_ONLY=true
            shift
            ;;
        --data-sources-only)
            DATA_SOURCES_ONLY=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --no-color)
            NO_COLOR=true
            shift
            ;;
        -h|--help)
            sed -n '3,44p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Disable colors if requested
if [ "$NO_COLOR" = true ]; then
    GREEN=''
    RED=''
    YELLOW=''
    BLUE=''
    CYAN=''
    NC=''
fi

# Run cleanup if requested
if [ "$CLEANUP" = true ]; then
    echo -e "${BLUE}===== Pre-Test Cleanup =====${NC}"
    echo ""

    # Check if BCM credentials are set
    if [ -z "${BCM_ENDPOINT:-}" ] || [ -z "${BCM_USERNAME:-}" ] || [ -z "${BCM_PASSWORD:-}" ]; then
        echo -e "${YELLOW}Warning: BCM credentials not set. Skipping cleanup.${NC}"
        echo "Set BCM_ENDPOINT, BCM_USERNAME, and BCM_PASSWORD to enable cleanup."
        echo ""
    else
        # Determine cleanup script location
        CLEANUP_SCRIPT="/workspace/scripts/cleanup-test-resources-auto.sh"

        if [ ! -f "$CLEANUP_SCRIPT" ]; then
            echo -e "${YELLOW}Warning: Cleanup script not found at $CLEANUP_SCRIPT${NC}"
            echo "Skipping cleanup step."
            echo ""
        else
            echo "Running cleanup script: $CLEANUP_SCRIPT"
            echo ""

            # Run cleanup script (continue even if it has warnings)
            if bash "$CLEANUP_SCRIPT"; then
                echo -e "${GREEN}✅ Cleanup completed successfully${NC}"
            else
                cleanup_exit=$?
                if [ $cleanup_exit -eq 0 ]; then
                    echo -e "${GREEN}✅ Cleanup completed${NC}"
                else
                    echo -e "${YELLOW}⚠️  Cleanup completed with warnings (exit code: $cleanup_exit)${NC}"
                    echo "Continuing with tests..."
                fi
            fi
            echo ""
        fi
    fi
fi

# Validate directory
if [ ! -d "$TEST_DIR" ]; then
    echo -e "${RED}Error: Directory $TEST_DIR does not exist${NC}"
    exit 1
fi

# Check for required environment variables
if [ -z "${TF_ACC:-}" ]; then
    echo -e "${YELLOW}Warning: TF_ACC is not set. Set TF_ACC=1 to enable acceptance tests.${NC}"
    echo ""
fi

# Set Go environment variables
export GOMODCACHE="${GOMODCACHE:-/workspace/.go/pkg/mod}"
export GOCACHE="${GOCACHE:-/workspace/.go/cache}"
export GOPATH="${GOPATH:-/workspace/.go}"

# Create results directory
RESULTS_DIR=$(mktemp -d)
trap "rm -rf $RESULTS_DIR" EXIT

# Create output log file
OUTPUT_LOG="${RESULTS_DIR}/parallel_test_output.log"

echo "===== Terraform Provider Parallel Test Execution =====" | tee "$OUTPUT_LOG"
echo "Test Directory: $TEST_DIR" | tee -a "$OUTPUT_LOG"
echo "Test Pattern: $TEST_PATTERN" | tee -a "$OUTPUT_LOG"
echo "Concurrency: $CONCURRENCY" | tee -a "$OUTPUT_LOG"
echo "Timeout: $TIMEOUT" | tee -a "$OUTPUT_LOG"
echo "Stagger Delay: ${STAGGER_DELAY}s" | tee -a "$OUTPUT_LOG"
echo "Output Log: $OUTPUT_LOG" | tee -a "$OUTPUT_LOG"
echo "" | tee -a "$OUTPUT_LOG"

# Find test files
TEST_FILES=()
if [ -n "$SPECIFIC_FILE" ]; then
    if [ -f "$TEST_DIR/$SPECIFIC_FILE" ]; then
        TEST_FILES=("$TEST_DIR/$SPECIFIC_FILE")
    else
        echo -e "${RED}Error: Test file $SPECIFIC_FILE not found in $TEST_DIR${NC}"
        exit 1
    fi
elif [ "$RESOURCES_ONLY" = true ]; then
    mapfile -t TEST_FILES < <(find "$TEST_DIR" -name "resource_*_test.go" | sort)
elif [ "$DATA_SOURCES_ONLY" = true ]; then
    mapfile -t TEST_FILES < <(find "$TEST_DIR" -name "data_source_*_test.go" | sort)
else
    mapfile -t TEST_FILES < <(find "$TEST_DIR" -name "*_test.go" | sort)
fi

if [ ${#TEST_FILES[@]} -eq 0 ]; then
    echo -e "${RED}Error: No test files found${NC}"
    exit 1
fi

echo "Found ${#TEST_FILES[@]} test file(s)" | tee -a "$OUTPUT_LOG"
echo "" | tee -a "$OUTPUT_LOG"

# Function to run tests from a single file
run_test_file() {
    local file=$1
    local file_base=$(basename "$file")
    local result_file="$RESULTS_DIR/${file_base}.result"
    local output_file="$RESULTS_DIR/${file_base}.output"
    local start_time=$(date +%s)

    echo -e "${CYAN}[START]${NC} $file_base" | tee -a "$OUTPUT_LOG"

    # Extract test function names from the file
    # This allows us to run only tests from this specific file
    local test_functions=$(grep -o "^func Test[A-Za-z0-9_]*" "$file" | sed 's/^func //' | paste -sd "|" -)

    if [ -z "$test_functions" ]; then
        echo -e "${YELLOW}[SKIP]${NC} $file_base (no test functions found)" | tee -a "$OUTPUT_LOG"
        echo "0|0|0|0|0" > "$result_file"
        return 0
    fi

    # Use file-specific test names as pattern
    # If TEST_PATTERN is "TestAcc", just use the extracted function names directly
    # since they already start with Test/TestAcc
    local combined_pattern="^(${test_functions})$"

    # Run the test
    if [ "$VERBOSE" = true ]; then
        TF_ACC=1 go test -v -timeout "$TIMEOUT" "$TEST_DIR" -run "$combined_pattern" \
            2>&1 | tee "$output_file"
        exit_code=${PIPESTATUS[0]}
    else
        TF_ACC=1 go test -v -timeout "$TIMEOUT" "$TEST_DIR" -run "$combined_pattern" \
            > "$output_file" 2>&1
        exit_code=$?
    fi

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    # Parse test results
    local passed=$(grep -c "^--- PASS:" "$output_file" 2>/dev/null || echo 0)
    local failed=$(grep -c "^--- FAIL:" "$output_file" 2>/dev/null || echo 0)
    local skipped=$(grep -c "^--- SKIP:" "$output_file" 2>/dev/null || echo 0)

    # Save result summary
    echo "$exit_code|$passed|$failed|$skipped|$duration" > "$result_file"

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}[PASS]${NC} $file_base (${duration}s, passed: $passed)" | tee -a "$OUTPUT_LOG"
    else
        echo -e "${RED}[FAIL]${NC} $file_base (${duration}s, passed: $passed, failed: $failed)" | tee -a "$OUTPUT_LOG"

        # Show failures if not verbose
        if [ "$VERBOSE" = false ]; then
            echo -e "${YELLOW}Failures in $file_base:${NC}" | tee -a "$OUTPUT_LOG"
            grep -A 5 "^--- FAIL:" "$output_file" | head -n 30 | tee -a "$OUTPUT_LOG"
            echo "" | tee -a "$OUTPUT_LOG"
        fi
    fi

    return $exit_code
}

export -f run_test_file
export RESULTS_DIR TEST_DIR TEST_PATTERN TIMEOUT VERBOSE OUTPUT_LOG
export GREEN RED YELLOW BLUE CYAN NC

# Run tests in parallel with optional stagger delay
if [ "$STAGGER_DELAY" -gt 0 ]; then
    # Run with stagger delay between starting each test file
    echo -e "${YELLOW}Using stagger delay: ${STAGGER_DELAY}s between test file starts${NC}" | tee -a "$OUTPUT_LOG"

    # Use background jobs with controlled delay
    pids=()
    test_count=0

    for file in "${TEST_FILES[@]}"; do
        # Wait for slot in concurrency limit
        while [ "$(jobs -r | wc -l)" -ge "$CONCURRENCY" ]; do
            sleep 0.5
        done

        # Stagger delay before starting (except for first file)
        if [ $test_count -gt 0 ]; then
            sleep "$STAGGER_DELAY"
        fi
        test_count=$((test_count + 1))

        # Start test in background
        run_test_file "$file" &
        pids+=($!)
    done

    # Wait for all tests to complete
    parallel_exit=0
    for pid in "${pids[@]}"; do
        wait "$pid" || parallel_exit=1
    done
elif command -v parallel &> /dev/null; then
    # Use GNU parallel for better progress tracking (no stagger needed)
    printf '%s\n' "${TEST_FILES[@]}" | \
        parallel -j "$CONCURRENCY" --line-buffer run_test_file {}
    parallel_exit=$?
else
    # Fallback to xargs
    printf '%s\n' "${TEST_FILES[@]}" | \
        xargs -I {} -P "$CONCURRENCY" bash -c 'run_test_file "$@"' _ {}
    parallel_exit=$?
fi

echo ""
echo "===== Test Summary ====="
echo ""

# Aggregate results
total_passed=0
total_failed=0
total_skipped=0
total_duration=0
failed_files=()

for file in "${TEST_FILES[@]}"; do
    file_base=$(basename "$file")
    result_file="$RESULTS_DIR/${file_base}.result"

    if [ -f "$result_file" ]; then
        IFS='|' read -r exit_code passed failed skipped duration < "$result_file"
        total_passed=$((total_passed + passed))
        total_failed=$((total_failed + failed))
        total_skipped=$((total_skipped + skipped))
        total_duration=$((total_duration + duration))

        if [ "$exit_code" -ne 0 ]; then
            failed_files+=("$file_base")
        fi
    fi
done

# Display summary
echo "Test Files: ${#TEST_FILES[@]}"
echo "Total Passed: ${total_passed}"
echo "Total Failed: ${total_failed}"
echo "Total Skipped: ${total_skipped}"
echo "Total Duration: ${total_duration}s"
echo ""

if [ ${#failed_files[@]} -gt 0 ]; then
    echo -e "${RED}Failed Files (${#failed_files[@]}):${NC}"
    for file in "${failed_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo -e "${YELLOW}Detailed output saved in: $RESULTS_DIR${NC}"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    exit 0
fi
