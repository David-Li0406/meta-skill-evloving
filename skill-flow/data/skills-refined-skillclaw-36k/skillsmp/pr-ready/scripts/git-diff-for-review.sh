#!/usr/bin/env bash
#
# git-diff-for-review.sh
# 
# Generates a clean, AI-parseable diff between staged changes and a target branch.
# Designed for cross-platform compatibility (Linux, macOS, Windows/Git Bash).
#
# Usage: ./git-diff-for-review.sh [target-branch] [output-file]
#
# Examples:
#   ./git-diff-for-review.sh              # Compare staged changes vs HEAD
#   ./git-diff-for-review.sh dev          # Compare staged changes vs dev branch
#   ./git-diff-for-review.sh main review.diff
#

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================

readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_VERSION="1.0.0"
readonly DEFAULT_OUTPUT_FILE="diff-for-review.md"
readonly CONTEXT_LINES=5

# =============================================================================
# Color Support (disabled on non-interactive or Windows without proper terminal)
# =============================================================================

setup_colors() {
    if [[ -t 1 ]] && [[ -z "${NO_COLOR:-}" ]] && [[ "${TERM:-}" != "dumb" ]]; then
        RED='\033[0;31m'
        GREEN='\033[0;32m'
        YELLOW='\033[0;33m'
        BLUE='\033[0;34m'
        BOLD='\033[1m'
        RESET='\033[0m'
    else
        RED=''
        GREEN=''
        YELLOW=''
        BLUE=''
        BOLD=''
        RESET=''
    fi
}

# =============================================================================
# Logging Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${RESET} $*" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${RESET} $*" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARNING]${RESET} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${RESET} $*" >&2
}

# =============================================================================
# Helper Functions
# =============================================================================

print_usage() {
    cat << EOF
${BOLD}${SCRIPT_NAME}${RESET} v${SCRIPT_VERSION}

Generate a clean diff between staged changes and a target branch for AI code review.

${BOLD}USAGE:${RESET}
    $SCRIPT_NAME [target-branch] [output-file]

${BOLD}ARGUMENTS:${RESET}
    target-branch    The branch to compare against (default: HEAD)
    output-file      Optional. Output filename (default: ${DEFAULT_OUTPUT_FILE})

${BOLD}OPTIONS:${RESET}
    -h, --help       Show this help message
    -v, --version    Show version information
    --stdout         Output diff to stdout instead of saving to a file
    --unstaged       Include unstaged changes (staged + unstaged vs target branch)
    --all            Include all changes (staged + unstaged + untracked vs target branch)

${BOLD}EXAMPLES:${RESET}
    $SCRIPT_NAME                     # Compare staged changes vs HEAD
    $SCRIPT_NAME dev                 # Compare staged changes vs dev branch
    $SCRIPT_NAME main my-review.md   # Custom output file
    $SCRIPT_NAME feature/login --unstaged
    $SCRIPT_NAME main --stdout       # Output to stdout instead of file

${BOLD}OUTPUT FORMAT:${RESET}
    The script generates a Markdown file optimized for AI parsing, containing:
    - Summary of changes (files modified, added, deleted)
    - Individual file diffs with syntax highlighting hints
    - Clean, minimal diff format similar to GitHub PR reviews

EOF
}

print_version() {
    echo "$SCRIPT_NAME version $SCRIPT_VERSION"
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Normalize path for cross-platform compatibility
normalize_path() {
    local path="$1"
    # Convert Windows-style paths if running in Git Bash
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "$path" | sed 's|\\|/|g'
    else
        echo "$path"
    fi
}

# Get the file extension for syntax highlighting hints
get_file_extension() {
    local filename="$1"
    echo "${filename##*.}" | tr '[:upper:]' '[:lower:]'
}

# Map file extension to language for markdown code blocks
get_language_hint() {
    local ext="$1"
    case "$ext" in
        py) echo "python" ;;
        js) echo "javascript" ;;
        ts) echo "typescript" ;;
        jsx) echo "jsx" ;;
        tsx) echo "tsx" ;;
        rb) echo "ruby" ;;
        go) echo "go" ;;
        rs) echo "rust" ;;
        java) echo "java" ;;
        kt) echo "kotlin" ;;
        swift) echo "swift" ;;
        c|h) echo "c" ;;
        cpp|cc|cxx|hpp) echo "cpp" ;;
        cs) echo "csharp" ;;
        php) echo "php" ;;
        sh|bash) echo "bash" ;;
        sql) echo "sql" ;;
        html|htm) echo "html" ;;
        css) echo "css" ;;
        scss|sass) echo "scss" ;;
        json) echo "json" ;;
        yaml|yml) echo "yaml" ;;
        xml) echo "xml" ;;
        md) echo "markdown" ;;
        dockerfile) echo "dockerfile" ;;
        tf) echo "terraform" ;;
        vue) echo "vue" ;;
        svelte) echo "svelte" ;;
        *) echo "diff" ;;
    esac
}

# =============================================================================
# Validation Functions
# =============================================================================

check_git_installed() {
    if ! command_exists git; then
        log_error "Git is not installed or not in PATH."
        exit 1
    fi
}

