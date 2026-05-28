#!/bin/bash
# sync-skills.sh - 從 GitHub 同步 skill 到 sqlite-memory
#
# 用途：將遠端 skill repos 的 metadata 索引到本地 sqlite-memory
# 這樣 evolve CP1 就能自動推薦相關 skill
#
# 使用方式：
#   ./scripts/sync-skills.sh              # 同步所有 repos
#   ./scripts/sync-skills.sh --software   # 只同步 software skills
#   ./scripts/sync-skills.sh --domain     # 只同步 domain skills
#   ./scripts/sync-skills.sh --list       # 列出已索引的 skills
#   ./scripts/sync-skills.sh --local      # 強制使用本地 repo（如果存在）
#   ./scripts/sync-skills.sh --remote     # 強制使用遠端 repo（clone 到 cache）

set -e

# 配置
CACHE_DIR="${HOME}/.claude/skill-cache"
SOFTWARE_REPO="https://github.com/miles990/claude-software-skills.git"
DOMAIN_REPO="https://github.com/miles990/claude-domain-skills.git"
DB_PATH="${HOME}/.claude/claude.db"

# 本地 repo 路徑（優先使用）
# 會從 sqlite-memory 的 config:ecosystem-repos-locations 自動讀取
# 或使用以下預設路徑
LOCAL_SOFTWARE_REPO=""
LOCAL_DOMAIN_REPO=""

# 顏色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 確保快取目錄存在
mkdir -p "$CACHE_DIR"

# 從 sqlite-memory 讀取本地 repo 路徑
detect_local_repos() {
    if [[ ! -f "$DB_PATH" ]]; then
        return 1
    fi

    local config_content
    config_content=$(sqlite3 "$DB_PATH" "SELECT content FROM memory WHERE key = 'config:ecosystem-repos-locations';" 2>/dev/null) || return 1

    if [[ -z "$config_content" ]]; then
        return 1
    fi

    # 解析 config 中的路徑
    local sw_path dm_path
    sw_path=$(echo "$config_content" | grep -E "claude-software-skills:" | sed 's/.*claude-software-skills:[[:space:]]*//' | tr -d '\n\r')
    dm_path=$(echo "$config_content" | grep -E "claude-domain-skills:" | sed 's/.*claude-domain-skills:[[:space:]]*//' | tr -d '\n\r')

    # 驗證路徑存在
    if [[ -n "$sw_path" ]] && [[ -d "$sw_path/.git" ]]; then
        LOCAL_SOFTWARE_REPO="$sw_path"
        log_info "偵測到本地 software-skills: $sw_path"
    fi

    if [[ -n "$dm_path" ]] && [[ -d "$dm_path/.git" ]]; then
        LOCAL_DOMAIN_REPO="$dm_path"
        log_info "偵測到本地 domain-skills: $dm_path"
    fi
}

# 嘗試常見路徑
try_common_paths() {
    local common_paths=(
        "${HOME}/Workspace"
        "${HOME}/Projects"
        "${HOME}/Code"
        "${HOME}/Development"
        "${HOME}/dev"
    )

    for base in "${common_paths[@]}"; do
        if [[ -z "$LOCAL_SOFTWARE_REPO" ]] && [[ -d "${base}/claude-software-skills/.git" ]]; then
            LOCAL_SOFTWARE_REPO="${base}/claude-software-skills"
            log_info "找到本地 software-skills: $LOCAL_SOFTWARE_REPO"
        fi
        if [[ -z "$LOCAL_DOMAIN_REPO" ]] && [[ -d "${base}/claude-domain-skills/.git" ]]; then
            LOCAL_DOMAIN_REPO="${base}/claude-domain-skills"
            log_info "找到本地 domain-skills: $LOCAL_DOMAIN_REPO"
        fi
    done
}

# 轉義 SQL 字串中的單引號
escape_sql() {
    echo "$1" | sed "s/'/''/g"
}

