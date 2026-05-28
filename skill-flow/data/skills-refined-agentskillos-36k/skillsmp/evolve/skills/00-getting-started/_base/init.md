# 初始化指南

> 首次使用 Self-Evolving Agent 的設定步驟

## 最小需求

| 必要 | 項目 | 說明 |
|------|------|------|
| ✅ | Git Repo | 版本控制 |
| ✅ | `.claude/memory/` | 記憶儲存 |
| 建議 | `CLAUDE.md` | 專案約束 |
| 可選 | MCP 配置 | 擴展能力（context7, PAL） |

## 記憶系統初始化

首次使用時，建立以下目錄結構：

```bash
# 檢查是否已存在
ls .claude/memory/ 2>/dev/null || echo "需要初始化"
```

若不存在，建立：

```
.claude/memory/
├── index.md              # 快速索引（必須維護）
├── learnings/            # 學習記錄
│   └── .gitkeep
├── decisions/            # 決策記錄 (ADR)
│   └── .gitkeep
├── failures/             # 失敗經驗
│   └── .gitkeep
├── patterns/             # 推理模式
│   └── .gitkeep
├── strategies/           # 策略記錄
│   └── .gitkeep
├── discoveries/          # 涌現發現
│   └── .gitkeep
└── skill-metrics/        # 技能效果追蹤
    └── .gitkeep
```

## index.md 模板

```markdown
# 專案記憶索引

> Last curated: YYYY-MM-DD
> Total entries: 0
> Next review: YYYY-MM-DD (7 days)

## 統計
- Learnings: 0 筆
- Failures: 0 筆
- Decisions: 0 筆
- Patterns: 0 筆

## 最近學習
<!-- LEARNINGS_START -->
<!-- LEARNINGS_END -->

## 重要決策
<!-- DECISIONS_START -->
<!-- DECISIONS_END -->

## 失敗經驗
<!-- FAILURES_START -->
<!-- FAILURES_END -->

## 推理模式
<!-- PATTERNS_START -->
<!-- PATTERNS_END -->

## 標籤索引
<!-- TAGS_START -->
<!-- TAGS_END -->
```

## 快速檢查指令

```bash
# 一鍵檢查環境
git status && \
ls CLAUDE.md 2>/dev/null || echo "⚠️ 建議建立 CLAUDE.md" && \
ls .claude/memory/ 2>/dev/null || echo "⚠️ 需要初始化記憶系統"
```

## 下一步

環境就緒後，使用 `/evolve [目標]` 開始執行任務。
