#!/usr/bin/env bash
# system-analyzer.sh - Deep system analysis and troubleshooting

set -euo pipefail

BOLD='\033[1m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

header() {
    echo -e "\n${BOLD}${CYAN}=== $1 ===${NC}\n"
}

info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

success() {
    echo -e "${GREEN}✓${NC} $*"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $*"
}

error() {
    echo -e "${RED}✗${NC} $*"
}

# System overview
system_overview() {
    header "System Overview"
    
    info "Hostname: $(hostname)"
    info "Kernel: $(uname -r)"
    info "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
    info "Uptime: $(uptime -p)"
    info "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
    
    # NixOS specific
    if [[ -f /etc/NIXOS ]]; then
        success "NixOS detected"
        info "Generation: $(nixos-version 2>/dev/null || echo "Unknown")"
        info "Channel: $(nix-channel --list 2>/dev/null | head -1 || echo "Flake-based")"
    fi
}

# Resource analysis
resource_analysis() {
    header "Resource Analysis"
    
    # CPU
    echo -e "${BOLD}CPU:${NC}"
    lscpu | grep -E "Model name|CPU\(s\)|MHz|Cache"
    
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
        warning "High CPU usage: ${CPU_USAGE}%"
    else
        success "CPU usage: ${CPU_USAGE}%"
    fi
    
    # Memory
    echo -e "\n${BOLD}Memory:${NC}"
    free -h | grep -E "Mem|Swap"
    
    MEM_PERCENT=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [[ $MEM_PERCENT -gt 80 ]]; then
        warning "High memory usage: ${MEM_PERCENT}%"
        echo "Top memory consumers:"
        ps aux --sort=-%mem | head -6
    else
        success "Memory usage: ${MEM_PERCENT}%"
    fi
    
    # Disk
    echo -e "\n${BOLD}Disk Usage:${NC}"
    df -h | grep -v "tmpfs\|loop"
    
    # Check for full partitions
    while IFS= read -r line; do
        USAGE=$(echo "$line" | awk '{print $5}' | sed 's/%//')
        if [[ $USAGE -gt 90 ]]; then
            error "Critical disk usage on: $(echo "$line" | awk '{print $6}')"
        elif [[ $USAGE -gt 80 ]]; then
            warning "High disk usage on: $(echo "$line" | awk '{print $6}')"
        fi
    done < <(df -h | grep -v "tmpfs\|loop\|Filesystem")
}

# Network analysis
network_analysis() {
    header "Network Analysis"
    
    # Active interfaces
    echo -e "${BOLD}Active Interfaces:${NC}"
    ip -br addr show | grep -v "^lo"
    
    # Default route
    echo -e "\n${BOLD}Default Gateway:${NC}"
    ip route | grep default
    
    # DNS
    echo -e "\n${BOLD}DNS Configuration:${NC}"
    if [[ -f /etc/resolv.conf ]]; then
        grep nameserver /etc/resolv.conf
    fi
    
    # Active connections
    echo -e "\n${BOLD}Active Connections:${NC}"
    ss -s
    
    # Port listeners
    echo -e "\n${BOLD}Listening Ports:${NC}"
    ss -tlnp | head -10
    
    # Network errors
    ERRORS=$(ip -s link | grep -E "errors|dropped" | awk '{sum+=$1} END {print sum}')
    if [[ $ERRORS -gt 0 ]]; then
        warning "Network errors detected: $ERRORS"
        ip -s link
    else
        success "No network errors"
    fi
}

# Process analysis
process_analysis() {
    header "Process Analysis"
    
    echo -e "${BOLD}Top CPU Consumers:${NC}"
    ps aux --sort=-%cpu | head -6
    
    echo -e "\n${BOLD}Top Memory Consumers:${NC}"
    ps aux --sort=-%mem | head -6
    
    echo -e "\n${BOLD}Zombie Processes:${NC}"
    ZOMBIES=$(ps aux | grep -c " Z ")
    if [[ $ZOMBIES -gt 0 ]]; then
        warning "$ZOMBIES zombie processes found"
        ps aux | grep " Z "
    else
        success "No zombie processes"
    fi
    
    # Long-running processes
    echo -e "\n${BOLD}Long-Running Processes (>1 day):${NC}"
    ps -eo pid,user,etime,cmd --sort=-etime | awk 'NR==1 || $3 ~ /-/'
}

# Service health
service_health() {
    header "Service Health"
    
    if command -v systemctl &>/dev/null; then
        echo -e "${BOLD}Failed Services:${NC}"
        FAILED=$(systemctl list-units --failed --no-pager --no-legend)
        if [[ -n "$FAILED" ]]; then
            error "Failed services detected:"
            echo "$FAILED"
        else
            success "All services running"
        fi
        
        echo -e "\n${BOLD}Service Status:${NC}"
        systemctl list-units --type=service --state=running --no-pager | head -10
    fi
}

