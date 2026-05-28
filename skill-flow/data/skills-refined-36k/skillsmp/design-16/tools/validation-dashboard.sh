#!/bin/bash
#
# validation-dashboard.sh - Real-time validation dashboard
#
# Usage: ./tools/validation-dashboard.sh [--results-dir <dir>] [--refresh <seconds>]
#
# Features:
#   - Terminal-based dashboard
#   - Shows all spec validation statuses
#   - Displays confidence trends
#   - Highlights critical issues
#   - Auto-refreshes

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
DIM='\033[2m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
RESULTS_DIR="/tmp/design-ops-validator-results"
REFRESH=5
ONCE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --results-dir)
            RESULTS_DIR="$2"
            shift 2
            ;;
        --refresh)
            REFRESH="$2"
            shift 2
            ;;
        --once)
            ONCE=true
            shift
            ;;
        --help|-h)
            cat << 'EOF'
Validation Dashboard

Usage: ./tools/validation-dashboard.sh [options]

Options:
  --results-dir <dir>   Directory containing validation results
                        (default: /tmp/design-ops-validator-results)
  --refresh <seconds>   Refresh interval (default: 5)
  --once                Display once and exit

The dashboard shows:
  - Overall system health
  - Per-spec validation status
  - Confidence scores with trends
  - Critical/major violation counts
  - Last update timestamps

Press Ctrl+C to exit.
EOF
            exit 0
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
        *)
            RESULTS_DIR="$1"
            shift
            ;;
    esac
done

# Cleanup on exit
cleanup() {
    tput cnorm  # Show cursor
    echo ""
    exit 0
}
trap cleanup SIGINT SIGTERM

# ============================================================================
# Helper Functions
# ============================================================================

draw_box() {
    local width=$1
    local title=$2

    printf "${CYAN}╔"
    printf '═%.0s' $(seq 1 $((width - 2)))
    printf "╗${NC}\n"

    printf "${CYAN}║${NC} ${BOLD}%-$((width - 4))s${NC} ${CYAN}║${NC}\n" "$title"

    printf "${CYAN}╠"
    printf '═%.0s' $(seq 1 $((width - 2)))
    printf "╣${NC}\n"
}

draw_box_bottom() {
    local width=$1

    printf "${CYAN}╚"
    printf '═%.0s' $(seq 1 $((width - 2)))
    printf "╝${NC}\n"
}

draw_row() {
    local width=$1
    shift
    local content="$*"

    printf "${CYAN}║${NC} %-$((width - 4))s ${CYAN}║${NC}\n" "$content"
}

confidence_bar() {
    local score=$1
    local width=20
    local filled=$((score * width / 100))
    local empty=$((width - filled))

    local color=$GREEN
    [[ $score -lt 80 ]] && color=$YELLOW
    [[ $score -lt 60 ]] && color=$RED

    printf "${color}"
    printf '█%.0s' $(seq 1 $filled) 2>/dev/null || true
    printf "${DIM}"
    printf '░%.0s' $(seq 1 $empty) 2>/dev/null || true
    printf "${NC}"
}

format_timestamp() {
    local ts=$1
    # Extract just time portion
    echo "$ts" | grep -oE '[0-9]{2}:[0-9]{2}:[0-9]{2}' | head -1 || echo "N/A"
}

# ============================================================================
# Dashboard Display
# ============================================================================

