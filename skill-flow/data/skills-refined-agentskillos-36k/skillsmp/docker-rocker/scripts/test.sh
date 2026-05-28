#!/bin/bash
# =============================================================================
# Docker Test Script for FastAPI Applications
# Builds testing image and runs pytest
# Usage: ./test.sh [pytest-args]
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PYTEST_ARGS="${@:--v --cov=app --cov-report=term-missing}"

echo -e "${YELLOW}Building test image...${NC}"

export DOCKER_BUILDKIT=1

docker build \
    --target testing \
    --tag app:test \
    .

echo ""
echo -e "${YELLOW}Running tests...${NC}"
echo "  Args: $PYTEST_ARGS"
echo ""

# Run tests
docker run --rm \
    -e DATABASE_URL=sqlite+aiosqlite:///:memory: \
    -e ENVIRONMENT=testing \
    app:test \
    pytest $PYTEST_ARGS

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
else
    echo ""
    echo -e "${RED}Tests failed with exit code: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
