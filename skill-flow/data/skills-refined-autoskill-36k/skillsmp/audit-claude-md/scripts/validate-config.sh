#!/usr/bin/env bash
set -euo pipefail

# validate-config.sh - Pure bash YAML config validator for audit-claude-md command
# Outputs structured JSON with validation results and normalized config
#
# Usage: validate-config.sh [--help] [--verbose] <config-file>
# Exit codes: 0 = valid (may have warnings), 1 = invalid or error

VERSION="1.0.0"
VERBOSE=false

# Default values
DEFAULT_CHECK_ONLY=false
DEFAULT_AUTO_SPLIT=false
DEFAULT_REFERENCE_URL="https://humanlayer.dev/blog/best-practices"
DEFAULT_MAX_FILE_SIZE=500
DEFAULT_CLAUDE_MD="CLAUDE.md"
DEFAULT_AGENTS_MD="AGENTS.md"

# Validation state
declare -a WARNINGS=()
ERROR_MSG=""
ERROR_LINE=0

# Parsed config storage
declare -A VALIDATION=()
declare -A BEST_PRACTICES=()
declare -A FILES=()

#------------------------------------------------------------------------------
# Utility Functions
#------------------------------------------------------------------------------

usage() {
    cat <<EOF
validate-config.sh v${VERSION}
Validate and normalize audit-claude-md command configuration files.

USAGE:
    validate-config.sh [OPTIONS] <config-file>

OPTIONS:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose debug output

ARGUMENTS:
    <config-file>   Path to .claude/audit-claude-md.yaml

EXIT CODES:
    0   Valid configuration (may have warnings)
    1   Invalid configuration or error

OUTPUT:
    JSON object with structure:
    {
      "valid": true|false,
      "error": null|{type, line, message},
      "warnings": [{field, message}],
      "config": {...normalized config...}
    }
EOF
}

debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo "[DEBUG] $*" >&2
    fi
}

add_warning() {
    local field="$1"
    local message="$2"
    WARNINGS+=("${field}|${message}")
    debug "Warning: $field - $message"
}

set_error() {
    local type="$1"
    local line="$2"
    local message="$3"
    ERROR_MSG="$message"
    ERROR_LINE="$line"
    debug "Error at line $line: $message"
}

#------------------------------------------------------------------------------
# JSON Generation (no jq dependency)
#------------------------------------------------------------------------------

json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\t'/\\t}"
    s="${s//$'\r'/\\r}"
    echo "$s"
}

json_string() {
    local s="$1"
    echo "\"$(json_escape "$s")\""
}

json_bool() {
    local val="$1"
    if [[ "$val" == "true" || "$val" == "yes" || "$val" == "1" ]]; then
        echo "true"
    else
        echo "false"
    fi
}

json_number() {
    local val="$1"
    if [[ "$val" =~ ^[0-9]+$ ]]; then
        echo "$val"
    else
        echo "500"  # Default
    fi
}

build_warnings_json() {
    local result="["
    local first=true

    for warning in "${WARNINGS[@]}"; do
        local field="${warning%%|*}"
        local message="${warning#*|}"

        if [[ "$first" != "true" ]]; then
            result+=","
        fi
        first=false

        result+="{\"field\":$(json_string "$field"),\"message\":$(json_string "$message")}"
    done

    result+="]"
    echo "$result"
}

build_validation_json() {
    local check_only="${VALIDATION[checkOnly]:-$DEFAULT_CHECK_ONLY}"
    local auto_split="${VALIDATION[autoSplit]:-$DEFAULT_AUTO_SPLIT}"
    echo "{\"checkOnly\":$(json_bool "$check_only"),\"autoSplit\":$(json_bool "$auto_split")}"
}

build_best_practices_json() {
    local ref_url="${BEST_PRACTICES[referenceUrl]:-$DEFAULT_REFERENCE_URL}"
    local max_size="${BEST_PRACTICES[maxFileSize]:-$DEFAULT_MAX_FILE_SIZE}"
    echo "{\"referenceUrl\":$(json_string "$ref_url"),\"maxFileSize\":$(json_number "$max_size")}"
}

build_files_json() {
    local claude_md="${FILES[claudeMd]:-$DEFAULT_CLAUDE_MD}"
    local agents_md="${FILES[agentsMd]:-$DEFAULT_AGENTS_MD}"
    echo "{\"claudeMd\":$(json_string "$claude_md"),\"agentsMd\":$(json_string "$agents_md")}"
}

