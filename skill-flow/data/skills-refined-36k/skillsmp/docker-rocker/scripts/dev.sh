#!/bin/bash
# =============================================================================
# Docker Development Script
# Starts development environment with hot-reload
# Usage: ./dev.sh [up|down|logs|shell]
# =============================================================================

set -e

COMMAND="${1:-up}"

# Colors
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

case "$COMMAND" in
    up)
        echo -e "${YELLOW}Starting development environment...${NC}"
        docker compose up --build
        ;;
    down)
        echo -e "${YELLOW}Stopping development environment...${NC}"
        docker compose down
        echo -e "${GREEN}Environment stopped.${NC}"
        ;;
    logs)
        docker compose logs -f api
        ;;
    shell)
        echo -e "${YELLOW}Opening shell in API container...${NC}"
        docker compose exec api /bin/bash
        ;;
    rebuild)
        echo -e "${YELLOW}Rebuilding and restarting...${NC}"
        docker compose down
        docker compose up --build
        ;;
    *)
        echo "Usage: ./dev.sh [up|down|logs|shell|rebuild]"
        echo "  up      - Start development environment (default)"
        echo "  down    - Stop development environment"
        echo "  logs    - Follow API logs"
        echo "  shell   - Open shell in API container"
        echo "  rebuild - Rebuild and restart"
        exit 1
        ;;
esac
