# SQLite 統一架構 - PDCA Plan

> 建立日期：2026-01-16
> 狀態：計劃中
> 北極星：sqlite-memory-system.md

## 願景

**單一資料庫統一管理整個 AI 助手生態系** — 整合 Memory、skillpkg、Context、失敗經驗。

## 架構設計

### 統一資料庫位置

```
~/.claude/claude.db
```

### Schema 設計

```sql
-- 1. Memory 表 (原 evolve memory)
CREATE TABLE memory (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,                        -- JSON array
    scope TEXT DEFAULT 'global',      -- 'global' | 'project:{name}'
    source TEXT,                      -- 'evolve' | 'skillpkg' | 'manual'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Skills 表 (取代 .skillpkg/state.json)
CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    version TEXT NOT NULL,
    source TEXT NOT NULL,
    project_path TEXT,
    installed_by TEXT,
    installed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used_at DATETIME,
    use_count INTEGER DEFAULT 0
);

-- 3. Skill Usage 表 (效果追蹤)
CREATE TABLE skill_usage (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    project_path TEXT,
    started_at DATETIME,
    completed_at DATETIME,
    success BOOLEAN,
    outcome TEXT,
    tokens_used INTEGER,
    notes TEXT,
    FOREIGN KEY (skill_name) REFERENCES skills(name)
);

-- 4. Failures 表 (失敗經驗共享)
CREATE TABLE failures (
    id INTEGER PRIMARY KEY,
    error_pattern TEXT NOT NULL,
    error_message TEXT,
    solution TEXT,
    skill_name TEXT,
    project_path TEXT,
    occurrence_count INTEGER DEFAULT 1,
    last_seen_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Context 表 (跨 Skill 狀態)
CREATE TABLE context (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    skill_name TEXT,
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, key)
);

-- Indexes
CREATE INDEX idx_memory_scope ON memory(scope);
CREATE INDEX idx_memory_source ON memory(source);
CREATE INDEX idx_skills_name ON skills(name);
CREATE INDEX idx_skill_usage_skill ON skill_usage(skill_name);
CREATE INDEX idx_failures_pattern ON failures(error_pattern);
CREATE INDEX idx_context_session ON context(session_id);

-- FTS5 全文搜尋
CREATE VIRTUAL TABLE memory_fts USING fts5(key, content, tags);
CREATE VIRTUAL TABLE failures_fts USING fts5(error_pattern, error_message, solution);
```

## MCP Server 設計

### 工具清單

| 工具 | 功能 | 參數 |
|------|------|------|
| `memory_write` | 寫入記憶 | key, content, tags?, scope? |
| `memory_read` | 讀取記憶 | key |
| `memory_search` | 搜尋記憶 | query, scope?, limit? |
| `memory_list` | 列出記憶 | scope?, prefix? |
| `memory_delete` | 刪除記憶 | key |
| `skill_register` | 註冊 skill | name, version, source |
| `skill_usage_start` | 開始使用 | skill_name |
| `skill_usage_end` | 結束使用 | skill_name, success, outcome |
| `skill_recommend` | 智能推薦 | project_type? |
| `failure_record` | 記錄失敗 | error_pattern, solution |
| `failure_search` | 搜尋解法 | error_message |
| `context_set` | 設定 context | key, value, expires? |
| `context_get` | 取得 context | key |
| `context_clear` | 清除 session | session_id? |

### Server 架構

```
claude-memory-mcp/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts           # MCP Server 入口
│   ├── database.ts        # SQLite 連接管理
│   ├── tools/
│   │   ├── memory.ts      # memory_* 工具
│   │   ├── skills.ts      # skill_* 工具
│   │   ├── failures.ts    # failure_* 工具
│   │   └── context.ts     # context_* 工具
│   └── migrations/
│       └── 001_initial.sql
└── README.md
```

## 實作階段

### Phase 1: 核心基礎 (MCP Server)

**工作項目**:
- [ ] 建立 MCP Server 專案結構
- [ ] 實作 SQLite 連接管理
- [ ] 實作 memory_* 工具
- [ ] 實作 FTS5 搜尋
- [ ] 單元測試

**驗收標準**:
- memory_write/read/search 正常運作
- FTS5 搜尋 < 5ms
- 無外部相依 (pure SQLite)

### Phase 2: 遷移 evolve memory

**工作項目**:
- [ ] 撰寫遷移腳本
- [ ] 遷移現有 .claude/memory/*.md
- [ ] 更新 evolve skill CP1 使用新工具
- [ ] 更新 evolve skill CP3.5 使用新工具
- [ ] 保留 filesystem fallback

**驗收標準**:
- 所有現有 memory 成功遷移
- Token 使用減少 > 50%
- 搜尋速度提升 > 3x

### Phase 3: skillpkg 整合

**工作項目**:
- [ ] 實作 skill_* 工具
- [ ] 修改 skillpkg StateManager
- [ ] 遷移現有 state.json
- [ ] 效果追蹤功能

**驗收標準**:
- skillpkg 正常運作
- 跨專案 skill 可見
- 使用統計可查詢

### Phase 4: 失敗經驗系統

**工作項目**:
- [ ] 實作 failure_* 工具
- [ ] 建立失敗模式識別
- [ ] 整合到 evolve skill
- [ ] 自動建議解法

**驗收標準**:
- 錯誤可索引
- 解法可搜尋
- 重複錯誤自動提示

### Phase 5: 智能推薦

**工作項目**:
- [ ] 實作 skill_recommend 工具
- [ ] 基於歷史成功率推薦
- [ ] 基於專案類型推薦
- [ ] 整合到 Claude Code

**驗收標準**:
- 推薦準確率 > 70%
- 回應時間 < 10ms

## 效益預估

| 指標 | 現況 | 目標 | 方法 |
|------|------|------|------|
| Token/搜尋 | ~2300 | < 200 | FTS5 精確查詢 |
| 搜尋速度 | ~20ms | < 5ms | SQLite index |
| 跨專案共享 | ❌ | ✅ | 統一資料庫 |
| Skill 追蹤 | ❌ | ✅ | skill_usage 表 |
| 失敗共享 | ❌ | ✅ | failures 表 |
| 狀態文件 | N 個 | 1 個 | 統一 DB |

## 風險與緩解

| 風險 | 影響 | 緩解措施 |
|------|------|---------|
| 資料庫損壞 | 高 | 定期備份、WAL 模式 |
| 遷移失敗 | 中 | 保留原始文件、可回滾 |
| MCP 不穩定 | 中 | Filesystem fallback |
| 效能不如預期 | 低 | 已有 benchmark 驗證 |

## 成功標準

- [ ] MCP Server 運作穩定
- [ ] Token 使用減少 > 50%
- [ ] 搜尋速度 < 5ms
- [ ] 跨專案 memory 可用
- [ ] Skill 效果可追蹤
- [ ] 失敗經驗可搜尋