build_config_json() {
    cat <<EOF
{"validation":$(build_validation_json),"bestPractices":$(build_best_practices_json),"files":$(build_files_json)}
EOF
}

output_success() {
    cat <<EOF
{"valid":true,"error":null,"warnings":$(build_warnings_json),"config":$(build_config_json)}
EOF
}

output_error() {
    local error_json="{\"type\":\"syntax\",\"line\":$ERROR_LINE,\"message\":$(json_string "$ERROR_MSG")}"
    cat <<EOF
{"valid":false,"error":$error_json,"warnings":[],"config":null}
EOF
}

output_missing() {
    # Config file doesn't exist - use defaults
    cat <<EOF
{"valid":true,"error":null,"warnings":[],"config":null}
EOF
}

#------------------------------------------------------------------------------
# YAML Parsing
#------------------------------------------------------------------------------

get_indent_level() {
    local line="$1"
    local stripped="${line#"${line%%[![:space:]]*}"}"
    local spaces=$((${#line} - ${#stripped}))
    echo $((spaces / 2))
}

trim() {
    local s="$1"
    s="${s#"${s%%[![:space:]]*}"}"
    s="${s%"${s##*[![:space:]]}"}"
    echo "$s"
}

is_comment_or_empty() {
    local line="$1"
    local trimmed
    trimmed=$(trim "$line")
    [[ -z "$trimmed" || "$trimmed" == \#* ]]
}

parse_key_value() {
    local line="$1"
    local trimmed
    trimmed=$(trim "$line")

    if [[ "$trimmed" != *:* ]]; then
        return 1
    fi

    local key="${trimmed%%:*}"
    local value="${trimmed#*:}"

    key=$(trim "$key")
    value=$(trim "$value")

    if [[ "$value" == \"*\" || "$value" == \'*\' ]]; then
        value="${value:1:${#value}-2}"
    fi

    echo "$key|$value"
}

is_boolean() {
    local val="$1"
    val=$(echo "$val" | tr '[:upper:]' '[:lower:]')
    [[ "$val" == "true" || "$val" == "false" || "$val" == "yes" || "$val" == "no" ]]
}

is_number() {
    local val="$1"
    [[ "$val" =~ ^[0-9]+$ ]]
}

normalize_boolean() {
    local val="$1"
    val=$(echo "$val" | tr '[:upper:]' '[:lower:]')
    if [[ "$val" == "true" || "$val" == "yes" ]]; then
        echo "true"
    else
        echo "false"
    fi
}

parse_yaml_file() {
    local file="$1"
    local line_num=0
    local current_section=""
    local has_content=false

    debug "Parsing file: $file"

    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))

        if is_comment_or_empty "$line"; then
            continue
        fi

        has_content=true
        local indent
        indent=$(get_indent_level "$line")
        debug "Line $line_num (indent=$indent): $line"

        local parsed
        if ! parsed=$(parse_key_value "$line"); then
            set_error "syntax" "$line_num" "Invalid syntax - expected 'key: value' format"
            return 1
        fi

        local key="${parsed%%|*}"
        local value="${parsed#*|}"

        debug "  Key: '$key', Value: '$value'"

        if [[ $indent -eq 0 ]]; then
            # Root level
            current_section="$key"

            case "$current_section" in
                validation|bestPractices|files)
                    debug "  Entering section: $current_section"
                    ;;
                *)
                    add_warning "$key" "Unknown root field '$key' will be ignored"
                    current_section=""
                    ;;
            esac

        elif [[ $indent -eq 1 ]]; then
            # Nested field
            case "$current_section" in
                validation)
                    case "$key" in
                        checkOnly)
                            if is_boolean "$value"; then
                                VALIDATION[checkOnly]=$(normalize_boolean "$value")
                                debug "  Set validation.checkOnly = ${VALIDATION[checkOnly]}"
                            else
                                add_warning "validation.checkOnly" "Expected boolean, got '$value' - using default"
                                VALIDATION[checkOnly]="$DEFAULT_CHECK_ONLY"
                            fi
                            ;;
                        autoSplit)
                            if is_boolean "$value"; then
                                VALIDATION[autoSplit]=$(normalize_boolean "$value")
                                debug "  Set validation.autoSplit = ${VALIDATION[autoSplit]}"
                            else
                                add_warning "validation.autoSplit" "Expected boolean, got '$value' - using default"
                                VALIDATION[autoSplit]="$DEFAULT_AUTO_SPLIT"
                            fi
                            ;;
                        *)
                            add_warning "validation.$key" "Unknown field 'validation.$key' - will be ignored"
                            ;;
                    esac
                    ;;

                bestPractices)
                    case "$key" in
                        referenceUrl)
                            BEST_PRACTICES[referenceUrl]="$value"
                            debug "  Set bestPractices.referenceUrl = $value"
                            ;;
                        maxFileSize)
                            if is_number "$value"; then
                                BEST_PRACTICES[maxFileSize]="$value"
                                debug "  Set bestPractices.maxFileSize = $value"
                            else
                                add_warning "bestPractices.maxFileSize" "Expected number, got '$value' - using default"
                                BEST_PRACTICES[maxFileSize]="$DEFAULT_MAX_FILE_SIZE"
                            fi
                            ;;
                        *)
                            add_warning "bestPractices.$key" "Unknown field 'bestPractices.$key' - will be ignored"
                            ;;
                    esac
                    ;;

                files)
                    case "$key" in
                        claudeMd)
                            FILES[claudeMd]="$value"
                            debug "  Set files.claudeMd = $value"
                            ;;
                        agentsMd)
                            FILES[agentsMd]="$value"
                            debug "  Set files.agentsMd = $value"
                            ;;
                        *)
                            add_warning "files.$key" "Unknown field 'files.$key' - will be ignored"
                            ;;
                    esac
                    ;;

                *)
                    debug "  Ignoring field in unknown section"
                    ;;
            esac
        fi

    done < "$file"

    if [[ "$has_content" != "true" ]]; then
        debug "File is empty or contains only comments"
        return 2
    fi

    return 0
}

