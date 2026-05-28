#!/usr/bin/env bash
#
# resource-audit.sh - Resource usage audit across all Upsun environments
#
# Usage: ./resource-audit.sh PROJECT_ID
#
# Returns:
#   0 - Audit completed successfully
#   1 - Error during audit
#
# Description:
#   Analyzes resource usage across all environments in a project.
#   Identifies over-provisioned and under-provisioned resources.
#   Provides recommendations for cost optimization and performance.
#   Includes CPU, memory, disk usage, and autoscaling status.
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
OVER_PROVISIONED=()
UNDER_PROVISIONED=()
OPTIMAL=()

# Usage
if [ -z "$PROJECT_ID" ]; then
    echo "Usage: $0 PROJECT_ID"
    echo ""
    echo "Example: $0 abc123"
    exit 1
fi

echo "========================================="
echo "Resource Audit Report"
echo "========================================="
echo "Project: $PROJECT_ID"
echo "Generated: $(date)"
echo "========================================="

# Check authentication
echo -e "\n${GREEN}Checking authentication...${NC}"
if ! upsun auth:info --no-interaction >/dev/null 2>&1; then
    echo -e "${RED}✗ Not authenticated${NC}"
    echo "Run: upsun auth:browser-login"
    exit 1
fi
echo -e "${GREEN}✓ Authenticated${NC}"

# Get list of environments
echo -e "\n${GREEN}Retrieving environments...${NC}"
ENVIRONMENTS=$(upsun environment:list -p "$PROJECT_ID" --pipe --no-interaction 2>&1 || echo "ERROR")

if [ "$ENVIRONMENTS" = "ERROR" ]; then
    echo -e "${RED}✗ Cannot retrieve environments${NC}"
    exit 1
fi

ENV_COUNT=$(echo "$ENVIRONMENTS" | wc -l | tr -d ' ')
echo "Found $ENV_COUNT environment(s)"
echo ""

