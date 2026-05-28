#!/bin/bash
# setup-skill-index.sh - 設定 LEANN 語義索引環境
#
# 功能：
#   1. 安裝 LEANN 向量資料庫
#   2. 同步 skill repos（使用現有 sync-skills.sh）
#   3. 建立 LEANN 向量索引
#   4. 驗證搜尋功能
#
# 用法:
#   ./scripts/setup-skill-index.sh              # 完整設定
#   ./scripts/setup-skill-index.sh --rebuild    # 重建索引
#   ./scripts/setup-skill-index.sh --test       # 測試搜尋
#   ./scripts/setup-skill-index.sh --status     # 查看狀態

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILL_CACHE="${HOME}/.claude/skill-cache"
LEANN_INDEX="${HOME}/.claude/leann-indexes/skills"
LEANN_INDEX_NAME="skills"

# 顏色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${CYAN}[STEP]${NC} $1"; }

# 顯示標題
show_header() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}    🔍 LEANN Skill Discovery - Setup                        ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}    語義搜尋 79 skills，自動推薦最相關的能力               ${CYAN}║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# 檢查並安裝 macOS 依賴（LEANN 的 HNSW backend 需要）
check_macos_deps() {
    if [[ "$(uname)" != "Darwin" ]]; then
        return 0  # 非 macOS，跳過
    fi

    log_step "檢查 macOS 依賴..."

    # 檢查 brew
    if ! command -v brew &> /dev/null; then
        log_warn "Homebrew 未安裝，部分依賴可能無法自動安裝"
        return 1
    fi

    # LEANN HNSW backend 需要的依賴
    local deps=("libomp" "boost" "protobuf" "zeromq" "pkgconf")
    local missing=()

    for dep in "${deps[@]}"; do
        if ! brew list "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_info "安裝缺少的依賴: ${missing[*]}"
        brew install "${missing[@]}"
    fi

    log_success "macOS 依賴已就緒"
    return 0
}

# 檢查 uv 是否安裝
check_uv() {
    if command -v uv &> /dev/null; then
        log_success "uv 已安裝: $(uv --version)"
        return 0
    else
        return 1
    fi
}

# 安裝 uv
install_uv() {
    log_step "安裝 uv 套件管理器..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # 重新載入 PATH
    export PATH="$HOME/.local/bin:$PATH"

    if check_uv; then
        log_success "uv 安裝成功"
    else
        log_error "uv 安裝失敗，請手動安裝: https://docs.astral.sh/uv/"
        exit 1
    fi
}

# 檢查 LEANN 是否安裝
check_leann() {
    local venv_dir="${HOME}/.claude/leann-venv"

    # 檢查虛擬環境是否存在且有效
    if [[ -d "$venv_dir" ]] && [[ -f "$venv_dir/bin/python" ]]; then
        # 檢查是否已有 LEANN 完整版
        if "$venv_dir/bin/python" -c "from leann import LeannBuilder" &> /dev/null; then
            log_success "LEANN 完整版已安裝"
            export LEANN_PYTHON="$venv_dir/bin/python"
            return 0
        fi

        # 如果只有 sentence-transformers，嘗試升級到 LEANN 完整版
        if "$venv_dir/bin/python" -c "from sentence_transformers import SentenceTransformer" &> /dev/null; then
            log_info "偵測到 sentence-transformers 替代方案，嘗試升級到 LEANN 完整版..."

            # 靜默嘗試安裝 LEANN（可能會因系統限制失敗）
            if "$venv_dir/bin/pip" install leann 2>/dev/null; then
                if "$venv_dir/bin/python" -c "from leann import LeannBuilder" &> /dev/null; then
                    log_success "🎉 成功升級到 LEANN 完整版！"
                    export LEANN_PYTHON="$venv_dir/bin/python"
                    return 0
                fi
            fi

            # 升級失敗，繼續使用替代方案
            log_info "LEANN 完整版仍不可用（需要 macOS 14+ / Python 3.12+），繼續使用替代方案"
            export LEANN_PYTHON="$venv_dir/bin/python"
            return 0
        fi
    fi

    # 清理過時的 wrapper 腳本
    if [[ -f "${HOME}/.local/bin/leann" ]]; then
        rm -f "${HOME}/.local/bin/leann" "${HOME}/.local/bin/leann-python"
        log_info "清理過時的 wrapper 腳本"
    fi

    return 1
}

