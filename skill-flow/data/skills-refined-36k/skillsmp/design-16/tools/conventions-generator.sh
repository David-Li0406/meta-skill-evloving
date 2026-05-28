#!/bin/bash
#
# conventions-generator.sh
# Analyzes a codebase and generates a comprehensive CONVENTIONS.md
#
# Usage: ./conventions-generator.sh <codebase-path> [--output path] [--verbose]
#
# Author: DesignOps Tooling
# Version: 1.0.0
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
VERBOSE=false
OUTPUT_PATH=""
CODEBASE_PATH=""

# Directories to skip (escaped for grep -E)
SKIP_DIRS="node_modules|__pycache__|\.git|\.svn|\.hg|dist|build|\.next|\.nuxt|coverage|\.pytest_cache|\.mypy_cache|\.tox|\.eggs|egg-info|venv|\.venv|env|\.env|vendor|Pods|\.gradle|target|bin|obj|out|\.idea|\.vscode"

# ============================================================================
# Utility Functions
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

show_usage() {
    cat << EOF
Usage: $(basename "$0") <codebase-path> [options]

Analyzes a codebase and generates a comprehensive CONVENTIONS.md file.

Arguments:
  <codebase-path>    Path to the codebase to analyze

Options:
  --output, -o       Output path for CONVENTIONS.md (default: <codebase-path>/CONVENTIONS.md)
  --verbose, -v      Enable verbose output
  --help, -h         Show this help message

Examples:
  $(basename "$0") ./my-project
  $(basename "$0") /path/to/project --output ./docs/CONVENTIONS.md
  $(basename "$0") . -v
EOF
}

# ============================================================================
# Parse Arguments
# ============================================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --output|-o)
                OUTPUT_PATH="$2"
                shift 2
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                if [[ -z "$CODEBASE_PATH" ]]; then
                    CODEBASE_PATH="$1"
                else
                    log_error "Multiple codebase paths specified"
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate codebase path
    if [[ -z "$CODEBASE_PATH" ]]; then
        log_error "Codebase path is required"
        show_usage
        exit 1
    fi

    if [[ ! -d "$CODEBASE_PATH" ]]; then
        log_error "Codebase path does not exist or is not a directory: $CODEBASE_PATH"
        exit 1
    fi

    # Convert to absolute path
    CODEBASE_PATH="$(cd "$CODEBASE_PATH" && pwd)"

    # Set default output path
    if [[ -z "$OUTPUT_PATH" ]]; then
        OUTPUT_PATH="$CODEBASE_PATH/CONVENTIONS.md"
    fi

    log_verbose "Codebase path: $CODEBASE_PATH"
    log_verbose "Output path: $OUTPUT_PATH"
}

# ============================================================================
# Detection Functions
# ============================================================================

