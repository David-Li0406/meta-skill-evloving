#!/usr/bin/env bash
# shellcheck shell=bash
#
# jd-lib.sh: Shared library for Johnny Decimal scripts
#
# Source this file from other jd-* scripts:
#   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   source "${SCRIPT_DIR}/jd-lib.sh"
#
# Human vs Agent Mode:
#   Scripts auto-detect human mode (TTY + no --porcelain flag).
#   - Human mode: colors, short paths, interactive features (editor)
#   - Agent mode (--porcelain): full paths, no colors, never interactive
#
#   Call jd_parse_common_args "$@" early, then use JD_PORCELAIN to check mode.

# --- Configuration (exported for use by scripts that source this library) ---
export JD_ROOT="${XDG_DOCUMENTS_DIR:-${HOME}/Documents}"
export JDEX_PATH="${JD_ROOT}/00-09 System/00 System/00.00 JDex for System"

# Validate that JD_ROOT exists and is a directory
# Call this early in scripts after sourcing the library
jd_validate_root() {
    if [[ ! -d "$JD_ROOT" ]]; then
        echo "Error: JD_ROOT does not exist: ${JD_ROOT}" >&2
        echo "Set XDG_DOCUMENTS_DIR or create the directory." >&2
        return 1
    fi
}

# --- Human vs Agent Mode ---

# Set to "true" by jd_parse_common_args if --porcelain is passed
# Exported so subshells and child scripts can check the mode
export JD_PORCELAIN="false"

# Colors (set if TTY and not porcelain mode)
# Exported so subshells and scripts can use them
export JD_COLOR_ID=""
export JD_COLOR_NAME=""
export JD_COLOR_PATH=""
export JD_COLOR_SUCCESS=""
export JD_COLOR_ERROR=""
export JD_COLOR_WARN=""
export JD_COLOR_RESET=""

# Initialize colors if stdout is a TTY
jd_init_colors() {
    if [[ -t 1 ]] && [[ "$JD_PORCELAIN" != "true" ]]; then
        JD_COLOR_ID=$'\033[1;34m'      # Bold blue
        JD_COLOR_NAME=$'\033[0;37m'    # White
        JD_COLOR_PATH=$'\033[0;90m'    # Gray
        JD_COLOR_SUCCESS=$'\033[0;32m' # Green
        JD_COLOR_ERROR=$'\033[0;31m'   # Red
        JD_COLOR_WARN=$'\033[0;33m'    # Yellow
        JD_COLOR_RESET=$'\033[0m'
    fi
}

# Check if we're in human-interactive mode (TTY + not porcelain)
jd_is_interactive() {
    [[ -t 1 ]] && [[ -t 0 ]] && [[ "$JD_PORCELAIN" != "true" ]]
}

# Parse common arguments (--porcelain, --help)
# Usage: jd_parse_common_args "$@"; set -- "${JD_REMAINING_ARGS[@]}"
JD_REMAINING_ARGS=()
jd_parse_common_args() {
    JD_REMAINING_ARGS=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --porcelain)
                JD_PORCELAIN="true"
                shift
                ;;
            *)
                JD_REMAINING_ARGS+=("$1")
                shift
                ;;
        esac
    done
    # Initialize colors after parsing (so --porcelain disables them)
    jd_init_colors
}

# --- Output Helpers ---

# Format a JD path for display
# In human mode: just the basename (e.g., "21.10 Example Bank")
# In porcelain mode: full path
jd_format_path() {
    local path="$1"
    if [[ "$JD_PORCELAIN" == "true" ]]; then
        echo "$path"
    else
        local name
        name=$(basename "$path")
        # Color the ID portion
        if [[ "$name" =~ ^([0-9][0-9][-\.][0-9]*[0-9]?)\ (.*)$ ]]; then
            echo "${JD_COLOR_ID}${BASH_REMATCH[1]}${JD_COLOR_RESET} ${BASH_REMATCH[2]}"
        elif [[ "$name" =~ ^([0-9][0-9])\ (.*)$ ]]; then
            echo "${JD_COLOR_ID}${BASH_REMATCH[1]}${JD_COLOR_RESET} ${BASH_REMATCH[2]}"
        else
            echo "$name"
        fi
    fi
}

jd_success() {
    echo "${JD_COLOR_SUCCESS}$*${JD_COLOR_RESET}"
}

jd_error() {
    echo "${JD_COLOR_ERROR}Error: $*${JD_COLOR_RESET}" >&2
}

jd_warn() {
    echo "${JD_COLOR_WARN}Warning: $*${JD_COLOR_RESET}" >&2
}

# --- Path Finding Functions ---