# 解析 SKILL.md 並直接寫入資料庫
parse_and_index_skill() {
    local skill_file="$1"
    local repo_name="$2"
    local skill_path="$3"

    if [[ ! -f "$skill_file" ]]; then
        return 1
    fi

    # 提取 frontmatter（YAML 格式）
    local in_frontmatter=false
    local name=""
    local description=""
    local version=""
    local triggers=""

    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == "---" ]]; then
            if $in_frontmatter; then
                break
            else
                in_frontmatter=true
                continue
            fi
        fi

        if $in_frontmatter; then
            # 解析 YAML 格式的 key: value
            if [[ "$line" =~ ^name:\ *(.*)$ ]]; then
                name="${BASH_REMATCH[1]}"
                # 移除引號
                name="${name#\"}"
                name="${name%\"}"
                name="${name#\'}"
                name="${name%\'}"
            elif [[ "$line" =~ ^description:\ *(.*)$ ]]; then
                description="${BASH_REMATCH[1]}"
                description="${description#\"}"
                description="${description%\"}"
            elif [[ "$line" =~ ^version:\ *(.*)$ ]]; then
                version="${BASH_REMATCH[1]}"
            elif [[ "$line" =~ ^triggers:\ *(.*)$ ]]; then
                triggers="${BASH_REMATCH[1]}"
            fi
        fi
    done < "$skill_file"

    # 如果沒有 name，使用目錄名
    if [[ -z "$name" ]]; then
        name=$(basename "$(dirname "$skill_file")")
    fi

    # 如果沒有 version，使用 1.0.0
    if [[ -z "$version" ]]; then
        version="1.0.0"
    fi

    # 從路徑提取 category
    local category
    category=$(echo "$skill_path" | cut -d'/' -f1)

    # 構建 memory key
    local key="skill:${repo_name}:${category}:${name}"

    # 構建 content（簡化格式）
    local content="name: ${name}
repo: github:miles990/${repo_name}
path: ${skill_path}
category: ${category}
triggers: ${triggers}"

    # 轉義 SQL 特殊字元
    local escaped_key=$(escape_sql "$key")
    local escaped_content=$(escape_sql "$content")
    local escaped_name=$(escape_sql "$name")

    # 構建 tags JSON
    local tags="[\"skill\",\"${category}\",\"${repo_name}\"]"

    # 寫入 sqlite-memory
    sqlite3 "$DB_PATH" "INSERT OR REPLACE INTO memory (key, content, tags, scope, source, updated_at) VALUES ('${escaped_key}', '${escaped_content}', '${tags}', 'global', 'sync-skills', datetime('now'));"

    # 獲取剛插入的 rowid
    local rowid
    rowid=$(sqlite3 "$DB_PATH" "SELECT id FROM memory WHERE key = '${escaped_key}';")

    # 更新 FTS 索引（先刪除再插入）
    sqlite3 "$DB_PATH" "INSERT INTO memory_fts(memory_fts, rowid, key, content, tags) VALUES ('delete', ${rowid}, '${escaped_key}', '${escaped_content}', '${tags}');" 2>/dev/null || true
    sqlite3 "$DB_PATH" "INSERT INTO memory_fts(rowid, key, content, tags) VALUES (${rowid}, '${escaped_key}', '${escaped_content}', '${tags}');"

    echo "  ✓ ${category}/${name}"
    return 0
}

# 同步單個 repo（支援本地優先）
# 輸出：將路徑寫入全域變數 SYNC_RESULT_PATH
sync_repo() {
    local repo_url="$1"
    local repo_name="$2"
    local local_path="$3"
    local force_mode="$4"  # "local", "remote", or ""
    local cache_path="$CACHE_DIR/$repo_name"

    log_info "同步 $repo_name..."

    # 決定使用哪個路徑
    local use_path=""
    local source_type=""

    if [[ "$force_mode" == "local" ]]; then
        # 強制本地模式
        if [[ -n "$local_path" ]] && [[ -d "$local_path/.git" ]]; then
            use_path="$local_path"
            source_type="local (forced)"
        else
            log_error "本地 repo 不存在: $local_path"
            return 1
        fi
    elif [[ "$force_mode" == "remote" ]]; then
        # 強制遠端模式
        use_path="$cache_path"
        source_type="remote (forced)"
    else
        # 自動模式：優先本地
        if [[ -n "$local_path" ]] && [[ -d "$local_path/.git" ]]; then
            use_path="$local_path"
            source_type="local (auto)"
            # 更新本地 repo
            log_info "使用本地 repo，執行 git pull..."
            (cd "$local_path" && git pull --quiet) || log_warn "git pull 失敗，使用現有版本"
        else
            use_path="$cache_path"
            source_type="remote (auto)"
        fi
    fi

    # 如果使用 cache，需要 clone/pull
    if [[ "$use_path" == "$cache_path" ]]; then
        if [[ -d "$cache_path" ]]; then
            log_info "更新快取: $cache_path"
            (cd "$cache_path" && git pull --quiet) || {
                log_warn "更新失敗，重新克隆"
                rm -rf "$cache_path"
                git clone --quiet --depth 1 "$repo_url" "$cache_path"
            }
        else
            log_info "克隆 repo: $repo_url"
            git clone --quiet --depth 1 "$repo_url" "$cache_path"
        fi
    fi

    log_success "同步完成: $repo_name [$source_type]"

    # 使用全域變數返回路徑（避免與 log 輸出混淆）
    SYNC_RESULT_PATH="$use_path"
}

