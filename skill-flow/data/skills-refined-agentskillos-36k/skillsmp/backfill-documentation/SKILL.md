---
name: backfill-documentation
description: 當功能已實作完成但缺少設計文件和實作計劃時使用。根據現有程式碼和 git 歷史，自動生成符合 /hi-brainstorm 和 /hi-ace 格式的文件。
---

# 補充文件（Backfill Documentation）

## 概述

當功能已經實作完成，但沒有經過正式的設計流程時，使用此技能來補充文件。這確保所有功能都有完整的文件記錄，便於未來維護和理解。

**開始時宣布：** "我正在使用 backfill-documentation 技能來補充文件。"

**必要子技能：**
- 使用 hi-skills:brainstorming 的設計文件格式
- 使用 hi-skills:executing-plans 的實作計劃格式

## 流程

### 步驟 1：載入參考格式

**先調用技能取得格式規範：**
1. 調用 `Skill: brainstorming` - 取得設計文件的格式要求
2. 調用 `Skill: executing-plans` - 取得實作計劃的格式要求

### 步驟 2：收集資訊

1. **識別相關 commits**
   ```bash
   git log --oneline --since="YYYY-MM-DD" --grep="<關鍵字>"
   ```

2. **閱讀變更的檔案**
   - 從 git diff 或 git show 了解變更內容
   - 識別涉及的檔案和變更範圍

3. **理解功能**
   - 這個功能解決什麼問題？
   - 使用者體驗流程是什麼？
   - 資料如何流動？
   - 有哪些關鍵決策？

### 步驟 3：生成設計文件

**參照 brainstorming 技能格式**，建立 `docs/plans/YYYY-MM-DD-<topic>-design.md`：

必要元素（來自 brainstorming）：
1. **概述** - 功能目的和背景
2. **需求** - 明確的需求清單
3. **使用者體驗流程** - ASCII 流程圖
4. **資料流程** - 資料如何在系統中流動
5. **資料結構變更** - 新增或修改的型別/欄位
6. **UI 變更** - ASCII UI 圖（如適用）
7. **修改檔案清單** - 表格列出所有變更
8. **實作邏輯** - 關鍵程式碼片段
9. **驗收標準** - 所有項目標記為 `[x]` 已完成

### 步驟 4：生成實作計劃

**參照 executing-plans 技能格式**，建立 `docs/plans/YYYY-MM-DD-<topic>-plan.md`：

必要元素（來自 executing-plans）：
1. **狀態標記** - `> **狀態：** ✅ 已完成`
2. **目標和架構** - 簡短描述
3. **任務清單** - 每個任務標記 ✅，包含：
   - 檔案清單
   - 完成內容
4. **變更摘要** - 影響檔案和風險等級 🟢
5. **相關 Commits** - 列出相關的 git commits

### 步驟 5：建立索引檔

建立 `~/.claude/plans/YYYY-MM-DD-<project>-<topic>.md`：

```markdown
# <project>-<topic>

project_path: <專案路徑>
status: done
design_file: docs/plans/YYYY-MM-DD-<topic>-design.md
plan_file: docs/plans/YYYY-MM-DD-<topic>-plan.md
```

### 步驟 6：更新索引

執行 `/hi-update-plans-index` 更新計畫索引。

### 步驟 7：提交文件

```bash
git add docs/plans/
git commit -m "docs: 補充 <功能名稱> 的設計與實作計劃文件

- 新增 <topic>-design.md（設計文件）
- 新增 <topic>-plan.md（實作計劃，已完成）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## 設計文件範本

參照 `/hi-brainstorm` 輸出格式：

```markdown
# <功能名稱>設計

## 概述

<簡短描述功能目的和解決的問題>

## 需求

1. <需求 1>
2. <需求 2>
3. ...

## 使用者體驗流程

```
┌─────────────────────────────────────────────────────────┐
│ <流程步驟>                                               │
├─────────────────────────────────────────────────────────┤
│  <UI 元素描述>                                           │
└─────────────────────────────────────────────────────────┘
```

## 資料流程

```
<步驟描述>
       ↓
┌──────────────────────────────────────────────────────┐
│ <元件/系統名稱>                                       │
│                                                      │
│ 1. <動作 1>                                          │
│ 2. <動作 2>                                          │
└──────────────────────────────────────────────────────┘
```

## 資料結構變更

### <collection/type 名稱>

```typescript
{
  existingField: string;
  newField: string;  // 新增：說明
}
```

## UI 變更

<ASCII UI 圖>

## 修改檔案清單

| 檔案 | 變更內容 |
|-----|---------|
| `path/to/file.ts` | <變更描述> |

## 實作邏輯

```typescript
// 關鍵程式碼片段（說明核心邏輯）
```

## 驗收標準

- [x] <標準 1>
- [x] <標準 2>
```

## 實作計劃範本

參照 `/hi-ace` 輸出格式：

```markdown
# <功能名稱> 實作計劃

> **狀態：** ✅ 已完成

**目標：** <功能目標>

**架構：** <技術架構簡述>

**技術棧：** <使用的技術>

---

### 任務 1：<任務名稱> ✅

**檔案：**
- 修改：`path/to/file.ts`

**完成內容：**
- <完成的項目 1>
- <完成的項目 2>

---

### 任務 2：<任務名稱> ✅

...

---

## 變更摘要

**影響檔案：**
- `file1.ts` - <變更描述>
- `file2.ts` - <變更描述>

**整體風險：** 🟢（已完成，無問題）

**相關 Commits：**
- `<commit message 1>`
- `<commit message 2>`
```

## 記住

- **必須參照子技能** - 先調用 brainstorming 和 executing-plans 確認最新格式
- 從現有程式碼反推設計，不是編造
- 所有驗收標準標記為已完成（因為功能已實作）
- 實作計劃的任務從 git commits 推斷
- 確保文件能幫助未來的開發者理解功能
- 使用一致的格式和命名規則
