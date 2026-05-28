# 05-integration

> 外部工具整合：Plugin、PAL、spec-workflow、Memory MCP、Hooks

## 本模組包含

| 文件 | 整合對象 | 用途 |
|------|----------|------|
| [skill-integration.md](./_base/skill-integration.md) | Claude Code Plugin | Skill 搜尋、安裝、載入 |
| [pal-tools.md](./_base/pal-tools.md) | PAL MCP | 多模型協作、深度分析 |
| [spec-workflow.md](./_base/spec-workflow.md) | spec-workflow MCP | 需求到實作轉換 |
| [memory-mcp.md](./_base/memory-mcp.md) | Memory MCP | 智能記憶、Skill 追蹤、失敗索引 |
| [hooks.md](./_base/hooks.md) | Claude Code Hooks | 自動化觸發 |
| [github-to-skill.md](./_base/github-to-skill.md) | GitHub 開源項目 | 封裝 GitHub → Skill 策略 |
| [skill-ecosystem.md](./_base/skill-ecosystem.md) | Skill 生態系 | Skill 發現、推薦、組合 |
| [knowledge-acquisition.md](./_base/knowledge-acquisition.md) | 4C 方法論 | 系統性學習整合 |

## 整合概覽

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Plugin    │     │    PAL      │     │ spec-flow   │
│  Skill 管理 │     │  多模型協作  │     │  結構化規劃  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   evolve    │
                    │  自我進化    │
                    └──────┬──────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
│ Memory MCP  │     │   Hooks     │     │ Git Memory  │
│ SQLite 索引 │     │  自動觸發    │     │  詳細記錄   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Memory MCP 整合（v5.4+）

Memory MCP 提供統一的 SQLite 記憶系統，整合於 evolve 流程的關鍵檢查點：

| 檢查點 | Memory MCP 工具 | 用途 |
|--------|----------------|------|
| CP0 | `skill_usage_start` | 開始追蹤 Skill 使用 |
| CP1 | `memory_search` + `failure_search` | 搜尋經驗和失敗解法 |
| CP3.5 | `memory_write` | 記錄學習到 SQLite 索引 |
| CP5 | `failure_record` | 記錄失敗供跨專案搜尋 |
| 結束 | `skill_usage_end` | 結束追蹤，計算成功率 |

詳見 [memory-mcp.md](./_base/memory-mcp.md)

## 社群貢獻

