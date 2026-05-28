---
date: 2026-01-23
tags: [claude-code, plugin, hooks, eval-harness, continuous-learning, agents, competitor]
source: https://github.com/affaan-m/everything-claude-code
author: affaan-m (Anthropic Hackathon Winner)
status: resolved
---

# Everything Claude Code 專案分析

## 概述

Anthropic x Forum Ventures 駭客松冠軍整理的 Claude Code 配置集合，經過 10+ 個月實戰打磨。用於建構 zenith.chat 全程使用 Claude Code。

## 專案結構

```
everything-claude-code/
├── agents/           # 專門化子代理
├── skills/           # 工作流定義
├── commands/         # Slash 命令
├── rules/            # 強制遵守規則
├── hooks/            # 觸發式自動化
├── scripts/          # 跨平台 Node.js 工具
├── contexts/         # 動態 System Prompt 注入
├── mcp-configs/      # MCP Server 配置
└── .claude-plugin/   # Plugin 清單
```

## 核心亮點

### 1. Hooks 系統設計

```json
{
  "PreToolUse": [
    "攔截危險操作 (dev server outside tmux)",
    "建議使用 tmux",
    "阻擋隨意創建 .md 文件",
    "Strategic Compact 建議"
  ],
  "PostToolUse": [
    "自動 Prettier 格式化",
    "TypeScript 型別檢查",
    "console.log 警告",
    "PR 創建後提示"
  ],
  "SessionStart": ["載入前次 Context"],
  "SessionEnd": ["持久化 Session 狀態", "提取可重用 Pattern"],
  "PreCompact": ["Compact 前保存狀態"],
  "Stop": ["檢查 console.log"]
}
```

**啟發**：完整的生命週期 Hook 覆蓋，特別是 PreCompact 和 SessionEnd 的狀態保存機制。

### 2. Eval Harness 框架

評估驅動開發 (EDD) - 把 Eval 當作 AI 開發的單元測試：

| 指標 | 說明 | 用途 |
|------|------|------|
| pass@k | k 次嘗試內至少成功一次 | 一般功能測試 |
| pass^k | 連續 k 次都成功 | 關鍵路徑驗證 |

三種 Grader：
- **Code-Based**: 確定性檢查 (grep, npm test)
- **Model-Based**: Claude 評估開放式輸出
- **Human**: 標記需要人工審查

**整合建議**：可強化我們的 CP2 驗證階段，加入 pass@k 指標追蹤。

### 3. Agent 分工

| Agent | 用途 | 觸發時機 |
|-------|------|----------|
| planner | 實作規劃 | 複雜功能/重構 |
| architect | 系統設計 | 架構決策 |
| tdd-guide | TDD 流程 | 新功能/修 Bug |
| code-reviewer | 品質審查 | 寫完程式碼後 |
| security-reviewer | 安全分析 | Commit 前 |
| build-error-resolver | 修復建置錯誤 | Build 失敗時 |

**特色**：強調 PROACTIVELY 使用，不需用戶提示。

### 4. Continuous Learning

Session 結束時自動提取 Pattern：

```javascript
patterns_to_detect: [
  "error_resolution",      // 錯誤解決方式
  "user_corrections",      // 用戶糾正
  "workarounds",           // 框架/庫的變通方案
  "debugging_techniques",  // 除錯技巧
  "project_specific"       // 專案慣例
]
```

儲存為 `~/.claude/skills/learned/[pattern-name].md`

### 5. Context 管理最佳實踐

- 保持 < 10 個 MCP 啟用
- 避免使用 context window 最後 20%
- 模型選擇：Haiku (輕量 90% Sonnet 能力) / Sonnet (主力) / Opus (深度推理)

### 6. Verification Loop

六階段驗證流程：
1. Build Verification
2. Type Check
3. Lint Check
4. Test Suite (80% coverage)
5. Security Scan (secrets, console.log)
6. Diff Review

## 與 Self-Evolving Agent 比較

| 面向 | everything-claude-code | Self-Evolving Agent |
|------|------------------------|---------------------|
| 定位 | Plugin/配置庫 | 自主進化框架 |
| 核心理念 | 工具集成 + 自動化 | 目標驅動 + 持續學習 |
| 記憶系統 | Hooks 持久化 | Git-based Memory |
| 學習機制 | Continuous Learning | PDCA + Reflexion |
| 驗證系統 | Verification Loop + Eval | 強制 Checkpoints |

### 互補性分析

**他們有，我們可借鑑**：
- 跨平台 Node.js Hooks
- Eval Harness (pass@k 指標)
- Package Manager 自動偵測
- Strategic Compact 建議
- Context 動態注入

