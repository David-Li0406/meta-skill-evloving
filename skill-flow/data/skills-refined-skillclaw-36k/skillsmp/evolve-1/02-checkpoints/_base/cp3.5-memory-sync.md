# Checkpoint 3.5: Memory 同步

> 創建 Memory 文件後，**立即**同步（index.md + Memory MCP）

## 觸發時機

當執行以下操作後：
- Write 到 `.claude/memory/learnings/*.md`
- Write 到 `.claude/memory/failures/*.md`
- Write 到 `.claude/memory/decisions/*.md`
- Write 到 `.claude/memory/patterns/*.md`

## 強制步驟

```
Step 1: Write memory file (Markdown)
        ↓
Step 2: Edit index.md (添加條目)
        ↓
Step 3: memory_write (同步到 SQLite 索引)  ← Memory MCP
        ↓
Step 4: Verify (確認已更新)
```

## 範例

### 完整流程（Git Memory + Memory MCP）

```python
# Step 1: 創建 memory 文件（詳細內容）
Write(
    file_path=".claude/memory/learnings/2026-01-16-new-learning.md",
    content="..."
)

# Step 2: 立即更新 index.md（不可省略！）
Edit(
    file_path=".claude/memory/index.md",
    old_string="<!-- LEARNINGS_START -->",
    new_string="<!-- LEARNINGS_START -->\n- [New Learning](learnings/2026-01-16-new-learning.md) - tag1, tag2"
)

# Step 3: 同步到 Memory MCP（加速搜尋）
memory_write({
    "key": "learning:2026-01-16:new-learning",
    "content": "一句話摘要，方便 FTS5 搜尋",
    "tags": ["tag1", "tag2"],
    "scope": "global",
    "source": "evolve"
})

# Step 4: 驗證
Read(file_path=".claude/memory/index.md")
```

### Memory MCP 不可用時（回退方案）

```python
# 只執行 Step 1, 2, 4（跳過 Step 3）
```

## 雙重記錄的意義

| 系統 | 內容 | 用途 |
|------|------|------|
| **Git Memory** | 完整 Markdown 文件 | 人類可讀、版本控制、詳細記錄 |
| **Memory MCP** | 一句話摘要 + tags | FTS5 快速搜尋、跨專案索引 |

**建議**：
- Git Memory = 詳細文件（完整 context）
- Memory MCP = 搜尋索引（快速定位）

## 常見錯誤

| 錯誤 | 後果 | 預防 |
|------|------|------|
| 忘記更新 index | 記憶無法被搜尋到 | Write 後立即 Edit |
| 批次更新 index | 可能遺漏某些條目 | 每個 Write 配對一個 Edit |
| index 格式錯誤 | 破壞索引結構 | 使用標準格式 |
| 只更新 MCP | Git Memory 不完整 | 兩者都要更新 |

## 背景

此檢查點源自 evolve-trader 專案的實際失敗經驗：
- 創建多個 memory 文件後忘記更新 index.md
- 用戶反饋：「我看 .claude/memory 沒有新的紀錄」
- 根本原因：儲存與索引是兩個分離的動作，容易忽略後者
