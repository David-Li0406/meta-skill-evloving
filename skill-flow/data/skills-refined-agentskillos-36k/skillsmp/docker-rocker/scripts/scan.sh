#!/bin/bash
# =============================================================================
# Docker Security Scan Script
# Scans image for vulnerabilities using Docker Scout
# Usage: ./scan.sh [image-tag]
# =============================================================================

set -e

IMAGE="${1:-app:latest}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Scanning image for vulnerabilities...${NC}"
echo "  Image: $IMAGE"
echo ""

# Check if Docker Scout is available
if ! docker scout version &> /dev/null; then
    echo -e "${RED}Docker Scout not available.${NC}"
    echo "Install with: docker scout plugin install"
    echo ""
    echo "Falling back to basic analysis..."
    echo ""
    docker history "$IMAGE"
    exit 0
fi

# Run Docker Scout CVE scan
echo -e "${YELLOW}Running CVE scan...${NC}"
docker scout cves "$IMAGE"

echo ""
echo -e "${YELLOW}Running recommendations...${NC}"
docker scout recommendations "$IMAGE"

echo ""
echo -e "${GREEN}Scan complete!${NC}"
