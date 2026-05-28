#!/usr/bin/env bash
#
# pre-deploy-check.sh - Pre-deployment validation for Upsun environments
#
# Usage: ./pre-deploy-check.sh PROJECT_ID ENVIRONMENT_NAME
#
# Returns:
#   0 - Safe to deploy
#   1 - Issues detected, review before deploying
#   2 - Critical issues, deployment not recommended
#
# Description:
#   Validates environment state before deployment to catch common issues:
#   - Incomplete activities
#   - Resource availability
#   - Recent deployment failures
#   - Disk space
#   - Service status
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
WARNINGS=0
BLOCKERS=0

# Usage
if [ -z "$PROJECT_ID" ] || [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 PROJECT_ID ENVIRONMENT_NAME"
    echo ""
    echo "Example: $0 abc123 production"
    exit 2
fi

echo "========================================="
echo "Pre-Deployment Check"
echo "========================================="
echo "Project: $PROJECT_ID"
echo "Environment: $ENVIRONMENT"
echo "Time: $(date)"
echo "========================================="

# Check authentication
echo -e "\n${GREEN}[1/7]${NC} Verifying authentication..."
if ! upsun auth:info --no-interaction >/dev/null 2>&1; then
    echo -e "${RED}✗ Not authenticated${NC}"
    echo "Run: upsun auth:browser-login"
    exit 2
fi
echo -e "${GREEN}✓ Authenticated${NC}"

# Check for incomplete activities
echo -e "\n${GREEN}[2/7]${NC} Checking for incomplete activities..."
INCOMPLETE_COUNT=$(upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" -i --no-interaction --pipe 2>/dev/null | wc -l | tr -d ' ')

if [ "$INCOMPLETE_COUNT" -gt 0 ]; then
    echo -e "${RED}✗ $INCOMPLETE_COUNT incomplete activities found${NC}"
    echo "Incomplete activities:"
    upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" -i --no-interaction --limit 5 2>/dev/null
    echo ""
    echo -e "${RED}BLOCKER: Wait for activities to complete before deploying${NC}"
    ((BLOCKERS++))
else
    echo -e "${GREEN}✓ No incomplete activities${NC}"
fi

# Check recent deployment history
echo -e "\n${GREEN}[3/7]${NC} Checking recent deployment history..."
RECENT_ACTIVITIES=$(upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" --type environment.push --limit 5 --no-interaction 2>&1 || echo "ERROR")

if [ "$RECENT_ACTIVITIES" = "ERROR" ]; then
    echo -e "${YELLOW}⚠ Cannot retrieve activity history${NC}"
    ((WARNINGS++))
else
    # Check for recent failures
    FAILED_COUNT=$(echo "$RECENT_ACTIVITIES" | grep -ci "failed" || echo "0")
    if [ "$FAILED_COUNT" -gt 2 ]; then
        echo -e "${RED}✗ Multiple recent deployment failures detected${NC}"
        echo "Last 5 deployments:"
        echo "$RECENT_ACTIVITIES" | head -n 10
        echo ""
        echo -e "${YELLOW}WARNING: Investigate recent failures before deploying${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN}✓ Recent deployment history looks good${NC}"
    fi
fi

# Check disk space
echo -e "\n${GREEN}[4/7]${NC} Checking disk space..."
DISK_OUTPUT=$(upsun disk -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")

if [ "$DISK_OUTPUT" = "ERROR" ]; then
    echo -e "${YELLOW}⚠ Cannot retrieve disk usage${NC}"
    ((WARNINGS++))
else
    DISK_PERCENT=$(echo "$DISK_OUTPUT" | grep -oP '\d+%' | head -n 1 | tr -d '%' || echo "0")
    if [ "$DISK_PERCENT" -gt 95 ]; then
        echo -e "${RED}✗ Disk usage critical: ${DISK_PERCENT}%${NC}"
        echo -e "${RED}BLOCKER: Free up disk space before deploying${NC}"
        ((BLOCKERS++))
    elif [ "$DISK_PERCENT" -gt 85 ]; then
        echo -e "${YELLOW}⚠ Disk usage high: ${DISK_PERCENT}%${NC}"
        echo -e "${YELLOW}WARNING: Consider cleaning up before deployment${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN}✓ Disk space available: $((100 - DISK_PERCENT))% free${NC}"
    fi
fi

# Check environment status
echo -e "\n${GREEN}[5/7]${NC} Checking environment status..."
ENV_STATUS=$(upsun environment:info -p "$PROJECT_ID" -e "$ENVIRONMENT" status --no-interaction 2>&1 || echo "ERROR")

if [ "$ENV_STATUS" = "ERROR" ]; then
    echo -e "${RED}✗ Cannot access environment${NC}"
    echo -e "${RED}BLOCKER: Environment not accessible${NC}"
    ((BLOCKERS++))
elif [[ "$ENV_STATUS" == *"active"* ]]; then
    echo -e "${GREEN}✓ Environment is active${NC}"
elif [[ "$ENV_STATUS" == *"inactive"* ]]; then
    echo -e "${YELLOW}⚠ Environment is inactive${NC}"
    echo "Activate with: upsun environment:activate -p $PROJECT_ID -e $ENVIRONMENT"
    ((WARNINGS++))
else
    echo -e "${YELLOW}⚠ Environment status: $ENV_STATUS${NC}"
    ((WARNINGS++))
fi

# Check resource availability
echo -e "\n${GREEN}[6/7]${NC} Checking resource allocation..."
RESOURCES=$(upsun resources -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")

if [ "$RESOURCES" = "ERROR" ]; then
    echo -e "${YELLOW}⚠ Cannot retrieve resource information${NC}"
    ((WARNINGS++))
else
    # Just verify we can get resources
    echo -e "${GREEN}✓ Resource allocation confirmed${NC}"
fi

# Check for configuration issues
echo -e "\n${GREEN}[7/7]${NC} Validating configuration..."
if [ -f ".upsun/config.yaml" ]; then
    if upsun validate --no-interaction >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Configuration valid${NC}"
    else
        echo -e "${RED}✗ Configuration validation failed${NC}"
        upsun validate 2>&1 | head -n 10
        echo ""
        echo -e "${RED}BLOCKER: Fix configuration errors before deploying${NC}"
        ((BLOCKERS++))
    fi
else
    echo -e "${YELLOW}⚠ No .upsun/config.yaml found in current directory${NC}"
    echo "Run this script from project root, or configuration is remote."
fi

# Summary
echo ""
echo "========================================="
echo "Pre-Deployment Check Summary"
echo "========================================="

if [ "$BLOCKERS" -gt 0 ]; then
    echo -e "${RED}Status: BLOCKED${NC}"
    echo -e "${RED}Critical Issues: $BLOCKERS${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
    echo ""
    echo -e "${RED}❌ DO NOT DEPLOY${NC}"
    echo "Fix critical issues before proceeding."
    echo ""
    echo "Recommendations:"
    echo "1. Resolve all blockers listed above"
    echo "2. Re-run this check"
    echo "3. Only deploy when check passes"
    exit 2
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}Status: CAUTION${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
    echo ""
    echo -e "${YELLOW}⚠ PROCEED WITH CAUTION${NC}"
    echo "Review warnings and determine if deployment should proceed."
    echo ""
    echo "Recommendations:"
    echo "1. Review all warnings above"
    echo "2. Address critical warnings if possible"
    echo "3. Ensure backup exists before deploying"
    echo "4. Monitor deployment closely"
    exit 1
else
    echo -e "${GREEN}Status: READY${NC}"
    echo -e "${GREEN}No issues detected${NC}"
    echo ""
    echo -e "${GREEN}✓ SAFE TO DEPLOY${NC}"
    echo ""
    echo "Recommended next steps:"
    echo "1. Create backup: upsun backup:create -p $PROJECT_ID -e $ENVIRONMENT"
    echo "2. Deploy: upsun push -p $PROJECT_ID -e $ENVIRONMENT"
    echo "3. Monitor: upsun activity:list -p $PROJECT_ID -e $ENVIRONMENT -i"
    exit 0
fi
