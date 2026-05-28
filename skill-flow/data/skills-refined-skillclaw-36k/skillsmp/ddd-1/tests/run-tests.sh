#!/bin/bash

# Run validation tests for DDD skill
# Usage: ./run-tests.sh [options] [suites...]
#
# Options:
#   --json          Output results as JSON
#   --timing        Show detailed timing info
#   --verbose       Show all test output
#   --quiet         Only show summary
#
# Suites:
#   agents          Agent structure validation
#   content         Content quality validation
#   routing         Routing configuration validation
#   examples        Code examples validation
#   all             Run all suites (default)
#
# Examples:
#   ./run-tests.sh                    # Run all tests
#   ./run-tests.sh agents content     # Run specific suites
#   ./run-tests.sh --json             # Output as JSON
#   ./run-tests.sh --timing agents    # Run with timing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Options
JSON_OUTPUT=false
SHOW_TIMING=false
VERBOSE=false
QUIET=false

# Results storage
declare -a SUITE_NAMES=()
declare -a SUITE_RESULTS=()
declare -a SUITE_TIMES=()
declare -a SUITE_PASSED=()
declare -a SUITE_FAILED=()

TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_TIME=0

# Parse options
SUITES=()
while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      JSON_OUTPUT=true
      QUIET=true
      shift
      ;;
    --timing)
      SHOW_TIMING=true
      shift
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    --quiet)
      QUIET=true
      shift
      ;;
    --help|-h)
      head -25 "$0" | tail -23
      exit 0
      ;;
    agents|content|routing|examples|all)
      SUITES+=("$1")
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Default to all suites
if [ ${#SUITES[@]} -eq 0 ]; then
  SUITES=("all")
fi

# Expand "all" to individual suites
if [[ " ${SUITES[*]} " =~ " all " ]]; then
  SUITES=("agents" "content" "routing" "examples")
fi

# Get current timestamp in ms
get_time_ms() {
  date +%s%3N 2>/dev/null || python3 -c 'import time; print(int(time.time() * 1000))'
}

# Format duration
format_duration() {
  local ms=$1
  if [ "$ms" -lt 1000 ]; then
    echo "${ms}ms"
  else
    local secs=$((ms / 1000))
    local rem=$((ms % 1000))
    echo "${secs}.${rem}s"
  fi
}

# Print header
print_header() {
  if [ "$QUIET" = false ]; then
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║           DDD Skill Validation Test Suite                      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
  fi
}

# Run a single test suite
run_test() {
  local suite_key=$1
  local test_name=$2
  local test_file=$3

  if [ "$QUIET" = false ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 Running: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  fi

  local start_time=$(get_time_ms)
  local output
  local exit_code=0

  # Capture output and exit code
  output=$(node "$SCRIPT_DIR/$test_file" 2>&1) || exit_code=$?

  local end_time=$(get_time_ms)
  local duration=$((end_time - start_time))

  # Extract passed/failed counts from output
  local passed=$(echo "$output" | grep -oP '(\d+) passed' | head -1 | grep -oP '\d+' || echo "0")
  local failed=$(echo "$output" | grep -oP '(\d+) failed' | head -1 | grep -oP '\d+' || echo "0")

  # Store results
  SUITE_NAMES+=("$test_name")
  SUITE_TIMES+=("$duration")
  SUITE_PASSED+=("$passed")
  SUITE_FAILED+=("$failed")

  if [ $exit_code -eq 0 ]; then
    SUITE_RESULTS+=("passed")
    if [ "$QUIET" = false ]; then
      if [ "$VERBOSE" = true ]; then
        echo "$output"
      fi
      if [ "$SHOW_TIMING" = true ]; then
        echo "✅ $test_name: PASSED ($(format_duration $duration))"
      else
        echo "✅ $test_name: PASSED"
      fi
    fi
  else
    SUITE_RESULTS+=("failed")
    TOTAL_FAILED=$((TOTAL_FAILED + 1))
    if [ "$QUIET" = false ]; then
      echo "$output"
      if [ "$SHOW_TIMING" = true ]; then
        echo "❌ $test_name: FAILED ($(format_duration $duration))"
      else
        echo "❌ $test_name: FAILED"
      fi
    fi
  fi

  TOTAL_TIME=$((TOTAL_TIME + duration))

  if [ "$QUIET" = false ]; then
    echo ""
  fi
}

# Map suite key to name and file
get_suite_info() {
  case $1 in
    agents)   echo "Agent Structure|validate-agents.test.js" ;;
    content)  echo "Content Quality|validate-content.test.js" ;;
    routing)  echo "Routing Configuration|validate-routing.test.js" ;;
    examples) echo "Code Examples|validate-examples.test.js" ;;
  esac
}

