#!/bin/bash
# Jira API Client for Claude KM Skill
# Supports Atlassian Cloud (*.atlassian.net)

set -e

# =============================================================================
# Dependency Checks
# =============================================================================

check_dependencies() {
    local missing=()
    command -v jq >/dev/null 2>&1 || missing+=("jq")
    command -v curl >/dev/null 2>&1 || missing+=("curl")

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: Missing required dependencies: ${missing[*]}" >&2
        echo "Please install them and try again." >&2
        return 1
    fi
}

# Run dependency check early (except for help)
if [[ "${1:-}" != "help" ]] && [[ "${1:-}" != "--help" ]] && [[ "${1:-}" != "-h" ]] && [[ -n "${1:-}" ]]; then
    check_dependencies || exit 1
fi

# =============================================================================
# Input Validation
# =============================================================================

# Validate issue key format (PROJECT-123)
validate_issue_key() {
    local key="$1"
    if [[ ! "$key" =~ ^[A-Z][A-Z0-9]+-[0-9]+$ ]]; then
        echo "Error: Invalid issue key format: $key" >&2
        echo "Expected format: PROJECT-123 (e.g., PROJ-42)" >&2
        return 1
    fi
}

# Validate transition ID (numeric)
validate_transition_id() {
    local id="$1"
    if [[ ! "$id" =~ ^[0-9]+$ ]]; then
        echo "Error: Invalid transition ID: $id" >&2
        echo "Transition ID must be numeric" >&2
        return 1
    fi
}

# =============================================================================
# Configuration
# =============================================================================

# Config file location (project-level or user-level)
JIRA_CONFIG_FILE="${JIRA_CONFIG_FILE:-.jira-config}"
JIRA_USER_CONFIG="$HOME/.config/claude-km/jira.conf"

# Load config from file if exists
# Priority: .jira-config > .env > ~/.config/claude-km/jira.conf > env vars
load_config() {
    # Try project-level config first
    if [[ -f "$JIRA_CONFIG_FILE" ]]; then
        source "$JIRA_CONFIG_FILE"
    # Then try .env file (only load JIRA_* variables)
    elif [[ -f ".env" ]]; then
        while IFS='=' read -r key value; do
            # Only export JIRA_* variables, skip comments and empty lines
            if [[ "$key" =~ ^JIRA_ ]]; then
                # Remove surrounding quotes from value
                value="${value%\"}"
                value="${value#\"}"
                value="${value%\'}"
                value="${value#\'}"
                export "$key=$value"
            fi
        done < .env
    # Then try user-level config
    elif [[ -f "$JIRA_USER_CONFIG" ]]; then
        source "$JIRA_USER_CONFIG"
    fi
}

# Required environment variables (can be set in config file):
# JIRA_DOMAIN - e.g., "mycompany.atlassian.net"
# JIRA_EMAIL - e.g., "user@example.com"
# JIRA_API_TOKEN - API token from https://id.atlassian.com/manage-profile/security/api-tokens
# JIRA_PROJECT - default project key, e.g., "PROJ"

load_config

# Validate required config
validate_config() {
    local missing=()
    [[ -z "$JIRA_DOMAIN" ]] && missing+=("JIRA_DOMAIN")
    [[ -z "$JIRA_EMAIL" ]] && missing+=("JIRA_EMAIL")
    [[ -z "$JIRA_API_TOKEN" ]] && missing+=("JIRA_API_TOKEN")

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: Missing required configuration: ${missing[*]}" >&2
        echo "" >&2
        echo "Set these in one of:" >&2
        echo "  1. Environment variables" >&2
        echo "  2. Project config: $JIRA_CONFIG_FILE" >&2
        echo "  3. Project .env file" >&2
        echo "  4. User config: $JIRA_USER_CONFIG" >&2
        echo "" >&2
        echo "Run: jira-client.sh init" >&2
        return 1
    fi

    # Sanitize JIRA_DOMAIN: strip protocol and trailing slash
    JIRA_DOMAIN="${JIRA_DOMAIN#https://}"
    JIRA_DOMAIN="${JIRA_DOMAIN#http://}"
    JIRA_DOMAIN="${JIRA_DOMAIN%/}"

    # Validate domain format
    if [[ ! "$JIRA_DOMAIN" =~ ^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$ ]]; then
        echo "Error: Invalid JIRA_DOMAIN format: $JIRA_DOMAIN" >&2
        echo "Expected: company.atlassian.net (without https://)" >&2
        return 1
    fi
}

