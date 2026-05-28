#!/bin/bash
#
# check-lint.sh
#
# Auto-detect and run linter for Node.js/TypeScript or Python projects.
# Finds local tools first, falls back to global, gracefully handles missing tools.
#
# Exit codes:
#   0 - Linting passed or no linter needed
#   1 - Lint errors found

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

# Detect Node.js linter
detect_node_linter() {
    # Check for Biome
    if [ -f "biome.json" ] || [ -f "biome.jsonc" ]; then
        echo "biome"
        return
    fi

    # Check for ESLint config files
    if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.cjs" ] || [ -f ".eslintrc.json" ] || \
       [ -f ".eslintrc.yaml" ] || [ -f ".eslintrc.yml" ] || [ -f ".eslintrc" ]; then
        echo "eslint"
        return
    fi

    # Check for flat config ESLint
    if [ -f "eslint.config.js" ] || [ -f "eslint.config.mjs" ] || [ -f "eslint.config.cjs" ]; then
        echo "eslint"
        return
    fi

    # Check for local ESLint installation
    if [ -f "node_modules/.bin/eslint" ]; then
        echo "eslint"
        return
    fi

    # Check for local Biome installation
    if [ -f "node_modules/.bin/biome" ]; then
        echo "biome"
        return
    fi

    echo ""
}

# Detect Python linter
detect_python_linter() {
    # Check for ruff config
    if [ -f "ruff.toml" ] || [ -f ".ruff.toml" ]; then
        echo "ruff"
        return
    fi

    # Check for ruff in pyproject.toml
    if [ -f "pyproject.toml" ] && grep -q "\[tool.ruff\]" pyproject.toml 2>/dev/null; then
        echo "ruff"
        return
    fi

    # Check for flake8 config
    if [ -f ".flake8" ] || [ -f "setup.cfg" ] && grep -q "\[flake8\]" setup.cfg 2>/dev/null; then
        echo "flake8"
        return
    fi

    # Try available commands
    if command -v ruff &> /dev/null; then
        echo "ruff"
    elif command -v flake8 &> /dev/null; then
        echo "flake8"
    elif command -v pylint &> /dev/null; then
        echo "pylint"
    else
        echo ""
    fi
}

# Run Node.js linting
check_node_lint() {
    log_header "Node.js/TypeScript Linting"

    if [ ! -f "package.json" ] && [ ! -f "tsconfig.json" ]; then
        log_info "No Node.js project found, skipping Node.js lint check"
        return 0
    fi

    local linter
    linter=$(detect_node_linter)

    if [ -z "$linter" ]; then
        log_warn "No Node.js linter detected"
        log_info "Install with: npm install eslint --save-dev"
        return 0
    fi

    log_info "Detected linter: $linter"

    case "$linter" in
        biome)
            log_info "Running Biome..."
            if [ -f "node_modules/.bin/biome" ]; then
                if ./node_modules/.bin/biome check .; then
                    log_success "Linting passed! No Biome errors found."
                    return 0
                else
                    log_error "Linting failed!"
                    echo ""
                    log_info "Auto-fix available: npx biome check --apply ."
                    return 1
                fi
            else
                log_warn "Biome not installed locally. Run: npm install @biomejs/biome --save-dev"
                return 0
            fi
            ;;
        eslint)
            log_info "Running ESLint..."
            local eslint_cmd=""

            if [ -f "node_modules/.bin/eslint" ]; then
                eslint_cmd="./node_modules/.bin/eslint"
            elif command -v eslint &> /dev/null; then
                eslint_cmd="eslint"
            fi

            if [ -z "$eslint_cmd" ]; then
                log_warn "ESLint not installed. Run: npm install eslint --save-dev"
                return 0
            fi

            # Determine extensions based on project
            local extensions=".js,.jsx"
            if [ -f "tsconfig.json" ]; then
                extensions=".ts,.tsx,.js,.jsx"
            fi

            if $eslint_cmd . --ext "$extensions" 2>/dev/null; then
                log_success "Linting passed! No ESLint errors found."
                return 0
            else
                log_error "Linting failed!"
                echo ""
                log_info "Auto-fix available: $eslint_cmd . --ext $extensions --fix"
                return 1
            fi
            ;;
    esac
}

# Run Python linting
check_python_lint() {
    log_header "Python Linting"

    if [ ! -f "pyproject.toml" ] && [ ! -f "setup.py" ] && [ ! -f "requirements.txt" ]; then
        log_info "No Python project found, skipping Python lint check"
        return 0
    fi

    local linter
    linter=$(detect_python_linter)

    if [ -z "$linter" ]; then
        log_warn "No Python linter detected"
        log_info "Install with: pip install ruff  or  pip install flake8"
        return 0
    fi

    log_info "Detected linter: $linter"

    case "$linter" in
        ruff)
            log_info "Running ruff..."
            if ruff check .; then
                log_success "Linting passed! No ruff errors found."
                return 0
            else
                log_error "Linting failed!"
                echo ""
                log_info "Auto-fix available: ruff check --fix ."
                return 1
            fi
            ;;
        flake8)
            log_info "Running flake8..."
            if flake8 .; then
                log_success "Linting passed! No flake8 errors found."
                return 0
            else
                log_error "Linting failed!"
                return 1
            fi
            ;;
        pylint)
            log_info "Running pylint..."
            # Find Python files
            local py_files
            py_files=$(find . -name "*.py" -not -path "./venv/*" -not -path "./.venv/*" -not -path "./.*" 2>/dev/null | head -100)

            if [ -z "$py_files" ]; then
                log_info "No Python files found"
                return 0
            fi

            if echo "$py_files" | xargs pylint --exit-zero 2>/dev/null; then
                log_success "Linting completed."
                return 0
            else
                log_error "Linting failed!"
                return 1
            fi
            ;;
    esac
}

# Main
main() {
    local exit_code=0
    local is_node=false
    local is_python=false

    # Detect project types
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

    # Run appropriate linters
    if [ "$is_node" = true ]; then
        if ! check_node_lint; then
            exit_code=1
        fi
    fi

    if [ "$is_python" = true ]; then
        if ! check_python_lint; then
            exit_code=1
        fi
    fi

    exit $exit_code
}

main "$@"
