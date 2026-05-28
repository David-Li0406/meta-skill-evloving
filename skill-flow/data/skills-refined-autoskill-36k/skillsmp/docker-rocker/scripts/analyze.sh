#!/bin/bash
# =============================================================================
# Docker Image Analysis Script
# Analyzes image size, layers, and optimization opportunities
# Usage: ./analyze.sh [image-tag]
# =============================================================================

set -e

IMAGE="${1:-app:latest}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${YELLOW}Analyzing Docker image: $IMAGE${NC}"
echo "=============================================="
echo ""

# Image size
echo -e "${CYAN}Image Size:${NC}"
docker images "$IMAGE" --format "  Size: {{.Size}}"
echo ""

# Layer history
echo -e "${CYAN}Layer History:${NC}"
docker history "$IMAGE" --format "table {{.CreatedBy}}\t{{.Size}}" | head -20
echo ""

# Image details
echo -e "${CYAN}Image Details:${NC}"
docker inspect "$IMAGE" --format "  Created: {{.Created}}"
docker inspect "$IMAGE" --format "  Architecture: {{.Architecture}}"
docker inspect "$IMAGE" --format "  OS: {{.Os}}"
echo ""

# Environment variables
echo -e "${CYAN}Environment Variables:${NC}"
docker inspect "$IMAGE" --format '{{range .Config.Env}}  {{.}}{{"\n"}}{{end}}'

# Exposed ports
echo -e "${CYAN}Exposed Ports:${NC}"
docker inspect "$IMAGE" --format '{{range $p, $conf := .Config.ExposedPorts}}  {{$p}}{{"\n"}}{{end}}'

# User
echo -e "${CYAN}Running User:${NC}"
docker inspect "$IMAGE" --format "  User: {{.Config.User}}"
echo ""

# Health check
echo -e "${CYAN}Health Check:${NC}"
docker inspect "$IMAGE" --format "  {{.Config.Healthcheck.Test}}"
echo ""

# Recommendations
echo -e "${YELLOW}Optimization Recommendations:${NC}"
echo "  - Target size: <200MB for production images"
echo "  - Ensure running as non-root user"
echo "  - Verify health check is configured"
echo "  - Check for unnecessary layers"
echo ""

# Check if Dive is available for detailed analysis
if command -v dive &> /dev/null; then
    echo -e "${YELLOW}Run 'dive $IMAGE' for detailed layer analysis${NC}"
fi

echo -e "${GREEN}Analysis complete!${NC}"
