# Memory MCP 整合

> 使用 [sqlite-memory-mcp](https://www.npmjs.com/package/sqlite-memory-mcp) 實現智能記憶管理、Skill 追蹤、失敗經驗索引
>
> GitHub: https://github.com/miles990/claude-memory-mcp

## 概覽

Memory MCP 提供統一的 SQLite 記憶系統，整合於 evolve 流程的關鍵檢查點：

```
CP0 ─► skill_usage_start()     # 開始追蹤
CP1 ─► memory_search()         # 搜尋經驗
    ─► failure_search()        # 搜尋失敗解法
CP3.5 ► memory_write()         # 記錄學習
CP5 ─► failure_record()        # 記錄失敗
結束 ─► skill_usage_end()      # 結束追蹤
```

## 工具清單

### Memory 工具（經驗管理）

| 工具 | 用途 | 觸發時機 |
|------|------|----------|
| `memory_write` | 寫入記憶 | CP3.5 記錄學習 |
| `memory_search` | FTS5 全文搜尋 | CP1 搜尋經驗 |
| `memory_list` | 列出記憶 | 需要瀏覽時 |
| `memory_stats` | 統計資訊 | 健檢時 |

### Skill 工具（使用追蹤）

| 工具 | 用途 | 觸發時機 |
|------|------|----------|
| `skill_usage_start` | 開始追蹤 | CP0 任務開始 |
| `skill_usage_end` | 結束追蹤 | 任務完成/失敗 |
| `skill_recommend` | 智能推薦 | 選擇 Skill 時 |
| `skill_stats` | 使用統計 | 健檢時 |

### Failure 工具（失敗索引）

| 工具 | 用途 | 觸發時機 |
|------|------|----------|
| `failure_record` | 記錄失敗 | CP5 失敗驗屍 |
| `failure_search` | 搜尋解法 | CP1 查找類似問題 |
| `failure_list` | 列出失敗 | 回顧時 |
| `failure_stats` | 失敗統計 | 健檢時 |

### Context 工具（狀態共享）

| 工具 | 用途 | 觸發時機 |
|------|------|----------|
| `context_set` | 設定狀態 | 跨 Skill 傳遞 |
| `context_get` | 取得狀態 | 讀取共享狀態 |
| `context_share` | 跨 Session | 工作交接 |

## 整合流程

### CP0: 任務開始 - 開始追蹤

```python
# 記錄 Skill 使用開始
skill_usage_start({
    "skill_name": "evolve",
    "project_path": "/path/to/project"  # 可選
})
# 返回 usage_id，供結束時使用
```

### CP1: 搜尋經驗（強化版）

**取代原本的 Grep 搜尋**：

```python
# 1. 搜尋相關記憶（FTS5 全文搜尋）
memory_search({
    "query": "關鍵字1 OR 關鍵字2",  # 支援 FTS5 語法
    "scope": "global",               # 或 "project:xxx"
    "limit": 10
})

# 2. 搜尋類似失敗經驗
failure_search({
    "query": "TypeError undefined",
    "limit": 5
})
```

**FTS5 搜尋語法**：
- `word1 word2` - 同時包含
- `word1 OR word2` - 任一包含
- `"exact phrase"` - 精確匹配
- `word*` - 前綴匹配

### CP3.5: 記錄學習

```python
# 記錄成功經驗到 SQLite
memory_write({
    "key": "learning:2026-01-16:memory-mcp-integration",
    "content": "整合 Memory MCP 到 evolve 流程，關鍵是...",
    "tags": ["memory", "mcp", "integration"],
    "scope": "global",  # 跨專案共享
    "source": "evolve"
})
```

### CP5: 記錄失敗

```python
# 記錄失敗經驗供未來查詢
failure_record({
    "error_pattern": "TypeError: Cannot read properties of undefined",
    "error_message": "完整錯誤訊息...",
    "solution": "需要先檢查 null 值",  # 如果已解決
    "skill_name": "evolve",
    "project_path": "/path/to/project"
})
```

### 任務結束: 結束追蹤

```python
# 成功完成
skill_usage_end({
    "usage_id": 123,  # 來自 skill_usage_start
    "success": True,
    "outcome": "成功整合 Memory MCP",
    "tokens_used": 15000,  # 估計值
    "notes": "可選備註"
})

# 失敗結束
skill_usage_end({
    "usage_id": 123,
    "success": False,
    "outcome": "因 X 原因失敗",
    "notes": "失敗原因分析"
})
```

## 智能推薦

根據歷史成功率推薦 Skill：

```python
skill_recommend({
    "project_type": "typescript",  # 可選過濾
    "limit": 5
})
# 返回按成功率排序的推薦列表
```

## 與 Git Memory 的關係

Memory MCP 與 `.claude/memory/` Git-based 系統**並存**：

| 系統 | 用途 | 特點 |
|------|------|------|
| **Git Memory** | 詳細學習記錄 | 版本控制、人類可讀 |
| **Memory MCP** | 快速搜尋索引 | FTS5、Token 優化 |

**建議流程**：
1. 詳細記錄寫入 `.claude/memory/` (Markdown)
2. 同時寫入 Memory MCP (SQLite) 作為索引
3. 搜尋時優先用 Memory MCP，找到後讀取原始 Markdown

## 效能對比

| 指標 | Git Memory (Grep) | Memory MCP (FTS5) |
|------|-------------------|-------------------|
| 搜尋速度 | ~20ms | ~3.5ms |
| Token/搜尋 | ~2300 | ~200 |
| 跨專案 | 需指定路徑 | 自動 |
| 失敗索引 | 無 | 有 |
| 使用追蹤 | 無 | 有 |

## 注意事項

1. **資料庫位置**: `~/.claude/claude.db`（自動建立）
2. **WAL 模式**: 支援並發讀寫
3. **自動 Schema**: 首次使用自動初始化
4. **Fallback**: 若 MCP 不可用，回退到 Git Memory

## 安裝

### 方式一：從 npm 安裝（推薦）

```bash
npm install -g sqlite-memory-mcp
```

### 方式二：從源碼安裝

```bash
git clone https://github.com/miles990/claude-memory-mcp.git
cd claude-memory-mcp
npm install && npm run build
```

## 配置

使用 CLI 安裝（推薦）：

```bash
claude mcp add --transport stdio --scope user sqlite-memory -- npx sqlite-memory-mcp
```

或在專案 `.mcp.json` 加入：

```json
{
  "mcpServers": {
    "sqlite-memory": {
      "command": "npx",
      "args": ["sqlite-memory-mcp"]
    }
  }
}
```
