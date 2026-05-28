#!/bin/bash
# Deploy and Test
#
# Deploys changes from repository to hooks directory and runs tests.
# Usage: ./deploy-and-test.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

REPO_DIR="$HOME/Tools/claude-requirements-framework"
TEST_FILE="$HOME/.claude/hooks/test_requirements.py"

if [ ! -d "$REPO_DIR" ]; then
    echo -e "${RED}❌ Repository not found: $REPO_DIR${NC}"
    exit 1
fi

cd "$REPO_DIR"

echo "🚀 Deploy and Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Check sync status
echo "Step 1: Checking sync status..."
./sync.sh status
echo ""

# Step 2: Deploy
echo "Step 2: Deploying..."
./sync.sh deploy
echo -e "${GREEN}✓${NC} Deployed"
echo ""

# Step 3: Run tests
echo "Step 3: Running tests..."
start_time=$(date +%s)

if python3 "$TEST_FILE"; then
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}✅ Deploy and test successful${NC} (${duration}s)"
    echo ""
    echo "💡 Next steps:"
    echo "   git add ."
    echo "   git commit -m 'feat: description'"
    echo "   git push"
else
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${RED}❌ Tests failed${NC} (${duration}s)"
    echo ""
    echo "💡 Fix the failing tests before committing"
    exit 1
fi
