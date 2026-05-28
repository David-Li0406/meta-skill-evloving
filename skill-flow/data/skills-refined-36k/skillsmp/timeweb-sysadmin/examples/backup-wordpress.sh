#!/bin/bash
# WordPress Backup Script — S3 Cold Storage
# Run via cron or manually from local workspace
#
# Usage:
#   ./backup-wordpress.sh truesharing 45.8.96.209
#   ./backup-wordpress.sh rockcult 81.200.144.104

set -euo pipefail

# ============================================
# Configuration
# ============================================
SITE_NAME="${1:-}"
SERVER_IP="${2:-}"
BACKUP_BUCKET="s3://backups-cold"
DATE=$(date +%Y-%m-%d_%H%M)
BACKUP_DIR="/tmp/backups"
KEEP_DAILY=7
KEEP_WEEKLY=4

# S3 Configuration (Timeweb)
export AWS_ENDPOINT_URL="https://s3.twcstorage.ru"
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY should be in environment

if [[ -z "$SITE_NAME" || -z "$SERVER_IP" ]]; then
    echo "Usage: $0 <site-name> <server-ip>"
    echo "Example: $0 truesharing 45.8.96.209"
    exit 1
fi

echo "🔄 Starting backup for $SITE_NAME ($SERVER_IP)..."

# ============================================
# Create local temp directory
# ============================================
mkdir -p "$BACKUP_DIR/$SITE_NAME"
cd "$BACKUP_DIR/$SITE_NAME"

# ============================================
# Backup Database
# ============================================
echo "📦 Backing up database..."
ssh root@"$SERVER_IP" "mysqldump --single-transaction --quick wordpress" \
    | gzip > "db_${DATE}.sql.gz"

# ============================================
# Backup Files (wp-content)
# ============================================
echo "📦 Backing up wp-content..."
ssh root@"$SERVER_IP" "tar czf - /var/www/html/wp-content" \
    > "files_${DATE}.tar.gz"

# ============================================
# Upload to S3 Cold Storage
# ============================================
echo "☁️ Uploading to S3..."
aws s3 cp "db_${DATE}.sql.gz" "$BACKUP_BUCKET/$SITE_NAME/daily/db_${DATE}.sql.gz"
aws s3 cp "files_${DATE}.tar.gz" "$BACKUP_BUCKET/$SITE_NAME/daily/files_${DATE}.tar.gz"

# ============================================
# Cleanup Old Backups
# ============================================
echo "🧹 Cleaning up old backups..."

# List and remove old daily backups (keep last $KEEP_DAILY)
aws s3 ls "$BACKUP_BUCKET/$SITE_NAME/daily/" \
    | grep "db_" \
    | sort -r \
    | tail -n +$((KEEP_DAILY + 1)) \
    | awk '{print $4}' \
    | xargs -I {} aws s3 rm "$BACKUP_BUCKET/$SITE_NAME/daily/{}" 2>/dev/null || true

# Weekly backup (every Sunday)
if [[ $(date +%u) -eq 7 ]]; then
    echo "📅 Creating weekly backup..."
    aws s3 cp "$BACKUP_BUCKET/$SITE_NAME/daily/db_${DATE}.sql.gz" \
              "$BACKUP_BUCKET/$SITE_NAME/weekly/db_${DATE}.sql.gz"
    aws s3 cp "$BACKUP_BUCKET/$SITE_NAME/daily/files_${DATE}.tar.gz" \
              "$BACKUP_BUCKET/$SITE_NAME/weekly/files_${DATE}.tar.gz"
fi

# Local cleanup
rm -rf "$BACKUP_DIR/$SITE_NAME"

echo "✅ Backup complete for $SITE_NAME"
echo "   DB: $BACKUP_BUCKET/$SITE_NAME/daily/db_${DATE}.sql.gz"
echo "   Files: $BACKUP_BUCKET/$SITE_NAME/daily/files_${DATE}.tar.gz"
