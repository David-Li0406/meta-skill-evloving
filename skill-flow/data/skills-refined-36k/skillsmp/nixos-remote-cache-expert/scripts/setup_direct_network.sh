#!/usr/bin/env bash
# NixOS Remote Cache Server - Direct Network Connection Setup
# Configures point-to-point ethernet connection between cache server and client

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
SERVER_IP="${SERVER_IP:-10.255.255.1}"
CLIENT_IP="${CLIENT_IP:-10.255.255.2}"
SUBNET_MASK="24"
INTERFACE="${INTERFACE:-}"

usage() {
    echo "Usage: $0 [--server|--client] [--interface IFACE]"
    echo ""
    echo "Configure direct ethernet connection for NixOS cache server"
    echo ""
    echo "Options:"
    echo "  --server              Configure this machine as cache server"
    echo "  --client              Configure this machine as cache client"
    echo "  --interface IFACE     Specify network interface (auto-detect if not provided)"
    echo ""
    echo "Environment variables:"
    echo "  SERVER_IP             Server IP address (default: 10.255.255.1)"
    echo "  CLIENT_IP             Client IP address (default: 10.255.255.2)"
    exit 1
}

detect_ethernet_interface() {
    local iface
    iface=$(ip -br link show | grep -E "eth|enp" | awk '{print $1}' | head -1)
    
    if [ -z "$iface" ]; then
        echo -e "${RED}Error: No ethernet interface found${NC}" >&2
        exit 1
    fi
    
    echo "$iface"
}

configure_server() {
    local iface="$1"
    
    echo -e "${BLUE}Configuring as CACHE SERVER${NC}"
    echo "Interface: $iface"
    echo "Server IP: $SERVER_IP/$SUBNET_MASK"
    echo "Expected Client IP: $CLIENT_IP"
    echo ""
    
    # Generate NixOS configuration
    cat > /tmp/direct-network-config.nix <<EOF
# Direct Network Connection for NixOS Cache Server
# Add this to your configuration.nix

{
  networking.interfaces.$iface = {
    ipv4.addresses = [{
      address = "$SERVER_IP";
      prefixLength = $SUBNET_MASK;
    }];
  };
  
  # Optimize network for local cache traffic
  boot.kernel.sysctl = {
    "net.core.rmem_max" = 134217728;  # 128MB
    "net.core.wmem_max" = 134217728;  # 128MB
    "net.ipv4.tcp_rmem" = "4096 87380 67108864";  # 64MB
    "net.ipv4.tcp_wmem" = "4096 65536 67108864";  # 64MB
    "net.ipv4.tcp_congestion_control" = "bbr";
    "net.core.default_qdisc" = "fq";
  };
  
  # Firewall rules for cache traffic
  networking.firewall = {
    enable = true;
    interfaces.$iface = {
      allowedTCPPorts = [ 
        5000  # nix-serve default port
      ];
    };
  };
}
EOF
    
    echo -e "${GREEN}✓ Configuration generated: /tmp/direct-network-config.nix${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Add the configuration to your /etc/nixos/configuration.nix"
    echo "2. Run: sudo nixos-rebuild switch"
    echo "3. Verify with: ip addr show $iface"
    echo "4. Test connectivity: ping $CLIENT_IP (after client is configured)"
}

configure_client() {
    local iface="$1"
    
    echo -e "${BLUE}Configuring as CACHE CLIENT${NC}"
    echo "Interface: $iface"
    echo "Client IP: $CLIENT_IP/$SUBNET_MASK"
    echo "Cache Server IP: $SERVER_IP"
    echo ""
    
    # Generate NixOS configuration
    cat > /tmp/direct-network-config.nix <<EOF
# Direct Network Connection for NixOS Cache Client
# Add this to your configuration.nix

{
  networking.interfaces.$iface = {
    ipv4.addresses = [{
      address = "$CLIENT_IP";
      prefixLength = $SUBNET_MASK;
    }];
  };
  
  # Configure Nix to use local cache server
  nix.settings = {
    substituters = [
      "http://$SERVER_IP:5000"  # Local cache server (tried first)
      "https://cache.nixos.org"  # Fallback to official cache
    ];
    trusted-public-keys = [
      # Add your cache server's public key here after generating it
      # Run on server: nix-store --generate-binary-cache-key cache-key cache-key.sec cache-key.pub
      # Then add the content of cache-key.pub here
    ];
  };
  
  # Optimize network for local cache traffic
  boot.kernel.sysctl = {
    "net.core.rmem_max" = 134217728;
    "net.core.wmem_max" = 134217728;
    "net.ipv4.tcp_rmem" = "4096 87380 67108864";
    "net.ipv4.tcp_wmem" = "4096 65536 67108864";
    "net.ipv4.tcp_congestion_control" = "bbr";
    "net.core.default_qdisc" = "fq";
  };
}
EOF
    
    echo -e "${GREEN}✓ Configuration generated: /tmp/direct-network-config.nix${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Add the configuration to your /etc/nixos/configuration.nix"
    echo "2. Run: sudo nixos-rebuild switch"
    echo "3. Verify with: ip addr show $iface"
    echo "4. Test connectivity: ping $SERVER_IP"
}

# Parse arguments
MODE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --server)
            MODE="server"
            shift
            ;;
        --client)
            MODE="client"
            shift
            ;;
        --interface)
            INTERFACE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate mode
if [ -z "$MODE" ]; then
    echo -e "${RED}Error: Must specify --server or --client${NC}"
    usage
fi

# Detect or validate interface
if [ -z "$INTERFACE" ]; then
    INTERFACE=$(detect_ethernet_interface)
    echo -e "${YELLOW}Auto-detected interface: $INTERFACE${NC}"
else
    if ! ip link show "$INTERFACE" &>/dev/null; then
        echo -e "${RED}Error: Interface $INTERFACE not found${NC}"
        exit 1
    fi
fi

echo ""

# Configure based on mode
case $MODE in
    server)
        configure_server "$INTERFACE"
        ;;
    client)
        configure_client "$INTERFACE"
        ;;
esac

echo -e "\n${BLUE}=== Why Direct Connection? ===${NC}"
echo "✓ Eliminates switch/router latency (typically 0.5-2ms reduction)"
echo "✓ Dedicated bandwidth - no contention with other network traffic"
echo "✓ Network isolation - cache traffic doesn't interfere with other services"
echo "✓ Simpler troubleshooting - fewer network hops"
echo "✓ Lower CPU overhead - no NAT/routing processing"
