#!/bin/bash
# WordPress Restore Script — From S3 Cold Storage
#
# Usage:
#   ./restore-wordpress.sh truesharing 45.8.96.209 2025-01-21_1200

set -euo pipefail

# ============================================
# Configuration
# ============================================
SITE_NAME="${1:-}"
SERVER_IP="${2:-}"
BACKUP_DATE="${3:-}"
BACKUP_BUCKET="s3://backups-cold"
RESTORE_DIR="/tmp/restore"

# S3 Configuration (Timeweb)
export AWS_ENDPOINT_URL="https://s3.twcstorage.ru"

if [[ -z "$SITE_NAME" || -z "$SERVER_IP" || -z "$BACKUP_DATE" ]]; then
    echo "Usage: $0 <site-name> <server-ip> <backup-date>"
    echo "Example: $0 truesharing 45.8.96.209 2025-01-21_1200"
    echo ""
    echo "List available backups:"
    echo "  aws s3 ls $BACKUP_BUCKET/$SITE_NAME/daily/"
    exit 1
fi

echo "⚠️  WARNING: This will RESTORE $SITE_NAME from backup $BACKUP_DATE"
echo "    Server: $SERVER_IP"
read -p "Are you sure? (type 'yes' to confirm): " confirm
if [[ "$confirm" != "yes" ]]; then
    echo "Aborted."
    exit 1
fi

echo "🔄 Starting restore for $SITE_NAME..."

# ============================================
# Download from S3
# ============================================
mkdir -p "$RESTORE_DIR/$SITE_NAME"
cd "$RESTORE_DIR/$SITE_NAME"

echo "📥 Downloading backup from S3..."
aws s3 cp "$BACKUP_BUCKET/$SITE_NAME/daily/db_${BACKUP_DATE}.sql.gz" ./
aws s3 cp "$BACKUP_BUCKET/$SITE_NAME/daily/files_${BACKUP_DATE}.tar.gz" ./

# ============================================
# Restore Database
# ============================================
echo "📦 Restoring database..."
gunzip -c "db_${BACKUP_DATE}.sql.gz" | ssh root@"$SERVER_IP" "mysql wordpress"

# ============================================
# Restore Files
# ============================================
echo "📦 Restoring files..."
cat "files_${BACKUP_DATE}.tar.gz" | ssh root@"$SERVER_IP" "tar xzf - -C /"

# ============================================
# Fix Permissions
# ============================================
echo "🔧 Fixing permissions..."
ssh root@"$SERVER_IP" "chown -R www-data:www-data /var/www/html/wp-content"

# ============================================
# Cleanup
# ============================================
rm -rf "$RESTORE_DIR/$SITE_NAME"

echo "✅ Restore complete for $SITE_NAME from $BACKUP_DATE"
echo "   Please verify the site: https://${SITE_NAME}.ru"
