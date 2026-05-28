#!/bin/bash
#
# Mount floppy disk with secure options
#
# Security options applied:
#   - noexec: Prevent executable files
#   - nosuid: Ignore setuid bits
#   - nodev:  Ignore device files
#   - umask=077: Owner-only permissions
#   - sync,flush: Immediate write-through
#
set -euo pipefail

DEVICE="${FLOPPY_DEVICE:-/dev/sde}"
MOUNT_POINT="${FLOPPY_MOUNT:-/mnt/floppy}"
KEYSTORE_DIR=".keystore"

# Check if device exists
if [ ! -b "$DEVICE" ]; then
    echo "Error: Device $DEVICE not found" >&2
    echo "Is the floppy disk inserted?" >&2
    echo "" >&2
    echo "Available block devices:" >&2
    lsblk -o NAME,SIZE,TYPE,MOUNTPOINT 2>/dev/null || ls -la /dev/sd* 2>/dev/null || true
    exit 1
fi

# Check if already mounted
if mountpoint -q "$MOUNT_POINT" 2>/dev/null; then
    echo "Already mounted at $MOUNT_POINT"
    exit 0
fi

# Create mount point if needed
if [ ! -d "$MOUNT_POINT" ]; then
    echo "Creating mount point $MOUNT_POINT (requires sudo)"
    sudo mkdir -p "$MOUNT_POINT"
fi

# Set restrictive umask for this session
umask 077

# Mount with security options
echo "Mounting $DEVICE at $MOUNT_POINT (requires sudo)"
sudo mount -t vfat "$DEVICE" "$MOUNT_POINT" \
    -o noexec,nosuid,nodev,umask=077,uid=$(id -u),gid=$(id -g),sync,flush

# Create keystore directory if it doesn't exist
if [ ! -d "$MOUNT_POINT/$KEYSTORE_DIR" ]; then
    mkdir -p "$MOUNT_POINT/$KEYSTORE_DIR"
    chmod 700 "$MOUNT_POINT/$KEYSTORE_DIR"
fi

echo "Mounted $DEVICE at $MOUNT_POINT"
echo "Keystore directory: $MOUNT_POINT/$KEYSTORE_DIR"