display_dashboard() {
    local term_width=$(tput cols 2>/dev/null || echo 80)
    local box_width=$((term_width - 2))
    [[ $box_width -gt 100 ]] && box_width=100

    # Clear screen and hide cursor
    clear
    tput civis

    # Header
    echo ""
    printf "${MAGENTA}"
    printf "  ╔═══════════════════════════════════════════════════════════════╗\n"
    printf "  ║           DESIGN OPS VALIDATION DASHBOARD                     ║\n"
    printf "  ╚═══════════════════════════════════════════════════════════════╝${NC}\n"
    echo ""

    # Check if results directory exists
    if [[ ! -d "$RESULTS_DIR" ]]; then
        echo -e "  ${YELLOW}No results directory found: $RESULTS_DIR${NC}"
        echo ""
        echo -e "  ${DIM}Start the continuous validator to generate results:${NC}"
        echo -e "  ${CYAN}./tools/continuous-validator.sh start --spec <file> --domain <domain>${NC}"
        return
    fi

    # Collect results
    local total_specs=0
    local healthy_specs=0
    local warning_specs=0
    local critical_specs=0
    local total_confidence=0

    declare -a spec_data

    shopt -s nullglob
    for result_file in "$RESULTS_DIR"/*.json; do
        [[ -f "$result_file" ]] || continue

        local spec_name=$(basename "$result_file" .json)
        local confidence=$(jq -r '.confidence_score // 0' "$result_file")
        local critical=$(jq -r '.summary.critical // 0' "$result_file")
        local major=$(jq -r '.summary.major // 0' "$result_file")
        local warnings=$(jq -r '.summary.warnings // 0' "$result_file")
        local timestamp=$(jq -r '.timestamp // "N/A"' "$result_file")

        ((total_specs++))
        total_confidence=$((total_confidence + confidence))

        if [[ $critical -gt 0 ]]; then
            ((critical_specs++))
        elif [[ $confidence -lt 60 ]]; then
            ((warning_specs++))
        else
            ((healthy_specs++))
        fi

        spec_data+=("$spec_name|$confidence|$critical|$major|$warnings|$timestamp")
    done

    # Calculate average confidence
    local avg_confidence=0
    if [[ $total_specs -gt 0 ]]; then
        avg_confidence=$((total_confidence / total_specs))
    fi

    # System Health Summary
    draw_box $box_width "SYSTEM HEALTH"

    local health_status="${GREEN}HEALTHY${NC}"
    if [[ $critical_specs -gt 0 ]]; then
        health_status="${RED}CRITICAL${NC}"
    elif [[ $warning_specs -gt 0 ]]; then
        health_status="${YELLOW}WARNING${NC}"
    fi

    draw_row $box_width "Status: $health_status"
    draw_row $box_width "Specs Monitored: $total_specs"
    draw_row $box_width "Average Confidence: $avg_confidence%"
    draw_row $box_width ""

    # Health breakdown bar
    local bar_width=$((box_width - 20))
    local healthy_width=$((healthy_specs * bar_width / (total_specs > 0 ? total_specs : 1)))
    local warning_width=$((warning_specs * bar_width / (total_specs > 0 ? total_specs : 1)))
    local critical_width=$((critical_specs * bar_width / (total_specs > 0 ? total_specs : 1)))

    printf "${CYAN}║${NC}   "
    printf "${GREEN}"
    printf '█%.0s' $(seq 1 $healthy_width) 2>/dev/null || true
    printf "${YELLOW}"
    printf '█%.0s' $(seq 1 $warning_width) 2>/dev/null || true
    printf "${RED}"
    printf '█%.0s' $(seq 1 $critical_width) 2>/dev/null || true
    printf "${NC}"
    printf "%*s${CYAN}║${NC}\n" $((box_width - 5 - healthy_width - warning_width - critical_width)) ""

    draw_row $box_width "  ${GREEN}■${NC} Healthy: $healthy_specs  ${YELLOW}■${NC} Warning: $warning_specs  ${RED}■${NC} Critical: $critical_specs"

    draw_box_bottom $box_width
    echo ""

    # Per-Spec Details
    if [[ $total_specs -gt 0 ]]; then
        draw_box $box_width "SPEC VALIDATION STATUS"

        # Header row
        printf "${CYAN}║${NC}  ${DIM}%-20s  %-24s  %5s  %5s  %8s${NC}  ${CYAN}║${NC}\n" \
            "SPEC" "CONFIDENCE" "CRIT" "MAJOR" "UPDATED"

        draw_row $box_width "$(printf '─%.0s' $(seq 1 $((box_width - 6))))"

        for data in "${spec_data[@]}"; do
            IFS='|' read -r spec_name confidence critical major warnings timestamp <<< "$data"

            # Status indicator
            local status_icon="${GREEN}●${NC}"
            if [[ $critical -gt 0 ]]; then
                status_icon="${RED}●${NC}"
            elif [[ $confidence -lt 60 ]]; then
                status_icon="${YELLOW}●${NC}"
            fi

            # Format critical/major with color
            local crit_display="${DIM}0${NC}"
            [[ $critical -gt 0 ]] && crit_display="${RED}$critical${NC}"

            local major_display="${DIM}0${NC}"
            [[ $major -gt 0 ]] && major_display="${YELLOW}$major${NC}"

            local time_display=$(format_timestamp "$timestamp")

            printf "${CYAN}║${NC}  $status_icon %-18s  " "$spec_name"
            confidence_bar "$confidence"
            printf " %3d%%  " "$confidence"
            printf "%-5s  %-5s  %8s  ${CYAN}║${NC}\n" \
                "$critical" "$major" "$time_display"
        done

        draw_box_bottom $box_width
    fi

    echo ""

    # Footer
    printf "  ${DIM}Last refresh: $(date '+%H:%M:%S')  |  "
    printf "Refresh interval: ${REFRESH}s  |  "
    printf "Press Ctrl+C to exit${NC}\n"
}

# ============================================================================
# Main Loop
# ============================================================================

if [[ "$ONCE" == "true" ]]; then
    display_dashboard
    tput cnorm  # Show cursor
    exit 0
fi

while true; do
    display_dashboard
    sleep "$REFRESH"
done
