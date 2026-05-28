#!/usr/bin/env bash
set -euo pipefail

# validate-config.sh - Pure bash YAML config validator for commit command
# Outputs structured JSON with validation results and normalized config
#
# Usage: validate-config.sh [--help] [--verbose] <config-file>
# Exit codes: 0 = valid (may have warnings), 1 = invalid or error

VERSION="1.0.0"
VERBOSE=false

# Default values
DEFAULT_GITMOJI_ENABLED=true
DEFAULT_HOOKS_RUN_BY_DEFAULT=true
DEFAULT_FORMAT_CO_AUTHOR=false

# Validation state
declare -a WARNINGS=()
ERROR_MSG=""
ERROR_LINE=0

# Parsed config storage
declare -A GITMOJI=()
declare -A HOOKS=()
declare -A FORMAT=()

# Custom gitmoji list (parallel arrays for emoji, code, description)
declare -a GITMOJI_CUSTOM_EMOJI=()
declare -a GITMOJI_CUSTOM_CODE=()
declare -a GITMOJI_CUSTOM_DESC=()

# Multiline value accumulator
MULTILINE_VALUE=""
MULTILINE_FIELD=""
MULTILINE_INDENT=0
IN_MULTILINE=false

#------------------------------------------------------------------------------
# Utility Functions
#------------------------------------------------------------------------------