# 安裝 LEANN
install_leann() {
    log_step "安裝 LEANN 向量資料庫..."

    # 先檢查 macOS 依賴
    check_macos_deps || log_warn "macOS 依賴檢查失敗，繼續嘗試安裝..."

    local installed=false
    local venv_dir="${HOME}/.claude/leann-venv"

    # 優先使用專用虛擬環境（最可靠的方式）
    log_info "建立專用虛擬環境: $venv_dir"

    # 檢查是否需要重建虛擬環境
    local need_rebuild=false

    if [[ -d "$venv_dir" ]]; then
        # 檢查 LEANN Builder 是否可用（完整安裝）
        if "$venv_dir/bin/python" -c "from leann import LeannBuilder" &> /dev/null; then
            log_success "LEANN 完整版已安裝，跳過安裝步驟"
            export LEANN_PYTHON="$venv_dir/bin/python"
            return 0
        fi

        # 如果系統環境變了（macOS/Python 升級），嘗試重新安裝 LEANN
        if "$venv_dir/bin/python" -c "from sentence_transformers import SentenceTransformer" &> /dev/null; then
            # 目前使用替代方案，嘗試看看 LEANN 是否可以安裝了
            log_info "嘗試升級到 LEANN 完整版..."
            if "$venv_dir/bin/pip" install leann 2>/dev/null; then
                if "$venv_dir/bin/python" -c "from leann import LeannBuilder" &> /dev/null; then
                    log_success "成功升級到 LEANN 完整版！"
                    export LEANN_PYTHON="$venv_dir/bin/python"
                    return 0
                fi
            fi
            log_info "LEANN 完整版仍不可用，繼續使用替代方案"
            export LEANN_PYTHON="$venv_dir/bin/python"
            return 0
        fi

        # 虛擬環境損壞，需要重建
        log_info "清理損壞的虛擬環境..."
        rm -rf "$venv_dir"
    fi

    # 建立新虛擬環境
    if [[ ! -d "$venv_dir" ]]; then
        # 使用標準 python3 -m venv（確保有 pip）
        log_info "建立虛擬環境..."
        python3 -m venv "$venv_dir"
    fi

    # 確認虛擬環境存在且有 Python
    if [[ ! -f "$venv_dir/bin/python" ]]; then
        log_error "虛擬環境建立失敗"
        exit 1
    fi

    # 確保有 pip
    if [[ ! -f "$venv_dir/bin/pip" ]]; then
        log_info "安裝 pip..."
        "$venv_dir/bin/python" -m ensurepip --upgrade
    fi

    # 安裝 LEANN
    log_info "在虛擬環境中安裝 LEANN..."

    # 升級 pip
    "$venv_dir/bin/pip" install --upgrade pip wheel setuptools

    # 嘗試安裝 leann
    log_info "嘗試安裝 leann..."
    if "$venv_dir/bin/pip" install leann 2>&1; then
        installed=true
    else
        log_warn "標準安裝失敗，嘗試其他方式..."

        # 嘗試用 uv pip
        if command -v uv &> /dev/null; then
            log_info "嘗試 uv pip install..."
            if uv pip install leann --python "$venv_dir/bin/python" 2>&1; then
                installed=true
            fi
        fi

        # 最後嘗試只安裝核心
        if ! $installed; then
            log_warn "嘗試只安裝核心模組..."
            "$venv_dir/bin/pip" install --no-deps leann 2>/dev/null || true
            "$venv_dir/bin/pip" install numpy sentence-transformers 2>/dev/null || true

            # 檢查是否至少有基本功能
            if "$venv_dir/bin/python" -c "import leann" &> /dev/null; then
                installed=true
                log_warn "核心安裝成功，但部分 backend 可能不可用"
            fi
        fi
    fi

    # 建立 wrapper script 到 ~/.local/bin
    mkdir -p "${HOME}/.local/bin"

    # 建立 Python import 用的 wrapper
    cat > "${HOME}/.local/bin/leann-python" << 'WRAPPER'
#!/bin/bash
VENV_DIR="${HOME}/.claude/leann-venv"
exec "$VENV_DIR/bin/python" "$@"
WRAPPER
    chmod +x "${HOME}/.local/bin/leann-python"

    # 驗證安裝 - 檢查是否有可用的語義搜尋功能
    local leann_ok=false
    local st_ok=false

    # 檢查 LEANN 完整安裝
    if "$venv_dir/bin/python" -c "from leann import LeannBuilder; print('LEANN Builder OK')" 2>/dev/null; then
        log_success "LEANN 完整安裝成功"
        leann_ok=true

        # 建立 leann CLI wrapper
        cat > "${HOME}/.local/bin/leann" << 'WRAPPER'
#!/bin/bash
VENV_DIR="${HOME}/.claude/leann-venv"
exec "$VENV_DIR/bin/python" -m leann "$@"
WRAPPER
        chmod +x "${HOME}/.local/bin/leann"
    fi

    # 檢查 sentence-transformers（替代方案）
    if "$venv_dir/bin/python" -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers OK')" 2>/dev/null; then
        log_success "sentence-transformers 安裝成功"
        st_ok=true
    fi

    # 判斷結果
    if $leann_ok; then
        log_success "使用 LEANN 作為語義搜尋引擎"
        export LEANN_PYTHON="$venv_dir/bin/python"
        return 0
    elif $st_ok; then
        log_warn "LEANN Backend (HNSW) 不可用 - 將使用 sentence-transformers 替代"
        log_info "原因：leann-backend-hnsw 需要 macOS 14+ 和 Python 3.12+"
        log_success "語義搜尋環境準備完成（使用 sentence-transformers）"
        export LEANN_PYTHON="$venv_dir/bin/python"
        return 0
    else
        log_error "語義搜尋環境安裝失敗"
        log_info "請嘗試手動安裝:"
        log_info "  $venv_dir/bin/pip install sentence-transformers"
        exit 1
    fi
}

