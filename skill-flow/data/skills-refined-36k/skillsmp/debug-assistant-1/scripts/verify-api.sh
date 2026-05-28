#!/bin/bash
# 验证 API 端点
# Usage: ./verify-api.sh <service> <endpoint> [method] [data]
# Example: ./verify-api.sh cretas /api/mobile/health

set -e

SERVICE="${1:-cretas}"
ENDPOINT="${2:-/api/mobile/health}"
METHOD="${3:-GET}"
DATA="$4"

# 服务配置
declare -A BASE_URLS=(
    ["cretas"]="http://139.196.165.140:10010"
    ["ai"]="http://139.196.165.140:8085"
    ["mall"]="http://139.196.165.140:7500"
    ["local-cretas"]="http://localhost:10010"
    ["local-ai"]="http://localhost:8085"
    ["local-mall"]="http://localhost:7500"
)

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

BASE_URL=${BASE_URLS[$SERVICE]}

if [ -z "$BASE_URL" ]; then
    echo -e "${RED}错误: 未知服务 '$SERVICE'${NC}"
    echo "可用服务: cretas, ai, mall, local-cretas, local-ai, local-mall"
    exit 1
fi

URL="${BASE_URL}${ENDPOINT}"

echo -e "${YELLOW}=== API 验证 ===${NC}"
echo -e "${CYAN}URL:${NC} $URL"
echo -e "${CYAN}Method:${NC} $METHOD"
if [ -n "$DATA" ]; then
    echo -e "${CYAN}Data:${NC} $DATA"
fi
echo ""

# 发送请求
echo -e "${YELLOW}=== 响应 ===${NC}"

if [ "$METHOD" = "GET" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$URL" \
        -H "Content-Type: application/json" \
        --connect-timeout 10)
elif [ "$METHOD" = "POST" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$URL" \
        -H "Content-Type: application/json" \
        -d "$DATA" \
        --connect-timeout 10)
else
    RESPONSE=$(curl -s -w "\n%{http_code}" -X "$METHOD" "$URL" \
        -H "Content-Type: application/json" \
        --connect-timeout 10)
fi

# 解析响应
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

# 显示状态
if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo -e "${GREEN}Status: $HTTP_CODE OK${NC}"
elif [ "$HTTP_CODE" -ge 400 ] && [ "$HTTP_CODE" -lt 500 ]; then
    echo -e "${YELLOW}Status: $HTTP_CODE Client Error${NC}"
elif [ "$HTTP_CODE" -ge 500 ]; then
    echo -e "${RED}Status: $HTTP_CODE Server Error${NC}"
else
    echo -e "${CYAN}Status: $HTTP_CODE${NC}"
fi

echo ""
echo -e "${YELLOW}=== Body ===${NC}"

# 尝试格式化 JSON
if command -v jq &> /dev/null; then
    echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
else
    echo "$BODY"
fi

echo ""

# 常见端点快速测试
if [ "$ENDPOINT" = "quick" ]; then
    echo -e "${YELLOW}=== 快速测试所有健康端点 ===${NC}"
    echo ""

    for svc in cretas ai mall; do
        case $svc in
            cretas) ep="/api/mobile/health" ;;
            ai) ep="/health" ;;
            mall) ep="/actuator/health" ;;
        esac

        url="${BASE_URLS[$svc]}${ep}"
        code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" 2>/dev/null || echo "000")

        if [ "$code" = "200" ]; then
            echo -e "${GREEN}✓ $svc ($url) - $code${NC}"
        else
            echo -e "${RED}✗ $svc ($url) - $code${NC}"
        fi
    done
fi
