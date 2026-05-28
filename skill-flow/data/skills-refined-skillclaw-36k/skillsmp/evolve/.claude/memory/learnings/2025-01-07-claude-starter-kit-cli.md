---
date: 2025-01-07
tags: [cli, scaffold, npx, commander, inquirer, multi-select, domain-skills]
task: 建立 claude-starter-kit 獨立 CLI 工具
status: resolved
---

# Claude Starter Kit CLI 開發經驗

## 情境
需要建立一個簡單的一鍵安裝工具，讓用戶快速設置 Claude Code 專案配置。

## 需求分析

### 用戶期望
- `npx claude-starter-kit` 一鍵安裝
- 簡單的 CLI 控制腳手架配置
- 支援多種專業領域（不只技術領域）

### 領域分類
| 類別 | 領域 |
|------|------|
| 技術 | frontend, backend, devops, ai-ml |
| 商業 | quant-trading, finance, marketing, product |
| 創意 | game-design, ui-ux, content, brand |

## 架構決策

### 選擇方案 C：混合模式
- **核心內建**：CLAUDE.md, 基本 rules, memory 系統模板
- **擴展下載**：透過 skillpkg 安裝專業技能包

### 優點
1. 離線可用（核心功能）
2. 按需下載（節省空間）
3. 擴展性強（新領域只需新增 skill）

## 技術實作

### 目錄結構
```
cli/
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts          # 入口點
    ├── commands/
    │   └── init.ts       # 主要初始化命令
    ├── templates/
    │   └── index.ts      # 內建模板
    └── domains/
        └── index.ts      # 領域配置
```

### 關鍵依賴
```json
{
  "commander": "^12.0.0",
  "inquirer": "^9.0.0",
  "chalk": "^5.3.0",
  "ora": "^8.0.0"
}
```

### 預設模式
| 模式 | 包含內容 |
|------|----------|
| minimal | CLAUDE.md + 基本 rules |
| standard | + MCP 配置 + Memory 系統 + self-evolving-agent |
| full | + 所有 rules + software-skills |

## 遇到的問題

### TypeScript 類型錯誤
**問題**：`PRESETS.skills.includes()` 報錯 `never` 類型
**原因**：TypeScript 無法推斷 object literal 的類型
**解決**：加入明確的類型註解
```typescript
const PRESETS: Record<string, {
  name: string;
  components: string[];
  skills: string[];
  domains: string[];
}> = { ... };
```

## 使用方式

```bash
# 快速安裝（推薦配置）
npx claude-starter-kit -y

# 互動式安裝
npx claude-starter-kit

# 指定預設
npx claude-starter-kit --preset full

# 跳過技能安裝
npx claude-starter-kit --no-install
```

## 相關檔案
- `https://github.com/miles990/claude-starter-kit`
- `/Users/user/Workspace/claude-starter-kit/cli/`

## 下一步
- 建立 claude-business-skills 專案
- 建立 claude-creative-skills 專案
- 發布到 npm
