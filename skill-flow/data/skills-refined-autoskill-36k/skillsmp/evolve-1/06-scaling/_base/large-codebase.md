# Large Codebase 優化

> 將 Claude Code 檔案搜尋時間從 **8 秒降到 200 毫秒**

## 問題診斷

### 何時需要此優化

| 症狀 | 診斷 |
|------|------|
| 檔案搜尋需要 2+ 秒 | 可能需要優化 |
| 提及檔案名時明顯延遲 | 需要優化 |
| 專案檔案數 > 10,000 | 建議預防性優化 |
| 大型 monorepo | 強烈建議 |

### 預設行為說明

Claude Code 預設使用 fast filesystem traversal：
- 對小型專案效果良好
- 大型專案會逐漸變慢
- 每次搜尋都重新遍歷檔案系統

## 解決方案：fileSuggestion 自訂配置

### 核心概念

```
預設：每次搜尋 → 遍歷所有檔案 → 返回結果（慢）
優化：搜尋 → 查詢索引 → 返回結果（快）
```

使用自訂索引腳本取代預設的檔案系統遍歷。

### 配置步驟

#### Step 1: 建立索引腳本

```bash
# ~/.claude/file-suggestion.sh
#!/bin/bash
# 快速檔案索引腳本

CACHE_FILE="${HOME}/.claude/file-index-cache"
CACHE_TTL=300  # 快取有效期：5 分鐘

# 檢查快取是否有效
if [[ -f "$CACHE_FILE" ]]; then
    # macOS 和 Linux 相容的快取年齡檢查
    if [[ "$(uname)" == "Darwin" ]]; then
        age=$(($(date +%s) - $(stat -f %m "$CACHE_FILE")))
    else
        age=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE")))
    fi

    if [[ $age -lt $CACHE_TTL ]]; then
        cat "$CACHE_FILE"
        exit 0
    fi
fi

# 重建索引
# 優先使用 fd（更快），回退到 find
if command -v fd &>/dev/null; then
    fd --type f \
       --hidden \
       --exclude .git \
       --exclude node_modules \
       --exclude __pycache__ \
       --exclude .venv \
       --exclude dist \
       --exclude build \
       > "$CACHE_FILE"
else
    find . -type f \
        -not -path '*/.git/*' \
        -not -path '*/node_modules/*' \
        -not -path '*/__pycache__/*' \
        -not -path '*/.venv/*' \
        -not -path '*/dist/*' \
        -not -path '*/build/*' \
        > "$CACHE_FILE"
fi

cat "$CACHE_FILE"
```

設定執行權限：

```bash
chmod +x ~/.claude/file-suggestion.sh
```

#### Step 2: 配置 Claude Code

```json
// ~/.claude/settings.json 或專案內 .claude/settings.json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

#### Step 3: 驗證效果

```bash
# 測試腳本執行時間
time ~/.claude/file-suggestion.sh

# 預期結果：
# - 首次執行：根據專案大小，可能需要數秒
# - 快取命中：< 100ms
```

## 進階配置

### 專案特定排除

根據專案類型調整排除清單：

```bash
# Node.js 專案
--exclude node_modules --exclude .next --exclude .nuxt

# Python 專案
--exclude __pycache__ --exclude .venv --exclude .tox

# Rust 專案
--exclude target

# iOS/Android 專案
--exclude Pods --exclude build --exclude .gradle
```

### 多專案支援

若同時處理多個專案，可以依據當前目錄動態調整：

```bash
#!/bin/bash
# 進階版：依專案目錄使用不同快取

PROJECT_HASH=$(pwd | md5sum | cut -d' ' -f1)
CACHE_FILE="${HOME}/.claude/file-index-${PROJECT_HASH}"
# ... 後續邏輯相同
```

### 手動刷新快取

當新增大量檔案後，手動刷新：

```bash
rm ~/.claude/file-index-cache
# 下次搜尋會自動重建
```

## 效能對比

| 情境 | 預設 | 優化後 |
|------|------|--------|
| 10,000 檔案專案 | ~2 秒 | ~100ms |
| 50,000 檔案 monorepo | ~8 秒 | ~200ms |
| 100,000+ 檔案 | 可能超時 | ~500ms |

## 適用場景

### 建議使用

- ✅ 大型企業專案（TikTok、Google 級別）
- ✅ Monorepo 架構
- ✅ 檔案搜尋已明顯變慢
- ✅ 需要流暢開發體驗

### 不建議使用

- ❌ 小型專案（< 1,000 檔案）
- ❌ 檔案頻繁變動且需要即時反映
- ❌ 不熟悉命令列操作

## 限制和注意事項

1. **快取延遲**：新建檔案在快取過期前不會被索引
2. **維護成本**：需要確保腳本在所有環境都能執行
3. **fd 依賴**：建議安裝 `fd` 以獲得最佳效能（`brew install fd` / `apt install fd-find`）

## 相關資源

- [Boris Cherny Tips](../../../.claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md) - 大型 Codebase 優化段落
- 來源：TikTok iOS 工程師 @leocooout 分享
