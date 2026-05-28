#!/bin/bash
#
# conventions-updater.sh
# Updates specific sections of an existing CONVENTIONS.md while preserving manual edits
#
# Usage: ./conventions-updater.sh <codebase-path> --section "Section Name" [options]
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
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default values
VERBOSE=false
DRY_RUN=false
CODEBASE_PATH=""
CONVENTIONS_PATH=""
SECTION=""
AUTO_APPLY=false

# Section markers
SECTION_START_MARKER="<!-- AUTO-GENERATED:START -->"
SECTION_END_MARKER="<!-- AUTO-GENERATED:END -->"

# Directories to skip (escaped for grep -E, same as generator)
SKIP_DIRS="node_modules|__pycache__|\.git|\.svn|\.hg|dist|build|\.next|\.nuxt|coverage|\.pytest_cache|\.mypy_cache|\.tox|\.eggs|egg-info|venv|\.venv|env|\.env|vendor|Pods|\.gradle|target|bin|obj|out|\.idea|\.vscode"

# Valid section names
VALID_SECTIONS=(
    "File Organization"
    "File Naming"
    "Import Patterns"
    "Code Style"
    "Error Handling"
    "Logging"
    "Testing"
    "Documentation"
    "Security"
    "All"
)

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
        echo -e "${CYAN}[DEBUG]${NC} $1"
    fi
}

show_usage() {
    cat << EOF
Usage: $(basename "$0") <codebase-path> --section "Section Name" [options]

Updates specific sections of an existing CONVENTIONS.md while preserving manual edits.

Arguments:
  <codebase-path>    Path to the codebase to analyze

Required Options:
  --section, -s      Section to update (use "All" to update all sections)

Optional:
  --conventions, -c  Path to CONVENTIONS.md (default: <codebase-path>/CONVENTIONS.md)
  --dry-run, -d      Show diff without applying changes
  --apply, -y        Apply changes without prompting
  --verbose, -v      Enable verbose output
  --list, -l         List available sections
  --help, -h         Show this help message

Valid Sections:
$(printf '  - %s\n' "${VALID_SECTIONS[@]}")

Examples:
  $(basename "$0") ./my-project --section "Error Handling"
  $(basename "$0") ./my-project -s "Testing" --dry-run
  $(basename "$0") ./my-project -s "All" -y
  $(basename "$0") --list
EOF
}

list_sections() {
    echo ""
    echo "Available sections for update:"
    echo ""
    for section in "${VALID_SECTIONS[@]}"; do
        echo "  - $section"
    done
    echo ""
    echo "Use: $(basename "$0") <codebase-path> --section \"Section Name\""
    echo ""
}

validate_section() {
    local input="$1"
    for valid in "${VALID_SECTIONS[@]}"; do
        if [[ "${input,,}" == "${valid,,}" ]]; then
            echo "$valid"
            return 0
        fi
    done
    return 1
}

# ============================================================================
# Parse Arguments
# ============================================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --section|-s)
                SECTION="$2"
                shift 2
                ;;
            --conventions|-c)
                CONVENTIONS_PATH="$2"
                shift 2
                ;;
            --dry-run|-d)
                DRY_RUN=true
                shift
                ;;
            --apply|-y)
                AUTO_APPLY=true
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --list|-l)
                list_sections
                exit 0
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

    # Validate section
    if [[ -z "$SECTION" ]]; then
        log_error "--section is required"
        show_usage
        exit 1
    fi

    local normalized_section
    if ! normalized_section=$(validate_section "$SECTION"); then
        log_error "Invalid section: $SECTION"
        echo ""
        list_sections
        exit 1
    fi
    SECTION="$normalized_section"

    # Set default conventions path
    if [[ -z "$CONVENTIONS_PATH" ]]; then
        CONVENTIONS_PATH="$CODEBASE_PATH/CONVENTIONS.md"
    fi

    # Check if conventions file exists
    if [[ ! -f "$CONVENTIONS_PATH" ]]; then
        log_error "CONVENTIONS.md not found at: $CONVENTIONS_PATH"
        log_info "Run conventions-generator.sh first to create the initial file."
        exit 1
    fi

    log_verbose "Codebase path: $CODEBASE_PATH"
    log_verbose "Conventions path: $CONVENTIONS_PATH"
    log_verbose "Section to update: $SECTION"
}