check_inside_git_repo() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        log_error "Not inside a Git repository."
        log_info "Please run this script from within a Git project directory."
        exit 1
    fi
}

check_branch_exists() {
    local branch="$1"
    
    # Check local branches
    if git show-ref --verify --quiet "refs/heads/$branch" 2>/dev/null; then
        return 0
    fi
    
    # Check remote branches
    if git show-ref --verify --quiet "refs/remotes/origin/$branch" 2>/dev/null; then
        log_info "Branch '$branch' found as remote branch 'origin/$branch'"
        return 0
    fi
    
    # Check if it's a valid ref (could be a tag or commit hash)
    if git rev-parse --verify "$branch" >/dev/null 2>&1; then
        return 0
    fi
    
    return 1
}

check_staged_changes() {
    if git diff --cached --quiet 2>/dev/null; then
        return 1  # No staged changes
    fi
    return 0  # Has staged changes
}

get_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null
}

# =============================================================================
# Diff Generation Functions
# =============================================================================

generate_diff_header() {
    local target_branch="$1"
    local current_branch
    local repo_name
    local timestamp
    
    current_branch=$(git branch --show-current 2>/dev/null || echo "HEAD")
    repo_name=$(basename "$(get_repo_root)")
    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC" 2>/dev/null || date +"%Y-%m-%d %H:%M:%S")
    
    cat << EOF
# Code Review Diff

## Metadata
- **Repository:** ${repo_name}
- **Current Branch:** ${current_branch}
- **Target Branch:** ${target_branch}
- **Generated:** ${timestamp}
- **Comparison:** Staged changes vs ${target_branch}

---

EOF
}

generate_file_summary() {
    local target_branch="$1"
    local diff_stat
    local files_changed
    local insertions
    local deletions
    
    # Get diff statistics
    diff_stat=$(git diff --cached --stat "$target_branch" 2>/dev/null || echo "")
    
    if [[ -z "$diff_stat" ]]; then
        cat << EOF
## Summary
No changes detected between staged changes and ${target_branch}.

EOF
        return 1
    fi
    
    # Parse statistics from the last line
    local stat_line
    stat_line=$(echo "$diff_stat" | tail -1)
    
    files_changed=$(echo "$stat_line" | grep -oE '[0-9]+ file' | grep -oE '[0-9]+' || echo "0")
    insertions=$(echo "$stat_line" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
    deletions=$(echo "$stat_line" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")
    
    cat << EOF
## Summary

| Metric | Count |
|--------|-------|
| Files Changed | ${files_changed:-0} |
| Insertions (+) | ${insertions:-0} |
| Deletions (-) | ${deletions:-0} |

### Files Modified

EOF
    
    # List all changed files with their status
    git diff --cached --name-status "$target_branch" 2>/dev/null | while IFS=$'\t' read -r status filename; do
        local status_label
        case "$status" in
            A) status_label="Added" ;;
            M) status_label="Modified" ;;
            D) status_label="Deleted" ;;
            R*) status_label="Renamed" ;;
            C*) status_label="Copied" ;;
            *) status_label="Changed" ;;
        esac
        echo "- \`${filename}\` (${status_label})"
    done
    
    echo ""
    echo "---"
    echo ""
    
    return 0
}

generate_file_diffs() {
    local target_branch="$1"
    local context_lines="$2"
    
    echo "## File Changes"
    echo ""
    
    # Get list of changed files
    local changed_files
    changed_files=$(git diff --cached --name-only "$target_branch" 2>/dev/null)
    
    if [[ -z "$changed_files" ]]; then
        echo "No file changes to display."
        return
    fi
    
    # Process each file
    echo "$changed_files" | while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        
        local ext
        local lang
        local file_diff
        
        ext=$(get_file_extension "$file")
        lang=$(get_language_hint "$ext")
        
        echo "### \`${file}\`"
        echo ""
        
        # Get the diff for this specific file
        file_diff=$(git diff --cached -U"$context_lines" --no-color "$target_branch" -- "$file" 2>/dev/null || echo "")
        
        if [[ -z "$file_diff" ]]; then
            echo "_No changes in this file._"
            echo ""
            continue
        fi
        
        # Extract just the diff content (skip the header lines for cleaner output)
        # But keep enough context for understanding
        echo "\`\`\`diff"
        
        # Process the diff to make it cleaner
        echo "$file_diff" | awk '
            BEGIN { in_hunk = 0 }
            /^diff --git/ { next }
            /^index [0-9a-f]+/ { next }
            /^---/ { print; next }
            /^\+\+\+/ { print; next }
            /^@@/ { 
                print ""
                print $0
                in_hunk = 1
                next 
            }
            in_hunk { print }
        '
        
        echo "\`\`\`"
        echo ""
    done
}