# Find the area directory for a given category or ID
# Usage: find_area_dir 21 or find_area_dir 21.10
# Returns: Full path to area directory (e.g., /path/to/20-29 Finances)
find_area_dir() {
    local input="$1"
    local category="${input%%.*}"
    local area_prefix="${category:0:1}0"

    local area_dir
    area_dir=$(find "$JD_ROOT" -maxdepth 1 -type d -name "${area_prefix}-[0-9][0-9] *" 2>/dev/null | head -1)

    if [[ -z "$area_dir" ]]; then
        jd_error "No area found for '${input}'"
        return 1
    fi

    echo "$area_dir"
}

# Find the category directory for a given category or ID
# Usage: find_category_dir 21 or find_category_dir 21.10
# Returns: Full path to category directory (e.g., /path/to/21 Banks)
find_category_dir() {
    local input="$1"
    local category="${input%%.*}"

    local area_dir
    area_dir=$(find_area_dir "$input") || return 1

    local category_dir
    category_dir=$(find "$area_dir" -maxdepth 1 -type d -name "${category} *" 2>/dev/null | head -1)

    if [[ -z "$category_dir" ]]; then
        jd_error "No category found for '${input}'"
        return 1
    fi

    echo "$category_dir"
}

# Find the subcategory (ID) directory
# Usage: find_id_dir 21.10
# Returns: Full path to subcategory directory (e.g., /path/to/21.10 Example Bank)
find_id_dir() {
    local id="$1"

    if [[ ! "$id" =~ ^[0-9][0-9]\.[0-9]+$ ]]; then
        jd_error "Invalid ID format '${id}'. Expected XX.YY"
        return 1
    fi

    local category_dir
    category_dir=$(find_category_dir "$id") || return 1

    local subcat_dir
    subcat_dir=$(find "$category_dir" -maxdepth 1 -type d -name "${id} *" 2>/dev/null | head -1)

    if [[ -z "$subcat_dir" ]]; then
        jd_error "No subcategory found for '${id}'"
        return 1
    fi

    echo "$subcat_dir"
}

# Get the name portion of an ID's folder
# Usage: get_id_name 21.10
# Returns: Just the name (e.g., "Example Bank")
get_id_name() {
    local id="$1"

    local subcat_dir
    subcat_dir=$(find_id_dir "$id" 2>/dev/null) || return 1

    # Extract just the name part (after "XX.YY ")
    basename "$subcat_dir" | sed "s/^${id} //"
}

