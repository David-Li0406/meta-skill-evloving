#!/bin/bash
# UpdraftPlus Backup Configuration Checker
# Validates UpdraftPlus plugin configuration and permissions

set -e

CONTAINER_NAME=${1:-wordpress-clemence}

echo "========================================"
echo "UpdraftPlus Backup Validator"
echo "========================================"
echo ""
echo "Container: $CONTAINER_NAME"
echo ""

ERRORS=0
WARNINGS=0

# ========================================
# 1. Check if UpdraftPlus is installed
# ========================================

echo "=== UpdraftPlus Installation ==="
echo ""

# Check plugin directory exists
if ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME test -d /var/www/html/wp-content/plugins/updraftplus" 2>/dev/null; then
    echo "✅ UpdraftPlus plugin directory found"

    # Check if activated (via database)
    PLUGIN_STATUS=$(ssh automation@69.62.108.82 "docker exec mysql-clemence mysql -u clemence_user -pClemenceDB2025 clemence_db -N -e \"SELECT option_value FROM wp_options WHERE option_name='active_plugins';\" 2>/dev/null" | grep -c "updraftplus" || echo 0)

    if [ "$PLUGIN_STATUS" -gt 0 ]; then
        echo "✅ UpdraftPlus is active"
    else
        echo "❌ ERROR: UpdraftPlus installed but not active"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "❌ ERROR: UpdraftPlus not installed"
    ERRORS=$((ERRORS + 1))
    echo ""
    echo "Install with:"
    echo "  wp plugin install updraftplus --activate --allow-root"
    exit 1
fi

echo ""

# ========================================
# 2. Check FS_METHOD configuration
# ========================================

echo "=== WordPress Filesystem Method ==="
echo ""

FS_METHOD=$(ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME grep -c \"define('FS_METHOD'\" /var/www/html/wp-config.php" 2>/dev/null || echo 0)

if [ "$FS_METHOD" -gt 0 ]; then
    # Get the value
    FS_VALUE=$(ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME grep \"define('FS_METHOD'\" /var/www/html/wp-config.php" 2>/dev/null | sed "s/.*'FS_METHOD',\s*'\([^']*\)'.*/\1/")

    if [ "$FS_VALUE" = "direct" ]; then
        echo "✅ FS_METHOD set to 'direct' (correct)"
    else
        echo "⚠️  WARNING: FS_METHOD set to '$FS_VALUE' (recommended: 'direct')"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "❌ ERROR: FS_METHOD not defined in wp-config.php"
    echo "   WordPress will ask for FTP credentials"
    ERRORS=$((ERRORS + 1))
    echo ""
    echo "Fix with:"
    echo "  docker cp $CONTAINER_NAME:/var/www/html/wp-config.php /tmp/wp-config.php"
    echo "  sed -i \"130a define('FS_METHOD', 'direct');\" /tmp/wp-config.php"
    echo "  docker cp /tmp/wp-config.php $CONTAINER_NAME:/var/www/html/wp-config.php"
fi

echo ""

# ========================================
# 3. Check updraft directory permissions
# ========================================

echo "=== UpdraftPlus Directory Permissions ==="
echo ""

UPDRAFT_DIR="/var/www/html/wp-content/updraft"