# ============================================================================
# Section Analysis Functions (copied from generator for consistency)
# ============================================================================

analyze_file_naming() {
    local result=""
    local snake_case=$(find "$CODEBASE_PATH" -type f \( -name "*_*.py" -o -name "*_*.js" -o -name "*_*.ts" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local kebab_case=$(find "$CODEBASE_PATH" -type f \( -name "*-*.js" -o -name "*-*.ts" -o -name "*-*.tsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local test_prefix=$(find "$CODEBASE_PATH" -type f -name "test_*" 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    local test_suffix=$(find "$CODEBASE_PATH" -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')

    result+="$SECTION_START_MARKER\n"
    result+="### Detected Patterns\n\n"
    result+="| Pattern | Count | Notes |\n"
    result+="|---------|-------|-------|\n"
    [[ $snake_case -gt 0 ]] && result+="| snake_case | $snake_case | Common in Python |\n"
    [[ $kebab_case -gt 0 ]] && result+="| kebab-case | $kebab_case | Common in web projects |\n"
    result+="\n### Test File Naming\n\n"
    if [[ $test_prefix -gt $test_suffix && $test_prefix -gt 0 ]]; then
        result+="- Primary pattern: \`test_*.py\` (prefix style, $test_prefix files)\n"
    elif [[ $test_suffix -gt 0 ]]; then
        result+="- Primary pattern: \`*.test.*\` or \`*.spec.*\` (suffix style, $test_suffix files)\n"
    else
        result+="- No consistent test file naming pattern detected\n"
    fi
    result+="\n$SECTION_END_MARKER"

    echo -e "$result"
}

analyze_directory_structure() {
    local result=""
    local dirs=$(find "$CODEBASE_PATH" -maxdepth 1 -type d ! -name ".*" ! -path "$CODEBASE_PATH" 2>/dev/null | sort)

    result+="$SECTION_START_MARKER\n"
    result+="\`\`\`\n"
    result+="$(basename "$CODEBASE_PATH")/\n"

    for dir in $dirs; do
        local dirname=$(basename "$dir")
        if [[ ! "$dirname" =~ ^(node_modules|__pycache__|\.git|dist|build|coverage|venv|\.venv)$ ]]; then
            result+="├── $dirname/\n"
            local subdirs=$(find "$dir" -maxdepth 1 -type d ! -path "$dir" 2>/dev/null | head -5 | sort)
            for subdir in $subdirs; do
                local subdirname=$(basename "$subdir")
                if [[ ! "$subdirname" =~ ^(node_modules|__pycache__|\.git)$ ]]; then
                    result+="│   ├── $subdirname/\n"
                fi
            done
        fi
    done
    result+="\`\`\`\n"
    result+="\n$SECTION_END_MARKER"

    echo -e "$result"
}

analyze_imports() {
    local result=""
    result+="$SECTION_START_MARKER\n"

    # Python imports
    local py_files=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -20)
    if [[ -n "$py_files" ]]; then
        result+="### Python Imports\n\n"
        local absolute_imports=$(grep -h "^from [a-zA-Z]" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local relative_imports=$(grep -h "^from \." $py_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $absolute_imports -gt $relative_imports ]]; then
            result+="- **Style**: Absolute imports preferred ($absolute_imports absolute vs $relative_imports relative)\n"
        else
            result+="- **Style**: Relative imports common ($relative_imports relative vs $absolute_imports absolute)\n"
        fi
        result+="\n"
    fi

    # JavaScript/TypeScript imports
    local js_files=$(find "$CODEBASE_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.jsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | head -20)
    if [[ -n "$js_files" ]]; then
        result+="### JavaScript/TypeScript Imports\n\n"
        local es_imports=$(grep -h "^import " $js_files 2>/dev/null | wc -l | tr -d ' ')
        local cjs_requires=$(grep -h "require(" $js_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $es_imports -gt $cjs_requires ]]; then
            result+="- **Module style**: ES Modules (\`import/export\`) - $es_imports occurrences\n"
        elif [[ $cjs_requires -gt 0 ]]; then
            result+="- **Module style**: CommonJS (\`require/module.exports\`) - $cjs_requires occurrences\n"
        fi

        if grep -q "from '@/" $js_files 2>/dev/null; then
            result+="- **Path aliases**: \`@/\` alias detected for imports\n"
        fi
        result+="\n"
    fi

    result+="$SECTION_END_MARKER"
    echo -e "$result"
}

analyze_error_handling() {
    local result=""
    result+="$SECTION_START_MARKER\n"

    # Python
    local py_files=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$py_files" ]]; then
        local try_count=$(grep -r "try:" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local raise_count=$(grep -r "raise " $py_files 2>/dev/null | wc -l | tr -d ' ')
        local bare_except=$(grep -r "except:" $py_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $try_count -gt 0 ]]; then
            result+="### Python\n\n"
            result+="| Pattern | Count |\n"
            result+="|---------|-------|\n"
            result+="| try/except blocks | $try_count |\n"
            result+="| Custom raises | $raise_count |\n"
            [[ $bare_except -gt 0 ]] && result+="| Bare except (avoid) | $bare_except |\n"
            result+="\n"
        fi
    fi

    # JavaScript
    local js_files=$(find "$CODEBASE_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$js_files" ]]; then
        local try_catch=$(grep -r "try {" $js_files 2>/dev/null | wc -l | tr -d ' ')
        local promise_catch=$(grep -r "\.catch(" $js_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $try_catch -gt 0 || $promise_catch -gt 0 ]]; then
            result+="### JavaScript/TypeScript\n\n"
            result+="| Pattern | Count |\n"
            result+="|---------|-------|\n"
            [[ $try_catch -gt 0 ]] && result+="| try/catch blocks | $try_catch |\n"
            [[ $promise_catch -gt 0 ]] && result+="| Promise .catch() | $promise_catch |\n"
            result+="\n"
        fi
    fi

    result+="$SECTION_END_MARKER"
    echo -e "$result"
}

analyze_logging() {
    local result=""
    result+="$SECTION_START_MARKER\n"

    # Python
    local py_files=$(find "$CODEBASE_PATH" -type f -name "*.py" 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$py_files" ]]; then
        local logging_import=$(grep -r "import logging" $py_files 2>/dev/null | wc -l | tr -d ' ')
        local print_debug=$(grep -r "print(" $py_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $logging_import -gt 0 || $print_debug -gt 0 ]]; then
            result+="### Python\n\n"
            [[ $logging_import -gt 0 ]] && result+="- **Logging framework**: Standard \`logging\` module ($logging_import imports)\n"
            [[ $print_debug -gt 5 ]] && result+="\n> **Note**: $print_debug \`print()\` statements found. Consider using structured logging.\n"
            result+="\n"
        fi
    fi

    # JavaScript
    local js_files=$(find "$CODEBASE_PATH" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" \) 2>/dev/null | grep -Ev "$SKIP_DIRS")
    if [[ -n "$js_files" ]]; then
        local console_log=$(grep -r "console\.log" $js_files 2>/dev/null | wc -l | tr -d ' ')

        if [[ $console_log -gt 0 ]]; then
            result+="### JavaScript/TypeScript\n\n"
            result+="| Method | Count |\n"
            result+="|--------|-------|\n"
            result+="| console.log | $console_log |\n"
            result+="\n"
        fi
    fi

    result+="$SECTION_END_MARKER"
    echo -e "$result"
}

analyze_testing() {
    local result=""
    result+="$SECTION_START_MARKER\n"
    result+="### Test Frameworks Detected\n\n"

    # Detect frameworks
    if [[ -f "$CODEBASE_PATH/pytest.ini" ]] || grep -q "pytest" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null; then
        result+="- **Python**: pytest\n"
    fi
    if [[ -f "$CODEBASE_PATH/jest.config.js" || -f "$CODEBASE_PATH/jest.config.ts" ]]; then
        result+="- **JavaScript/TypeScript**: Jest\n"
    fi
    if [[ -f "$CODEBASE_PATH/vitest.config.ts" ]]; then
        result+="- **JavaScript/TypeScript**: Vitest\n"
    fi
    if [[ -d "$CODEBASE_PATH/cypress" ]]; then
        result+="- **E2E Testing**: Cypress\n"
    fi
    if [[ -f "$CODEBASE_PATH/playwright.config.ts" ]]; then
        result+="- **E2E Testing**: Playwright\n"
    fi

    local test_files=$(find "$CODEBASE_PATH" -type f \( -name "test_*.py" -o -name "*_test.py" -o -name "*.test.js" -o -name "*.test.ts" -o -name "*.spec.js" -o -name "*.spec.ts" \) 2>/dev/null | grep -Ev "$SKIP_DIRS" | wc -l | tr -d ' ')
    result+="\n### Test Patterns\n\n"
    result+="- **Total test files**: $test_files\n"

    result+="\n$SECTION_END_MARKER"
    echo -e "$result"
}

analyze_documentation() {
    local result=""
    result+="$SECTION_START_MARKER\n"
    result+="### Documentation Files\n\n"

    [[ -f "$CODEBASE_PATH/README.md" ]] && result+="- [x] README.md present\n" || result+="- [ ] README.md missing\n"
    [[ -f "$CODEBASE_PATH/CONTRIBUTING.md" ]] && result+="- [x] CONTRIBUTING.md present\n"
    [[ -f "$CODEBASE_PATH/CHANGELOG.md" ]] && result+="- [x] Changelog present\n"
    if [[ -d "$CODEBASE_PATH/docs" ]]; then
        local doc_count=$(find "$CODEBASE_PATH/docs" -type f \( -name "*.md" -o -name "*.rst" \) 2>/dev/null | wc -l | tr -d ' ')
        result+="- [x] docs/ directory ($doc_count documentation files)\n"
    fi

    result+="\n$SECTION_END_MARKER"
    echo -e "$result"
}

analyze_security() {
    local result=""
    result+="$SECTION_START_MARKER\n"
    result+="### Security Configuration\n\n"

    [[ -f "$CODEBASE_PATH/.env.example" ]] && result+="- [x] .env.example template present\n"
    grep -q ".env" "$CODEBASE_PATH/.gitignore" 2>/dev/null && result+="- [x] .env files in .gitignore\n" || result+="- [ ] **Warning**: .env may not be in .gitignore\n"

    result+="\n### Security Tools Detected\n\n"
    if [[ -f "$CODEBASE_PATH/.pre-commit-config.yaml" ]]; then
        grep -q "detect-secrets\|gitleaks" "$CODEBASE_PATH/.pre-commit-config.yaml" 2>/dev/null && result+="- [x] Secret scanning in pre-commit hooks\n"
    fi
    [[ -f "$CODEBASE_PATH/.github/dependabot.yml" ]] && result+="- [x] Dependabot configured\n"

    result+="\n$SECTION_END_MARKER"
    echo -e "$result"
}

analyze_code_style() {
    local result=""
    result+="$SECTION_START_MARKER\n"
    result+="### Linting & Formatting\n\n"

    # Python
    if [[ -f "$CODEBASE_PATH/pyproject.toml" ]]; then
        grep -q "ruff" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null && result+="- **Python linting**: Ruff\n"
        grep -q "black" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null && result+="- **Python formatting**: Black\n"
        grep -q "mypy" "$CODEBASE_PATH/pyproject.toml" 2>/dev/null && result+="- **Type checking**: mypy\n"
    fi

    # JavaScript/TypeScript
    [[ -f "$CODEBASE_PATH/.eslintrc.js" || -f "$CODEBASE_PATH/.eslintrc.json" || -f "$CODEBASE_PATH/eslint.config.js" ]] && result+="- **JavaScript linting**: ESLint\n"
    [[ -f "$CODEBASE_PATH/.prettierrc" || -f "$CODEBASE_PATH/prettier.config.js" ]] && result+="- **JavaScript formatting**: Prettier\n"
    [[ -f "$CODEBASE_PATH/tsconfig.json" ]] && result+="- **TypeScript**: Configured\n"

    # Pre-commit
    [[ -f "$CODEBASE_PATH/.pre-commit-config.yaml" ]] && result+="\nPre-commit hooks configured.\n"

    result+="\n$SECTION_END_MARKER"
    echo -e "$result"
}

# ============================================================================
# Update Functions
# ============================================================================

get_section_content() {
    local section_name="$1"

    case "$section_name" in
        "File Organization")
            analyze_directory_structure
            ;;
        "File Naming")
            analyze_file_naming
            ;;
        "Import Patterns")
            analyze_imports
            ;;
        "Code Style")
            analyze_code_style
            ;;
        "Error Handling")
            analyze_error_handling
            ;;
        "Logging")
            analyze_logging
            ;;
        "Testing")
            analyze_testing
            ;;
        "Documentation")
            analyze_documentation
            ;;
        "Security")
            analyze_security
            ;;
        *)
            log_error "Unknown section: $section_name"
            return 1
            ;;
    esac
}

