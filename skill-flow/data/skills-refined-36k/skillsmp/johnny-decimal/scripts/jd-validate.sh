#!/usr/bin/env bash
# shellcheck shell=bash
#
# jd-validate: Validate filenames against Johnny Decimal conventions
#
# Usage:
#   jd-validate <filename>
#   jd-validate statement.pdf        # Warns about missing date
#   jd-validate 2024-12-27_doc.pdf   # OK
#   jd-validate file.pdf --porcelain # Machine-readable output (for agents)

set -euo pipefail

# --- Load shared library ---
# Resolve symlink to find actual script location
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/jd-lib.sh"

# Parse common args (--porcelain)
jd_parse_common_args "$@"
set -- "${JD_REMAINING_ARGS[@]}"

# --- Functions ---

validate_filename() {
    local filename="$1"
    local basename_file
    basename_file=$(basename "$filename")
    local warnings=()
    local errors=()

    # Check for spaces (should use underscores)
    if [[ "$basename_file" =~ \  ]]; then
        warnings+=("Contains spaces - prefer underscores")
    fi

    # Check for date prefix on common transient file types
    if [[ ! "$basename_file" =~ ^[0-9]{4}[-_]?[0-9]{2}[-_]?[0-9]{2} ]] && \
       [[ ! "$basename_file" =~ ^[0-9]{8} ]]; then
        # Check if it looks like a transient file that should have a date
        if [[ "$basename_file" =~ (statement|receipt|invoice|bill|check|paystub) ]]; then
            warnings+=("Transient document without date prefix - consider YYYY-MM-DD_name.ext")
        fi
    fi

    # Check for special characters that might cause issues
    if [[ "$basename_file" =~ [\'\"\`\$\&\|\<\>\;] ]]; then
        errors+=("Contains problematic special characters")
    fi

    # Output results
    if [[ "$JD_PORCELAIN" == "true" ]]; then
        # Machine-readable output
        if [[ ${#errors[@]} -gt 0 ]]; then
            echo "ERROR:$basename_file:${errors[*]}"
            return 1
        elif [[ ${#warnings[@]} -gt 0 ]]; then
            echo "WARN:$basename_file:${warnings[*]}"
            return 0
        else
            echo "OK:$basename_file"
            return 0
        fi
    else
        # Human-readable output
        if [[ ${#errors[@]} -gt 0 ]]; then
            echo "${JD_COLOR_ERROR}ERRORS${JD_COLOR_RESET} for '$basename_file':"
            for err in "${errors[@]}"; do
                echo "  - $err"
            done
        fi

        if [[ ${#warnings[@]} -gt 0 ]]; then
            echo "${JD_COLOR_WARN}WARNINGS${JD_COLOR_RESET} for '$basename_file':"
            for warn in "${warnings[@]}"; do
                echo "  - $warn"
            done
        fi

        if [[ ${#errors[@]} -eq 0 ]] && [[ ${#warnings[@]} -eq 0 ]]; then
            jd_success "OK: '$basename_file' follows conventions"
            return 0
        elif [[ ${#errors[@]} -gt 0 ]]; then
            return 1
        else
            return 0  # Warnings don't fail
        fi
    fi
}

# --- Main ---

if [[ $# -eq 0 ]]; then
    echo "Usage: jd-validate <filename> [filename...]" >&2
    exit 1
fi

exit_code=0
for file in "$@"; do
    if ! validate_filename "$file"; then
        exit_code=1
    fi
done

exit $exit_code
