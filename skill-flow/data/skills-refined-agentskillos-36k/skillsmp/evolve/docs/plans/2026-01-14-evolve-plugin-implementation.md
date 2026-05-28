# evolve Plugin v5.0 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 將現有的 evolve skill 轉換為 Claude Code Plugin 格式，並新增 Skill Creator 功能

**Architecture:**
- 建立 `evolve-plugin/` 目錄結構，包含 `.claude-plugin/plugin.json`
- 移動現有 `skills/` 到 plugin 結構
- 新增 Hooks（JSON + additionalContext 格式）強化 CheckPoint
- 新增 Skill Creator 完整工作流（4 階段）

**Tech Stack:**
- Claude Code Plugin format
- Bash scripts for hooks
- Markdown for skills/commands

---

## Phase 1: Plugin 結構建立

### Task 1.1: 建立 Plugin 目錄結構

**Files:**
- Create: `evolve-plugin/.claude-plugin/plugin.json`
- Create: `evolve-plugin/README.md`

**Step 1: 建立目錄結構**

Run:
```bash
mkdir -p evolve-plugin/.claude-plugin
mkdir -p evolve-plugin/commands/evolve
mkdir -p evolve-plugin/commands/new-skill
mkdir -p evolve-plugin/hooks
mkdir -p evolve-plugin/skills
```

**Step 2: 建立 plugin.json**

Create `evolve-plugin/.claude-plugin/plugin.json`:
```json
{
  "name": "evolve",
  "description": "Self-evolving agent + Skill creator - 自主學習、持續改進、建立新 Skill",
  "version": "5.0.0",
  "author": {
    "name": "miles990"
  }
}
```

**Step 3: 建立 README.md**

Create `evolve-plugin/README.md`:
```markdown
# evolve Plugin

> Self-Evolving Agent - 讓 AI 自主達成目標、從經驗中學習並持續改進

## 安裝

```bash
/plugin install miles990/evolve-plugin
```

## 使用

```bash
# 自我進化模式
/evolve [目標描述]

# 建立新 Skill
/evolve --new-skill [skill 名稱]
```

## 功能

- **自我進化**：PDCA 循環 + CheckPoint 護欄 + Memory 系統
- **Skill Creator**：引導式建立 + 範本 + 驗證 + 發布到 GitHub

## 文件

詳見 `skills/` 目錄下的模組化知識。
```

**Step 4: 驗證目錄結構**

Run:
```bash
tree evolve-plugin/
```

Expected:
```
evolve-plugin/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   ├── evolve/
│   └── new-skill/
├── hooks/
└── skills/
```

**Step 5: Commit**

```bash
git add evolve-plugin/
git commit -m "feat(plugin): initialize evolve-plugin structure"
```

---

### Task 1.2: 移動現有 Skills 到 Plugin

**Files:**
- Move: `skills/*` → `evolve-plugin/skills/`
- Keep: `skills/SKILL.md` as entry point reference

**Step 1: 複製 skills 到 plugin**

Run:
```bash
cp -r skills/* evolve-plugin/skills/
```

**Step 2: 驗證複製完成**

Run:
```bash
ls evolve-plugin/skills/
```

Expected:
```
00-getting-started  02-checkpoints  04-emergence    06-scaling      SKILL.md
01-core             03-memory       05-integration  99-evolution
```

**Step 3: 更新 SKILL.md 版本號為 5.0.0**

Modify `evolve-plugin/skills/SKILL.md` line 3:
```diff
- version: 4.5.0
+ version: 5.0.0
```

**Step 4: Commit**

```bash
git add evolve-plugin/skills/
git commit -m "feat(plugin): copy skills to plugin structure"
```

---

### Task 1.3: 建立 /evolve 命令

**Files:**
- Create: `evolve-plugin/commands/evolve/COMMAND.md`

**Step 1: 建立 COMMAND.md**