# Security checks
security_checks() {
    header "Security Analysis"
    
    # Failed login attempts
    echo -e "${BOLD}Failed Login Attempts:${NC}"
    if [[ -f /var/log/auth.log ]]; then
        FAILED_LOGINS=$(grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l)
        if [[ $FAILED_LOGINS -gt 10 ]]; then
            warning "$FAILED_LOGINS failed login attempts found"
            grep "Failed password" /var/log/auth.log | tail -5
        else
            success "Failed logins: $FAILED_LOGINS"
        fi
    fi
    
    # Check for SUID files
    echo -e "\n${BOLD}SUID Binaries Check:${NC}"
    SUID_COUNT=$(find /usr/bin /bin /sbin -perm -4000 2>/dev/null | wc -l)
    info "Found $SUID_COUNT SUID binaries"
    
    # Firewall status
    echo -e "\n${BOLD}Firewall Status:${NC}"
    if command -v ufw &>/dev/null; then
        ufw status || info "UFW not active"
    elif command -v firewall-cmd &>/dev/null; then
        firewall-cmd --state 2>/dev/null || info "Firewalld not active"
    elif [[ -f /etc/nftables.conf ]]; then
        success "nftables configured"
    else
        warning "No firewall detected"
    fi
}

# NixOS specific checks
nixos_checks() {
    if [[ ! -f /etc/NIXOS ]]; then
        return
    fi
    
    header "NixOS Analysis"
    
    # Nix store size
    echo -e "${BOLD}Nix Store:${NC}"
    STORE_SIZE=$(du -sh /nix/store 2>/dev/null | cut -f1)
    info "Store size: $STORE_SIZE"
    
    # GC roots
    GC_ROOTS=$(nix-store --gc --print-roots 2>/dev/null | wc -l)
    info "GC roots: $GC_ROOTS"
    
    # Generations
    echo -e "\n${BOLD}System Generations:${NC}"
    nixos-rebuild list-generations 2>/dev/null | tail -5 || info "Cannot list generations"
    
    # Optimization
    echo -e "\n${BOLD}Store Optimization:${NC}"
    LINKS=$(nix-store --optimise --dry-run 2>&1 | grep "can be freed" | awk '{print $1, $2, $3}')
    if [[ -n "$LINKS" ]]; then
        warning "Potential savings: $LINKS"
        info "Run: nix-store --optimise"
    else
        success "Store optimized"
    fi
    
    # Flake status
    if [[ -f /etc/nixos/flake.nix ]]; then
        success "Flake-based configuration detected"
        echo -e "\n${BOLD}Flake Inputs:${NC}"
        nix flake metadata /etc/nixos 2>/dev/null || warning "Cannot read flake metadata"
    fi
}

# Log analysis
log_analysis() {
    header "Recent Log Errors"
    
    if command -v journalctl &>/dev/null; then
        echo -e "${BOLD}Last Hour Errors:${NC}"
        journalctl --priority=err --since="1 hour ago" --no-pager | tail -20
        
        echo -e "\n${BOLD}Kernel Errors:${NC}"
        journalctl -k --priority=err --no-pager | tail -10
    else
        echo -e "${BOLD}System Logs:${NC}"
        if [[ -f /var/log/syslog ]]; then
            grep -i error /var/log/syslog | tail -10
        fi
    fi
}

# Performance metrics
performance_metrics() {
    header "Performance Metrics"
    
    # I/O statistics
    if command -v iostat &>/dev/null; then
        echo -e "${BOLD}I/O Statistics:${NC}"
        iostat -x 1 2 | tail -n +4
    fi
    
    # Context switches
    echo -e "\n${BOLD}Context Switches/Interrupts:${NC}"
    vmstat 1 3 | tail -1
}

# Generate recommendations
generate_recommendations() {
    header "Recommendations"
    
    # Check memory
    MEM_PERCENT=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [[ $MEM_PERCENT -gt 80 ]]; then
        warning "High memory usage. Consider:"
        echo "  - Identify memory leaks with: ps aux --sort=-%mem"
        echo "  - Check for runaway processes"
        echo "  - Add swap space if needed"
    fi
    
    # Check disk
    DISK_FULL=$(df -h | awk 'NR>1 {gsub("%","",$5); if($5>90) print $6}')
    if [[ -n "$DISK_FULL" ]]; then
        warning "Disk space critical on: $DISK_FULL"
        echo "  - Clean package cache: nix-collect-garbage -d"
        echo "  - Find large files: ncdu /"
    fi
    
    # NixOS specific
    if [[ -f /etc/NIXOS ]]; then
        GC_ROOTS=$(nix-store --gc --print-roots 2>/dev/null | wc -l)
        if [[ $GC_ROOTS -gt 100 ]]; then
            warning "Many GC roots ($GC_ROOTS). Clean up:"
            echo "  - nix-env --delete-generations old"
            echo "  - nix-collect-garbage -d"
        fi
    fi
}

# Main execution
main() {
    echo -e "${BOLD}${MAGENTA}"
    cat << "EOF"
╔═══════════════════════════════════════╗
║   System Analyzer & Troubleshooter   ║
╚═══════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    case "${1:-full}" in
        full)
            system_overview
            resource_analysis
            network_analysis
            process_analysis
            service_health
            security_checks
            nixos_checks
            log_analysis
            generate_recommendations
            ;;
        quick)
            system_overview
            resource_analysis
            generate_recommendations
            ;;
        network)
            network_analysis
            ;;
        security)
            security_checks
            ;;
        nixos)
            nixos_checks
            ;;
        *)
            echo "Usage: $0 {full|quick|network|security|nixos}"
            exit 1
            ;;
    esac
    
    echo -e "\n${BOLD}${GREEN}Analysis complete!${NC}"
}

main "$@"
