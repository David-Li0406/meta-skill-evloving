#!/bin/bash
#
# watch-mode.sh - Watch spec files for changes and run continuous validation
#
# Usage: ./tools/watch-mode.sh --spec <file> --domain <domain> [--interval <seconds>]
#
# Features:
#   - Monitors spec file for changes
#   - Runs validator on each change
#   - Displays real-time confidence score
#   - Shows violation/warning counts
#   - Triggers full analysis when significant changes detected

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
DIM='\033[2m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$SCRIPT_DIR")"
AGENTS_DIR="$DESIGN_OPS_ROOT/agents"
CONFIG_DIR="$DESIGN_OPS_ROOT/config"

# Defaults
SPEC_FILE=""
DOMAIN="general"
INTERVAL=2
OUTPUT_DIR="/tmp/design-ops-watch"
QUIET=false
ONCE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --spec)
            SPEC_FILE="$2"
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
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --quiet|-q)
            QUIET=true
            shift
            ;;
        --once)
            ONCE=true
            shift
            ;;
        --help|-h)
            cat << 'EOF'
Watch Mode - Continuous Spec Validation

Usage: ./tools/watch-mode.sh --spec <file> --domain <domain> [options]

Options:
  --spec <file>       Spec file to watch (required)
  --domain <domain>   Validation domain (api, database, security, etc.)
  --interval <sec>    Check interval in seconds (default: 2)
  --output <dir>      Output directory for validation results
  --quiet, -q         Minimal output
  --once              Run once and exit (no watching)

Controls:
  Ctrl+C              Stop watching

Output:
  Real-time display of:
  - Confidence score with trend indicator
  - Violation and warning counts
  - Last check timestamp
  - File modification status
EOF
            exit 0
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
        *)
            SPEC_FILE="$1"
            shift
            ;;
    esac
done

