#!/bin/bash

set -euo pipefail

# ========================
#       常量定义
# ========================
SCRIPT_NAME=$(basename "$0")

# ========================
#       工具函数
# ========================

log_info() {
    echo "🔹 $*"
}

log_success() {
    echo "✅ $*"
}

log_error() {
    echo "❌ $*" >&2
}

log_warn() {
    echo "⚠️  $*"
}

log_section() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 $*"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# ========================
#       检查函数
# ========================

check_tgz_files() {
    log_section "1. 检查 .tgz 文件"

    local tgz_files=(*.tgz)
    local valid_count=0
    local invalid_count=0

    if [[ ! -e "${tgz_files[0]}" ]]; then
        log_warn "未找到 .tgz 文件"
        return 0
    fi

    for file in *.tgz; do
        if helm lint "$file" > /dev/null 2>&1; then
            log_success "$file 格式正确"
            ((valid_count++))
        else
            log_error "$file 格式错误"
            ((invalid_count++))
        fi
    done

    echo ""
    echo "总结: $valid_count 个有效, $invalid_count 个无效"

    return $invalid_count
}

check_index_yaml() {
    log_section "2. 检查 index.yaml"

    if [[ ! -f "index.yaml" ]]; then
        log_error "index.yaml 不存在"
        return 1
    fi

    log_success "index.yaml 存在"

    # 验证 YAML 语法
    if command -v python3 &>/dev/null; then
        if python3 -c "import yaml; yaml.safe_load(open('index.yaml'))" 2>/dev/null; then
            log_success "index.yaml 语法正确"
        else
            log_error "index.yaml 语法错误"
            return 1
        fi
    else
        log_warn "python3 未安装,跳过 YAML 语法检查"
    fi

    # 显示索引中的 charts
    log_info "索引中包含的 Charts:"
    grep "^  [a-z-]*:$" index.yaml | sed 's/://g' | sed 's/^/  - /' || true

    return 0
}

check_url_accessibility() {
    log_section "3. 检查仓库 URL 可访问性"

    # 从 index.yaml 提取 URL
    if [[ ! -f "index.yaml" ]]; then
        log_warn "index.yaml 不存在,跳过 URL 检查"
        return 0
    fi

    local index_url=$(grep -m 1 "urls:" index.yaml | grep -oP 'https?://[^/]+' || echo "")

    if [[ -z "$index_url" ]]; then
        log_warn "无法从 index.yaml 提取仓库 URL"
        return 0
    fi

    log_info "检查 URL: $index_url/index.yaml"

    if command -v curl &>/dev/null; then
        local http_code=$(curl -s -o /dev/null -w "%{http_code}" "$index_url/index.yaml" 2>/dev/null || echo "000")

        if [[ "$http_code" == "200" ]]; then
            log_success "仓库 URL 可访问 (HTTP $http_code)"
            return 0
        elif [[ "$http_code" == "000" ]]; then
            log_warn "无法连接到仓库 URL (可能是网络问题或 URL 配置错误)"
            return 0
        else
            log_warn "仓库 URL 返回 HTTP $http_code"
            return 0
        fi
    else
        log_warn "curl 未安装,跳过 URL 可访问性检查"
        return 0
    fi
}

check_digest_matches() {
    log_section "4. 检查 digest 完整性"

    if [[ ! -f "index.yaml" ]]; then
        log_warn "index.yaml 不存在,跳过 digest 检查"
        return 0
    fi

    local tgz_files=(*.tgz)
    local mismatch_count=0
    local match_count=0

    if [[ ! -e "${tgz_files[0]}" ]]; then
        log_warn "未找到 .tgz 文件"
        return 0
    fi

    for tgz in *.tgz; do
        local actual_digest=$(sha256sum "$tgz" | awk '{print $1}')
        local name=$(basename "$tgz")

        # 从 index.yaml 提取 digest
        local index_digest=$(grep -B 2 "$name" index.yaml 2>/dev/null | grep "digest:" | awk '{print $2}' || echo "")

        if [[ -z "$index_digest" ]]; then
            log_warn "$name 不在 index.yaml 中"
            ((mismatch_count++))
            continue
        fi

        if [[ "$actual_digest" == "$index_digest" ]]; then
            log_success "$name digest 匹配"
            ((match_count++))
        else
            log_error "$name digest 不匹配"
            echo "  实际: $actual_digest"
            echo "  索引: $index_digest"
            ((mismatch_count++))
        fi
    done

    echo ""
    echo "总结: $match_count 个匹配, $mismatch_count 个不匹配"

    return $mismatch_count
}

check_git_status() {
    log_section "5. 检查 Git 状态"

    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_warn "不是 Git 仓库"
        return 0
    fi

    log_info "Git 仓库状态:"
    git status --short *.tgz index.yaml 2>/dev/null || {
        log_success "工作目录干净"
        return 0
    }

    echo ""
    log_warn "有未提交的变更"
    echo "  运行以下命令提交: git add *.tgz index.yaml && git commit -m \"chore: 更新索引\""

    return 0
}

generate_report() {
    log_section "健康检查报告"

    local total_issues=$1

    if [[ $total_issues -eq 0 ]]; then
        log_success "✨ 所有检查通过!仓库状态健康"
        echo ""
        echo "建议:"
        echo "  - 定期运行此脚本进行健康检查"
        echo "  - 在发布新版本前运行验证"
    else
        log_error "发现 $total_issues 个问题"
        echo ""
        echo "建议:"
        echo "  1. 查看上述错误信息"
        echo "  2. 参考 troubleshooting.md 解决问题"
        echo "  3. 运行 update-index.sh 重新生成索引"
    fi
}

# ========================
#        主程序
# ========================

main() {
    echo "🏥 Helm Chart 仓库健康检查"
    echo ""

    local total_issues=0

    # 执行各项检查
    check_tgz_files || ((total_issues+=$?))
    check_index_yaml || ((total_issues+=$?))
    check_url_accessibility || ((total_issues+=$?))
    check_digest_matches || ((total_issues+=$?))
    check_git_status || ((total_issues+=$?))

    # 生成报告
    echo ""
    generate_report $total_issues

    # 返回状态码
    if [[ $total_issues -eq 0 ]]; then
        return 0
    else
        return 1
    fi
}

main "$@"
