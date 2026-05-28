#!/bin/bash
#
# check-types.sh
#
# Auto-detect and run type checker for Node.js/TypeScript or Python projects.
# Finds local tools first, falls back to global, gracefully handles missing tools.
#
# Exit codes:
#   0 - Type checks passed or no type checker needed
#   1 - Type errors found

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SHARED_DIR="$SCRIPT_DIR/../../../shared/utils"

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
RESET='\033[0m'

log_header() {
    echo -e "\n${CYAN}============================================================${RESET}"
    echo -e "${CYAN}  $1${RESET}"
    echo -e "${CYAN}============================================================${RESET}"
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

# Find TypeScript compiler - local first, then global
find_tsc() {
    if [ -f "node_modules/.bin/tsc" ]; then
        echo "./node_modules/.bin/tsc"
    elif command -v tsc &> /dev/null; then
        echo "tsc"
    else
        echo ""
    fi
}

# Run TypeScript type checking
check_typescript() {
    log_header "TypeScript Type Checking"

    if [ ! -f "tsconfig.json" ]; then
        log_info "No tsconfig.json found, skipping TypeScript check"
        return 0
    fi

    local tsc_cmd
    tsc_cmd=$(find_tsc)

    if [ -z "$tsc_cmd" ]; then
        log_warn "TypeScript not found. Install with: npm install typescript --save-dev"
        return 0
    fi

    log_info "Running TypeScript compiler in check mode..."
    log_info "Using: $tsc_cmd"

    if $tsc_cmd --noEmit; then
        log_success "Type checking passed! No TypeScript errors found."
        return 0
    else
        log_error "Type checking failed!"
        echo ""
        log_info "Tips to fix type errors:"
        echo "  - Review the error messages above"
        echo "  - Add missing type annotations"
        echo "  - Fix type incompatibilities"
        echo "  - Check for missing @types/* packages"
        return 1
    fi
}

# Run Python type checking
check_python() {
    log_header "Python Type Checking"

    # Check if this is a Python project
    if [ ! -f "pyproject.toml" ] && [ ! -f "setup.py" ] && [ ! -f "requirements.txt" ]; then
        log_info "No Python project files found, skipping Python type check"
        return 0
    fi

    # Try mypy first
    if command -v mypy &> /dev/null; then
        log_info "Running mypy type checker..."

        if mypy . --ignore-missing-imports 2>/dev/null; then
            log_success "Type checking passed! No mypy errors found."
            return 0
        else
            log_error "Type checking failed!"
            return 1
        fi
    fi

    # Try pyright
    if command -v pyright &> /dev/null; then
        log_info "Running pyright type checker..."

        if pyright; then
            log_success "Type checking passed! No pyright errors found."
            return 0
        else
            log_error "Type checking failed!"
            return 1
        fi
    fi

    log_warn "No Python type checker found (mypy/pyright)"
    log_info "Install with: pip install mypy  or  pip install pyright"
    return 0
}

# Main
main() {
    local exit_code=0
    local is_node=false
    local is_python=false

    # Detect project types (a project can be both)
    if [ -f "package.json" ] || [ -f "tsconfig.json" ]; then
        is_node=true
    fi

    if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        is_python=true
    fi

    if [ "$is_node" = false ] && [ "$is_python" = false ]; then
        log_warn "No Node.js or Python project detected"
        exit 0
    fi

    # Run appropriate type checkers
    if [ "$is_node" = true ]; then
        if ! check_typescript; then
            exit_code=1
        fi
    fi

    if [ "$is_python" = true ]; then
        if ! check_python; then
            exit_code=1
        fi
    fi

    exit $exit_code
}

main "$@"