usage() {
    cat <<EOF
validate-config.sh v${VERSION}
Validate and normalize commit command configuration files.

USAGE:
    validate-config.sh [OPTIONS] <config-file>

OPTIONS:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose debug output

ARGUMENTS:
    <config-file>   Path to .claude/commit.yaml

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
    s="${s//\\/\\\\}"     # Escape backslashes
    s="${s//\"/\\\"}"     # Escape quotes
    s="${s//$'\n'/\\n}"   # Escape newlines
    s="${s//$'\t'/\\t}"   # Escape tabs
    s="${s//$'\r'/\\r}"   # Escape carriage returns
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

build_gitmoji_json() {
    local enabled="${GITMOJI[enabled]:-$DEFAULT_GITMOJI_ENABLED}"
    local custom_json="[]"

    # Build custom gitmoji array if any exist
    if [[ ${#GITMOJI_CUSTOM_EMOJI[@]} -gt 0 ]]; then
        custom_json="["
        for i in "${!GITMOJI_CUSTOM_EMOJI[@]}"; do
            [[ $i -gt 0 ]] && custom_json+=","
            local emoji_str
            local code_str
            local desc_str
            emoji_str=$(json_string "${GITMOJI_CUSTOM_EMOJI[$i]}")
            code_str=$(json_string "${GITMOJI_CUSTOM_CODE[$i]}")
            desc_str=$(json_string "${GITMOJI_CUSTOM_DESC[$i]:-}")
            custom_json+="{\"emoji\":$emoji_str,\"code\":$code_str,\"description\":$desc_str}"
        done
        custom_json+="]"
    fi

    echo "{\"enabled\":$(json_bool "$enabled"),\"custom\":$custom_json}"
}

build_hooks_json() {
    local run_by_default="${HOOKS[runByDefault]:-$DEFAULT_HOOKS_RUN_BY_DEFAULT}"
    echo "{\"runByDefault\":$(json_bool "$run_by_default")}"
}

build_format_json() {
    local co_author="${FORMAT[coAuthor]:-$DEFAULT_FORMAT_CO_AUTHOR}"
    local msg_tpl="${FORMAT[messageTemplate]:-}"
    local body_tpl="${FORMAT[bodyTemplate]:-}"

    local msg_json="null"
    [[ -n "$msg_tpl" ]] && msg_json=$(json_string "$msg_tpl")

    local body_json="null"
    [[ -n "$body_tpl" ]] && body_json=$(json_string "$body_tpl")

    echo "{\"coAuthor\":$(json_bool "$co_author"),\"messageTemplate\":$msg_json,\"bodyTemplate\":$body_json}"
}

build_config_json() {
    cat <<EOF
{"gitmoji":$(build_gitmoji_json),"hooks":$(build_hooks_json),"format":$(build_format_json)}
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
# YAML Parsing (simplified for 2-level nesting)
#------------------------------------------------------------------------------

get_indent_level() {
    local line="$1"
    local stripped="${line#"${line%%[![:space:]]*}"}"
    local spaces=$((${#line} - ${#stripped}))
    echo $((spaces / 2))
}

trim() {
    local s="$1"
    # Remove leading whitespace
    s="${s#"${s%%[![:space:]]*}"}"
    # Remove trailing whitespace
    s="${s%"${s##*[![:space:]]}"}"
    echo "$s"
}

is_comment_or_empty() {
    local line="$1"
    local trimmed
    trimmed=$(trim "$line")

    [[ -z "$trimmed" || "$trimmed" == \#* ]]
}

is_list_item() {
    local line="$1"
    local trimmed
    trimmed=$(trim "$line")
    [[ "$trimmed" == -* ]]
}

is_multiline_start() {
    local value="$1"
    [[ "$value" == "|" || "$value" == ">" || "$value" == "|"* || "$value" == ">"* ]]
}

parse_list_item_field() {
    # Parse "- key: value" or "  key: value" within a list item
    local line="$1"
    local trimmed
    trimmed=$(trim "$line")

    # Remove leading "- " if present
    if [[ "$trimmed" == -\ * ]]; then
        trimmed="${trimmed:2}"
        trimmed=$(trim "$trimmed")
    fi

    # Check for colon
    if [[ "$trimmed" != *:* ]]; then
        return 1
    fi

    local key="${trimmed%%:*}"
    local value="${trimmed#*:}"
    key=$(trim "$key")
    value=$(trim "$value")

    # Remove surrounding quotes from value if present
    if [[ "$value" == \"*\" || "$value" == \'*\' ]]; then
        value="${value:1:${#value}-2}"
    fi

    echo "$key|$value"
}

parse_key_value() {
    local line="$1"
    local trimmed
    trimmed=$(trim "$line")

    # Check for colon
    if [[ "$trimmed" != *:* ]]; then
        return 1
    fi

    local key="${trimmed%%:*}"
    local value="${trimmed#*:}"

    key=$(trim "$key")
    value=$(trim "$value")

    # Remove surrounding quotes from value if present
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

    # List parsing state
    local in_list=false
    local list_field=""
    local current_list_item_idx=-1
    local current_list_emoji=""
    local current_list_code=""
    local current_list_desc=""

    # Multiline parsing state
    local in_multiline=false
    local multiline_field=""
    local multiline_value=""
    local multiline_base_indent=0

    debug "Parsing file: $file"

    while IFS= read -r line || [[ -n "$line" ]]; do
        ((line_num++))

        local indent
        indent=$(get_indent_level "$line")

        # Handle multiline continuation
        if [[ "$in_multiline" == "true" ]]; then
            if is_comment_or_empty "$line"; then
                # Empty lines in multiline are preserved
                if [[ -n "$multiline_value" ]]; then
                    multiline_value+=$'\n'
                fi
                continue
            fi

            # Check if still in multiline (indent > base)
            if [[ $indent -gt $multiline_base_indent ]]; then
                # Add line content (stripped of base indent)
                local content
                content=$(trim "$line")
                if [[ -n "$multiline_value" ]]; then
                    multiline_value+=$'\n'"$content"
                else
                    multiline_value="$content"
                fi
                continue
            else
                # End of multiline - save it
                FORMAT[$multiline_field]="$multiline_value"
                debug "  Set format.$multiline_field = (multiline, ${#multiline_value} chars)"
                in_multiline=false
                multiline_value=""
                # Fall through to process current line
            fi
        fi

        # Skip comments and empty lines
        if is_comment_or_empty "$line"; then
            continue
        fi

        has_content=true
        debug "Line $line_num (indent=$indent): $line"

        # Handle list items in gitmoji.custom
        if [[ "$in_list" == "true" && "$list_field" == "gitmoji.custom" ]]; then
            if is_list_item "$line" && [[ $indent -eq 2 ]]; then
                # Save previous list item if any
                if [[ $current_list_item_idx -ge 0 ]]; then
                    GITMOJI_CUSTOM_EMOJI+=("$current_list_emoji")
                    GITMOJI_CUSTOM_CODE+=("$current_list_code")
                    GITMOJI_CUSTOM_DESC+=("$current_list_desc")
                    debug "  Saved custom gitmoji: $current_list_emoji ($current_list_code)"
                fi

                # Start new list item
                ((current_list_item_idx++))
                current_list_emoji=""
                current_list_code=""
                current_list_desc=""

                # Parse first field from "- key: value"
                local parsed
                if parsed=$(parse_list_item_field "$line"); then
                    local key="${parsed%%|*}"
                    local value="${parsed#*|}"
                    case "$key" in
                        emoji) current_list_emoji="$value" ;;
                        code) current_list_code="$value" ;;
                        description) current_list_desc="$value" ;;
                        *) add_warning "gitmoji.custom[$current_list_item_idx].$key" "Unknown field" ;;
                    esac
                fi
                continue
            elif [[ $indent -eq 3 ]]; then
                # Continuation of list item properties
                local parsed
                if parsed=$(parse_key_value "$line"); then
                    local key="${parsed%%|*}"
                    local value="${parsed#*|}"
                    case "$key" in
                        emoji) current_list_emoji="$value" ;;
                        code) current_list_code="$value" ;;
                        description) current_list_desc="$value" ;;
                        *) add_warning "gitmoji.custom[$current_list_item_idx].$key" "Unknown field" ;;
                    esac
                fi
                continue
            else
                # End of list - save last item
                if [[ $current_list_item_idx -ge 0 && -n "$current_list_emoji" ]]; then
                    GITMOJI_CUSTOM_EMOJI+=("$current_list_emoji")
                    GITMOJI_CUSTOM_CODE+=("$current_list_code")
                    GITMOJI_CUSTOM_DESC+=("$current_list_desc")
                    debug "  Saved custom gitmoji: $current_list_emoji ($current_list_code)"
                fi
                in_list=false
                list_field=""
                current_list_item_idx=-1
                # Fall through to process current line
            fi
        fi

        # Parse key:value
        local parsed
        if ! parsed=$(parse_key_value "$line"); then
            set_error "syntax" "$line_num" "Invalid syntax - expected 'key: value' format"
            return 1
        fi

        local key="${parsed%%|*}"
        local value="${parsed#*|}"

        debug "  Key: '$key', Value: '$value'"

        # Handle based on indent level
        if [[ $indent -eq 0 ]]; then
            # Root level section
            current_section="$key"

            case "$current_section" in
                gitmoji|hooks|format)
                    debug "  Entering section: $current_section"
                    ;;
                *)
                    add_warning "$key" "Unknown root field '$key' will be ignored"
                    current_section=""
                    ;;
            esac

        elif [[ $indent -eq 1 ]]; then
            # First-level nested field
            case "$current_section" in
                gitmoji)
                    case "$key" in
                        enabled)
                            if is_boolean "$value"; then
                                GITMOJI[enabled]=$(normalize_boolean "$value")
                                debug "  Set gitmoji.enabled = ${GITMOJI[enabled]}"
                            else
                                add_warning "gitmoji.enabled" "Expected boolean for 'gitmoji.enabled', got '$value' - using default"
                                GITMOJI[enabled]="$DEFAULT_GITMOJI_ENABLED"
                            fi
                            ;;
                        custom)
                            # Start of custom gitmoji list
                            in_list=true
                            list_field="gitmoji.custom"
                            current_list_item_idx=-1
                            debug "  Entering gitmoji.custom list"
                            ;;
                        *)
                            add_warning "gitmoji.$key" "Unknown field 'gitmoji.$key' - will be ignored"
                            ;;
                    esac
                    ;;

                hooks)
                    case "$key" in
                        runByDefault)
                            if is_boolean "$value"; then
                                HOOKS[runByDefault]=$(normalize_boolean "$value")
                                debug "  Set hooks.runByDefault = ${HOOKS[runByDefault]}"
                            else
                                add_warning "hooks.runByDefault" "Expected boolean for 'hooks.runByDefault', got '$value' - using default"
                                HOOKS[runByDefault]="$DEFAULT_HOOKS_RUN_BY_DEFAULT"
                            fi
                            ;;
                        *)
                            add_warning "hooks.$key" "Unknown field 'hooks.$key' - will be ignored"
                            ;;
                    esac
                    ;;

                format)
                    case "$key" in
                        coAuthor)
                            if is_boolean "$value"; then
                                FORMAT[coAuthor]=$(normalize_boolean "$value")
                                debug "  Set format.coAuthor = ${FORMAT[coAuthor]}"
                            else
                                add_warning "format.coAuthor" "Expected boolean for 'format.coAuthor', got '$value' - using default"
                                FORMAT[coAuthor]="$DEFAULT_FORMAT_CO_AUTHOR"
                            fi
                            ;;
                        messageTemplate)
                            FORMAT[messageTemplate]="$value"
                            debug "  Set format.messageTemplate = $value"
                            # Validate template contains {description}
                            if [[ "$value" != *"{description}"* ]]; then
                                add_warning "format.messageTemplate" "Template should include {description} placeholder"
                            fi
                            ;;
                        bodyTemplate)
                            if is_multiline_start "$value"; then
                                # Start multiline parsing
                                in_multiline=true
                                multiline_field="bodyTemplate"
                                multiline_base_indent=$indent
                                multiline_value=""
                                debug "  Starting multiline bodyTemplate"
                            else
                                FORMAT[bodyTemplate]="$value"
                                debug "  Set format.bodyTemplate = $value"
                            fi
                            ;;
                        *)
                            add_warning "format.$key" "Unknown field 'format.$key' - will be ignored"
                            ;;
                    esac
                    ;;

                *)
                    # Inside an unknown section, ignore
                    debug "  Ignoring field in unknown section"
                    ;;
            esac

        elif [[ $indent -ge 2 ]]; then
            # Deeper nesting - only allowed in lists
            if [[ "$in_list" != "true" ]]; then
                set_error "syntax" "$line_num" "Unexpected nesting at indent level $indent"
                return 1
            fi
        fi

    done < "$file"

    # Save any remaining list item
    if [[ "$in_list" == "true" && $current_list_item_idx -ge 0 && -n "$current_list_emoji" ]]; then
        GITMOJI_CUSTOM_EMOJI+=("$current_list_emoji")
        GITMOJI_CUSTOM_CODE+=("$current_list_code")
        GITMOJI_CUSTOM_DESC+=("$current_list_desc")
        debug "  Saved final custom gitmoji: $current_list_emoji ($current_list_code)"
    fi

    # Save any remaining multiline value
    if [[ "$in_multiline" == "true" && -n "$multiline_value" ]]; then
        FORMAT[$multiline_field]="$multiline_value"
        debug "  Saved final multiline $multiline_field"
    fi

    # Validate custom gitmoji
    for i in "${!GITMOJI_CUSTOM_EMOJI[@]}"; do
        if [[ -z "${GITMOJI_CUSTOM_CODE[$i]:-}" ]]; then
            add_warning "gitmoji.custom[$i]" "Missing required 'code' field"
        elif [[ ! "${GITMOJI_CUSTOM_CODE[$i]}" =~ ^:[a-z_]+:$ ]]; then
            add_warning "gitmoji.custom[$i].code" "Code '${GITMOJI_CUSTOM_CODE[$i]}' should match :word: format"
        fi
    done

    # Check if file was effectively empty
    if [[ "$has_content" != "true" ]]; then
        debug "File is empty or contains only comments"
        return 2  # Signal empty file
    fi

    return 0
}

