#!/usr/bin/env bash
# NixOS Remote Cache Server - System Diagnostics
# Analyzes hardware, network, and system capabilities for optimal cache server configuration

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== NixOS Remote Cache Server - System Diagnostics ===${NC}\n"

# Hardware Analysis
echo -e "${GREEN}[HARDWARE]${NC}"
echo -n "CPU Model: "
grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs
echo -n "CPU Cores: "
nproc
echo -n "Total RAM: "
free -h | awk '/^Mem:/{print $2}'
echo -n "Available RAM: "
free -h | awk '/^Mem:/{print $7}'
echo -n "Swap: "
free -h | awk '/^Swap:/{print $2}'

# Storage Analysis
echo -e "\n${GREEN}[STORAGE]${NC}"
df -h / | tail -1 | awk '{print "Root Partition: "$2" total, "$4" available ("$5" used)"}'
if [ -d "/nix/store" ]; then
    du -sh /nix/store 2>/dev/null | awk '{print "Nix Store Size: "$1}' || echo "Nix Store Size: Unable to calculate"
fi

# Network Analysis
echo -e "\n${GREEN}[NETWORK INTERFACES]${NC}"
ip -br addr show | grep -v "lo" | while read -r line; do
    iface=$(echo "$line" | awk '{print $1}')
    status=$(echo "$line" | awk '{print $2}')
    ip=$(echo "$line" | awk '{print $3}')
    
    echo -n "$iface: $status"
    [ "$ip" != "" ] && echo " - $ip" || echo ""
    
    # Check link speed for ethernet interfaces
    if [[ "$iface" =~ ^(eth|enp) ]]; then
        speed=$(cat /sys/class/net/"$iface"/speed 2>/dev/null || echo "N/A")
        [ "$speed" != "N/A" ] && echo "  └─ Link Speed: ${speed}Mbps"
    fi
done

# Check for direct network connection possibility
echo -e "\n${GREEN}[NETWORK TOPOLOGY]${NC}"
if ip -br addr show | grep -qE "eth|enp"; then
    echo -e "${YELLOW}✓ Ethernet interface detected - Direct RJ45 connection possible${NC}"
    echo "  Recommendation: Use direct cable connection between machines for:"
    echo "  • Reduced latency (no switch/router overhead)"
    echo "  • Dedicated bandwidth"
    echo "  • Network isolation for cache traffic"
else
    echo "⚠ No ethernet interface found - WiFi only setup detected"
fi

# Performance Recommendations
echo -e "\n${BLUE}[RECOMMENDATIONS]${NC}"

# RAM-based recommendations
ram_mb=$(free -m | awk '/^Mem:/{print $2}')
if [ "$ram_mb" -lt 6144 ]; then
    echo -e "${YELLOW}⚠ Low RAM detected ($ram_mb MB)${NC}"
    echo "  • Enable aggressive cache eviction"
    echo "  • Limit concurrent builds: nix.settings.max-jobs = 1"
    echo "  • Consider RAM upgrade during Black Friday sales"
    echo "  • Enable zram compression"
else
    echo -e "${GREEN}✓ Adequate RAM for cache server${NC}"
fi

# Storage recommendations
root_avail_gb=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$root_avail_gb" -lt 100 ]; then
    echo -e "${YELLOW}⚠ Limited storage space (${root_avail_gb}GB available)${NC}"
    echo "  • Enable automatic garbage collection"
    echo "  • Set max-free: nix.settings.max-free = $(($root_avail_gb * 1024 * 1024 * 1024 / 4))"
else
    echo -e "${GREEN}✓ Adequate storage for cache server${NC}"
fi

# CPU recommendations
cpu_cores=$(nproc)
if [ "$cpu_cores" -le 2 ]; then
    echo -e "${YELLOW}⚠ Limited CPU cores ($cpu_cores)${NC}"
    echo "  • Reduce max-jobs: nix.settings.max-jobs = 1"
    echo "  • Enable distributed builds if possible"
else
    echo -e "${GREEN}✓ Adequate CPU cores for caching${NC}"
fi

echo -e "\n${BLUE}=== Diagnostics Complete ===${NC}"
