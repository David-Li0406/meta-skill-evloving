#!/bin/bash
# 检查后端日志
# Usage: ./check-backend-logs.sh <service> [lines|error|status]
# Example: ./check-backend-logs.sh cretas 50

set -e

SERVICE="${1:-all}"
ACTION="${2:-50}"
SERVER="root@139.196.165.140"

# 服务配置
declare -A LOG_PATHS=(
    ["cretas"]="/www/wwwroot/cretas/cretas-backend.log"
    ["ai"]="/www/ai-service/ai-service.log"
    ["mall"]="/www/mall/logistics-admin.log"
)

declare -A PORTS=(
    ["cretas"]="10010"
    ["ai"]="8085"
    ["mall"]="7500"
)

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查服务状态
check_status() {
    local service=$1
    local port=${PORTS[$service]}

    echo -e "${YELLOW}=== $service (端口 $port) ===${NC}"

    # 检查进程
    if ssh $SERVER "lsof -i:$port" 2>/dev/null | grep -q LISTEN; then
        echo -e "${GREEN}✓ 服务运行中${NC}"

        # 健康检查
        case $service in
            cretas)
                if curl -s --connect-timeout 5 "http://139.196.165.140:$port/api/mobile/health" | grep -q "UP\|ok"; then
                    echo -e "${GREEN}✓ 健康检查通过${NC}"
                else
                    echo -e "${YELLOW}⚠ 健康检查无响应${NC}"
                fi
                ;;
            ai)
                if curl -s --connect-timeout 5 "http://139.196.165.140:$port/health" | grep -q "healthy\|ok"; then
                    echo -e "${GREEN}✓ 健康检查通过${NC}"
                else
                    echo -e "${YELLOW}⚠ 健康检查无响应${NC}"
                fi
                ;;
            mall)
                if curl -s --connect-timeout 5 "http://139.196.165.140:$port/actuator/health" | grep -q "UP"; then
                    echo -e "${GREEN}✓ 健康检查通过${NC}"
                else
                    echo -e "${YELLOW}⚠ 健康检查无响应${NC}"
                fi
                ;;
        esac
    else
        echo -e "${RED}✗ 服务未运行${NC}"
    fi
    echo ""
}

# 查看日志
view_logs() {
    local service=$1
    local lines=$2
    local log_path=${LOG_PATHS[$service]}

    echo -e "${YELLOW}=== $service 日志 (最近 $lines 行) ===${NC}"
    ssh $SERVER "tail -$lines $log_path 2>/dev/null" || echo -e "${RED}无法读取日志${NC}"
    echo ""
}

# 过滤错误日志
filter_errors() {
    local service=$1
    local log_path=${LOG_PATHS[$service]}

    echo -e "${YELLOW}=== $service ERROR 日志 ===${NC}"
    ssh $SERVER "grep -i 'ERROR\|Exception\|FATAL' $log_path 2>/dev/null | tail -50" || echo "无错误日志"
    echo ""
}

# 主逻辑
case $SERVICE in
    all|status)
        echo -e "${YELLOW}=== 所有服务状态 ===${NC}"
        echo ""
        for svc in cretas ai mall; do
            check_status $svc
        done
        ;;
    cretas|ai|mall)
        case $ACTION in
            status)
                check_status $SERVICE
                ;;
            error)
                filter_errors $SERVICE
                ;;
            [0-9]*)
                view_logs $SERVICE $ACTION
                ;;
            *)
                view_logs $SERVICE 50
                ;;
        esac
        ;;
    *)
        echo "Usage: $0 <service> [lines|error|status]"
        echo ""
        echo "Services: cretas, ai, mall, all"
        echo ""
        echo "Examples:"
        echo "  $0 all           # 检查所有服务状态"
        echo "  $0 cretas 100    # 查看 cretas 最近 100 行日志"
        echo "  $0 ai error      # 查看 ai 服务错误日志"
        exit 1
        ;;
esac