# Check if directory exists
if ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME test -d $UPDRAFT_DIR" 2>/dev/null; then
    echo "✅ updraft/ directory exists"

    # Check ownership
    OWNER=$(ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME stat -c '%U:%G' $UPDRAFT_DIR" 2>/dev/null || echo "unknown")

    if [ "$OWNER" = "www-data:www-data" ]; then
        echo "✅ Owner: www-data:www-data (correct)"
    else
        echo "❌ ERROR: Owner: $OWNER (should be www-data:www-data)"
        ERRORS=$((ERRORS + 1))
        echo "   Fix with: chown -R www-data:www-data $UPDRAFT_DIR"
    fi

    # Check permissions
    PERMS=$(ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME stat -c '%a' $UPDRAFT_DIR" 2>/dev/null || echo "000")

    if [ "$PERMS" = "775" ] || [ "$PERMS" = "755" ]; then
        echo "✅ Permissions: $PERMS (correct)"
    else
        echo "⚠️  WARNING: Permissions: $PERMS (recommended: 775)"
        WARNINGS=$((WARNINGS + 1))
        echo "   Fix with: chmod 775 $UPDRAFT_DIR"
    fi

    # Test write access
    if ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME touch $UPDRAFT_DIR/test-write.txt 2>/dev/null && docker exec $CONTAINER_NAME rm $UPDRAFT_DIR/test-write.txt 2>/dev/null"; then
        echo "✅ Write test: OK (WordPress can write backups)"
    else
        echo "❌ ERROR: Write test FAILED (WordPress cannot write backups)"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "⚠️  WARNING: updraft/ directory doesn't exist yet"
    echo "   Will be created on first backup"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""

# ========================================
# 4. Check backup files
# ========================================

echo "=== Existing Backups ==="
echo ""

if ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME test -d $UPDRAFT_DIR" 2>/dev/null; then
    BACKUP_COUNT=$(ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME find $UPDRAFT_DIR -name 'backup_*.zip' -o -name 'backup_*.gz' | wc -l" 2>/dev/null || echo 0)

    if [ "$BACKUP_COUNT" -gt 0 ]; then
        echo "✅ $BACKUP_COUNT backup file(s) found"

        # List recent backups
        echo ""
        echo "Recent backups:"
        ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME ls -lh $UPDRAFT_DIR" 2>/dev/null | grep -E 'backup_.*\.(zip|gz)' | tail -5 | awk '{print "  - " $9 " (" $5 ")"}'
    else
        echo "⚠️  WARNING: No backup files found"
        echo "   Run a manual backup to test"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "⚠️  No backup directory yet"
fi

echo ""

# ========================================
# 5. Check backup schedule (if configured)
# ========================================

echo "=== Backup Schedule ==="
echo ""

# Check if scheduled backups are configured via database
SCHEDULE_CONFIG=$(ssh automation@69.62.108.82 "docker exec mysql-clemence mysql -u clemence_user -pClemenceDB2025 clemence_db -N -e \"SELECT option_value FROM wp_options WHERE option_name='updraft_interval';\" 2>/dev/null" || echo "")

if [ -n "$SCHEDULE_CONFIG" ] && [ "$SCHEDULE_CONFIG" != "manual" ]; then
    echo "✅ Automatic backups scheduled: $SCHEDULE_CONFIG"
else
    echo "⚠️  WARNING: No automatic backup schedule configured"
    echo "   Configure in UpdraftPlus → Settings"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""

# ========================================
# 6. Check remote storage (optional)
# ========================================

echo "=== Remote Storage ==="
echo ""

# Check if remote storage is configured
REMOTE_STORAGE=$(ssh automation@69.62.108.82 "docker exec mysql-clemence mysql -u clemence_user -pClemenceDB2025 clemence_db -N -e \"SELECT option_value FROM wp_options WHERE option_name='updraft_service';\" 2>/dev/null" || echo "")

if [ -n "$REMOTE_STORAGE" ] && [ "$REMOTE_STORAGE" != "none" ]; then
    echo "✅ Remote storage configured: $REMOTE_STORAGE"
else
    echo "⚠️  WARNING: No remote storage configured"
    echo "   Backups only stored locally (not recommended)"
    echo "   Configure in UpdraftPlus → Settings → Remote Storage"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""

# ========================================
# Summary
# ========================================

echo "========================================"
echo "Validation Summary"
echo "========================================"
echo ""
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ UpdraftPlus is properly configured!"
    echo ""
    echo "✅ Ready to create backups"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  UpdraftPlus works but has warnings"
    echo ""
    echo "Recommendations:"
    echo "  1. Configure automatic backup schedule"
    echo "  2. Set up remote storage (Google Drive, Dropbox, S3)"
    echo "  3. Test manual backup in WordPress admin"
    exit 0
else
    echo "❌ UpdraftPlus configuration has errors"
    echo ""
    echo "Critical issues to fix:"
    if [ $(ssh automation@69.62.108.82 "docker exec $CONTAINER_NAME grep -c \"define('FS_METHOD'\" /var/www/html/wp-config.php" 2>/dev/null || echo 0) -eq 0 ]; then
        echo "  1. Add FS_METHOD to wp-config.php"
    fi
    echo "  2. Fix updraft/ directory permissions"
    echo "  3. Verify www-data ownership"
    exit 1
fi
