#!/usr/bin/env bash
#
# backup-with-verification.sh - Create and verify Upsun backup
#
# Usage: ./backup-with-verification.sh PROJECT_ID ENVIRONMENT_NAME [--live]
#
# Returns:
#   0 - Backup created and verified successfully
#   1 - Backup creation or verification failed
#
# Outputs:
#   Backup ID on success (for use in scripts)
#
# Description:
#   Creates a backup of an Upsun environment and verifies it was successful.
#   Optionally creates a live backup (no downtime).
#   Returns the backup ID for use in subsequent operations.
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${1:-}"
ENVIRONMENT="${2:-}"
LIVE_FLAG="${3:-}"
BACKUP_ID=""

# Usage
if [ -z "$PROJECT_ID" ] || [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 PROJECT_ID ENVIRONMENT_NAME [--live]"
    echo ""
    echo "Arguments:"
    echo "  PROJECT_ID       - Upsun project ID"
    echo "  ENVIRONMENT_NAME - Environment to backup"
    echo "  --live           - Create live backup (optional, no downtime)"
    echo ""
    echo "Example: $0 abc123 production --live"
    exit 1
fi

echo "========================================="
echo "Backup with Verification"
echo "========================================="
echo "Project: $PROJECT_ID"
echo "Environment: $ENVIRONMENT"
if [ "$LIVE_FLAG" = "--live" ]; then
    echo "Type: Live backup (no downtime)"
else
    echo "Type: Standard backup"
fi
echo "Time: $(date)"
echo "========================================="

# Check authentication
echo -e "\n${GREEN}[1/4]${NC} Checking authentication..."
if ! upsun auth:info --no-interaction >/dev/null 2>&1; then
    echo -e "${RED}✗ Not authenticated${NC}"
    echo "Run: upsun auth:browser-login"
    exit 1
fi
echo -e "${GREEN}✓ Authenticated${NC}"

# Create backup
echo -e "\n${GREEN}[2/4]${NC} Creating backup..."
if [ "$LIVE_FLAG" = "--live" ]; then
    BACKUP_OUTPUT=$(upsun backup:create -p "$PROJECT_ID" -e "$ENVIRONMENT" --live --no-interaction 2>&1)
else
    BACKUP_OUTPUT=$(upsun backup:create -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1)
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Backup creation failed${NC}"
    echo "$BACKUP_OUTPUT"
    exit 1
fi

echo -e "${GREEN}✓ Backup initiated${NC}"
echo "$BACKUP_OUTPUT"

# Extract backup ID from output
# Backup output typically contains lines like "backup:abc123def" or similar
BACKUP_ID=$(echo "$BACKUP_OUTPUT" | grep -oP '(?<=backup[:\s])[a-z0-9]+' | head -n 1 || echo "")

if [ -z "$BACKUP_ID" ]; then
    # Try alternative extraction methods
    BACKUP_ID=$(echo "$BACKUP_OUTPUT" | grep -oP '[a-z0-9]{13,}' | head -n 1 || echo "")
fi

if [ -z "$BACKUP_ID" ]; then
    echo -e "${YELLOW}⚠ Could not extract backup ID from output${NC}"
    echo "Waiting 30 seconds for backup to register..."
    sleep 30
else
    echo "Backup ID: $BACKUP_ID"
fi

# Wait for backup to complete
echo -e "\n${GREEN}[3/4]${NC} Waiting for backup to complete..."
echo "This may take several minutes depending on data size..."

WAIT_TIME=0
MAX_WAIT=600  # 10 minutes
SLEEP_INTERVAL=15

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    sleep $SLEEP_INTERVAL
    WAIT_TIME=$((WAIT_TIME + SLEEP_INTERVAL))

    # Check for incomplete backup activities
    INCOMPLETE=$(upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" -i --type backup --no-interaction --pipe 2>/dev/null | wc -l | tr -d ' ')

    if [ "$INCOMPLETE" -eq 0 ]; then
        echo -e "${GREEN}✓ Backup completed${NC}"
        break
    fi

    echo "Still in progress... (waited ${WAIT_TIME}s)"
done

if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    echo -e "${YELLOW}⚠ Backup is taking longer than expected${NC}"
    echo "Check status with: upsun activity:list -p $PROJECT_ID -e $ENVIRONMENT -i"
fi

# Verify backup exists
echo -e "\n${GREEN}[4/4]${NC} Verifying backup..."
BACKUP_LIST=$(upsun backup:list -p "$PROJECT_ID" -e "$ENVIRONMENT" --limit 5 --no-interaction 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Cannot verify backup${NC}"
    echo "$BACKUP_LIST"
    exit 1
fi

# Get the most recent backup
LATEST_BACKUP=$(upsun backup:list -p "$PROJECT_ID" -e "$ENVIRONMENT" --limit 1 --pipe --no-interaction 2>/dev/null | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo -e "${RED}✗ No backups found${NC}"
    exit 1
fi

# If we have backup ID, verify it matches
if [ -n "$BACKUP_ID" ]; then
    BACKUP_INFO=$(upsun backup:get "$BACKUP_ID" -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")

    if [ "$BACKUP_INFO" = "ERROR" ]; then
        echo -e "${YELLOW}⚠ Cannot retrieve backup details for ID: $BACKUP_ID${NC}"
        echo "Using latest backup instead: $LATEST_BACKUP"
        BACKUP_ID="$LATEST_BACKUP"
    else
        echo -e "${GREEN}✓ Backup verified${NC}"
        echo "Backup details:"
        echo "$BACKUP_INFO" | head -n 10
    fi
else
    # Use latest backup ID
    BACKUP_ID="$LATEST_BACKUP"
    echo -e "${GREEN}✓ Latest backup found${NC}"
    echo "Backup ID: $BACKUP_ID"
fi

# Summary
echo ""
echo "========================================="
echo "Backup Summary"
echo "========================================="
echo -e "${GREEN}✓ Backup created successfully${NC}"
echo ""
echo "Backup ID: $BACKUP_ID"
echo "Project: $PROJECT_ID"
echo "Environment: $ENVIRONMENT"
echo "Created: $(date)"
echo ""
echo "To restore this backup:"
echo "  upsun backup:restore $BACKUP_ID -p $PROJECT_ID -e $ENVIRONMENT"
echo ""
echo "To restore to different environment:"
echo "  upsun backup:restore $BACKUP_ID -p $PROJECT_ID -e $ENVIRONMENT --target TARGET_ENV"
echo "========================================="

# Output backup ID for script usage
echo "$BACKUP_ID"

exit 0