# Auto-assign based on summary prefix mapping
auto_assign() {
    local summary="$1"
    local issue_key="$2"

    # Extract prefix from [prefix] pattern in summary
    local prefix
    prefix=$(echo "$summary" | grep -oE '^\[[^]]+\]' | tr -d '[]' | tr '-' '_' | tr '[:upper:]' '[:lower:]')

    if [[ -z "$prefix" ]]; then
        return 0
    fi

    # Lookup in mapping (JIRA_ASSIGN_MAP_<prefix>)
    local var_name="JIRA_ASSIGN_MAP_${prefix}"
    local account_id="${!var_name}"

    if [[ -n "$account_id" ]]; then
        local payload
        payload=$(jq -n --arg id "$account_id" '{accountId: $id}')
        local result
        result=$(jira_api PUT "/issue/${issue_key}/assignee" "$payload")
        if [[ -z "$result" ]]; then
            echo "Auto-assigned $issue_key (prefix: $prefix)" >&2
        else
            echo "Warning: Auto-assign failed for $issue_key" >&2
        fi
    else
        echo "Note: No auto-assign mapping for prefix [$prefix]." >&2
        echo "  Add to config: JIRA_ASSIGN_MAP_${prefix}=\"<accountId>\"" >&2
        echo "  Or create a Jira Automation Rule (Project Settings > Automation)" >&2
    fi
}

# Base URL for API calls
get_base_url() {
    echo "https://${JIRA_DOMAIN}/rest/api/3"
}

# =============================================================================
# Markdown to ADF Converter
# =============================================================================

# Convert markdown text to Atlassian Document Format (ADF) JSON
# Supports: headings, bullet lists, ordered lists, code blocks, bold, italic, inline code
markdown_to_adf() {
    local markdown="$1"

    # Use jq to parse markdown lines into ADF nodes
    echo "$markdown" | jq -Rs '
def parse_inline_marks:
    # Simple inline formatting: convert **bold**, *italic*, `code`
    # Uses gsub-based approach for reliability
    . as $text |
    # If no special chars, return plain text node
    if ($text | test("[*`]") | not) then
        [{type: "text", text: $text}]
    else
        # Split by inline code first (highest priority)
        [$text | split("`")] | .[0] as $parts |
        if ($parts | length) > 2 then
            # Has inline code - process pairs
            [range(0; $parts | length)] | map(
                $parts[.] as $part |
                if . % 2 == 1 then
                    # Odd index = inside backticks
                    {type: "text", text: $part, marks: [{type: "code"}]}
                elif ($part | test("\\*\\*")) then
                    # Process bold in non-code segments
                    [$part | split("**")] | .[0] as $bparts |
                    [range(0; $bparts | length)] | map(
                        $bparts[.] as $bp |
                        if . % 2 == 1 then
                            {type: "text", text: $bp, marks: [{type: "strong"}]}
                        elif ($bp | length) > 0 then
                            {type: "text", text: $bp}
                        else empty end
                    )[]
                elif ($part | length) > 0 then
                    {type: "text", text: $part}
                else empty end
            )
        elif ($text | test("\\*\\*")) then
            # Process bold
            [$text | split("**")] | .[0] as $bparts |
            [range(0; $bparts | length)] | map(
                $bparts[.] as $bp |
                if . % 2 == 1 then
                    {type: "text", text: $bp, marks: [{type: "strong"}]}
                elif ($bp | length) > 0 then
                    {type: "text", text: $bp}
                else empty end
            )
        elif ($text | test("\\*[^*]+\\*")) then
            # Process italic
            [$text | split("*")] | .[0] as $iparts |
            [range(0; $iparts | length)] | map(
                $iparts[.] as $ip |
                if . % 2 == 1 then
                    {type: "text", text: $ip, marks: [{type: "em"}]}
                elif ($ip | length) > 0 then
                    {type: "text", text: $ip}
                else empty end
            )
        else
            [{type: "text", text: $text}]
        end
    end | [.[] | select(.text != "")];

split("\n") |

# Process lines into blocks
reduce .[] as $line (
    {blocks: [], current_list: null, list_type: null, code_block: false, code_lines: [], code_lang: ""};

    if .code_block then
        if ($line | test("^```")) then
            # End code block
            .blocks += [{
                type: "codeBlock",
                attrs: (if .code_lang != "" then {language: .code_lang} else {} end),
                content: [{type: "text", text: (.code_lines | join("\n"))}]
            }] |
            .code_block = false |
            .code_lines = [] |
            .code_lang = ""
        else
            .code_lines += [$line]
        end
    elif ($line | test("^```")) then
        # Start code block - flush any pending list
        (if .current_list != null then
            .blocks += [{type: .list_type, content: .current_list}] |
            .current_list = null |
            .list_type = null
        else . end) |
        .code_block = true |
        .code_lang = ($line | sub("^```"; "") | sub("\\s*$"; ""))
    elif ($line | test("^#{1,6}\\s")) then
        # Heading - flush any pending list
        (if .current_list != null then
            .blocks += [{type: .list_type, content: .current_list}] |
            .current_list = null |
            .list_type = null
        else . end) |
        ($line | capture("^(?<hashes>#{1,6})\\s+(?<text>.+)$")) as $m |
        .blocks += [{
            type: "heading",
            attrs: {level: ($m.hashes | length)},
            content: ($m.text | parse_inline_marks)
        }]
    elif ($line | test("^[-*]\\s+")) then
        # Bullet list item
        ($line | sub("^[-*]\\s+"; "")) as $text |
        if .list_type == "bulletList" then
            .current_list += [{type: "listItem", content: [{type: "paragraph", content: ($text | parse_inline_marks)}]}]
        else
            (if .current_list != null then
                .blocks += [{type: .list_type, content: .current_list}]
            else . end) |
            .list_type = "bulletList" |
            .current_list = [{type: "listItem", content: [{type: "paragraph", content: ($text | parse_inline_marks)}]}]
        end
    elif ($line | test("^[0-9]+\\.\\s+")) then
        # Ordered list item
        ($line | sub("^[0-9]+\\.\\s+"; "")) as $text |
        if .list_type == "orderedList" then
            .current_list += [{type: "listItem", content: [{type: "paragraph", content: ($text | parse_inline_marks)}]}]
        else
            (if .current_list != null then
                .blocks += [{type: .list_type, content: .current_list}]
            else . end) |
            .list_type = "orderedList" |
            .current_list = [{type: "listItem", content: [{type: "paragraph", content: ($text | parse_inline_marks)}]}]
        end
    elif ($line | test("^\\s*$")) then
        # Empty line - flush list
        (if .current_list != null then
            .blocks += [{type: .list_type, content: .current_list}] |
            .current_list = null |
            .list_type = null
        else . end)
    else
        # Regular paragraph - flush list
        (if .current_list != null then
            .blocks += [{type: .list_type, content: .current_list}] |
            .current_list = null |
            .list_type = null
        else . end) |
        .blocks += [{type: "paragraph", content: ($line | parse_inline_marks)}]
    end
) |

# Flush any remaining list
(if .current_list != null then
    .blocks += [{type: .list_type, content: .current_list}]
else . end) |

# Build final ADF document
{
    type: "doc",
    version: 1,
    content: (if (.blocks | length) == 0 then [{type: "paragraph", content: [{type: "text", text: ""}]}] else .blocks end)
}
'
}

