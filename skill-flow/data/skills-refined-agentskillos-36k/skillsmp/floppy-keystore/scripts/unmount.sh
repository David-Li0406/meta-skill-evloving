#!/bin/bash
#
# Safely unmount floppy disk
#
# This script syncs the filesystem before unmounting to ensure
# all data is written to the disk.
#
set -euo pipefail

MOUNT_POINT="${FLOPPY_MOUNT:-/mnt/floppy}"

# Check if mounted
if ! mountpoint -q "$MOUNT_POINT" 2>/dev/null; then
    echo "Not mounted at $MOUNT_POINT"
    exit 0
fi

# Sync filesystem before unmount
echo "Syncing filesystem..."
sync

# Unmount
echo "Unmounting $MOUNT_POINT (requires sudo)"
sudo umount "$MOUNT_POINT"

echo "Unmounted $MOUNT_POINT"
echo "Floppy disk can now be safely removed"