# 同步 skill repos
sync_skills() {
    log_step "同步 skill repos..."

    local sync_script="$SCRIPT_DIR/sync-skills.sh"

    if [[ -f "$sync_script" ]]; then
        bash "$sync_script"
    else
        log_warn "sync-skills.sh 不存在，手動同步..."

        mkdir -p "$SKILL_CACHE"

        # Clone claude-software-skills
        if [[ ! -d "$SKILL_CACHE/claude-software-skills" ]]; then
            log_info "Clone claude-software-skills..."
            git clone --depth 1 https://github.com/miles990/claude-software-skills.git "$SKILL_CACHE/claude-software-skills"
        else
            log_info "更新 claude-software-skills..."
            (cd "$SKILL_CACHE/claude-software-skills" && git pull --quiet) || true
        fi

        # Clone claude-domain-skills
        if [[ ! -d "$SKILL_CACHE/claude-domain-skills" ]]; then
            log_info "Clone claude-domain-skills..."
            git clone --depth 1 https://github.com/miles990/claude-domain-skills.git "$SKILL_CACHE/claude-domain-skills"
        else
            log_info "更新 claude-domain-skills..."
            (cd "$SKILL_CACHE/claude-domain-skills" && git pull --quiet) || true
        fi
    fi

    log_success "Skill repos 同步完成"
}

# 取得 LEANN Python 路徑
get_leann_python() {
    local venv_python="${HOME}/.claude/leann-venv/bin/python"
    if [[ -f "$venv_python" ]]; then
        echo "$venv_python"
    else
        echo "python3"
    fi
}

