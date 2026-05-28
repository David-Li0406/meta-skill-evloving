#!/usr/bin/env bash
# NixOS Remote Cache Server - Performance Monitor
# Real-time monitoring of cache server performance and metrics

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
REFRESH_INTERVAL="${REFRESH_INTERVAL:-2}"
CACHE_PORT="${CACHE_PORT:-5000}"

# Clear screen and show header
show_header() {
    clear
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}     NixOS Remote Cache Server - Performance Monitor        ${BLUE}║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${CYAN}Refresh: ${REFRESH_INTERVAL}s | Press Ctrl+C to exit${NC}\n"
}

# Get cache service status
check_cache_service() {
    if systemctl is-active nix-serve >/dev/null 2>&1; then
        echo -e "${GREEN}● RUNNING${NC}"
    else
        echo -e "${RED}● STOPPED${NC}"
    fi
}

# Get system metrics
get_system_metrics() {
    # CPU usage
    local cpu_usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    
    # Memory usage
    local mem_total mem_used mem_percent
    mem_total=$(free -m | awk '/^Mem:/{print $2}')
    mem_used=$(free -m | awk '/^Mem:/{print $3}')
    mem_percent=$(awk "BEGIN {printf \"%.1f\", ($mem_used/$mem_total)*100}")
    
    # Disk usage
    local disk_total disk_used disk_percent
    disk_total=$(df -h / | tail -1 | awk '{print $2}')
    disk_used=$(df -h / | tail -1 | awk '{print $3}')
    disk_percent=$(df -h / | tail -1 | awk '{print $5}')
    
    # Network stats
    local rx_bytes tx_bytes
    if [ -f /sys/class/net/eth0/statistics/rx_bytes ]; then
        rx_bytes=$(cat /sys/class/net/eth0/statistics/rx_bytes)
        tx_bytes=$(cat /sys/class/net/eth0/statistics/tx_bytes)
    else
        rx_bytes=0
        tx_bytes=0
    fi
    
    echo "$cpu_usage|$mem_used|$mem_total|$mem_percent|$disk_used|$disk_total|$disk_percent|$rx_bytes|$tx_bytes"
}

# Calculate bandwidth
calculate_bandwidth() {
    local prev_rx="$1"
    local prev_tx="$2"
    local curr_rx="$3"
    local curr_tx="$4"
    local interval="$5"
    
    local rx_rate tx_rate
    rx_rate=$(awk "BEGIN {printf \"%.2f\", ($curr_rx - $prev_rx) / $interval / 1024 / 1024}")
    tx_rate=$(awk "BEGIN {printf \"%.2f\", ($curr_tx - $prev_tx) / $interval / 1024 / 1024}")
    
    echo "$rx_rate|$tx_rate"
}

# Get Nix store stats
get_nix_stats() {
    local store_size store_paths
    store_size=$(du -sh /nix/store 2>/dev/null | awk '{print $1}' || echo "N/A")
    store_paths=$(find /nix/store -maxdepth 1 -type d 2>/dev/null | wc -l || echo "N/A")
    
    echo "$store_size|$store_paths"
}

# Check active connections
get_active_connections() {
    if command -v ss >/dev/null 2>&1; then
        ss -tn state established "( sport = :$CACHE_PORT or dport = :$CACHE_PORT )" 2>/dev/null | grep -c "^ESTAB" || echo "0"
    else
        netstat -tn 2>/dev/null | grep ":$CACHE_PORT" | grep -c "ESTABLISHED" || echo "0"
    fi
}

