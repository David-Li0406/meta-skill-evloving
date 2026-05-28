#!/bin/bash
# Self-Evolving Agent - Global Skill Sync Script
# 將原子化 skills 同步到全域 ~/.claude/skills/evolve/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GLOBAL_SKILL_DIR="$HOME/.claude/skills/evolve"

echo "🔄 Syncing Self-Evolving Agent to global skills..."
echo "   From: $PROJECT_ROOT/skills/"
echo "   To:   $GLOBAL_SKILL_DIR/"

# 確保全域目錄存在
mkdir -p "$GLOBAL_SKILL_DIR"

# 方法1：複製整個 skills 目錄（保持原子化結構）
if [[ "$1" == "--atomic" ]]; then
    echo ""
    echo "📦 Syncing atomic structure..."

    # 複製所有模組
    rsync -av --delete \
        --exclude='community/' \
        "$PROJECT_ROOT/skills/" \
        "$GLOBAL_SKILL_DIR/"

    echo ""
    echo "✅ Atomic structure synced to $GLOBAL_SKILL_DIR/"
    echo "   Use: /evolve [goal]"
    exit 0
fi

# 方法2：生成整合版 SKILL.md（預設）
echo ""
echo "📄 Generating integrated SKILL.md..."

# 讀取主 SKILL.md
cat "$PROJECT_ROOT/skills/SKILL.md" > "$GLOBAL_SKILL_DIR/SKILL.md"

# 追加分隔線
echo "" >> "$GLOBAL_SKILL_DIR/SKILL.md"
echo "---" >> "$GLOBAL_SKILL_DIR/SKILL.md"
echo "" >> "$GLOBAL_SKILL_DIR/SKILL.md"
echo "# 📚 完整模組內容" >> "$GLOBAL_SKILL_DIR/SKILL.md"
echo "" >> "$GLOBAL_SKILL_DIR/SKILL.md"
echo "> 以下是原子化模組的完整內容，供全域使用。" >> "$GLOBAL_SKILL_DIR/SKILL.md"
echo "" >> "$GLOBAL_SKILL_DIR/SKILL.md"

# 追加各模組內容
for module_dir in "$PROJECT_ROOT/skills"/*/; do
    module_name=$(basename "$module_dir")

    # 跳過非目錄
    [[ ! -d "$module_dir" ]] && continue

    # 跳過隱藏目錄
    [[ "$module_name" == .* ]] && continue

    echo "   Processing: $module_name"

    # 模組標題
    echo "## 📁 $module_name" >> "$GLOBAL_SKILL_DIR/SKILL.md"
    echo "" >> "$GLOBAL_SKILL_DIR/SKILL.md"

    # 讀取 _base 目錄下的所有 md 文件
    if [[ -d "$module_dir/_base" ]]; then
        for md_file in "$module_dir/_base"/*.md; do
            [[ ! -f "$md_file" ]] && continue

            file_name=$(basename "$md_file")
            echo "### 📄 $file_name" >> "$GLOBAL_SKILL_DIR/SKILL.md"
            echo "" >> "$GLOBAL_SKILL_DIR/SKILL.md"
            cat "$md_file" >> "$GLOBAL_SKILL_DIR/SKILL.md"
            echo "" >> "$GLOBAL_SKILL_DIR/SKILL.md"
        done
    fi
done

# 計算行數
line_count=$(wc -l < "$GLOBAL_SKILL_DIR/SKILL.md")

echo ""
echo "✅ Integrated SKILL.md generated!"
echo "   Location: $GLOBAL_SKILL_DIR/SKILL.md"
echo "   Lines: $line_count"
echo ""
echo "Usage: /evolve [goal]"