# =============================================================================
# API Helper Functions
# =============================================================================

# Make authenticated API request
jira_api() {
    local method="$1"
    local endpoint="$2"
    local data="$3"

    local url="$(get_base_url)${endpoint}"
    local auth=$(echo -n "${JIRA_EMAIL}:${JIRA_API_TOKEN}" | base64)

    local curl_args=(
        -s
        -X "$method"
        -H "Authorization: Basic $auth"
        -H "Content-Type: application/json"
        -H "Accept: application/json"
    )

    if [[ -n "$data" ]]; then
        curl_args+=(-d "$data")
    fi

    curl "${curl_args[@]}" "$url"
}

# =============================================================================
# Commands
# =============================================================================

# Initialize configuration
cmd_init() {
    local domain="" email="" token="" project=""
    local config_type="project"
    local config_file

    local token_stdin=false

    # Parse arguments for non-interactive mode
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --domain)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --domain requires a value" >&2; return 1; }
                domain="$2"; shift 2 ;;
            --email)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --email requires a value" >&2; return 1; }
                email="$2"; shift 2 ;;
            --token)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --token requires a value" >&2; return 1; }
                token="$2"; shift 2 ;;
            --token-stdin)
                token_stdin=true; shift ;;
            --project)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --project requires a value" >&2; return 1; }
                project="$2"; shift 2 ;;
            --location)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --location requires a value" >&2; return 1; }
                [[ "$2" != "project" && "$2" != "user" && "$2" != "env" ]] && { echo "Error: --location must be 'project', 'user', or 'env'" >&2; return 1; }
                config_type="$2"; shift 2 ;;
            user|project|env) config_type="$1"; shift ;;
            *)
                echo "Unknown option: $1" >&2
                echo "Usage: jira-client.sh init --domain X --email Y --token Z --project P [--location project|user]" >&2
                return 1
                ;;
        esac
    done

    # Read token from stdin if --token-stdin was specified
    if [[ "$token_stdin" == true ]]; then
        read -r token
        if [[ -z "$token" ]]; then
            echo "Error: No token received from stdin" >&2
            return 1
        fi
    fi

    # Fall back to JIRA_API_TOKEN environment variable if --token not provided
    if [[ -z "$token" ]] && [[ -n "${JIRA_API_TOKEN:-}" ]]; then
        token="$JIRA_API_TOKEN"
    fi

    if [[ "$config_type" == "user" ]]; then
        config_file="$JIRA_USER_CONFIG"
        mkdir -p "$(dirname "$config_file")"
    elif [[ "$config_type" == "env" ]]; then
        config_file=".env"
    else
        config_file="$JIRA_CONFIG_FILE"
    fi

    # If arguments not fully provided, fall back to interactive mode
    if [[ -z "$domain" ]] || [[ -z "$email" ]] || [[ -z "$token" ]] || [[ -z "$project" ]]; then
        # Check if running in interactive terminal
        if [[ ! -t 0 ]]; then
            echo "Error: Non-interactive mode detected but required arguments missing." >&2
            echo "" >&2
            echo "Usage: jira-client.sh init --domain X --email Y --token Z --project P [--location project|user]" >&2
            echo "" >&2
            echo "Arguments:" >&2
            echo "  --domain      Jira domain (e.g., mycompany.atlassian.net)" >&2
            echo "  --email       Your Atlassian account email" >&2
            echo "  --token       API token (visible in process list - use alternatives below)" >&2
            echo "  --token-stdin Read token from stdin (e.g., echo \$TOKEN | jira-client.sh init --token-stdin ...)" >&2
            echo "  --project     Default project key (e.g., PROJ)" >&2
            echo "  --location    Config location: 'project' (default), 'user', or 'env'" >&2
            echo "" >&2
            echo "Token can also be set via JIRA_API_TOKEN environment variable." >&2
            return 1
        fi

        echo "Jira Configuration Setup"
        echo "========================"
        echo ""

        [[ -z "$domain" ]] && read -p "Jira Domain (e.g., mycompany.atlassian.net): " domain
        [[ -z "$email" ]] && read -p "Email: " email
        [[ -z "$token" ]] && { read -sp "API Token: " token; echo ""; }
        [[ -z "$project" ]] && read -p "Default Project Key (e.g., PROJ): " project
    fi

    # Validate required fields
    if [[ -z "$domain" ]] || [[ -z "$email" ]] || [[ -z "$token" ]] || [[ -z "$project" ]]; then
        echo "Error: All fields are required (domain, email, token, project)" >&2
        return 1
    fi

    # Format validation
    if [[ ! "$domain" =~ ^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$ ]]; then
        echo "Error: Invalid domain format. Expected something like 'mycompany.atlassian.net'." >&2
        return 1
    fi

    if [[ ! "$email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        echo "Error: Invalid email format. Expected something like 'user@example.com'." >&2
        return 1
    fi

    if [[ ! "$project" =~ ^[A-Z][A-Z0-9]*$ ]]; then
        echo "Error: Invalid project key format. Use uppercase letters and numbers (e.g., 'PROJ')." >&2
        return 1
    fi

    if [[ "$config_type" == "env" ]]; then
        # For .env: remove existing JIRA_* lines and append new ones
        if [[ -f "$config_file" ]]; then
            # Remove existing JIRA_* lines
            local tmp_file
            tmp_file=$(mktemp)
            grep -v '^JIRA_' "$config_file" > "$tmp_file" 2>/dev/null || true
            mv "$tmp_file" "$config_file"
        fi
        # Append JIRA config
        cat >> "$config_file" << EOF
JIRA_DOMAIN="$domain"
JIRA_EMAIL="$email"
JIRA_API_TOKEN="$token"
JIRA_PROJECT="$project"
EOF
    else
        cat > "$config_file" << EOF
# Jira Configuration
# Generated: $(date '+%Y-%m-%d %H:%M')

JIRA_DOMAIN="$domain"
JIRA_EMAIL="$email"
JIRA_API_TOKEN="$token"
JIRA_PROJECT="$project"
EOF
    fi

    chmod 600 "$config_file"

    echo "Configuration saved to: $config_file"

    # Add to .gitignore if project-level
    if [[ "$config_type" != "user" ]] && [[ -f ".gitignore" ]]; then
        if [[ "$config_type" == "env" ]]; then
            if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
                echo ".env" >> .gitignore
                echo "Added .env to .gitignore"
            fi
        else
            if ! grep -q "^\.jira-config$" .gitignore 2>/dev/null; then
                echo ".jira-config" >> .gitignore
                echo "Added .jira-config to .gitignore"
            fi
        fi
    fi
}

# Test connection
cmd_test() {
    validate_config || return 1

    echo "Testing connection to ${JIRA_DOMAIN}..."
    local result=$(jira_api GET "/myself")

    if echo "$result" | jq -e '.accountId' > /dev/null 2>&1; then
        local name=$(echo "$result" | jq -r '.displayName')
        local email=$(echo "$result" | jq -r '.emailAddress')
        echo "Connected as: $name ($email)"
        return 0
    else
        echo "Connection failed:" >&2
        echo "$result" | jq -r '.errorMessages[]?' 2>/dev/null || echo "$result" >&2
        return 1
    fi
}

# List projects
cmd_projects() {
    validate_config || return 1

    local result=$(jira_api GET "/project")
    echo "$result" | jq -r '.[] | "\(.key)\t\(.name)"' | column -t -s $'\t'
}

# Create issue
cmd_create() {
    validate_config || return 1

    local project="" summary="" description="" issue_type="Task" assign_to=""

    # Parse positional and flag arguments
    local positional=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --assign)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --assign requires a value (accountId or 'me')" >&2; return 1; }
                assign_to="$2"; shift 2 ;;
            --assign-self)
                assign_to="me"; shift ;;
            *)
                positional+=("$1"); shift ;;
        esac
    done

    project="${positional[0]:-$JIRA_PROJECT}"
    summary="${positional[1]:-}"
    description="${positional[2]:-}"
    issue_type="${positional[3]:-Task}"

    if [[ -z "$project" ]] || [[ -z "$summary" ]]; then
        echo "Usage: jira-client.sh create <project> <summary> [description] [issue_type] [--assign me|accountId]" >&2
        return 1
    fi

    # Build payload using jq for safe JSON escaping
    local payload
    if [[ -n "$description" ]]; then
        local adf_description
        adf_description=$(markdown_to_adf "$description")

        payload=$(jq -n \
            --arg project "$project" \
            --arg summary "$summary" \
            --argjson description "$adf_description" \
            --arg issue_type "$issue_type" \
            '{
                fields: {
                    project: { key: $project },
                    summary: $summary,
                    description: $description,
                    issuetype: { name: $issue_type }
                }
            }')
    else
        payload=$(jq -n \
            --arg project "$project" \
            --arg summary "$summary" \
            --arg issue_type "$issue_type" \
            '{
                fields: {
                    project: { key: $project },
                    summary: $summary,
                    issuetype: { name: $issue_type }
                }
            }')
    fi

    local result=$(jira_api POST "/issue" "$payload")

    if echo "$result" | jq -e '.key' > /dev/null 2>&1; then
        local key=$(echo "$result" | jq -r '.key')
        # Info messages to stderr, key to stdout for programmatic use
        echo "Created: $key" >&2
        echo "URL: https://${JIRA_DOMAIN}/browse/$key" >&2

        # Handle assignment: explicit flag > prefix mapping
        if [[ -n "$assign_to" ]]; then
            local aid="$assign_to"
            if [[ "$aid" == "me" ]]; then
                aid=$(jira_api GET "/myself" | jq -r '.accountId')
            fi
            local assign_payload
            assign_payload=$(jq -n --arg id "$aid" '{accountId: $id}')
            local assign_result
            assign_result=$(jira_api PUT "/issue/${key}/assignee" "$assign_payload")
            if [[ -z "$assign_result" ]]; then
                echo "Assigned: $key" >&2
            else
                echo "Warning: Assignment failed for $key" >&2
            fi
        else
            auto_assign "$summary" "$key"
        fi

        echo "$key"
    else
        echo "Failed to create issue:" >&2
        echo "$result" | jq -r '.errors // .errorMessages[]?' 2>/dev/null || echo "$result" >&2
        return 1
    fi
}

