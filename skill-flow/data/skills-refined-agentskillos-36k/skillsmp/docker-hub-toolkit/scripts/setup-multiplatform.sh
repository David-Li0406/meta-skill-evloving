#!/bin/bash
# Setup Docker Buildx for multi-platform builds
# Usage: bash scripts/setup-multiplatform.sh

set -euo pipefail

echo "=== Multi-Platform Build Setup ==="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

# Check buildx
echo ">> Checking buildx availability..."
if ! docker buildx version &> /dev/null; then
    echo "Error: Docker buildx not available. Update Docker to 19.03+."
    exit 1
fi
echo "  Buildx version: $(docker buildx version)"

# Setup QEMU for cross-platform emulation
echo ""
echo ">> Setting up QEMU emulation..."
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes 2>/dev/null || \
    docker run --rm --privileged tonistiigi/binfmt --install all

# Create/use multiarch builder
echo ""
echo ">> Creating multiarch builder..."
if docker buildx inspect multiarch &> /dev/null 2>&1; then
    echo "  Builder 'multiarch' already exists, using it."
    docker buildx use multiarch
else
    docker buildx create --name multiarch --driver docker-container --use
fi

# Bootstrap the builder
echo ""
echo ">> Bootstrapping builder..."
docker buildx inspect --bootstrap

# Show available platforms
echo ""
echo ">> Available platforms:"
docker buildx inspect --bootstrap 2>/dev/null | grep "Platforms:" || \
    echo "  linux/amd64, linux/arm64, linux/arm/v7 (typical)"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Usage:"
echo "  docker buildx build --platform linux/amd64,linux/arm64 -t user/app:tag --push ."
echo ""
echo "To build without pushing (load to local):"
echo "  docker buildx build --platform linux/amd64 -t user/app:tag --load ."