generate_ai_instructions() {
    cat << EOF
---

## Review Instructions for AI

When reviewing this diff, please analyze:

1. **Code Quality**
   - Are there any bugs or logical errors?
   - Is the code following best practices?
   - Are there any security vulnerabilities?

2. **Style & Consistency**
   - Does the code follow consistent naming conventions?
   - Is the code properly formatted?
   - Are there any code style issues?

3. **Performance**
   - Are there any potential performance issues?
   - Could any operations be optimized?

4. **Documentation**
   - Are new functions/methods properly documented?
   - Are complex logic blocks commented?

5. **Testing Considerations**
   - What test cases should cover these changes?
   - Are edge cases handled?

Please provide specific, actionable feedback with line references where applicable.

EOF
}

# =============================================================================
# Main Function
# =============================================================================

main() {
    setup_colors
    
    local target_branch=""
    local output_file="$DEFAULT_OUTPUT_FILE"
    local include_unstaged=false
    local include_all=false
    local output_to_stdout=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                print_usage
                exit 0
                ;;
            -v|--version)
                print_version
                exit 0
                ;;
            --stdout)
                output_to_stdout=true
                shift
                ;;
            --unstaged)
                include_unstaged=true
                shift
                ;;
            --all)
                include_all=true
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
            *)
                if [[ -z "$target_branch" ]]; then
                    target_branch="$1"
                elif [[ "$output_file" == "$DEFAULT_OUTPUT_FILE" ]]; then
                    output_file="$1"
                else
                    log_error "Unexpected argument: $1"
                    print_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Set default target branch to HEAD if not specified
    if [[ -z "$target_branch" ]]; then
        target_branch="HEAD"
        log_info "No target branch specified, defaulting to HEAD"
    fi
    
    # Normalize output path
    output_file=$(normalize_path "$output_file")
    
    log_info "Starting diff generation..."
    
    # Run validation checks
    check_git_installed
    check_inside_git_repo
    
    if ! check_branch_exists "$target_branch"; then
        log_error "Branch '$target_branch' does not exist."
        log_info "Available local branches:"
        git branch --list | sed 's/^/  /'
        exit 1
    fi
    
    # Check for staged changes (warn but don't fail if none)
    if ! check_staged_changes; then
        if [[ "$include_unstaged" == true || "$include_all" == true ]]; then
            log_warn "No staged changes found. Comparing working tree to '$target_branch'."
        else
            log_warn "No staged changes found."
            log_info "Stage your changes with 'git add <files>' or use --unstaged flag."
            log_info "Proceeding to generate diff anyway (may be empty)..."
        fi
    fi
    
    # Adjust git diff command based on flags
    local diff_type="--cached"
    if [[ "$include_all" == true ]]; then
        # Create a temporary stash to include all changes
        log_info "Including all changes (staged + unstaged + untracked)..."
        diff_type=""
    elif [[ "$include_unstaged" == true ]]; then
        log_info "Including staged and unstaged changes..."
    # Generate diff output
        diff_type=""
    fi
    
    # Generate the diff file
    log_info "Generating diff against branch '$target_branch'..."
    
    local diff_output
    diff_output=$(
        generate_diff_header "$target_branch"
        
        if [[ "$diff_type" == "--cached" ]]; then
            generate_file_summary "$target_branch"
            generate_file_diffs "$target_branch" "$CONTEXT_LINES"
        else
            # For unstaged/all, we need to compare working tree
            # Temporarily modify functions to not use --cached
            git diff --stat "$target_branch" 2>/dev/null | head -n -1 | while IFS= read -r line; do
                echo "- $line"
            done
            echo ""
            echo "---"
            echo ""
            echo "## File Changes"
            echo ""
            
            git diff --name-only "$target_branch" 2>/dev/null | while IFS= read -r file; do
                [[ -z "$file" ]] && continue
                local ext=$(get_file_extension "$file")
                local lang=$(get_language_hint "$ext")
                
                echo "### \`${file}\`"
                echo ""
                echo "\`\`\`diff"
                git diff -U"$CONTEXT_LINES" --no-color "$target_branch" -- "$file" 2>/dev/null | awk '
                    BEGIN { in_hunk = 0 }
                    /^diff --git/ { next }
                    /^index [0-9a-f]+/ { next }
                    /^---/ { print; next }
                    /^\+\+\+/ { print; next }
                    /^@@/ { print ""; print $0; in_hunk = 1; next }
                    in_hunk { print }
                '
                echo "\`\`\`"
                echo ""
            done
        fi
        
        # generate_ai_instructions
    )
    
    # Output to stdout or file based on flag
    if [[ "$output_to_stdout" == true ]]; then
        echo "$diff_output"
        # log_success "Diff output generated successfully" >&2
    else
        echo "$diff_output" > "$output_file"
        
        # Verify output
        if [[ -f "$output_file" ]]; then
            local file_size
            file_size=$(wc -c < "$output_file" | tr -d ' ')
            
            if [[ "$file_size" -lt 100 ]]; then
                log_warn "Output file is very small. There may be no significant changes."
            fi
            
            log_success "Diff saved to: $output_file"
            log_info "File size: ${file_size} bytes"
            log_info "You can now pass this file to an AI for code review."
        else
            log_error "Failed to create output file."
            exit 1
        fi
    fi
}

# =============================================================================
# Script Entry Point
# =============================================================================

main "$@"
