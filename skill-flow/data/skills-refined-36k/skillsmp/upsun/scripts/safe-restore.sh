#!/usr/bin/env bash
#
# safe-restore.sh - Safely restore Upsun backup with validation
#
# Usage: ./safe-restore.sh PROJECT_ID ENVIRONMENT_NAME BACKUP_ID [--target TARGET_ENV]
#
# Returns:
#   0 - Restore completed successfully
#   1 - Restore failed or validation failed
#
# Description:
#   Performs a safe backup restore with the following steps:
#   1. Verifies backup exists and is valid
#   2. Creates a pre-restore safety backup
#   3. Performs the restore
#   4. Validates the restored environment
#   5. Provides rollback instructions if needed
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${1:-}"
ENVIRONMENT="${2:-}"
BACKUP_ID="${3:-}"
TARGET_FLAG="${4:-}"
TARGET_ENV="${5:-}"
PRE_RESTORE_BACKUP_ID=""

# Usage
if [ -z "$PROJECT_ID" ] || [ -z "$ENVIRONMENT" ] || [ -z "$BACKUP_ID" ]; then
    echo "Usage: $0 PROJECT_ID ENVIRONMENT_NAME BACKUP_ID [--target TARGET_ENV]"
    echo ""
    echo "Arguments:"
    echo "  PROJECT_ID       - Upsun project ID"
    echo "  ENVIRONMENT_NAME - Source environment (where backup is from)"
    echo "  BACKUP_ID        - Backup ID to restore"
    echo "  --target         - Restore to different environment (optional)"
    echo "  TARGET_ENV       - Target environment name (required if --target used)"
    echo ""
    echo "Example: $0 abc123 production backup_id_123"
    echo "Example: $0 abc123 production backup_id_123 --target staging"
    exit 1
fi

# Determine actual target environment
ACTUAL_TARGET="$ENVIRONMENT"
if [ "$TARGET_FLAG" = "--target" ] && [ -n "$TARGET_ENV" ]; then
    ACTUAL_TARGET="$TARGET_ENV"
fi

echo "========================================="
echo "Safe Backup Restore"
echo "========================================="
echo "Project: $PROJECT_ID"
echo "Backup from: $ENVIRONMENT"
echo "Backup ID: $BACKUP_ID"
echo "Restore to: $ACTUAL_TARGET"
echo "Time: $(date)"
echo "========================================="

# Warning for production
if [[ "$ACTUAL_TARGET" == *"production"* ]] || [[ "$ACTUAL_TARGET" == *"main"* ]]; then
    echo ""
    echo -e "${RED}⚠️  WARNING: Restoring to production environment!${NC}"
    echo ""
    read -p "Are you sure you want to continue? (type 'yes' to confirm): " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "Restore cancelled."
        exit 1
    fi
fi

# Check authentication
echo -e "\n${GREEN}[1/7]${NC} Checking authentication..."
if ! upsun auth:info --no-interaction >/dev/null 2>&1; then
    echo -e "${RED}✗ Not authenticated${NC}"
    echo "Run: upsun auth:browser-login"
    exit 1
fi
echo -e "${GREEN}✓ Authenticated${NC}"

