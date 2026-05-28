#!/bin/bash
# Generate fix script template

if [ -z "$1" ]; then
    echo "Usage: $0 <fix-name> '<fix-description>'"
    exit 1
fi

FIX_NAME=$1
FIX_DESC=$2
DATE=$(date +%Y%m%d-%H%M%S)

cat << FIX_SCRIPT
#!/bin/bash
# Fix script for: $FIX_DESC
# Generated: $DATE
# Usage: bash $FIX_NAME-fix.sh

set -e  # Exit on error

echo "=== Starting Fix: $FIX_DESC ==="

# Backup configuration
BACKUP_DIR="~/backup-\${DATE}"
mkdir -p \$BACKUP_DIR
echo "Backup directory: \$BACKUP_DIR"

# TODO: Add backup commands here
# cp /path/to/config \$BACKUP_DIR/

# TODO: Add fix commands here
# Example:
# sed -i 's|old|new|g' /path/to/config
# systemctl restart service

# Verification
echo "=== Verifying Fix ==="
# TODO: Add verification commands here
# Example:
# systemctl status service
# ss -tlnp | grep :port

echo "=== Fix Complete ==="
echo "Backup location: \$BACKUP_DIR"
FIX_SCRIPT
