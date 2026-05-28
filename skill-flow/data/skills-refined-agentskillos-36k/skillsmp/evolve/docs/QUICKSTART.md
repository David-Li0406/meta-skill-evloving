# Quick Start Guide

> 5 分鐘上手 Self-Evolving Agent v4.0.0

## 安裝

### 方法一：一鍵安裝（推薦）

```bash
# 基本安裝
curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash

# 完整安裝（含 hooks 和 memory 初始化）
curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash -s -- --with-hooks --with-memory

# 安裝到指定專案
curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash -s -- --target /path/to/project
```

### 方法二：Plugin（推薦）

```bash
# 添加 marketplace
/plugin marketplace add miles990/self-evolving-agent

# 安裝
/plugin install evolve@self-evolving-agent
```

### 方法三：手動安裝

```bash
git clone https://github.com/miles990/self-evolving-agent.git
cp -r self-evolving-agent/skills /path/to/your/project/.claude/skills/evolve
```

## 基本使用

```
/evolve [你的目標]
```

### 範例

```bash
# 效能優化
/evolve 優化 UserList 組件，目標首次渲染 < 100ms

# 學習新技術
/evolve 用 ComfyUI 建立遊戲素材生成工作流程

# 重構程式碼
/evolve 將這個模組重構為 TypeScript，加入完整型別定義
```

### Flags

```bash
--explore          # 探索模式 - 允許自主選擇方向
--emergence        # 涌現模式 - 啟用跨領域連結探索
--autonomous       # 自主模式 - 完全自主
--max-iterations N # 最大迭代次數（預設 10）
--from-spec NAME   # 從 spec-workflow 執行
```

## v4.0.0 原子化架構

新版本將 SKILL.md 拆分為獨立模組：

```
skills/
├── SKILL.md                    # 主入口（192行）
├── 00-getting-started/         # 入門
│   ├── _base/                  # 官方內容
│   └── community/              # 社群貢獻
├── 01-core/                    # 核心流程
├── 02-checkpoints/             # 強制檢查點
├── 03-memory/                  # 記憶系統
├── 04-emergence/               # 涌現機制
├── 05-integration/             # 外部整合
└── 99-evolution/               # 自我進化
```

## 自動領域識別

Agent 會自動識別任務關鍵詞並載入相關領域知識：

| 說 | 載入 |
|----|------|
| 「分析財報」 | finance/investment-analysis |
| 「規劃 Sprint」 | business/project-management |
| 「設計 UI」 | creative/ui-ux-design |
| 「寫小說大綱」 | creative/storytelling |

## 核心流程

```
PSB Setup → 目標分析 → 自動領域識別 → 能力評估 → 技能習得 → PDCA 執行 → 記憶儲存
```

## 記憶系統

經驗會自動儲存到 `.claude/memory/`：

```
.claude/memory/
├── index.md      # 快速索引（必須維護）
├── learnings/    # 成功經驗
├── failures/     # 失敗教訓
├── decisions/    # 決策記錄 (ADR)
├── patterns/     # 推理模式
├── strategies/   # 策略記錄
└── discoveries/  # 涌現發現
```

## 強制檢查點

以下檢查點**不可跳過**：

| 檢查點 | 時機 | 動作 |
|--------|------|------|
| CP1 | 任務開始前 | 搜尋 Memory |
| CP2 | 程式碼變更後 | 編譯 + 測試 |
| CP3 | Milestone 完成後 | 目標確認 |
| CP3.5 | Memory 創建後 | 同步 index.md |

## 進階技巧

### 明確的目標描述

```bash
# ❌ 模糊
/evolve 優化效能

# ✅ 明確
/evolve 優化 UserList 組件
       目標：首次渲染 < 100ms
       約束：不改變 API 介面
       驗證：使用 React DevTools Profiler
```

### 使用涌現模式

```bash
# 啟用跨領域探索
/evolve 改進這個專案 --emergence --max-iterations 10
```

## 相關文檔

- [完整使用手冊](../USAGE.md)
- [原子化模組](../skills/SKILL.md)
- [基本範例](../examples/basic-usage.md)
- [失敗處理範例](../examples/failure-handling.md)
- [Memory 管理範例](../examples/memory-management.md)
- [變更日誌](../CHANGELOG.md)
