---
date: 2026-01-11
tags: [architecture, atomic-design, skill-design, makepad-skills]
task: 從 makepad-skills 學習並改進 self-evolving-agent 架構
status: resolved
---

# 從 makepad-skills 學習原子化架構

## 情境

用戶發現了 https://github.com/ZhangHanDong/makepad-skills 這個 repo，想要借鏡其設計來改進 self-evolving-agent。

## 學習重點

### makepad-skills 的設計亮點

1. **原子化架構**
   - 將知識拆分成獨立模組（00-06 + 99）
   - 每個模組有 `_base/` 和 `community/` 分離
   - 官方更新不會覆蓋社群貢獻

2. **自我進化機制**
   - Self-Evolution: 累積 patterns
   - Self-Correction: 失敗時自動修正
   - Self-Validation: 驗證與框架版本相容
   - Personalization: 適應專案風格

3. **Hook 驅動觸發**
   - Pre-tool: 偵測版本
   - Post-failure: 識別錯誤
   - Session-end: 提示記錄學習

4. **一行安裝**
   - `curl | bash` 模式
   - 自動備份現有安裝

### 與 self-evolving-agent 的差異

| 面向 | makepad-skills | self-evolving-agent |
|------|----------------|---------------------|
| 領域 | Makepad 專用 | 領域無關通用框架 |
| 驅動 | Hook 驅動 | PDCA 循環驅動 |
| 進化 | 被動收集 | 主動涌現探索 |
| 路由 | 版本相容驗證 | 多階技能路由 |

## 實作的改進

1. **原子化改造** (v4.0.0)
   - 從 2027 行 SKILL.md 拆分成模組化結構
   - 7 個模組：00-getting-started 到 99-evolution
   - 每個模組有 _base/ 和 community/ 目錄

2. **一行安裝腳本**
   ```bash
   curl -fsSL .../install.sh | bash -s -- --with-hooks --with-memory
   ```

3. **Hook 整合**
   - PostToolUse: 提醒驗證變更
   - Stop: 提醒記錄學習

## 決定不採用的設計

- ❌ 版本相容性驗證（那是 Makepad 特定需求）
- ❌ 知識分類路由（我們有更完整的多階路由）

## 效果

- SKILL.md: 2027 → 191 行 (主入口)
- 模組化：11 個獨立 markdown 文件
- 社群貢獻：不會與官方更新衝突
- 安裝：一行命令完成

## 相關資源

- [makepad-skills](https://github.com/ZhangHanDong/makepad-skills)
- 原子化設計靈感來源
