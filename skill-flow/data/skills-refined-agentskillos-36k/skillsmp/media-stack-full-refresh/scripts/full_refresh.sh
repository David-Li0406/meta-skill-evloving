#!/bin/bash
#
# Full Media Stack Refresh Script
#
# Refreshes entire media infrastructure after Real-Debrid changes:
# 1. Restart Zurg (rebuild torrent database)
# 2. Restart Rclone (clear mount cache)
# 3. Verify mount health
# 4. (Optional) Restart Jellyfin
# 5. Trigger Jellyfin library scan
# 6. Verify results
#
# Usage:
#   ./full_refresh.sh              # Full refresh with Jellyfin restart
#   ./full_refresh.sh --skip-jellyfin  # Skip Jellyfin restart
#
# Requirements:
#   - Docker and docker-compose
#   - Jellyfin API token in environment or script
#   - SSH access to srv759970.hstgr.cloud as automation user

set -e  # Exit on error

# Configuration
COMPOSE_DIR="/home/automation/apps/14-media-servers/jellyfin-stack"
JELLYFIN_TOKEN="${JELLYFIN_API_TOKEN:-9af5f56a66e44ee68ddeec7bd07c9db8}"
JELLYFIN_URL="http://localhost:8096"
MOUNT_PATH="/mnt/rd/shows"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
SKIP_JELLYFIN=false
if [[ "$1" == "--skip-jellyfin" ]]; then
    SKIP_JELLYFIN=true
fi

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Restart Zurg
log_info "Step 1/7: Restarting Zurg..."
docker restart zurg
sleep 10

# Verify Zurg healthy
if docker ps | grep -q "zurg.*healthy"; then
    log_info "✓ Zurg is healthy"

    # Show torrent count
    TORRENT_COUNT=$(docker logs zurg 2>&1 | grep "Compiled" | tail -1 | grep -oP '\d+(?= torrents)')
    if [ -n "$TORRENT_COUNT" ]; then
        log_info "  Compiled $TORRENT_COUNT torrents"
    fi
else
    log_error "✗ Zurg is not healthy"
    exit 1
fi

# Step 2: Restart Rclone
log_info "Step 2/7: Restarting Rclone..."
docker restart rclone
sleep 15

# Verify Rclone running
if docker ps | grep -q "rclone.*Up"; then
    log_info "✓ Rclone is running"
else
    log_error "✗ Rclone is not running"
    exit 1
fi

# Step 3: Verify mount health
log_info "Step 3/7: Verifying mount health..."
if [ -d "$MOUNT_PATH" ]; then
    SHOW_COUNT=$(ls "$MOUNT_PATH" 2>/dev/null | wc -l)
    log_info "✓ Mount accessible ($SHOW_COUNT shows found)"
else
    log_error "✗ Mount not accessible at $MOUNT_PATH"
    exit 1
fi

# Step 4: Restart Jellyfin (optional)
if [ "$SKIP_JELLYFIN" = false ]; then
    log_info "Step 4/7: Restarting Jellyfin..."
    log_warn "  This will interrupt active streams!"
    docker restart jellyfin
    sleep 30

    # Verify Jellyfin healthy
    HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' "$JELLYFIN_URL/health")
    if [ "$HTTP_CODE" = "200" ]; then
        log_info "✓ Jellyfin is healthy"
    else
        log_error "✗ Jellyfin health check failed (HTTP $HTTP_CODE)"
        exit 1
    fi
else
    log_info "Step 4/7: Skipping Jellyfin restart (--skip-jellyfin)"
fi

# Step 5: Trigger Jellyfin library scan
log_info "Step 5/7: Triggering Jellyfin library scan..."
SCAN_RESPONSE=$(curl -s -X POST "$JELLYFIN_URL/Library/Refresh" \
    -H "X-Emby-Token: $JELLYFIN_TOKEN" \
    -w '%{http_code}')

if echo "$SCAN_RESPONSE" | grep -q "20[0-4]"; then
    log_info "✓ Library scan triggered"
else
    log_error "✗ Failed to trigger scan (HTTP $SCAN_RESPONSE)"
    exit 1
fi

# Step 6: Wait for scan to complete
log_info "Step 6/7: Waiting for scan to complete..."
log_warn "  This may take 2-30 minutes depending on library size"
log_info "  Monitor progress: docker logs jellyfin --follow"

# Wait 2 minutes minimum
sleep 120

# Step 7: Verify results
log_info "Step 7/7: Verifying results..."

# Get library counts
COUNTS=$(curl -s "$JELLYFIN_URL/Items/Counts" \
    -H "X-Emby-Token: $JELLYFIN_TOKEN" 2>/dev/null)

if [ -n "$COUNTS" ]; then
    SERIES_COUNT=$(echo "$COUNTS" | grep -oP '"SeriesCount":\K\d+' || echo "0")
    EPISODE_COUNT=$(echo "$COUNTS" | grep -oP '"EpisodeCount":\K\d+' || echo "0")
    MOVIE_COUNT=$(echo "$COUNTS" | grep -oP '"MovieCount":\K\d+' || echo "0")

    log_info "✓ Library statistics retrieved"
    log_info "  Series: $SERIES_COUNT"
    log_info "  Episodes: $EPISODE_COUNT"
    log_info "  Movies: $MOVIE_COUNT"
else
    log_warn "Could not retrieve library statistics"
fi

# Final success
echo ""
log_info "========================================="
log_info "  MEDIA STACK REFRESH COMPLETED"
log_info "========================================="
log_info ""
log_info "Next steps:"
log_info "  1. Check Jellyfin web UI for new content"
log_info "  2. Run 'docker logs jellyfin --tail 50' to check for errors"
log_info "  3. If content missing, check file naming in mount"
log_info ""
