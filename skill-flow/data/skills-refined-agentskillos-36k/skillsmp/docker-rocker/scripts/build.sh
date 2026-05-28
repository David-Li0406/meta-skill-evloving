#!/bin/bash
# =============================================================================
# Docker Build Script for FastAPI Applications
# Usage: ./build.sh [target] [tag]
#   target: runtime (default), testing, development
#   tag: image tag (default: app:latest)
# =============================================================================

set -e

# Default values
TARGET="${1:-runtime}"
TAG="${2:-app:latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Building Docker image...${NC}"
echo "  Target: $TARGET"
echo "  Tag: $TAG"
echo ""

# Enable BuildKit for better caching
export DOCKER_BUILDKIT=1

# Build with cache
docker build \
    --target "$TARGET" \
    --tag "$TAG" \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    .

# Get image size
SIZE=$(docker images "$TAG" --format "{{.Size}}")

echo ""
echo -e "${GREEN}Build complete!${NC}"
echo "  Image: $TAG"
echo "  Size: $SIZE"
echo ""

# Verify the image
echo -e "${YELLOW}Verifying image...${NC}"
docker run --rm "$TAG" python -c "import sys; print(f'Python {sys.version}')"

echo -e "${GREEN}Image verified successfully!${NC}"
