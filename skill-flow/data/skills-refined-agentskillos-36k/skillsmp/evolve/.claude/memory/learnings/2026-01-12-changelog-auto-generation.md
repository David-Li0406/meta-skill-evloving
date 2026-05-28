---
date: 2026-01-12
tags: [changelog, automation, bash, conventional-commits, git]
task: 建立 CHANGELOG 自動生成腳本
status: resolved
---

# CHANGELOG 自動生成腳本

## 情境

使用 `/evolve` 執行 Phase 1 P1 任務：建立 CHANGELOG 自動生成腳本，作為「吃自己的狗糧」的第一個真實任務。

## 解決方案

創建 `scripts/generate-changelog.sh`：

### 功能
- 解析 git log 中的 conventional commits
- 自動分類：feat→Added, fix→Fixed, docs→Documentation, refactor→Changed, chore→Maintenance
- 支援 scope 解析：`feat(v4.2.0):` 會正確提取描述
- 生成 Keep a Changelog 格式輸出

### 參數
```bash
--all        # 生成所有 commits
--since TAG  # 從指定 tag 開始
--preview    # 預覽不寫入
--output     # 指定輸出檔案
--help       # 顯示幫助
```

### 核心實現

```bash
# Conventional Commits 正則解析
if [[ "$MESSAGE" =~ ^feat(\(.+\))?:\ (.+) ]]; then
    FEAT_COMMITS+=("- ${BASH_REMATCH[2]} (\`${HASH}\`)")
fi
```

## 驗證

```
✅ --help 正常顯示
✅ --preview 模式正常
✅ --since TAG 正確過濾
✅ --all 生成完整記錄
✅ feat/fix/docs/refactor/chore 全部正確分類
```

## 學習重點

1. **Bash 正則**: `[[ "$str" =~ ^pattern(.*)$ ]]` 配合 `BASH_REMATCH` 提取群組
2. **陣列操作**: `declare -a ARR=()` + `ARR+=("item")` + `${#ARR[@]}` 計數
3. **Git log 格式**: `--pretty=format:"%s|%h|%ai"` 自訂輸出格式
4. **Keep a Changelog**: 標準格式是 `## [version] - date` + `### Added/Fixed/Changed`

## 產出

- `scripts/generate-changelog.sh` - 193 行 bash 腳本
- 支援 7 種 commit 類型 + other 分類
- 完整的 --help 說明

## 效果

首次使用 `/evolve` 完成真實任務，產生了：
- 1 個新腳本
- 1 筆 learning 記錄
- PDCA 完整執行一輪
