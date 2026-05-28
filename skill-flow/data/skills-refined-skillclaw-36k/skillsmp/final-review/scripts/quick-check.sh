#!/bin/bash
# Pop-CLI Quick Check Script
# Runs fast checks (formatting and clippy only)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

cd "$(git rev-parse --show-toplevel)" || exit 1

echo -e "${BLUE}Quick Check: Formatting + Clippy${NC}\n"

# Formatting
echo -e "→ Checking formatting..."
if cargo +nightly fmt --all -- --check 2>/dev/null; then
    echo -e "${GREEN}✓ Formatting OK${NC}"
else
    echo -e "${RED}✗ Format issues - run: cargo +nightly fmt --all${NC}"
    exit 1
fi

# Clippy
echo -e "→ Running clippy..."
if cargo clippy --all-targets --all-features -- -D warnings 2>&1 | tail -5; then
    echo -e "${GREEN}✓ Clippy OK${NC}"
else
    echo -e "${RED}✗ Clippy warnings found${NC}"
    exit 1
fi

echo -e "\n${GREEN}Quick check passed!${NC}"