apply_defaults() {
    debug "Applying defaults..."

    if [[ -z "${VALIDATION[checkOnly]:-}" ]]; then
        VALIDATION[checkOnly]="$DEFAULT_CHECK_ONLY"
        debug "  Default validation.checkOnly = $DEFAULT_CHECK_ONLY"
    fi

    if [[ -z "${VALIDATION[autoSplit]:-}" ]]; then
        VALIDATION[autoSplit]="$DEFAULT_AUTO_SPLIT"
        debug "  Default validation.autoSplit = $DEFAULT_AUTO_SPLIT"
    fi

    if [[ -z "${BEST_PRACTICES[referenceUrl]:-}" ]]; then
        BEST_PRACTICES[referenceUrl]="$DEFAULT_REFERENCE_URL"
        debug "  Default bestPractices.referenceUrl = $DEFAULT_REFERENCE_URL"
    fi

    if [[ -z "${BEST_PRACTICES[maxFileSize]:-}" ]]; then
        BEST_PRACTICES[maxFileSize]="$DEFAULT_MAX_FILE_SIZE"
        debug "  Default bestPractices.maxFileSize = $DEFAULT_MAX_FILE_SIZE"
    fi

    if [[ -z "${FILES[claudeMd]:-}" ]]; then
        FILES[claudeMd]="$DEFAULT_CLAUDE_MD"
        debug "  Default files.claudeMd = $DEFAULT_CLAUDE_MD"
    fi

    if [[ -z "${FILES[agentsMd]:-}" ]]; then
        FILES[agentsMd]="$DEFAULT_AGENTS_MD"
        debug "  Default files.agentsMd = $DEFAULT_AGENTS_MD"
    fi
}

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------

main() {
    local config_file=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -*)
                echo "Unknown option: $1" >&2
                usage >&2
                exit 1
                ;;
            *)
                config_file="$1"
                shift
                ;;
        esac
    done

    if [[ -z "$config_file" ]]; then
        echo "Error: Config file path required" >&2
        usage >&2
        exit 1
    fi

    debug "Config file: $config_file"

    if [[ ! -f "$config_file" ]]; then
        debug "Config file does not exist - outputting null config"
        output_missing
        exit 0
    fi

    if [[ ! -r "$config_file" ]]; then
        set_error "io" "0" "Cannot read config file: $config_file"
        output_error
        exit 1
    fi

    local parse_result
    set +e
    parse_yaml_file "$config_file"
    parse_result=$?
    set -e

    if [[ $parse_result -eq 1 ]]; then
        output_error
        exit 1
    elif [[ $parse_result -eq 2 ]]; then
        debug "Empty config file - outputting null config"
        output_missing
        exit 0
    fi

    apply_defaults
    output_success
    exit 0
}

main "$@"