Create `evolve-plugin/commands/evolve/COMMAND.md`:
```markdown
---
name: evolve
description: 自我進化 Agent - 給定目標，自主學習並迭代改進直到完成
arguments:
  - name: goal
    description: 目標描述
    required: false
  - name: --explore
    description: 探索模式 - 允許自主選擇方向
    required: false
  - name: --emergence
    description: 涌現模式 - 啟用跨領域連結探索
    required: false
  - name: --autonomous
    description: 自主模式 - 完全自主，追求系統性創新
    required: false
  - name: --new-skill
    description: 建立新 Skill（完整工作流）
    required: false
---

# /evolve

執行 Self-Evolving Agent 流程。

## 流程

1. **CP0: 北極星錨定** — 建立或讀取專案願景
2. **PSB System** — Plan → Setup → Build（環境準備）
3. **目標分析** — 深度訪談 + 架構等級判斷
4. **能力評估 → Skill 習得**
5. **PDCA Cycle** — Plan → Do → Check → Act（含方向校正）
6. **Memory 記錄** — Git-based 學習記錄
7. **CP6: 專案健檢** — 每 5 次迭代檢查

## 使用範例

```bash
# 基本使用
/evolve 建立一個 ComfyUI 工作流程

# 探索模式
/evolve --explore 優化這段程式碼

# 建立新 Skill
/evolve --new-skill "git commit helper"
```

## 詳細文件

參見 `skills/SKILL.md` 和各模組目錄。
```

**Step 2: Commit**

```bash
git add evolve-plugin/commands/evolve/
git commit -m "feat(plugin): add /evolve command"
```

---

## Phase 2: Hooks 實作

### Task 2.1: 建立 CheckPoint 提醒 Hook

**Files:**
- Create: `evolve-plugin/hooks/checkpoint-reminder.json`
- Create: `evolve-plugin/hooks/checkpoint-reminder.sh`

**Step 1: 建立 hook 配置 JSON**

Create `evolve-plugin/hooks/checkpoint-reminder.json`:
```json
{
  "hooks": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/checkpoint-reminder.sh"
        }
      ]
    }
  ]
}
```

**Step 2: 建立 hook 腳本**

Create `evolve-plugin/hooks/checkpoint-reminder.sh`:
```bash
#!/bin/bash
# CheckPoint 提醒 Hook
# 輸出 JSON 格式，讓 Claude 透過 additionalContext 看到提醒

cat << 'EOF'
{
  "additionalContext": "🔍 CheckPoint 提醒：\n• CP1.5: 確認已檢查現有實作、專案慣例\n• CP2: 記得執行編譯+測試驗證"
}
EOF
```

**Step 3: 設定執行權限**

Run:
```bash
chmod +x evolve-plugin/hooks/checkpoint-reminder.sh
```

**Step 4: 測試腳本輸出**

Run:
```bash
./evolve-plugin/hooks/checkpoint-reminder.sh
```

Expected:
```json
{
  "additionalContext": "🔍 CheckPoint 提醒：\n• CP1.5: 確認已檢查現有實作、專案慣例\n• CP2: 記得執行編譯+測試驗證"
}
```

**Step 5: Commit**

```bash
git add evolve-plugin/hooks/checkpoint-reminder.*
git commit -m "feat(plugin): add checkpoint reminder hook"
```

---

### Task 2.2: 建立 Memory 同步 Hook

**Files:**
- Create: `evolve-plugin/hooks/memory-sync.json`
- Create: `evolve-plugin/hooks/memory-sync.sh`

**Step 1: 建立 hook 配置 JSON**

Create `evolve-plugin/hooks/memory-sync.json`:
```json
{
  "hooks": [
    {
      "matcher": "Write",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/memory-sync.sh"
        }
      ]
    }
  ]
}
```

**Step 2: 建立 hook 腳本**

Create `evolve-plugin/hooks/memory-sync.sh`:
```bash
#!/bin/bash
# Memory 同步提醒 Hook
# 只在寫入 .claude/memory/ 目錄時觸發

FILE="$CLAUDE_TOOL_ARG_FILE_PATH"

if [[ "$FILE" == *".claude/memory/"* ]]; then
  cat << 'EOF'
{
  "additionalContext": "📝 CP3.5: 已創建 Memory 文件，記得同步 index.md"
}
EOF
fi
```

**Step 3: 設定執行權限**

Run:
```bash
chmod +x evolve-plugin/hooks/memory-sync.sh
```

**Step 4: 測試腳本（模擬 memory 路徑）**

Run:
```bash
CLAUDE_TOOL_ARG_FILE_PATH="/test/.claude/memory/test.md" ./evolve-plugin/hooks/memory-sync.sh
```

Expected:
```json
{
  "additionalContext": "📝 CP3.5: 已創建 Memory 文件，記得同步 index.md"
}
```

