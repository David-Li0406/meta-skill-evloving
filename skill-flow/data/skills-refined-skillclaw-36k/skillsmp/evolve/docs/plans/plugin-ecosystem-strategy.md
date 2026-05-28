# Plugin 生態系統整合策略

> 完整規劃：evolve Plugin 升級 + skillpkg 轉型藍圖

**建立日期**: 2026-01-14
**版本**: v1.0

---

## 一、北極星錨定

### 願景

```
建立一個完整的 AI Agent 工具生態系統：

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   evolve Plugin          skillpkg MCP               User            │
│   ═══════════════        ═══════════                ════            │
│                                                                     │
│   提供「自我進化」       提供「發現+管理」           一鍵安裝        │
│   的核心能力             的生態系統工具              即可使用        │
│                                                                     │
│   Skill + Hooks +        搜尋 + 推薦 +              /evolve         │
│   Agents + Commands      安裝 + 同步                 直接用          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 完成標準

| 項目 | 驗收條件 |
|------|----------|
| **evolve Plugin** | `/plugin install evolve` 一鍵安裝，包含所有功能 |
| **skillpkg 轉型** | 支援 Plugin 格式搜尋、分析、推薦 |
| **整合運作** | 兩者協同，無重複功能 |

### 不做清單

- ❌ 不重新發明 Plugin 安裝機制（用官方 /plugin）
- ❌ 不維護 Plugin registry（用 GitHub）
- ❌ 不改變 SKILL.md 格式（保持相容）

---

## 二、evolve Plugin 架構設計

### 2.1 目錄結構

```
evolve-plugin/
├── .claude-plugin/
│   └── plugin.json                    # Plugin 元資料
│
├── commands/
│   └── evolve/
│       └── COMMAND.md                 # /evolve 命令定義
│
├── agents/
│   ├── goal-analyzer/
│   │   └── AGENT.md                   # 目標分析 Agent
│   ├── pdca-executor/
│   │   └── AGENT.md                   # PDCA 執行 Agent
│   └── memory-manager/
│       └── AGENT.md                   # Memory 管理 Agent
│
├── skills/
│   ├── 00-getting-started/            # 入門模組
│   ├── 01-core/                       # 核心流程
│   ├── 02-checkpoints/                # CheckPoint 護欄
│   ├── 03-memory/                     # Memory 系統
│   ├── 04-emergence/                  # 涌現機制
│   ├── 05-integration/                # 外部整合
│   ├── 06-scaling/                    # 大規模優化
│   └── 99-evolution/                  # 自我進化
│
├── hooks/
│   ├── checkpoint-reminder.sh         # CheckPoint 提醒 Hook
│   └── memory-sync-reminder.sh        # Memory 同步提醒
│
├── README.md
└── CHANGELOG.md
```

### 2.2 plugin.json 定義

```json
{
  "name": "evolve",
  "description": "Self-evolving agent - 讓 AI 自主達成目標、從經驗中學習並持續改進",
  "version": "4.5.0",
  "author": {
    "name": "miles990",
    "email": "miles990@example.com"
  }
}
```

### 2.3 Hooks 配置

#### hooks/checkpoint-reminder.sh

```bash
#!/bin/bash
# Hook: PostToolUse
# Matcher: Edit|Write
# Description: CP1.5 + CP2 提醒

echo "🔍 CheckPoint 提醒："
echo "  • CP1.5: 確認已檢查現有實作、專案慣例"
echo "  • CP2: 記得執行編譯+測試驗證"
```

#### hooks/memory-sync-reminder.sh

```bash
#!/bin/bash
# Hook: PostToolUse
# Matcher: Write
# Condition: file path contains .claude/memory/
# Description: CP3.5 Memory 同步提醒

FILE="$CLAUDE_TOOL_ARG_FILE_PATH"

if [[ "$FILE" == *".claude/memory/"* ]]; then
  echo "📝 CP3.5: 已創建 Memory 文件，記得同步 index.md"
fi
```

### 2.4 命令定義

#### commands/evolve/COMMAND.md

```markdown
---
name: evolve
description: 自我進化 Agent - 給定目標，自主學習並迭代改進直到完成
arguments:
  - name: goal
    description: 目標描述
    required: true
  - name: flags
    description: 選項 (--explore, --emergence, --autonomous)
    required: false
