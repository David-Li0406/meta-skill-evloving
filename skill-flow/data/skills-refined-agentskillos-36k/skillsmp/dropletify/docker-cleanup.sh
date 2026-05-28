#!/bin/bash
#
# Docker Cleanup Script for DigitalOcean Droplets
# This script maintains a clean Docker environment by:
# - Keeping only the 5 most recent images per repository
# - Pruning unused Docker resources (containers, networks, volumes)
# - Logging cleanup operations
#
# Usage: Run via cron (recommended daily at 3 AM)
# Crontab entry: 0 3 * * * /usr/local/bin/docker-cleanup.sh >> /var/log/docker-cleanup.log 2>&1
#

set -e

RETENTION_COUNT=5
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

echo "$LOG_PREFIX === Starting Docker cleanup ==="

# Function to cleanup images for a specific repository
cleanup_repository_images() {
  local repo=$1
  local image_ids=$(docker images "$repo" --format "{{.ID}}" 2>/dev/null || echo "")
  
  if [ -z "$image_ids" ]; then
    return 0
  fi
  
  local total_images=$(echo "$image_ids" | wc -l)
  echo "$LOG_PREFIX Repository: $repo - Found $total_images image(s)"
  
  if [ "$total_images" -gt "$RETENTION_COUNT" ]; then
    local images_to_delete=$(echo "$image_ids" | tail -n +$((RETENTION_COUNT + 1)))
    local delete_count=$(echo "$images_to_delete" | wc -l)
    
    echo "$LOG_PREFIX   Removing $delete_count old image(s)..."
    echo "$images_to_delete" | xargs -r docker rmi -f 2>/dev/null || true
    echo "$LOG_PREFIX   ✓ Cleaned up $delete_count image(s) from $repo"
  else
    echo "$LOG_PREFIX   ✓ Only $total_images image(s), no cleanup needed"
  fi
}

# Get unique repository names (excluding <none>)
echo "$LOG_PREFIX Scanning repositories..."
repositories=$(docker images --format "{{.Repository}}" | grep -v "<none>" | sort -u)

if [ -z "$repositories" ]; then
  echo "$LOG_PREFIX No repositories found"
else
  repo_count=$(echo "$repositories" | wc -l)
  echo "$LOG_PREFIX Found $repo_count unique repository/repositories"
  echo ""
  
  # Cleanup each repository
  while IFS= read -r repo; do
    cleanup_repository_images "$repo"
  done <<< "$repositories"
fi

echo ""
echo "$LOG_PREFIX Pruning unused Docker resources..."

# Remove stopped containers
stopped_containers=$(docker ps -aq -f status=exited 2>/dev/null || echo "")
if [ -n "$stopped_containers" ]; then
  stopped_count=$(echo "$stopped_containers" | wc -l)
  echo "$LOG_PREFIX   Removing $stopped_count stopped container(s)..."
  echo "$stopped_containers" | xargs -r docker rm 2>/dev/null || true
  echo "$LOG_PREFIX   ✓ Removed stopped containers"
else
  echo "$LOG_PREFIX   ✓ No stopped containers to remove"
fi

# Remove dangling images
dangling_images=$(docker images -f "dangling=true" -q 2>/dev/null || echo "")
if [ -n "$dangling_images" ]; then
  dangling_count=$(echo "$dangling_images" | wc -l)
  echo "$LOG_PREFIX   Removing $dangling_count dangling image(s)..."
  echo "$dangling_images" | xargs -r docker rmi -f 2>/dev/null || true
  echo "$LOG_PREFIX   ✓ Removed dangling images"
else
  echo "$LOG_PREFIX   ✓ No dangling images to remove"
fi

# Prune unused networks
echo "$LOG_PREFIX   Pruning unused networks..."
docker network prune -f >/dev/null 2>&1 || true
echo "$LOG_PREFIX   ✓ Pruned unused networks"

# Prune unused volumes (careful: only removes anonymous volumes)
echo "$LOG_PREFIX   Pruning unused volumes..."
docker volume prune -f >/dev/null 2>&1 || true
echo "$LOG_PREFIX   ✓ Pruned unused volumes"

echo ""
echo "$LOG_PREFIX === Disk usage after cleanup ==="
df -h / | grep -E 'Filesystem|/dev/'

echo ""
echo "$LOG_PREFIX === Remaining Docker images ==="
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}" | head -20

# Show total Docker disk usage
echo ""
echo "$LOG_PREFIX === Docker disk usage ==="
docker system df

echo ""
echo "$LOG_PREFIX === Cleanup completed successfully ==="