**我們有，他們沒有**：
- 北極星錨定系統
- PDCA 迭代框架
- Worktree 隔離模式
- 多策略重試機制
- 涌現機制檢查
- 架構等級判斷

## 整合優先度

| 優先度 | 功能 | 整合方式 |
|--------|------|----------|
| 高 | Eval Harness pass@k | 強化 CP2 驗證 |
| 高 | Continuous Learning Pattern | 補充 CP4 涌現檢查 |
| 中 | Hooks 生命週期 | 參考設計模式 |
| 中 | Verification Loop | 整合到 PDCA Check |
| 低 | Package Manager 偵測 | 視需求 |

## 關鍵引用

> "Eval-Driven Development treats evals as the unit tests of AI development"

> "Context Window: Don't enable all MCPs at once. Your 200k context window can shrink to 70k with too many tools enabled."

> "Rule of thumb: Have 20-30 MCPs configured, Keep under 10 enabled per project, Under 80 tools active"

## 資源連結

- Shorthand Guide: https://x.com/affaanmustafa/status/2012378465664745795
- Longform Guide: https://x.com/affaanmustafa/status/2014040193557471352
- zenith.chat: https://zenith.chat

---

# Twitter 指南深度分析

## Shorthand Guide 重點

### Session 狀態管理

Session 文件格式：`~/.claude/sessions/YYYY-MM-DD-topic.tmp`

```markdown
# Session: [topic]
## Current State
[What you're working on]
## Completed
[Done items]
## Blockers
[Issues]
## Key Decisions
[Choices made]
## Context for Next Session
[Handoff notes]
```

### 指令權威層級

```
System prompt (最高) > User messages > Tool results (最低)
```

### CLI Context Switching

```bash
# 每日開發
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
# PR 審查模式
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'
# 研究/探索模式
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'
```

### 動態 System Prompt 注入

```bash
claude --system-prompt "$(cat memory.md)"
```

---

## Longform Guide 核心洞察

### 1. Strategic Compact（策略性壓縮）

**時機選擇**：
- 探索完成後 / 執行開始前
- Milestone 完成後 / 下一階段前
- 偵錯循環後 / 實施修復前
- 主要決策後

### 2. Memory Persistence Hooks

```json
{
  "hooks": {
    "PreCompact": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "~/.claude/hooks/memory-persistence/pre-compact.sh"}]
    }],
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "~/.claude/hooks/memory-persistence/session-start.sh"}]
    }],
    "Stop": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "~/.claude/hooks/memory-persistence/session-end.sh"}]
    }]
  }
}
```

### 3. Token 優化策略

| 任務 | 模型 | 原因 |
|------|------|------|
| 探索/搜尋 | Haiku | 快速、便宜、找檔案夠用 |
| 簡單編輯 | Haiku | 單檔案變更、指令清晰 |
| 多檔案實作 | Sonnet | 編碼最佳平衡 |
| 複雜架構 | Opus | 需要深度推理 |
| PR 審查 | Sonnet | 理解上下文、捕捉細微差異 |
| 安全分析 | Opus | 不能漏掉漏洞 |
| 寫文檔 | Haiku | 結構簡單 |
| 除錯複雜 Bug | Opus | 需要掌握整個系統 |

### 4. mgrep vs grep 性能比較

- 成本減少 50%
- 速度提升 2x
- 76% 勝率

### 5. Eval Pattern Types

**Checkpoint-Based**（適合線性工作流）：
- 設置明確檢查點
- 驗證失敗必須修復才能繼續
- 適合有清晰里程碑的功能實作

**Continuous**（適合長時間 Session）：
- 每 N 分鐘或重大變更後執行
- 完整測試套件 + lint
- 適合探索性重構或維護

### 6. pass@k 實際數據

| 指標 | k=1 | k=3 | k=5 |
|------|-----|-----|-----|
| pass@k (至少一次成功) | 70% | 91% | 97% |
| pass^k (全部成功) | 70% | 34% | 17% |

**選擇指南**：
- pass@k：只需要能工作就好
- pass^k：需要一致性和確定性輸出

### 7. 8 步 Eval Roadmap

1. 早期開始 - 從真實失敗中取 20-50 個簡單任務
2. 將用戶報告的失敗轉為測試案例
3. 寫明確任務 - 兩個專家應得出相同結論
4. 建立平衡問題集 - 測試應該和不應該發生的行為
5. 建立穩健框架 - 每次試驗從乾淨環境開始
6. 評估 agent 產出，而非過程
7. 閱讀多次試驗的記錄
8. 監控飽和度 - 100% 通過率意味著需要更多測試