# Verify backup exists
echo -e "\n${GREEN}[2/7]${NC} Verifying backup exists..."
BACKUP_INFO=$(upsun backup:get "$BACKUP_ID" -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")

if [ "$BACKUP_INFO" = "ERROR" ]; then
    echo -e "${RED}✗ Backup not found or invalid${NC}"
    echo "Backup ID: $BACKUP_ID"
    echo ""
    echo "List available backups:"
    echo "  upsun backup:list -p $PROJECT_ID -e $ENVIRONMENT"
    exit 1
fi

echo -e "${GREEN}✓ Backup verified${NC}"
echo "Backup details:"
echo "$BACKUP_INFO" | head -n 10

# Create pre-restore safety backup
echo -e "\n${GREEN}[3/7]${NC} Creating pre-restore safety backup..."
echo "Target environment: $ACTUAL_TARGET"

PRE_RESTORE_OUTPUT=$(upsun backup:create -p "$PROJECT_ID" -e "$ACTUAL_TARGET" --live --no-interaction 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Pre-restore backup failed${NC}"
    echo "$PRE_RESTORE_OUTPUT"
    echo ""
    echo -e "${RED}Cannot proceed without safety backup${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-restore backup initiated${NC}"

# Extract pre-restore backup ID
PRE_RESTORE_BACKUP_ID=$(echo "$PRE_RESTORE_OUTPUT" | grep -oP '(?<=backup[:\s])[a-z0-9]+' | head -n 1 || echo "")

if [ -z "$PRE_RESTORE_BACKUP_ID" ]; then
    PRE_RESTORE_BACKUP_ID=$(echo "$PRE_RESTORE_OUTPUT" | grep -oP '[a-z0-9]{13,}' | head -n 1 || echo "")
fi

if [ -n "$PRE_RESTORE_BACKUP_ID" ]; then
    echo "Pre-restore backup ID: $PRE_RESTORE_BACKUP_ID"
else
    echo -e "${YELLOW}⚠ Could not extract pre-restore backup ID${NC}"
fi

# Wait for pre-restore backup to complete
echo "Waiting for pre-restore backup to complete (30 seconds)..."
sleep 30

# Perform restore
echo -e "\n${GREEN}[4/7]${NC} Performing restore..."
echo "This may take several minutes..."

if [ "$TARGET_FLAG" = "--target" ] && [ -n "$TARGET_ENV" ]; then
    RESTORE_OUTPUT=$(upsun backup:restore "$BACKUP_ID" -p "$PROJECT_ID" -e "$ENVIRONMENT" --target "$TARGET_ENV" --no-interaction 2>&1)
else
    RESTORE_OUTPUT=$(upsun backup:restore "$BACKUP_ID" -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1)
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Restore failed${NC}"
    echo "$RESTORE_OUTPUT"
    echo ""
    echo -e "${BLUE}Rollback information:${NC}"
    if [ -n "$PRE_RESTORE_BACKUP_ID" ]; then
        echo "Restore pre-restore backup with:"
        echo "  upsun backup:restore $PRE_RESTORE_BACKUP_ID -p $PROJECT_ID -e $ACTUAL_TARGET"
    else
        echo "Check recent backups:"
        echo "  upsun backup:list -p $PROJECT_ID -e $ACTUAL_TARGET"
    fi
    exit 1
fi

echo -e "${GREEN}✓ Restore initiated${NC}"
echo "$RESTORE_OUTPUT"

# Wait for restore to complete
echo -e "\n${GREEN}[5/7]${NC} Waiting for restore to complete..."
echo "This may take 5-15 minutes depending on data size..."

WAIT_TIME=0
MAX_WAIT=900  # 15 minutes
SLEEP_INTERVAL=30

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    sleep $SLEEP_INTERVAL
    WAIT_TIME=$((WAIT_TIME + SLEEP_INTERVAL))

    # Check for incomplete restore activities
    INCOMPLETE=$(upsun activity:list -p "$PROJECT_ID" -e "$ACTUAL_TARGET" -i --type backup --no-interaction --pipe 2>/dev/null | wc -l | tr -d ' ')

    if [ "$INCOMPLETE" -eq 0 ]; then
        echo -e "${GREEN}✓ Restore completed${NC}"
        break
    fi

    echo "Still in progress... (waited ${WAIT_TIME}s / ${MAX_WAIT}s)"
done

if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    echo -e "${YELLOW}⚠ Restore is taking longer than expected${NC}"
    echo "Check status with: upsun activity:list -p $PROJECT_ID -e $ACTUAL_TARGET -i"
fi

# Validate environment
echo -e "\n${GREEN}[6/7]${NC} Validating restored environment..."

# Check environment status
ENV_STATUS=$(upsun environment:info -p "$PROJECT_ID" -e "$ACTUAL_TARGET" status --no-interaction 2>&1 || echo "ERROR")

if [ "$ENV_STATUS" = "ERROR" ]; then
    echo -e "${RED}✗ Cannot access environment after restore${NC}"
    echo ""
    echo -e "${BLUE}Rollback recommended${NC}"
    if [ -n "$PRE_RESTORE_BACKUP_ID" ]; then
        echo "Restore pre-restore backup with:"
        echo "  upsun backup:restore $PRE_RESTORE_BACKUP_ID -p $PROJECT_ID -e $ACTUAL_TARGET"
    fi
    exit 1
elif [[ "$ENV_STATUS" == *"active"* ]]; then
    echo -e "${GREEN}✓ Environment is active${NC}"
else
    echo -e "${YELLOW}⚠ Environment status: $ENV_STATUS${NC}"
fi

# Get environment URL
ENV_URL=$(upsun environment:url -p "$PROJECT_ID" -e "$ACTUAL_TARGET" --primary --pipe --no-interaction 2>/dev/null || echo "")

if [ -n "$ENV_URL" ]; then
    echo "Environment URL: $ENV_URL"

    # Test HTTP accessibility
    echo "Testing HTTP accessibility..."
    HTTP_STATUS=$(curl -Is -m 10 "$ENV_URL" 2>/dev/null | head -n 1 || echo "FAILED")

    if [[ "$HTTP_STATUS" == *"200"* ]] || [[ "$HTTP_STATUS" == *"301"* ]] || [[ "$HTTP_STATUS" == *"302"* ]]; then
        echo -e "${GREEN}✓ Environment is accessible (HTTP: $HTTP_STATUS)${NC}"
    elif [ "$HTTP_STATUS" = "FAILED" ]; then
        echo -e "${YELLOW}⚠ Cannot connect to environment${NC}"
    else
        echo -e "${YELLOW}⚠ Unexpected HTTP status: $HTTP_STATUS${NC}"
    fi
fi

# Final summary
echo -e "\n${GREEN}[7/7]${NC} Restore complete"

echo ""
echo "========================================="
echo "Restore Summary"
echo "========================================="
echo -e "${GREEN}✓ Restore completed successfully${NC}"
echo ""
echo "Restored backup: $BACKUP_ID"
echo "From environment: $ENVIRONMENT"
echo "To environment: $ACTUAL_TARGET"
echo "Completed: $(date)"
echo ""
if [ -n "$PRE_RESTORE_BACKUP_ID" ]; then
    echo -e "${BLUE}Safety backup created:${NC} $PRE_RESTORE_BACKUP_ID"
    echo "Keep this backup for potential rollback"
    echo ""
    echo "To rollback if needed:"
    echo "  upsun backup:restore $PRE_RESTORE_BACKUP_ID -p $PROJECT_ID -e $ACTUAL_TARGET"
    echo ""
fi
echo "Next steps:"
echo "1. Test critical functionality"
echo "2. Check application logs: upsun logs -p $PROJECT_ID -e $ACTUAL_TARGET --tail"
echo "3. Verify data integrity"
if [ -n "$ENV_URL" ]; then
    echo "4. Access environment: $ENV_URL"
fi
echo "========================================="

exit 0
