#!/usr/bin/env bash
#
# code-security.sh - Code Security Operations for GitHub Ops Skill
# MCP Parity: list_code_scanning_alerts, get_code_scanning_alert,
#             list_dependabot_alerts, get_dependabot_alert,
#             list_secret_scanning_alerts, get_secret_scanning_alert
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

LIMIT=30
STATE="open"
JSON_OUTPUT=false

usage() {
    cat << EOF
Usage: $(basename "$0") <action> [options]

Code Security Operations - GitHub MCP Server Parity

Actions:
  code-alerts       List code scanning alerts
  code-alert        View a code scanning alert
  dependabot-alerts List Dependabot alerts
  dependabot-alert  View a Dependabot alert
  secret-alerts     List secret scanning alerts
  secret-alert      View a secret scanning alert

Common Options:
  --owner OWNER     Repository owner
  --repo REPO       Repository name
  --number NUMBER   Alert number
  --state STATE     Filter by state (open, closed, all)
  --severity LEVEL  Filter by severity (critical, high, medium, low)
  --ref REF         Git reference for code scanning
  --limit N         Maximum results (default: 30)
  --json            Output in JSON format
  --help            Show this help message

Examples:
  $(basename "$0") code-alerts --owner facebook --repo react --state open
  $(basename "$0") dependabot-alerts --owner cli --repo cli --severity high
  $(basename "$0") secret-alerts --owner myorg --repo myrepo
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
success() { echo -e "${GREEN}$1${NC}"; }
info() { echo -e "${BLUE}$1${NC}"; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --owner) OWNER="$2"; shift 2 ;;
            --repo) REPO="$2"; shift 2 ;;
            --number) NUMBER="$2"; shift 2 ;;
            --state) STATE="$2"; shift 2 ;;
            --severity) SEVERITY="$2"; shift 2 ;;
            --ref) REF="$2"; shift 2 ;;
            --tool) TOOL="$2"; shift 2 ;;
            --limit) LIMIT="$2"; shift 2 ;;
            --json) JSON_OUTPUT=true; shift ;;
            --help) usage ;;
            *) shift ;;
        esac
    done
}

# Action: List code scanning alerts
action_code_alerts() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing code scanning alerts for $OWNER/$REPO (state: $STATE)"
    
    local url="repos/$OWNER/$REPO/code-scanning/alerts?state=$STATE&per_page=$LIMIT"
    [[ -n "${REF:-}" ]] && url="$url&ref=$REF"
    [[ -n "${SEVERITY:-}" ]] && url="$url&severity=$SEVERITY"
    [[ -n "${TOOL:-}" ]] && url="$url&tool_name=$TOOL"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "$url"
    else
        gh api "$url" --jq '.[] | "#\(.number)\t\(.state)\t\(.rule.severity)\t\(.rule.id)\t\(.most_recent_instance.location.path // "-")"' 2>/dev/null | column -t -s $'\t' || \
            echo "No code scanning alerts found or code scanning is not enabled."
    fi
}

# Action: View code scanning alert
action_code_alert() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching code scanning alert #$NUMBER"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/code-scanning/alerts/$NUMBER"
    else
        gh api "repos/$OWNER/$REPO/code-scanning/alerts/$NUMBER" --jq '{
            number: .number,
            state: .state,
            rule_id: .rule.id,
            rule_description: .rule.description,
            severity: .rule.severity,
            tool: .tool.name,
            file: .most_recent_instance.location.path,
            line: .most_recent_instance.location.start_line,
            created_at: .created_at
        }'
    fi
}

# Action: List Dependabot alerts
action_dependabot_alerts() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing Dependabot alerts for $OWNER/$REPO (state: $STATE)"
    
    local url="repos/$OWNER/$REPO/dependabot/alerts?state=$STATE&per_page=$LIMIT"
    [[ -n "${SEVERITY:-}" ]] && url="$url&severity=$SEVERITY"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "$url"
    else
        gh api "$url" --jq '.[] | "#\(.number)\t\(.state)\t\(.security_vulnerability.severity)\t\(.dependency.package.name)\t\(.security_vulnerability.vulnerable_version_range)"' 2>/dev/null | column -t -s $'\t' || \
            echo "No Dependabot alerts found or Dependabot is not enabled."
    fi
}

# Action: View Dependabot alert
action_dependabot_alert() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching Dependabot alert #$NUMBER"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/dependabot/alerts/$NUMBER"
    else
        gh api "repos/$OWNER/$REPO/dependabot/alerts/$NUMBER" --jq '{
            number: .number,
            state: .state,
            package: .dependency.package.name,
            ecosystem: .dependency.package.ecosystem,
            severity: .security_vulnerability.severity,
            vulnerable_range: .security_vulnerability.vulnerable_version_range,
            patched_version: .security_vulnerability.first_patched_version.identifier,
            cve: .security_advisory.cve_id,
            ghsa: .security_advisory.ghsa_id,
            summary: .security_advisory.summary
        }'
    fi
}

# Action: List secret scanning alerts
action_secret_alerts() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    
    info "Listing secret scanning alerts for $OWNER/$REPO (state: $STATE)"
    
    local url="repos/$OWNER/$REPO/secret-scanning/alerts?state=$STATE&per_page=$LIMIT"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "$url"
    else
        gh api "$url" --jq '.[] | "#\(.number)\t\(.state)\t\(.secret_type_display_name)\t\(.created_at[0:10])"' 2>/dev/null | column -t -s $'\t' || \
            echo "No secret scanning alerts found or secret scanning is not enabled."
    fi
}

# Action: View secret scanning alert
action_secret_alert() {
    [[ -z "${OWNER:-}" ]] && error "Missing --owner"
    [[ -z "${REPO:-}" ]] && error "Missing --repo"
    [[ -z "${NUMBER:-}" ]] && error "Missing --number"
    
    info "Fetching secret scanning alert #$NUMBER"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        gh api "repos/$OWNER/$REPO/secret-scanning/alerts/$NUMBER"
    else
        gh api "repos/$OWNER/$REPO/secret-scanning/alerts/$NUMBER" --jq '{
            number: .number,
            state: .state,
            secret_type: .secret_type_display_name,
            resolution: .resolution,
            resolved_by: .resolved_by.login,
            created_at: .created_at,
            resolved_at: .resolved_at
        }'
    fi
}

main() {
    [[ $# -eq 0 ]] && usage
    local action="$1"; shift
    parse_args "$@"
    
    case "$action" in
        code-alerts) action_code_alerts ;;
        code-alert) action_code_alert ;;
        dependabot-alerts) action_dependabot_alerts ;;
        dependabot-alert) action_dependabot_alert ;;
        secret-alerts) action_secret_alerts ;;
        secret-alert) action_secret_alert ;;
        --help|-h) usage ;;
        *) error "Unknown action: $action" ;;
    esac
}

main "$@"
