#!/usr/bin/env bash
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

#
# Generic Terraform Example Test Framework
#
# This is a TEMPLATE - copy to your project's scripts/ directory and customize:
# 1. Update PROVIDER_NAME variable
# 2. Update required environment variables in show_help()
# 3. Implement cleanup_resources() function for your provider
#
# Usage: See show_help() function below
#

set -euo pipefail

#############################################################################
# PROJECT CONFIGURATION - CUSTOMIZE THESE
#############################################################################

# REQUIRED: Set your provider name
PROVIDER_NAME="${PROVIDER_NAME:-myprovider}"

# REQUIRED: Implement this function to cleanup test resources
# This is provider-specific and must query your API to find and delete test resources
cleanup_resources() {
    log_info "Phase 4: Cleanup..."
    log_error "cleanup_resources() not implemented!"
    log_error "You must implement cleanup logic for your provider"
    log_error "See template comments for guidance"
    return 1
}

# Example cleanup implementation:
# cleanup_resources() {
#     # 1. Authenticate with your API
#     # 2. Query for resources with test prefix (e.g., "citest-")
#     # 3. Delete found resources with retry logic
#     # 4. Verify deletion
#     # 5. Return 0 on success, 1 on failure
# }

#############################################################################
# GENERIC TEST FRAMEWORK - DO NOT MODIFY BELOW THIS LINE
#############################################################################

# Trap handlers for cleanup on exit/interrupt
INTERRUPTED=false

cleanup_on_exit() {
    if [ "$INTERRUPTED" = true ]; then
        log_info ""
        log_info "Interrupted by user - cleaning up before exit..."
        cleanup_resources || true
        exit "$EXIT_INTERRUPTED"
    fi
}

handle_interrupt() {
    INTERRUPTED=true
    log_info ""
    log_info "Received interrupt signal (Ctrl+C)..."
    cleanup_on_exit
}

trap cleanup_on_exit EXIT
trap handle_interrupt SIGINT SIGTERM

# Exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_TEST_FAILURE=1
readonly EXIT_CONFIG_ERROR=2
readonly EXIT_BUILD_FAILURE=3
readonly EXIT_INTERRUPTED=130

# Color codes for output
readonly COLOR_INFO='\033[0;36m'
readonly COLOR_PASS='\033[0;32m'
readonly COLOR_FAIL='\033[0;31m'
readonly COLOR_ERROR='\033[0;31m'
readonly COLOR_RESET='\033[0m'

# Default configuration
PROVIDER_VERSION="${PROVIDER_VERSION:-0.1.0}"
SKIP_BUILD="${SKIP_BUILD:-false}"
PARALLEL_LIMIT="${PARALLEL_LIMIT:-4}"
CLEANUP_ONLY="${CLEANUP_ONLY:-false}"
VERBOSE="${VERBOSE:-false}"
NO_CLEANUP="${NO_CLEANUP:-false}"
DATA_SOURCES_ONLY="${DATA_SOURCES_ONLY:-false}"
RESOURCES_ONLY="${RESOURCES_ONLY:-false}"

# Test results tracking
PASSED_COUNT=0
FAILED_COUNT=0
FAILED_EXAMPLES=()

# Timing tracking
START_TIME=0
BUILD_TIME=0
DATA_SOURCES_TIME=0
RESOURCES_TIME=0
CLEANUP_TIME=0

#############################################################################
# CLI Parsing and Help
#############################################################################

show_help() {
    cat <<EOF
Terraform Example Test Suite

Validates all Terraform examples in the examples/ directory by building the
provider, executing examples, and cleaning up test resources.

USAGE:
  ./scripts/test-examples.sh [OPTIONS]

OPTIONS:
  --help                  Display this help message
  --cleanup-only          Skip tests, only cleanup existing test resources
  --verbose               Show detailed output including terraform logs
  --no-cleanup            Skip cleanup phase (useful for debugging)
  --data-sources-only     Only test data source examples
  --resources-only        Only test resource examples

ENVIRONMENT VARIABLES (Required):
  PROVIDER_NAME       Provider name (default: $PROVIDER_NAME)
  <Add your provider-specific required env vars here>

ENVIRONMENT VARIABLES (Optional):
  PROVIDER_VERSION    Provider version for binary (default: 0.1.0)
  SKIP_BUILD          Skip provider build phase (default: false)
  PARALLEL_LIMIT      Max parallel data source tests (default: 4)
  VERBOSE             Enable verbose logging (default: false)

EXIT CODES:
  0   All tests passed, cleanup successful
  1   One or more tests failed
  2   Configuration error (missing env vars)
  3   Provider build failed
  130 Interrupted by user (Ctrl+C)

EXAMPLES:
  # Run all tests
  ./scripts/test-examples.sh

  # Debug a failing resource test
  ./scripts/test-examples.sh --resources-only --no-cleanup --verbose

  # Cleanup orphaned resources
  ./scripts/test-examples.sh --cleanup-only

  # Quick validation (data sources only)
  ./scripts/test-examples.sh --data-sources-only

EOF
    exit 0
}