# 建立語義索引
build_leann_index() {
    log_step "建立語義向量索引..."

    mkdir -p "$(dirname "$LEANN_INDEX")"

    local LEANN_PYTHON
    LEANN_PYTHON=$(get_leann_python)
    log_info "使用 Python: $LEANN_PYTHON"

    # 使用 Python 腳本建立索引
    # 支援兩種模式：LEANN（如果可用）或 sentence-transformers 替代方案
    "$LEANN_PYTHON" << 'PYTHON_SCRIPT'
import os
import sys
import json
from pathlib import Path

SKILL_CACHE = Path.home() / ".claude" / "skill-cache"
INDEX_PATH = Path.home() / ".claude" / "leann-indexes" / "skills"

def parse_skill_md(file_path: Path) -> dict:
    """解析 SKILL.md 檔案"""
    content = file_path.read_text(encoding='utf-8')

    # 提取 frontmatter
    metadata = {
        'name': '',
        'description': '',
        'triggers': '',
        'path': str(file_path.relative_to(SKILL_CACHE)),
    }

    lines = content.split('\n')
    in_frontmatter = False
    body_lines = []

    for line in lines:
        if line.strip() == '---':
            if in_frontmatter:
                in_frontmatter = False
                continue
            else:
                in_frontmatter = True
                continue

        if in_frontmatter:
            if line.startswith('name:'):
                metadata['name'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith('description:'):
                metadata['description'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith('triggers:'):
                metadata['triggers'] = line.split(':', 1)[1].strip()
        else:
            body_lines.append(line)

    # 取前 500 字作為內容摘要
    body = '\n'.join(body_lines)[:500]
    metadata['body'] = body

    return metadata

def collect_skills():
    """收集所有 SKILL.md"""
    print(f"掃描 skill 目錄: {SKILL_CACHE}")

    skills = []
    for skill_file in SKILL_CACHE.rglob("SKILL.md"):
        # 跳過根目錄和隱藏目錄
        rel_path = skill_file.relative_to(SKILL_CACHE)
        if len(rel_path.parts) < 2:
            continue
        if any(part.startswith('.') for part in rel_path.parts):
            continue

        try:
            metadata = parse_skill_md(skill_file)
            if metadata['name']:
                skills.append(metadata)
                print(f"  ✓ {metadata['name']}")
        except Exception as e:
            print(f"  ✗ {skill_file}: {e}")

    print(f"\n共找到 {len(skills)} 個 skills")
    return skills

def build_with_leann(skills):
    """使用 LEANN 建立索引"""
    from leann import LeannBuilder

    print(f"\n建立 LEANN 索引: {INDEX_PATH}")
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    builder = LeannBuilder(backend_name="hnsw")

    for skill in skills:
        search_text = f"""
Skill: {skill['name']}
Description: {skill['description']}
Triggers: {skill['triggers']}

{skill['body']}
""".strip()

        builder.add_text(
            search_text,
            metadata={
                'name': skill['name'],
                'path': skill['path'],
                'description': skill['description'],
            }
        )

    builder.build_index(str(INDEX_PATH))
    return True

def build_with_sentence_transformers(skills):
    """使用 sentence-transformers 建立簡易向量索引（替代方案）"""
    import numpy as np
    from sentence_transformers import SentenceTransformer

    print(f"\n使用 sentence-transformers 建立索引（替代方案）")
    print("載入模型 all-MiniLM-L6-v2...")

    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 準備文本
    texts = []
    metadata_list = []

    for skill in skills:
        search_text = f"""
Skill: {skill['name']}
Description: {skill['description']}
Triggers: {skill['triggers']}

{skill['body']}
""".strip()
        texts.append(search_text)
        metadata_list.append({
            'name': skill['name'],
            'path': skill['path'],
            'description': skill['description'],
        })

    # 生成嵌入向量
    print("生成嵌入向量...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # 儲存索引
    INDEX_PATH.mkdir(parents=True, exist_ok=True)

    # 儲存為 numpy 格式
    np.save(str(INDEX_PATH / "embeddings.npy"), embeddings)

    # 儲存 metadata
    with open(INDEX_PATH / "metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=2)

    # 儲存原始文本（用於顯示）
    with open(INDEX_PATH / "texts.json", 'w', encoding='utf-8') as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 索引儲存至: {INDEX_PATH}")
    return True

def main():
    skills = collect_skills()

    if not skills:
        print("ERROR: 沒有找到任何 skill")
        sys.exit(1)

    # 嘗試使用 LEANN
    try:
        from leann import LeannBuilder
        if build_with_leann(skills):
            print(f"\n✅ LEANN 索引建立完成")
            print(f"   共索引 {len(skills)} 個 skills")
            return
    except ImportError:
        print("LEANN Builder 不可用，使用替代方案...")
    except Exception as e:
        print(f"LEANN 建立失敗: {e}")
        print("使用替代方案...")

    # 使用 sentence-transformers 替代方案
    if build_with_sentence_transformers(skills):
        print(f"\n✅ 語義索引建立完成（使用 sentence-transformers）")
        print(f"   共索引 {len(skills)} 個 skills")

if __name__ == "__main__":
    main()
PYTHON_SCRIPT

    if [[ $? -eq 0 ]]; then
        log_success "LEANN 索引建立完成"
    else
        log_error "LEANN 索引建立失敗"
        exit 1
    fi
}

# 測試搜尋
test_search() {
    log_step "測試語義搜尋..."

    echo ""
    echo "測試查詢："
    echo ""

    local LEANN_PYTHON
    LEANN_PYTHON=$(get_leann_python)

    "$LEANN_PYTHON" << 'PYTHON_SCRIPT'
import json
from pathlib import Path
import numpy as np

INDEX_PATH = Path.home() / ".claude" / "leann-indexes" / "skills"

def search_with_leann(query, top_k=3):
    """使用 LEANN 搜尋"""
    from leann import LeannSearcher
    searcher = LeannSearcher(str(INDEX_PATH))
    return searcher.search(query, top_k=top_k)

def search_with_sentence_transformers(query, top_k=3):
    """使用 sentence-transformers 搜尋（替代方案）"""
    from sentence_transformers import SentenceTransformer

    # 載入索引
    embeddings = np.load(str(INDEX_PATH / "embeddings.npy"))
    with open(INDEX_PATH / "metadata.json", 'r', encoding='utf-8') as f:
        metadata_list = json.load(f)

    # 載入模型並生成查詢向量
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query])[0]

    # 計算餘弦相似度
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # 取 top_k 結果
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            'metadata': metadata_list[idx],
            'score': float(similarities[idx])
        })
    return results

# 檢查索引是否存在
if not INDEX_PATH.exists():
    print(f"ERROR: 索引不存在: {INDEX_PATH}")
    exit(1)

# 判斷使用哪種搜尋方式
use_leann = False
try:
    from leann import LeannSearcher
    # 檢查是否有 LEANN 格式的索引
    if (INDEX_PATH / "index.bin").exists() or (INDEX_PATH / "index").exists():
        use_leann = True
except ImportError:
    pass

test_queries = [
    "卡牌遊戲開發",
    "API 設計最佳實踐",
    "量化交易策略",
    "Flutter 遊戲",
    "前端 UI 設計",
]

print(f"搜尋引擎: {'LEANN' if use_leann else 'sentence-transformers'}\n")

for query in test_queries:
    print(f"🔍 \"{query}\"")

    try:
        if use_leann:
            results = search_with_leann(query, top_k=3)
            for i, result in enumerate(results, 1):
                name = result.metadata.get('name', 'unknown')
                desc = result.metadata.get('description', '')[:50]
                score = result.score if hasattr(result, 'score') else 'N/A'
                print(f"   {i}. {name} ({score:.2f})" if isinstance(score, float) else f"   {i}. {name}")
                if desc:
                    print(f"      {desc}...")
        else:
            results = search_with_sentence_transformers(query, top_k=3)
            for i, result in enumerate(results, 1):
                name = result['metadata'].get('name', 'unknown')
                desc = result['metadata'].get('description', '')[:50]
                score = result['score']
                print(f"   {i}. {name} ({score:.2f})")
                if desc:
                    print(f"      {desc}...")
    except Exception as e:
        print(f"   ERROR: {e}")

    print()
PYTHON_SCRIPT
}