detect_languages() {
    log_info "Detecting programming languages..." >&2

    local languages=()
    local counts=()

    # Count files by extension
    local py_count=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local js_count=$(find "$CODEBASE_PATH" -type f -name "*.js" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local ts_count=$(find "$CODEBASE_PATH" -type f -name "*.ts" -o -name "*.tsx" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local go_count=$(find "$CODEBASE_PATH" -type f -name "*.go" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local rs_count=$(find "$CODEBASE_PATH" -type f -name "*.rs" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local java_count=$(find "$CODEBASE_PATH" -type f -name "*.java" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local rb_count=$(find "$CODEBASE_PATH" -type f -name "*.rb" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local sh_count=$(find "$CODEBASE_PATH" -type f -name "*.sh" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local css_count=$(find "$CODEBASE_PATH" -type f \( -name "*.css" -o -name "*.scss" -o -name "*.sass" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')

    # Build language list
    [[ $py_count -gt 0 ]] && languages+=("Python:$py_count")
    [[ $js_count -gt 0 ]] && languages+=("JavaScript:$js_count")
    [[ $ts_count -gt 0 ]] && languages+=("TypeScript:$ts_count")
    [[ $go_count -gt 0 ]] && languages+=("Go:$go_count")
    [[ $rs_count -gt 0 ]] && languages+=("Rust:$rs_count")
    [[ $java_count -gt 0 ]] && languages+=("Java:$java_count")
    [[ $rb_count -gt 0 ]] && languages+=("Ruby:$rb_count")
    [[ $sh_count -gt 0 ]] && languages+=("Shell:$sh_count")
    [[ $css_count -gt 0 ]] && languages+=("CSS/SCSS:$css_count")

    # Handle empty languages array
    if [[ ${#languages[@]} -eq 0 ]]; then
        echo "No code files detected"
        return
    fi

    # Sort by count (descending)
    local sorted_output
    sorted_output=$(printf '%s\n' "${languages[@]}" | sort -t: -k2 -nr)

    echo "$sorted_output"
}

analyze_file_naming() {
    log_info "Analyzing file naming conventions..." >&2

    local result=""

    # Check for different naming patterns
    local snake_case=$(find "$CODEBASE_PATH" -type f \( -name "*_*.py" -o -name "*_*.js" -o -name "*_*.ts" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local kebab_case=$(find "$CODEBASE_PATH" -type f \( -name "*-*.js" -o -name "*-*.ts" -o -name "*-*.tsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local pascal_case=$(find "$CODEBASE_PATH" -type f -regex '.*[A-Z][a-z]*[A-Z].*\.\(js\|ts\|tsx\|jsx\)' 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local camel_case=$(find "$CODEBASE_PATH" -type f -regex '.*[a-z][A-Z].*\.\(js\|ts\)' 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')

    # Detect test file patterns
    local test_prefix=$(find "$CODEBASE_PATH" -type f -name "test_*" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local test_suffix=$(find "$CODEBASE_PATH" -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')

    # Build result
    result="### Detected Patterns\n\n"
    result+="| Pattern | Count | Notes |\n"
    result+="|---------|-------|-------|\n"
    [[ $snake_case -gt 0 ]] && result+="| snake_case | $snake_case | Common in Python |\n"
    [[ $kebab_case -gt 0 ]] && result+="| kebab-case | $kebab_case | Common in web projects |\n"
    [[ $pascal_case -gt 0 ]] && result+="| PascalCase | $pascal_case | Components/Classes |\n"

    result+="\n### Test File Naming\n\n"
    if [[ $test_prefix -gt $test_suffix && $test_prefix -gt 0 ]]; then
        result+="- Primary pattern: \`test_*.py\` (prefix style, $test_prefix files)\n"
    elif [[ $test_suffix -gt 0 ]]; then
        result+="- Primary pattern: \`*.test.*\` or \`*.spec.*\` (suffix style, $test_suffix files)\n"
    else
        result+="- No consistent test file naming pattern detected\n"
    fi

    echo -e "$result"
}

analyze_directory_structure() {
    log_info "Analyzing directory structure..." >&2

    local result=""

    result="\`\`\`\n"
    result+="$(basename "$CODEBASE_PATH")/\n"

    # Get top-level directories using null-terminated output for safety with spaces
    while IFS= read -r -d '' dir; do
        local dirname=$(basename "$dir")
        # Skip common non-essential directories
        if [[ ! "$dirname" =~ ^(node_modules|__pycache__|\.git|dist|build|coverage|venv|\.venv)$ ]]; then
            result+="├── $dirname/\n"
            # Show one level of subdirectories
            while IFS= read -r -d '' subdir; do
                local subdirname=$(basename "$subdir")
                if [[ ! "$subdirname" =~ ^(node_modules|__pycache__|\.git)$ ]]; then
                    result+="│   ├── $subdirname/\n"
                fi
            done < <(find "$dir" -maxdepth 1 -type d ! -path "$dir" -print0 2>/dev/null | head -c 10000 | sort -z)
        fi
    done < <(find "$CODEBASE_PATH" -maxdepth 1 -type d ! -name ".*" ! -path "$CODEBASE_PATH" -print0 2>/dev/null | sort -z)

    result+="\`\`\`\n"

    # Detect common patterns
    result+="\n### Detected Patterns\n\n"

    if [[ -d "$CODEBASE_PATH/src" ]]; then
        result+="- **Source directory**: \`src/\` - Main source code\n"
    fi
    if [[ -d "$CODEBASE_PATH/lib" ]]; then
        result+="- **Library directory**: \`lib/\` - Shared libraries/utilities\n"
    fi
    if [[ -d "$CODEBASE_PATH/tests" || -d "$CODEBASE_PATH/test" || -d "$CODEBASE_PATH/__tests__" ]]; then
        result+="- **Test directory**: Tests are separated from source\n"
    fi
    if [[ -d "$CODEBASE_PATH/docs" ]]; then
        result+="- **Documentation**: \`docs/\` directory present\n"
    fi
    if [[ -d "$CODEBASE_PATH/scripts" ]]; then
        result+="- **Scripts**: \`scripts/\` for build/utility scripts\n"
    fi
    if [[ -d "$CODEBASE_PATH/config" || -d "$CODEBASE_PATH/configs" ]]; then
        result+="- **Configuration**: Centralized config directory\n"
    fi

    echo -e "$result"
}

analyze_imports() {
    log_info "Analyzing import patterns..." >&2

    local result=""

    # Python imports
    local py_files=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -20)
    if [[ -n "$py_files" ]]; then
        result+="### Python Imports\n\n"

        # Check for absolute vs relative imports
        local absolute_imports=$(grep -h "^from [a-zA-Z]" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local relative_imports=$(grep -h "^from \." $py_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $absolute_imports -gt $relative_imports ]]; then
            result+="- **Style**: Absolute imports preferred ($absolute_imports absolute vs $relative_imports relative)\n"
        else
            result+="- **Style**: Relative imports common ($relative_imports relative vs $absolute_imports absolute)\n"
        fi

        # Check for import grouping
        result+="- **Import order**: "
        if grep -q "^import " <<< "$(head -30 $(echo $py_files | tr ' ' '\n' | head -1) 2>/dev/null)"; then
            result+="Standard library imports typically first\n"
        else
            result+="Check individual files for ordering\n"
        fi

        # Common third-party imports
        local common_imports=$(grep -oh "^from [a-zA-Z_][a-zA-Z0-9_]*" $py_files 2>/dev/null | sort | uniq -c | sort -rn | head -5)
        if [[ -n "$common_imports" ]]; then
            result+="\n**Common imports**:\n\`\`\`\n$common_imports\n\`\`\`\n"
        fi
        result+="\n"
    fi

    # JavaScript/TypeScript imports
    local js_files=$(find "$CODEBASE_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.jsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -20)
    if [[ -n "$js_files" ]]; then
        result+="### JavaScript/TypeScript Imports\n\n"

        # Check for ES modules vs CommonJS
        local es_imports=$(grep -h "^import " $js_files 2>/dev/null | wc -l | tr -d ' ')
        local cjs_requires=$(grep -h "require(" $js_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $es_imports -gt $cjs_requires ]]; then
            result+="- **Module style**: ES Modules (\`import/export\`) - $es_imports occurrences\n"
        elif [[ $cjs_requires -gt 0 ]]; then
            result+="- **Module style**: CommonJS (\`require/module.exports\`) - $cjs_requires occurrences\n"
        fi

        # Check for path aliases
        if grep -q "from '@/" $js_files 2>/dev/null; then
            result+="- **Path aliases**: \`@/\` alias detected for imports\n"
        fi
        if grep -q "from '~/" $js_files 2>/dev/null; then
            result+="- **Path aliases**: \`~/\` alias detected for imports\n"
        fi

        result+="\n"
    fi

    # Go imports
    local go_files=$(find "$CODEBASE_PATH" -type f -name "*.go" 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -20)
    if [[ -n "$go_files" ]]; then
        result+="### Go Imports\n\n"

        # Check for grouped imports
        if grep -q 'import (' $go_files 2>/dev/null; then
            result+="- **Style**: Grouped import blocks used\n"
        fi

        result+="\n"
    fi

    echo -e "$result"
}

analyze_error_handling() {
    log_info "Analyzing error handling patterns..." >&2

    local result=""

    # Python error handling
    local py_files=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$py_files" ]]; then
        local try_count=$(grep -r "try:" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local except_count=$(grep -r "except " $py_files 2>/dev/null | wc -l | tr -d ' ')
        local raise_count=$(grep -r "raise " $py_files 2>/dev/null | wc -l | tr -d ' ')
        local bare_except=$(grep -r "except:" $py_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $try_count -gt 0 ]]; then
            result+="### Python\n\n"
            result+="| Pattern | Count |\n"
            result+="|---------|-------|\n"
            result+="| try/except blocks | $try_count |\n"
            result+="| Custom raises | $raise_count |\n"
            [[ $bare_except -gt 0 ]] && result+="| Bare except (avoid) | $bare_except |\n"

            # Extract common exception types
            local exception_types=$(grep -oh "except [A-Z][a-zA-Z]*" $py_files 2>/dev/null | sort | uniq -c | sort -rn | head -5)
            if [[ -n "$exception_types" ]]; then
                result+="\n**Common exception types**:\n\`\`\`\n$exception_types\n\`\`\`\n"
            fi
            result+="\n"
        fi
    fi

    # JavaScript/TypeScript error handling
    local js_files=$(find "$CODEBASE_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$js_files" ]]; then
        local try_catch=$(grep -r "try {" $js_files 2>/dev/null | wc -l | tr -d ' ')
        local catch_count=$(grep -r "catch" $js_files 2>/dev/null | wc -l | tr -d ' ')
        local throw_count=$(grep -r "throw " $js_files 2>/dev/null | wc -l | tr -d ' ')
        local promise_catch=$(grep -r "\.catch(" $js_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $try_catch -gt 0 || $promise_catch -gt 0 ]]; then
            result+="### JavaScript/TypeScript\n\n"
            result+="| Pattern | Count |\n"
            result+="|---------|-------|\n"
            [[ $try_catch -gt 0 ]] && result+="| try/catch blocks | $try_catch |\n"
            [[ $promise_catch -gt 0 ]] && result+="| Promise .catch() | $promise_catch |\n"
            [[ $throw_count -gt 0 ]] && result+="| throw statements | $throw_count |\n"
            result+="\n"
        fi
    fi

    # Go error handling
    local go_files=$(find "$CODEBASE_PATH" -type f -name "*.go" 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$go_files" ]]; then
        local err_check=$(grep -r "if err != nil" $go_files 2>/dev/null | wc -l | tr -d ' ')
        local error_return=$(grep -r "return.*err" $go_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $err_check -gt 0 ]]; then
            result+="### Go\n\n"
            result+="| Pattern | Count |\n"
            result+="|---------|-------|\n"
            result+="| \`if err != nil\` checks | $err_check |\n"
            result+="| Error returns | $error_return |\n"
            result+="\n"
        fi
    fi

    echo -e "$result"
}

analyze_logging() {
    log_info "Analyzing logging patterns..." >&2

    local result=""

    # Python logging
    local py_files=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$py_files" ]]; then
        local logging_import=$(grep -r "import logging" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local logger_get=$(grep -r "getLogger" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local print_debug=$(grep -r "print(" $py_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $logging_import -gt 0 || $print_debug -gt 0 ]]; then
            result+="### Python\n\n"

            if [[ $logging_import -gt 0 ]]; then
                result+="- **Logging framework**: Standard \`logging\` module ($logging_import imports)\n"
                result+="- **Logger initialization**: \`logging.getLogger(__name__)\` pattern ($logger_get occurrences)\n"
            fi

            if [[ $print_debug -gt 5 ]]; then
                result+="\n> **Note**: $print_debug \`print()\` statements found. Consider using structured logging.\n"
            fi

            # Check log levels used
            local log_levels=$(grep -oh "logging\.\(debug\|info\|warning\|error\|critical\)" $py_files 2>/dev/null | sort | uniq -c | sort -rn)
            if [[ -n "$log_levels" ]]; then
                result+="\n**Log level usage**:\n\`\`\`\n$log_levels\n\`\`\`\n"
            fi
            result+="\n"
        fi
    fi

    # JavaScript/TypeScript logging
    local js_files=$(find "$CODEBASE_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$js_files" ]]; then
        local console_log=$(grep -r "console\.log" $js_files 2>/dev/null | wc -l | tr -d ' ')
        local console_error=$(grep -r "console\.error" $js_files 2>/dev/null | wc -l | tr -d ' ')
        local winston=$(grep -r "winston\|logger\." $js_files 2>/dev/null | wc -l | tr -d ' ')
        local pino=$(grep -r "pino\|fastify\.log" $js_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $console_log -gt 0 || $winston -gt 0 || $pino -gt 0 ]]; then
            result+="### JavaScript/TypeScript\n\n"

            if [[ $winston -gt 0 ]]; then
                result+="- **Logging framework**: Winston detected ($winston occurrences)\n"
            elif [[ $pino -gt 0 ]]; then
                result+="- **Logging framework**: Pino detected ($pino occurrences)\n"
            else
                result+="- **Logging**: Console methods used\n"
            fi

            result+="| Method | Count |\n"
            result+="|--------|-------|\n"
            [[ $console_log -gt 0 ]] && result+="| console.log | $console_log |\n"
            [[ $console_error -gt 0 ]] && result+="| console.error | $console_error |\n"

            result+="\n"
        fi
    fi

    # Go logging
    local go_files=$(find "$CODEBASE_PATH" -type f -name "*.go" 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$go_files" ]]; then
        local log_pkg=$(grep -r "\"log\"" $go_files 2>/dev/null | wc -l | tr -d ' ')
        local zap=$(grep -r "go.uber.org/zap" $go_files 2>/dev/null | wc -l | tr -d ' ')
        local logrus=$(grep -r "sirupsen/logrus" $go_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $log_pkg -gt 0 || $zap -gt 0 || $logrus -gt 0 ]]; then
            result+="### Go\n\n"

            if [[ $zap -gt 0 ]]; then
                result+="- **Logging framework**: Zap (structured logging)\n"
            elif [[ $logrus -gt 0 ]]; then
                result+="- **Logging framework**: Logrus\n"
            else
                result+="- **Logging**: Standard \`log\` package\n"
            fi
            result+="\n"
        fi
    fi

    echo -e "$result"
}

analyze_testing() {
    log_info "Analyzing testing patterns..." >&2

    local result=""

    # Detect test frameworks
    result+="### Test Frameworks Detected\n\n"

    # Python
    if [[ -f "$CODEBASE_PATH/pytest.ini" || -f "$CODEBASE_PATH/pyproject.toml" ]]; then
        if grep -q "pytest" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null || [[ -f "$CODEBASE_PATH/pytest.ini" ]]; then
            result+="- **Python**: pytest\n"
        fi
    fi
    if [[ -f "$CODEBASE_PATH/setup.cfg" ]] && grep -q "unittest" "$CODEBASE_PATH/setup.cfg" 2>/dev/null; then
        result+="- **Python**: unittest\n"
    fi

    # JavaScript/TypeScript
    if [[ -f "$CODEBASE_PATH/jest.config.js" || -f "$CODEBASE_PATH/jest.config.ts" ]]; then
        result+="- **JavaScript/TypeScript**: Jest\n"
    fi
    if [[ -f "$CODEBASE_PATH/vitest.config.ts" || -f "$CODEBASE_PATH/vitest.config.js" ]]; then
        result+="- **JavaScript/TypeScript**: Vitest\n"
    fi
    if [[ -f "$CODEBASE_PATH/cypress.json" || -d "$CODEBASE_PATH/cypress" ]]; then
        result+="- **E2E Testing**: Cypress\n"
    fi
    if [[ -f "$CODEBASE_PATH/playwright.config.ts" || -f "$CODEBASE_PATH/playwright.config.js" ]]; then
        result+="- **E2E Testing**: Playwright\n"
    fi

    # Go
    local go_test_files=$(find "$CODEBASE_PATH" -type f -name "*_test.go" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    if [[ $go_test_files -gt 0 ]]; then
        result+="- **Go**: Standard testing package ($go_test_files test files)\n"
    fi

    # Test patterns
    result+="\n### Test Patterns\n\n"

    # Count test files
    local test_files=$(find "$CODEBASE_PATH" -type f \( -name "test_*.py" -o -name "*_test.py" -o -name "*.test.js" -o -name "*.test.ts" -o -name "*.spec.js" -o -name "*.spec.ts" -o -name "*_test.go" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    result+="- **Total test files**: $test_files\n"

    # Check for test utilities
    if [[ -d "$CODEBASE_PATH/tests/fixtures" || -d "$CODEBASE_PATH/test/fixtures" ]]; then
        result+="- **Fixtures**: Dedicated fixtures directory found\n"
    fi
    if [[ -d "$CODEBASE_PATH/tests/mocks" || -d "$CODEBASE_PATH/__mocks__" ]]; then
        result+="- **Mocks**: Dedicated mocks directory found\n"
    fi

    # Coverage configuration
    if [[ -f "$CODEBASE_PATH/.coveragerc" || -f "$CODEBASE_PATH/coverage.py" ]]; then
        result+="- **Coverage**: Python coverage configured\n"
    fi
    if grep -q "coverage" "$CODEBASE_PATH/package.json" 2>/dev/null; then
        result+="- **Coverage**: JavaScript coverage configured\n"
    fi

    echo -e "$result"
}

analyze_documentation() {
    log_info "Analyzing documentation patterns..." >&2

    local result=""

    # Python docstrings
    local py_files=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -20)
    if [[ -n "$py_files" ]]; then
        local triple_quotes=$(grep -r '"""' $py_files 2>/dev/null | wc -l | tr -d ' ')
        local google_style=$(grep -r "Args:" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local numpy_style=$(grep -r "Parameters" $py_files 2>/dev/null | grep -v "import" | wc -l | tr -d ' ')
        local sphinx_style=$(grep -r ":param " $py_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $triple_quotes -gt 0 ]]; then
            result+="### Python Docstrings\n\n"

            if [[ $google_style -gt $numpy_style && $google_style -gt $sphinx_style ]]; then
                result+="- **Style**: Google-style docstrings detected\n"
                result+="- **Example pattern**:\n"
                result+="\`\`\`python\n"
                result+="def function(arg1, arg2):\n"
                result+="    \"\"\"Short description.\n\n"
                result+="    Args:\n"
                result+="        arg1: Description of arg1.\n"
                result+="        arg2: Description of arg2.\n\n"
                result+="    Returns:\n"
                result+="        Description of return value.\n"
                result+="    \"\"\"\n"
                result+="\`\`\`\n"
            elif [[ $numpy_style -gt $sphinx_style ]]; then
                result+="- **Style**: NumPy-style docstrings detected\n"
            elif [[ $sphinx_style -gt 0 ]]; then
                result+="- **Style**: Sphinx/reST-style docstrings detected\n"
            else
                result+="- **Docstrings**: Present but style unclear\n"
            fi
            result+="\n"
        fi
    fi

    # JSDoc
    local js_files=$(find "$CODEBASE_PATH" -type f \( -name "*.js" -o -name "*.ts" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -20)
    if [[ -n "$js_files" ]]; then
        local jsdoc=$(grep -r "@param\|@returns\|@type" $js_files 2>/dev/null | wc -l | tr -d ' ')
        local tsdoc=$(grep -r "@remarks\|@example" $js_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $jsdoc -gt 0 ]]; then
            result+="### JavaScript/TypeScript Documentation\n\n"
            result+="- **Style**: JSDoc comments detected ($jsdoc occurrences)\n"
            result+="- **Common tags**: @param, @returns, @type\n"
            result+="\n"
        fi
    fi

    # README and other docs
    result+="### Documentation Files\n\n"

    if [[ -f "$CODEBASE_PATH/README.md" ]]; then
        result+="- [x] README.md present\n"
    else
        result+="- [ ] README.md missing\n"
    fi

    if [[ -f "$CODEBASE_PATH/CONTRIBUTING.md" ]]; then
        result+="- [x] CONTRIBUTING.md present\n"
    fi

    if [[ -f "$CODEBASE_PATH/CHANGELOG.md" || -f "$CODEBASE_PATH/HISTORY.md" ]]; then
        result+="- [x] Changelog present\n"
    fi

    if [[ -d "$CODEBASE_PATH/docs" ]]; then
        local doc_count=$(find "$CODEBASE_PATH/docs" -type f \( -name "*.md" -o -name "*.rst" \) 2>/dev/null | wc -l | tr -d ' ')
        result+="- [x] docs/ directory ($doc_count documentation files)\n"
    fi

    echo -e "$result"
}

analyze_security() {
    log_info "Analyzing security patterns..." >&2

    local result=""

    # Check for security-related files
    result+="### Security Configuration\n\n"

    if [[ -f "$CODEBASE_PATH/.env.example" ]]; then
        result+="- [x] .env.example template present\n"
    fi

    if grep -q ".env" "$CODEBASE_PATH/.gitignore" 2>/dev/null; then
        result+="- [x] .env files in .gitignore\n"
    else
        result+="- [ ] **Warning**: .env may not be in .gitignore\n"
    fi

    # Check for secrets in code (basic check)
    local potential_secrets=$(grep -rn "password\s*=\s*['\"]" "$CODEBASE_PATH" 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -5)
    if [[ -n "$potential_secrets" ]]; then
        result+="\n> **Warning**: Potential hardcoded credentials detected. Review these locations.\n"
    fi

    # Security dependencies
    result+="\n### Security Tools Detected\n\n"

    if [[ -f "$CODEBASE_PATH/.pre-commit-config.yaml" ]]; then
        if grep -q "detect-secrets\|gitleaks\|trufflehog" "$CODEBASE_PATH/.pre-commit-config.yaml" 2>/dev/null; then
            result+="- [x] Secret scanning in pre-commit hooks\n"
        fi
        if grep -q "bandit\|safety" "$CODEBASE_PATH/.pre-commit-config.yaml" 2>/dev/null; then
            result+="- [x] Security linting configured\n"
        fi
    fi

    if [[ -f "$CODEBASE_PATH/.snyk" || -f "$CODEBASE_PATH/snyk.json" ]]; then
        result+="- [x] Snyk vulnerability scanning\n"
    fi

    if [[ -f "$CODEBASE_PATH/dependabot.yml" || -f "$CODEBASE_PATH/.github/dependabot.yml" ]]; then
        result+="- [x] Dependabot configured for dependency updates\n"
    fi

    echo -e "$result"
}

analyze_code_quality() {
    log_info "Analyzing code quality tools..." >&2

    local result=""

    result+="### Linting & Formatting\n\n"

    # Python
    if [[ -f "$CODEBASE_PATH/pyproject.toml" ]] || [[ -f "$CODEBASE_PATH/setup.cfg" ]]; then
        if grep -q "ruff" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null; then
            result+="- **Python linting**: Ruff\n"
        elif grep -q "flake8" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null || [[ -f "$CODEBASE_PATH/.flake8" ]]; then
            result+="- **Python linting**: Flake8\n"
        fi

        if grep -q "black" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null; then
            result+="- **Python formatting**: Black\n"
        fi

        if grep -q "isort" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null; then
            result+="- **Import sorting**: isort\n"
        fi

        if grep -q "mypy" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null || [[ -f "$CODEBASE_PATH/mypy.ini" ]]; then
            result+="- **Type checking**: mypy\n"
        fi
    fi

    # JavaScript/TypeScript
    if [[ -f "$CODEBASE_PATH/.eslintrc.js" || -f "$CODEBASE_PATH/.eslintrc.json" || -f "$CODEBASE_PATH/eslint.config.js" ]]; then
        result+="- **JavaScript linting**: ESLint\n"
    fi

    if [[ -f "$CODEBASE_PATH/.prettierrc" || -f "$CODEBASE_PATH/prettier.config.js" ]]; then
        result+="- **JavaScript formatting**: Prettier\n"
    fi

    if [[ -f "$CODEBASE_PATH/tsconfig.json" ]]; then
        result+="- **TypeScript**: Configured\n"

        if grep -q '"strict": true' "$CODEBASE_PATH/tsconfig.json" 2>/dev/null; then
            result+="  - Strict mode enabled\n"
        fi
    fi

    # Go
    if [[ -f "$CODEBASE_PATH/.golangci.yml" || -f "$CODEBASE_PATH/.golangci.yaml" ]]; then
        result+="- **Go linting**: golangci-lint\n"
    fi

    # Rust
    if [[ -f "$CODEBASE_PATH/rustfmt.toml" || -f "$CODEBASE_PATH/.rustfmt.toml" ]]; then
        result+="- **Rust formatting**: rustfmt\n"
    fi
    if [[ -f "$CODEBASE_PATH/clippy.toml" ]]; then
        result+="- **Rust linting**: Clippy\n"
    fi

    # Pre-commit
    if [[ -f "$CODEBASE_PATH/.pre-commit-config.yaml" ]]; then
        result+="\n### Pre-commit Hooks\n\n"
        result+="Pre-commit hooks configured. Key hooks:\n"
        result+="\`\`\`yaml\n"
        grep -A 1 "repo:" "$CODEBASE_PATH/.pre-commit-config.yaml" 2>/dev/null | head -20
        result+="\n\`\`\`\n"
    fi

    echo -e "$result"
}

# ============================================================================
# Generate CONVENTIONS.md
# ============================================================================

generate_conventions() {
    log_info "Generating CONVENTIONS.md..." >&2

    local project_name=$(basename "$CODEBASE_PATH")
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Detect languages
    local languages_raw=$(detect_languages)
    local primary_languages=""
    for lang in $languages_raw; do
        local name=$(echo "$lang" | cut -d: -f1)
        local count=$(echo "$lang" | cut -d: -f2)
        primary_languages+="- $name ($count files)\n"
    done

    # Start building the document
    cat << EOF
# $project_name Conventions

> Auto-generated by conventions-generator.sh on $timestamp
>
> To regenerate: \`./conventions-generator.sh "$CODEBASE_PATH"\`

## Overview

This document describes the coding conventions and patterns used in this codebase, extracted through automated analysis.

### Languages Detected

$(echo -e "$primary_languages")

---

## 1. File Organization

$(analyze_directory_structure)

---

## 2. File Naming

$(analyze_file_naming)

---

## 3. Import Patterns

$(analyze_imports)

---

## 4. Code Style

$(analyze_code_quality)

---

## 5. Error Handling

$(analyze_error_handling)

---

## 6. Logging

$(analyze_logging)

---

## 7. Testing

$(analyze_testing)

---

## 8. Documentation

$(analyze_documentation)

---

## 9. Security

$(analyze_security)

---

## 10. Performance Best Practices

### Detected Patterns

_This section requires manual review. Consider documenting:_

- [ ] Caching strategies used
- [ ] Database query optimization patterns
- [ ] Async/await patterns
- [ ] Memory management considerations
- [ ] Build optimization settings

---

## How to Use This Document

### In Spec Documents

Reference these conventions in your technical specifications:

\`\`\`markdown
## Implementation Notes

Follow the conventions documented in [CONVENTIONS.md](./CONVENTIONS.md):
- Error handling: See Section 5
- Logging: See Section 6
- Testing: See Section 7
\`\`\`

### In Code Reviews

Use this document as a checklist during code reviews to ensure consistency.

### Updating Conventions

When patterns change, regenerate this document and review the diff:

\`\`\`bash
./conventions-generator.sh "$CODEBASE_PATH" --output CONVENTIONS.md.new
diff CONVENTIONS.md CONVENTIONS.md.new
\`\`\`

Or update specific sections:

\`\`\`bash
./conventions-updater.sh "$CODEBASE_PATH" --section "Error Handling"
\`\`\`

---

## Appendix: Analysis Metadata

- **Generated**: $timestamp
- **Codebase Path**: $CODEBASE_PATH
- **Generator Version**: 1.0.0
- **Directories Skipped**: node_modules, __pycache__, .git, dist, build, venv, etc.

EOF
}

# ============================================================================
# Main
# ============================================================================

main() {
    echo ""
    echo "=========================================="
    echo "  CONVENTIONS.md Generator v1.0.0"
    echo "=========================================="
    echo ""

    parse_args "$@"

    log_info "Analyzing codebase: $CODEBASE_PATH"
    echo ""

    # Generate the document
    local content=$(generate_conventions)

    # Create output directory if needed
    local output_dir=$(dirname "$OUTPUT_PATH")
    if [[ ! -d "$output_dir" ]]; then
        mkdir -p "$output_dir"
    fi

    # Write the file
    echo -e "$content" > "$OUTPUT_PATH"

    echo ""
    log_success "CONVENTIONS.md generated successfully!"
    log_info "Output: $OUTPUT_PATH"
    echo ""

    # Show summary
    local line_count=$(wc -l < "$OUTPUT_PATH" | tr -d ' ')
    log_info "Document contains $line_count lines"
}

main "$@"
