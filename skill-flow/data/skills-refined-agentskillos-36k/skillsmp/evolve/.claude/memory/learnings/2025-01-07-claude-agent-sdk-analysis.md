---
date: "2025-01-07"
tags: [claude-agent-sdk, architecture, comparison, self-evolving-agent, production]
task: 分析 Claude Agent SDK 與 self-evolving-agent 的關係
status: resolved
source: https://x.com/boringmarketer/status/2008201943764889623
---

# Claude Agent SDK 架構分析

## 情境
@boringmarketer 在 X 上分享 Claude Agent SDK 的架構圖，引發社群討論。

## Agent SDK 架構

```
GOAL: "handle this lead"
        ↓
AGENT LOOP: observe → think → act → learn → repeat
        ↓
┌─────────────┬─────────────┬─────────────┐
│ SUBAGENTS   │ SKILLS      │ TOOLS       │
│ code-review │ lead-research│ Built-in    │
│ test-runner │ email-draft │ MCP         │
│ researcher  │ (auto-invoke)│ Custom      │
│ (parallel)  │ (domain     │ (your       │
│             │  expertise) │  functions) │
└─────────────┴─────────────┴─────────────┘
        ↓
HOOKS: guard rails, logging, human-in-the-loop
        ↓
STRUCTURED OUTPUT: validated JSON matching schema
```

## 社群討論重點

### Claude Code vs Agent SDK 的使用時機

| 場景 | 選擇 |
|------|------|
| 互動式開發、即時回饋 | Claude Code |
| 背景執行、無人值守 | Agent SDK |
| 原型驗證、探索 | Claude Code |
| 嵌入產品、API 呼叫 | Agent SDK |

### Matt Stockton 的工作流程
> "prototype your agent with the same building blocks directly in Claude Code - and then when it's working, there's a fairly easy path to using the SDK to run it in 'production'"

**建議路徑：**
1. 在 Claude Code 中原型驗證
2. 確認可行後遷移到 Agent SDK
3. 部署為生產環境服務

## self-evolving-agent 對應關係

| Agent SDK 概念 | self-evolving-agent 實現 |
|----------------|-------------------------|
| Agent Loop | PDCA 循環（Plan-Do-Check-Act） |
| Subagents | Boris Tip #8 策略（verify-app, code-simplifier, build-validator） |
| Skills | skillpkg 技能系統（自動習得、載入） |
| Tools | MCP + Claude Code 內建工具 |
| Hooks | PostToolUse（自動格式化）、Stop（驗證） |
| Structured Output | 標準化完成格式 ✅/⏸️/❌ |

## 洞察

### 我們已經實現的
- ✅ Agent Loop（PDCA）
- ✅ Subagent 策略
- ✅ Skill 自動習得
- ✅ Hooks 整合
- ✅ 結構化輸出

### 可以加強的
- 🔄 更明確的「導出到 Agent SDK」路徑
- 🔄 背景執行模式（ralph-wiggum 已部分實現）
- 🔄 更豐富的 Subagent 策略池

## 建議發展方向

| 時程 | 方向 |
|------|------|
| **短期** | 繼續強化 `/evolve` 作為「原型驗證」工具 |
| **中期** | 加入「導出到 Agent SDK」功能或指南 |
| **長期** | 建立 Claude Code → Agent SDK 的標準遷移路徑 |

## 驗證
✅ 分析完成
✅ 與現有架構對比完成
✅ 提出改進方向

## 相關檔案
- `SKILL.md` - self-evolving-agent 技能定義
- `.claude/memory/strategies/subagents.md` - Subagent 策略
- `.claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md` - Boris 技巧