# Iterate through each environment
while IFS= read -r ENV; do
    if [ -z "$ENV" ]; then
        continue
    fi

    echo "========================================="
    echo "Environment: $ENV"
    echo "========================================="

    # Check environment status
    ENV_STATUS=$(upsun environment:info -p "$PROJECT_ID" -e "$ENV" status --no-interaction 2>&1 || echo "ERROR")

    if [ "$ENV_STATUS" = "ERROR" ]; then
        echo -e "${YELLOW}⚠ Cannot access environment${NC}"
        continue
    fi

    if [[ "$ENV_STATUS" == *"inactive"* ]] || [[ "$ENV_STATUS" == *"paused"* ]]; then
        echo -e "${BLUE}Status: $ENV_STATUS (skipping metrics)${NC}"
        continue
    fi

    echo "Status: $ENV_STATUS"

    # Get resources
    echo -e "\n--- Resource Allocation ---"
    RESOURCES=$(upsun resources -p "$PROJECT_ID" -e "$ENV" --no-interaction 2>&1 || echo "ERROR")

    if [ "$RESOURCES" = "ERROR" ]; then
        echo -e "${YELLOW}⚠ Cannot retrieve resource allocation${NC}"
    else
        echo "$RESOURCES" | head -n 20
    fi

    # Get CPU usage (last 24 hours)
    echo -e "\n--- CPU Usage (Last 24h) ---"
    CPU_OUTPUT=$(upsun cpu -p "$PROJECT_ID" -e "$ENV" --start "-24 hours" --no-interaction 2>&1 || echo "ERROR")

    CPU_AVG=0
    if [ "$CPU_OUTPUT" != "ERROR" ]; then
        # Extract all percentages and calculate rough average
        CPU_VALUES=$(echo "$CPU_OUTPUT" | grep -oP '\d+(?=%)' || echo "")
        if [ -n "$CPU_VALUES" ]; then
            CPU_SUM=0
            CPU_COUNT=0
            while IFS= read -r VAL; do
                CPU_SUM=$((CPU_SUM + VAL))
                CPU_COUNT=$((CPU_COUNT + 1))
            done <<< "$CPU_VALUES"

            if [ $CPU_COUNT -gt 0 ]; then
                CPU_AVG=$((CPU_SUM / CPU_COUNT))
            fi
        fi

        CPU_PEAK=$(echo "$CPU_VALUES" | sort -rn | head -n 1 || echo "0")

        echo "Average: ~${CPU_AVG}%"
        echo "Peak: ${CPU_PEAK}%"

        # Assess CPU
        if [ "$CPU_AVG" -lt 30 ]; then
            echo -e "${YELLOW}Assessment: Under-utilized (consider downsizing)${NC}"
            OVER_PROVISIONED+=("$ENV: CPU avg ${CPU_AVG}%")
        elif [ "$CPU_AVG" -gt 80 ]; then
            echo -e "${RED}Assessment: Over-utilized (consider scaling up)${NC}"
            UNDER_PROVISIONED+=("$ENV: CPU avg ${CPU_AVG}%")
        else
            echo -e "${GREEN}Assessment: Optimal utilization${NC}"
            OPTIMAL+=("$ENV: CPU")
        fi
    else
        echo -e "${YELLOW}⚠ Cannot retrieve CPU metrics${NC}"
    fi

    # Get Memory usage (last 24 hours)
    echo -e "\n--- Memory Usage (Last 24h) ---"
    MEM_OUTPUT=$(upsun memory -p "$PROJECT_ID" -e "$ENV" --start "-24 hours" --no-interaction 2>&1 || echo "ERROR")

    MEM_AVG=0
    if [ "$MEM_OUTPUT" != "ERROR" ]; then
        MEM_VALUES=$(echo "$MEM_OUTPUT" | grep -oP '\d+(?=%)' || echo "")
        if [ -n "$MEM_VALUES" ]; then
            MEM_SUM=0
            MEM_COUNT=0
            while IFS= read -r VAL; do
                MEM_SUM=$((MEM_SUM + VAL))
                MEM_COUNT=$((MEM_COUNT + 1))
            done <<< "$MEM_VALUES"

            if [ $MEM_COUNT -gt 0 ]; then
                MEM_AVG=$((MEM_SUM / MEM_COUNT))
            fi
        fi

        MEM_PEAK=$(echo "$MEM_VALUES" | sort -rn | head -n 1 || echo "0")

        echo "Average: ~${MEM_AVG}%"
        echo "Peak: ${MEM_PEAK}%"

        # Assess Memory
        if [ "$MEM_AVG" -lt 40 ]; then
            echo -e "${YELLOW}Assessment: Under-utilized (consider downsizing)${NC}"
            OVER_PROVISIONED+=("$ENV: Memory avg ${MEM_AVG}%")
        elif [ "$MEM_AVG" -gt 85 ]; then
            echo -e "${RED}Assessment: Over-utilized (consider scaling up)${NC}"
            UNDER_PROVISIONED+=("$ENV: Memory avg ${MEM_AVG}%")
        else
            echo -e "${GREEN}Assessment: Optimal utilization${NC}"
            OPTIMAL+=("$ENV: Memory")
        fi
    else
        echo -e "${YELLOW}⚠ Cannot retrieve memory metrics${NC}"
    fi

    # Get Disk usage
    echo -e "\n--- Disk Usage ---"
    DISK_OUTPUT=$(upsun disk -p "$PROJECT_ID" -e "$ENV" --no-interaction 2>&1 || echo "ERROR")

    if [ "$DISK_OUTPUT" != "ERROR" ]; then
        DISK_PERCENT=$(echo "$DISK_OUTPUT" | grep -oP '\d+%' | head -n 1 | tr -d '%' || echo "0")
        echo "Usage: ${DISK_PERCENT}%"

        if [ "$DISK_PERCENT" -gt 85 ]; then
            echo -e "${RED}Assessment: High usage (cleanup or expand needed)${NC}"
            UNDER_PROVISIONED+=("$ENV: Disk ${DISK_PERCENT}%")
        elif [ "$DISK_PERCENT" -lt 30 ]; then
            echo -e "${YELLOW}Assessment: Low usage (consider smaller disk)${NC}"
            OVER_PROVISIONED+=("$ENV: Disk ${DISK_PERCENT}%")
        else
            echo -e "${GREEN}Assessment: Appropriate allocation${NC}"
            OPTIMAL+=("$ENV: Disk")
        fi
    else
        echo -e "${YELLOW}⚠ Cannot retrieve disk metrics${NC}"
    fi

    # Get Autoscaling status
    echo -e "\n--- Autoscaling ---"
    AUTOSCALING=$(upsun autoscaling -p "$PROJECT_ID" -e "$ENV" --no-interaction 2>&1 || echo "ERROR")

    if [ "$AUTOSCALING" != "ERROR" ]; then
        if [[ "$AUTOSCALING" == *"enabled"* ]] || [[ "$AUTOSCALING" == *"true"* ]]; then
            echo -e "${GREEN}Enabled${NC}"
            echo "$AUTOSCALING" | head -n 10
        else
            echo -e "${BLUE}Disabled${NC}"
            if [ "$CPU_AVG" -gt 60 ] || [ "$MEM_AVG" -gt 70 ]; then
                echo -e "${YELLOW}Recommendation: Consider enabling autoscaling${NC}"
            fi
        fi
    else
        echo -e "${BLUE}Not available or not configured${NC}"
    fi

    echo ""

