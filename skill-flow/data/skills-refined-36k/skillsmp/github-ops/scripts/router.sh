#!/usr/bin/env bash
#
# router.sh - Unified Router for GitHub Ops Skill
# Routes commands to the appropriate domain script
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: $(basename "$0") <domain> <action> [options]

GitHub Ops - Unified Router
Routes commands to specialized domain scripts.

Domains:
  repos             Repository operations (view, list, clone, fork, create, etc.)
  issues            Issue operations (list, view, create, update, close, etc.)
  prs               Pull request operations (list, view, create, merge, etc.)
  actions           GitHub Actions (workflows, runs, jobs, logs, etc.)
  releases          Release management (list, view, create, download, etc.)
  code-security     Security alerts (code scanning, dependabot, secrets)
  search            Search (repos, code, issues, prs, users, commits)
  users             User operations (me, profile, followers, repos, etc.)
  orgs              Organization operations (view, members, teams, repos)
  discussions       Discussion operations (list, view, comments, create)
  notifications     Notification management (list, thread, mark-read)
  gists             Gist operations (list, view, create, edit, delete)
  projects          GitHub Projects V2 (list, view, items, fields)

Options:
  --help            Show this help message

Examples:
  $(basename "$0") repos view --owner cli --repo cli
  $(basename "$0") issues list --owner facebook --repo react --state open
  $(basename "$0") prs create --owner myorg --repo myrepo --title "Feature" --body "Description"
  $(basename "$0") search repos --query "language:typescript stars:>10000"
  $(basename "$0") actions runs --owner cli --repo cli --limit 5

For domain-specific help:
  $(basename "$0") <domain> --help
EOF
    exit 0
}

error() { echo -e "${RED}Error: $1${NC}" >&2; exit 1; }
info() { echo -e "${BLUE}$1${NC}"; }

# Map domain to script
get_script() {
    local domain="$1"
    case "$domain" in
        repos|repository|repositories)
            echo "$SCRIPT_DIR/repos.sh" ;;
        issues|issue)
            echo "$SCRIPT_DIR/issues.sh" ;;
        prs|pr|pulls|pull-requests)
            echo "$SCRIPT_DIR/prs.sh" ;;
        actions|workflows|runs)
            echo "$SCRIPT_DIR/actions.sh" ;;
        releases|release)
            echo "$SCRIPT_DIR/releases.sh" ;;
        code-security|security|alerts)
            echo "$SCRIPT_DIR/code-security.sh" ;;
        search)
            echo "$SCRIPT_DIR/search.sh" ;;
        users|user)
            echo "$SCRIPT_DIR/users.sh" ;;
        orgs|org|organizations)
            echo "$SCRIPT_DIR/orgs.sh" ;;
        discussions|discussion)
            echo "$SCRIPT_DIR/discussions.sh" ;;
        notifications|notify)
            echo "$SCRIPT_DIR/notifications.sh" ;;
        gists|gist)
            echo "$SCRIPT_DIR/gists.sh" ;;
        projects|project)
            echo "$SCRIPT_DIR/projects.sh" ;;
        *)
            echo "" ;;
    esac
}

# List available domains
list_domains() {
    info "Available domains:"
    echo ""
    echo "  repos          - Repository operations"
    echo "  issues         - Issue management"
    echo "  prs            - Pull request operations"
    echo "  actions        - GitHub Actions & workflows"
    echo "  releases       - Release management"
    echo "  code-security  - Security scanning alerts"
    echo "  search         - Search GitHub"
    echo "  users          - User profile operations"
    echo "  orgs           - Organization operations"
    echo "  discussions    - GitHub Discussions"
    echo "  notifications  - Notification management"
    echo "  gists          - Gist operations"
    echo "  projects       - GitHub Projects V2"
    echo ""
    echo "Use '$(basename "$0") <domain> --help' for domain-specific help"
}

main() {
    [[ $# -eq 0 ]] && usage
    
    local domain="$1"
    
    # Handle help
    if [[ "$domain" == "--help" ]] || [[ "$domain" == "-h" ]]; then
        usage
    fi
    
    if [[ "$domain" == "list" ]] || [[ "$domain" == "domains" ]]; then
        list_domains
        exit 0
    fi
    
    # Get the script for this domain
    local script
    script=$(get_script "$domain")
    
    if [[ -z "$script" ]]; then
        error "Unknown domain: $domain. Use '$(basename "$0") list' to see available domains."
    fi
    
    if [[ ! -x "$script" ]]; then
        error "Script not found or not executable: $script"
    fi
    
    # Shift off the domain and pass remaining args to the script
    shift
    exec "$script" "$@"
}

main "$@"
