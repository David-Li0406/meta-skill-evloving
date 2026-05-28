# 記憶系統結構

> Git-based Memory：版本控制、可追溯、可協作

## 目錄結構

```
.claude/memory/
├── index.md              # 快速索引（必須維護）
├── north-star/           # 🌟 北極星文件（v4.4 新增）
│   └── {project-name}.md
├── learnings/            # 學習記錄
│   └── {date}-{slug}.md
├── decisions/            # 決策記錄 (ADR)
│   └── {number}-{title}.md
├── failures/             # 失敗經驗
│   └── {date}-{slug}.md
├── patterns/             # 推理模式
│   └── {category}-{name}.md
├── strategies/           # 策略記錄
│   └── {task-type}.md
├── discoveries/          # 涌現發現
│   └── {date}-{name}.md
├── lessons/              # CP5 結構化教訓（失敗後驗屍）
│   └── {date}-{failure-id}.md
└── skill-metrics/        # 技能效果追蹤
    ├── index.md
    ├── by-task-type/
    └── by-skill/
```

## 各層用途

| 層 | 用途 | 檔名格式 |
|---|------|----------|
| **north-star** | 🌟 專案北極星、方向錨定（v4.4 新增） | `{project-name}.md` |
| **learnings** | 解決方案、最佳實踐、成功經驗 | `{date}-{slug}.md` |
| **decisions** | 架構決策記錄 (ADR)、技術選型 | `{number}-{title}.md` |
| **failures** | 失敗經驗、踩坑記錄、教訓 | `{date}-{slug}.md` |
| **patterns** | 可複用的推理模式、思考框架 | `{category}-{name}.md` |
| **strategies** | 任務類型的策略池、成功率統計 | `{task-type}.md` |
| **discoveries** | 涌現發現、跨領域連結、意外洞察 | `{date}-{name}.md` |
| **lessons** | CP5 結構化教訓、失敗後驗屍 | `{date}-{failure-id}.md` |
| **skill-metrics** | 技能效果追蹤、排行榜 | 依結構 |

## 北極星文件（v4.4 新增）

專案級的方向錨定文件，防止「做到後面迷失方向」：

```yaml
---
created: {date}
project: "{專案名稱}"
status: active | paused | completed | abandoned
last_checkpoint: {date}
iteration_count: 0
---

# 🌟 北極星：{專案名稱}

## 一句話願景
> [20字內：這個專案存在的理由]

## 完成標準（Done = 什麼？）
- [ ] [可驗證的標準 1]
- [ ] [可驗證的標準 2]

## 不做清單（Scope 護欄）
- ❌ [明確排除 1]
- ❌ [明確排除 2]

## 當初為什麼開始？
[1-2句話，迷失時回來看這段]
```

**相關檢查點**：
- CP0：北極星錨定（建立/讀取）
- CP3：方向校正（對照北極星）
- CP6：專案健檢（定期對照）

## Git-based 優勢

- ✅ **版本控制** - 追蹤歷史、可回滾
- ✅ **跨工具共享** - Claude Code ↔ Copilot ↔ Cursor
- ✅ **離線可用** - 無需外部服務
- ✅ **團隊協作** - PR 審核記憶變更
- ✅ **快速搜尋** - 標準 Grep 工具
- ✅ **專案可攜** - 記憶隨 repo 遷移

## 搜尋範例

```python
# 搜尋學習記錄
Grep(pattern="ComfyUI", path=".claude/memory/learnings/")

# 搜尋失敗經驗
Grep(pattern="memory leak", path=".claude/memory/failures/")

# 全域搜尋
Grep(pattern="關鍵字", path=".claude/memory/")
```
