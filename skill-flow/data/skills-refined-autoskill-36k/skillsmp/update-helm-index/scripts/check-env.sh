#!/bin/bash

set -euo pipefail

# ========================
#       常量定义
# ========================
SCRIPT_NAME=$(basename "$0")
HELM_MIN_VERSION="3.0.0"
REQUIRED_COMMANDS=("helm" "git" "grep" "sha256sum")

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

# ========================
#       检查函数
# ========================

check_command_exists() {
    local cmd="$1"
    if command -v "$cmd" &>/dev/null; then
        log_success "$cmd 已安装"
        return 0
    else
        log_error "$cmd 未安装"
        return 1
    fi
}

version_compare() {
    # 比较版本号
    # 返回: 0 如果 $1 >= $2, 1 否则
    if [[ "$1" == "$2" ]]; then
        return 0
    fi

    local IFS=.
    local i ver1=($1) ver2=($2)

    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done

    for ((i=0; i<${#ver1[@]}; i++)); do
        if [[ -z ${ver2[i]} ]]; then
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]})); then
            return 0
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 1
        fi
    done
    return 0
}

check_helm_version() {
    log_info "检查 Helm 版本..."

    if ! command -v helm &>/dev/null; then
        log_error "Helm 未安装"
        echo "   请访问 https://helm.sh/docs/intro/install/ 安装 Helm"
        return 1
    fi

    local helm_version=$(helm version --short 2>/dev/null | grep -oP 'v\K[0-9]+\.[0-9]+\.[0-9]+' | head -1)

    if [[ -z "$helm_version" ]]; then
        # 尝试旧版本格式
        helm_version=$(helm version 2>/dev/null | grep -oP 'Version:"v\K[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    fi

    if [[ -z "$helm_version" ]]; then
        log_error "无法获取 Helm 版本"
        return 1
    fi

    if version_compare "$helm_version" "$HELM_MIN_VERSION"; then
        log_success "Helm 版本: v$helm_version (>= $HELM_MIN_VERSION)"
        return 0
    else
        log_error "Helm 版本: v$helm_version (需要 >= $HELM_MIN_VERSION)"
        echo "   请升级 Helm 到最新版本"
        return 1
    fi
}

check_git_config() {
    log_info "检查 Git 配置..."

    local user_name=$(git config user.name 2>/dev/null || echo "")
    local user_email=$(git config user.email 2>/dev/null || echo "")

    local status=0

    if [[ -z "$user_name" ]]; then
        log_error "Git user.name 未配置"
        echo "   运行: git config --global user.name \"Your Name\""
        status=1
    else
        log_success "Git user.name: $user_name"
    fi

    if [[ -z "$user_email" ]]; then
        log_error "Git user.email 未配置"
        echo "   运行: git config --global user.email \"your.email@example.com\""
        status=1
    else
        log_success "Git user.email: $user_email"
    fi

    return $status
}

check_directory_permissions() {
    log_info "检查目录权限..."

    if [[ -w . ]]; then
        log_success "当前目录可写"
        return 0
    else
        log_error "当前目录不可写"
        echo "   请检查目录权限"
        return 1
    fi
}

check_tgz_files() {
    log_info "检查 .tgz 文件..."

    local tgz_count=$(ls *.tgz 2>/dev/null | wc -l)

    if [[ $tgz_count -eq 0 ]]; then
        log_warn "未找到 .tgz 文件"
        echo "   可能需要先运行: helm package charts/*"
        return 0
    else
        log_success "找到 $tgz_count 个 .tgz 文件"
        return 0
    fi
}

check_index_file() {
    log_info "检查 index.yaml..."

    if [[ -f "index.yaml" ]]; then
        log_success "index.yaml 存在"

        # 验证 YAML 语法
        if command -v python3 &>/dev/null; then
            if python3 -c "import yaml; yaml.safe_load(open('index.yaml'))" 2>/dev/null; then
                log_success "index.yaml 语法正确"
            else
                log_error "index.yaml 语法错误"
                return 1
            fi
        fi
        return 0
    else
        log_warn "index.yaml 不存在"
        echo "   首次使用需要运行: helm repo index . --url <REPO_URL>"
        return 0
    fi
}

# ========================
#        主流程
# ========================

main() {
    echo "🚀 Helm Chart 仓库环境检查"
    echo ""

    local all_passed=0

    # 检查必需命令
    log_info "检查必需命令..."
    for cmd in "${REQUIRED_COMMANDS[@]}"; do
        if ! check_command_exists "$cmd"; then
            all_passed=1
        fi
    done
    echo ""

    # 检查 Helm 版本
    if ! check_helm_version; then
        all_passed=1
    fi
    echo ""

    # 检查 Git 配置
    if ! check_git_config; then
        all_passed=1
    fi
    echo ""

    # 检查目录权限
    if ! check_directory_permissions; then
        all_passed=1
    fi
    echo ""

    # 检查 .tgz 文件
    check_tgz_files
    echo ""

    # 检查 index.yaml
    check_index_file
    echo ""

    # 总结
    if [[ $all_passed -eq 0 ]]; then
        log_success "✨ 所有环境检查通过!"
        echo ""
        echo "您可以运行以下命令更新 Helm 索引:"
        echo "  bash .claude/skills/update-helm-index/scripts/update-index.sh"
        return 0
    else
        log_error "❌ 部分检查失败,请修复上述问题后再继续"
        return 1
    fi
}

main "$@"