**Step 5: 測試腳本（非 memory 路徑）**

Run:
```bash
CLAUDE_TOOL_ARG_FILE_PATH="/test/src/file.ts" ./evolve-plugin/hooks/memory-sync.sh
```

Expected: (no output)

**Step 6: Commit**

```bash
git add evolve-plugin/hooks/memory-sync.*
git commit -m "feat(plugin): add memory sync reminder hook"
```

---

## Phase 3: Skill Creator 實作

### Task 3.1: 建立 Skill Creator 知識模組

**Files:**
- Create: `evolve-plugin/skills/skill-creator/SKILL.md`

**Step 1: 建立目錄**

Run:
```bash
mkdir -p evolve-plugin/skills/skill-creator/templates
mkdir -p evolve-plugin/skills/skill-creator/scripts
```

**Step 2: 建立 SKILL.md**

Create `evolve-plugin/skills/skill-creator/SKILL.md`:
```markdown
---
name: skill-creator
version: 1.0.0
description: 引導式建立新 Skill 的完整工作流
triggers: [new-skill, create-skill, 建立skill, 新增skill]
---

# Skill Creator

> 完整工作流：引導式訪談 → 分析生成 → 驗證 → 發布到 GitHub

## 使用方式

```bash
/evolve --new-skill "skill 名稱"
```

## 四階段流程

### Stage 1: 引導式訪談

向使用者提問，收集需求：

1. **問題定義**：這個 skill 要解決什麼問題？
2. **目標使用者**：新手 / 進階 / 專家？
3. **前置需求**：需要什麼 MCP servers 或 CLI tools？
4. **參考來源**：有沒有類似的 skill 可以參考？

輸出：內部需求文件

### Stage 2: 分析 + 生成

1. 搜尋 GitHub 上類似的 skills 作為參考
2. 選擇適合的範本（basic / advanced）
3. 生成 SKILL.md 初稿
4. 建立目錄結構（如需要 scripts/templates）

輸出：完整的 skill 目錄

### Stage 3: 驗證

檢查清單：
- [ ] SKILL.md frontmatter 格式正確
- [ ] 必要欄位存在（name, description, version）
- [ ] 模擬使用情境，確認指令清楚
- [ ] 如有 scripts，確認可執行

輸出：驗證報告

### Stage 4: 發布到 GitHub

1. 詢問：建立新 repo 或加入現有 repo？
2. 生成 README.md
3. git init + commit + push
4. 輸出安裝指令

輸出：
```
✅ Skill 已發布！

GitHub: https://github.com/<user>/<repo>
安裝: /plugin install <user>/<repo>
```

## 範本選擇指南

| 情況 | 範本 |
|------|------|
| 簡單指令、無依賴 | basic-skill.md |
| 需要 MCP、有複雜流程 | advanced-skill.md |

## 驗證腳本

```bash
./scripts/validate-skill.sh <skill-directory>
```

## 發布腳本

```bash
./scripts/publish-skill.sh <skill-directory> [--new-repo]
```
```

**Step 3: Commit**

```bash
git add evolve-plugin/skills/skill-creator/SKILL.md
git commit -m "feat(plugin): add skill-creator knowledge module"
```

---

### Task 3.2: 建立 Skill 範本

**Files:**
- Create: `evolve-plugin/skills/skill-creator/templates/basic-skill.md`
- Create: `evolve-plugin/skills/skill-creator/templates/advanced-skill.md`

**Step 1: 建立基礎範本**

Create `evolve-plugin/skills/skill-creator/templates/basic-skill.md`:
```markdown
---
name: {{NAME}}
version: 1.0.0
description: {{DESCRIPTION}}
triggers: [{{TRIGGERS}}]
---

# {{NAME}}

> {{DESCRIPTION}}

## When to Use

- {{USE_CASE_1}}
- {{USE_CASE_2}}

## Instructions

{{INSTRUCTIONS}}

## Examples

```
{{EXAMPLE}}
```

## Notes

{{NOTES}}
```

**Step 2: 建立進階範本**