### 8. 並行化最佳實踐

**Cascade Method**：
- 在右邊新標籤開啟新任務
- 從左到右掃描，最舊到最新
- 保持一致的方向流
- 專注最多 3-4 個任務

**Git Worktrees 並行**：
```bash
# 創建並行工作樹
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
git worktree add ../project-refactor refactor-branch

# 每個工作樹獲得自己的 Claude 實例
cd ../project-feature-a && claude
```

**好處**：
- 實例間無 git 衝突
- 每個都有乾淨工作目錄
- 易於比較輸出
- 可對相同任務進行不同方法的基準測試

### 9. Two-Instance Kickoff Pattern

**Instance 1: Scaffolding Agent**
- 建立專案結構
- 設置配置（CLAUDE.md, rules, agents）
- 建立慣例
- 搭好骨架

**Instance 2: Deep Research Agent**
- 連接所有服務、網路搜尋
- 創建詳細 PRD
- 創建架構 Mermaid 圖
- 編譯實際文檔參考

### 10. llms.txt Pattern

許多文檔網站提供 LLM 優化版本：
```
https://www.helius.dev/docs/llms.txt
```
可直接餵給 Claude 的乾淨文檔格式。

### 11. Orchestrator Sequential Phases

```markdown
Phase 1: RESEARCH (use Explore agent)
- Gather context
- Identify patterns
- Output: research-summary.md

Phase 2: PLAN (use planner agent)
- Read research-summary.md
- Create implementation plan
- Output: plan.md

Phase 3: IMPLEMENT (use tdd-guide agent)
- Read plan.md
- Write tests first
- Implement code
- Output: code changes

Phase 4: REVIEW (use code-reviewer agent)
- Review all changes
- Output: review-comments.md

Phase 5: VERIFY (use build-error-resolver if needed)
- Run tests
- Fix issues
- Output: done or loop back
```

**關鍵規則**：
1. 每個 agent 接收一個清晰輸入，產出一個清晰輸出
2. 輸出成為下一階段的輸入
3. 永不跳過階段
4. 用 `/clear` 在 agent 間保持上下文清新
5. 將中間輸出存入文件（不只是記憶）

### 12. Agent Abstraction Tierlist

**Tier 1: Direct Buffs (易用)**
- Subagents - 防止上下文腐爛
- Metaprompting - 3 分鐘 prompt → 20 分鐘任務
- 開始時多問用戶

**Tier 2: High Skill Floor (難精通)**
- Long-running agents - 需理解 15 min vs 1.5 hr vs 4 hr 任務權衡
- Parallel multi-agent - 只適合高度複雜或良好分割的任務
- Role-based multi-agent - 模型演進太快
- Computer use agents - 非常早期

**要點**：從 Tier 1 開始，有真正需求才升級到 Tier 2。

### 13. Sub-Agent Context Problem

問題：Sub-agent 只知道字面查詢，不知道背後的 PURPOSE/REASONING。

**Iterative Retrieval Pattern**：
1. Orchestrator dispatch 帶 query + objective
2. Sub-agent 返回 summary
3. 評估是否足夠？
4. 不足夠 → 追問 → sub-agent 取答案
5. 最多 3 個循環

### 14. MCP 優化技巧

用 CLI 命令取代 MCP 節省 Context Window：
```bash
# 不要一直載入 GitHub MCP
# 改用 /gh-pr 命令包裝 gh pr create
```

With **lazy loading**，context window 問題大部分解決。但 token 成本仍可用 CLI + skills 方法優化。

---

## 參考資源

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Jan 2026)
- Anthropic: "Claude Code Best Practices" (Apr 2025)
- Fireworks AI: "Eval Driven Development with Claude Code" (Aug 2025)
- [YK: 32 Claude Code Tips](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to) (Dec 2025)
- Addy Osmani: "My LLM coding workflow going into 2026"
- @PerceptualPeak: Sub-Agent Context Negotiation
- @menhguin: Agent Abstractions Tierlist
- @omarsar0: Compound Effects Philosophy
- [RLanceMartin: Session Reflection Pattern](https://rlancemartin.github.io/2025/12/01/claude_diary/)
- @alexhillman: Self-Improving Memory System

---

## 驗證

- [x] 完整分析 agents/, skills/, hooks/, rules/
- [x] 識別可借鑑的設計模式
- [x] 與 Self-Evolving Agent 比較
- [x] 提出整合優先度建議
- [x] 研究 Shorthand Guide (Twitter)
- [x] 研究 Longform Guide (Twitter)
- [x] 整合兩篇指南核心洞察