---

# /evolve

執行 Self-Evolving Agent 流程。

## 流程

1. CP0: 北極星錨定
2. PSB: Plan → Setup → Build
3. 目標分析 + 深度訪談
4. 能力評估 → Skill 習得
5. PDCA Cycle（含方向校正）
6. Memory 記錄
7. CP6: 專案健檢

## 使用範例

\`\`\`
/evolve 建立一個 ComfyUI 工作流程
/evolve --explore 優化這段程式碼
/evolve --autonomous 為專案建立測試覆蓋率
\`\`\`
```

### 2.5 遷移計劃

```
Phase 1: 結構轉換（1-2 天）
─────────────────────────
1. 建立 evolve-plugin/ 目錄
2. 移動現有 skills/ 到 evolve-plugin/skills/
3. 建立 .claude-plugin/plugin.json
4. 建立 commands/evolve/COMMAND.md

Phase 2: Hooks 整合（1 天）
───────────────────────────
1. 建立 hooks/checkpoint-reminder.sh
2. 建立 hooks/memory-sync-reminder.sh
3. 測試 Hook 觸發

Phase 3: Agents 拆分（2-3 天）
─────────────────────────────
1. 拆分 goal-analyzer Agent
2. 拆分 pdca-executor Agent
3. 拆分 memory-manager Agent

Phase 4: 測試 + 發布（1 天）
──────────────────────────
1. 本地測試 /plugin install
2. 發布到 GitHub
3. 更新文檔
```

---

## 三、skillpkg 轉型策略

### 3.1 定位調整

```
Before: skillpkg = SKILL.md 的 npm
After:  skillpkg = Plugin 生態系統的「增強層」

                    ┌─────────────────────────┐
                    │    Claude Code 官方     │
                    │  /plugin install <name> │
                    │                         │
                    │  做：基礎安裝           │
                    │  不做：搜尋、推薦、同步  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │      skillpkg MCP       │
                    │                         │
                    │  做：搜尋、推薦、分析   │
                    │      批次安裝、跨平台同步│
                    │                         │
                    │  不做：重複安裝機制     │
                    └─────────────────────────┘
```

### 3.2 新增功能

| 功能 | 說明 | 優先級 |
|------|------|--------|
| `search_plugins` | 搜尋 GitHub 上的 Plugin | P0 |
| `analyze_plugin` | 分析 Plugin 品質、安全性 | P0 |
| `recommend_plugins` | 根據目標推薦 Plugin | P1 |
| `batch_install_plugins` | 批次安裝多個 Plugin | P1 |
| `plugin_status` | 顯示已安裝的 Plugin 狀態 | P2 |

### 3.3 MCP Tools 擴展

```typescript
// 新增工具
interface SkillpkgMCPTools {
  // 現有工具（保留）
  search_skills: (query: string) => Promise<Skill[]>;
  install_skill: (source: string) => Promise<void>;
  load_skill: (name: string) => Promise<string>;

  // 新增 Plugin 支援
  search_plugins: (query: string) => Promise<Plugin[]>;
  analyze_plugin: (source: string) => Promise<PluginAnalysis>;
  recommend_plugins: (goal: string) => Promise<PluginRecommendation[]>;

  // 智慧推薦（合併 Skill + Plugin）
  recommend_for_goal: (goal: string) => Promise<{
    plugins: PluginRecommendation[];
    skills: SkillRecommendation[];
    reasoning: string;
  }>;
}
```

### 3.4 搜尋來源擴展

```
目前：
  • GitHub SKILL.md 搜尋
  • miles990/claude-software-skills
  • anthropics/awesome-claude-skills

新增：
  • GitHub Plugin 搜尋（.claude-plugin/plugin.json）
  • anthropics/claude-code/plugins（官方 Plugin）
  • 社群 Plugin 倉庫
```

### 3.5 實作計劃

