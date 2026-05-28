#!/bin/bash

set -euo pipefail

# ========================
#       常量定义
# ========================
SCRIPT_NAME=$(basename "$0")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="${HELM_REPO_URL:-https://helm-chart.anubis.cafe}"

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

log_step() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 $*"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

show_usage() {
    cat << EOF
用法: $SCRIPT_NAME [OPTIONS]

自动化 Helm Chart 仓库索引更新流程

选项:
  --dry-run       只显示将要执行的操作,不实际执行
  --skip-checks   跳过环境检查(不推荐)
  --auto-push     自动推送到远程仓库(默认需要确认)
  --url <URL>     指定仓库 URL (默认: $REPO_URL)
  --help          显示此帮助信息

环境变量:
  HELM_REPO_URL   设置仓库 URL (可被 --url 覆盖)

示例:
  # 预览模式(推荐首次使用)
  $SCRIPT_NAME --dry-run

  # 执行更新
  $SCRIPT_NAME

  # 自动推送到远程
  $SCRIPT_NAME --auto-push

  # 使用自定义 URL
  $SCRIPT_NAME --url https://example.com/charts
EOF
}

# ========================
#       命令行参数
# ========================

DRY_RUN=false
SKIP_CHECKS=false
AUTO_PUSH=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --skip-checks)
            SKIP_CHECKS=true
            shift
            ;;
        --auto-push)
            AUTO_PUSH=true
            shift
            ;;
        --url)
            REPO_URL="$2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            log_error "未知选项: $1"
            show_usage
            exit 1
            ;;
    esac
done

# ========================
#       执行函数
# ========================

run_command() {
    local description="$1"
    shift

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY-RUN] $description"
        echo "  命令: $*"
    else
        log_info "$description"
        "$@" || {
            log_error "命令执行失败: $*"
            return 1
        }
    fi
}

# ========================
#       主流程函数
# ========================

step_1_check_environment() {
    log_step "步骤 1/6: 环境检查"

    if [[ "$SKIP_CHECKS" == "true" ]]; then
        log_warn "跳过环境检查"
        return 0
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] 将运行环境检查"
        return 0
    fi

    if [[ -f "$SCRIPT_DIR/check-env.sh" ]]; then
        bash "$SCRIPT_DIR/check-env.sh" || {
            log_error "环境检查失败,请修复问题后重试"
            return 1
        }
    else
        log_warn "check-env.sh 脚本不存在,跳过环境检查"
    fi
}

step_2_verify_packages() {
    log_step "步骤 2/6: 验证现有包"

    run_command "列出现有的 .tgz 包" ls -lh *.tgz 2>/dev/null || {
        log_warn "未找到 .tgz 文件"
        return 0
    }
}

step_3_package_charts() {
    log_step "步骤 3/6: 打包 Charts"

    if [[ ! -d "charts" ]]; then
        log_warn "charts 目录不存在,跳过打包步骤"
        return 0
    fi

    local charts_to_package=$(find charts -maxdepth 1 -type d ! -path charts)

    if [[ -z "$charts_to_package" ]]; then
        log_warn "charts 目录为空,跳过打包步骤"
        return 0
    fi

    log_info "找到以下 Charts:"
    echo "$charts_to_package" | sed 's|charts/|  - |g'

    run_command "打包所有 Charts" helm package charts/*
}

step_4_update_index() {
    log_step "步骤 4/6: 更新 Helm 仓库索引"

    log_info "仓库 URL: $REPO_URL"

    run_command "生成 index.yaml" helm repo index . --url "$REPO_URL"

    if [[ "$DRY_RUN" == "false" ]]; then
        log_success "index.yaml 已更新"
    fi
}

step_5_verify_index() {
    log_step "步骤 5/6: 验证索引更新"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] 将验证 index.yaml"
        return 0
    fi

    if [[ ! -f "index.yaml" ]]; then
        log_error "index.yaml 不存在"
        return 1
    fi

    # 验证 YAML 语法
    if command -v python3 &>/dev/null; then
        if python3 -c "import yaml; yaml.safe_load(open('index.yaml'))" 2>/dev/null; then
            log_success "index.yaml 语法正确"
        else
            log_error "index.yaml 语法错误"
            return 1
        fi
    fi

    # 显示更新的 charts
    log_info "索引中包含的 Charts:"
    grep "^  [a-z-]*:$" index.yaml | sed 's/://g' | sed 's/^/  - /'
}

step_6_git_commit() {
    log_step "步骤 6/6: Git 提交"

    # 检查是否有变更
    if [[ "$DRY_RUN" == "false" ]]; then
        if ! git diff --quiet *.tgz index.yaml 2>/dev/null && ! git diff --cached --quiet *.tgz index.yaml 2>/dev/null; then
            log_info "检测到以下变更:"
            git status --short *.tgz index.yaml 2>/dev/null || true
        else
            log_warn "没有检测到变更"
            return 0
        fi
    fi

    run_command "添加变更到暂存区" git add *.tgz index.yaml

    # 生成提交信息
    local commit_message="chore: 更新 Helm Chart 仓库索引

- 重新打包 Charts
- 更新 index.yaml 以反映最新的 .tgz 包

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY-RUN] 提交信息:"
        echo "$commit_message"
    else
        git commit -m "$commit_message" || {
            log_warn "提交失败(可能没有变更)"
            return 0
        }
        log_success "变更已提交"
    fi

    # 推送到远程
    if [[ "$AUTO_PUSH" == "true" ]]; then
        run_command "推送到远程仓库" git push
        if [[ "$DRY_RUN" == "false" ]]; then
            log_success "已推送到远程仓库"
        fi
    else
        if [[ "$DRY_RUN" == "false" ]]; then
            echo ""
            log_warn "变更已提交但未推送到远程"
            echo "  运行以下命令推送: git push"
            echo "  或使用 --auto-push 选项自动推送"
        fi
    fi
}

# ========================
#        主程序
# ========================

main() {
    echo "🚀 Helm Chart 仓库索引更新"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log_warn "运行在 DRY-RUN 模式,不会执行实际操作"
        echo ""
    fi

    # 执行各个步骤
    step_1_check_environment || exit 1
    step_2_verify_packages || exit 1
    step_3_package_charts || exit 1
    step_4_update_index || exit 1
    step_5_verify_index || exit 1
    step_6_git_commit || exit 1

    # 完成
    echo ""
    log_success "🎉 索引更新完成!"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo ""
        log_info "这是 DRY-RUN 模式的预览"
        echo "  运行不带 --dry-run 参数以执行实际操作"
    fi
}

main "$@"