Create `evolve-plugin/skills/skill-creator/templates/advanced-skill.md`:
```markdown
---
name: {{NAME}}
version: 1.0.0
description: {{DESCRIPTION}}
triggers: [{{TRIGGERS}}]
dependencies:
  mcp:
    - package: "{{MCP_PACKAGE}}"
---

# {{NAME}}

> {{DESCRIPTION}}

## Overview

{{OVERVIEW}}

## Prerequisites

- {{PREREQ_1}}
- {{PREREQ_2}}

## When to Use

| Scenario | Action |
|----------|--------|
| {{SCENARIO_1}} | {{ACTION_1}} |
| {{SCENARIO_2}} | {{ACTION_2}} |

## Instructions

### Step 1: {{STEP_1_TITLE}}

{{STEP_1_CONTENT}}

### Step 2: {{STEP_2_TITLE}}

{{STEP_2_CONTENT}}

## Configuration

```json
{{CONFIG_EXAMPLE}}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| {{ISSUE_1}} | {{SOLUTION_1}} |
| {{ISSUE_2}} | {{SOLUTION_2}} |

## Related Skills

- {{RELATED_SKILL_1}}
- {{RELATED_SKILL_2}}
```

**Step 3: Commit**

```bash
git add evolve-plugin/skills/skill-creator/templates/
git commit -m "feat(plugin): add skill templates (basic + advanced)"
```

---

### Task 3.3: 建立驗證腳本

**Files:**
- Create: `evolve-plugin/skills/skill-creator/scripts/validate-skill.sh`

**Step 1: 建立驗證腳本**

Create `evolve-plugin/skills/skill-creator/scripts/validate-skill.sh`:
```bash
#!/bin/bash
# Skill 驗證腳本
# 用法: ./validate-skill.sh <skill-directory>

set -e

SKILL_DIR="$1"

if [ -z "$SKILL_DIR" ]; then
  echo "❌ 用法: ./validate-skill.sh <skill-directory>"
  exit 1
fi

if [ ! -d "$SKILL_DIR" ]; then
  echo "❌ 目錄不存在: $SKILL_DIR"
  exit 1
fi

SKILL_FILE="$SKILL_DIR/SKILL.md"

if [ ! -f "$SKILL_FILE" ]; then
  echo "❌ SKILL.md 不存在"
  exit 1
fi

echo "🔍 驗證 Skill: $SKILL_DIR"
echo ""

# 檢查 frontmatter
echo "檢查 frontmatter..."

if ! head -1 "$SKILL_FILE" | grep -q "^---$"; then
  echo "  ❌ 缺少 frontmatter 開頭 (---)"
  exit 1
fi
echo "  ✅ frontmatter 開頭存在"

# 檢查必要欄位
if ! grep -q "^name:" "$SKILL_FILE"; then
  echo "  ❌ 缺少 name 欄位"
  exit 1
fi
echo "  ✅ name 欄位存在"

if ! grep -q "^description:" "$SKILL_FILE"; then
  echo "  ❌ 缺少 description 欄位"
  exit 1
fi
echo "  ✅ description 欄位存在"

if ! grep -q "^version:" "$SKILL_FILE"; then
  echo "  ❌ 缺少 version 欄位"
  exit 1
fi
echo "  ✅ version 欄位存在"

# 檢查 scripts 是否可執行
if [ -d "$SKILL_DIR/scripts" ]; then
  echo ""
  echo "檢查 scripts..."
  for script in "$SKILL_DIR/scripts/"*.sh; do
    if [ -f "$script" ]; then
      if [ -x "$script" ]; then
        echo "  ✅ $script 可執行"
      else
        echo "  ⚠️ $script 不可執行，正在修正..."
        chmod +x "$script"
        echo "  ✅ 已修正"
      fi
    fi
  done
fi

echo ""
echo "✅ 驗證通過！"
```

**Step 2: 設定執行權限**

Run:
```bash
chmod +x evolve-plugin/skills/skill-creator/scripts/validate-skill.sh
```

**Step 3: 測試驗證腳本**

Run:
```bash
./evolve-plugin/skills/skill-creator/scripts/validate-skill.sh evolve-plugin/skills/skill-creator
```

Expected:
```
🔍 驗證 Skill: evolve-plugin/skills/skill-creator

檢查 frontmatter...
  ✅ frontmatter 開頭存在
  ✅ name 欄位存在
  ✅ description 欄位存在
  ✅ version 欄位存在

