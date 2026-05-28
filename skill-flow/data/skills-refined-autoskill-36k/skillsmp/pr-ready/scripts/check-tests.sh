#!/bin/bash
#
# check-tests.sh
#
# Runs tests for Node.js/TypeScript and Python projects.
# Auto-detects the test framework and runs the appropriate command.
#
# Exit codes:
#   0 - Tests passed (or no tests found)
#   1 - Tests failed

set -uo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

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

# Check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if npm script exists
npm_script_exists() {
    local script=$1
    if [ -f "package.json" ]; then
        node -e "const pkg = require('./package.json'); process.exit(pkg.scripts && pkg.scripts['$script'] ? 0 : 1)" 2>/dev/null
        return $?
    fi
    return 1
}

# Run Node.js/TypeScript tests
run_node_tests() {
    log_info "Checking for Node.js test framework..."

    # Check for npm test script first (most common)
    if npm_script_exists "test"; then
        log_info "Found 'test' script in package.json"
        log_info "Running: npm test"
        echo ""
        if npm test; then
            log_success "Node.js tests passed"
            return 0
        else
            log_error "Node.js tests failed"
            return 1
        fi
    fi

    # Check for Jest directly
    if [ -f "node_modules/.bin/jest" ]; then
        log_info "Found Jest in node_modules"
        log_info "Running: npx jest"
        echo ""
        if npx jest; then
            log_success "Jest tests passed"
            return 0
        else
            log_error "Jest tests failed"
            return 1
        fi
    fi

    # Check for Vitest
    if [ -f "node_modules/.bin/vitest" ]; then
        log_info "Found Vitest in node_modules"
        log_info "Running: npx vitest run"
        echo ""
        if npx vitest run; then
            log_success "Vitest tests passed"
            return 0
        else
            log_error "Vitest tests failed"
            return 1
        fi
    fi

    # Check for Mocha
    if [ -f "node_modules/.bin/mocha" ]; then
        log_info "Found Mocha in node_modules"
        log_info "Running: npx mocha"
        echo ""
        if npx mocha; then
            log_success "Mocha tests passed"
            return 0
        else
            log_error "Mocha tests failed"
            return 1
        fi
    fi

    # Check for Bun test
    if [ -f "bun.lockb" ] && command_exists bun; then
        log_info "Found Bun project"
        log_info "Running: bun test"
        echo ""
        if bun test; then
            log_success "Bun tests passed"
            return 0
        else
            log_error "Bun tests failed"
            return 1
        fi
    fi

    log_warn "No Node.js test framework detected"
    log_info "Install a test framework: npm install --save-dev jest"
    return 0
}

# Run Python tests
run_python_tests() {
    log_info "Checking for Python test framework..."

    # Check for pytest
    if command_exists pytest; then
        log_info "Found pytest"
        log_info "Running: pytest"
        echo ""
        if pytest; then
            log_success "pytest tests passed"
            return 0
        else
            log_error "pytest tests failed"
            return 1
        fi
    fi

    # Check for pytest in virtual environment
    if [ -f ".venv/bin/pytest" ]; then
        log_info "Found pytest in .venv"
        log_info "Running: .venv/bin/pytest"
        echo ""
        if .venv/bin/pytest; then
            log_success "pytest tests passed"
            return 0
        else
            log_error "pytest tests failed"
            return 1
        fi
    fi

    # Check for unittest (built-in)
    if [ -d "tests" ] || [ -d "test" ]; then
        log_info "Found tests directory, trying unittest"
        log_info "Running: python -m unittest discover"
        echo ""
        if python -m unittest discover; then
            log_success "unittest tests passed"
            return 0
        else
            log_error "unittest tests failed"
            return 1
        fi
    fi

    log_warn "No Python test framework detected"
    log_info "Install pytest: pip install pytest"
    return 0
}

# Detect project type and run appropriate tests
main() {
    local node_project=false
    local python_project=false
    local result=0

    # Detect Node.js project
    if [ -f "package.json" ] || [ -f "tsconfig.json" ]; then
        node_project=true
    fi

    # Detect Python project
    if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        python_project=true
    fi

    if [ "$node_project" = false ] && [ "$python_project" = false ]; then
        log_warn "No Node.js or Python project detected"
        exit 0
    fi

    # Run Node.js tests
    if [ "$node_project" = true ]; then
        if ! run_node_tests; then
            result=1
        fi
        echo ""
    fi

    # Run Python tests
    if [ "$python_project" = true ]; then
        if ! run_python_tests; then
            result=1
        fi
    fi

    exit $result
}

main "$@"