done <<< "$ENVIRONMENTS"

# Summary Report
echo ""
echo "========================================="
echo "Resource Audit Summary"
echo "========================================="

echo -e "\n${GREEN}Optimally Provisioned (${#OPTIMAL[@]}):${NC}"
if [ ${#OPTIMAL[@]} -eq 0 ]; then
    echo "  None"
else
    for item in "${OPTIMAL[@]}"; do
        echo "  ✓ $item"
    done
fi

echo -e "\n${YELLOW}Over-Provisioned (${#OVER_PROVISIONED[@]}):${NC}"
if [ ${#OVER_PROVISIONED[@]} -eq 0 ]; then
    echo "  None - Good resource efficiency!"
else
    for item in "${OVER_PROVISIONED[@]}"; do
        echo "  ⚠ $item"
    done
    echo ""
    echo "  Recommendation: Consider downsizing to reduce costs"
fi

echo -e "\n${RED}Under-Provisioned (${#UNDER_PROVISIONED[@]}):${NC}"
if [ ${#UNDER_PROVISIONED[@]} -eq 0 ]; then
    echo "  None - All environments have adequate resources!"
else
    for item in "${UNDER_PROVISIONED[@]}"; do
        echo "  ✗ $item"
    done
    echo ""
    echo "  Recommendation: Scale up resources or enable autoscaling"
fi

# Recommendations
echo ""
echo "========================================="
echo "Recommendations"
echo "========================================="

if [ ${#UNDER_PROVISIONED[@]} -gt 0 ]; then
    echo -e "${RED}Priority: Address under-provisioned environments${NC}"
    echo "  • Scale up resources: upsun resources:set -p $PROJECT_ID -e ENV_NAME"
    echo "  • Enable autoscaling: upsun autoscaling:set -p $PROJECT_ID -e ENV_NAME"
fi

if [ ${#OVER_PROVISIONED[@]} -gt 0 ]; then
    echo -e "${YELLOW}Optimization: Reduce over-provisioned resources${NC}"
    echo "  • Downsize: upsun resources:set -p $PROJECT_ID -e ENV_NAME"
    echo "  • Potential cost savings available"
fi

echo ""
echo "For detailed metrics, run:"
echo "  upsun metrics -p $PROJECT_ID -e ENVIRONMENT_NAME"
echo ""
echo "For resource changes:"
echo "  upsun resources:set -p $PROJECT_ID -e ENVIRONMENT_NAME"
echo ""
echo "========================================="
echo "Audit Complete"
echo "========================================="

exit 0