# Output JSON results
output_json() {
  local timestamp=$(date -Iseconds)
  local total_suites=${#SUITE_NAMES[@]}
  local passed_suites=$((total_suites - TOTAL_FAILED))

  echo "{"
  echo "  \"timestamp\": \"$timestamp\","
  echo "  \"version\": \"1.0.0\","
  echo "  \"totalDuration\": $TOTAL_TIME,"
  echo "  \"totalDurationFormatted\": \"$(format_duration $TOTAL_TIME)\","
  echo "  \"summary\": {"
  echo "    \"suites\": $total_suites,"
  echo "    \"passed\": $passed_suites,"
  echo "    \"failed\": $TOTAL_FAILED"
  echo "  },"
  echo "  \"suites\": ["

  for i in "${!SUITE_NAMES[@]}"; do
    local comma=""
    if [ $i -lt $((${#SUITE_NAMES[@]} - 1)) ]; then
      comma=","
    fi
    echo "    {"
    echo "      \"name\": \"${SUITE_NAMES[$i]}\","
    echo "      \"result\": \"${SUITE_RESULTS[$i]}\","
    echo "      \"duration\": ${SUITE_TIMES[$i]},"
    echo "      \"durationFormatted\": \"$(format_duration ${SUITE_TIMES[$i]})\","
    echo "      \"tests\": {"
    echo "        \"passed\": ${SUITE_PASSED[$i]},"
    echo "        \"failed\": ${SUITE_FAILED[$i]}"
    echo "      }"
    echo "    }$comma"
  done

  echo "  ]"
  echo "}"
}

# Print summary
print_summary() {
  if [ "$QUIET" = false ]; then
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    if [ "$SHOW_TIMING" = true ]; then
      echo "📊 Test Suite Summary"
      echo "────────────────────────────────────────────────────────────────"
      printf "%-25s %-10s %-12s %s\n" "Suite" "Result" "Duration" "Tests"
      echo "────────────────────────────────────────────────────────────────"

      for i in "${!SUITE_NAMES[@]}"; do
        local result_icon="✅"
        if [ "${SUITE_RESULTS[$i]}" = "failed" ]; then
          result_icon="❌"
        fi
        printf "%-25s %s %-8s %-12s %s/%s\n" \
          "${SUITE_NAMES[$i]}" \
          "$result_icon" \
          "${SUITE_RESULTS[$i]}" \
          "$(format_duration ${SUITE_TIMES[$i]})" \
          "${SUITE_PASSED[$i]}" \
          "$((${SUITE_PASSED[$i]} + ${SUITE_FAILED[$i]}))"
      done

      echo "────────────────────────────────────────────────────────────────"
      echo "Total time: $(format_duration $TOTAL_TIME)"
      echo ""
    fi

    if [ $TOTAL_FAILED -eq 0 ]; then
      echo "✅ All ${#SUITE_NAMES[@]} test suites passed!"
    else
      echo "❌ $TOTAL_FAILED of ${#SUITE_NAMES[@]} test suite(s) failed"
    fi
    echo "════════════════════════════════════════════════════════════════"
  fi
}

# Main execution
main() {
  print_header

  for suite in "${SUITES[@]}"; do
    local info=$(get_suite_info "$suite")
    local name=$(echo "$info" | cut -d'|' -f1)
    local file=$(echo "$info" | cut -d'|' -f2)
    run_test "$suite" "$name" "$file"
  done

  if [ "$JSON_OUTPUT" = true ]; then
    output_json
  else
    print_summary
  fi

  if [ $TOTAL_FAILED -gt 0 ]; then
    exit 1
  fi
}

main
