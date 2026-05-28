#!/usr/bin/env bash
#
# health-check.sh - Comprehensive Upsun environment health check
#
# Usage: ./health-check.sh PROJECT_ID ENVIRONMENT_NAME
#
# Returns:
#   0 - Environment is healthy
#   1 - Issues detected
#   2 - Critical issues detected
#
# Description:
#   Performs a comprehensive health check on an Upsun environment including:
#   - Deployment status
#   - Incomplete activities
#   - Resource usage
#   - Service status
#   - Recent errors
#   - Performance metrics
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
ISSUES=0
CRITICAL=0

# Usage
if [ -z "$PROJECT_ID" ] || [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 PROJECT_ID ENVIRONMENT_NAME"
    echo ""
    echo "Example: $0 abc123 production"
    exit 2
fi

echo "========================================="
echo "Upsun Environment Health Check"
echo "========================================="
echo "Project: $PROJECT_ID"
echo "Environment: $ENVIRONMENT"
echo "Time: $(date)"
echo "========================================="

# Check authentication
echo -e "\n${GREEN}[1/8]${NC} Checking authentication..."
if ! upsun auth:info --no-interaction >/dev/null 2>&1; then
    echo -e "${RED}✗ Not authenticated${NC}"
    echo "Run: upsun auth:browser-login"
    exit 2
fi
echo -e "${GREEN}✓ Authenticated${NC}"

# Check environment status
echo -e "\n${GREEN}[2/8]${NC} Checking environment status..."
ENV_STATUS=$(upsun environment:info -p "$PROJECT_ID" -e "$ENVIRONMENT" status --no-interaction 2>&1 || echo "ERROR")

if [ "$ENV_STATUS" = "ERROR" ]; then
    echo -e "${RED}✗ Cannot access environment${NC}"
    ((CRITICAL++))
else
    if [[ "$ENV_STATUS" == *"active"* ]]; then
        echo -e "${GREEN}✓ Environment is active${NC}"
    elif [[ "$ENV_STATUS" == *"inactive"* ]]; then
        echo -e "${YELLOW}⚠ Environment is inactive${NC}"
        ((ISSUES++))
    elif [[ "$ENV_STATUS" == *"paused"* ]]; then
        echo -e "${YELLOW}⚠ Environment is paused${NC}"
        ((ISSUES++))
    else
        echo -e "${YELLOW}⚠ Environment status: $ENV_STATUS${NC}"
        ((ISSUES++))
    fi
fi

# Check for incomplete activities
echo -e "\n${GREEN}[3/8]${NC} Checking for incomplete activities..."
INCOMPLETE_COUNT=$(upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" -i --no-interaction --pipe 2>/dev/null | wc -l | tr -d ' ')

if [ "$INCOMPLETE_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✓ No incomplete activities${NC}"
else
    echo -e "${YELLOW}⚠ $INCOMPLETE_COUNT incomplete activities detected${NC}"
    echo "Recent incomplete activities:"
    upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" -i --no-interaction --limit 3 2>/dev/null || echo "Cannot retrieve activities"
    ((ISSUES++))
fi

# Check recent errors
echo -e "\n${GREEN}[4/8]${NC} Checking for recent errors..."
ERROR_LOG=$(upsun logs -p "$PROJECT_ID" -e "$ENVIRONMENT" --type error --lines 10 --no-interaction 2>&1 || echo "")

if [ -z "$ERROR_LOG" ] || [[ "$ERROR_LOG" == *"No log"* ]]; then
    echo -e "${GREEN}✓ No recent errors in logs${NC}"
else
    ERROR_COUNT=$(echo "$ERROR_LOG" | grep -ci "error" || echo "0")
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo -e "${YELLOW}⚠ Found $ERROR_COUNT error messages in recent logs${NC}"
        echo "Sample errors:"
        echo "$ERROR_LOG" | head -n 5
        ((ISSUES++))
    else
        echo -e "${GREEN}✓ No critical errors detected${NC}"
    fi
fi

# Check resources
echo -e "\n${GREEN}[5/8]${NC} Checking resource allocation..."
RESOURCES=$(upsun resources -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")

if [ "$RESOURCES" = "ERROR" ]; then
    echo -e "${YELLOW}⚠ Cannot retrieve resource information${NC}"
    ((ISSUES++))
else
    echo "$RESOURCES" | head -n 15
fi

# Check CPU usage
echo -e "\n${GREEN}[6/8]${NC} Checking CPU usage (last hour)..."
CPU_OUTPUT=$(upsun cpu -p "$PROJECT_ID" -e "$ENVIRONMENT" --start "-1 hour" --no-interaction 2>&1 || echo "ERROR")

if [ "$CPU_OUTPUT" = "ERROR" ]; then
    echo -e "${YELLOW}⚠ Cannot retrieve CPU metrics${NC}"
    ((ISSUES++))
else
    # Extract last CPU percentage if available
    CPU_PERCENT=$(echo "$CPU_OUTPUT" | grep -oP '\d+%' | tail -n 1 | tr -d '%' || echo "0")
    if [ "$CPU_PERCENT" -gt 90 ]; then
        echo -e "${RED}✗ High CPU usage: ${CPU_PERCENT}%${NC}"
        ((CRITICAL++))
    elif [ "$CPU_PERCENT" -gt 75 ]; then
        echo -e "${YELLOW}⚠ Elevated CPU usage: ${CPU_PERCENT}%${NC}"
        ((ISSUES++))
    else
        echo -e "${GREEN}✓ CPU usage normal: ${CPU_PERCENT}%${NC}"
    fi
fi

# Check memory usage
echo -e "\n${GREEN}[7/8]${NC} Checking memory usage (last hour)..."
MEM_OUTPUT=$(upsun memory -p "$PROJECT_ID" -e "$ENVIRONMENT" --start "-1 hour" --no-interaction 2>&1 || echo "ERROR")

if [ "$MEM_OUTPUT" = "ERROR" ]; then
    echo -e "${YELLOW}⚠ Cannot retrieve memory metrics${NC}"
    ((ISSUES++))
else
    # Extract last memory percentage if available
    MEM_PERCENT=$(echo "$MEM_OUTPUT" | grep -oP '\d+%' | tail -n 1 | tr -d '%' || echo "0")
    if [ "$MEM_PERCENT" -gt 90 ]; then
        echo -e "${RED}✗ High memory usage: ${MEM_PERCENT}%${NC}"
        ((CRITICAL++))
    elif [ "$MEM_PERCENT" -gt 80 ]; then
        echo -e "${YELLOW}⚠ Elevated memory usage: ${MEM_PERCENT}%${NC}"
        ((ISSUES++))
    else
        echo -e "${GREEN}✓ Memory usage normal: ${MEM_PERCENT}%${NC}"
    fi
fi

# Check disk usage
echo -e "\n${GREEN}[8/8]${NC} Checking disk usage..."
DISK_OUTPUT=$(upsun disk -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")

if [ "$DISK_OUTPUT" = "ERROR" ]; then
    echo -e "${YELLOW}⚠ Cannot retrieve disk metrics${NC}"
    ((ISSUES++))
else
    DISK_PERCENT=$(echo "$DISK_OUTPUT" | grep -oP '\d+%' | head -n 1 | tr -d '%' || echo "0")
    if [ "$DISK_PERCENT" -gt 90 ]; then
        echo -e "${RED}✗ Disk usage critical: ${DISK_PERCENT}%${NC}"
        ((CRITICAL++))
    elif [ "$DISK_PERCENT" -gt 80 ]; then
        echo -e "${YELLOW}⚠ Disk usage high: ${DISK_PERCENT}%${NC}"
        ((ISSUES++))
    else
        echo -e "${GREEN}✓ Disk usage normal: ${DISK_PERCENT}%${NC}"
    fi
fi

# Summary
echo ""
echo "========================================="
echo "Health Check Summary"
echo "========================================="

if [ "$CRITICAL" -gt 0 ]; then
    echo -e "${RED}Status: CRITICAL${NC}"
    echo -e "${RED}Critical Issues: $CRITICAL${NC}"
    echo -e "${YELLOW}Warnings: $ISSUES${NC}"
    echo ""
    echo "Immediate action required!"
    exit 2
elif [ "$ISSUES" -gt 0 ]; then
    echo -e "${YELLOW}Status: WARNING${NC}"
    echo -e "${YELLOW}Issues Detected: $ISSUES${NC}"
    echo ""
    echo "Review and address warnings."
    exit 1
else
    echo -e "${GREEN}Status: HEALTHY${NC}"
    echo -e "${GREEN}No issues detected${NC}"
    exit 0
fi