✅ 驗證通過！
```

**Step 4: Commit**

```bash
git add evolve-plugin/skills/skill-creator/scripts/validate-skill.sh
git commit -m "feat(plugin): add skill validation script"
```

---

### Task 3.4: 建立發布腳本

**Files:**
- Create: `evolve-plugin/skills/skill-creator/scripts/publish-skill.sh`

**Step 1: 建立發布腳本**

Create `evolve-plugin/skills/skill-creator/scripts/publish-skill.sh`:
```bash
#!/bin/bash
# Skill 發布腳本
# 用法: ./publish-skill.sh <skill-directory> [--new-repo]

set -e

SKILL_DIR="$1"
NEW_REPO="$2"

if [ -z "$SKILL_DIR" ]; then
  echo "❌ 用法: ./publish-skill.sh <skill-directory> [--new-repo]"
  exit 1
fi

if [ ! -d "$SKILL_DIR" ]; then
  echo "❌ 目錄不存在: $SKILL_DIR"
  exit 1
fi

SKILL_FILE="$SKILL_DIR/SKILL.md"
SKILL_NAME=$(grep "^name:" "$SKILL_FILE" | sed 's/name: *//')
SKILL_DESC=$(grep "^description:" "$SKILL_FILE" | sed 's/description: *//')

echo "📦 準備發布 Skill: $SKILL_NAME"
echo "   描述: $SKILL_DESC"
echo ""

# 生成 README.md
README_FILE="$SKILL_DIR/README.md"
if [ ! -f "$README_FILE" ]; then
  echo "📝 生成 README.md..."
  cat > "$README_FILE" << EOF
# $SKILL_NAME

> $SKILL_DESC

## 安裝

\`\`\`bash
/plugin install <user>/<repo>
\`\`\`

## 使用

參見 SKILL.md

## License

MIT
EOF
  echo "  ✅ README.md 已生成"
fi

# Git 操作
cd "$SKILL_DIR"

if [ "$NEW_REPO" == "--new-repo" ]; then
  echo ""
  echo "🆕 建立新 repo..."
  if [ ! -d ".git" ]; then
    git init
    echo "  ✅ git init 完成"
  fi
fi

if [ -d ".git" ]; then
  echo ""
  echo "📤 準備 commit..."
  git add -A
  git status
  echo ""
  echo "⏸️ 請手動執行:"
  echo "   git commit -m 'feat: initial skill release'"
  echo "   git remote add origin <your-repo-url>"
  echo "   git push -u origin main"
else
  echo ""
  echo "⚠️ 不是 git repo，請先執行:"
  echo "   cd $SKILL_DIR"
  echo "   git init"
fi

echo ""
echo "✅ 發布準備完成！"
```

**Step 2: 設定執行權限**

Run:
```bash
chmod +x evolve-plugin/skills/skill-creator/scripts/publish-skill.sh
```

**Step 3: Commit**

```bash
git add evolve-plugin/skills/skill-creator/scripts/publish-skill.sh
git commit -m "feat(plugin): add skill publish script"
```

---

### Task 3.5: 建立 /new-skill 命令

**Files:**
- Create: `evolve-plugin/commands/new-skill/COMMAND.md`

**Step 1: 建立 COMMAND.md**

Create `evolve-plugin/commands/new-skill/COMMAND.md`:
```markdown
---
name: new-skill
description: 引導式建立新 Skill - 完整工作流（訪談 → 生成 → 驗證 → 發布）
arguments:
  - name: name
    description: Skill 名稱
    required: true
---

# /new-skill

引導式建立新 Skill 的完整工作流。

## 別名

```bash
/evolve --new-skill <name>
```

## 流程

### Stage 1: 引導式訪談

我會問你以下問題：

1. **問題定義**：這個 skill 要解決什麼問題？
2. **目標使用者**：新手 / 進階 / 專家？
3. **前置需求**：需要什麼 MCP servers 或 CLI tools？
4. **參考來源**：有沒有類似的 skill 可以參考？

### Stage 2: 分析 + 生成

1. 搜尋類似 skills 作為參考
2. 選擇範本（basic / advanced）
3. 生成 SKILL.md 初稿
4. 建立目錄結構

### Stage 3: 驗證

執行驗證腳本檢查：
- SKILL.md frontmatter 格式
- 必要欄位存在
- scripts 可執行

### Stage 4: 發布到 GitHub

1. 建立新 repo 或加入現有 repo
2. 生成 README.md
3. git commit + push
4. 輸出安裝指令

## 範本

- `basic-skill.md` - 簡單指令，無依賴
- `advanced-skill.md` - 需要 MCP，複雜流程

## 使用範例

```bash
/new-skill "git commit helper"
/new-skill "api-documentation-generator"
```
```

