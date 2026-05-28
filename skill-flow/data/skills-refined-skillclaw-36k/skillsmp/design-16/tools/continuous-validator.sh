#!/bin/bash
#
# continuous-validator.sh - Background validation service
#
# Usage: ./tools/continuous-validator.sh start|stop|status [options]
#
# Commands:
#   start     Start the validation service
#   stop      Stop the validation service
#   status    Show service status
#   validate  Run single validation
#
# Features:
#   - Runs as background process
#   - Monitors multiple spec files
#   - Writes results to shared location
#   - Supports webhook notifications
#   - Integrates with validation dashboard

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$SCRIPT_DIR")"
AGENTS_DIR="$DESIGN_OPS_ROOT/agents"
CONFIG_DIR="$DESIGN_OPS_ROOT/config"

# Service configuration
SERVICE_NAME="design-ops-validator"
PID_FILE="/tmp/${SERVICE_NAME}.pid"
LOG_FILE="/tmp/${SERVICE_NAME}.log"
STATE_FILE="/tmp/${SERVICE_NAME}.state"
RESULTS_DIR="/tmp/${SERVICE_NAME}-results"

# Defaults
COMMAND=""
SPEC_FILES=()
DOMAIN="general"
INTERVAL=30
WEBHOOK_URL=""
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        start|stop|status|validate)
            COMMAND="$1"
            shift
            ;;
        --spec)
            SPEC_FILES+=("$2")
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --interval)
            INTERVAL="$2"
            shift 2
            ;;
        --webhook)
            WEBHOOK_URL="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            cat << 'EOF'
Continuous Validator Service

Usage: ./tools/continuous-validator.sh <command> [options]

Commands:
  start       Start the background validation service
  stop        Stop the validation service
  status      Show service status and recent results
  validate    Run a single validation pass

Options:
  --spec <file>      Spec file(s) to monitor (can specify multiple)
  --domain <domain>  Validation domain (default: general)
  --interval <sec>   Validation interval in seconds (default: 30)
  --webhook <url>    Webhook URL for notifications
  --verbose, -v      Show detailed output

Examples:
  # Start monitoring a spec
  ./tools/continuous-validator.sh start --spec spec.md --domain api

  # Monitor multiple specs
  ./tools/continuous-validator.sh start --spec api-spec.md --spec db-spec.md

  # Check status
  ./tools/continuous-validator.sh status

  # Stop the service
  ./tools/continuous-validator.sh stop
EOF
            exit 0
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
        *)
            # Assume it's a spec file
            SPEC_FILES+=("$1")
            shift
            ;;
    esac
done

# ============================================================================
# Helper Functions
# ============================================================================

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" >> "$LOG_FILE"
    [[ "$VERBOSE" == "true" ]] && echo -e "${BLUE}[$timestamp]${NC} $1"
}

is_running() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

get_pid() {
    if [[ -f "$PID_FILE" ]]; then
        cat "$PID_FILE"
    fi
}

send_webhook() {
    local event=$1
    local data=$2

    if [[ -n "$WEBHOOK_URL" ]]; then
        curl -s -X POST "$WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{\"event\": \"$event\", \"data\": $data}" \
            > /dev/null 2>&1 || true
    fi
}

run_validation_pass() {
    local spec=$1
    local domain=$2
    local output_dir=$3

    local spec_name=$(basename "$spec" | sed 's/\.[^.]*$//')
    local result_file="$output_dir/${spec_name}.json"

    # Run validator
    bash "$AGENTS_DIR/validator.sh" "$spec" \
        --domain "$domain" \
        --output "$output_dir" \
        > /dev/null 2>&1

    local exit_code=$?

    # Rename output to spec-specific name
    if [[ -f "$output_dir/validation.json" ]]; then
        mv "$output_dir/validation.json" "$result_file"
    fi

    # Update state
    local confidence=$(jq -r '.confidence_score // 0' "$result_file" 2>/dev/null || echo "0")
    local critical=$(jq -r '.summary.critical // 0' "$result_file" 2>/dev/null || echo "0")

    echo "{\"spec\": \"$spec\", \"confidence\": $confidence, \"critical\": $critical, \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$output_dir/${spec_name}.state"

    return $exit_code
}

# ============================================================================
# Commands
# ============================================================================