apply_defaults() {
    debug "Applying defaults..."

    if [[ -z "${GITMOJI[enabled]:-}" ]]; then
        GITMOJI[enabled]="$DEFAULT_GITMOJI_ENABLED"
        debug "  Default gitmoji.enabled = $DEFAULT_GITMOJI_ENABLED"
    fi

    if [[ -z "${HOOKS[runByDefault]:-}" ]]; then
        HOOKS[runByDefault]="$DEFAULT_HOOKS_RUN_BY_DEFAULT"
        debug "  Default hooks.runByDefault = $DEFAULT_HOOKS_RUN_BY_DEFAULT"
    fi

    if [[ -z "${FORMAT[coAuthor]:-}" ]]; then
        FORMAT[coAuthor]="$DEFAULT_FORMAT_CO_AUTHOR"
        debug "  Default format.coAuthor = $DEFAULT_FORMAT_CO_AUTHOR"
    fi
}

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------

main() {
    local config_file=""

    # Parse arguments
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

    # Check config file argument
    if [[ -z "$config_file" ]]; then
        echo "Error: Config file path required" >&2
        usage >&2
        exit 1
    fi

    debug "Config file: $config_file"

    # Check if file exists
    if [[ ! -f "$config_file" ]]; then
        debug "Config file does not exist - outputting null config"
        output_missing
        exit 0
    fi

    # Check if file is readable
    if [[ ! -r "$config_file" ]]; then
        set_error "io" "0" "Cannot read config file: $config_file"
        output_error
        exit 1
    fi

    # Parse YAML
    local parse_result
    set +e
    parse_yaml_file "$config_file"
    parse_result=$?
    set -e

    if [[ $parse_result -eq 1 ]]; then
        # Syntax error
        output_error
        exit 1
    elif [[ $parse_result -eq 2 ]]; then
        # Empty file - use defaults
        debug "Empty config file - outputting null config"
        output_missing
        exit 0
    fi

    # Apply defaults
    apply_defaults

    # Output success
    output_success
    exit 0
}

main "$@"