# Parse command-line arguments
for arg in "$@"; do
    case "$arg" in
        --help)
            show_help
            ;;
        --cleanup-only)
            CLEANUP_ONLY=true
            ;;
        --verbose)
            VERBOSE=true
            ;;
        --no-cleanup)
            NO_CLEANUP=true
            ;;
        --data-sources-only)
            DATA_SOURCES_ONLY=true
            ;;
        --resources-only)
            RESOURCES_ONLY=true
            ;;
        *)
            echo -e "${COLOR_ERROR}[ERROR] Unknown argument: $arg${COLOR_RESET}"
            echo "Use --help for usage information"
            exit "$EXIT_CONFIG_ERROR"
            ;;
    esac
done

#############################################################################
# Logging Functions
#############################################################################

log_info() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${COLOR_INFO}[INFO]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') | $*"
    else
        echo -e "${COLOR_INFO}[INFO]${COLOR_RESET} $*"
    fi
}

log_pass() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${COLOR_PASS}[PASS]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') | $*"
    else
        echo -e "${COLOR_PASS}[PASS]${COLOR_RESET} $*"
    fi
}

log_fail() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${COLOR_FAIL}[FAIL]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') | $*"
    else
        echo -e "${COLOR_FAIL}[FAIL]${COLOR_RESET} $*"
    fi
}

log_error() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${COLOR_ERROR}[ERROR]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') | $*"
    else
        echo -e "${COLOR_ERROR}[ERROR]${COLOR_RESET} $*"
    fi
}

log_debug() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${COLOR_INFO}[DEBUG]${COLOR_RESET} $(date '+%Y-%m-%d %H:%M:%S') | $*"
    fi
}

#############################################################################
# Environment Validation
#############################################################################

validate_environment() {
    # Validate flag combinations
    if [ "$DATA_SOURCES_ONLY" = true ] && [ "$RESOURCES_ONLY" = true ]; then
        log_error "Cannot use --data-sources-only and --resources-only together"
        exit "$EXIT_CONFIG_ERROR"
    fi

    if [ "$CLEANUP_ONLY" = true ] && [ "$NO_CLEANUP" = true ]; then
        log_error "Cannot use --cleanup-only and --no-cleanup together"
        exit "$EXIT_CONFIG_ERROR"
    fi

    log_info "========================================"
    log_info "Terraform Example Test Suite"
    log_info "========================================"
    log_debug "Provider: $PROVIDER_NAME"
    log_debug "Provider Version: $PROVIDER_VERSION"

    # Determine execution mode
    local exec_mode="all"
    if [ "$CLEANUP_ONLY" = true ]; then
        exec_mode="cleanup-only"
    elif [ "$DATA_SOURCES_ONLY" = true ]; then
        exec_mode="data-sources-only"
    elif [ "$RESOURCES_ONLY" = true ]; then
        exec_mode="resources-only"
    fi
    log_debug "Execution Mode: $exec_mode"
    log_info ""
    log_info "Phase 1: Validating environment..."

    # Add your provider-specific environment validation here
    # Example:
    # if [ -z "${MY_PROVIDER_ENDPOINT:-}" ]; then
    #     log_error "Missing MY_PROVIDER_ENDPOINT"
    #     exit "$EXIT_CONFIG_ERROR"
    # fi

    log_info ""
}

#############################################################################
# Provider Binary Build
#############################################################################