# Main monitoring loop
main() {
    local prev_metrics curr_metrics
    local prev_rx prev_tx
    
    # Initial metrics
    prev_metrics=$(get_system_metrics)
    prev_rx=$(echo "$prev_metrics" | cut -d'|' -f8)
    prev_tx=$(echo "$prev_metrics" | cut -d'|' -f9)
    
    while true; do
        show_header
        
        # Service status
        echo -e "${YELLOW}[CACHE SERVICE]${NC}"
        echo -n "Status: "
        check_cache_service
        echo -n "Active Connections: "
        get_active_connections
        echo ""
        
        # Get current metrics
        curr_metrics=$(get_system_metrics)
        
        local cpu mem_used mem_total mem_percent disk_used disk_total disk_percent curr_rx curr_tx
        IFS='|' read -r cpu mem_used mem_total mem_percent disk_used disk_total disk_percent curr_rx curr_tx <<< "$curr_metrics"
        
        # Calculate bandwidth
        local bandwidth rx_rate tx_rate
        bandwidth=$(calculate_bandwidth "$prev_rx" "$prev_tx" "$curr_rx" "$curr_tx" "$REFRESH_INTERVAL")
        IFS='|' read -r rx_rate tx_rate <<< "$bandwidth"
        
        # System resources
        echo -e "${YELLOW}[SYSTEM RESOURCES]${NC}"
        
        # CPU
        echo -n "CPU Usage: "
        if (( $(awk "BEGIN {print ($cpu > 80)}") )); then
            echo -e "${RED}${cpu}%${NC}"
        elif (( $(awk "BEGIN {print ($cpu > 50)}") )); then
            echo -e "${YELLOW}${cpu}%${NC}"
        else
            echo -e "${GREEN}${cpu}%${NC}"
        fi
        
        # Memory
        echo -n "Memory: ${mem_used}MB / ${mem_total}MB "
        if (( $(awk "BEGIN {print ($mem_percent > 80)}") )); then
            echo -e "(${RED}${mem_percent}%${NC})"
        elif (( $(awk "BEGIN {print ($mem_percent > 60)}") )); then
            echo -e "(${YELLOW}${mem_percent}%${NC})"
        else
            echo -e "(${GREEN}${mem_percent}%${NC})"
        fi
        
        # Disk
        echo -n "Disk: ${disk_used} / ${disk_total} "
        local disk_percent_num=${disk_percent%?}
        if (( disk_percent_num > 85 )); then
            echo -e "(${RED}${disk_percent}${NC})"
        elif (( disk_percent_num > 70 )); then
            echo -e "(${YELLOW}${disk_percent}${NC})"
        else
            echo -e "(${GREEN}${disk_percent}${NC})"
        fi
        
        echo ""
        
        # Network
        echo -e "${YELLOW}[NETWORK]${NC}"
        echo "Download: ${rx_rate} MB/s"
        echo "Upload: ${tx_rate} MB/s"
        echo ""
        
        # Nix store
        echo -e "${YELLOW}[NIX STORE]${NC}"
        local nix_stats store_size store_paths
        nix_stats=$(get_nix_stats)
        IFS='|' read -r store_size store_paths <<< "$nix_stats"
        echo "Store Size: $store_size"
        echo "Store Paths: $store_paths"
        echo ""
        
        # Recent activity (last 5 builds)
        if command -v journalctl >/dev/null 2>&1; then
            echo -e "${YELLOW}[RECENT ACTIVITY]${NC}"
            journalctl -u nix-daemon -n 5 --no-pager --output=short-iso 2>/dev/null | \
                tail -5 | \
                cut -c1-70 || echo "No recent activity"
        fi
        
        # Update previous values
        prev_rx=$curr_rx
        prev_tx=$curr_tx
        
        sleep "$REFRESH_INTERVAL"
    done
}

# Handle script arguments
case "${1:-}" in
    -h|--help)
        echo "Usage: $0 [INTERVAL]"
        echo ""
        echo "Monitor NixOS cache server performance"
        echo ""
        echo "Arguments:"
        echo "  INTERVAL    Refresh interval in seconds (default: 2)"
        exit 0
        ;;
    *)
        if [ -n "${1:-}" ]; then
            REFRESH_INTERVAL="$1"
        fi
        ;;
esac

# Run monitor
main
