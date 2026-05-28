---
date: 2026-01-12
tags: [makefile, automation, explore-mode, level-1, changelog, memory-stats]
task: 優化 Makefile 並探索其他自動化機會
status: resolved
level: 1 (探索模式)
---

# Makefile 優化 + 探索模式發現

## 情境

使用 `/evolve --explore` 執行 Level 1 任務：優化 Makefile，整合 changelog 生成腳本。

## 主要任務

### 整合 changelog 腳本

將 `scripts/generate-changelog.sh` 整合到 Makefile：

```makefile
changelog: ## Generate CHANGELOG.md (preview mode)
	@./scripts/generate-changelog.sh --preview

changelog-save: ## Generate and save CHANGELOG.md
	@./scripts/generate-changelog.sh --all --output CHANGELOG.md

changelog-since: ## Generate changelog since a tag
	# make changelog-since TAG=v4.1.0
```

## 探索模式發現（Level 1 涌現）

完成主要任務後，**主動發現**並實作了額外的自動化機會：

### Memory 管理命令

```makefile
memory-stats: ## Show memory system statistics
	# 顯示各類記憶檔案數量
	# 顯示 index.md 狀態

memory-recent: ## Show recently modified memory files
	# 列出最近 7 天修改的記憶文件
```

### 效益

| 命令 | 用途 | 決策減少 |
|------|------|----------|
| `make changelog` | 快速預覽變更記錄 | 不用記 script 參數 |
| `make memory-stats` | 一覽記憶系統狀態 | 不用手動統計 |
| `make memory-recent` | 追蹤最近活動 | 不用寫 find 命令 |

## 學習重點

### 1. Level 1 探索模式的價值

> 完成任務後「探索」帶來額外發現

- 主要任務：整合 changelog ✅
- 涌現發現：memory-stats, memory-recent 命令
- **關鍵**：探索模式讓 AI 主動尋找「還能做什麼」

### 2. Makefile 設計原則

```
自動化 = 減少決策點 + 減少重複勞動
```

- 用 `make` 統一所有常用操作
- 用 `##` 註解自動生成 help
- 提供 preview 模式避免誤操作

## 驗證

```
✅ make help - 顯示所有命令（含新增）
✅ make changelog - 正確調用腳本
✅ make memory-stats - 正確統計數量
✅ make memory-recent - 正確顯示最近文件
✅ make recent - 替代原 changelog 快速檢視
```

## 效果

首次 Level 1 探索模式：
- 主要任務完成：1 項
- 涌現發現：2 個額外自動化命令
- 這證明 `--explore` flag 確實能促進額外發現
