#!/usr/bin/env bash
#
# environment-status.sh - Detailed Upsun environment status in JSON format
#
# Usage: ./environment-status.sh PROJECT_ID ENVIRONMENT_NAME
#
# Returns:
#   0 - Status retrieved successfully
#   1 - Error retrieving status
#
# Outputs:
#   JSON object with comprehensive environment status
#
# Description:
#   Retrieves detailed environment information in machine-readable JSON format.
#   Useful for monitoring, automation, and integration with other tools.
#   Output includes: status, resources, URLs, recent activities, metrics.
#

set -euo pipefail

# Configuration
PROJECT_ID="${1:-}"
ENVIRONMENT="${2:-}"

# Usage
if [ -z "$PROJECT_ID" ] || [ -z "$ENVIRONMENT" ]; then
    echo '{"error": "Usage: ./environment-status.sh PROJECT_ID ENVIRONMENT_NAME"}' >&2
    exit 1
fi

# Check authentication
if ! upsun auth:info --no-interaction >/dev/null 2>&1; then
    echo '{"error": "Not authenticated. Run: upsun auth:browser-login"}' >&2
    exit 1
fi

# Initialize JSON output
cat <<EOF
{
  "project_id": "$PROJECT_ID",
  "environment": "$ENVIRONMENT",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": {
EOF

# Get environment status
ENV_STATUS=$(upsun environment:info -p "$PROJECT_ID" -e "$ENVIRONMENT" status --no-interaction 2>&1 || echo "error")
echo "    \"state\": \"$ENV_STATUS\","

# Get environment type
ENV_TYPE=$(upsun environment:info -p "$PROJECT_ID" -e "$ENVIRONMENT" type --no-interaction 2>&1 || echo "unknown")
echo "    \"type\": \"$ENV_TYPE\","

# Get parent environment
ENV_PARENT=$(upsun environment:info -p "$PROJECT_ID" -e "$ENVIRONMENT" parent --no-interaction 2>&1 || echo "none")
echo "    \"parent\": \"$ENV_PARENT\""

echo "  },"

# URLs
echo "  \"urls\": {"
ENV_URLS=$(upsun environment:url -p "$PROJECT_ID" -e "$ENVIRONMENT" --pipe --no-interaction 2>/dev/null || echo "")
if [ -n "$ENV_URLS" ]; then
    PRIMARY_URL=$(echo "$ENV_URLS" | head -n 1)
    echo "    \"primary\": \"$PRIMARY_URL\","
    # Count total URLs
    URL_COUNT=$(echo "$ENV_URLS" | wc -l | tr -d ' ')
    echo "    \"count\": $URL_COUNT"
else
    echo "    \"primary\": null,"
    echo "    \"count\": 0"
fi
echo "  },"

# Resources
echo "  \"resources\": {"
RESOURCES_OUTPUT=$(upsun resources -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")

if [ "$RESOURCES_OUTPUT" != "ERROR" ]; then
    # Try to extract resource info (this is simplified, actual parsing would be more complex)
    echo "    \"available\": true,"
    echo "    \"details\": \"See full output for details\""
else
    echo "    \"available\": false,"
    echo "    \"details\": null"
fi
echo "  },"

# Activities
echo "  \"activities\": {"

# Recent activities count
RECENT_COUNT=$(upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" --limit 10 --pipe --no-interaction 2>/dev/null | wc -l | tr -d ' ')
echo "    \"recent_count\": $RECENT_COUNT,"

# Incomplete activities count
INCOMPLETE_COUNT=$(upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" -i --pipe --no-interaction 2>/dev/null | wc -l | tr -d ' ')
echo "    \"incomplete_count\": $INCOMPLETE_COUNT,"

# Last activity ID
LAST_ACTIVITY=$(upsun activity:list -p "$PROJECT_ID" -e "$ENVIRONMENT" --limit 1 --pipe --no-interaction 2>/dev/null | head -n 1 || echo "")
if [ -n "$LAST_ACTIVITY" ]; then
    echo "    \"last_activity_id\": \"$LAST_ACTIVITY\""
else
    echo "    \"last_activity_id\": null"
fi

echo "  },"

# Metrics (simplified)
echo "  \"metrics\": {"

# CPU
CPU_OUTPUT=$(upsun cpu -p "$PROJECT_ID" -e "$ENVIRONMENT" --start "-1 hour" --no-interaction 2>&1 || echo "ERROR")
if [ "$CPU_OUTPUT" != "ERROR" ]; then
    CPU_PERCENT=$(echo "$CPU_OUTPUT" | grep -oP '\d+%' | tail -n 1 | tr -d '%' || echo "0")
    echo "    \"cpu_percent\": $CPU_PERCENT,"
else
    echo "    \"cpu_percent\": null,"
fi

# Memory
MEM_OUTPUT=$(upsun memory -p "$PROJECT_ID" -e "$ENVIRONMENT" --start "-1 hour" --no-interaction 2>&1 || echo "ERROR")
if [ "$MEM_OUTPUT" != "ERROR" ]; then
    MEM_PERCENT=$(echo "$MEM_OUTPUT" | grep -oP '\d+%' | tail -n 1 | tr -d '%' || echo "0")
    echo "    \"memory_percent\": $MEM_PERCENT,"
else
    echo "    \"memory_percent\": null,"
fi

# Disk
DISK_OUTPUT=$(upsun disk -p "$PROJECT_ID" -e "$ENVIRONMENT" --no-interaction 2>&1 || echo "ERROR")
if [ "$DISK_OUTPUT" != "ERROR" ]; then
    DISK_PERCENT=$(echo "$DISK_OUTPUT" | grep -oP '\d+%' | head -n 1 | tr -d '%' || echo "0")
    echo "    \"disk_percent\": $DISK_PERCENT"
else
    echo "    \"disk_percent\": null"
fi

echo "  },"

# Health assessment
echo "  \"health\": {"

HEALTH="healthy"
HEALTH_ISSUES=()

# Check status
if [ "$ENV_STATUS" != "active" ]; then
    HEALTH="warning"
    HEALTH_ISSUES+=("Environment not active: $ENV_STATUS")
fi

# Check incomplete activities
if [ "$INCOMPLETE_COUNT" -gt 0 ]; then
    HEALTH="warning"
    HEALTH_ISSUES+=("$INCOMPLETE_COUNT incomplete activities")
fi

# Check CPU
if [ "$CPU_OUTPUT" != "ERROR" ]; then
    if [ "$CPU_PERCENT" -gt 90 ]; then
        HEALTH="critical"
        HEALTH_ISSUES+=("High CPU usage: ${CPU_PERCENT}%")
    elif [ "$CPU_PERCENT" -gt 75 ]; then
        if [ "$HEALTH" = "healthy" ]; then
            HEALTH="warning"
        fi
        HEALTH_ISSUES+=("Elevated CPU usage: ${CPU_PERCENT}%")
    fi
fi

# Check memory
if [ "$MEM_OUTPUT" != "ERROR" ]; then
    if [ "$MEM_PERCENT" -gt 90 ]; then
        HEALTH="critical"
        HEALTH_ISSUES+=("High memory usage: ${MEM_PERCENT}%")
    elif [ "$MEM_PERCENT" -gt 80 ]; then
        if [ "$HEALTH" = "healthy" ]; then
            HEALTH="warning"
        fi
        HEALTH_ISSUES+=("Elevated memory usage: ${MEM_PERCENT}%")
    fi
fi

# Check disk
if [ "$DISK_OUTPUT" != "ERROR" ]; then
    if [ "$DISK_PERCENT" -gt 90 ]; then
        HEALTH="critical"
        HEALTH_ISSUES+=("Critical disk usage: ${DISK_PERCENT}%")
    elif [ "$DISK_PERCENT" -gt 80 ]; then
        if [ "$HEALTH" = "healthy" ]; then
            HEALTH="warning"
        fi
        HEALTH_ISSUES+=("High disk usage: ${DISK_PERCENT}%")
    fi
fi

echo "    \"status\": \"$HEALTH\","
echo "    \"issues_count\": ${#HEALTH_ISSUES[@]},"

# Output issues as JSON array
echo "    \"issues\": ["
if [ ${#HEALTH_ISSUES[@]} -gt 0 ]; then
    for i in "${!HEALTH_ISSUES[@]}"; do
        if [ $i -eq $((${#HEALTH_ISSUES[@]} - 1)) ]; then
            echo "      \"${HEALTH_ISSUES[$i]}\""
        else
            echo "      \"${HEALTH_ISSUES[$i]}\","
        fi
    done
else
    echo "    ]"
fi
if [ ${#HEALTH_ISSUES[@]} -gt 0 ]; then
    echo "    ]"
fi

echo "  }"

# Close JSON
echo "}"

exit 0