# Create subtask under a parent issue
cmd_create_subtask() {
    validate_config || return 1

    local parent_key="" summary="" description="" due_date="" assign_to=""

    # Parse arguments
    local positional=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --due)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --due requires a date (YYYY-MM-DD)" >&2; return 1; }
                due_date="$2"; shift 2 ;;
            --assign)
                [[ -z "${2:-}" || "$2" == --* ]] && { echo "Error: --assign requires a value (accountId or 'me')" >&2; return 1; }
                assign_to="$2"; shift 2 ;;
            --assign-self)
                assign_to="me"; shift ;;
            *)
                positional+=("$1"); shift ;;
        esac
    done

    parent_key="${positional[0]:-}"
    summary="${positional[1]:-}"
    description="${positional[2]:-}"

    if [[ -z "$parent_key" ]] || [[ -z "$summary" ]]; then
        echo "Usage: jira-client.sh create-subtask <parent-key> <summary> [description] [--due YYYY-MM-DD] [--assign me|accountId]" >&2
        return 1
    fi

    validate_issue_key "$parent_key" || return 1

    # Validate due date format if provided
    if [[ -n "$due_date" ]] && [[ ! "$due_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "Error: Invalid date format. Expected YYYY-MM-DD" >&2
        return 1
    fi

    # Extract project from parent key
    local project
    project=$(echo "$parent_key" | cut -d'-' -f1)

    # Build payload
    local payload
    if [[ -n "$description" ]]; then
        local adf_description
        adf_description=$(markdown_to_adf "$description")

        payload=$(jq -n \
            --arg project "$project" \
            --arg parent "$parent_key" \
            --arg summary "$summary" \
            --argjson description "$adf_description" \
            --arg due_date "$due_date" \
            '{
                fields: {
                    project: { key: $project },
                    parent: { key: $parent },
                    summary: $summary,
                    description: $description,
                    issuetype: { name: "Subtask" }
                }
            } | if $due_date != "" then .fields.duedate = $due_date else . end')
    else
        payload=$(jq -n \
            --arg project "$project" \
            --arg parent "$parent_key" \
            --arg summary "$summary" \
            --arg due_date "$due_date" \
            '{
                fields: {
                    project: { key: $project },
                    parent: { key: $parent },
                    summary: $summary,
                    issuetype: { name: "Subtask" }
                }
            } | if $due_date != "" then .fields.duedate = $due_date else . end')
    fi

    local result=$(jira_api POST "/issue" "$payload")

    if echo "$result" | jq -e '.key' > /dev/null 2>&1; then
        local key=$(echo "$result" | jq -r '.key')
        echo "Created subtask: $key (parent: $parent_key)" >&2
        echo "URL: https://${JIRA_DOMAIN}/browse/$key" >&2

        # Handle assignment
        if [[ -n "$assign_to" ]]; then
            local aid="$assign_to"
            if [[ "$aid" == "me" ]]; then
                aid=$(jira_api GET "/myself" | jq -r '.accountId')
            fi
            local assign_payload
            assign_payload=$(jq -n --arg id "$aid" '{accountId: $id}')
            local assign_result
            assign_result=$(jira_api PUT "/issue/${key}/assignee" "$assign_payload")
            if [[ -z "$assign_result" ]]; then
                echo "Assigned: $key" >&2
            fi
        else
            auto_assign "$summary" "$key"
        fi

        echo "$key"
    else
        echo "Failed to create subtask:" >&2
        echo "$result" | jq -r '.errors // .errorMessages[]?' 2>/dev/null || echo "$result" >&2
        return 1
    fi
}

# Create multiple subtasks from a JSON file
cmd_create_subtasks() {
    validate_config || return 1

    local parent_key="${1:-}"
    local file="${2:-}"

    if [[ -z "$parent_key" ]] || [[ -z "$file" ]]; then
        echo "Usage: jira-client.sh create-subtasks <parent-key> <file.json>" >&2
        echo "" >&2
        echo "File format (JSON array):" >&2
        echo '  [{"summary": "Task 1", "description": "Details", "due": "2026-02-10"}]' >&2
        return 1
    fi

    validate_issue_key "$parent_key" || return 1

    if [[ ! -f "$file" ]]; then
        echo "Error: File not found: $file" >&2
        return 1
    fi

    local count=0
    local total
    total=$(jq '. | length' "$file")

    echo "Creating $total subtasks under $parent_key..." >&2

    jq -c '.[]' "$file" | while read -r item; do
        local summary due_date description assign
        summary=$(echo "$item" | jq -r '.summary')
        description=$(echo "$item" | jq -r '.description // ""')
        due_date=$(echo "$item" | jq -r '.due // ""')
        assign=$(echo "$item" | jq -r '.assign // ""')

        local args=("$parent_key" "$summary")
        [[ -n "$description" ]] && args+=("$description")
        [[ -n "$due_date" ]] && args+=("--due" "$due_date")
        [[ -n "$assign" ]] && args+=("--assign" "$assign")

        cmd_create_subtask "${args[@]}"
        count=$((count + 1))
        echo "  [$count/$total] done" >&2
    done

    echo "Created $total subtasks under $parent_key" >&2
}

# Get issue details
cmd_get() {
    validate_config || return 1

    local issue_key="$1"

    if [[ -z "$issue_key" ]]; then
        echo "Usage: jira-client.sh get <issue_key>" >&2
        return 1
    fi

    validate_issue_key "$issue_key" || return 1

    local result=$(jira_api GET "/issue/$issue_key")

    if echo "$result" | jq -e '.key' > /dev/null 2>&1; then
        echo "$result" | jq '{
            key: .key,
            summary: .fields.summary,
            status: .fields.status.name,
            type: .fields.issuetype.name,
            priority: .fields.priority.name,
            assignee: (.fields.assignee.displayName // "Unassigned"),
            reporter: .fields.reporter.displayName,
            created: .fields.created,
            updated: .fields.updated,
            url: "https://'"${JIRA_DOMAIN}"'/browse/\(.key)"
        }'
    else
        echo "Issue not found: $issue_key" >&2
        return 1
    fi
}

# List issues (with JQL)
cmd_list() {
    validate_config || return 1

    local project="${1:-$JIRA_PROJECT}"
    local status="${2:-}"
    local max_results="${3:-20}"

    local jql="project = $project"
    if [[ -n "$status" ]]; then
        jql="$jql AND status = '$status'"
    fi
    jql="$jql ORDER BY updated DESC"

    local encoded_jql=$(echo "$jql" | jq -sRr @uri)
    local result=$(jira_api GET "/search?jql=$encoded_jql&maxResults=$max_results&fields=key,summary,status,issuetype,priority,assignee")

    echo "$result" | jq -r '.issues[] | "\(.key)\t\(.fields.status.name)\t\(.fields.summary)"' | column -t -s $'\t'
}

# Search issues by text
cmd_search() {
    validate_config || return 1

    local query="$1"
    local project="${2:-$JIRA_PROJECT}"
    local max_results="${3:-20}"

    if [[ -z "$query" ]]; then
        echo "Usage: jira-client.sh search <query> [project] [max_results]" >&2
        return 1
    fi

    local jql="text ~ \"$query\""
    if [[ -n "$project" ]]; then
        jql="project = $project AND $jql"
    fi
    jql="$jql ORDER BY updated DESC"

    local encoded_jql=$(echo "$jql" | jq -sRr @uri)
    local result=$(jira_api GET "/search?jql=$encoded_jql&maxResults=$max_results&fields=key,summary,status,issuetype")

    echo "$result" | jq -r '.issues[] | "\(.key)\t\(.fields.status.name)\t\(.fields.summary)"' | column -t -s $'\t'
}

# Get available transitions for an issue
cmd_transitions() {
    validate_config || return 1

    local issue_key="$1"

    if [[ -z "$issue_key" ]]; then
        echo "Usage: jira-client.sh transitions <issue_key>" >&2
        return 1
    fi

    validate_issue_key "$issue_key" || return 1

    local result=$(jira_api GET "/issue/$issue_key/transitions")
    echo "$result" | jq -r '.transitions[] | "\(.id)\t\(.name)"' | column -t -s $'\t'
}

# Transition issue to new status
cmd_transition() {
    validate_config || return 1

    local issue_key="$1"
    local transition_id="$2"

    if [[ -z "$issue_key" ]] || [[ -z "$transition_id" ]]; then
        echo "Usage: jira-client.sh transition <issue_key> <transition_id>" >&2
        echo "Use 'jira-client.sh transitions <issue_key>' to see available transitions" >&2
        return 1
    fi

    validate_issue_key "$issue_key" || return 1
    validate_transition_id "$transition_id" || return 1

    # Build payload using jq for safe JSON
    local payload=$(jq -n --arg id "$transition_id" '{transition: {id: $id}}')
    local result=$(jira_api POST "/issue/$issue_key/transitions" "$payload")

    # Jira API returns 204 No Content on success (empty response)
    if [[ -z "$result" ]]; then
        echo "Transitioned $issue_key successfully"
        # Show new status
        cmd_get "$issue_key" | jq -r '"New status: \(.status)"'
    else
        echo "Failed to transition:" >&2
        echo "$result" >&2
        return 1
    fi
}

# Add comment to issue
cmd_comment() {
    validate_config || return 1

    local issue_key="$1"
    local comment="$2"

    if [[ -z "$issue_key" ]] || [[ -z "$comment" ]]; then
        echo "Usage: jira-client.sh comment <issue_key> <comment>" >&2
        return 1
    fi

    validate_issue_key "$issue_key" || return 1

    # Convert markdown comment to ADF format
    local adf_body
    adf_body=$(markdown_to_adf "$comment")

    local payload=$(jq -n --argjson body "$adf_body" '{body: $body}')

    local result=$(jira_api POST "/issue/$issue_key/comment" "$payload")

    if echo "$result" | jq -e '.id' > /dev/null 2>&1; then
        echo "Comment added to $issue_key"
    else
        echo "Failed to add comment:" >&2
        echo "$result" >&2
        return 1
    fi
}

# Assign issue
cmd_assign() {
    validate_config || return 1

    local issue_key="$1"
    local account_id="$2"  # Use -1 for unassigned, or account ID

    if [[ -z "$issue_key" ]]; then
        echo "Usage: jira-client.sh assign <issue_key> [account_id|-1|me]" >&2
        return 1
    fi

    validate_issue_key "$issue_key" || return 1

    # Get current user's account ID if "me"
    if [[ "$account_id" == "me" ]]; then
        account_id=$(jira_api GET "/myself" | jq -r '.accountId')
    fi

    # Build payload using jq for safe JSON escaping
    local payload
    if [[ "$account_id" == "-1" ]] || [[ -z "$account_id" ]]; then
        payload='{"accountId": null}'
    else
        payload=$(jq -n --arg id "$account_id" '{accountId: $id}')
    fi

    local result=$(jira_api PUT "/issue/$issue_key/assignee" "$payload")

    # Jira API returns 204 No Content on success (empty response)
    if [[ -z "$result" ]]; then
        if [[ "$account_id" == "-1" ]] || [[ -z "$account_id" ]]; then
            echo "Unassigned $issue_key"
        else
            echo "Assigned $issue_key"
        fi
    else
        echo "Failed to assign:" >&2
        echo "$result" >&2
        return 1
    fi
}

# Get my assigned issues
cmd_my_issues() {
    validate_config || return 1

    local status="${1:-}"
    local max_results="${2:-20}"

    local jql="assignee = currentUser()"
    if [[ -n "$status" ]]; then
        jql="$jql AND status = '$status'"
    fi
    jql="$jql ORDER BY updated DESC"

    local encoded_jql=$(echo "$jql" | jq -sRr @uri)
    local result=$(jira_api GET "/search?jql=$encoded_jql&maxResults=$max_results&fields=key,summary,status,issuetype,project")

    echo "$result" | jq -r '.issues[] | "\(.key)\t\(.fields.status.name)\t\(.fields.summary)"' | column -t -s $'\t'
}

# List assignable users for a project
cmd_users() {
    validate_config || return 1

    local project="${1:-$JIRA_PROJECT}"

    if [[ -z "$project" ]]; then
        echo "Usage: jira-client.sh users [project]" >&2
        return 1
    fi

    local result
    result=$(jira_api GET "/user/assignable/search?project=$project&maxResults=50")

    if echo "$result" | jq -e '.[0].accountId' > /dev/null 2>&1; then
        printf "%-40s %-25s %s\n" "ACCOUNT_ID" "DISPLAY_NAME" "EMAIL"
        printf "%-40s %-25s %s\n" "----------" "------------" "-----"
        echo "$result" | jq -r '.[] | "\(.accountId)\t\(.displayName)\t\(.emailAddress // "N/A")"' | \
            while IFS=$'\t' read -r id name email; do
                printf "%-40s %-25s %s\n" "$id" "$name" "$email"
            done
    else
        echo "No assignable users found for project $project" >&2
        return 1
    fi
}

# Show status/config info
cmd_status() {
    echo "=== Jira Client Configuration ==="
    echo ""

    if [[ -f "$JIRA_CONFIG_FILE" ]]; then
        echo "Project config: $JIRA_CONFIG_FILE (found)"
    else
        echo "Project config: $JIRA_CONFIG_FILE (not found)"
    fi

    if [[ -f "$JIRA_USER_CONFIG" ]]; then
        echo "User config: $JIRA_USER_CONFIG (found)"
    else
        echo "User config: $JIRA_USER_CONFIG (not found)"
    fi

    echo ""
    echo "Current settings:"
    echo "  Domain: ${JIRA_DOMAIN:-<not set>}"
    echo "  Email: ${JIRA_EMAIL:-<not set>}"
    # Never expose token value - only show if set or not
    if [[ -n "$JIRA_API_TOKEN" ]]; then
        echo "  Token: <set>"
    else
        echo "  Token: <not set>"
    fi
    echo "  Project: ${JIRA_PROJECT:-<not set>}"
}

# =============================================================================
# Main
# =============================================================================

show_help() {
    cat << EOF
Jira API Client for Claude KM Skill

Usage: jira-client.sh <command> [arguments]

Configuration Commands:
  init [options]         Initialize configuration
                        Options: --domain, --email, --token, --token-stdin, --project
                        --location: project (default), user, or env (.env file)
  test                  Test connection
  status                Show configuration status

Issue Commands:
  create <project> <summary> [description] [type] [--assign me|accountId]
                        Create new issue (auto-assigns via prefix mapping)
  create-subtask <parent-key> <summary> [description] [--due YYYY-MM-DD] [--assign me|accountId]
                        Create subtask under parent issue
  create-subtasks <parent-key> <file.json>
                        Batch create subtasks from JSON file
  get <issue_key>       Get issue details
  list [project] [status] [max]
                        List issues in project
  search <query> [project] [max]
                        Search issues by text
  my-issues [status] [max]
                        List my assigned issues

Status Commands:
  transitions <issue_key>
                        List available transitions
  transition <issue_key> <transition_id>
                        Transition issue to new status

Other Commands:
  comment <issue_key> <comment>
                        Add comment to issue
  assign <issue_key> [account_id|me|-1]
                        Assign issue (me=self, -1=unassign)
  users [project]       List assignable users with accountId
  projects              List available projects

Examples:
  jira-client.sh init
  jira-client.sh init --domain myco.atlassian.net --email me@co.com --token XXXX --project PROJ
  jira-client.sh init --domain myco.atlassian.net --email me@co.com --project PROJ --token-stdin <<< "\$TOKEN"
  JIRA_API_TOKEN=XXX jira-client.sh init --domain myco.atlassian.net --email me@co.com --project PROJ
  jira-client.sh init --domain myco.atlassian.net --email me@co.com --token X --project P --location env
  jira-client.sh create PROJ "Fix login bug" "Users can't login" Bug
  jira-client.sh create PROJ "[api] Add endpoint" "Details" Task --assign me
  jira-client.sh create-subtask PROJ-123 "[api] Implement handler" "## Details" --due 2026-02-10
  jira-client.sh create-subtasks PROJ-123 subtasks.json
  jira-client.sh users PROJ
  jira-client.sh list PROJ "In Progress"
  jira-client.sh transition PROJ-123 31
  jira-client.sh my-issues "To Do"

Environment Variables:
  JIRA_DOMAIN           Jira domain (e.g., company.atlassian.net)
  JIRA_EMAIL            Your Atlassian account email
  JIRA_API_TOKEN        API token from Atlassian
  JIRA_PROJECT          Default project key

Auto-assign Configuration:
  Add prefix mappings to .jira-config:
    JIRA_ASSIGN_MAP_api="accountId-of-backend-dev"
    JIRA_ASSIGN_MAP_frontend="accountId-of-frontend-dev"
  Issues with [api] or [frontend] prefix will be auto-assigned.
  Use 'jira-client.sh users' to find accountIds.

Token Methods (most secure first):
  1. Interactive mode: prompted securely (hidden input)
  2. --token-stdin: pipe from secret manager (e.g., echo "\$TOKEN" | jira-client.sh init --token-stdin ...)
  3. JIRA_API_TOKEN env var: set before running init (not logged in history)
  4. --token flag: visible in process list and shell history (least secure)
EOF
}

# Main command dispatcher
main() {
    local command="${1:-}"

    # Show help when no command or explicit help flag
    if [[ -z "$command" || "$command" == "help" || "$command" == "--help" || "$command" == "-h" ]]; then
        show_help
        return 0
    fi

    # Shift past command name (safe here because we know $1 exists)
    shift

    case "$command" in
        init)        cmd_init "$@" ;;
        test)        cmd_test "$@" ;;
        status)      cmd_status "$@" ;;
        projects)    cmd_projects "$@" ;;
        create)      cmd_create "$@" ;;
        create-subtask)  cmd_create_subtask "$@" ;;
        create-subtasks) cmd_create_subtasks "$@" ;;
        get)         cmd_get "$@" ;;
        list)        cmd_list "$@" ;;
        search)      cmd_search "$@" ;;
        my-issues)   cmd_my_issues "$@" ;;
        transitions) cmd_transitions "$@" ;;
        transition)  cmd_transition "$@" ;;
        comment)     cmd_comment "$@" ;;
        assign)      cmd_assign "$@" ;;
        users)       cmd_users "$@" ;;
        *)
            echo "Unknown command: $command" >&2
            echo "Run 'jira-client.sh help' for usage" >&2
            return 1
            ;;
    esac
}

main "$@"
