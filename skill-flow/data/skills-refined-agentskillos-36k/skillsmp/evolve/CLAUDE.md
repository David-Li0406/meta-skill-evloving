# Self-Evolving Agent - Project Context

> 專案約束文件，供 AI 助手理解專案規範

## 專案概述

這是一個 **Claude Code Skill**，讓 AI 能夠自主達成目標、從經驗中學習並持續改進。

## 技術棧

- **語言**: Markdown (Skill 定義)、Bash (腳本)
- **架構**: 原子化模組設計
- **記憶系統**: Git-based (.claude/memory/)
- **整合**: PAL MCP、spec-workflow MCP、Claude Code Plugin

## 目錄結構

```
skills/
├── SKILL.md                 # 主入口（全域 skill 文件）
├── 00-getting-started/      # 入門模組
├── 01-core/                 # 核心流程
├── 02-checkpoints/          # 強制檢查點
├── 03-memory/               # 記憶系統
├── 04-emergence/            # 涌現機制
├── 05-integration/          # 外部整合
└── 99-evolution/            # 自我進化
```

## 設計原則

1. **有主見的設計**: 合理預設值 > 讓 AI 選擇
2. **深且窄**: 專注高價值任務，不追求廣度
3. **預期失敗**: 設計優雅降級機制
4. **增強回饋**: 清晰的進度和錯誤報告

## 重要約定

### Checkpoint 規則（不可跳過）

| 檢查點 | 時機 | 動作 |
|--------|------|------|
| CP1 | 任務開始前 | 搜尋 .claude/memory/ |
| CP2 | 程式碼變更後 | 編譯 + 測試驗證 |
| CP3 | Milestone 後 | 確認目標和方向 |
| CP3.5 | Memory 創建後 | 同步 index.md |
| CP4 | 迭代完成後 | 涌現機會檢查 |

### Memory 操作

- 創建 memory 文件後**立即**更新 index.md
- 使用標準格式（見 03-memory/_base/operations.md）
- 定期清理過時記錄

### 版本規範

- 版本號: v{major}.{minor}.{patch}
- 變更記錄: CHANGELOG.md
- 重大變更需更新 skills/SKILL.md 版本

## 禁止事項

- ❌ 跳過強制檢查點
- ❌ 創建 memory 後不更新 index.md
- ❌ 修改 _base/ 目錄下的官方文件（除非是版本更新）
- ❌ 在腳本中使用硬編碼絕對路徑

## 開發指南

### 添加新模組

1. 在 `skills/` 下創建新目錄
2. 添加 `_base/` 子目錄
3. 創建 `README.md` 說明文件
4. 更新 `skills/SKILL.md` 目錄結構

### 測試變更

```bash
# 環境檢查
./scripts/check-env.sh

# Memory 驗證
./scripts/validate-memory.sh
```

### 提交規範

```
feat: 新功能
fix: 修復
docs: 文檔
refactor: 重構
chore: 雜項
```

## 相關資源

- [USAGE.md](./USAGE.md) - 詳細使用手冊
- [examples/](./examples/) - 使用範例
- [docs/](./docs/) - 延伸文檔