# Validate inputs
if [[ -z "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Spec file required (--spec)${NC}"
    exit 1
fi

if [[ ! -f "$SPEC_FILE" ]]; then
    echo -e "${RED}Error: Spec file not found: $SPEC_FILE${NC}"
    exit 1
fi

# Setup
mkdir -p "$OUTPUT_DIR"
VALIDATION_FILE="$OUTPUT_DIR/validation.json"
LAST_HASH=""
LAST_CONFIDENCE=0
CHECK_COUNT=0

# Cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}Watch mode stopped${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM

# ============================================================================
# Helper Functions
# ============================================================================

get_file_hash() {
    if command -v md5sum &> /dev/null; then
        md5sum "$1" | cut -d' ' -f1
    elif command -v md5 &> /dev/null; then
        md5 -q "$1"
    else
        # Fallback to modification time
        stat -f%m "$1" 2>/dev/null || stat -c%Y "$1"
    fi
}

format_confidence() {
    local score=$1
    local prev=$2
    local color
    local trend

    if [[ $score -ge 80 ]]; then
        color=$GREEN
    elif [[ $score -ge 60 ]]; then
        color=$YELLOW
    else
        color=$RED
    fi

    if [[ $score -gt $prev ]]; then
        trend="↑"
    elif [[ $score -lt $prev ]]; then
        trend="↓"
    else
        trend="─"
    fi

    echo -e "${color}${score}%${NC} ${DIM}${trend}${NC}"
}

run_validation() {
    local spec=$1
    local domain=$2
    local output=$3

    # Run validator silently
    bash "$AGENTS_DIR/validator.sh" "$spec" \
        --domain "$domain" \
        --output "$output" \
        > /dev/null 2>&1 || true
}

display_status() {
    local confidence=$1
    local prev_confidence=$2
    local critical=$3
    local major=$4
    local warnings=$5
    local modified=$6

    # Clear previous line and print status
    if [[ "$QUIET" != "true" ]]; then
        printf "\r\033[K"  # Clear line
        printf "${CYAN}[%s]${NC} " "$(date +%H:%M:%S)"
        printf "Confidence: %s " "$(format_confidence "$confidence" "$prev_confidence")"
        printf "${DIM}|${NC} "

        if [[ $critical -gt 0 ]]; then
            printf "${RED}Critical: %d${NC} " "$critical"
        fi

        if [[ $major -gt 0 ]]; then
            printf "${YELLOW}Major: %d${NC} " "$major"
        fi

        if [[ $warnings -gt 0 ]]; then
            printf "${DIM}Warnings: %d${NC} " "$warnings"
        fi

        if [[ "$modified" == "true" ]]; then
            printf "${GREEN}(updated)${NC}"
        fi
    fi
}

# ============================================================================
# Main Watch Loop
# ============================================================================

echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                    WATCH MODE - LIVE VALIDATION               ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Watching:${NC} $SPEC_FILE"
echo -e "${BLUE}Domain:${NC}   $DOMAIN"
echo -e "${BLUE}Interval:${NC} ${INTERVAL}s"
echo ""
echo -e "${DIM}Press Ctrl+C to stop${NC}"
echo ""

# Initial validation
echo -e "${YELLOW}Running initial validation...${NC}"
run_validation "$SPEC_FILE" "$DOMAIN" "$OUTPUT_DIR"

if [[ -f "$VALIDATION_FILE" ]]; then
    LAST_CONFIDENCE=$(jq -r '.confidence_score' "$VALIDATION_FILE")
    LAST_HASH=$(get_file_hash "$SPEC_FILE")

    CRITICAL=$(jq -r '.summary.critical' "$VALIDATION_FILE")
    MAJOR=$(jq -r '.summary.major' "$VALIDATION_FILE")
    WARNINGS=$(jq -r '.summary.warnings' "$VALIDATION_FILE")

    echo ""
    display_status "$LAST_CONFIDENCE" "$LAST_CONFIDENCE" "$CRITICAL" "$MAJOR" "$WARNINGS" "false"
    echo ""
fi

# Exit if --once
if [[ "$ONCE" == "true" ]]; then
    echo ""
    echo -e "${GREEN}Single validation complete${NC}"

    if [[ -f "$VALIDATION_FILE" ]]; then
        echo ""
        echo -e "${BLUE}Results:${NC}"
        echo -e "  Confidence: ${LAST_CONFIDENCE}%"
        echo -e "  Critical:   $CRITICAL"
        echo -e "  Major:      $MAJOR"
        echo -e "  Warnings:   $WARNINGS"
        echo ""
        echo -e "${BLUE}Output:${NC} $VALIDATION_FILE"
    fi

    exit 0
fi

# Watch loop
echo -e "${CYAN}Monitoring for changes...${NC}"
echo ""

while true; do
    sleep "$INTERVAL"

    CURRENT_HASH=$(get_file_hash "$SPEC_FILE")

    if [[ "$CURRENT_HASH" != "$LAST_HASH" ]]; then
        # File changed - run validation
        ((CHECK_COUNT++))

        run_validation "$SPEC_FILE" "$DOMAIN" "$OUTPUT_DIR"

        if [[ -f "$VALIDATION_FILE" ]]; then
            PREV_CONFIDENCE=$LAST_CONFIDENCE
            LAST_CONFIDENCE=$(jq -r '.confidence_score' "$VALIDATION_FILE")

            CRITICAL=$(jq -r '.summary.critical' "$VALIDATION_FILE")
            MAJOR=$(jq -r '.summary.major' "$VALIDATION_FILE")
            WARNINGS=$(jq -r '.summary.warnings' "$VALIDATION_FILE")

            display_status "$LAST_CONFIDENCE" "$PREV_CONFIDENCE" "$CRITICAL" "$MAJOR" "$WARNINGS" "true"

            # Alert on significant changes
            DELTA=$((LAST_CONFIDENCE - PREV_CONFIDENCE))
            if [[ $DELTA -le -10 ]]; then
                echo ""
                echo -e "${RED}⚠ Confidence dropped by ${DELTA#-}%${NC}"
            elif [[ $DELTA -ge 10 ]]; then
                echo ""
                echo -e "${GREEN}✓ Confidence improved by ${DELTA}%${NC}"
            fi

            # Alert on critical violations
            if [[ $CRITICAL -gt 0 ]]; then
                echo ""
                echo -e "${RED}⚠ ${CRITICAL} critical violation(s) - review required${NC}"
            fi
        fi

        LAST_HASH=$CURRENT_HASH
    else
        # No change - just update timestamp
        if [[ "$QUIET" != "true" ]]; then
            printf "\r\033[K"
            printf "${DIM}[%s] Watching... (no changes)${NC}" "$(date +%H:%M:%S)"
        fi
    fi
done
