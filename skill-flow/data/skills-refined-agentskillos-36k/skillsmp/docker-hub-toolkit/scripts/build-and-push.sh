#!/bin/bash
# Build, tag, and push Python Docker image to Docker Hub
# Usage: bash scripts/build-and-push.sh USERNAME APP_NAME VERSION [PLATFORM]
#
# Examples:
#   bash scripts/build-and-push.sh myuser task-mgmt-api 1.0.0
#   bash scripts/build-and-push.sh myuser task-mgmt-api 1.0.0 linux/amd64,linux/arm64

set -euo pipefail

# Arguments
USERNAME="${1:?Error: Docker Hub username required}"
APP_NAME="${2:?Error: Application name required}"
VERSION="${3:?Error: Version tag required}"
PLATFORM="${4:-linux/amd64}"

# Derived values
IMAGE="${USERNAME}/${APP_NAME}"
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
FULL_TAG="${VERSION}-${GIT_SHA}"

echo "=== Docker Hub Build & Push ==="
echo "Image: ${IMAGE}"
echo "Version: ${VERSION}"
echo "Git SHA: ${GIT_SHA}"
echo "Platform: ${PLATFORM}"
echo ""

# Step 1: Verify Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Step 2: Verify authentication
echo ">> Checking Docker Hub authentication..."
if ! docker info 2>/dev/null | grep -q "Username"; then
    echo "Warning: Not logged in to Docker Hub. Run 'docker login' first."
    echo "Attempting login..."
    docker login -u "${USERNAME}"
fi

# Step 3: Ensure BuildKit is enabled
export DOCKER_BUILDKIT=1

# Step 4: Build the image
echo ""
echo ">> Building image..."
if [[ "${PLATFORM}" == *","* ]]; then
    # Multi-platform build requires buildx and push together
    echo ">> Multi-platform build detected. Setting up buildx..."
    docker buildx create --name multiarch --use 2>/dev/null || docker buildx use multiarch
    docker buildx inspect --bootstrap

    echo ">> Building and pushing multi-platform image..."
    docker buildx build \
        --platform "${PLATFORM}" \
        -t "${IMAGE}:${VERSION}" \
        -t "${IMAGE}:${FULL_TAG}" \
        -t "${IMAGE}:latest" \
        --push \
        .

    echo ""
    echo "=== Multi-platform build and push complete ==="
else
    # Single platform build
    docker build \
        -t "${IMAGE}:${VERSION}" \
        -t "${IMAGE}:${FULL_TAG}" \
        -t "${IMAGE}:latest" \
        .

    # Step 5: Show image size
    echo ""
    echo ">> Image size:"
    docker images "${IMAGE}" --format "  {{.Tag}}: {{.Size}}"

    # Step 6: Push all tags
    echo ""
    echo ">> Pushing to Docker Hub..."
    docker push "${IMAGE}:${VERSION}"
    docker push "${IMAGE}:${FULL_TAG}"
    docker push "${IMAGE}:latest"

    echo ""
    echo "=== Build and push complete ==="
fi

echo ""
echo "Images available at: https://hub.docker.com/r/${IMAGE}"
echo "Tags pushed: ${VERSION}, ${FULL_TAG}, latest"