cmd_start() {
    if is_running; then
        echo -e "${YELLOW}Service is already running (PID: $(get_pid))${NC}"
        exit 1
    fi

    if [[ ${#SPEC_FILES[@]} -eq 0 ]]; then
        echo -e "${RED}Error: At least one spec file required (--spec)${NC}"
        exit 1
    fi

    # Verify spec files exist
    for spec in "${SPEC_FILES[@]}"; do
        if [[ ! -f "$spec" ]]; then
            echo -e "${RED}Error: Spec file not found: $spec${NC}"
            exit 1
        fi
    done

    # Create directories
    mkdir -p "$RESULTS_DIR"

    echo -e "${CYAN}Starting continuous validator...${NC}"
    echo -e "  Specs:    ${SPEC_FILES[*]}"
    echo -e "  Domain:   $DOMAIN"
    echo -e "  Interval: ${INTERVAL}s"

    # Start background process
    (
        log "Service started"
        log "Monitoring: ${SPEC_FILES[*]}"
        log "Domain: $DOMAIN"
        log "Interval: ${INTERVAL}s"

        while true; do
            for spec in "${SPEC_FILES[@]}"; do
                if [[ -f "$spec" ]]; then
                    log "Validating: $spec"
                    run_validation_pass "$spec" "$DOMAIN" "$RESULTS_DIR"

                    # Check for alerts
                    local spec_name=$(basename "$spec" | sed 's/\.[^.]*$//')
                    local result_file="$RESULTS_DIR/${spec_name}.json"

                    if [[ -f "$result_file" ]]; then
                        local critical=$(jq -r '.summary.critical // 0' "$result_file")
                        if [[ $critical -gt 0 ]]; then
                            log "ALERT: $spec has $critical critical violations"
                            send_webhook "critical_violation" "{\"spec\": \"$spec\", \"count\": $critical}"
                        fi
                    fi
                else
                    log "WARNING: Spec file not found: $spec"
                fi
            done

            sleep "$INTERVAL"
        done
    ) >> "$LOG_FILE" 2>&1 &

    local pid=$!
    echo "$pid" > "$PID_FILE"

    # Save configuration to state file
    cat > "$STATE_FILE" << EOF
{
  "pid": $pid,
  "started": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "domain": "$DOMAIN",
  "interval": $INTERVAL,
  "specs": $(printf '%s\n' "${SPEC_FILES[@]}" | jq -R . | jq -s .)
}
EOF

    echo -e "${GREEN}Service started (PID: $pid)${NC}"
    echo -e "  Log:     $LOG_FILE"
    echo -e "  Results: $RESULTS_DIR"
}

cmd_stop() {
    if ! is_running; then
        echo -e "${YELLOW}Service is not running${NC}"
        exit 0
    fi

    local pid=$(get_pid)
    echo -e "${CYAN}Stopping service (PID: $pid)...${NC}"

    kill "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"

    log "Service stopped"
    echo -e "${GREEN}Service stopped${NC}"
}

cmd_status() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  CONTINUOUS VALIDATOR STATUS${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    if is_running; then
        local pid=$(get_pid)
        echo -e "${GREEN}Status: RUNNING${NC} (PID: $pid)"

        if [[ -f "$STATE_FILE" ]]; then
            local started=$(jq -r '.started' "$STATE_FILE")
            local domain=$(jq -r '.domain' "$STATE_FILE")
            local interval=$(jq -r '.interval' "$STATE_FILE")

            echo -e "Started: $started"
            echo -e "Domain:  $domain"
            echo -e "Interval: ${interval}s"
        fi
    else
        echo -e "${RED}Status: STOPPED${NC}"
    fi

    echo ""

    # Show recent results
    if [[ -d "$RESULTS_DIR" ]] && ls "$RESULTS_DIR"/*.json >/dev/null 2>&1; then
        echo -e "${BLUE}Recent Validation Results:${NC}"
        echo ""

        for result_file in "$RESULTS_DIR"/*.json; do
            local spec_name=$(basename "$result_file" .json)
            local confidence=$(jq -r '.confidence_score // "N/A"' "$result_file")
            local critical=$(jq -r '.summary.critical // 0' "$result_file")
            local major=$(jq -r '.summary.major // 0' "$result_file")
            local timestamp=$(jq -r '.timestamp // "N/A"' "$result_file")

            # Color based on confidence
            local conf_color=$GREEN
            [[ $confidence -lt 80 ]] && conf_color=$YELLOW
            [[ $confidence -lt 60 ]] && conf_color=$RED

            echo -e "  ${BLUE}$spec_name${NC}"
            echo -e "    Confidence: ${conf_color}${confidence}%${NC}"

            if [[ $critical -gt 0 ]]; then
                echo -e "    Critical:   ${RED}$critical${NC}"
            fi

            if [[ $major -gt 0 ]]; then
                echo -e "    Major:      ${YELLOW}$major${NC}"
            fi

            echo -e "    Updated:    $timestamp"
            echo ""
        done
    else
        echo -e "${YELLOW}No validation results found${NC}"
    fi

    # Show log tail
    if [[ -f "$LOG_FILE" ]]; then
        echo -e "${BLUE}Recent Log Entries:${NC}"
        tail -5 "$LOG_FILE" | while read -r line; do
            echo -e "  ${DIM}$line${NC}"
        done
    fi
}

cmd_validate() {
    if [[ ${#SPEC_FILES[@]} -eq 0 ]]; then
        echo -e "${RED}Error: At least one spec file required (--spec)${NC}"
        exit 1
    fi

    mkdir -p "$RESULTS_DIR"

    echo -e "${CYAN}Running single validation pass...${NC}"

    for spec in "${SPEC_FILES[@]}"; do
        if [[ -f "$spec" ]]; then
            echo -e "  Validating: $spec"
            run_validation_pass "$spec" "$DOMAIN" "$RESULTS_DIR"

            local spec_name=$(basename "$spec" | sed 's/\.[^.]*$//')
            local result_file="$RESULTS_DIR/${spec_name}.json"

            if [[ -f "$result_file" ]]; then
                local confidence=$(jq -r '.confidence_score' "$result_file")
                echo -e "    Confidence: $confidence%"
            fi
        else
            echo -e "${RED}  Spec file not found: $spec${NC}"
        fi
    done

    echo -e "${GREEN}Validation complete${NC}"
    echo -e "Results: $RESULTS_DIR"
}

# ============================================================================
# Main
# ============================================================================

case $COMMAND in
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    status)
        cmd_status
        ;;
    validate)
        cmd_validate
        ;;
    *)
        echo -e "${RED}Error: Command required (start|stop|status|validate)${NC}"
        echo "Run with --help for usage"
        exit 1
        ;;
esac