# 顯示狀態
show_status() {
    echo ""
    echo -e "${CYAN}=== LEANN Skill Discovery 狀態 ===${NC}"
    echo ""

    # 檢查 uv
    echo -n "uv:     "
    if check_uv 2>/dev/null; then
        echo -e "${GREEN}✓ 已安裝${NC}"
    else
        echo -e "${RED}✗ 未安裝${NC}"
    fi

    # 檢查 LEANN
    echo -n "LEANN:  "
    if check_leann 2>/dev/null; then
        echo -e "${GREEN}✓ 已安裝${NC}"
    else
        echo -e "${RED}✗ 未安裝${NC}"
    fi

    # 檢查 skill cache
    echo -n "Skills: "
    if [[ -d "$SKILL_CACHE/claude-software-skills" ]] && [[ -d "$SKILL_CACHE/claude-domain-skills" ]]; then
        local sw_count=$(find "$SKILL_CACHE/claude-software-skills" -name "SKILL.md" | wc -l)
        local dm_count=$(find "$SKILL_CACHE/claude-domain-skills" -name "SKILL.md" | wc -l)
        echo -e "${GREEN}✓ 已同步${NC} (software: $sw_count, domain: $dm_count)"
    else
        echo -e "${RED}✗ 未同步${NC}"
    fi

    # 檢查索引
    echo -n "Index:  "
    if [[ -d "$LEANN_INDEX" ]]; then
        local size=$(du -sh "$LEANN_INDEX" 2>/dev/null | cut -f1)
        echo -e "${GREEN}✓ 已建立${NC} ($size)"
    else
        echo -e "${RED}✗ 未建立${NC}"
    fi

    echo ""
}

