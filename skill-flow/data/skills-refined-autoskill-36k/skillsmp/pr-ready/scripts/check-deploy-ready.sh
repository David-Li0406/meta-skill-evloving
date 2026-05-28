#!/bin/bash
#
# check-deploy-ready.sh
#
# Unified deployment readiness checker for Node.js/TypeScript and Python projects.
# Runs type checking, linting, tests, and generates truncated diff for AI code review.
#
# Exit codes:
#   0 - All checks passed
#   1 - One or more checks failed

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SHARED_DIR="$SCRIPT_DIR/../../../shared/utils"

# Max lines for diff output (to stay within AI context limits)
MAX_DIFF_LINES=${MAX_DIFF_LINES:-500}

# Source shared utilities if available
if [ -f "$SHARED_DIR/project-detect.sh" ]; then
    source "$SHARED_DIR/project-detect.sh"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

log_header() {
    echo -e "\n${BOLD}${CYAN}============================================================${RESET}"
    echo -e "${BOLD}${CYAN}  $1${RESET}"
    echo -e "${BOLD}${CYAN}============================================================${RESET}"
}

log_info() {
    echo -e "${BLUE}[INFO]${RESET} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${RESET} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARNING]${RESET} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${RESET} $*"
}

# Generate truncated diff for AI code review
generate_diff_for_review() {
    if [ ! -d ".git" ]; then
        log_warn "Not a git repository. Skipping diff generation."
        return
    fi

    # Get list of changed files
    local changed_files
    changed_files=$(git diff --name-only HEAD 2>/dev/null || git diff --name-only 2>/dev/null)

    if [ -z "$changed_files" ]; then
        log_info "No changes to review."
        return
    fi

    # Get file stats
    local file_count
    file_count=$(echo "$changed_files" | wc -l | tr -d ' ')

    log_header "Code Review Diff"
    echo ""
    log_info "Changed files ($file_count):"
    echo "$changed_files" | while read -r file; do
        echo "  - $file"
    done
    echo ""

    # Generate diff and truncate if needed
    local full_diff
    full_diff=$(git diff HEAD 2>/dev/null || git diff 2>/dev/null)

    local total_lines
    total_lines=$(echo "$full_diff" | wc -l | tr -d ' ')

    if [ "$total_lines" -gt "$MAX_DIFF_LINES" ]; then
        log_warn "Diff is $total_lines lines. Truncating to $MAX_DIFF_LINES lines for AI review."
        echo ""
        echo '```diff'
        echo "$full_diff" | head -n "$MAX_DIFF_LINES"
        echo '```'
        echo ""
        echo "[... truncated $((total_lines - MAX_DIFF_LINES)) more lines ...]"
    else
        echo '```diff'
        echo "$full_diff"
        echo '```'
    fi
}

# Print summary
print_summary() {
    local type_result=$1
    local lint_result=$2
    local test_result=$3

    echo ""
    log_header "Deployment Readiness Summary"
    echo ""

    if [ "$type_result" -eq 0 ]; then
        echo -e "  Type Checking:  ${GREEN}PASSED${RESET}"
    else
        echo -e "  Type Checking:  ${RED}FAILED${RESET}"
    fi

    if [ "$lint_result" -eq 0 ]; then
        echo -e "  Linting:        ${GREEN}PASSED${RESET}"
    else
        echo -e "  Linting:        ${RED}FAILED${RESET}"
    fi

    if [ "$test_result" -eq 0 ]; then
        echo -e "  Tests:          ${GREEN}PASSED${RESET}"
    else
        echo -e "  Tests:          ${RED}FAILED${RESET}"
    fi

    echo ""

    if [ "$type_result" -eq 0 ] && [ "$lint_result" -eq 0 ] && [ "$test_result" -eq 0 ]; then
        echo -e "${GREEN}${BOLD}All automated checks passed!${RESET}"
        echo ""
        log_info "Please review the diff above for code quality issues."
        return 0
    else
        echo -e "${RED}${BOLD}Some checks failed. Please fix the issues above.${RESET}"
        return 1
    fi
}

# Detect project type
detect_project() {
    local types=""

    if [ -f "package.json" ] || [ -f "tsconfig.json" ]; then
        types="node"
    fi

    if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        if [ -n "$types" ]; then
            types="$types,python"
        else
            types="python"
        fi
    fi

    echo "$types"
}

# Main
main() {
    log_header "Deployment Readiness Check"

    # Detect project type
    local project_type
    project_type=$(detect_project)

    if [ -z "$project_type" ]; then
        log_warn "No Node.js or Python project detected in current directory"
        log_info "Looking for: package.json, tsconfig.json, pyproject.toml, setup.py, requirements.txt"
        exit 0
    fi

    log_info "Detected project type(s): $project_type"
    echo ""

    # Run type checking
    local type_result=0
    log_info "Running type checker..."
    if ! bash "$SCRIPT_DIR/check-types.sh"; then
        type_result=1
    fi

    # Run linting
    local lint_result=0
    log_info "Running linter..."
    if ! bash "$SCRIPT_DIR/check-lint.sh"; then
        lint_result=1
    fi

    # Run tests
    local test_result=0
    log_info "Running tests..."
    if ! bash "$SCRIPT_DIR/check-tests.sh"; then
        test_result=1
    fi

    # Generate diff for AI code review
    generate_diff_for_review

    # Print summary
    if print_summary "$type_result" "$lint_result" "$test_result"; then
        exit 0
    else
        exit 1
    fi
}

main "$@"