# 索引 skills 到 sqlite-memory
index_skills() {
    local cache_path="$1"
    local repo_name="$2"
    local count=0

    log_info "索引 $repo_name 的 skills..."

    # 查找所有 SKILL.md 文件
    while IFS= read -r skill_file; do
        # 計算相對路徑
        local rel_path="${skill_file#$cache_path/}"
        local skill_path=$(dirname "$rel_path")

        # 跳過根目錄的 SKILL.md 和隱藏目錄
        if [[ "$skill_path" == "." ]] || [[ "$skill_path" == *"/.claude"* ]] || [[ "$skill_path" == ".claude"* ]]; then
            continue
        fi

        # 解析並索引
        if parse_and_index_skill "$skill_file" "$repo_name" "$skill_path"; then
            ((count++))
        fi
    done < <(find "$cache_path" -name "SKILL.md" -type f 2>/dev/null)

    log_success "索引完成: $count skills"

    # 使用全域變數返回數量（避免與 log 輸出混淆）
    INDEX_RESULT_COUNT=$count
}

# 列出已索引的 skills
list_indexed_skills() {
    log_info "已索引的 skills:"
    echo ""

    sqlite3 -header -column "$DB_PATH" <<EOF
SELECT
    key,
    substr(content, 1, 60) as preview,
    updated_at
FROM memory
WHERE key LIKE 'skill:%'
ORDER BY key;
EOF

    echo ""
    local count
    count=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM memory WHERE key LIKE 'skill:%';")
    log_info "共 $count 個 skills 已索引"
}

# 清除索引
clear_index() {
    log_warn "清除所有 skill 索引..."
    sqlite3 "$DB_PATH" "DELETE FROM memory WHERE key LIKE 'skill:%';"
    log_success "索引已清除"
}

# 主函數
main() {
    local sync_software=false
    local sync_domain=false
    local list_only=false
    local clear_only=false
    local force_mode=""  # "", "local", "remote"

    # 解析參數
    while [[ $# -gt 0 ]]; do
        case $1 in
            --software)
                sync_software=true
                shift
                ;;
            --domain)
                sync_domain=true
                shift
                ;;
            --list)
                list_only=true
                shift
                ;;
            --clear)
                clear_only=true
                shift
                ;;
            --local)
                force_mode="local"
                shift
                ;;
            --remote)
                force_mode="remote"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [選項]"
                echo ""
                echo "選項:"
                echo "  --software   只同步 software skills"
                echo "  --domain     只同步 domain skills"
                echo "  --list       列出已索引的 skills"
                echo "  --clear      清除所有索引"
                echo "  --local      強制使用本地 repo"
                echo "  --remote     強制使用遠端 repo（clone 到 cache）"
                echo "  --help       顯示此幫助"
                echo ""
                echo "自動偵測優先順序："
                echo "  1. sqlite-memory config:ecosystem-repos-locations"
                echo "  2. 常見開發目錄（~/Workspace, ~/Projects 等）"
                echo "  3. skill-cache（從 GitHub clone）"
                exit 0
                ;;
            *)
                log_error "未知選項: $1"
                exit 1
                ;;
        esac
    done

    # 確保資料庫存在
    if [[ ! -f "$DB_PATH" ]]; then
        log_error "sqlite-memory 資料庫不存在: $DB_PATH"
        log_info "請先啟動 sqlite-memory-mcp 或手動初始化"
        exit 1
    fi

    if $list_only; then
        list_indexed_skills
        exit 0
    fi

    if $clear_only; then
        clear_index
        exit 0
    fi

    # 自動偵測本地 repo（除非強制遠端模式）
    if [[ "$force_mode" != "remote" ]]; then
        log_info "偵測本地 repo..."
        detect_local_repos
        try_common_paths
        echo ""
    fi

    # 如果沒有指定，同步所有
    if ! $sync_software && ! $sync_domain; then
        sync_software=true
        sync_domain=true
    fi

    local total=0

    if $sync_software; then
        sync_repo "$SOFTWARE_REPO" "claude-software-skills" "$LOCAL_SOFTWARE_REPO" "$force_mode"
        local sw_path="$SYNC_RESULT_PATH"
        index_skills "$sw_path" "claude-software-skills"
        ((total += INDEX_RESULT_COUNT)) || true
    fi

    if $sync_domain; then
        sync_repo "$DOMAIN_REPO" "claude-domain-skills" "$LOCAL_DOMAIN_REPO" "$force_mode"
        local dm_path="$SYNC_RESULT_PATH"
        index_skills "$dm_path" "claude-domain-skills"
        ((total += INDEX_RESULT_COUNT)) || true
    fi

    echo ""
    log_success "同步完成！共 $total 個 skills"
    log_info "使用 memory_search 搜尋 skills"
}

main "$@"