**Step 2: Commit**

```bash
git add evolve-plugin/commands/new-skill/
git commit -m "feat(plugin): add /new-skill command"
```

---

## Phase 4: 整合測試

### Task 4.1: 驗證 Plugin 結構完整性

**Step 1: 檢查目錄結構**

Run:
```bash
tree evolve-plugin/ -L 3
```

Expected structure:
```
evolve-plugin/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   ├── evolve/
│   │   └── COMMAND.md
│   └── new-skill/
│       └── COMMAND.md
├── hooks/
│   ├── checkpoint-reminder.json
│   ├── checkpoint-reminder.sh
│   ├── memory-sync.json
│   └── memory-sync.sh
└── skills/
    ├── 00-getting-started/
    ├── 01-core/
    ├── ...
    └── skill-creator/
        ├── SKILL.md
        ├── scripts/
        └── templates/
```

**Step 2: 驗證 plugin.json 格式**

Run:
```bash
cat evolve-plugin/.claude-plugin/plugin.json | python3 -m json.tool
```

Expected: Valid JSON output

**Step 3: 驗證所有 hooks JSON 格式**

Run:
```bash
for f in evolve-plugin/hooks/*.json; do echo "=== $f ===" && cat "$f" | python3 -m json.tool; done
```

Expected: All valid JSON

**Step 4: 驗證所有 scripts 可執行**

Run:
```bash
find evolve-plugin -name "*.sh" -exec ls -la {} \;
```

Expected: All .sh files have `x` permission

---

### Task 4.2: 最終 Commit

**Step 1: 查看所有變更**

Run:
```bash
git status
```

**Step 2: 如有未 commit 的變更，一次性 commit**

Run:
```bash
git add evolve-plugin/
git commit -m "feat(plugin): complete evolve-plugin v5.0.0

- Plugin structure with .claude-plugin/plugin.json
- /evolve command for self-evolving workflow
- /new-skill command for skill creation workflow
- Hooks for CheckPoint reminders (JSON + additionalContext)
- Skill Creator with templates and scripts
- All existing skills migrated"
```

---

## Phase 5: 文件更新

### Task 5.1: 更新主 README

**Files:**
- Modify: `README.md`

**Step 1: 在 README.md 添加 Plugin 安裝說明**

在 Quick Start 或 Installation 區塊添加：
```markdown
## 安裝 (Plugin 版本)

```bash
/plugin install miles990/evolve-plugin
```

## 安裝 (傳統 Skill 版本)

```bash
# 全域安裝
cp -r skills/evolve ~/.claude/skills/
```
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add plugin installation instructions"
```

---

## Summary

| Phase | Tasks | 預計檔案數 |
|-------|-------|-----------|
| 1: Plugin 結構 | 3 | 5 |
| 2: Hooks | 2 | 4 |
| 3: Skill Creator | 5 | 6 |
| 4: 整合測試 | 2 | 0 |
| 5: 文件更新 | 1 | 1 |
| **Total** | **13** | **16** |

---

## Execution Checklist

- [ ] Phase 1: Plugin 結構建立
  - [ ] Task 1.1: 建立 Plugin 目錄結構
  - [ ] Task 1.2: 移動現有 Skills 到 Plugin
  - [ ] Task 1.3: 建立 /evolve 命令
- [ ] Phase 2: Hooks 實作
  - [ ] Task 2.1: 建立 CheckPoint 提醒 Hook
  - [ ] Task 2.2: 建立 Memory 同步 Hook
- [ ] Phase 3: Skill Creator 實作
  - [ ] Task 3.1: 建立 Skill Creator 知識模組
  - [ ] Task 3.2: 建立 Skill 範本
  - [ ] Task 3.3: 建立驗證腳本
  - [ ] Task 3.4: 建立發布腳本
  - [ ] Task 3.5: 建立 /new-skill 命令
- [ ] Phase 4: 整合測試
  - [ ] Task 4.1: 驗證 Plugin 結構完整性
  - [ ] Task 4.2: 最終 Commit
- [ ] Phase 5: 文件更新
  - [ ] Task 5.1: 更新主 README