find_section_in_file() {
    local section_name="$1"
    local file="$2"

    # Find the line number where the section starts
    local section_pattern="^## [0-9]*\. $section_name"
    local line_num=$(grep -n "$section_pattern" "$file" 2>/dev/null | head -1 | cut -d: -f1)

    if [[ -z "$line_num" ]]; then
        # Try without number prefix
        section_pattern="^## $section_name"
        line_num=$(grep -n "$section_pattern" "$file" 2>/dev/null | head -1 | cut -d: -f1)
    fi

    echo "$line_num"
}

find_next_section() {
    local start_line="$1"
    local file="$2"

    # Find the next section header after start_line
    local next_section=$(tail -n +$((start_line + 1)) "$file" | grep -n "^## " | head -1 | cut -d: -f1)

    if [[ -n "$next_section" ]]; then
        echo $((start_line + next_section))
    else
        # Return end of file
        wc -l < "$file" | tr -d ' '
    fi
}

update_section() {
    local section_name="$1"
    local new_content="$2"
    local temp_file=$(mktemp)
    local backup_file="${CONVENTIONS_PATH}.backup"

    log_info "Updating section: $section_name"

    # Find section boundaries
    local section_start=$(find_section_in_file "$section_name" "$CONVENTIONS_PATH")

    if [[ -z "$section_start" ]]; then
        log_warning "Section '$section_name' not found in CONVENTIONS.md"
        log_info "Consider regenerating the file with conventions-generator.sh"
        return 1
    fi

    local section_end=$(find_next_section "$section_start" "$CONVENTIONS_PATH")

    log_verbose "Section starts at line: $section_start"
    log_verbose "Next section at line: $section_end"

    # Check for auto-generated markers within the section
    local auto_start=""
    local auto_end=""

    local section_content=$(sed -n "${section_start},${section_end}p" "$CONVENTIONS_PATH")

    if echo "$section_content" | grep -q "$SECTION_START_MARKER"; then
        # Find marker positions relative to section start
        local marker_start=$(echo "$section_content" | grep -n "$SECTION_START_MARKER" | head -1 | cut -d: -f1)
        local marker_end=$(echo "$section_content" | grep -n "$SECTION_END_MARKER" | head -1 | cut -d: -f1)

        if [[ -n "$marker_start" && -n "$marker_end" ]]; then
            auto_start=$((section_start + marker_start - 1))
            auto_end=$((section_start + marker_end - 1))
            log_verbose "Found auto-generated block: lines $auto_start to $auto_end"
        fi
    fi

    # Build the updated file
    if [[ -n "$auto_start" && -n "$auto_end" ]]; then
        # Replace only the auto-generated portion
        head -n $((auto_start - 1)) "$CONVENTIONS_PATH" > "$temp_file"
        echo -e "$new_content" >> "$temp_file"
        tail -n +$((auto_end + 1)) "$CONVENTIONS_PATH" >> "$temp_file"
    else
        # No markers found - append after section header
        head -n "$section_start" "$CONVENTIONS_PATH" > "$temp_file"
        echo "" >> "$temp_file"
        echo -e "$new_content" >> "$temp_file"
        echo "" >> "$temp_file"

        # Find content between section header and next section
        local content_start=$((section_start + 1))
        local content_lines=$((section_end - section_start - 1))

        if [[ $content_lines -gt 0 ]]; then
            # Keep any non-auto-generated content
            local existing=$(sed -n "${content_start},$((section_end - 1))p" "$CONVENTIONS_PATH" | grep -v "^$SECTION_START_MARKER\|^$SECTION_END_MARKER")
            if [[ -n "$existing" ]]; then
                echo "" >> "$temp_file"
                echo "<!-- Manual additions below -->" >> "$temp_file"
                echo "$existing" >> "$temp_file"
            fi
        fi

        tail -n +$section_end "$CONVENTIONS_PATH" >> "$temp_file"
    fi

    # Show diff
    echo ""
    echo "=========================================="
    echo "  Changes for: $section_name"
    echo "=========================================="
    echo ""

    if command -v diff &> /dev/null; then
        diff --color=auto -u "$CONVENTIONS_PATH" "$temp_file" || true
    else
        diff -u "$CONVENTIONS_PATH" "$temp_file" || true
    fi

    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "Dry run - no changes applied"
        rm -f "$temp_file"
        return 0
    fi

    # Apply changes
    if [[ "$AUTO_APPLY" == "true" ]]; then
        cp "$CONVENTIONS_PATH" "$backup_file"
        mv "$temp_file" "$CONVENTIONS_PATH"
        log_success "Changes applied. Backup saved to: $backup_file"
    else
        echo -n "Apply these changes? [y/N]: "
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            cp "$CONVENTIONS_PATH" "$backup_file"
            mv "$temp_file" "$CONVENTIONS_PATH"
            log_success "Changes applied. Backup saved to: $backup_file"
        else
            log_info "Changes discarded"
            rm -f "$temp_file"
        fi
    fi
}

update_all_sections() {
    log_info "Updating all sections..."
    echo ""

    local sections_to_update=(
        "File Organization"
        "File Naming"
        "Import Patterns"
        "Code Style"
        "Error Handling"
        "Logging"
        "Testing"
        "Documentation"
        "Security"
    )

    for section in "${sections_to_update[@]}"; do
        log_info "Analyzing: $section"
        local content=$(get_section_content "$section")
        update_section "$section" "$content"
        echo ""
    done
}

# ============================================================================
# Main
# ============================================================================

main() {
    echo ""
    echo "=========================================="
    echo "  CONVENTIONS.md Updater v1.0.0"
    echo "=========================================="
    echo ""

    parse_args "$@"

    log_info "Codebase: $CODEBASE_PATH"
    log_info "Conventions file: $CONVENTIONS_PATH"
    log_info "Section: $SECTION"
    echo ""

    if [[ "$SECTION" == "All" ]]; then
        update_all_sections
    else
        local content=$(get_section_content "$SECTION")
        update_section "$SECTION" "$content"
    fi

    echo ""
    log_success "Update complete!"
}

main "$@"
