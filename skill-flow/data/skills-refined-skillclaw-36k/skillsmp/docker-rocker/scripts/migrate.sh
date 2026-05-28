#!/bin/bash
# =============================================================================
# Database Migration Script
# Runs Alembic migrations in Docker
# Usage: ./migrate.sh [command]
#   command: upgrade (default), downgrade, history, current
# =============================================================================

set -e

COMMAND="${1:-upgrade}"
REVISION="${2:-head}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check for DATABASE_URL_DIRECT
if [ -z "$DATABASE_URL_DIRECT" ]; then
    echo -e "${RED}Error: DATABASE_URL_DIRECT not set${NC}"
    echo "Use direct (non-pooled) connection for migrations"
    echo ""
    echo "Example:"
    echo "  export DATABASE_URL_DIRECT='postgresql+asyncpg://user:pass@host/db'"
    exit 1
fi

echo -e "${YELLOW}Running database migration...${NC}"
echo "  Command: alembic $COMMAND $REVISION"
echo ""

case "$COMMAND" in
    upgrade)
        docker compose run --rm \
            -e DATABASE_URL="$DATABASE_URL_DIRECT" \
            api alembic upgrade "$REVISION"
        ;;
    downgrade)
        docker compose run --rm \
            -e DATABASE_URL="$DATABASE_URL_DIRECT" \
            api alembic downgrade "$REVISION"
        ;;
    history)
        docker compose run --rm \
            -e DATABASE_URL="$DATABASE_URL_DIRECT" \
            api alembic history
        ;;
    current)
        docker compose run --rm \
            -e DATABASE_URL="$DATABASE_URL_DIRECT" \
            api alembic current
        ;;
    generate)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Migration message required${NC}"
            echo "Usage: ./migrate.sh generate 'migration message'"
            exit 1
        fi
        docker compose run --rm \
            -e DATABASE_URL="$DATABASE_URL_DIRECT" \
            api alembic revision --autogenerate -m "$2"
        ;;
    *)
        echo "Usage: ./migrate.sh [command] [revision]"
        echo "  upgrade [head]     - Apply migrations (default)"
        echo "  downgrade [-1]     - Rollback migrations"
        echo "  history            - Show migration history"
        echo "  current            - Show current revision"
        echo "  generate 'message' - Generate new migration"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Migration complete!${NC}"