# Find the next available ID number in a category
# Usage: next_available_id 21
# Returns: Next ID (e.g., "21.15")
next_available_id() {
    local category="$1"

    local category_dir
    category_dir=$(find_category_dir "$category") || return 1

    # Find all existing subcategory numbers
    local max_num=9  # Start after system IDs (XX.00-XX.09)

    while IFS= read -r dir; do
        # Extract the number after the dot
        local dirname
        dirname=$(basename "$dir")
        if [[ "$dirname" =~ ^${category}\.([0-9]+) ]]; then
            local num="${BASH_REMATCH[1]}"
            # Remove leading zeros for comparison
            num=$((10#$num))
            if [[ $num -gt $max_num ]]; then
                max_num=$num
            fi
        fi
    done < <(find "$category_dir" -maxdepth 1 -type d -name "${category}.[0-9]* *" 2>/dev/null)

    local next_num=$((max_num + 1))
    echo "${category}.${next_num}"
}

# --- Interactive Selection Functions ---

# Generic interactive selection from a list
# Usage: jd_select_from_list "prompt" "${items[@]}"
# Returns: The selected item (exactly as provided)
# Note: Caller must verify interactive mode; this function uses /dev/tty directly
jd_select_from_list() {
    local prompt="$1"
    shift
    local -a items=("$@")

    if [[ ${#items[@]} -eq 0 ]]; then
        jd_error "No items to select from"
        return 1
    fi

    echo "$prompt" >&2
    PS3="Enter number (or Ctrl+C to cancel): "
    local choice
    # Force single-column display for cleaner alignment
    local saved_columns="${COLUMNS:-}"
    COLUMNS=1
    select choice in "${items[@]}"; do
        if [[ -n "$choice" ]]; then
            COLUMNS="$saved_columns"
            echo "$choice"
            return 0
        else
            echo "Invalid selection. Try again." >&2
        fi
    done < /dev/tty
    COLUMNS="$saved_columns"
}

# Browse hierarchically to select a JD ID
# Returns: ID (e.g., "21.10")
# Note: Caller must verify interactive mode; this function uses /dev/tty directly
# Note: No colors in select items - ANSI codes break regex extraction
jd_browse_to_id() {
    # Level 1: Select area
    local -a areas=()
    while IFS= read -r dir; do
        areas+=("$(basename "$dir")")
    done < <(find "$JD_ROOT" -maxdepth 1 -type d -name '[0-9][0-9]-[0-9][0-9] *' 2>/dev/null | sort)

    if [[ ${#areas[@]} -eq 0 ]]; then
        jd_error "No areas found in ${JD_ROOT}"
        return 1
    fi

    local area_choice
    area_choice=$(jd_select_from_list "Select an area:" "${areas[@]}") || return 1

    # Extract area prefix (first two digits)
    local area_prefix
    if [[ "$area_choice" =~ ^([0-9][0-9])- ]]; then
        area_prefix="${BASH_REMATCH[1]}"
    else
        jd_error "Could not parse area selection"
        return 1
    fi

    # Level 2: Select category
    local area_dir
    area_dir=$(find "$JD_ROOT" -maxdepth 1 -type d -name "${area_prefix}-[0-9][0-9] *" 2>/dev/null | head -1)

    local -a categories=()
    while IFS= read -r dir; do
        categories+=("$(basename "$dir")")
    done < <(find "$area_dir" -maxdepth 1 -type d -name '[0-9][0-9] *' 2>/dev/null | sort)

    if [[ ${#categories[@]} -eq 0 ]]; then
        jd_error "No categories found in area ${area_prefix}"
        return 1
    fi

    local cat_choice
    cat_choice=$(jd_select_from_list "Select a category:" "${categories[@]}") || return 1

    # Extract category number (first two digits)
    local category
    if [[ "$cat_choice" =~ ^([0-9][0-9]) ]]; then
        category="${BASH_REMATCH[1]}"
    else
        jd_error "Could not parse category selection"
        return 1
    fi

    # Level 3: Select ID
    local category_dir
    category_dir=$(find_category_dir "$category") || return 1

    local -a ids=()
    while IFS= read -r dir; do
        ids+=("$(basename "$dir")")
    done < <(find "$category_dir" -maxdepth 1 -type d -name "${category}.[0-9]* *" 2>/dev/null | sort)

    if [[ ${#ids[@]} -eq 0 ]]; then
        jd_error "No IDs found in category ${category}"
        return 1
    fi

    local id_choice
    id_choice=$(jd_select_from_list "Select an ID:" "${ids[@]}") || return 1

    # Extract the ID (XX.YY)
    if [[ "$id_choice" =~ ^([0-9][0-9]\.[0-9]+) ]]; then
        echo "${BASH_REMATCH[1]}"
        return 0
    fi

    jd_error "Could not parse ID selection"
    return 1
}

# --- Search Functions ---

# Search for JD directories matching a query
# Usage: jd_search "query"
# Outputs: Matching paths (relative to JD_ROOT), one per line, sorted
# Exit codes: 0 = matches found, 1 = no matches
#
# Query types (auto-detected):
#   "10-" or "10-19" → Area search (maxdepth 1)
#   "12" or "12 "    → Category search (maxdepth 2)
#   "12.3" or "12.34"→ ID search (maxdepth 3, validated)
#   "foo"            → String search (maxdepth 3, validated)
jd_search() {
    local query="$1"

    # Run find in a subshell to avoid changing caller's directory
    # All output is relative paths, cleaned up and sorted
    (
        cd "$JD_ROOT" || exit 1

        # Determine search type based on query format
        if [[ "$query" =~ ^[0-9]{2}- ]]; then
            # Area search (e.g., "10-" or "10-19")
            find . -maxdepth 1 -type d -iname "${query}*" -print 2>/dev/null

        elif [[ "$query" =~ ^[0-9]{2}\s*$ ]]; then
            # Category search (e.g., "12" or "12 ")
            local trimmed_query="${query%% }"
            find . -maxdepth 2 -type d -iname "${trimmed_query} *" -print 2>/dev/null

        elif [[ "$query" =~ ^[0-9]{2}\. ]]; then
            # ID search (e.g., "12.3" or "12.34")
            find . -maxdepth 3 -type d -iname "${query}*" \
                \( -name '[0-9][0-9]-*' -o -name '[0-9][0-9].*' -o -name '[0-9][0-9] *' \) \
                -print 2>/dev/null

        else
            # Fallback to string search (e.g., "alex")
            find . -maxdepth 3 -type d -iname "*${query}*" \
                \( -name '[0-9][0-9]-*' -o -name '[0-9][0-9].*' -o -name '[0-9][0-9] *' \) \
                -print 2>/dev/null
        fi
    ) | sed 's|^\./||' | sort | grep -v '^$'

    # Return based on whether we found anything
    # The pipeline's exit status is from grep, which fails if no matches
    return "${PIPESTATUS[0]}"
}