# 主函數
main() {
    show_header

    case "${1:-}" in
        --status)
            show_status
            exit 0
            ;;
        --test)
            test_search
            exit 0
            ;;
        --rebuild)
            log_info "重建索引模式"
            sync_skills
            build_leann_index
            log_success "索引重建完成！"
            exit 0
            ;;
        --help|-h)
            echo "用法: $0 [選項]"
            echo ""
            echo "選項:"
            echo "  (無)       完整設定（安裝 + 同步 + 索引）"
            echo "  --rebuild  重建索引（跳過安裝檢查）"
            echo "  --test     測試語義搜尋"
            echo "  --status   查看目前狀態"
            echo "  --help     顯示此幫助"
            echo ""
            echo "設定完成後，/evolve 會自動使用語義搜尋推薦 skill"
            exit 0
            ;;
    esac

    # 完整設定流程
    log_step "Step 1/4: 檢查環境"

    # 檢查/安裝 uv
    if ! check_uv; then
        install_uv
    fi

    # 檢查/安裝 LEANN
    if ! check_leann; then
        install_leann
    fi

    echo ""
    log_step "Step 2/4: 同步 Skill Repos"
    sync_skills

    echo ""
    log_step "Step 3/4: 建立 LEANN 向量索引"
    build_leann_index

    echo ""
    log_step "Step 4/4: 驗證搜尋功能"
    test_search

    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}    ✅ LEANN Skill Discovery 設定完成！                     ${GREEN}║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "現在 /evolve 會自動使用語義搜尋推薦最相關的 skill"
    echo ""
    echo "手動搜尋："
    echo "  leann search skills \"你的任務描述\""
    echo ""
}

main "$@"
