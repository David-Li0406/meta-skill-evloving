#!/bin/bash
#
# fetch-errors.sh
#
# Fetches error logs from Google Cloud Logging for Cloud Functions.
# Outputs JSON format for further analysis.
#
# Usage:
#   ./fetch-errors.sh --project=PROJECT_ID [OPTIONS]
#
# Required:
#   --project=PROJECT_ID    GCP project ID
#
# Optional:
#   --function=NAME         Specific Cloud Function name
#   --hours=24              Time range in hours (default: 24)
#   --severity=ERROR        Log severity level (ERROR, WARNING, CRITICAL)
#   --limit=100             Maximum number of log entries (default: 100)
#   --output=FILE           Output file path (default: /tmp/gcp-errors.json)
#
# Exit codes:
#   0 - Success
#   1 - Error (missing args, auth failure, etc.)

set -uo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

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

# Default values
PROJECT=""
FUNCTION=""
HOURS=24
SEVERITY="ERROR"
LIMIT=100
OUTPUT="/tmp/gcp-errors.json"

# Parse arguments
parse_args() {
    for arg in "$@"; do
        case $arg in
            --project=*)
                PROJECT="${arg#*=}"
                ;;
            --function=*)
                FUNCTION="${arg#*=}"
                ;;
            --hours=*)
                HOURS="${arg#*=}"
                ;;
            --severity=*)
                SEVERITY="${arg#*=}"
                ;;
            --limit=*)
                LIMIT="${arg#*=}"
                ;;
            --output=*)
                OUTPUT="${arg#*=}"
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown argument: $arg"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat << 'EOF'
Usage: fetch-errors.sh --project=PROJECT_ID [OPTIONS]

Fetches error logs from Google Cloud Logging for Cloud Functions.

Required:
  --project=PROJECT_ID    GCP project ID

Optional:
  --function=NAME         Specific Cloud Function name
  --hours=24              Time range in hours (default: 24)
  --severity=ERROR        Log severity level (ERROR, WARNING, CRITICAL)
  --limit=100             Maximum number of log entries (default: 100)
  --output=FILE           Output file path (default: /tmp/gcp-errors.json)

Examples:
  # Get all errors from last 24 hours
  ./fetch-errors.sh --project=my-project

  # Get errors for specific function
  ./fetch-errors.sh --project=my-project --function=processPayment

  # Get critical errors from last hour
  ./fetch-errors.sh --project=my-project --hours=1 --severity=CRITICAL

  # Get last 500 errors and save to custom file
  ./fetch-errors.sh --project=my-project --limit=500 --output=errors.json
EOF
}

# Check gcloud CLI is installed and authenticated
check_gcloud() {
    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI is not installed"
        log_info "Install from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi

    # Check authentication
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | head -1 | grep -q "@"; then
        log_error "gcloud CLI is not authenticated"
        log_info "Run: gcloud auth login"
        exit 1
    fi

    log_info "gcloud CLI authenticated"
}

# Validate project exists
validate_project() {
    if [ -z "$PROJECT" ]; then
        log_error "Project ID is required"
        log_info "Usage: ./fetch-errors.sh --project=PROJECT_ID [OPTIONS]"
        exit 1
    fi

    # Check if project is accessible
    if ! gcloud projects describe "$PROJECT" &>/dev/null; then
        log_error "Cannot access project: $PROJECT"
        log_info "Check project ID and permissions"
        exit 1
    fi

    log_info "Project validated: $PROJECT"
}

# Build the Cloud Logging filter
build_filter() {
    local filter=""

    # Base filter for Cloud Functions
    filter="resource.type=\"cloud_run_revision\""

    # Add severity filter
    case "$SEVERITY" in
        CRITICAL)
            filter="$filter AND severity>=CRITICAL"
            ;;
        ERROR)
            filter="$filter AND severity>=ERROR"
            ;;
        WARNING)
            filter="$filter AND severity>=WARNING"
            ;;
        *)
            log_warn "Unknown severity: $SEVERITY, using ERROR"
            filter="$filter AND severity>=ERROR"
            ;;
    esac

    # Add function name filter if specified
    if [ -n "$FUNCTION" ]; then
        filter="$filter AND resource.labels.service_name=\"$FUNCTION\""
    fi

    # Add time filter
    local start_time
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        start_time=$(date -v-"${HOURS}"H -u +"%Y-%m-%dT%H:%M:%SZ")
    else
        # Linux
        start_time=$(date -u -d "$HOURS hours ago" +"%Y-%m-%dT%H:%M:%SZ")
    fi
    filter="$filter AND timestamp>=\"$start_time\""

    echo "$filter"
}

# Fetch logs from Cloud Logging
fetch_logs() {
    local filter
    filter=$(build_filter)

    log_info "Fetching logs with filter:"
    log_info "  $filter"
    log_info "Limit: $LIMIT entries"
    echo ""

    # Execute gcloud logging read
    local result
    result=$(gcloud logging read "$filter" \
        --project="$PROJECT" \
        --limit="$LIMIT" \
        --format="json" \
        2>&1)

    local exit_code=$?

    if [ $exit_code -ne 0 ]; then
        log_error "Failed to fetch logs"
        log_error "$result"
        exit 1
    fi

    # Check if any logs were returned
    if [ "$result" = "[]" ] || [ -z "$result" ]; then
        log_warn "No logs found matching the filter"
        echo "[]" > "$OUTPUT"
        log_info "Empty result saved to: $OUTPUT"
        exit 0
    fi

    # Save to output file
    echo "$result" > "$OUTPUT"

    # Count entries
    local count
    count=$(echo "$result" | grep -c '"insertId"' || echo "0")

    log_success "Fetched $count log entries"
    log_info "Output saved to: $OUTPUT"
}

# Main
main() {
    parse_args "$@"

    log_info "GCP Error Logs Fetcher"
    echo ""

    check_gcloud
    validate_project

    echo ""
    log_info "Parameters:"
    log_info "  Project:  $PROJECT"
    log_info "  Function: ${FUNCTION:-<all functions>}"
    log_info "  Hours:    $HOURS"
    log_info "  Severity: $SEVERITY"
    log_info "  Limit:    $LIMIT"
    log_info "  Output:   $OUTPUT"
    echo ""

    fetch_logs
}

main "$@"