```
Phase 1: Plugin 搜尋（3-5 天）
──────────────────────────────
1. 實作 search_plugins tool
   - 搜尋 GitHub 上的 .claude-plugin/plugin.json
   - 解析 plugin.json 元資料
   - 排序結果（星數、更新時間）

2. 實作 analyze_plugin tool
   - 讀取 plugin 結構
   - 分析包含的 components（agents, commands, skills, hooks）
   - 品質評分

Phase 2: 智慧推薦（2-3 天）
───────────────────────────
1. 擴展 recommend_skills 邏輯
2. 同時推薦適合的 Plugin 和 Skill
3. 提供選擇理由

Phase 3: 安裝整合（1-2 天）
───────────────────────────
1. Plugin 安裝引導（調用 /plugin install）
2. 批次安裝支援
3. 安裝後驗證
```

---

## 四、整合藍圖

### 4.1 完整生態系統

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                        User Journey                                 │
│                                                                     │
│   「我想讓 AI 能自主學習並完成複雜任務」                             │
│                                                                     │
│   Step 1: skillpkg 推薦                                             │
│   ─────────────────────                                             │
│   User: "幫我找能自我進化的 AI 工具"                                │
│   skillpkg MCP: → recommend_for_goal("self-evolving AI")           │
│              → 推薦 evolve Plugin + 相關 skills                     │
│                                                                     │
│   Step 2: 安裝 Plugin                                               │
│   ────────────────────                                              │
│   User: /plugin install miles990/evolve-plugin                      │
│   Claude Code: → 安裝 evolve Plugin                                 │
│              → 載入 skills, hooks, commands, agents                 │
│                                                                     │
│   Step 3: 使用                                                      │
│   ─────────                                                         │
│   User: /evolve 建立一個量化交易系統                                │
│   evolve Plugin: → 啟動 Self-Evolving Loop                         │
│                → Hooks 自動提醒 CheckPoints                         │
│                → Agents 協助分析和執行                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 分工明確

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│   Claude Code 官方          skillpkg             evolve       │
│   ════════════════          ════════             ══════       │
│                                                               │
│   /plugin 命令              MCP Server           Plugin       │
│   ├─ install               ├─ search             ├─ skills   │
│   ├─ list                  ├─ recommend          ├─ hooks    │
│   ├─ enable                ├─ analyze            ├─ agents   │
│   └─ disable               └─ batch ops          └─ commands │
│                                                               │
│   基礎設施層                 生態系統工具層         領域能力層  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 4.3 Timeline

```
                     Week 1          Week 2          Week 3
                    ─────────       ─────────       ─────────
evolve Plugin:      [結構轉換]─────[Hooks+Agents]──[測試發布]

skillpkg:                          [Plugin搜尋]────[智慧推薦]──[整合測試]

Integration:                                                   [E2E 測試]
```

---

## 五、風險與緩解

| 風險 | 影響 | 緩解措施 |
|------|------|----------|
| Plugin 格式可能變動 | 需要重新調整 | 保持結構簡單，緊密追蹤官方更新 |
| Hooks 噪音過多 | 使用者疲勞 | 從 Level 1 開始，漸進增加 |
| skillpkg 與官方功能重複 | 定位混淆 | 明確分工：官方做安裝，skillpkg 做發現+推薦 |
| 遷移過程中斷服務 | 使用者受影響 | 保留舊版 skill 直到 Plugin 穩定 |

---

## 六、下一步行動

### 立即行動（本週）

1. **建立 evolve-plugin 目錄結構**
   - 建立 .claude-plugin/plugin.json
   - 移動 skills/ 到新結構

2. **實作基礎 Hooks**
   - checkpoint-reminder.sh
   - memory-sync-reminder.sh

3. **本地測試**
   - 確認 /plugin install 可用

### 短期（2 週內）

4. **完成 evolve Plugin 全部功能**
5. **skillpkg 新增 search_plugins**
6. **發布 evolve Plugin 到 GitHub**

### 中期（1 個月內）

7. **skillpkg 完整 Plugin 支援**
8. **整合測試**
9. **文檔更新**

---

## 附錄

### A. 參考資源

- [Claude Code Plugins 官方文檔](https://code.claude.com/docs/en/plugins)
- [anthropics/claude-code/plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
- [Agent Skills 開放標準](https://agentskills.io)

### B. 相關專案

- [self-evolving-agent](https://github.com/miles990/self-evolving-agent)
- [skillpkg](https://github.com/miles990/skillpkg)