build_provider() {
    if [ "$SKIP_BUILD" = "true" ]; then
        log_info "Phase 2: Skipping provider build (SKIP_BUILD=true)..."
        log_info ""
        return
    fi

    local build_start
    build_start=$(date +%s)

    log_info "Phase 2: Building provider binary..."

    # Detect platform
    local os arch
    os=$(uname -s | tr '[:upper:]' '[:lower:]')
    case "$(uname -m)" in
        x86_64) arch="amd64" ;;
        arm64|aarch64) arch="arm64" ;;
        *) arch="amd64" ;;
    esac

    log_info "Detected platform: ${os}_${arch}"

    # Build binary
    local binary_name="terraform-provider-${PROVIDER_NAME}_v${PROVIDER_VERSION}"
    log_info "Building: $binary_name"

    cd /workspace
    if ! go build -o "$binary_name" . 2>&1; then
        log_error "Build failed"
        exit "$EXIT_BUILD_FAILURE"
    fi

    # Check binary was created
    if [ ! -f "$binary_name" ]; then
        log_error "Build failed: binary not found"
        exit "$EXIT_BUILD_FAILURE"
    fi

    local binary_size
    binary_size=$(du -h "$binary_name" | cut -f1)
    log_info "✓ Provider built successfully ($binary_size)"

    # Install to plugin directory
    local plugin_dir="$HOME/.terraform.d/plugins/registry.terraform.io/hashicorp/${PROVIDER_NAME}/${PROVIDER_VERSION}/${os}_${arch}"
    mkdir -p "$plugin_dir"
    cp "$binary_name" "$plugin_dir/"
    log_info "✓ Installed to: $plugin_dir"

    local build_end
    build_end=$(date +%s)
    BUILD_TIME=$((build_end - build_start))
    log_debug "Build completed in ${BUILD_TIME}s"
    log_info ""
}

#############################################################################
# Example Discovery
#############################################################################

