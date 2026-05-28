#!/bin/bash
#
# Docker Rollback Script for DigitalOcean Droplets
# This script handles automatic rollback to the last working Docker image
# when a deployment fails.
#
# Usage: ./rollback.sh <container-name> <image-name> <registry-path>
#
# The script will:
# 1. Verify/create a .rollback-<image-name>.env file
# 2. Read the LAST_WORKING_TAG from that file
# 3. Extract configuration from the failed container
# 4. Deploy a new container with the last working tag using the same config
#

set -e

# Validate arguments
if [ $# -lt 3 ]; then
  echo "Usage: $0 <container-name> <image-name> <registry-path>"
  echo "Example: $0 my-app my-app registry.digitalocean.com/my-registry/my-app"
  exit 1
fi

CONTAINER_NAME="$1"
IMAGE_NAME="$2"
REGISTRY_PATH="$3"
ROLLBACK_FILE="$HOME/.rollback-${IMAGE_NAME}.env"
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

echo "$LOG_PREFIX ==================================================================="
echo "$LOG_PREFIX ===           INITIATING ROLLBACK PROCEDURE                    ==="
echo "$LOG_PREFIX ==================================================================="
echo ""

# Step 1: Verify/create rollback configuration file
echo "$LOG_PREFIX [1/5] Verifying rollback configuration file..."
if [ ! -f "$ROLLBACK_FILE" ]; then
  echo "$LOG_PREFIX ⚠ Rollback file not found at $ROLLBACK_FILE"
  echo "$LOG_PREFIX   Creating new rollback file..."

  # Create the file with a default fallback to 'latest'
  cat > "$ROLLBACK_FILE" << EOF
# Rollback configuration for $IMAGE_NAME
# This file tracks the last known working Docker image tag
LAST_WORKING_TAG=latest
EOF

  echo "$LOG_PREFIX ✓ Created rollback file with default tag 'latest'"
  echo "$LOG_PREFIX   ⚠ WARNING: No previous working version recorded"
  echo "$LOG_PREFIX   Falling back to 'latest' tag - this may not be stable"
else
  echo "$LOG_PREFIX ✓ Found rollback file: $ROLLBACK_FILE"
fi
echo ""

# Step 2: Read last working tag
echo "$LOG_PREFIX [2/5] Reading last working tag..."
source "$ROLLBACK_FILE"

if [ -z "$LAST_WORKING_TAG" ]; then
  echo "$LOG_PREFIX ⚠ LAST_WORKING_TAG is empty, defaulting to 'latest'"
  LAST_WORKING_TAG="latest"
fi

echo "$LOG_PREFIX ✓ Last working tag: $LAST_WORKING_TAG"
ROLLBACK_IMAGE="${REGISTRY_PATH}:${LAST_WORKING_TAG}"
echo "$LOG_PREFIX   Rolling back to: $ROLLBACK_IMAGE"
echo ""

# Step 3: Extract configuration from failed container
echo "$LOG_PREFIX [3/5] Extracting configuration from failed container..."

# Check if container exists
if ! docker inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
  echo "$LOG_PREFIX ⚠ Container '$CONTAINER_NAME' not found"
  echo "$LOG_PREFIX   Will use default configuration for rollback"
  ENV_ARGS=""
  PORT_ARGS=""
  VOLUME_ARGS=""
  NETWORK_ARGS=""
else
  echo "$LOG_PREFIX ✓ Found container: $CONTAINER_NAME"

  # Extract environment variables (excluding PATH and HOSTNAME which are auto-set)
  echo "$LOG_PREFIX   Extracting environment variables..."
  ENV_VARS=$(docker inspect "$CONTAINER_NAME" --format='{{range .Config.Env}}{{println .}}{{end}}' | \
    grep -v "^PATH=" | \
    grep -v "^HOSTNAME=" | \
    grep -v "^HOME=" || true)

  ENV_ARGS=""
  if [ -n "$ENV_VARS" ]; then
    while IFS= read -r env; do
      ENV_ARGS="$ENV_ARGS -e \"$env\""
    done <<< "$ENV_VARS"
    echo "$LOG_PREFIX   ✓ Extracted $(echo "$ENV_VARS" | wc -l) environment variable(s)"
  else
    echo "$LOG_PREFIX   ℹ No custom environment variables found"
  fi

  # Extract port mappings
  echo "$LOG_PREFIX   Extracting port mappings..."
  PORT_MAPPINGS=$(docker inspect "$CONTAINER_NAME" --format='{{range $p, $conf := .NetworkSettings.Ports}}{{if $conf}}{{range $conf}}{{.HostPort}}:{{$p}}{{println}}{{end}}{{end}}{{end}}' || true)

  PORT_ARGS=""
  if [ -n "$PORT_MAPPINGS" ]; then
    while IFS= read -r port; do
      PORT_ARGS="$PORT_ARGS -p $port"
    done <<< "$PORT_MAPPINGS"
    echo "$LOG_PREFIX   ✓ Extracted $(echo "$PORT_MAPPINGS" | wc -l) port mapping(s)"
  else
    echo "$LOG_PREFIX   ℹ No port mappings found"
  fi

  # Extract volume mounts
  echo "$LOG_PREFIX   Extracting volume mounts..."
  VOLUME_MOUNTS=$(docker inspect "$CONTAINER_NAME" --format='{{range .Mounts}}{{if eq .Type "bind"}}{{.Source}}:{{.Destination}}{{println}}{{end}}{{end}}' || true)

  VOLUME_ARGS=""
  if [ -n "$VOLUME_MOUNTS" ]; then
    while IFS= read -r volume; do
      VOLUME_ARGS="$VOLUME_ARGS -v $volume"
    done <<< "$VOLUME_MOUNTS"
    echo "$LOG_PREFIX   ✓ Extracted $(echo "$VOLUME_MOUNTS" | wc -l) volume mount(s)"
  else
    echo "$LOG_PREFIX   ℹ No volume mounts found"
  fi

  # Extract network
  echo "$LOG_PREFIX   Extracting network configuration..."
  NETWORK=$(docker inspect "$CONTAINER_NAME" --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}' || true)

  NETWORK_ARGS=""
  if [ -n "$NETWORK" ] && [ "$NETWORK" != "bridge" ]; then
    NETWORK_ARGS="--network $NETWORK"
    echo "$LOG_PREFIX   ✓ Network: $NETWORK"
  else
    echo "$LOG_PREFIX   ℹ Using default network"
  fi
fi

echo ""

# Step 4: Stop and remove failed container
echo "$LOG_PREFIX [4/5] Cleaning up failed container..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true
echo "$LOG_PREFIX ✓ Cleaned up container: $CONTAINER_NAME"
echo ""

# Step 5: Pull and start container with last working tag
echo "$LOG_PREFIX [5/5] Deploying rollback container..."

echo "$LOG_PREFIX   Pulling image: $ROLLBACK_IMAGE"
if ! docker pull "$ROLLBACK_IMAGE"; then
  echo "$LOG_PREFIX ✗ Failed to pull rollback image"
  exit 1
fi
echo "$LOG_PREFIX   ✓ Image pulled successfully"

echo "$LOG_PREFIX   Starting container with previous configuration..."

# Build the docker run command
RUN_CMD="docker run -d \
  --name \"$CONTAINER_NAME\" \
  --restart unless-stopped"

# Add extracted configuration
[ -n "$PORT_ARGS" ] && RUN_CMD="$RUN_CMD $PORT_ARGS"
[ -n "$VOLUME_ARGS" ] && RUN_CMD="$RUN_CMD $VOLUME_ARGS"
[ -n "$NETWORK_ARGS" ] && RUN_CMD="$RUN_CMD $NETWORK_ARGS"
[ -n "$ENV_ARGS" ] && RUN_CMD="$RUN_CMD $ENV_ARGS"

RUN_CMD="$RUN_CMD \"$ROLLBACK_IMAGE\""

# Execute the command
eval $RUN_CMD

echo "$LOG_PREFIX   ✓ Container started: $CONTAINER_NAME"
echo ""

# Verify container is running
echo "$LOG_PREFIX Verifying rollback success..."
sleep 5

if docker ps --filter "name=$CONTAINER_NAME" --filter "status=running" | grep -q "$CONTAINER_NAME"; then
  echo "$LOG_PREFIX ✓ Container is running successfully"
  echo ""
  echo "$LOG_PREFIX ==================================================================="
  echo "$LOG_PREFIX ===         ROLLBACK COMPLETED SUCCESSFULLY                    ==="
  echo "$LOG_PREFIX ==================================================================="
  echo "$LOG_PREFIX Rolled back to: $ROLLBACK_IMAGE"
  echo "$LOG_PREFIX Container: $CONTAINER_NAME"
  exit 0
else
  echo "$LOG_PREFIX ✗ Container failed to start after rollback"
  echo "$LOG_PREFIX   Showing container logs:"
  docker logs "$CONTAINER_NAME" --tail=50
  echo ""
  echo "$LOG_PREFIX ==================================================================="
  echo "$LOG_PREFIX ===              ROLLBACK FAILED                               ==="
  echo "$LOG_PREFIX ==================================================================="
  exit 1
fi
