#!/usr/bin/env bash
# Concourse Pipeline Validation Script
#
# Usage:
#   validate-pipeline.sh <pipeline.yml> [vars.yml...]
#
# Features:
# - Validates YAML syntax
# - Checks for common configuration issues
# - Validates with fly if available
# - Reports potential problems

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0

log_error() {
    echo -e "${RED}ERROR:${NC} $1"
    ((ERRORS++))
}

log_warning() {
    echo -e "${YELLOW}WARNING:${NC} $1"
    ((WARNINGS++))
}

log_success() {
    echo -e "${GREEN}OK:${NC} $1"
}

log_info() {
    echo -e "INFO: $1"
}

# Check dependencies
check_dependencies() {
    if ! command -v yq &> /dev/null; then
        log_warning "yq not found - some validations will be skipped"
        log_info "Install yq: https://github.com/mikefarah/yq"
        return 1
    fi
    return 0
}

# Validate YAML syntax
validate_yaml_syntax() {
    local file="$1"
    log_info "Checking YAML syntax: $file"

    if command -v yq &> /dev/null; then
        if yq eval '.' "$file" > /dev/null 2>&1; then
            log_success "YAML syntax valid"
            return 0
        else
            log_error "Invalid YAML syntax in $file"
            yq eval '.' "$file" 2>&1 | head -5
            return 1
        fi
    elif command -v python3 &> /dev/null; then
        if python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
            log_success "YAML syntax valid"
            return 0
        else
            log_error "Invalid YAML syntax in $file"
            return 1
        fi
    else
        log_warning "Cannot validate YAML syntax - install yq or python3"
        return 0
    fi
}

# Check for required pipeline elements
validate_pipeline_structure() {
    local file="$1"
    log_info "Checking pipeline structure"

    if ! command -v yq &> /dev/null; then
        return 0
    fi

    # Check for jobs (required)
    local job_count
    job_count=$(yq eval '.jobs | length' "$file" 2>/dev/null || echo "0")
    if [[ "$job_count" -eq 0 ]]; then
        log_error "Pipeline has no jobs defined"
    else
        log_success "Found $job_count jobs"
    fi

    # Check each job has a name and plan
    local job_names
    job_names=$(yq eval '.jobs[].name' "$file" 2>/dev/null || echo "")
    for name in $job_names; do
        if [[ -z "$name" || "$name" == "null" ]]; then
            log_error "Job found without name"
        fi
    done

    # Check for resources
    local resource_count
    resource_count=$(yq eval '.resources | length' "$file" 2>/dev/null || echo "0")
    if [[ "$resource_count" -eq 0 ]]; then
        log_warning "Pipeline has no resources defined"
    else
        log_success "Found $resource_count resources"
    fi
}

# Check for common issues
validate_common_issues() {
    local file="$1"
    log_info "Checking for common issues"

    # Check for unescaped regex dots in tag_regex
    if grep -q 'tag_regex:.*\.[0-9]' "$file" 2>/dev/null; then
        if ! grep -q 'tag_regex:.*\\\\.' "$file" 2>/dev/null; then
            log_warning "Possible unescaped dots in tag_regex - use \\\\. for literal dots"
        fi
    fi

    # Check for mixed read/write on same git resource with tags
    if command -v yq &> /dev/null; then
        local git_resources
        git_resources=$(yq eval '.resources[] | select(.type == "git") | .name' "$file" 2>/dev/null || echo "")

        for resource in $git_resources; do
            local has_tag_regex
            has_tag_regex=$(yq eval ".resources[] | select(.name == \"$resource\") | .source.tag_regex" "$file" 2>/dev/null || echo "null")

            if [[ "$has_tag_regex" != "null" && -n "$has_tag_regex" ]]; then
                # Check if this resource is used in both get and put
                local used_in_get
                local used_in_put
                used_in_get=$(yq eval ".jobs[].plan[] | select(.get == \"$resource\") | .get" "$file" 2>/dev/null || echo "")
                used_in_put=$(yq eval ".jobs[].plan[] | select(.put == \"$resource\") | .put" "$file" 2>/dev/null || echo "")

                if [[ -n "$used_in_get" && -n "$used_in_put" ]]; then
                    log_warning "Resource '$resource' with tag_regex is used for both get and put - consider separating"
                fi
            fi
        done
    fi

    # Check for missing trigger: true on get steps
    if command -v yq &> /dev/null; then
        local jobs_without_triggers
        jobs_without_triggers=$(yq eval '.jobs[] | select((.plan[] | select(.get) | .trigger) != true) | .name' "$file" 2>/dev/null | head -5)
        if [[ -n "$jobs_without_triggers" ]]; then
            log_info "Jobs without auto-triggering gets (may be intentional): $(echo $jobs_without_triggers | tr '\n' ' ')"
        fi
    fi

    # Check for hardcoded credentials
    if grep -qiE '(password|secret|token|key):\s*[^(]' "$file" 2>/dev/null; then
        if ! grep -qE '\(\(' "$file" 2>/dev/null; then
            log_warning "Possible hardcoded credentials detected - use ((variables)) instead"
        fi
    fi
}

# Validate with fly CLI if available
validate_with_fly() {
    local file="$1"
    shift
    local var_files=("$@")

    if ! command -v fly &> /dev/null; then
        log_info "fly CLI not found - skipping Concourse validation"
        return 0
    fi

    log_info "Validating with fly CLI"

    local fly_args=("-c" "$file")
    for var_file in "${var_files[@]}"; do
        if [[ -f "$var_file" ]]; then
            fly_args+=("-l" "$var_file")
        fi
    done

    # Try to find a logged-in target
    local target
    target=$(fly targets 2>/dev/null | head -1 | awk '{print $1}' || echo "")

    if [[ -n "$target" ]]; then
        if fly -t "$target" validate-pipeline "${fly_args[@]}" 2>&1; then
            log_success "Pipeline validated successfully with fly"
        else
            log_error "fly validation failed"
        fi
    else
        log_info "No fly target found - using syntax-only validation"
        if fly validate-pipeline "${fly_args[@]}" 2>&1; then
            log_success "Pipeline syntax validated with fly"
        else
            log_error "fly syntax validation failed"
        fi
    fi
}

# Main function
main() {
    if [[ $# -lt 1 ]]; then
        echo "Usage: $0 <pipeline.yml> [vars.yml...]"
        echo ""
        echo "Validates a Concourse CI pipeline configuration"
        exit 1
    fi

    local pipeline_file="$1"
    shift
    local var_files=("$@")

    if [[ ! -f "$pipeline_file" ]]; then
        log_error "Pipeline file not found: $pipeline_file"
        exit 1
    fi

    echo "========================================="
    echo "Concourse Pipeline Validator"
    echo "========================================="
    echo ""

    check_dependencies
    echo ""

    validate_yaml_syntax "$pipeline_file"
    echo ""

    validate_pipeline_structure "$pipeline_file"
    echo ""

    validate_common_issues "$pipeline_file"
    echo ""

    validate_with_fly "$pipeline_file" "${var_files[@]}"
    echo ""

    echo "========================================="
    echo "Summary: $ERRORS errors, $WARNINGS warnings"
    echo "========================================="

    if [[ $ERRORS -gt 0 ]]; then
        exit 1
    fi

    exit 0
}

main "$@"