discover_examples() {
    local examples_dir="/workspace/examples"
    local data_source_examples=()
    local resource_examples=()

    # Discover data source examples
    local data_sources_dir="$examples_dir/data-sources"
    if [ -d "$data_sources_dir" ]; then
        while IFS= read -r -d '' tf_file; do
            data_source_examples+=("$tf_file")
        done < <(find "$data_sources_dir" -mindepth 2 -maxdepth 2 -name "*.tf" -print0)
    fi

    # Discover resource examples
    local resources_dir="$examples_dir/resources"
    if [ -d "$resources_dir" ]; then
        while IFS= read -r -d '' tf_file; do
            resource_examples+=("$tf_file")
        done < <(find "$resources_dir" -mindepth 2 -maxdepth 2 -name "*.tf" -print0)
    fi

    local total_examples=$((${#data_source_examples[@]} + ${#resource_examples[@]}))
    if [ $total_examples -eq 0 ]; then
        log_error "No test examples found in $examples_dir"
        exit "$EXIT_CONFIG_ERROR"
    fi

    echo "${data_source_examples[*]} | ${resource_examples[*]}"
}

#############################################################################
# Test Execution
#############################################################################

test_example() {
    local example_file="$1"
    local example_index="$2"
    local total_examples="$3"
    local dir_name=$(basename "$(dirname "$example_file")")
    local file_name=$(basename "$example_file")
    local example_name="$dir_name/$file_name"

    local test_start
    test_start=$(date +%s)

    log_info "[$example_index/$total_examples] Testing $example_name..."

    # Create temporary working directory
    local temp_dir
    temp_dir=$(mktemp -d -t "${PROVIDER_NAME}-test-${dir_name}-XXXXX")

    # Copy example file
    cp "$example_file" "$temp_dir/"

    # Inject provider configuration if needed
    if ! grep -q "provider \"$PROVIDER_NAME\"" "$temp_dir"/*.tf 2>/dev/null; then
        cat > "$temp_dir/_provider.tf" <<EOF
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    $PROVIDER_NAME = {
      source  = "hashicorp/$PROVIDER_NAME"
      version = "~> 0.1"
    }
  }
}

provider "$PROVIDER_NAME" {
  # Provider configuration from environment variables
}
EOF
    fi

    cd "$temp_dir"

    local test_passed=true
    local error_output=""
    local failed_phase=""

    # Run terraform init
    if ! error_output=$(terraform init -backend=false 2>&1); then
        failed_phase="terraform init"
        test_passed=false
    fi

    # Run terraform validate
    if [ "$test_passed" = true ]; then
        if ! error_output=$(terraform validate 2>&1); then
            failed_phase="terraform validate"
            test_passed=false
        fi
    fi

    # Run terraform plan
    if [ "$test_passed" = true ]; then
        if ! error_output=$(terraform plan -out=tfplan 2>&1); then
            failed_phase="terraform plan"
            test_passed=false
        fi
    fi

    # Cleanup temp directory
    cd /workspace
    rm -rf "$temp_dir"

    local test_end
    test_end=$(date +%s)
    local test_time=$((test_end - test_start))

    if [ "$test_passed" = true ]; then
        log_pass "[PASS] ✓ $example_name (${test_time}s)"
        PASSED_COUNT=$((PASSED_COUNT + 1))
        return 0
    else
        log_fail "[FAIL] ✗ $example_name (${test_time}s)"
        log_error "       Failed at: $failed_phase"
        if [ "$VERBOSE" = true ]; then
            echo "$error_output" | while IFS= read -r line; do
                log_error "         $line"
            done
        fi
        FAILED_COUNT=$((FAILED_COUNT + 1))
        FAILED_EXAMPLES+=("$example_name")
        return 1
    fi
}

run_tests() {
    log_info "Phase 3: Testing examples..."

    local discovery_result
    discovery_result=$(discover_examples)

    local data_sources_list="${discovery_result%% | *}"
    local resources_list="${discovery_result##* | }"

    local data_source_examples=()
    local resource_examples=()

    if [ -n "$data_sources_list" ] && [ "$data_sources_list" != "" ]; then
        read -ra data_source_examples <<< "$data_sources_list"
    fi

    if [ -n "$resources_list" ] && [ "$resources_list" != "" ]; then
        read -ra resource_examples <<< "$resources_list"
    fi

    # Apply filters
    if [ "$RESOURCES_ONLY" = true ]; then
        data_source_examples=()
    fi

    if [ "$DATA_SOURCES_ONLY" = true ]; then
        resource_examples=()
    fi

    local total_examples=$((${#data_source_examples[@]} + ${#resource_examples[@]}))
    log_info "Found $total_examples example(s) to test"
    log_info ""

    # Test data sources
    if [ ${#data_source_examples[@]} -gt 0 ]; then
        log_info "Testing data sources..."
        local ds_index=0
        for example_dir in "${data_source_examples[@]}"; do
            ds_index=$((ds_index + 1))
            test_example "$example_dir" "$ds_index" "${#data_source_examples[@]}" || true
        done
        log_info ""
    fi

    # Test resources
    if [ ${#resource_examples[@]} -gt 0 ]; then
        log_info "Testing resources..."
        local res_index=0
        for example_dir in "${resource_examples[@]}"; do
            res_index=$((res_index + 1))
            test_example "$example_dir" "$res_index" "${#resource_examples[@]}" || true
        done
        log_info ""
    fi
}

#############################################################################
# Summary and Exit
#############################################################################

print_summary() {
    local end_time
    end_time=$(date +%s)
    local total_time=$((end_time - START_TIME))

    log_info "========================================"
    log_info "TEST SUMMARY"
    log_info "========================================"

    local total_tests=$((PASSED_COUNT + FAILED_COUNT))
    log_info "Examples tested: $total_tests"

    if [ $FAILED_COUNT -eq 0 ]; then
        log_pass "  Passed: $PASSED_COUNT"
        log_pass "  Failed: 0"
    else
        log_info "  Passed: $PASSED_COUNT"
        log_fail "  Failed: $FAILED_COUNT"
    fi
    log_info ""

    if [ $FAILED_COUNT -gt 0 ]; then
        log_info "Failed examples:"
        for example in "${FAILED_EXAMPLES[@]}"; do
            log_fail "  ✗ $example"
        done
        log_info ""
    fi

    log_info "Timing:"
    if [ $BUILD_TIME -gt 0 ]; then
        log_info "  Build: ${BUILD_TIME}s"
    fi
    log_info "  Total: ${total_time}s"
    log_info ""

    log_info "========================================"

    if [ $FAILED_COUNT -eq 0 ]; then
        log_pass "RESULT: All tests passed ✓"
    else
        log_fail "RESULT: $FAILED_COUNT test(s) failed ✗"
    fi

    log_info "========================================"
}

#############################################################################
# Main Execution
#############################################################################

main() {
    START_TIME=$(date +%s)

    validate_environment

    if [ "$CLEANUP_ONLY" = true ]; then
        log_info "Running in cleanup-only mode"
        log_info ""
        if cleanup_resources; then
            log_pass "Cleanup completed successfully"
            exit "$EXIT_SUCCESS"
        else
            log_fail "Cleanup failed"
            exit "$EXIT_TEST_FAILURE"
        fi
    fi

    build_provider
    run_tests

    if [ "$NO_CLEANUP" = false ]; then
        cleanup_resources || true
    fi

    print_summary

    if [ $FAILED_COUNT -eq 0 ]; then
        exit "$EXIT_SUCCESS"
    else
        exit "$EXIT_TEST_FAILURE"
    fi
}

main "$@"
