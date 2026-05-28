#!/usr/bin/env bash
# ==============================================================================
# YAML Parsing Library
# ==============================================================================
# Provides YAML parsing using yq.
#
# Usage: Source this file and use yaml_get_* functions
# Requires: yq (https://github.com/mikefarah/yq)
# ==============================================================================

set -euo pipefail

# ==============================================================================
# yq Requirement Check
# ==============================================================================

# Ensure yq is installed - called when library is sourced
require_yq() {
    if ! command -v yq &>/dev/null; then
        echo "ERROR: yq is required but not installed." >&2
        echo "Install with: brew install yq" >&2
        exit 1
    fi
}

require_yq

# ==============================================================================
# Domain Field Accessors
# ==============================================================================

# Get a field from a domain definition
# Usage: yaml_get_domain_field <domain> <field>
# Example: yaml_get_domain_field "terraform" "triggers"
yaml_get_domain_field() {
    local domain="$1"
    local field="$2"
    local yaml_file="${DOMAINS_YAML:-}"
    
    [[ -z "$yaml_file" || ! -f "$yaml_file" ]] && return 1
    
    local result
    result=$(yq ".domains.${domain}.${field}" "$yaml_file" 2>/dev/null)
    if [[ "$result" == "null" || -z "$result" ]]; then
        echo ""
    elif [[ "$result" == -* ]]; then
        # Array format (starts with -)
        yq ".domains.${domain}.${field} | .[]" "$yaml_file" 2>/dev/null | tr '\n' ' ' | xargs
    else
        echo "$result" | xargs
    fi
}

# Get triggers for a domain
# Usage: yaml_get_domain_triggers <domain>
yaml_get_domain_triggers() {
    yaml_get_domain_field "$1" "triggers"
}

# Get synonyms for a domain
# Usage: yaml_get_domain_synonyms <domain>
yaml_get_domain_synonyms() {
    yaml_get_domain_field "$1" "synonyms"
}

# Get repos for a domain
# Usage: yaml_get_domain_repos <domain>
yaml_get_domain_repos() {
    yaml_get_domain_field "$1" "repos"
}

# ==============================================================================
# Design Pattern Accessors
# ==============================================================================

# Get a field from a design pattern
# Usage: yaml_get_pattern_field <pattern> <field>
yaml_get_pattern_field() {
    local pattern="$1"
    local field="$2"
    local yaml_file="${DOMAINS_YAML:-}"
    
    [[ -z "$yaml_file" || ! -f "$yaml_file" ]] && return 1
    
    yq -r ".design_patterns.\"${pattern}\".${field} // empty" "$yaml_file" 2>/dev/null
}

# Get nested field from design pattern
# Usage: yaml_get_pattern_nested <pattern> <path>
# Example: yaml_get_pattern_nested "vault" "types.read.description"
yaml_get_pattern_nested() {
    local pattern="$1"
    local path="$2"
    local yaml_file="${DOMAINS_YAML:-}"
    
    [[ -z "$yaml_file" || ! -f "$yaml_file" ]] && return 1
    
    yq -r ".design_patterns.\"${pattern}\".${path} // empty" "$yaml_file" 2>/dev/null
}

# ==============================================================================
# List Accessors
# ==============================================================================

# Get list of all domain names
# Usage: yaml_get_all_domains
yaml_get_all_domains() {
    local yaml_file="${DOMAINS_YAML:-}"
    
    [[ -z "$yaml_file" || ! -f "$yaml_file" ]] && return 1
    
    yq -r '.domains | keys | .[]' "$yaml_file" 2>/dev/null
}

# Get list of all design pattern names
# Usage: yaml_get_all_patterns
yaml_get_all_patterns() {
    local yaml_file="${DOMAINS_YAML:-}"
    
    [[ -z "$yaml_file" || ! -f "$yaml_file" ]] && return 1
    
    yq -r '.design_patterns | keys | .[]' "$yaml_file" 2>/dev/null
}

# ==============================================================================
# Search Configuration
# ==============================================================================

# Get search config value
# Usage: yaml_get_search_config <key>
yaml_get_search_config() {
    local key="$1"
    local yaml_file="${DOMAINS_YAML:-}"
    
    [[ -z "$yaml_file" || ! -f "$yaml_file" ]] && return 1
    
    yq -r ".search.${key} // empty" "$yaml_file" 2>/dev/null
}

# ==============================================================================
# Validation
# ==============================================================================

# Check if YAML file is valid
# Usage: yaml_validate <file>
yaml_validate() {
    local yaml_file="$1"
    
    [[ ! -f "$yaml_file" ]] && return 1
    
    yq '.' "$yaml_file" &>/dev/null
    return $?
}
